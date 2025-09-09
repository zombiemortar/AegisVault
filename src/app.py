import json
import traceback
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_file
import sqlite3
from encryption import encrypt_data, decrypt_data  # ✅ Import encryption functions
from session import session_expire_event, SessionManager  # ✅ Import session expiration event
from database import init_db, store_master_account, load_master_account, store_password, get_total_stored_passwords, update_password, delete_password, export_database, get_user_preferences, update_user_preferences, initialize_user_preferences, get_connection
from password_strength import PasswordStrengthAnalyzer
from password_generator import PasswordGenerator

# 🔒 Flask app setup
app = Flask(__name__)
app.secret_key = "supersecurekey"  # ✅ Replace with a strong, secure key
session_manager = SessionManager()  # 🔥 Create an instance
password_analyzer = PasswordStrengthAnalyzer()  # 🔐 Password strength analyzer
password_generator = PasswordGenerator()  # 🔐 Password generator
init_db()

# Encryption key is handled by encryption.py module
# No need to manually load it here


def get_db_connection():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

def user_exists(username):
    """ Check if the username already exists in the database. """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists



@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        users = conn.execute("SELECT * FROM master_account").fetchall()
        conn.close()

        for user in users:
            decrypted_username = decrypt_data(user["username"])
            decrypted_password = decrypt_data(user["password"])

            if decrypted_username == username and decrypted_password == password:
                print(f"DEBUG: Login successful for {username}")

                session["user_id"] = username
                session.permanent = True

                # Initialize user preferences if they don't exist
                initialize_user_preferences(username)
                
                session_manager.start_session(username)  # 🔥 Starts tracking session expiration
                return redirect("/dashboard")  # ✅ Redirect on success

            print("DEBUG: Password incorrect")

        print("DEBUG: User not found")
        return render_template("login.html", error="Invalid credentials!")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    username= session.get("user_id", "Guest")  # 🔒 Retrieves user ID from session
    print(f"DEBUG: Checking session expiration flag (Flask) → {session_expire_event.is_set()}")  # 🔎 Logs flag state
    total_passwords = get_total_stored_passwords()

    if "user_id" not in session or session_expire_event.is_set():  # ✅ Checks timeout flag properly
        print("DEBUG: Session expired. Redirecting back to login.")
        session.clear()  # 🔒 Removes user session
        return redirect("/")  # 🔄 Forces relogin

    return render_template("dashboard.html", username=username, total_passwords=total_passwords)  # ✅ Passes username to template


@app.route("/logout")
def logout():
    session.clear()  # 🔒 Clears user session
    return redirect("/")  # ✅ Redirects back to login page

# API endpoints for auto-lock features
@app.route("/api/preferences", methods=["GET"])
def get_preferences():
    """Get user preferences for auto-lock settings."""
    if "user_id" not in session:
        return {"error": "Not authenticated"}, 401
    
    username = session["user_id"]
    preferences = get_user_preferences(username)
    
    if preferences:
        return preferences
    else:
        return {"error": "Preferences not found"}, 404

@app.route("/api/preferences", methods=["POST"])
def update_preferences():
    """Update user preferences for auto-lock settings."""
    if "user_id" not in session:
        return {"error": "Not authenticated"}, 401
    
    username = session["user_id"]
    data = request.get_json()
    
    if not data:
        return {"error": "No data provided"}, 400
    
    try:
        update_user_preferences(username, **data)
        
        # Update session manager timeout if session_timeout changed
        if 'session_timeout' in data:
            session_manager.update_timeout(data['session_timeout'])
        
        return {"message": "Preferences updated successfully"}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/api/session/status", methods=["GET"])
def session_status():
    """Get current session status."""
    if "user_id" not in session:
        return {"active": False, "remaining_time": 0}
    
    username = session["user_id"]
    remaining_time = session_manager.get_remaining_time()
    
    return {
        "active": session_manager.active,
        "remaining_time": remaining_time,
        "username": username
    }

@app.route("/api/session/refresh", methods=["POST"])
def refresh_session():
    """Refresh the current session."""
    if "user_id" not in session:
        return {"error": "Not authenticated"}, 401
    
    session_manager.refresh_session()
    return {"message": "Session refreshed successfully"}

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # ✅ Ensure passwords match
        if password != confirm_password:
            flash("Passwords do not match. Please try again!", "error")
            return redirect(url_for("create_account"))

        # ✅ Check if username already exists
        conn = get_db_connection()  # 🔒 Correct database path
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM master_account WHERE username = ?", (username,))
        exists = cursor.fetchone() is not None

        if exists:
            conn.close()
            flash("Username already taken. Please choose another one!", "error")
            return redirect(url_for("create_account"))

        # ✅ Encrypt password before storing
        encrypted_username = encrypt_data(username)
        print(f"🔎 DEBUG: Encrypted Username → {encrypted_username}")
        encrypted_password = encrypt_data(password)
        print(f"🔎 DEBUG: Encrypted Password → {encrypted_password}")  # ✅ Verify encryption output

        # ✅ Store new user in the database
        cursor.execute("INSERT INTO master_account (username, password) VALUES (?, ?)", (encrypted_username, encrypted_password))
        conn.commit()
        conn.close()

        print(f"✅ DEBUG: Stored {username} in users table")  # 🔥 Confirms successful insertion

        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("login"))  # ✅ Redirect to login page

    return render_template("create_account.html")


