import sqlite3
import os

def check_database():
    print("=== Database Check ===")
    
    # Check if database exists
    db_path = "../data/passwords.db"
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
    
    # Check for encryption key in different locations
    possible_paths = [
        "encryption_key.key",
        "../src/encryption_key.key",
        "encryption_key.key"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Encryption key found at: {path}")
            return path
    
    print("❌ Encryption key not found in any expected location")
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
