import sys
from PyQt5.QtWidgets import QApplication
from encryption import store_password, retrieve_password, generate_key
from storage import store_user_metadata, get_user_salts
import auth
import session
import login_ui  # Import PyQt login screen
import os

# Initialize session manager
user_session = session.SessionManager()

# File for storing hashed master password securely
HASH_FILE = "master_hash.txt"
USER_FILE = "user_data.txt"


# Functions to save and load hashed passwords
def save_hash(hash_data):
    with open(HASH_FILE, "wb") as f:
        f.write(hash_data)


def load_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "rb") as f:
            return f.read()
    return None


# Functions to save and load usernames
def save_username(username):
    with open(USER_FILE, "w") as f:
        f.write(username)


def load_username():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return f.read().strip()
    return None


# Authentication logic before other processes
def login():
    stored_hash = load_hash()  # Load saved hash
    stored_username = load_username()  # Load saved username

    if stored_hash is None or stored_username is None:
        print("No account found. Please set up your username and master password.")
        username = input("Enter a username: ")
        master_password = input("Set up your master password: ")
        stored_hash = auth.hash_password(master_password)

        save_username(username)
        save_hash(stored_hash)
        print("✅ Username and Master Password saved securely.")
    else:
        app = QApplication(sys.argv)  # Initialize PyQt app
        login_screen = login_ui.LoginScreen()
        login_screen.show()
        app.exec_()


# Call login BEFORE initializing password management
login()


# Auto logout handling
def check_user_activity():
    if user_session.check_timeout():
        print("Session timed out. Logging out...")
        login()  # Restart authentication


# Initialize encryption key
key = generate_key()

# Define username for testing
username = load_username()

# Ensure user metadata is stored properly
store_user_metadata(username)

# Retrieve stored salts to confirm they exist
username_salt, password_salt = get_user_salts(username)


# Password management menu
def password_manager():
    print(f"\nWelcome, {username}! What would you like to do?")
    print("1. Store a new password")
    print("2. Retrieve a stored password")
    print("3. Exit")

    while True:
        check_user_activity()  # Ensure session timeout enforcement

        choice = input("Enter your choice (1/2/3): ")
        if choice == "1":
            account = input("Enter the account name: ")
            password = input("Enter the password: ")
            store_password(username, account, password, key)
            print(f"✅ Password stored securely for {account}!")
        elif choice == "2":
            account = input("Enter the account name to retrieve: ")
            retrieved_password = retrieve_password(username, account, key)
            print(f"🔑 Retrieved Password: {retrieved_password}")
        elif choice == "3":
            print("Exiting AegisVault. Goodbye!")
            exit()
        else:
            print("Invalid option. Please try again.")


# Start the password manager **after login succeeds**
password_manager()