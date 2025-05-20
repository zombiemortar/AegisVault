import sqlite3
from encryption import encrypt_data, decrypt_data

DB_PATH = "../data/passwords.db"

def test_update():
    """Manually test updating password in master_account."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 🔎 Retrieve current credentials for debugging
    cursor.execute("SELECT username, password FROM master_account")
    row = cursor.fetchone()

    if not row:
        print("❌ No credentials found in master_account.")
        conn.close()
        return

    stored_username, stored_password = row

    print("\n🔎 **Before Update** 🔎")
    print(f"➡️ Encrypted Username: {stored_username}")
    print(f"➡️ Encrypted Password: {stored_password}")

    # 🚀 Attempt update manually
    new_password = "test_update_value"  # Change to a test password
    encrypted_new_password = encrypt_data(new_password)

    cursor.execute("UPDATE master_account SET password = ? WHERE username = ?",
                   (encrypted_new_password, stored_username))
    conn.commit()

    # 🔎 Verify update success
    cursor.execute("SELECT username, password FROM master_account")
    updated_row = cursor.fetchone()
    conn.close()

    print("\n🔎 **After Update** 🔎")
    print(f"➡️ Encrypted Username: {updated_row[0]}")
    print(f"➡️ Encrypted Password: {updated_row[1]}")

if __name__ == "__main__":
    test_update()