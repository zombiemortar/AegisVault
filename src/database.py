import sqlite3
import os
from encryption import encrypt_data, decrypt_data
import json

DB_PATH = os.path.join("data", "passwords.db")  # ✅ Updated location
DATABASE_FILE = "../data/passwords.db"

def init_db():
    """Initializes the password storage database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY,
            website TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_account (
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            username TEXT PRIMARY KEY,
            session_timeout INTEGER DEFAULT 300,
            lock_on_tab_inactive BOOLEAN DEFAULT 1,
            lock_on_suspicious_activity BOOLEAN DEFAULT 1,
            auto_lock_enabled BOOLEAN DEFAULT 1,
            lock_on_window_blur BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Run migrations to add new columns to existing tables
    run_migrations(cursor)
    
    conn.commit()
    conn.close()

def run_migrations(cursor):
    """Run database migrations to update schema."""
    try:
        # Check if lock_on_window_blur column exists
        cursor.execute("PRAGMA table_info(user_preferences)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add lock_on_window_blur column if it doesn't exist
        if 'lock_on_window_blur' not in columns:
            print("🔧 Adding lock_on_window_blur column to user_preferences table...")
            cursor.execute("""
                ALTER TABLE user_preferences 
                ADD COLUMN lock_on_window_blur BOOLEAN DEFAULT 1
            """)
            print("✅ Migration completed: lock_on_window_blur column added")
        
    except sqlite3.Error as e:
        print(f"⚠️ Migration error: {e}")
        # Continue execution even if migration fails

def get_connection():
    """Establishes connection to the database."""
    return sqlite3.connect(DB_PATH)

def store_master_account(username, encrypted_password):
    """Updates the master account password for the given username."""
    conn = sqlite3.connect("../data/passwords.db")
    cursor = conn.cursor()

    try:
        # Debug: Check if the username exists
        cursor.execute("SELECT username FROM master_account WHERE username = ?", (username,))
        if cursor.fetchone():
            # Update the password
            cursor.execute(
                "UPDATE master_account SET password = ? WHERE username = ?",
                (encrypted_password, username)
            )
            print(f"DEBUG: Password updated for username: {username}")
        else:
            print(f"ERROR: Username {username} not found in the database.")
            raise ValueError("Username not found.")

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        conn.close()


def load_master_account():
    """Retrieves and decrypts master account credentials."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM master_account")
    row = cursor.fetchone()
    conn.close()
    if row:
        return decrypt_data(row[0]), decrypt_data(row[1])
    return None, None

def store_password(website, username, password):
    """Stores encrypted credentials but keeps website URLs plaintext."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO credentials (website, username, password) VALUES (?, ?, ?)",
                   (website, encrypt_data(username), encrypt_data(password)))  # ✅ Website remains unchanged
    conn.commit()
    conn.close()


def retrieve_password(website):
    """Retrieves username and password for a given plaintext website."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT username, password FROM credentials WHERE website = ?",
                   (website,))  # ✅ No encryption on lookup
    row = cursor.fetchone()
    conn.close()

    if row:
        return decrypt_data(row[0]), decrypt_data(row[1])  # ✅ Decrypt only username & password

    print("❌ No stored credentials found for that website.")
    return None, None


