from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import auth
import os

HASH_FILE = "master_hash.txt"
USER_FILE = "user_data.txt"

# Functions to manage username and hash storage
def load_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "rb") as f:
            return f.read()
    return None

def save_hash(hash_data):
    with open(HASH_FILE, "wb") as f:
        f.write(hash_data)

def load_username():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return f.read().strip()
    return None

def save_username(username):
    with open(USER_FILE, "w") as f:
        f.write(username)

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AegisVault Login")
        self.setFixedSize(400, 250)

        # UI Elements
        self.title = QLabel("Welcome to AegisVault", self)
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter your username")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter master password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("background-color: #5A67D8; color: white; padding: 8px; border-radius: 5px;")

        # Connect button to login function
        self.login_button.clicked.connect(self.authenticate)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def authenticate(self):
        username = self.username_input.text().strip()
        master_password = self.password_input.text().strip()
        stored_username = load_username()
        stored_hash = load_hash()

        if stored_username is None or stored_hash is None:
            stored_hash = auth.hash_password(master_password)
            save_username(username)
            save_hash(stored_hash)
            QMessageBox.information(self, "Account Created", "Username and master password saved securely.")
            return

        if username == stored_username and auth.verify_password(stored_hash, master_password):
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
            self.close()  # Close login screen after authentication
            # 🚨 TODO: Launch main UI here!
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password, try again.")

# Launch the UI
def run_login_ui():
    app = QApplication([])
    login_screen = LoginScreen()
    login_screen.show()
    app.exec_()