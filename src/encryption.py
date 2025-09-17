import os
import sys
from cryptography.fernet import Fernet

def get_encryption_key_path():
    """Get the appropriate path for the encryption key."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        if sys.platform == 'win32':
            app_data = os.path.join(os.environ.get('APPDATA', ''), 'AegisVault')
        elif sys.platform == 'darwin':
            app_data = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'AegisVault')
        else:
            app_data = os.path.join(os.path.expanduser('~'), '.local', 'share', 'AegisVault')
    else:
        # Running as script
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        app_data = os.path.normpath(os.path.join(BASE_DIR, "..", "data"))
    
    os.makedirs(app_data, exist_ok=True)
    return os.path.join(app_data, "encryption_key.key")

# Initialize encryption with the stored key
key = None
if not os.path.exists(get_encryption_key_path()):
    key = Fernet.generate_key()
    with open(get_encryption_key_path(), "wb") as key_file:
        key_file.write(key)
else:
    with open(get_encryption_key_path(), "rb") as key_file:
        key = key_file.read()

print(f"Generated Key: {key}")  # ✅ Debugging output

cipher_suite = Fernet(key)


def encrypt_data(data):
    """Encrypts data using AES-256."""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypts AES-256 encrypted data."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()