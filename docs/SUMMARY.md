# Aegis Vault - Codebase Summary

## Project Overview
Aegis Vault is a secure password management application built with Python Flask that provides encrypted storage, password strength analysis, and a modern web interface. The application prioritizes security through encryption, session management, and comprehensive password analysis tools.

## Core Architecture

### Web Application Framework
The application is built using **Flask**, a lightweight Python web framework that provides the foundation for all web routes and functionality. The app structure follows a modular design with separate modules for different concerns including encryption, database management, session handling, and password analysis. The application uses SQLite as its database backend for simplicity and portability.

### Security Infrastructure
The security layer is built around **Fernet encryption** from the cryptography library, providing AES-256 encryption for all sensitive data. Each installation generates a unique encryption key stored in `encryption_key.key`, ensuring that encrypted data cannot be decrypted without the specific key. The encryption system automatically handles encoding/decoding of data and integrates seamlessly with the database layer.

## Major Feature Sets

### 1. User Authentication & Account Management
The authentication system provides secure user registration and login functionality with encrypted credential storage. Users can create accounts with username/password combinations that are immediately encrypted before database storage. The system prevents duplicate usernames and validates password confirmation during registration. Master account credentials are stored separately from regular passwords, maintaining a clear separation of concerns. The login system validates encrypted credentials and establishes secure sessions for authenticated users.

### 2. Session Management & Security
A sophisticated session management system provides automatic timeout functionality after 30 seconds of inactivity, ensuring that sensitive data is not left exposed on unattended devices. The system uses threading to monitor session activity in the background and automatically expires sessions when timeout conditions are met. Session data is stored securely and cleared upon logout or expiration, with automatic redirection to the login page for expired sessions.

### 3. Password Storage & Management
The core password vault functionality allows users to store, retrieve, update, and delete website credentials with automatic encryption. Each credential entry includes website URL, username, and password, with the website remaining in plaintext for searchability while usernames and passwords are encrypted. The system provides CRUD operations for credentials with proper error handling and validation. All password operations are logged for security auditing purposes.

### 4. Password Strength Analysis
A comprehensive password strength analyzer evaluates passwords using multiple metrics including entropy calculation, character set analysis, and pattern recognition. The system provides detailed feedback on password weaknesses and generates specific improvement suggestions. Password analysis includes entropy calculations in bits, strength scoring from 0-100, and identification of common weak patterns like keyboard sequences or repeated characters. The analyzer integrates with the web interface to provide real-time feedback during password creation.

### 5. Web Interface & User Experience
The application features a modern, responsive web interface built with Bootstrap 5 and custom CSS. The interface includes a dark/light theme toggle system with CSS custom properties for consistent theming. The dashboard provides an overview of stored passwords and quick access to key functions. The vault interface displays credentials in a searchable table format with password visibility toggles and inline editing capabilities. All forms include proper validation and user feedback through flash messages.

### 6. Search & Filtering Capabilities
Advanced search functionality allows users to quickly locate specific credentials by searching across website names, usernames, or any text content. The search operates in real-time as users type, providing instant filtering of results. The interface displays search result counts and maintains responsive performance even with large numbers of stored credentials. Search results are highlighted and the system provides clear feedback on search status.

### 7. Data Backup & Recovery
The backup system creates encrypted JSON exports of all stored credentials, allowing users to backup their password database or transfer data between installations. The export process decrypts data for backup purposes while maintaining security during the export operation. Users can also import previously exported backup files to restore their credential database, with proper validation of JSON format and error handling for corrupted files.

### 8. Account Settings & Management
The settings interface allows users to modify their master account password securely with proper validation and confirmation. Password changes are encrypted before storage and the system provides clear feedback on operation success or failure. The interface also includes account deletion functionality with proper session cleanup and security measures.

### 9. Database Management
The SQLite database system provides efficient storage with proper indexing and constraint management. The database schema includes separate tables for master accounts and credentials, with proper foreign key relationships and unique constraints. Database operations are wrapped in proper connection management with automatic cleanup and error handling. The system includes database initialization functions and maintains data integrity through transaction management.

### 10. Security Monitoring & Logging
Comprehensive logging throughout the application provides security auditing capabilities and debugging information. All authentication attempts, password operations, and session activities are logged with appropriate detail levels. The system includes debug output for development purposes and maintains security logs for production monitoring. Error handling provides detailed information for troubleshooting while maintaining security.

## Technical Implementation Details

### Dependencies & Libraries
- **Flask 3.0.2**: Core web framework
- **cryptography 45.0.2**: Encryption and security functions
- **SQLAlchemy 2.0.28**: Database abstraction layer
- **Bootstrap 5.3.0**: Frontend UI framework
- **Custom CSS/JS**: Theme system and interactive features

### File Structure
```
src/
├── app.py              # Main Flask application and routes
├── database.py         # Database operations and management
├── encryption.py       # Encryption/decryption functions
├── password_strength.py # Password analysis engine
├── session.py          # Session management system
├── templates/          # HTML templates
├── static/            # CSS, JavaScript, and assets
└── requirements.txt   # Python dependencies
```

### Security Features
- AES-256 encryption for all sensitive data
- Automatic session timeout (30 seconds)
- Encrypted credential storage
- Secure password validation
- XSS protection through proper escaping
- CSRF protection through session validation

## Current Development Status
The application is in active development with a solid foundation of core security features implemented. The codebase demonstrates good separation of concerns, comprehensive error handling, and a focus on security best practices. The modular architecture allows for easy extension and maintenance of individual components.