def delete_password(website):
    """Deletes stored credentials for a given website."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    print(f"🔎 Checking for existing website before deletion: {website}")  # Debug

    cursor.execute("SELECT username FROM credentials WHERE website = ?", (website,))
    row = cursor.fetchone()

    if row:
        cursor.execute("DELETE FROM credentials WHERE website = ?", (website,))
        conn.commit()
        print(f"✅ Credentials for {website} successfully removed.")  # Debug
    else:
        print("❌ No matching credentials found for deletion.")

    conn.close()

def get_user_preferences(username):
    """Get user preferences for auto-lock and other settings."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check if preferences exist for this user
    cursor.execute("SELECT * FROM user_preferences WHERE username = ?", (username,))
    preferences = cursor.fetchone()
    
    if not preferences:
        # Initialize default preferences
        cursor.execute("""
            INSERT INTO user_preferences (username, session_timeout, lock_on_tab_inactive, 
                                        lock_on_suspicious_activity, auto_lock_enabled, lock_on_window_blur)
            VALUES (?, 300, 1, 1, 1, 1)
        """, (username,))
        conn.commit()
        
        # Fetch the newly created preferences
        cursor.execute("SELECT * FROM user_preferences WHERE username = ?", (username,))
        preferences = cursor.fetchone()
    
    conn.close()
    
    if preferences:
        # Handle different column counts (for backward compatibility)
        if len(preferences) >= 8:  # New schema with lock_on_window_blur
            return {
                'username': preferences[0],
                'session_timeout': preferences[1],
                'lock_on_tab_inactive': bool(preferences[2]),
                'lock_on_suspicious_activity': bool(preferences[3]),
                'auto_lock_enabled': bool(preferences[4]),
                'lock_on_window_blur': bool(preferences[5]),
                'created_at': preferences[6],
                'updated_at': preferences[7]
            }
        else:  # Old schema without lock_on_window_blur
            return {
                'username': preferences[0],
                'session_timeout': preferences[1],
                'lock_on_tab_inactive': bool(preferences[2]),
                'lock_on_suspicious_activity': bool(preferences[3]),
                'auto_lock_enabled': bool(preferences[4]),
                'lock_on_window_blur': True,  # Default to True for backward compatibility
                'created_at': preferences[5] if len(preferences) > 5 else None,
                'updated_at': preferences[6] if len(preferences) > 6 else None
            }
    return None

def update_user_preferences(username, **kwargs):
    """Update user preferences."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Build update query dynamically
    update_fields = []
    values = []
    
    for field, value in kwargs.items():
        if field in ['session_timeout', 'lock_on_tab_inactive', 'lock_on_suspicious_activity', 'auto_lock_enabled', 'lock_on_window_blur']:
            update_fields.append(f"{field} = ?")
            values.append(value)
    
    if update_fields:
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        query = f"UPDATE user_preferences SET {', '.join(update_fields)} WHERE username = ?"
        values.append(username)
        
        cursor.execute(query, values)
        conn.commit()
    
    conn.close()

def initialize_user_preferences(username):
    """Initialize default preferences for a new user."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Run migrations first to ensure table structure is up to date
    run_migrations(cursor)
    
    cursor.execute("""
        INSERT OR IGNORE INTO user_preferences (username, session_timeout, lock_on_tab_inactive, 
                                              lock_on_suspicious_activity, auto_lock_enabled, lock_on_window_blur)
        VALUES (?, 300, 1, 1, 1, 1)
    """, (username,))
    
    conn.commit()
    conn.close()

def update_password(website, new_password):
    """Updates stored password for a given website."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    print(f"🔎 Checking for existing website: {website}")  # Debug

    cursor.execute("SELECT password FROM credentials WHERE website = ?", (website,))
    row = cursor.fetchone()

    if row:
        cursor.execute("UPDATE credentials SET password = ? WHERE website = ?",
                       (encrypt_data(new_password), website))
        conn.commit()
        print(f"✅ Password for {website} updated successfully.")  # Debug
    else:
        print("❌ No matching credentials found for update.")

    conn.close()

def get_all_stored_urls():
    """Retrieves all stored website URLs."""
    conn = sqlite3.connect("../data/passwords.db")
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT website FROM credentials")
    urls = [row[0] for row in cursor.fetchall()]

    conn.close()
    return urls  # ✅ Returns a list of stored URLs

def get_total_stored_passwords():
    """Retrieves the total number of stored passwords in the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM credentials")  # ✅ Ensure correct table name
    total = cursor.fetchone()[0]  # ✅ Extract count value

    conn.close()
    return total

def get_all_credentials():
    """Fetches all stored passwords."""
    conn = sqlite3.connect("../data/passwords.db")
    cursor = conn.cursor()

    cursor.execute("SELECT website, username, password FROM credentials")
    credentials = [
        {
            "website": row[0],
            "username": decrypt_data(row[1]),  # 🔓 Ensure proper decryption
            "password": decrypt_data(row[2])  # 🔓 Ensure plaintext display
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return credentials


def export_database():
    """Creates a decrypted JSON backup of all stored credentials."""
    credentials = get_all_credentials()  # 🔓 Already decrypting usernames & passwords

    backup_dir = "../backup"
    os.makedirs(backup_dir, exist_ok=True)  # ✅ Ensure the folder exists

    backup_path = os.path.join(backup_dir, "AegisVault_Backup.json")

    with open(backup_path, "w") as backup_file:
        json.dump(credentials, backup_file, indent=4)  # ✅ Save decrypted version

    return backup_path  # ✅ Path for Flask to serve

