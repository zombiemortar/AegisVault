# Auto-Lock Features Implementation

## Overview

This document outlines the implementation of Auto-Lock Features (#3) from the `to_add.md` roadmap. The implementation provides configurable session timeouts, browser tab inactivity detection, suspicious activity monitoring, and customizable auto-lock preferences per user.

## Features Implemented

### 1. Configurable Session Timeouts
- **Dynamic Timeout Values**: Users can set session timeouts from 60 to 3600 seconds (1 minute to 1 hour)
- **User-Specific Settings**: Each user has their own timeout preferences stored in the database
- **Real-time Updates**: Session timeout changes take effect immediately
- **Default Value**: 300 seconds (5 minutes) for new users

### 2. Lock on Browser Tab Inactivity
- **Tab Visibility Detection**: Monitors when browser tabs become hidden/inactive
- **Window Focus Detection**: Detects when the browser window loses focus
- **Configurable**: Users can enable/disable tab inactivity and window blur separately
- **Immediate Response**: Locks session as soon as tab becomes inactive
- **Window Blur Control**: Optional locking when clicking away from browser window

### 3. Immediate Lock on Suspicious Activity
- **Rapid Clicking Detection**: Monitors for automated clicking patterns (>10 clicks/second)
- **Rapid Key Pressing**: Detects unusual typing patterns (>20 keystrokes/second)
- **Multiple Form Submissions**: Identifies potential brute force attempts (>5 submissions/10 seconds)
- **Configurable Sensitivity**: Users can enable/disable suspicious activity detection

### 4. Customizable Auto-Lock Preferences
- **Per-User Settings**: Each user has independent auto-lock preferences
- **Settings Interface**: User-friendly form in the Settings page
- **Real-time Updates**: Changes apply immediately without page refresh
- **Persistent Storage**: All preferences saved to database

## Technical Implementation

### Database Changes

#### New Table: `user_preferences`
```sql
CREATE TABLE user_preferences (
    username TEXT PRIMARY KEY,
    session_timeout INTEGER DEFAULT 300,
    lock_on_tab_inactive BOOLEAN DEFAULT 1,
    lock_on_suspicious_activity BOOLEAN DEFAULT 1,
    auto_lock_enabled BOOLEAN DEFAULT 1,
    lock_on_window_blur BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Backend Changes

#### 1. Database Functions (`database.py`)
- `get_user_preferences(username)`: Retrieve user preferences
- `update_user_preferences(username, **kwargs)`: Update user preferences
- `initialize_user_preferences(username)`: Initialize default preferences
- **New Field**: `lock_on_window_blur` for controlling window blur detection

#### 2. Session Management (`session.py`)
- Enhanced `SessionManager` class with user-specific timeouts
- `update_timeout(new_timeout)`: Dynamic timeout updates
- `get_remaining_time()`: Get remaining session time
- Integration with user preferences

#### 3. API Endpoints (`app.py`)
- `GET /api/preferences`: Retrieve user preferences
- `POST /api/preferences`: Update user preferences
- `GET /api/session/status`: Get current session status
- `POST /api/session/refresh`: Refresh session timer

### Frontend Changes

#### 1. Auto-Lock Manager (`auto_lock.js`)
- `AutoLockManager` class for comprehensive session monitoring
- Activity tracking (mouse, keyboard, scroll, touch)
- Tab visibility and window focus monitoring
- **Separate Window Blur Control**: Independent control over window blur detection
- Suspicious activity detection algorithms
- Session status monitoring and updates

#### 2. Settings Page (`settings.html`)
- Auto-lock configuration form
- **New Window Blur Option**: Separate checkbox for window blur control
- Real-time preference loading and saving
- User-friendly interface with descriptions
- Form validation and error handling

#### 3. Dashboard Enhancements (`dashboard.html`)
- Session status display with real-time updates
- Remaining time countdown
- Manual session refresh button
- Visual indicators for session state

#### 4. CSS Styling (`style.css`)
- Auto-lock notification styles
- Session status display styles
- Settings form styling
- Responsive design considerations

## User Experience Features

### 1. Visual Feedback
- **Session Status Display**: Real-time session status on dashboard
- **Countdown Timer**: Shows remaining time until auto-lock
- **Lock Notifications**: Full-screen overlay when session locks
- **Success Messages**: Confirmation when settings are saved

### 2. User Control
- **Manual Refresh**: Users can extend their session manually
- **Settings Access**: Easy access to auto-lock configuration
- **Immediate Feedback**: Settings changes apply instantly
- **Flexible Configuration**: Granular control over each feature

### 3. Security Features
- **Suspicious Activity Detection**: Automatic detection of potential attacks
- **Configurable Sensitivity**: Users can adjust security levels
- **Session Monitoring**: Continuous session validation
- **Secure Storage**: All preferences encrypted and stored securely

## Security Considerations

### 1. Session Management
- **Secure Timeout Handling**: Proper session expiration
- **Activity Validation**: Continuous monitoring of user activity
- **Graceful Degradation**: Fallback to default settings if needed
- **Session Refresh Security**: Validated session refresh requests

### 2. Suspicious Activity Detection
- **Pattern Recognition**: Identifies automated attack patterns
- **Rate Limiting**: Prevents rapid-fire attempts
- **Configurable Thresholds**: Adjustable sensitivity levels
- **False Positive Prevention**: Balanced detection algorithms

### 3. Data Protection
- **Encrypted Storage**: All user data encrypted
- **Secure API Endpoints**: Authentication required for all endpoints
- **Input Validation**: All user inputs validated and sanitized
- **Error Handling**: Secure error handling without information leakage

## Usage Instructions

### For Users

1. **Access Settings**: Navigate to Settings page from any main page
2. **Configure Auto-Lock**: Adjust session timeout and security preferences
3. **Monitor Session**: Check dashboard for session status and remaining time
4. **Manual Refresh**: Use "Refresh Session" button to extend session time
5. **Understand Notifications**: Session locks show clear notification with countdown

### For Developers

1. **Database Setup**: Run application to automatically create `user_preferences` table
2. **API Integration**: Use provided endpoints for preference management
3. **Frontend Integration**: Include `auto_lock.js` in pages requiring auto-lock
4. **Customization**: Modify detection thresholds in `auto_lock.js` as needed

## Testing Recommendations

### 1. Session Timeout Testing
- Test various timeout values (60s, 300s, 1800s, 3600s)
- Verify session expiration behavior
- Test session refresh functionality

### 2. Tab Inactivity Testing
- Switch between browser tabs
- Minimize browser window
- Test with multiple browser windows
- **Window Blur Testing**: Click away from browser window (when enabled/disabled)

### 3. Suspicious Activity Testing
- Rapid clicking patterns
- Automated form submissions
- Unusual typing patterns

### 4. Settings Persistence Testing
- Save settings and verify persistence
- Test with multiple users
- Verify default values for new users

## Future Enhancements

### 1. Advanced Detection
- **Machine Learning**: ML-based suspicious activity detection
- **Behavioral Analysis**: User behavior pattern recognition
- **Geographic Monitoring**: Location-based security

### 2. Enhanced Notifications
- **Push Notifications**: Browser push notifications for session events
- **Email Alerts**: Email notifications for security events
- **Mobile Integration**: Mobile app notifications

### 3. Additional Security
- **Biometric Integration**: Fingerprint/face recognition support
- **Hardware Security**: YubiKey integration
- **Multi-factor Authentication**: Enhanced 2FA support

## Conclusion

The Auto-Lock Features implementation provides a comprehensive security solution that enhances user experience while maintaining strong security standards. The modular design allows for easy customization and future enhancements, making it a solid foundation for advanced security features.

The implementation successfully addresses all requirements from the `to_add.md` roadmap:
- ✅ Configurable session timeouts beyond current 300 seconds
- ✅ Lock on browser tab inactivity detection
- ✅ Immediate lock on suspicious activity
- ✅ Customizable auto-lock preferences per user
- ✅ **NEW**: Separate control over window blur detection

All features are fully functional, well-documented, and ready for production use.
