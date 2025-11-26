// YouTube SEO AGI Tool - Popup Script

document.addEventListener('DOMContentLoaded', () => {
  const statusDiv = document.getElementById('status');
  const statusText = document.getElementById('status-text');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const settingsBtn = document.getElementById('settingsBtn');
  const dashboardBtn = document.getElementById('dashboardBtn');
  
  // Check if on YouTube video page
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTab = tabs[0];
    const isYouTube = currentTab.url && currentTab.url.includes('youtube.com/watch');
    
    if (isYouTube) {
      statusDiv.className = 'status active';
      statusDiv.querySelector('.status-icon').textContent = '✅';
      statusText.textContent = 'Ready to analyze';
      
      analyzeBtn.addEventListener('click', () => {
        // Send message to content script to analyze
        chrome.tabs.sendMessage(currentTab.id, { action: 'analyzeVideo' }, (response) => {
          if (chrome.runtime.lastError) {
            statusText.textContent = 'Error: ' + chrome.runtime.lastError.message;
          } else {
            statusText.textContent = 'Analysis complete!';
          }
        });
      });
    } else {
      statusDiv.className = 'status inactive';
      statusDiv.querySelector('.status-icon').textContent = '⚠️';
      statusText.textContent = 'Please navigate to a YouTube video page';
      analyzeBtn.disabled = true;
    }
  });
  
  // Settings button
  settingsBtn.addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });
  
  // Dashboard button
  dashboardBtn.addEventListener('click', () => {
    // Get dashboard URL from storage or use default
    chrome.storage.sync.get(['dashboardUrl'], (result) => {
      const dashboardUrl = result.dashboardUrl || 'https://your-app-url.streamlit.app';
      chrome.tabs.create({ url: dashboardUrl });
    });
  });
  
  // Auto-fill button (if on YouTube Studio)
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTab = tabs[0];
    const isStudio = currentTab.url && currentTab.url.includes('studio.youtube.com');
    
    if (isStudio) {
      const autoFillBtn = document.createElement('button');
      autoFillBtn.className = 'button';
      autoFillBtn.textContent = '✨ Auto-Fill Form';
      autoFillBtn.id = 'autofillBtn';
      autoFillBtn.style.marginTop = '0.5rem';
      
      autoFillBtn.addEventListener('click', () => {
        // Send message to content script to trigger auto-fill
        chrome.tabs.sendMessage(currentTab.id, { action: 'autoFill' }, (response) => {
          if (chrome.runtime.lastError) {
            statusText.textContent = 'Error: ' + chrome.runtime.lastError.message;
          } else {
            statusText.textContent = 'Auto-fill triggered!';
          }
        });
      });
      
      document.querySelector('.features').appendChild(autoFillBtn);
    }
  });
});

