from Crypto.Cipher import AES
import secrets
from storage import store_encrypted_password, retrieve_encrypted_password, get_user_salts

# Generate a random encryption key (AES-256)
def generate_key() -> bytes:
    """Generates a 32-byte key for AES-256 encryption."""
    return secrets.token_bytes(32)

# Encrypt a password using AES-256 with a unique password salt
def encrypt_password(username: str, password: str, key: bytes) -> bytes:
    """Encrypts a password using AES-256 and a unique salt."""
    _, password_salt = get_user_salts(username)  # Retrieve password salt

    if password_salt is None:
        raise ValueError("Password salt not found for user.")

    password_bytes = password.encode() + password_salt  # Append salt before encryption

    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(password_bytes)

    return cipher.nonce + tag + ciphertext  # Store nonce, tag, and ciphertext together

# Decrypt a password using AES-256 and ensure correct salt is applied
def decrypt_password(username: str, encrypted_data: bytes, key: bytes) -> str:
    """Decrypts an AES-256 encrypted password using the correct salt."""
    _, password_salt = get_user_salts(username)  # Retrieve password salt

    if password_salt is None:
        raise ValueError("Password salt not found for user.")

    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    try:
        decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        print("Decryption failed. Possible data corruption or incorrect key.")
        return None

    # Debugging outputs
    # print(f"Raw Decrypted Bytes: {decrypted_bytes}")
    # print(f"Expected Salt: {password_salt}")

    # Validate password salt before returning
    if not decrypted_bytes.endswith(password_salt):
        # print("Password integrity check failed. Salt mismatch.")
        return None

    return decrypted_bytes[:-len(password_salt)].decode()  # Remove salt and return password

# Store an encrypted password securely
def store_password(username: str, account: str, password: str, key: bytes):
    """Encrypts and stores a password securely."""
    encrypted_data = encrypt_password(username, password, key)
    store_encrypted_password(username, account, encrypted_data)

# Retrieve and decrypt a stored password
def retrieve_password(username: str, account: str, key: bytes) -> str:
    """Retrieves and decrypts a stored password."""
    encrypted_data = retrieve_encrypted_password(username, account)
    if encrypted_data is None:
        return None

    return decrypt_password(username, encrypted_data, key)