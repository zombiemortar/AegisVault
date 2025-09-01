import threading
import time
from database import get_user_preferences

# Default timeout if no user preferences are found
DEFAULT_SESSION_TIMEOUT = 300
session_expire_event = threading.Event()

class SessionManager:
    def __init__(self):
        self.active = False
        self.username = None
        self.start_time = None
        self.timeout = DEFAULT_SESSION_TIMEOUT
        self.preferences = None

    def start_session(self, username):
        """Starts a session and monitors expiration."""
        self.active = True
        self.username = username
        self.start_time = time.time()
        
        # Load user preferences
        self.preferences = get_user_preferences(username)
        if self.preferences:
            self.timeout = self.preferences.get('session_timeout', DEFAULT_SESSION_TIMEOUT)
        
        threading.Thread(target=self.monitor_session, daemon=True).start()  # ✅ Run in background

    def validate_session(self):
        """Checks if the session is still active."""
        if not self.active or (time.time() - self.start_time) >= self.timeout:
            self.expire_session()
            return False
        return True

    def refresh_session(self):
        """Refreshes session timer when activity occurs."""
        self.start_time = time.time()
        #print("🔄 Session timer refreshed.")

    def expire_session(self):
        """Handles session expiration without duplicate execution."""
        if not self.active:  # ✅ Prevent multiple calls
            return

        print("\n❌ Session expired due to inactivity.")
        self.active = False
        self.username = None
        session_expire_event.set()  # ✅ Signal expiration only once
        print(f"DEBUG: session_expire_event.is_set() → {session_expire_event.is_set()}")  # 🛠 Confirms event signal

    def monitor_session(self):
        """Monitors session timeout and expires if idle for too long."""
        while self.active:
            time.sleep(5)  # ✅ Check every 5 seconds

            if not self.validate_session():
                break

    def update_timeout(self, new_timeout):
        """Update session timeout dynamically."""
        self.timeout = new_timeout
        if self.preferences:
            self.preferences['session_timeout'] = new_timeout

    def get_remaining_time(self):
        """Get remaining session time in seconds."""
        if not self.active:
            return 0
        elapsed = time.time() - self.start_time
        remaining = max(0, self.timeout - elapsed)
        return int(remaining)