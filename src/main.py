from encryption import store_password, retrieve_password, generate_key
from storage import store_user_metadata, get_user_salts
import auth
import session
import os

# Initialize session manager
user_session = session.SessionManager()

# File for storing hashed master password securely
HASH_FILE = "master_hash.txt"


# Functions to save and load hashed passwords
def save_hash(hash_data):
    with open(HASH_FILE, "wb") as f:
        f.write(hash_data)


def load_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "rb") as f:
            return f.read()
    return None


# Authentication logic before other processes
def login():
    stored_hash = load_hash()  # Load saved hash

    while True:  # Keeps looping until authentication is successful
        if stored_hash is None:
            master_password = input("Set up your master password: ")
            stored_hash = auth.hash_password(master_password)
            save_hash(stored_hash)
            print("Master password saved securely.")
            break  # Move forward after setting the password
        else:
            master_password = input("Enter your master password: ")
            if auth.verify_password(stored_hash, master_password):
                print("Login successful!")
                user_session.reset_activity()  # Reset session timer
                break  # Continue into password management
            else:
                print("Incorrect password. Try again.")

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
username = "example_user"

# Ensure user metadata is stored properly
store_user_metadata(username)

# Retrieve stored salts to confirm they exist
username_salt, password_salt = get_user_salts(username)


# Password management menu
def password_manager():
    print("\nWelcome to AegisVault! What would you like to do?")
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