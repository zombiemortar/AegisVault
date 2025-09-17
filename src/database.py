import sqlite3
import os
import sys
from encryption import encrypt_data, decrypt_data
import json
from datetime import datetime

def get_app_data_dir():
    """Get the appropriate data directory for the application."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        if sys.platform == 'win32':
            # Windows: Use AppData\Roaming\AegisVault
            app_data = os.path.join(os.environ.get('APPDATA', ''), 'AegisVault')
        elif sys.platform == 'darwin':
            # macOS: Use ~/Library/Application Support/AegisVault
            app_data = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'AegisVault')
        else:
            # Linux: Use ~/.local/share/AegisVault
            app_data = os.path.join(os.path.expanduser('~'), '.local', 'share', 'AegisVault')
    else:
        # Running as script - use relative path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        app_data = os.path.normpath(os.path.join(BASE_DIR, "..", "data"))
    
    # Create directory if it doesn't exist
    os.makedirs(app_data, exist_ok=True)
    return app_data

# Get the database file path
DATA_DIR = get_app_data_dir()
DATABASE_FILE = os.path.join(DATA_DIR, "passwords.db")

def init_db():
    """Initializes the password storage database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY,
                website TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                action_type TEXT NOT NULL,
                action_description TEXT NOT NULL,
                target_resource TEXT,
                ip_address TEXT,
                user_agent TEXT,
                success BOOLEAN DEFAULT 1,
                error_message TEXT,
                session_id TEXT,
                additional_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Run migrations to add new columns to existing tables
        run_migrations(cursor)
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error during init_db: {e}")
        raise
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def run_migrations(cursor):
    """Run database migrations to update schema."""
    try:
        # Migrate user_preferences: add lock_on_window_blur if missing
        cursor.execute("PRAGMA table_info(user_preferences)")
        up_columns = [column[1] for column in cursor.fetchall()]
        if 'lock_on_window_blur' not in up_columns:
            print("🔧 Adding lock_on_window_blur column to user_preferences table...")
            cursor.execute(
                """
                ALTER TABLE user_preferences 
                ADD COLUMN lock_on_window_blur BOOLEAN DEFAULT 1
                """
            )
            print("✅ Migration completed: lock_on_window_blur column added")

        # Migrate credentials: add timestamps and soft-delete if missing
        cursor.execute("PRAGMA table_info(credentials)")
        cred_columns = [column[1] for column in cursor.fetchall()]
        if 'created_at' not in cred_columns:
            print("🔧 Adding created_at to credentials...")
            cursor.execute("ALTER TABLE credentials ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        if 'updated_at' not in cred_columns:
            print("🔧 Adding updated_at to credentials...")
            cursor.execute("ALTER TABLE credentials ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        if 'deleted_at' not in cred_columns:
            print("🔧 Adding deleted_at to credentials (for soft deletes)...")
            cursor.execute("ALTER TABLE credentials ADD COLUMN deleted_at TIMESTAMP")

        # Indexes for better performance
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_credentials_website ON credentials(website)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_credentials_deleted_at ON credentials(deleted_at)"
        )
        # Partial index for active (not deleted) credentials if supported
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_credentials_website_active ON credentials(website) WHERE deleted_at IS NULL"
        )
        
        # Audit logs indexes for better performance
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_logs_username ON audit_logs(username)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_logs_action_type ON audit_logs(action_type)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_logs_success ON audit_logs(success)"
        )
        
    except sqlite3.Error as e:
        print(f"⚠️ Migration error: {e}")
        # Continue execution even if migration fails

def get_connection():
    """Establishes connection to the database using the canonical path."""
    return sqlite3.connect(DATABASE_FILE)

def store_master_account(username, encrypted_password):
    """Updates the master account password for the given username."""
    conn = sqlite3.connect(DATABASE_FILE)
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
    # Use UPSERT to update existing row while keeping created_at and clearing soft-delete
    cursor.execute(
        """
        INSERT INTO credentials (website, username, password)
        VALUES (?, ?, ?)
        ON CONFLICT(website) DO UPDATE SET
            username = excluded.username,
            password = excluded.password,
            updated_at = CURRENT_TIMESTAMP,
            deleted_at = NULL
        """,
        (website, encrypt_data(username), encrypt_data(password))
    )  # ✅ Website remains unchanged
    conn.commit()
    conn.close()


