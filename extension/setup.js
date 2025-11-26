// Setup script for extension configuration
// Run this once to configure API URLs

// Configuration
const CONFIG = {
  // Update these with your actual URLs
  apiBaseUrl: 'https://your-app-url.streamlit.app/api',
  dashboardUrl: 'https://your-app-url.streamlit.app'
};

// Update background.js
function updateBackgroundJs() {
  console.log('Updating background.js...');
  // This would be done manually by editing the file
  console.log('Please update API_BASE_URL in background.js to:', CONFIG.apiBaseUrl);
}

// Update content.js
function updateContentJs() {
  console.log('Updating content.js...');
  // This would be done manually by editing the file
  console.log('Please update apiBaseUrl in content.js to:', CONFIG.apiBaseUrl);
}

// Save to Chrome storage
function saveToStorage() {
  chrome.storage.sync.set({
    apiBaseUrl: CONFIG.apiBaseUrl,
    dashboardUrl: CONFIG.dashboardUrl
  }, () => {
    console.log('Configuration saved to Chrome storage');
  });
}

// Instructions
console.log(`
╔══════════════════════════════════════════════════════════════╗
║  YouTube SEO AGI Tool - Extension Setup                     ║
╚══════════════════════════════════════════════════════════════╝

1. Update API URLs in the following files:
   - extension/background.js (line ~8)
   - extension/content.js (line ~8)
   - extension/popup.js (line ~50)

2. Replace 'https://your-app-url.streamlit.app' with your actual URL

3. Reload the extension in chrome://extensions/

4. Test on YouTube!
`);

