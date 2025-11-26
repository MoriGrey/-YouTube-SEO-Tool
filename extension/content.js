// YouTube SEO AGI Tool - Content Script
// Injects SEO data and optimization suggestions into YouTube pages
// Also provides auto-fill functionality for YouTube Studio

(function() {
  'use strict';
  
  // Configuration
  const CONFIG = {
    apiBaseUrl: 'https://your-app-url.streamlit.app', // TODO: Update with actual URL (no /api)
    showSEOOverlay: true,
    showKeywordSuggestions: true,
    autoFillEnabled: true, // Enable auto-fill feature
    autoFillDelay: 500 // Delay before auto-filling (ms)
  };
  
  // Extract video ID from URL
  function getVideoId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('v');
  }
  
  // Extract channel handle from page
  function getChannelHandle() {
    // Try multiple selectors for channel handle
    const channelLink = document.querySelector('ytd-channel-name a, ytd-video-owner-renderer a');
    if (channelLink) {
      const href = channelLink.getAttribute('href');
      if (href) {
        const match = href.match(/\/(?:c|channel|user|@)([^\/]+)/);
        if (match) {
          return match[1].replace('@', '');
        }
      }
    }
    return null;
  }
  
  // Check if we're on YouTube Studio
  function isYouTubeStudio() {
    return window.location.hostname.includes('studio.youtube.com') || 
           window.location.pathname.includes('/studio');
  }
  
  // Check if we're on YouTube video watch page
  function isVideoWatchPage() {
    return window.location.pathname === '/watch' && getVideoId();
  }
  
  // Auto-fill YouTube Studio form fields
  function autoFillYouTubeStudio(data, additionalData = {}) {
    if (!CONFIG.autoFillEnabled) return;
    
    // Wait for form to load
    setTimeout(() => {
      let filledCount = 0;
      
      // Title field - try multiple selectors
      const titleSelectors = [
        'input[aria-label*="Title" i]',
        'input[name*="title" i]',
        '#textbox[aria-label*="Title" i]',
        'ytd-text-input-renderer input',
        'input[placeholder*="title" i]',
        'ytd-text-input-renderer #text-input'
      ];
      
      let titleField = null;
      for (const selector of titleSelectors) {
        titleField = document.querySelector(selector);
        if (titleField && titleField.offsetParent !== null) { // Check if visible
          break;
        }
      }
      
      if (titleField && data.title_suggestions && data.title_suggestions.length > 0) {
        const bestTitle = data.title_suggestions[0];
        if (!titleField.value || titleField.value.trim().length < bestTitle.length) {
          // Clear and set value
          titleField.value = '';
          titleField.focus();
          titleField.value = bestTitle;
          
          // Trigger events
          titleField.dispatchEvent(new Event('input', { bubbles: true }));
          titleField.dispatchEvent(new Event('change', { bubbles: true }));
          titleField.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
          
          filledCount++;
          console.log('✅ Auto-filled title');
        }
      }
      
      // Description field - try multiple selectors
      const descSelectors = [
        'textarea[aria-label*="Description" i]',
        'textarea[name*="description" i]',
        '#textbox[aria-label*="Description" i]',
        'ytd-textarea-renderer textarea',
        'textarea[placeholder*="description" i]',
        'ytd-textarea-renderer #textarea'
      ];
      
      let descriptionField = null;
      for (const selector of descSelectors) {
        descriptionField = document.querySelector(selector);
        if (descriptionField && descriptionField.offsetParent !== null) {
          break;
        }
      }
      
      if (descriptionField && data.description) {
        if (!descriptionField.value || descriptionField.value.length < 100) {
          descriptionField.value = '';
          descriptionField.focus();
          descriptionField.value = data.description;
          
          // Trigger events
          descriptionField.dispatchEvent(new Event('input', { bubbles: true }));
          descriptionField.dispatchEvent(new Event('change', { bubbles: true }));
          descriptionField.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
          
          filledCount++;
          console.log('✅ Auto-filled description');
        }
      }
      
      // Tags field - YouTube uses chip-based input
      const tagSelectors = [
        'input[aria-label*="Tag" i]',
        'input[name*="tag" i]',
        '#chips-input input',
        'yt-chip-cloud-renderer input',
        'input[placeholder*="tag" i]'
      ];
      
      let tagsField = null;
      for (const selector of tagSelectors) {
        tagsField = document.querySelector(selector);
        if (tagsField && tagsField.offsetParent !== null) {
          break;
        }
      }
      
      if (tagsField && data.tags && data.tags.length > 0) {
        // Add tags one by one (YouTube chip system)
        const tagsToAdd = data.tags.slice(0, 15);
        tagsToAdd.forEach((tag, index) => {
          setTimeout(() => {
            tagsField.focus();
            tagsField.value = tag;
            tagsField.dispatchEvent(new Event('input', { bubbles: true }));
            tagsField.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', bubbles: true }));
            tagsField.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', bubbles: true }));
          }, index * 200); // Delay between tags
        });
        
        filledCount++;
        console.log('✅ Auto-filled tags');
      }
      
      // Show notification
      if (filledCount > 0) {
        showAutoFillNotification(`✅ Auto-filled ${filledCount} field(s) from SEO analysis`);
      } else {
        showAutoFillNotification('⚠️ Could not find form fields. Please ensure you are on the video edit page.');
      }
    }, CONFIG.autoFillDelay);
  }
  
  // Show auto-fill notification
  function showAutoFillNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'youtube-seo-autofill-notification';
    notification.innerHTML = `
      <div class="youtube-seo-notification-content">
        <span class="youtube-seo-notification-icon">✅</span>
        <span class="youtube-seo-notification-text">${message}</span>
        <button class="youtube-seo-notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
      </div>
    `;
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
      }
    }, 5000);
  }
  
  // Create SEO overlay
  function createSEOOverlay(seoData, additionalData = {}) {
    const overlay = document.createElement('div');
    overlay.id = 'youtube-seo-overlay';
    overlay.className = 'youtube-seo-overlay';
    
    const score = seoData.seo_score || 0;
    const scoreColor = score >= 80 ? '#4caf50' : score >= 60 ? '#ffc107' : '#f44336';
    
    // Additional scores
    const thumbnailScore = additionalData.thumbnail_score || seoData.thumbnail_score || 0;
    const captionScore = additionalData.caption_score || 0;
    
    // Tabs for different sections
    const hasTabs = isVideoWatchPage() && !isYouTubeStudio();
    
    overlay.innerHTML = `
      <div class="youtube-seo-header">
        <span class="youtube-seo-title">🎸 SEO Analysis</span>
        <button class="youtube-seo-close" onclick="this.parentElement.parentElement.remove()">×</button>
      </div>
      ${hasTabs ? `
        <div class="youtube-seo-tabs">
          <button class="youtube-seo-tab active" data-tab="overview">Overview</button>
          <button class="youtube-seo-tab" data-tab="similar">Similar Videos</button>
          <button class="youtube-seo-tab" data-tab="details">Details</button>
        </div>
      ` : ''}
      <div class="youtube-seo-content" id="seo-content-overview">
        <div class="youtube-seo-score" style="color: ${scoreColor}">
          ${score}/100
        </div>
        <div class="youtube-seo-breakdown">
          <div class="youtube-seo-item">
            <span>Title:</span>
            <span class="youtube-seo-value ${seoData.title_score >= 80 ? 'good' : seoData.title_score >= 60 ? 'medium' : 'poor'}">
              ${seoData.title_score || 0}/100
            </span>
          </div>
          <div class="youtube-seo-item">
            <span>Description:</span>
            <span class="youtube-seo-value ${seoData.description_score >= 80 ? 'good' : seoData.description_score >= 60 ? 'medium' : 'poor'}">
              ${seoData.description_score || 0}/100
            </span>
          </div>
          <div class="youtube-seo-item">
            <span>Tags:</span>
            <span class="youtube-seo-value ${seoData.tags_score >= 80 ? 'good' : seoData.tags_score >= 60 ? 'medium' : 'poor'}">
              ${seoData.tags_score || 0}/100
            </span>
          </div>
          ${thumbnailScore > 0 ? `
            <div class="youtube-seo-item">
              <span>Thumbnail:</span>
              <span class="youtube-seo-value ${thumbnailScore >= 80 ? 'good' : thumbnailScore >= 60 ? 'medium' : 'poor'}">
                ${thumbnailScore}/100
              </span>
            </div>
          ` : ''}
          ${captionScore > 0 ? `
            <div class="youtube-seo-item">
              <span>Captions:</span>
              <span class="youtube-seo-value ${captionScore >= 80 ? 'good' : captionScore >= 60 ? 'medium' : 'poor'}">
                ${captionScore}/100
              </span>
            </div>
          ` : ''}
        </div>
        ${seoData.recommendations && seoData.recommendations.length > 0 ? `
          <div class="youtube-seo-recommendations">
            <strong>💡 Quick Tips:</strong>
            <ul>
              ${seoData.recommendations.slice(0, 3).map(rec => `<li>${rec}</li>`).join('')}
            </ul>
          </div>
        ` : ''}
        <div class="youtube-seo-actions">
          <button class="youtube-seo-btn youtube-seo-btn-primary" id="autofill-btn">
            ${isYouTubeStudio() ? '✨ Auto-Fill Form' : '📋 Copy to Studio'}
          </button>
          ${!isYouTubeStudio() ? `
            <button class="youtube-seo-btn youtube-seo-btn-secondary" id="copy-all-btn">
              📄 Copy All Suggestions
            </button>
          ` : ''}
          <a href="${CONFIG.apiBaseUrl.replace('/api', '')}" target="_blank" class="youtube-seo-link">
            View Full Analysis →
          </a>
        </div>
      </div>
      ${hasTabs ? `
        <div class="youtube-seo-content hidden" id="seo-content-similar">
          <div class="youtube-seo-loading">Loading similar videos...</div>
        </div>
        <div class="youtube-seo-content hidden" id="seo-content-details">
          <div class="youtube-seo-details">
            ${additionalData.engagement ? `
              <div class="youtube-seo-section">
                <strong>🎯 Engagement Suggestions:</strong>
                ${additionalData.engagement.polls && additionalData.engagement.polls.length > 0 ? `
                  <div class="youtube-seo-subsection">
                    <strong>Polls:</strong>
                    <ul>
                      ${additionalData.engagement.polls.map(p => `<li>${p.question || p}</li>`).join('')}
                    </ul>
                  </div>
                ` : ''}
                ${additionalData.engagement.cards && additionalData.engagement.cards.length > 0 ? `
                  <div class="youtube-seo-subsection">
                    <strong>Cards:</strong>
                    <ul>
                      ${additionalData.engagement.cards.map(c => `<li>${c.title || c}</li>`).join('')}
                    </ul>
                  </div>
                ` : ''}
              </div>
            ` : ''}
          </div>
        </div>
      ` : ''}
    `;
    
    // Add tab handlers
    if (hasTabs) {
      const tabs = overlay.querySelectorAll('.youtube-seo-tab');
      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          tabs.forEach(t => t.classList.remove('active'));
          tab.classList.add('active');
          
          const tabName = tab.dataset.tab;
          document.querySelectorAll('.youtube-seo-content').forEach(content => {
            content.classList.add('hidden');
          });
          
          const contentId = `seo-content-${tabName}`;
          const content = overlay.querySelector(`#${contentId}`);
          if (content) {
            content.classList.remove('hidden');
            
            // Load similar videos if needed
            if (tabName === 'similar') {
              loadSimilarVideos(overlay, getVideoId());
            }
          }
        });
      });
    }
    
    // Add auto-fill button handler
    const autofillBtn = overlay.querySelector('#autofill-btn');
    if (autofillBtn) {
      autofillBtn.addEventListener('click', () => {
        if (isYouTubeStudio()) {
          autoFillYouTubeStudio(seoData);
        } else {
          // Copy to clipboard and open studio
          copySuggestionsToClipboard(seoData, additionalData);
          const videoId = getVideoId();
          if (videoId) {
            window.open(`https://studio.youtube.com/video/${videoId}/edit`, '_blank');
          }
        }
      });
    }
    
    // Add copy all button handler
    const copyAllBtn = overlay.querySelector('#copy-all-btn');
    if (copyAllBtn) {
      copyAllBtn.addEventListener('click', () => {
        copySuggestionsToClipboard(seoData, additionalData, true);
      });
    }
    
    return overlay;
  }
  
  // Copy suggestions to clipboard
  function copySuggestionsToClipboard(seoData, additionalData = {}, includeAll = false) {
    let text = 'YouTube SEO Suggestions\n';
    text += '='.repeat(30) + '\n\n';
    
    if (seoData.title_suggestions && seoData.title_suggestions.length > 0) {
      text += 'Title Suggestions:\n';
      seoData.title_suggestions.forEach((title, i) => {
        text += `${i + 1}. ${title}\n`;
      });
      text += '\n';
    }
    
    if (seoData.description) {
      text += 'Description:\n';
      text += seoData.description + '\n\n';
    }
    
    if (seoData.tags && seoData.tags.length > 0) {
      text += 'Tags:\n';
      text += seoData.tags.join(', ') + '\n\n';
    }
    
    if (includeAll && seoData.recommendations) {
      text += 'Recommendations:\n';
      seoData.recommendations.forEach((rec, i) => {
        text += `${i + 1}. ${rec}\n`;
      });
      text += '\n';
    }
    
    navigator.clipboard.writeText(text).then(() => {
      showAutoFillNotification('✅ Suggestions copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy:', err);
    });
  }
  
  // Load similar videos
  function loadSimilarVideos(overlay, videoId) {
    const content = overlay.querySelector('#seo-content-similar');
    if (!content) return;
    
    content.innerHTML = '<div class="youtube-seo-loading">Loading similar videos...</div>';
    
    chrome.runtime.sendMessage({
      action: 'getSimilarVideos',
      videoId: videoId,
      niche: null,
      maxResults: 5
    }, (response) => {
      if (response && response.success && response.data) {
        const similarVideos = response.data.similar_videos || [];
        const learnings = response.data.learnings || [];
        
        if (similarVideos.length === 0) {
          content.innerHTML = '<div class="youtube-seo-empty">No similar videos found</div>';
          return;
        }
        
        let html = '<div class="youtube-seo-similar-videos">';
        
        if (learnings.length > 0) {
          html += '<div class="youtube-seo-learnings"><strong>📚 Learnings from Top Videos:</strong><ul>';
          learnings.forEach(learning => {
            html += `<li>${learning}</li>`;
          });
          html += '</ul></div>';
        }
        
        html += '<div class="youtube-seo-video-list">';
        similarVideos.forEach(video => {
          html += `
            <div class="youtube-seo-video-item">
              <img src="${video.thumbnail}" alt="${video.title}" class="youtube-seo-video-thumb">
              <div class="youtube-seo-video-info">
                <div class="youtube-seo-video-title">${video.title}</div>
                <div class="youtube-seo-video-channel">${video.channel_title}</div>
                <div class="youtube-seo-video-stats">
                  <span>SEO: ${video.seo_score}/100</span>
                  <span>Views: ${formatNumber(video.views)}</span>
                </div>
                <a href="https://www.youtube.com/watch?v=${video.video_id}" target="_blank" class="youtube-seo-video-link">
                  Watch →
                </a>
              </div>
            </div>
          `;
        });
        html += '</div></div>';
        
        content.innerHTML = html;
      } else {
        content.innerHTML = '<div class="youtube-seo-empty">Error loading similar videos</div>';
      }
    });
  }
  
  // Format number
  function formatNumber(num) {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  }
  
  // Inject SEO overlay into page
  function injectSEOOverlay(seoData) {
    // Remove existing overlay
    const existing = document.getElementById('youtube-seo-overlay');
    if (existing) {
      existing.remove();
    }
    
    // Create and inject new overlay
    const overlay = createSEOOverlay(seoData);
    
    // Find insertion point
    if (isYouTubeStudio()) {
      // Insert near form fields
      const formContainer = document.querySelector('ytd-upload-dialog, ytd-metadata-editor, form');
      if (formContainer) {
        formContainer.insertBefore(overlay, formContainer.firstChild);
      } else {
        document.body.appendChild(overlay);
      }
    } else {
      // For watch pages, insert near video info
      const target = document.querySelector('#above-the-fold, #primary, ytd-watch-metadata');
      if (target) {
        target.insertBefore(overlay, target.firstChild);
      } else {
        document.body.appendChild(overlay);
      }
    }
  }
  
  // Show keyword suggestions
  function showKeywordSuggestions(keywords) {
    // Find description area
    const description = document.querySelector('#description, ytd-expander #content');
    if (description && keywords && keywords.length > 0) {
      const keywordBox = document.createElement('div');
      keywordBox.className = 'youtube-seo-keywords';
      keywordBox.innerHTML = `
        <div class="youtube-seo-keywords-header">
          <strong>🔑 Suggested Keywords:</strong>
        </div>
        <div class="youtube-seo-keywords-list">
          ${keywords.slice(0, 10).map(kw => `<span class="youtube-seo-keyword-tag">${kw}</span>`).join('')}
        </div>
      `;
      
      // Insert after description
      description.parentNode.insertBefore(keywordBox, description.nextSibling);
    }
  }
  
  // Main function to analyze current video
  async function analyzeCurrentVideo() {
    const videoId = getVideoId();
    if (!videoId && !isYouTubeStudio()) {
      return; // Not on a video page or studio
    }
    
    const channelHandle = getChannelHandle();
    
    try {
      // Request SEO analysis from background script
      chrome.runtime.sendMessage({
        action: 'getSEOAnalysis',
        videoId: videoId,
        channelHandle: channelHandle,
        niche: null, // Can be extracted from page if needed
        isStudio: isYouTubeStudio()
      }, (response) => {
        if (response && response.success && response.data) {
          // Load additional data (thumbnail, caption, engagement)
          loadAdditionalData(videoId, response.data, channelHandle);
        }
      });
    } catch (error) {
      console.error('Error analyzing video:', error);
    }
  }
  
  // Load additional data (thumbnail, caption, engagement)
  function loadAdditionalData(videoId, seoData, channelHandle) {
    const additionalData = {};
    let loadedCount = 0;
    const totalRequests = 3; // thumbnail, caption, engagement
    
    function checkComplete() {
      loadedCount++;
      if (loadedCount >= totalRequests) {
        if (CONFIG.showSEOOverlay) {
          injectSEOOverlay(seoData, additionalData);
        }
        
        // Auto-fill if on YouTube Studio
        if (isYouTubeStudio() && CONFIG.autoFillEnabled) {
          autoFillYouTubeStudio(seoData);
        }
        
        if (CONFIG.showKeywordSuggestions && seoData.keywords) {
          showKeywordSuggestions(seoData.keywords);
        }
      }
    }
    
    // Load thumbnail analysis
    chrome.runtime.sendMessage({
      action: 'getThumbnailAnalysis',
      videoId: videoId
    }, (response) => {
      if (response && response.success && response.data) {
        additionalData.thumbnail_score = response.data.thumbnail_score;
        additionalData.thumbnail_recommendations = response.data.recommendations;
      }
      checkComplete();
    });
    
    // Load caption analysis
    chrome.runtime.sendMessage({
      action: 'getCaptionAnalysis',
      videoId: videoId,
      niche: null
    }, (response) => {
      if (response && response.success && response.data) {
        additionalData.caption_score = response.data.caption_score;
        additionalData.caption_recommendations = response.data.recommendations;
        additionalData.has_captions = response.data.has_captions;
      }
      checkComplete();
    });
    
    // Load engagement suggestions
    chrome.runtime.sendMessage({
      action: 'getEngagementSuggestions',
      videoId: videoId,
      niche: null
    }, (response) => {
      if (response && response.success && response.data) {
        additionalData.engagement = response.data;
      }
      checkComplete();
    });
  }
  
  // Run analysis when page loads
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(analyzeCurrentVideo, 2000); // Wait for YouTube to load
    });
  } else {
    setTimeout(analyzeCurrentVideo, 2000);
  }
  
  // Re-analyze when navigating to new video (YouTube SPA)
  let lastVideoId = getVideoId();
  let lastUrl = window.location.href;
  const observer = new MutationObserver(() => {
    const currentVideoId = getVideoId();
    const currentUrl = window.location.href;
    
    // Check if URL changed (new video or navigation)
    if (currentUrl !== lastUrl || (currentVideoId && currentVideoId !== lastVideoId)) {
      lastVideoId = currentVideoId;
      lastUrl = currentUrl;
      setTimeout(analyzeCurrentVideo, 2000);
    }
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
  // Listen for messages from popup or background
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'analyzeVideo') {
      analyzeCurrentVideo();
      sendResponse({ success: true });
    } else if (request.action === 'autoFill') {
      if (request.data) {
        autoFillYouTubeStudio(request.data);
        sendResponse({ success: true });
      }
    }
    return true; // Keep channel open for async response
  });
  
})();
