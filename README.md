# AegisVault

## **Overview**
AegisVault is a **secure password management tool** designed for  
**strong encryption, authentication, and user-friendly access**.  

Using **AES-256 encryption**, **hashed master passwords**, and  
**session management**, it ensures **data integrity and protection  
against unauthorized access**.  

Built with **Python and PyQt**, AegisVault prioritizes both  
**security and usability**, making it easy for users to store and  
manage credentials securely.  

## **Features**
✅ **AES-256 encryption** for securely storing passwords  
✅ **Master password authentication** with hashed credentials (`bcrypt`)  
✅ **Session management with auto logout** for enhanced security  
✅ **User-friendly GUI built with PyQt** *(In Development)*  
✅ **Password generator** with customizable complexity *(Planned)*  
✅ **Audit logging** for tracking access attempts *(Planned)*  

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
pip install -r requirements.txt
```
## **Usage**
### **1. Run the application**
To start AegisVault, run:
```bash
python src/main.py
```
### **2. Set up your master password**  
If you are a first-time user, you'll be prompted to create a **master password**  
which will be securely hashed using `bcrypt`.  

### **3. Store and retrieve encrypted passwords**  
🔹 **Store passwords:** Enter a new password, which will be **AES-256 encrypted** before storage.  
🔹 **Retrieve passwords:** After authentication, decrypted passwords will be displayed securely.  
🔹 **Session management:** Auto-lock will trigger **after inactivity**, requiring re-authentication.  

### **4. Adjust settings (Upcoming Features)**  
Future updates will allow users to customize:  
- **Auto-lock timeout duration**  
- **Password generator complexity settings**  
- **GUI-based interactions for encryption and retrieval**  

---
## **Development Roadmap**
### **Week 1: Core Foundations**
- ⬜ Implement **master password authentication** with secure hashing  
- ⬜ Implement **session management & auto logout**  

### **Week 2: GUI & Password Management**
- ⬜ Build **PyQt-based user interface**  
- ⬜ Implement **password storage & retrieval in GUI**  

### **Week 3: Security Hardening & Optimization**
- ⬜ Conduct **security audits** (validate encryption, test vulnerabilities)  
- ⬜ Implement **backup & recovery mechanism** for encrypted vault data  
- ⬜ Optimize **UI usability** and refine input validation  

### **Week 4: Final Testing & Documentation**
- ⬜ Perform **end-to-end testing** on security & usability  
- ⬜ Fix **bugs & optimize performance**  
- ⬜ Write **documentation** for functionality & security measures  
- ⬜ Prepare for **future browser integration**  

## **Future Enhancements**
🔹 **Multi-factor authentication (2FA)** *(Under consideration)*  
🔹 **Cloud sync for encrypted vault storage** *(Planned)*  
🔹 **Integration with browser autofill functionality** *(Future Expansion)*  

 

## **Contributors**
Created by **Joseph Sparks**. Contributions welcome after v1.0!  

## **Legend: Priority System**
🔴 **High Priority** – Critical feature, must be completed ASAP  
🟡 **Medium Priority** – Important but can follow core foundation tasks  
🔵 **Low Priority** – Enhancements or future refinements  

✅ **Completed Task** – Successfully implemented and verified  
⬜ **Incomplete Task** – Still needs to be worked on  
