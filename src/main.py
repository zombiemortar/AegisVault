from encryption import store_password, retrieve_password, generate_key
from storage import store_user_metadata, get_user_salts

# Initialize encryption key
key = generate_key()

# Define username for testing
username = "example_user"

# Ensure user metadata is stored properly
store_user_metadata(username)

# Retrieve stored salts to confirm they exist
username_salt, password_salt = get_user_salts(username)
# print(f"Retrieved Username Salt: {username_salt}")
# print(f"Retrieved Password Salt: {password_salt}")

# Test storing a password
account = "example.com"
password = "MySuperSecretPassword123!"
store_password(username, account, password, key)
# print(f"Stored password for {account}")

# Test retrieving the password
retrieved_password = retrieve_password(username, account, key)
# print(f"Retrieved Password: {retrieved_password}")

# Verify password matches expected output
if retrieved_password == password:
    print("✅ Password successfully retrieved and verified!")
else:
    print("❌ Password retrieval failed or mismatch.")