import os
import threading
from database import (
    store_password, retrieve_password, store_master_account, load_master_account,
    delete_password, update_password, init_db, get_all_stored_urls
)
from encryption import generate_key, encrypt_data, decrypt_data
from session import SessionManager

# Initialize database and encryption key on startup
init_db()
generate_key()
session_active = False  # Tracks whether session is active
session_expired_event = threading.Event()  # Tracks session expiration
session = SessionManager()
stored_urls = get_all_stored_urls()
print("🔗 Stored Website URLs:", stored_urls)


def startup_menu():
    """Initial prompt to login or exit."""
    global session_active
    session_active = False  # Ensure fresh start each time

    while True:
        print("\n🔐 Welcome to AegisVault - Secure Password Manager")
        print("1. Login")
        print("2. Close Program")

        choice = input("Choose an option: ")
        if choice == "1":
            login()
        elif choice == "2":
            print("🔒 Program closed.")
            os._exit(0)  # Force exit
        else:
            print("❌ Invalid choice. Please select 1 or 2.")


def login():
    """Handles master account authentication and session start."""
    stored_username, stored_password = load_master_account()

    if not stored_username:
        print("No master account found. Let's create one.")
        username = input("Enter a master username: ")
        password = input("Enter a secure password: ")
        store_master_account(username, password)
        print("✅ Master account created successfully!")
        return startup_menu()

    entered_username = input("Enter master username: ")
    entered_password = input("Enter master password: ")

    if entered_username == stored_username and entered_password == stored_password:
        print("✅ Login successful! Starting session...")
        session.start_session(entered_username)  # ✅ Start session tracking
        main_menu()  # ✅ Transition to main menu
    else:
        print("❌ Incorrect username or password. Try again.")



def store_credentials():
    """Stores encrypted credentials securely."""
    if not session.validate_session():
        print("❌ Session expired. Please log in again.")
        return startup_menu()  # ✅ Restart login after expiration

    session.refresh_session()  # ✅ Reset timer
    website = input("Enter website URL: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    store_password(website, username, password)
    print("✅ Password stored securely!")


def retrieve_credentials():
    """Retrieves stored username and password for a given website."""
    if not session.validate_session():
        print("❌ Session expired. Please log in again.")
        return

    session.refresh_session()  # 🔄 Keep session active!

    website = input("Enter website URL to retrieve credentials: ")

    encrypted_website = encrypt_data(website)  # Debugging encryption match
    print(f"🔎 Encrypted Website Input: {encrypted_website}")  # Debug print

    stored_username, stored_password = retrieve_password(website)  # ✅ Uses `database.py` function

    if stored_username and stored_password:
        print(f"🔐 Stored Credentials for {website}:")
        print(f"   Username: {stored_username}")
        print(f"   Password: {stored_password}")
    else:
        print("❌ No matching credentials found.")

def delete_credentials():
    """Deletes stored credentials for a given website."""
    if not session.validate_session():
        print("❌ Session expired. Please log in again.")
        return

    session.refresh_session()  # 🔄 Keep session active!

    website = input("Enter website URL to delete credentials: ")
    delete_password(website)  # ✅ Calls function from `database.py`
    print(f"✅ Credentials for {website} successfully removed.")

def update_credentials():
    """Updates stored password for a given website."""
    if not session.validate_session():
        print("❌ Session expired. Please log in again.")
        return

    session.refresh_session()  # 🔄 Keep session active!

    website = input("Enter website URL to update password: ")
    new_password = input("Enter new password: ")
    update_password(website, new_password)  # ✅ Calls function from `database.py`
    print(f"✅ Password for {website} has been successfully updated.")


def main_menu():
    """Displays main menu options and starts session monitoring."""
    session.start_session("master_user")  # ✅ Ensure session starts properly
    threading.Thread(target=session.monitor_session, daemon=True).start()  # ✅ Call it from SessionManager

    while session.validate_session():
        print("\n🔐 AegisVault - Secure Password Manager")
        print("1. Store a new password")
        print("2. Retrieve a stored password")
        print("3. Delete a stored password")
        print("4. Update a stored password")
        print("5. Logout & Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            store_credentials()
        elif choice == "2":
            retrieve_credentials()
        elif choice == "3":
            delete_credentials()
        elif choice == "4":
            update_credentials()
        elif choice == "5":
            logout()
            break
        else:
            print("❌ Invalid choice. Try again.")


def logout():
    """Ends session cleanly without triggering an undefined event."""
    print("\n🔒 Logging out and exiting securely...")
    session.active = False  # ✅ Stop session tracking

    if 'session_expire_event' in globals():  # ✅ Avoid errors if it's missing
        session_expire_event.set()  # ✅ Signal expiration safely

    session.expire_session()  # ✅ Cleanly end session

def check_session():
    """Handles expired sessions and returns to startup menu if needed."""
    if not session.validate_session():
        startup_menu()  # ✅ Transition back to login AFTER expiration is detected

if __name__ == "__main__":
    startup_menu()