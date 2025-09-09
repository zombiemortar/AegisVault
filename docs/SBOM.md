# Software Bill of Materials (SBOM)
## Aegis Vault - Secure Password Manager

**Project:** Aegis Vault  
**Version:** 1.0.0  
**Generated:** December 2024  
**License:** MIT  

---

## Executive Summary

This Software Bill of Materials (SBOM) provides a comprehensive inventory of all software components, libraries, and dependencies used in the Aegis Vault password management application. The project is built using Python with Flask as the web framework and includes both web-based and command-line interfaces.

---

## 1. Core Application Dependencies

### 1.1 Python Runtime
- **Component:** Python
- **Version:** 3.8+ (compatible)
- **Type:** Runtime Environment
- **License:** Python Software Foundation License
- **Purpose:** Core programming language for the application

### 1.2 Web Framework
- **Component:** Flask
- **Version:** 3.0.2
- **Type:** Web Framework
- **License:** BSD-3-Clause
- **Purpose:** Web application framework for HTTP server functionality
- **Source:** PyPI

### 1.3 Database Management
- **Component:** SQLAlchemy
- **Version:** 2.0.28
- **Type:** Database ORM
- **License:** MIT
- **Purpose:** Object-relational mapping for database operations
- **Source:** PyPI

- **Component:** Flask-SQLAlchemy
- **Version:** 3.1.1
- **Type:** Flask Extension
- **License:** BSD-3-Clause
- **Purpose:** SQLAlchemy integration for Flask
- **Source:** PyPI

### 1.4 Authentication & Security
- **Component:** Flask-Login
- **Version:** 0.6.3
- **Type:** Authentication Extension
- **License:** MIT
- **Purpose:** User session management and authentication
- **Source:** PyPI

- **Component:** bcrypt
- **Version:** 4.3.0
- **Type:** Cryptographic Library
- **License:** Apache-2.0
- **Purpose:** Password hashing and secure authentication
- **Source:** PyPI

- **Component:** cryptography
- **Version:** 45.0.2
- **Type:** Cryptographic Library
- **License:** Apache-2.0 / BSD-3-Clause
- **Purpose:** Advanced cryptographic operations and encryption
- **Source:** PyPI

- **Component:** pycryptodome
- **Version:** 3.22.0
- **Type:** Cryptographic Library
- **License:** Public Domain / BSD-2-Clause
- **Purpose:** Additional cryptographic algorithms and secure random number generation
- **Source:** PyPI

- **Component:** pyotp
- **Version:** 2.9.0
- **Type:** OTP Library
- **License:** MIT
- **Purpose:** One-Time Password generation and validation
- **Source:** PyPI

### 1.5 System Dependencies
- **Component:** cffi
- **Version:** 1.17.1
- **Type:** Foreign Function Interface
- **License:** MIT
- **Purpose:** C Foreign Function Interface for Python
- **Source:** PyPI

- **Component:** pycparser
- **Version:** 2.22
- **Type:** C Parser
- **License:** BSD-3-Clause
- **Purpose:** C parser for cffi
- **Source:** PyPI

### 1.6 GUI Framework (Optional)
- **Component:** PyQt5
- **Version:** 5.15.11
- **Type:** GUI Framework
- **License:** GPL-3.0 / Commercial
- **Purpose:** Desktop GUI application interface (optional component)
- **Source:** PyPI

- **Component:** PyQt5-Qt5
- **Version:** 5.15.2
- **Type:** Qt5 Bindings
- **License:** GPL-3.0 / Commercial
- **Purpose:** Qt5 framework bindings for PyQt5
- **Source:** PyPI

- **Component:** PyQt5_sip
- **Version:** 12.17.0
- **Type:** SIP Bindings
- **License:** GPL-3.0 / Commercial
- **Purpose:** SIP bindings for PyQt5
- **Source:** PyPI

---

## 2. Frontend Dependencies

### 2.1 CSS Framework
- **Component:** Bootstrap
- **Version:** 5.3.0
- **Type:** CSS Framework
- **License:** MIT
- **Purpose:** Responsive web design and UI components
- **Source:** CDN (jsdelivr.net)
- **CDN URL:** https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/

### 2.2 JavaScript Libraries
- **Component:** Bootstrap JavaScript Bundle
- **Version:** 5.3.0
- **Type:** JavaScript Library
- **License:** MIT
- **Purpose:** Interactive UI components and functionality
- **Source:** CDN (jsdelivr.net)
- **CDN URL:** https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js

---

## 3. Built-in Python Modules

### 3.1 Standard Library Modules
The following Python standard library modules are used throughout the application:

