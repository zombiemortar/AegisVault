import bcrypt

# Generate a hashed master password
def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

# Verify user-entered password
def verify_password(stored_hash: bytes, user_input: str) -> bool:
    return bcrypt.checkpw(user_input.encode(), stored_hash)