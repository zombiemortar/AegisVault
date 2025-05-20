import os
from cryptography.fernet import Fernet

KEY_FILE = "encryption_key.key"


def generate_key():
    """Generates and returns a persistent encryption key only if none exists."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()

    return key  # ✅ Directly return the key

def load_key():
    """Loads encryption key from file or generates a new one."""
    return generate_key() if not os.path.exists(KEY_FILE) else open(KEY_FILE, "rb").read()

# Initialize encryption with the stored key
key = load_key()
cipher_suite = Fernet(key)


def encrypt_data(data):
    """Encrypts data using AES-256."""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypts AES-256 encrypted data."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()