def retrieve_password(website):
    """Retrieves username and password for a given plaintext website."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, password FROM credentials WHERE website = ? AND deleted_at IS NULL",
        (website,)
    )  # ✅ No encryption on lookup
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

    cursor.execute("SELECT username FROM credentials WHERE website = ? AND deleted_at IS NULL", (website,))
    row = cursor.fetchone()

    if row:
        # Soft delete: mark as deleted instead of removing the row
        cursor.execute(
            "UPDATE credentials SET deleted_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP WHERE website = ?",
            (website,)
        )
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

    cursor.execute("SELECT password FROM credentials WHERE website = ? AND deleted_at IS NULL", (website,))
    row = cursor.fetchone()

    if row:
        cursor.execute(
            "UPDATE credentials SET password = ?, updated_at = CURRENT_TIMESTAMP WHERE website = ?",
            (encrypt_data(new_password), website)
        )
        conn.commit()
        print(f"✅ Password for {website} updated successfully.")  # Debug
    else:
        print("❌ No matching credentials found for update.")

    conn.close()

def get_all_stored_urls():
    """Retrieves all stored website URLs."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT website FROM credentials")
    urls = [row[0] for row in cursor.fetchall()]

    conn.close()
    return urls  # ✅ Returns a list of stored URLs

def get_total_stored_passwords():
    """Retrieves the total number of stored passwords in the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM credentials WHERE deleted_at IS NULL")  # ✅ Ensure only active
    total = cursor.fetchone()[0]  # ✅ Extract count value

    conn.close()
    return total

def get_all_credentials():
    """Fetches all stored passwords."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT website, username, password FROM credentials WHERE deleted_at IS NULL")
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

# Audit Logging Functions
def log_audit_event(username, action_type, action_description, target_resource=None, 
                   ip_address=None, user_agent=None, success=True, error_message=None, 
                   session_id=None, additional_data=None):
    """Log an audit event to the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO audit_logs (username, action_type, action_description, target_resource,
                                  ip_address, user_agent, success, error_message, session_id, additional_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, action_type, action_description, target_resource, ip_address, 
              user_agent, success, error_message, session_id, additional_data))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error logging audit event: {e}")
    finally:
        conn.close()

def get_audit_logs(username=None, action_type=None, limit=100, offset=0, 
                  start_date=None, end_date=None, success_only=None):
    """Retrieve audit logs with optional filtering."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Build query with filters
    query = "SELECT * FROM audit_logs WHERE 1=1"
    params = []
    
    if username:
        query += " AND username = ?"
        params.append(username)
    
    if action_type:
        query += " AND action_type = ?"
        params.append(action_type)
    
    if start_date:
        query += " AND created_at >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND created_at <= ?"
        params.append(end_date)
    
    if success_only is not None:
        query += " AND success = ?"
        params.append(success_only)
    
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    try:
        cursor.execute(query, params)
        logs = cursor.fetchall()
        
        # Convert to list of dictionaries
        columns = [description[0] for description in cursor.description]
        result = []
        for row in logs:
            log_dict = dict(zip(columns, row))
            result.append(log_dict)
        
        return result
    except sqlite3.Error as e:
        print(f"Error retrieving audit logs: {e}")
        return []
    finally:
        conn.close()

def get_audit_log_stats(username=None, days=30):
    """Get audit log statistics for a user."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        # Get total events
        query = "SELECT COUNT(*) FROM audit_logs WHERE created_at >= datetime('now', '-{} days')".format(days)
        params = []
        
        if username:
            query += " AND username = ?"
            params.append(username)
        
        cursor.execute(query, params)
        total_events = cursor.fetchone()[0]
        
        # Get events by type
        query = "SELECT action_type, COUNT(*) FROM audit_logs WHERE created_at >= datetime('now', '-{} days')".format(days)
        if username:
            query += " AND username = ?"
        query += " GROUP BY action_type"
        
        cursor.execute(query, params)
        events_by_type = dict(cursor.fetchall())
        
        # Get success/failure ratio
        query = "SELECT success, COUNT(*) FROM audit_logs WHERE created_at >= datetime('now', '-{} days')".format(days)
        if username:
            query += " AND username = ?"
        query += " GROUP BY success"
        
        cursor.execute(query, params)
        success_stats = dict(cursor.fetchall())
        
        return {
            'total_events': total_events,
            'events_by_type': events_by_type,
            'success_stats': success_stats,
            'period_days': days
        }
    except sqlite3.Error as e:
        print(f"Error getting audit log stats: {e}")
        return {}
    finally:
        conn.close()

def cleanup_old_audit_logs(retention_days=90):
    """Clean up audit logs older than specified days."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DELETE FROM audit_logs 
            WHERE created_at < datetime('now', '-{} days')
        """.format(retention_days))
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        print(f"Cleaned up {deleted_count} old audit log entries")
        return deleted_count
    except sqlite3.Error as e:
        print(f"Error cleaning up audit logs: {e}")
        return 0
    finally:
        conn.close()

def export_audit_logs(username=None, start_date=None, end_date=None):
    """Export audit logs to JSON format."""
    logs = get_audit_logs(username=username, start_date=start_date, end_date=end_date, limit=10000)
    
    backup_dir = "../backup"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"AegisVault_AuditLogs_{timestamp}.json"
    backup_path = os.path.join(backup_dir, filename)
    
    with open(backup_path, "w") as backup_file:
        json.dump(logs, backup_file, indent=4, default=str)
    
    return backup_path

