import sqlite3
from encryption import encrypt_data, decrypt_data
from database import DATABASE_FILE

def create_test_user():
    print("=== Create Test User ===")
    print(f"🗄️ Using database: {DATABASE_FILE}")
    
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check existing users
    cursor.execute("SELECT * FROM master_account")
    existing_users = cursor.fetchall()
    
    print(f"Current users in database: {len(existing_users)}")
    
    if existing_users:
        print("\nExisting users:")
        for i, user in enumerate(existing_users, 1):
            try:
                decrypted_username = decrypt_data(user[0])
                decrypted_password = decrypt_data(user[1])
                print(f"  {i}. Username: {decrypted_username}, Password: {decrypted_password}")
            except Exception as e:
                print(f"  {i}. Encrypted data (decryption failed): {user[0][:20]}...")
    
    # Create a new test user
    print("\n=== Creating Test User ===")
    test_username = "testuser"
    test_password = "testpass123"
    
    # Check if user already exists
    cursor.execute("SELECT * FROM master_account WHERE username = ?", (encrypt_data(test_username),))
    if cursor.fetchone():
        print(f"❌ User '{test_username}' already exists")
    else:
        # Create new user
        encrypted_username = encrypt_data(test_username)
        encrypted_password = encrypt_data(test_password)
        
        cursor.execute("INSERT INTO master_account (username, password) VALUES (?, ?)", 
                      (encrypted_username, encrypted_password))
        conn.commit()
        
        print(f"✅ Created test user:")
        print(f"   Username: {test_username}")
        print(f"   Password: {test_password}")
    
    conn.close()

def test_login():
    print("\n=== Test Login ===")
    
    # Test credentials
    test_username = "testuser"
    test_password = "testpass123"
    
    # Connect to database
    conn = sqlite3.connect("../data/passwords.db")
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute("SELECT * FROM master_account")
    users = cursor.fetchall()
    
    # Try to find matching user
    for user in users:
        try:
            decrypted_username = decrypt_data(user[0])
            decrypted_password = decrypt_data(user[1])
            
            if decrypted_username == test_username and decrypted_password == test_password:
                print("✅ Login test successful!")
                print(f"   Username: {decrypted_username}")
                print(f"   Password: {decrypted_password}")
                conn.close()
                return True
        except Exception as e:
            print(f"❌ Decryption error: {e}")
    
    print("❌ Login test failed - no matching user found")
    conn.close()
    return False

if __name__ == "__main__":
    create_test_user()
    test_login()
    
    print("\n=== Instructions ===")
    print("1. Run the Flask app: python app.py")
    print("2. Go to http://localhost:5000")
    print("3. Login with:")
    print("   Username: testuser")
    print("   Password: testpass123")
