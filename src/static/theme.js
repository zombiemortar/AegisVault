// Enhanced Theme Management with System Preference Detection
class ThemeManager {
    constructor() {
        this.currentTheme = 'dark';
        this.systemPrefersDark = false;
        this.followSystem = true;
        this.init();
    }

    init() {
        this.detectSystemPreference();
        this.loadSavedPreferences();
        this.applyTheme();
        this.setupEventListeners();
        this.setupSystemPreferenceListener();
    }

    detectSystemPreference() {
        // Check if system prefers dark mode
        this.systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    loadSavedPreferences() {
        const savedTheme = localStorage.getItem('theme');
        const savedFollowSystem = localStorage.getItem('followSystem');
        
        if (savedFollowSystem !== null) {
            this.followSystem = savedFollowSystem === 'true';
        }
        
        if (savedTheme && !this.followSystem) {
            this.currentTheme = savedTheme;
        } else if (this.followSystem) {
            this.currentTheme = this.systemPrefersDark ? 'dark' : 'light';
        }
    }

    applyTheme() {
        const html = document.documentElement;
        html.setAttribute('data-theme', this.currentTheme);
        
        // Update theme switch if it exists
        const themeSwitch = document.getElementById('theme-switch');
        if (themeSwitch) {
            themeSwitch.checked = this.currentTheme === 'dark';
        }

        // Update follow system checkbox if it exists
        const followSystemCheckbox = document.getElementById('follow-system');
        if (followSystemCheckbox) {
            followSystemCheckbox.checked = this.followSystem;
        }

        // Trigger custom event for other components
        document.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { theme: this.currentTheme, followSystem: this.followSystem }
        }));
    }

    setupEventListeners() {
        // Theme switch event listener
        const themeSwitch = document.getElementById('theme-switch');
        if (themeSwitch) {
            themeSwitch.addEventListener('change', () => {
                this.toggleTheme();
            });
        }

        // Follow system preference checkbox
        const followSystemCheckbox = document.getElementById('follow-system');
        if (followSystemCheckbox) {
            followSystemCheckbox.addEventListener('change', () => {
                this.setFollowSystem(followSystemCheckbox.checked);
            });
        }
    }

    setupSystemPreferenceListener() {
        // Listen for system theme changes
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        
        mediaQuery.addEventListener('change', (e) => {
            this.systemPrefersDark = e.matches;
            if (this.followSystem) {
                this.currentTheme = this.systemPrefersDark ? 'dark' : 'light';
                this.applyTheme();
                this.savePreferences();
            }
        });
    }

    toggleTheme() {
        if (this.followSystem) {
            // If following system, toggle between system preference and opposite
            this.currentTheme = this.systemPrefersDark ? 'light' : 'dark';
            this.followSystem = false;
        } else {
            // Toggle between light and dark
            this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        }
        
        this.applyTheme();
        this.savePreferences();
    }

    setFollowSystem(follow) {
        this.followSystem = follow;
        
        if (follow) {
            this.currentTheme = this.systemPrefersDark ? 'dark' : 'light';
        }
        
        this.applyTheme();
        this.savePreferences();
    }

    setTheme(theme) {
        this.currentTheme = theme;
        this.followSystem = false;
        this.applyTheme();
        this.savePreferences();
    }

    savePreferences() {
        localStorage.setItem('theme', this.currentTheme);
        localStorage.setItem('followSystem', this.followSystem.toString());
    }

    getCurrentTheme() {
        return this.currentTheme;
    }

    isFollowingSystem() {
        return this.followSystem;
    }

    getSystemPreference() {
        return this.systemPrefersDark ? 'dark' : 'light';
    }
}

// Legacy function for backward compatibility
function toggleTheme() {
    if (window.themeManager) {
        window.themeManager.toggleTheme();
    }
}

// Initialize theme on page load
function initializeTheme() {
    window.themeManager = new ThemeManager();
}

// Run initialization when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeTheme);

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
} 