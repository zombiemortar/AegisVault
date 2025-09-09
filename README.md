<p align="center">
    <img src="src/static/aegisvault.jpg" alt="AegisVault Logo">
</p>


# AegisVault

## **Overview**
AegisVault is a **secure password management tool** designed for  
**strong encryption, authentication, and user-friendly access**.  

Using **AES-256 encryption**, **encrypted master passwords**, and  
**session management**, it ensures **data integrity and protection  
against unauthorized access**.  

Built with **Python and Flask**, AegisVault prioritizes both  
**security and usability**, making it easy for users to store and  
manage credentials securely through both web and command-line interfaces.  

## **Features**
- ✅ **AES-256 Encryption** - All sensitive data encrypted using Fernet
- ✅ **Dual Interface** - Web-based and command-line access
- ✅ **Secure Session Management** - Automatic timeout and auto-lock
- ✅ **Password Strength Analysis** - Built-in password strength checker
- ✅ **Secure Password Generation** - Cryptographically secure password creation
- ✅ **Database Export** - Encrypted backup functionality
- ✅ **Responsive Web UI** - Bootstrap-powered modern interface
- ✅ **Local Storage** - All data stored locally, no cloud dependencies


## **Installation**
### **1. Clone the repository**
```bash
git clone https://github.com/zombiemortar/AegisVault.git
cd AegisVault
```

### **2. Set up a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows
```
### **3. Install Dependencies**
```bash
cd src
pip install -r requirements.txt
```

**Dependencies:**
- Flask 3.0.2 - Web framework
- cryptography 45.0.2 - AES-256 encryption
- Python 3.8+ - Runtime environment

### **4. Run the App:**

**Web Interface:**
```bash
cd src
python app.py
```
Then open your browser to `http://localhost:5000`

**Command Line Interface:**
```bash
cd src
python main.py
```
## **Usage**
### **Web Interface**
1. **Create Account** - Set up your master account on first use
2. **Login** - Access your secure vault with your master credentials
3. **Dashboard** - View and manage your stored passwords
4. **Add Passwords** - Store new credentials with automatic encryption
5. **Settings** - Configure session timeout and export your database
6. **Auto-lock** - Automatic session expiration for security

### **Command Line Interface**
1. **Login** - Authenticate with your master account
2. **Store Passwords** - Add new credentials securely
3. **Retrieve Passwords** - View stored credentials
4. **Update/Delete** - Modify or remove stored passwords
5. **Session Management** - Automatic timeout and security features

## **Security Features**
- 🔒 **AES-256 Encryption** - Military-grade encryption for all stored data
- 🔒 **Local Storage Only** - No data transmitted to external services
- 🔒 **Session Timeout** - Automatic logout after inactivity
- 🔒 **Auto-lock** - Immediate lock on suspicious activity
- 🔒 **Secure Key Generation** - Cryptographically secure encryption keys
- 🔒 **No Telemetry** - Zero data collection or tracking

## **Project Structure**
```
Aegis Vault/
├── src/                    # Source code
│   ├── app.py             # Flask web application
│   ├── main.py            # Command-line interface
│   ├── database.py        # Database operations
│   ├── encryption.py      # AES-256 encryption
│   ├── session.py         # Session management
│   ├── password_*.py     # Password utilities
│   ├── templates/         # HTML templates
│   └── static/           # CSS, JS, images
├── data/                  # Database files
├── docs/                  # Documentation
└── backup/               # Backup files
```

## Future Revisions:

- 🔄 **Theme Customization**
- 🔄 **Two-Factor Authentication**
- 🔄 **Advanced Session tracking and expiration options**

## **Contributors**
Created by **Joseph Sparks**. Contributions welcome after v1.0!  

