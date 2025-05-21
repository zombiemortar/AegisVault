from flask import Flask, render_template, request, redirect, session, url_for, flash, send_file
import sqlite3
from encryption import encrypt_data, decrypt_data  # ✅ Import encryption functions
from session import session_expire_event, SessionManager  # ✅ Import session expiration event
from database import init_db, store_master_account, load_master_account, store_password, get_total_stored_passwords, update_password, delete_password, export_database

# 🔒 Flask app setup
app = Flask(__name__)
app.secret_key = "supersecurekey"  # ✅ Replace with a strong, secure key
session_manager = SessionManager()  # 🔥 Create an instance
init_db()

with open("../src/encryption_key.key", "rb") as f:
    key = f.read()
    print(f"🔎 Encryption Key: {key}")


def get_db_connection():
    conn = sqlite3.connect("../data/passwords.db")  # ✅ Correct database path
    conn.row_factory = sqlite3.Row
    return conn

def user_exists(username):
    """ Check if the username already exists in the database. """
    conn = sqlite3.connect("../data/passwords.db")
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
        conn = sqlite3.connect("../data/passwords.db")  # 🔒 Correct database path
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
    conn = sqlite3.connect("../data/passwords.db")
    cursor = conn.cursor()

    cursor.execute("SELECT website, username, password FROM credentials")
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

    # 🔥 Remove user from database (ensure this fits your schema)
    try:
        db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()
        session.clear()  # 🚀 Log user out after deletion
        flash("Your account has been successfully deleted.", "success")
        return redirect(url_for('create_account'))  # Redirect to signup after deletion
    except Exception as e:
        flash(f"Error deleting account: {str(e)}", "danger")
        return redirect(url_for('settings'))

@app.route("/export_backup")
def export_backup():
    """Serves the encrypted database backup as a downloadable file."""
    backup_path = export_database()  # 🔄 Generate backup before serving
    return send_file(backup_path, as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)