// YouTube SEO AGI Tool - Popup Script

const API_BASE_URL = 'https://youtoubeseo.streamlit.app';

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
      
      analyzeBtn.addEventListener('click', async () => {
        analyzeBtn.disabled = true;
        statusDiv.className = 'status inactive';
        statusText.textContent = '⏳ Analyzing video...';
        
        try {
          // Extract video ID from URL
          const url = new URL(currentTab.url);
          const videoId = url.searchParams.get('v');
          
          if (!videoId) {
            statusText.textContent = '❌ No video ID found in URL';
            analyzeBtn.disabled = false;
            return;
          }
          
          // Get channel handle from content script
          let channelHandle = null;
          try {
            const contentResponse = await chrome.tabs.sendMessage(currentTab.id, { action: 'getChannelHandle' });
            if (contentResponse && contentResponse.channelHandle) {
              channelHandle = contentResponse.channelHandle;
            }
          } catch (e) {
            console.log('Could not get channel handle from content script:', e);
          }
          
          // Request SEO analysis from background script
          const response = await new Promise((resolve, reject) => {
            chrome.runtime.sendMessage({
              action: 'getSEOAnalysis',
              videoId: videoId,
              channelHandle: channelHandle,
              niche: null
            }, (response) => {
              if (chrome.runtime.lastError) {
                reject(new Error(chrome.runtime.lastError.message));
              } else {
                resolve(response);
              }
            });
          });
          
          if (response && response.success && response.data) {
            // Display results in popup
            displayAnalysisResults(response.data, videoId);
            statusDiv.className = 'status active';
            statusText.textContent = '✅ Analysis complete!';
            
            // Also trigger content script to show overlay
            try {
              chrome.tabs.sendMessage(currentTab.id, { 
                action: 'showSEOOverlay', 
                data: response.data,
                additionalData: {} // Can be populated with thumbnail, caption, engagement data
              });
            } catch (e) {
              console.log('Could not send message to content script:', e);
            }
          } else {
            throw new Error(response?.error || 'Unknown error');
          }
        } catch (error) {
          console.error('Analysis error:', error);
          statusDiv.className = 'status inactive';
          
          // Show detailed error message
          let errorMsg = error.message || 'Unknown error';
          if (errorMsg.includes('Failed to fetch') || errorMsg.includes('NetworkError')) {
            errorMsg = 'Network error: Could not connect to server. Please check:\n1. Internet connection\n2. Server URL: ' + API_BASE_URL + '\n3. Server is running';
          } else if (errorMsg.includes('CORS')) {
            errorMsg = 'CORS error: Server does not allow requests from extension. Please check server CORS settings.';
          } else if (errorMsg.includes('parse JSON')) {
            errorMsg = 'Response parsing error: Server returned invalid data. ' + errorMsg;
          }
          
          statusText.textContent = '❌ Error: ' + errorMsg;
          
          // Show error details in console for debugging
          console.error('Full error details:', {
            message: error.message,
            stack: error.stack,
            name: error.name
          });
        } finally {
          analyzeBtn.disabled = false;
        }
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
      const dashboardUrl = result.dashboardUrl || 'https://youtoubeseo.streamlit.app';
      chrome.tabs.create({ url: dashboardUrl });
    });
  });
  
  // Display analysis results in popup
  function displayAnalysisResults(data, videoId) {
    // Create results container if it doesn't exist
    let resultsDiv = document.getElementById('analysis-results');
    if (!resultsDiv) {
      resultsDiv = document.createElement('div');
      resultsDiv.id = 'analysis-results';
      resultsDiv.style.cssText = `
        margin-top: 1rem;
        padding: 1rem;
        background: rgba(58, 63, 75, 0.3);
        border-radius: 8px;
        border: 1px solid #3a3f4b;
        max-height: 400px;
        overflow-y: auto;
      `;
      document.querySelector('.features').parentNode.insertBefore(resultsDiv, document.querySelector('.features'));
    }
    
    const score = data.seo_score || 0;
    const scoreColor = score >= 80 ? '#4caf50' : score >= 60 ? '#ffc107' : '#f44336';
    
    resultsDiv.innerHTML = `
      <div style="margin-bottom: 1rem;">
        <div style="font-size: 2rem; font-weight: bold; color: ${scoreColor}; text-align: center; margin-bottom: 0.5rem;">
          ${score}/100
        </div>
        <div style="text-align: center; color: #b0b0b0; font-size: 0.85rem;">SEO Score</div>
      </div>
      
      ${data.title_suggestions && data.title_suggestions.length > 0 ? `
        <div style="margin-bottom: 1rem;">
          <div style="font-weight: 600; margin-bottom: 0.5rem; color: #4a9eff;">📝 Title Suggestions:</div>
          <div style="font-size: 0.9rem; color: #fafafa;">
            ${data.title_suggestions.slice(0, 3).map((title, i) => 
              `<div style="margin-bottom: 0.5rem; padding: 0.5rem; background: rgba(74, 158, 255, 0.1); border-radius: 4px;">
                ${i + 1}. ${title}
              </div>`
            ).join('')}
          </div>
        </div>
      ` : ''}
      
      ${data.description ? `
        <div style="margin-bottom: 1rem;">
          <div style="font-weight: 600; margin-bottom: 0.5rem; color: #4a9eff;">📄 Description:</div>
          <div style="font-size: 0.85rem; color: #b0b0b0; max-height: 100px; overflow-y: auto; padding: 0.5rem; background: rgba(58, 63, 75, 0.2); border-radius: 4px;">
            ${data.description.substring(0, 200)}${data.description.length > 200 ? '...' : ''}
          </div>
        </div>
      ` : ''}
      
      ${data.tags && data.tags.length > 0 ? `
        <div style="margin-bottom: 1rem;">
          <div style="font-weight: 600; margin-bottom: 0.5rem; color: #4a9eff;">🏷️ Tags:</div>
          <div style="font-size: 0.85rem; color: #fafafa; display: flex; flex-wrap: wrap; gap: 0.25rem;">
            ${data.tags.slice(0, 10).map(tag => 
              `<span style="padding: 0.25rem 0.5rem; background: rgba(74, 158, 255, 0.2); border-radius: 4px; border: 1px solid #4a9eff;">
                ${tag}
              </span>`
            ).join('')}
          </div>
        </div>
      ` : ''}
      
      ${data.recommendations && data.recommendations.length > 0 ? `
        <div style="margin-bottom: 1rem;">
          <div style="font-weight: 600; margin-bottom: 0.5rem; color: #4a9eff;">💡 Recommendations:</div>
          <ul style="font-size: 0.85rem; color: #b0b0b0; padding-left: 1.5rem;">
            ${data.recommendations.slice(0, 3).map(rec => `<li style="margin-bottom: 0.25rem;">${rec}</li>`).join('')}
          </ul>
        </div>
      ` : ''}
      
      <div style="text-align: center; margin-top: 1rem;">
        <a href="https://youtoubeseo.streamlit.app" target="_blank" style="color: #4a9eff; text-decoration: none; font-size: 0.9rem;">
          View Full Analysis →
        </a>
      </div>
    `;
  }
  
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