@app.route("/vault")
def vault():
    """Fetch stored credentials and decrypt passwords before displaying."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT website, username, password FROM credentials WHERE deleted_at IS NULL")
    credentials = [
        {
            "website": row[0],
            "username": decrypt_data(row[1]),  # ✅ Just decrypt, no encryption needed
            "password": decrypt_data(row[2])   # ✅ Ensure plaintext display
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return render_template("vault.html", credentials=credentials)

@app.route("/update_password", methods=["POST"])
def update_password_route():
    """Updates stored password securely."""
    data = request.get_json()
    website = data["website"]
    new_password = data["new_password"]  # ✅ Keep plaintext; database.py encrypts automatically

    update_password(website, new_password)  # 🔒 Database will handle encryption
    return {"status": "success"}, 200

@app.route("/delete_password", methods=["POST"])
def delete_password_route():
    """Deletes stored credentials."""
    data = request.get_json()
    website = data["website"]

    delete_password(website)
    return {"status": "success"}, 200

@app.route("/settings")
def settings():
    return render_template("settings.html")  # ✅ Ensures it points to a valid template

@app.route("/add_password", methods=["GET", "POST"])
def add_password():
    if request.method == "POST":
        print(f"🔎 DEBUG: Incoming Form Data → {request.form}")  # ✅ Print received request data

        # Ensure we receive expected fields
        if "website" not in request.form:
            flash("Error: Website field is missing!", "danger")
            return redirect(url_for("add_password"))

        website = request.form["website"]
        username = request.form["username"]
        password = request.form["password"]

        store_password(website, username, password)

        flash("Password saved successfully!", "success")
        return redirect(url_for("vault"))

    return render_template("add_password.html")


@app.route('/change_password', methods=['POST'])
def change_password():
    """Handles password change for the master account."""
    # Load the current master account credentials
    username, stored_password = load_master_account()
    print(f"DEBUG: Current Username: {username}, Stored Password: {stored_password}")

    # Retrieve new password inputs from the form
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    print(f"DEBUG: New Password: {new_password}, Confirm Password: {confirm_password}")

    # Validate that the new passwords match
    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for('settings'))

    # Encrypt the new password
    encrypted_new_password = encrypt_data(new_password)
    print(f"DEBUG: Encrypted New Password: {encrypted_new_password}")

    try:
        # Update the master account password in the database
        store_master_account(username, encrypted_new_password)
        flash("Password updated securely!", "success")
    except Exception as e:
        print(f"ERROR: Failed to update password: {e}")
        flash("Failed to update password.", "danger")

    return redirect(url_for('settings'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = session.get('user_id')  # 🔒 Get the logged-in user's ID

    if not user_id:
        flash("Error: No user logged in.", "danger")
        return redirect(url_for('settings'))

    try:
        conn = get_db_connection()  # ✅ Get a proper DB connection
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE username = ?", (user_id,))  # 🔄 Ensure field matches schema
        conn.commit()
        conn.close()

        session.clear()  # 🚀 Log user out after deletion
        flash("Your account has been successfully deleted.", "success")
        return redirect(url_for('create_account'))  # 🔄 Redirect to account creation

    except Exception as e:
        flash(f"Error deleting account: {str(e)}", "danger")
        return redirect(url_for('settings'))

@app.route("/export_backup")
def export_backup():
    """Serves the encrypted database backup as a downloadable file."""
    backup_path = export_database()  # 🔄 Generate backup before serving
    return send_file(backup_path, as_attachment=True)


@app.route('/import_backup', methods=['POST'])
def import_backup():
    """Handles restoring passwords from a previously exported JSON file."""
    uploaded_file = request.files.get('backup_file')

    if not uploaded_file or uploaded_file.filename == '':
        flash("No file selected. Please upload a valid JSON file.", "danger")
        session.modified = True  # 🔄 Ensure session updates to display messages
        return redirect(url_for('settings'))

    try:
        # ✅ Load JSON data
        backup_data = json.load(uploaded_file)
        print(f"DEBUG: Backup Data Loaded → {backup_data}")  # 🔎 Verify JSON structure

        # 🔥 Pass each entry directly to `store_password()`
        for entry in backup_data:
            store_password(entry["website"], entry["username"], entry["password"])
            print(f"✅ Stored: {entry['website']} | {entry['username']} | {entry['password']}")  # Debugging output

        flash("Backup imported successfully!", "success")
        session.modified = True  # 🔄 Ensure flash messages persist

    except json.JSONDecodeError as json_err:
        flash(f"Invalid JSON format: {json_err}", "danger")
        print(f"❌ JSON Parsing Error: {json_err}")  # 🔎 Debugging output

    except Exception as e:
        flash(f"Unexpected error: {str(e)}", "danger")
        print(f"❌ General Error: {str(e)}")  # 🔎 Debugging output

    return redirect(url_for('settings'))

@app.route('/analyze_password', methods=['POST'])
def analyze_password():
    """Analyzes password strength and returns analysis data."""
    if "user_id" not in session:
        return {"error": "Not authenticated"}, 401
        
    data = request.get_json()
    password = data.get('password', '')
    
    analysis = password_analyzer.analyze_password(password)
    return analysis

@app.route('/password_stats', methods=['GET'])
def get_password_stats():
    """Gets password strength statistics for dashboard."""
    if "user_id" not in session:
        return {"error": "Not authenticated"}, 401
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM credentials WHERE deleted_at IS NULL")
        passwords = cursor.fetchall()
        conn.close()
        
        if not passwords:
            return {"total": 0, "strength_distribution": {}, "average_entropy": 0}
        
        # Analyze all passwords
        strength_counts = {"Very Strong": 0, "Strong": 0, "Moderate": 0, "Weak": 0, "Very Weak": 0}
        total_entropy = 0
        
        for row in passwords:
            decrypted_password = decrypt_data(row[0])
            analysis = password_analyzer.analyze_password(decrypted_password)
            strength_counts[analysis['strength_level']] += 1
            total_entropy += analysis['entropy']
        
        average_entropy = round(total_entropy / len(passwords), 2)
        
        return {
            "total": len(passwords),
            "strength_distribution": strength_counts,
            "average_entropy": average_entropy
        }
        
    except Exception as e:
        print(f"Error getting password stats: {e}")
        return {"error": "Failed to get password statistics"}, 500

@app.route('/generate_password', methods=['POST'])
def generate_password():
    """Generates a secure password based on user preferences."""
    if "user_id" not in session:
        return {"error": "Not authenticated"}, 401
        
    try:
        data = request.get_json()
        
        # Get generation options from request
        length = data.get('length', 16)
        include_lowercase = data.get('include_lowercase', True)
        include_uppercase = data.get('include_uppercase', True)
        include_digits = data.get('include_digits', True)
        include_symbols = data.get('include_symbols', True)
        avoid_similar = data.get('avoid_similar', True)
        avoid_ambiguous = data.get('avoid_ambiguous', True)
        generator_type = data.get('type', 'random')  # 'random', 'memorable', 'pronounceable'
        
        # Validate options
        options = {
            'length': length,
            'include_lowercase': include_lowercase,
            'include_uppercase': include_uppercase,
            'include_digits': include_digits,
            'include_symbols': include_symbols,
            'avoid_similar': avoid_similar,
            'avoid_ambiguous': avoid_ambiguous
        }
        
        validation_errors = password_generator.validate_options(options)
        if validation_errors:
            return {"error": validation_errors[0]}, 400
        
        # Generate password based on type
        if generator_type == 'memorable':
            word_count = data.get('word_count', 4)
            separator = data.get('separator', '-')
            include_numbers = data.get('include_numbers', True)
            include_symbols = data.get('include_symbols', True)
            password = password_generator.generate_memorable_password(
                word_count=word_count,
                separator=separator,
                include_numbers=include_numbers,
                include_symbols=include_symbols
            )
        elif generator_type == 'pronounceable':
            include_numbers = data.get('include_numbers', True)
            include_symbols = data.get('include_symbols', True)
            password = password_generator.generate_pronounceable_password(
                length=length,
                include_numbers=include_numbers,
                include_symbols=include_symbols
            )
        else:  # random
            password = password_generator.generate_password(
                length=length,
                include_lowercase=include_lowercase,
                include_uppercase=include_uppercase,
                include_digits=include_digits,
                include_symbols=include_symbols,
                avoid_similar=avoid_similar,
                avoid_ambiguous=avoid_ambiguous
            )
        
        # Get strength information for the generated password
        strength_info = password_generator.get_password_strength_info(password)
        
        return {
            "password": password,
            "strength_info": strength_info,
            "options": options
        }
        
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        print(f"Error generating password: {e}")
        return {"error": "Failed to generate password"}, 500

@app.route('/get_generator_options', methods=['GET'])
def get_generator_options():
    """Gets default generator options."""
    if "user_id" not in session:
        return {"error": "Not authenticated"}, 401
        
    try:
        options = password_generator.get_generator_options()
        return options
    except Exception as e:
        print(f"Error getting generator options: {e}")
        return {"error": "Failed to get generator options"}, 500

if __name__ == "__main__":
    app.run(debug=True)