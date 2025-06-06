// Theme toggle functionality
function toggleTheme() {
    const html = document.documentElement;
    const themeSwitch = document.getElementById('theme-switch');
    const newTheme = themeSwitch.checked ? 'dark' : 'light';
    
    // Update theme
    html.setAttribute('data-theme', newTheme);
    
    // Save preference
    localStorage.setItem('theme', newTheme);
}

// Initialize theme on page load
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const html = document.documentElement;
    const themeSwitch = document.getElementById('theme-switch');
    
    // Set initial theme
    html.setAttribute('data-theme', savedTheme);
    
    // Update checkbox if it exists
    if (themeSwitch) {
        themeSwitch.checked = savedTheme === 'dark';
    }
}

// Run initialization when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeTheme); 