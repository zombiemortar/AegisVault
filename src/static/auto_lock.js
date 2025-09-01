// Auto-Lock Features for AegisVault
class AutoLockManager {
    constructor() {
        this.inactivityTimer = null;
        this.lastActivity = Date.now();
        this.isLocked = false;
        this.preferences = null;
        this.sessionCheckInterval = null;
        
        this.init();
    }

    async init() {
        // Load user preferences
        await this.loadPreferences();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Start session monitoring
        this.startSessionMonitoring();
        
        // Start inactivity monitoring if enabled
        if (this.preferences && this.preferences.lock_on_tab_inactive) {
            this.startInactivityMonitoring();
        }
    }

    async loadPreferences() {
        try {
            const response = await fetch('/api/preferences');
            if (response.ok) {
                this.preferences = await response.json();
            }
        } catch (error) {
            console.error('Failed to load preferences:', error);
            // Use default preferences
            this.preferences = {
                session_timeout: 300,
                lock_on_tab_inactive: true,
                lock_on_window_blur: true,
                lock_on_suspicious_activity: true,
                auto_lock_enabled: true
            };
        }
    }

    setupEventListeners() {
        // Track user activity
        const activityEvents = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
        
        activityEvents.forEach(event => {
            document.addEventListener(event, () => {
                this.updateActivity();
            }, { passive: true });
        });

        // Tab visibility change
        document.addEventListener('visibilitychange', () => {
            if (document.hidden && this.preferences?.lock_on_tab_inactive) {
                this.handleTabInactive();
            }
        });

        // Window focus/blur
        window.addEventListener('blur', () => {
            if (this.preferences?.lock_on_window_blur) {
                this.handleWindowBlur();
            }
        });

        // Suspicious activity detection
        this.setupSuspiciousActivityDetection();
    }

    updateActivity() {
        this.lastActivity = Date.now();
        
        // Reset inactivity timer
        if (this.inactivityTimer) {
            clearTimeout(this.inactivityTimer);
        }
        
        if (this.preferences?.lock_on_tab_inactive) {
            this.inactivityTimer = setTimeout(() => {
                this.handleInactivity();
            }, this.preferences.session_timeout * 1000);
        }
    }

    startInactivityMonitoring() {
        this.updateActivity();
    }

    startSessionMonitoring() {
        // Check session status every 30 seconds
        this.sessionCheckInterval = setInterval(async () => {
            try {
                const response = await fetch('/api/session/status');
                if (response.ok) {
                    const data = await response.json();
                    if (!data.active) {
                        this.lockSession();
                    }
                }
            } catch (error) {
                console.error('Session check failed:', error);
            }
        }, 30000);
    }

    handleInactivity() {
        if (this.preferences?.auto_lock_enabled) {
            this.lockSession();
        }
    }

    handleTabInactive() {
        if (this.preferences?.auto_lock_enabled) {
            this.lockSession();
        }
    }

    handleWindowBlur() {
        if (this.preferences?.auto_lock_enabled) {
            this.lockSession();
        }
    }

    setupSuspiciousActivityDetection() {
        if (!this.preferences?.lock_on_suspicious_activity) {
            return;
        }

        // Detect rapid clicking (potential automated attack)
        let clickCount = 0;
        let clickTimer = null;

        document.addEventListener('click', () => {
            clickCount++;
            
            if (clickTimer) {
                clearTimeout(clickTimer);
            }
            
            clickTimer = setTimeout(() => {
                if (clickCount > 10) { // More than 10 clicks in 1 second
                    this.handleSuspiciousActivity('Rapid clicking detected');
                }
                clickCount = 0;
            }, 1000);
        });

        // Detect rapid key presses
        let keyCount = 0;
        let keyTimer = null;

        document.addEventListener('keydown', () => {
            keyCount++;
            
            if (keyTimer) {
                clearTimeout(keyTimer);
            }
            
            keyTimer = setTimeout(() => {
                if (keyCount > 20) { // More than 20 key presses in 1 second
                    this.handleSuspiciousActivity('Rapid key pressing detected');
                }
                keyCount = 0;
            }, 1000);
        });

        // Detect multiple failed login attempts
        this.detectFailedLogins();
    }

    detectFailedLogins() {
        // This would be implemented on the server side
        // For now, we'll just monitor for multiple form submissions
        let formSubmitCount = 0;
        let formSubmitTimer = null;

        document.addEventListener('submit', (event) => {
            if (event.target.tagName === 'FORM') {
                formSubmitCount++;
                
                if (formSubmitTimer) {
                    clearTimeout(formSubmitTimer);
                }
                
                formSubmitTimer = setTimeout(() => {
                    if (formSubmitCount > 5) { // More than 5 form submissions in 10 seconds
                        this.handleSuspiciousActivity('Multiple form submissions detected');
                    }
                    formSubmitCount = 0;
                }, 10000);
            }
        });
    }

    handleSuspiciousActivity(reason) {
        console.warn('Suspicious activity detected:', reason);
        
        if (this.preferences?.lock_on_suspicious_activity) {
            this.lockSession();
        }
    }

    async lockSession() {
        if (this.isLocked) {
            return;
        }

        this.isLocked = true;
        
        // Clear timers
        if (this.inactivityTimer) {
            clearTimeout(this.inactivityTimer);
        }
        if (this.sessionCheckInterval) {
            clearInterval(this.sessionCheckInterval);
        }

        // Show lock notification
        this.showLockNotification();

        // Redirect to login page after a short delay
        setTimeout(() => {
            window.location.href = '/';
        }, 2000);
    }

    showLockNotification() {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'auto-lock-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <h3>🔒 Session Locked</h3>
                <p>Your session has been locked for security reasons.</p>
                <p>Redirecting to login...</p>
            </div>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            color: white;
            font-family: Arial, sans-serif;
        `;
        
        notification.querySelector('.notification-content').style.cssText = `
            text-align: center;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        `;
        
        document.body.appendChild(notification);
    }

    getRemainingTime() {
        const elapsed = Date.now() - this.lastActivity;
        const remaining = Math.max(0, (this.preferences?.session_timeout || 300) * 1000 - elapsed);
        return Math.ceil(remaining / 1000);
    }

    updatePreferences(newPreferences) {
        this.preferences = { ...this.preferences, ...newPreferences };
        
        // Restart inactivity monitoring if needed
        if (this.inactivityTimer) {
            clearTimeout(this.inactivityTimer);
        }
        
        if (this.preferences.lock_on_tab_inactive) {
            this.startInactivityMonitoring();
        }
        
        // Update window blur event listener
        this.updateWindowBlurListener();
    }
    
    updateWindowBlurListener() {
        // Remove existing listener
        window.removeEventListener('blur', this.handleWindowBlur.bind(this));
        
        // Add new listener if enabled
        if (this.preferences?.lock_on_window_blur) {
            window.addEventListener('blur', () => {
                this.handleWindowBlur();
            });
        }
    }
}

// Initialize auto-lock manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.autoLockManager = new AutoLockManager();
});
