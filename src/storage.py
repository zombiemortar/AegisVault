import json
import os
import hashlib
import secrets

# File paths
USER_METADATA_FILE = "user_metadata.json"
PASSWORDS_FILE = "passwords.json"

# Generate a random salt
def generate_salt() -> bytes:
    """Generates a random 16-byte salt for hashing."""
    return secrets.token_bytes(16)

# Generate a secure SHA-256 hash for usernames using a unique salt
def hash_username(username: str, salt: bytes) -> str:
    """Hashes the username using SHA-256 and its associated salt."""
    return hashlib.sha256(username.encode() + salt).hexdigest()

# Store a user's unique salts for username & password hashing
def store_user_metadata(username: str):
    """Stores the salts associated with a given username in user_metadata.json."""
    if not os.path.exists(USER_METADATA_FILE):
        metadata = {"users": {}}
    else:
        with open(USER_METADATA_FILE, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    # Generate unique salts
    username_salt = generate_salt()
    password_salt = generate_salt()
    hashed_username = hash_username(username, username_salt)

    # Debug: Print generated salts
    # print(f"Generated username salt: {username_salt.hex()}")
    # print(f"Generated password salt: {password_salt.hex()}")

    # Ensure salts are stored correctly
    metadata["users"][hashed_username] = {
        "username_salt": username_salt.hex(),
        "password_salt": password_salt.hex()
    }

    with open(USER_METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print("User metadata saved successfully!")

# Retrieve a user's salts for username & password hashing
def get_user_salts(username: str) -> tuple[bytes, bytes]:
    """Retrieves the salts for a given username from user_metadata.json."""
    if not os.path.exists(USER_METADATA_FILE):
        return b'', b''

    with open(USER_METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    for hashed_username, user_data in metadata["users"].items():
        username_salt = bytes.fromhex(user_data["username_salt"])
        password_salt = bytes.fromhex(user_data["password_salt"])

        if hash_username(username, username_salt) == hashed_username:
            return username_salt, password_salt

    return b'', b''  # User not found

# Save an encrypted password using hashed username & password salt
def store_encrypted_password(username: str, account: str, encrypted_password: bytes):
    """Stores encrypted passwords securely in passwords.json."""
    username_salt, password_salt = get_user_salts(username)

    if username_salt is None or password_salt is None:
        print("User not found. Cannot store password.")
        return

    hashed_username = hash_username(username, username_salt)

    if not os.path.exists(PASSWORDS_FILE):
        passwords = {}
    else:
        with open(PASSWORDS_FILE, "r", encoding="utf-8") as f:
            passwords = json.load(f)

    if hashed_username not in passwords:
        passwords[hashed_username] = {}

    passwords[hashed_username][account] = encrypted_password.hex()  # Store in hex format

    with open(PASSWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(passwords, f, indent=4)

# Retrieve an encrypted password for a given username and account
def retrieve_encrypted_password(username: str, account: str) -> bytes:
    """Retrieves encrypted password for a given username and account."""
    if not os.path.exists(PASSWORDS_FILE):
        print("Passwords.json does not exist.")
        return None

    with open(PASSWORDS_FILE, "r", encoding="utf-8") as f:
        passwords = json.load(f)

    # Retrieve stored salts for username
    username_salt, _ = get_user_salts(username)
    if username_salt is None:
        print(f"Salt not found for username: {username}")
        return None

    hashed_username = hash_username(username, username_salt)

    # Debug Output: Show stored passwords structure
    # print("Stored passwords:", json.dumps(passwords, indent=4))
    # print(f"Looking for hashed username: {hashed_username}")

    if hashed_username in passwords and account in passwords[hashed_username]:
        encrypted_password = bytes.fromhex(passwords[hashed_username][account])
        # print(f"Encrypted password found for {account}: {encrypted_password}")
        return encrypted_password

    print("Password not found.")
    return None  # Password not found