- **json** - JSON data handling and serialization
- **os** - Operating system interface
- **sqlite3** - SQLite database interface
- **threading** - Threading support for session management
- **time** - Time-related functions
- **traceback** - Exception traceback utilities
- **re** - Regular expression operations
- **math** - Mathematical functions
- **secrets** - Cryptographically strong random number generation
- **string** - String manipulation utilities
- **typing** - Type hints support

---

## 4. Custom Application Components

### 4.1 Core Modules
- **app.py** - Main Flask application and web routes
- **main.py** - Command-line interface entry point
- **database.py** - Database operations and schema management
- **encryption.py** - Data encryption and decryption functions
- **session.py** - User session management and timeout handling
- **password_strength.py** - Password strength analysis and validation
- **password_generator.py** - Secure password generation utilities

### 4.2 Static Assets
- **style.css** - Custom CSS styling and theme management
- **auto_lock.js** - Client-side auto-lock functionality
- **theme.js** - Theme switching and system preference detection
- **aegisvault.jpg** - Application logo and branding assets

### 4.3 Templates
- **login.html** - User authentication interface
- **dashboard.html** - Main application dashboard
- **vault.html** - Password vault management interface
- **add_password.html** - Password entry form
- **settings.html** - Application settings and preferences
- **create_account.html** - User account creation form

---

## 5. Development Dependencies

### 5.1 Testing Framework
- **test_password_generator.py** - Unit tests for password generation
- **test_password_strength.py** - Unit tests for password strength analysis
- **test.py** - General application testing utilities

### 5.2 Database Files
- **passwords.db** - SQLite database file (user data)
- **encryption_key.key** - Encryption key file (generated at runtime)

---

## 6. Security Considerations

### 6.1 Cryptographic Libraries
- **cryptography** - Industry-standard cryptographic library
- **pycryptodome** - Additional cryptographic algorithms
- **bcrypt** - Secure password hashing
- **secrets** - Cryptographically secure random number generation

### 6.2 Data Protection
- All sensitive data is encrypted using AES-256 encryption
- Passwords are hashed using bcrypt with appropriate salt rounds
- Session management includes automatic timeout and security features
- Auto-lock functionality prevents unauthorized access

---

## 7. License Summary

| Component                | License                              | Type         |
|--------------------------|--------------------------------------|--------------|
| Flask                    | BSD-3-Clause                         | Open Source  |
| SQLAlchemy               | MIT                                  | Open Source  |
| Flask-SQLAlchemy         | BSD-3-Clause                         | Open Source  |
| Flask-Login              | MIT                                  | Open Source  |
| bcrypt                   | Apache-2.0                           | Open Source  |
| cryptography             | Apache-2.0 / BSD-3-Clause            | Open Source  |
| pycryptodome             | Public Domain / BSD-2-Clause         | Open Source  |
| pyotp                    | MIT                                  | Open Source  |
| Bootstrap                | MIT                                  | Open Source  |
| PyQt5                    | GPL-3.0 / Commercial                 | Dual License |
| Python                   | Python Software Foundation License   | Open Source  |

---

## 8. Vulnerability Assessment

### 8.1 Known Vulnerabilities
As of the generation date, all dependencies are current and no known critical vulnerabilities have been identified. Regular security updates are recommended.

### 8.2 Security Recommendations
1. Regularly update all dependencies to their latest stable versions
2. Monitor security advisories for all third-party components
3. Implement automated dependency scanning in CI/CD pipeline
4. Consider using dependency pinning for production deployments

---

## 9. Compliance and Standards

### 9.1 Security Standards
- Follows OWASP guidelines for web application security
- Implements secure password storage practices
- Uses industry-standard encryption algorithms
- Implements proper session management

### 9.2 Data Privacy
- No data is transmitted to external services
- All data is stored locally in encrypted format
- No telemetry or analytics data collection
- User data remains under user control

---

## 10. Maintenance and Updates

### 10.1 Update Schedule
- **Critical Security Updates:** Immediate
- **Minor Version Updates:** Monthly
- **Major Version Updates:** Quarterly
- **Dependency Updates:** As needed

### 10.2 End-of-Life Considerations
- Monitor end-of-life announcements for all dependencies
- Plan migration paths for deprecated components
- Maintain compatibility with supported Python versions

---

## 11. Contact Information

**Project Maintainer:** Aegis Vault Development Team  
**Repository:** [Project Repository URL]  
**Documentation:** [Project Documentation URL]  
**Security Issues:** [Security Contact Information]  

---

## 12. Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | December 2024 | Initial SBOM creation |

---

*This Software Bill of Materials is generated for the Aegis Vault project and should be updated whenever dependencies are added, removed, or updated.*
