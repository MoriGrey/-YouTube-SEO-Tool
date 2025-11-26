// vidIQ-like Platform - Enhanced Dashboard JavaScript

// Theme Management
(function() {
    'use strict';
    
    // Initialize theme from localStorage or default to dark
    function initTheme() {
        const savedTheme = localStorage.getItem('dashboard-theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeToggleIcon(savedTheme);
    }
    
    // Toggle theme
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('dashboard-theme', newTheme);
        updateThemeToggleIcon(newTheme);
    }
    
    // Update theme toggle icon
    function updateThemeToggleIcon(theme) {
        const icon = document.querySelector('.theme-toggle-icon');
        if (icon) {
            icon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }
    
    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTheme);
    } else {
        initTheme();
    }
    
    // Expose toggle function globally
    window.toggleTheme = toggleTheme;
    
    // Add theme toggle button if it doesn't exist
    function addThemeToggleButton() {
        if (!document.querySelector('.theme-toggle')) {
            const toggleBtn = document.createElement('div');
            toggleBtn.className = 'theme-toggle';
            toggleBtn.innerHTML = '<span class="theme-toggle-icon">🌙</span>';
            toggleBtn.onclick = toggleTheme;
            toggleBtn.title = 'Toggle theme';
            document.body.appendChild(toggleBtn);
        }
    }
    
    // Wait for Streamlit to load, then add button
    setTimeout(addThemeToggleButton, 1000);
})();

// Loading States
(function() {
    'use strict';
    
    // Show loading overlay
    window.showLoading = function(message = 'Loading...') {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.id = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="loading-spinner" style="margin: 0 auto 1rem;"></div>
                <p style="color: var(--text-primary); margin: 0;">${message}</p>
            </div>
        `;
        document.body.appendChild(overlay);
    };
    
    // Hide loading overlay
    window.hideLoading = function() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    };
})();

// Keyboard Shortcuts
(function() {
    'use strict';
    
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K: Search (placeholder)
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            // TODO: Implement search functionality
            console.log('Search shortcut pressed');
        }
        
        // Ctrl/Cmd + /: Show keyboard shortcuts help
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            // TODO: Show help modal
            console.log('Help shortcut pressed');
        }
        
        // Escape: Close modals/overlays
        if (e.key === 'Escape') {
            window.hideLoading();
        }
    });
})();

// Smooth Scroll
(function() {
    'use strict';
    
    window.smoothScrollTo = function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    };
})();

// Tooltip Enhancement
(function() {
    'use strict';
    
    // Auto-initialize tooltips for elements with data-tooltip attribute
    document.addEventListener('DOMContentLoaded', function() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        tooltipElements.forEach(function(el) {
            if (!el.classList.contains('tooltip-wrapper')) {
                el.classList.add('tooltip-wrapper');
                const tooltipText = el.getAttribute('data-tooltip');
                const tooltip = document.createElement('span');
                tooltip.className = 'tooltip';
                tooltip.textContent = tooltipText;
                el.appendChild(tooltip);
            }
        });
    });
})();

// Export functionality
window.exportData = function(data, filename, type = 'json') {
    let content, mimeType, extension;
    
    switch(type) {
        case 'json':
            content = JSON.stringify(data, null, 2);
            mimeType = 'application/json';
            extension = 'json';
            break;
        case 'csv':
            // Simple CSV conversion (for arrays of objects)
            if (Array.isArray(data) && data.length > 0) {
                const headers = Object.keys(data[0]);
                const rows = data.map(row => 
                    headers.map(header => JSON.stringify(row[header] || '')).join(',')
                );
                content = [headers.join(','), ...rows].join('\n');
            } else {
                content = '';
            }
            mimeType = 'text/csv';
            extension = 'csv';
            break;
        default:
            console.error('Unsupported export type:', type);
            return;
    }
    
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${filename}.${extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
};

// API Key Persistence
(function() {
    'use strict';
    
    // Save API key to localStorage (encrypted)
    window.saveAPIKey = function(apiKey) {
        try {
            // Simple base64 encoding (not real encryption, but better than plaintext)
            const encoded = btoa(apiKey);
            localStorage.setItem('youtube_api_key', encoded);
            localStorage.setItem('youtube_api_key_timestamp', Date.now().toString());
            console.log('API key saved to localStorage');
        } catch (e) {
            console.error('Failed to save API key:', e);
        }
    };
    
    // Load API key from localStorage
    window.loadAPIKey = function() {
        try {
            const encoded = localStorage.getItem('youtube_api_key');
            if (encoded) {
                const decoded = atob(encoded);
                return decoded;
            }
        } catch (e) {
            console.error('Failed to load API key:', e);
        }
        return null;
    };
    
    // Clear API key from localStorage
    window.clearAPIKey = function() {
        try {
            localStorage.removeItem('youtube_api_key');
            localStorage.removeItem('youtube_api_key_timestamp');
            console.log('API key cleared from localStorage');
        } catch (e) {
            console.error('Failed to clear API key:', e);
        }
    };
    
    // Auto-fill API key input on page load
    function autoFillAPIKey() {
        // Wait for Streamlit to fully load
        setTimeout(() => {
            const apiKey = loadAPIKey();
            if (apiKey) {
                // Find API key input field
                const inputs = document.querySelectorAll('input[type="password"]');
                inputs.forEach(input => {
                    // Check if this is the API key input (by placeholder or label)
                    const placeholder = input.getAttribute('placeholder') || '';
                    const ariaLabel = input.getAttribute('aria-label') || '';
                    if (placeholder.toLowerCase().includes('api') || 
                        ariaLabel.toLowerCase().includes('api') ||
                        input.id === 'api_key_input') {
                        // Only fill if empty
                        if (!input.value || input.value.length === 0) {
                            input.value = apiKey;
                            // Trigger input event
                            input.dispatchEvent(new Event('input', { bubbles: true }));
                            input.dispatchEvent(new Event('change', { bubbles: true }));
                            console.log('API key auto-filled from localStorage');
                        }
                    }
                });
            }
        }, 1000);
    }
    
    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', autoFillAPIKey);
    } else {
        autoFillAPIKey();
    }
    
    // Also try after Streamlit reruns
    const observer = new MutationObserver(() => {
        autoFillAPIKey();
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
})();

// Console log for debugging
console.log('vidIQ-like Platform Dashboard JS loaded');

