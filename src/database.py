import sqlite3
import os
from encryption import encrypt_data, decrypt_data

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
    conn.commit()
    conn.close()

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