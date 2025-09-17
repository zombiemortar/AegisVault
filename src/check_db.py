import sqlite3
import os
import sys
from database import get_app_data_dir, DATABASE_FILE

def check_database():
    print("=== Database Check ===")
    
    # Get the correct database path
    data_dir = get_app_data_dir()
    db_path = DATABASE_FILE
    print(f"📁 Data directory: {data_dir}")
    print(f"🗄️ Database path: {db_path}")
    
    # Check if database exists
    if os.path.exists(db_path):
        print(f"✅ Database exists at: {db_path}")
    else:
        print(f"❌ Database not found at: {db_path}")
        return
    
    # Connect to database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tables found: {[table[0] for table in tables]}")
        
        # Check master_account table
        if ('master_account',) in tables:
            cursor.execute("SELECT * FROM master_account")
            users = cursor.fetchall()
            print(f"👥 Users in master_account: {len(users)}")
            
            if users:
                print("User details:")
                for user in users:
                    print(f"  - Username: {user[0]}, Password: {user[1][:20]}...")
            else:
                print("❌ No users found in master_account table")
        else:
            print("❌ master_account table not found")
        
        # Check user_preferences table
        if ('user_preferences',) in tables:
            cursor.execute("SELECT * FROM user_preferences")
            prefs = cursor.fetchall()
            print(f"⚙️ User preferences: {len(prefs)}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")

def check_encryption_key():
    print("\n=== Encryption Key Check ===")
    
    # Import the encryption key path function
    from encryption import get_encryption_key_path
    
    key_path = get_encryption_key_path()
    print(f"🔑 Encryption key path: {key_path}")
    
    if os.path.exists(key_path):
        print(f"✅ Encryption key exists at: {key_path}")
        try:
            with open(key_path, "rb") as key_file:
                key_data = key_file.read()
                print(f"📏 Key size: {len(key_data)} bytes")
        except Exception as e:
            print(f"❌ Error reading key: {e}")
        return key_path
    else:
        print(f"❌ Encryption key not found at: {key_path}")
        return None

def check_encryption():
    print("\n=== Encryption Test ===")
    
    try:
        from encryption import encrypt_data, decrypt_data
        
        # Test encryption/decryption
        test_data = "test_password"
        encrypted = encrypt_data(test_data)
        decrypted = decrypt_data(encrypted)
        
        if test_data == decrypted:
            print("✅ Encryption/decryption working correctly")
        else:
            print("❌ Encryption/decryption failed")
            
    except Exception as e:
        print(f"❌ Encryption error: {e}")

if __name__ == "__main__":
    check_database()
    check_encryption_key()
    check_encryption()
