import os
from cryptography.fernet import Fernet

KEY_FILE = "encryption_key.key"

def generate_key():
    """Generates a persistent encryption key only if none exists."""
    if not os.path.exists(KEY_FILE):  # ✅ Avoids overwriting previous keys
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    """Loads the encryption key from a file."""
    try:
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("🔐 Encryption key not found, generating a new one.")
        generate_key()
        return load_key()

# Initialize encryption with the stored key
key = load_key()
cipher_suite = Fernet(key)


def encrypt_data(data):
    """Encrypts data using AES-256."""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypts AES-256 encrypted data."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()