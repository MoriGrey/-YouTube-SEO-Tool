// YouTube SEO AGI Tool - Content Script
// Injects SEO data and optimization suggestions into YouTube pages
// Also provides auto-fill functionality for YouTube Studio

(function() {
  'use strict';
  
  // Configuration
  const CONFIG = {
    apiBaseUrl: 'https://youtoubeseo.streamlit.app', // Update with actual Streamlit Cloud URL
    showSEOOverlay: true,
    showKeywordSuggestions: true,
    autoFillEnabled: true, // Enable auto-fill feature
    autoFillDelay: 2000 // Delay before auto-filling (ms) - increased for YouTube Studio
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
    if (!CONFIG.autoFillEnabled) {
      console.log('Auto-fill is disabled');
      return;
    }
    
    console.log('🔍 Starting auto-fill with data:', data);
    
    // Wait for form to load (increased delay for YouTube Studio)
    setTimeout(() => {
      let filledCount = 0;
      const errors = [];
      
      // Title field - try multiple selectors (YouTube Studio 2024 selectors)
      const titleSelectors = [
        'input[aria-label*="Title" i]',
        'input[name*="title" i]',
        '#textbox[aria-label*="Title" i]',
        'ytd-text-input-renderer input',
        'input[placeholder*="title" i]',
        'ytd-text-input-renderer #text-input',
        'input[id*="title" i]',
        'ytd-metadata-editor input[type="text"]',
        'ytd-metadata-editor #text-input',
        'ytd-metadata-editor ytd-text-input-renderer input',
        'input[aria-label*="Başlık" i]', // Turkish
        'input[aria-label*="Titel" i]' // German
      ];
      
      let titleField = null;
      for (const selector of titleSelectors) {
        try {
          titleField = document.querySelector(selector);
          if (titleField) {
            // Check if visible (more reliable check)
            const rect = titleField.getBoundingClientRect();
            const isVisible = rect.width > 0 && rect.height > 0 && 
                            titleField.offsetParent !== null &&
                            window.getComputedStyle(titleField).display !== 'none';
            if (isVisible) {
              console.log('✅ Found title field with selector:', selector);
              break;
            }
          }
        } catch (e) {
          console.warn('Error checking selector:', selector, e);
        }
      }
      
      if (!titleField) {
        errors.push('Title field not found');
        console.error('❌ Title field not found. Available inputs:', 
          Array.from(document.querySelectorAll('input, textarea')).map(el => ({
            tag: el.tagName,
            id: el.id,
            name: el.name,
            ariaLabel: el.getAttribute('aria-label'),
            placeholder: el.getAttribute('placeholder')
          }))
        );
      } else if (data.title_suggestions && data.title_suggestions.length > 0) {
        const bestTitle = data.title_suggestions[0];
        console.log('📝 Filling title:', bestTitle);
        
        // Clear and set value
        titleField.focus();
        titleField.select();
        titleField.value = '';
        
        // Use input event to trigger YouTube's internal handlers
        titleField.value = bestTitle;
        
        // Trigger multiple events to ensure YouTube detects the change
        const events = ['input', 'change', 'keyup', 'keydown', 'blur'];
        events.forEach(eventType => {
          titleField.dispatchEvent(new Event(eventType, { bubbles: true, cancelable: true }));
        });
        
        // Also try setting it via setter (triggers property change)
        Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(titleField, bestTitle);
        titleField.dispatchEvent(new Event('input', { bubbles: true }));
        
        filledCount++;
        console.log('✅ Auto-filled title:', bestTitle);
      } else {
        errors.push('No title suggestions available');
        console.warn('⚠️ No title suggestions in data');
      }
      
      // Description field - try multiple selectors
      const descSelectors = [
        'textarea[aria-label*="Description" i]',
        'textarea[name*="description" i]',
        '#textbox[aria-label*="Description" i]',
        'ytd-textarea-renderer textarea',
        'textarea[placeholder*="description" i]',
        'ytd-textarea-renderer #textarea',
        'textarea[id*="description" i]',
        'ytd-metadata-editor textarea',
        'ytd-metadata-editor ytd-textarea-renderer textarea',
        'textarea[aria-label*="Açıklama" i]', // Turkish
        'textarea[aria-label*="Beschreibung" i]' // German
      ];
      
      let descriptionField = null;
      for (const selector of descSelectors) {
        try {
          descriptionField = document.querySelector(selector);
          if (descriptionField) {
            const rect = descriptionField.getBoundingClientRect();
            const isVisible = rect.width > 0 && rect.height > 0 && 
                            descriptionField.offsetParent !== null &&
                            window.getComputedStyle(descriptionField).display !== 'none';
            if (isVisible) {
              console.log('✅ Found description field with selector:', selector);
              break;
            }
          }
        } catch (e) {
          console.warn('Error checking selector:', selector, e);
        }
      }
      
      if (!descriptionField) {
        errors.push('Description field not found');
        console.error('❌ Description field not found');
      } else if (data.description) {
        const descText = data.description;
        console.log('📝 Filling description (length:', descText.length, ')');
        
        descriptionField.focus();
        descriptionField.select();
        descriptionField.value = '';
        
        // Set value
        descriptionField.value = descText;
        
        // Trigger events
        const events = ['input', 'change', 'keyup', 'keydown', 'blur'];
        events.forEach(eventType => {
          descriptionField.dispatchEvent(new Event(eventType, { bubbles: true, cancelable: true }));
        });
        
        // Also try setter
        Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set.call(descriptionField, descText);
        descriptionField.dispatchEvent(new Event('input', { bubbles: true }));
        
        filledCount++;
        console.log('✅ Auto-filled description');
      } else {
        errors.push('No description available');
        console.warn('⚠️ No description in data');
      }
      
      // Tags field - YouTube uses chip-based input
      const tagSelectors = [
        'input[aria-label*="Tag" i]',
        'input[name*="tag" i]',
        '#chips-input input',
        'yt-chip-cloud-renderer input',
        'input[placeholder*="tag" i]',
        'input[id*="tag" i]',
        'ytd-metadata-editor input[type="text"]',
        'yt-chip-cloud-renderer ytd-chip-input-renderer input',
        'input[aria-label*="Etiket" i]', // Turkish
        'input[aria-label*="Schlagwort" i]' // German
      ];
      
      let tagsField = null;
      for (const selector of tagSelectors) {
        try {
          tagsField = document.querySelector(selector);
          if (tagsField) {
            const rect = tagsField.getBoundingClientRect();
            const isVisible = rect.width > 0 && rect.height > 0 && 
                            tagsField.offsetParent !== null &&
                            window.getComputedStyle(tagsField).display !== 'none';
            if (isVisible) {
              console.log('✅ Found tags field with selector:', selector);
              break;
            }
          }
        } catch (e) {
          console.warn('Error checking selector:', selector, e);
        }
      }
      
      if (!tagsField) {
        errors.push('Tags field not found');
        console.error('❌ Tags field not found');
      } else if (data.tags && data.tags.length > 0) {
        // Add tags one by one (YouTube chip system)
        const tagsToAdd = data.tags.slice(0, 15);
        console.log('📝 Adding tags:', tagsToAdd);
        
        tagsToAdd.forEach((tag, index) => {
          setTimeout(() => {
            tagsField.focus();
            tagsField.value = tag;
            tagsField.dispatchEvent(new Event('input', { bubbles: true }));
            
            // Simulate Enter key press
            const enterEvent = new KeyboardEvent('keydown', { 
              key: 'Enter', 
              code: 'Enter', 
              keyCode: 13,
              which: 13,
              bubbles: true,
              cancelable: true
            });
            tagsField.dispatchEvent(enterEvent);
            tagsField.dispatchEvent(new KeyboardEvent('keyup', { 
              key: 'Enter', 
              code: 'Enter',
              bubbles: true 
            }));
            
            console.log('✅ Added tag:', tag);
          }, index * 300); // Increased delay between tags
        });
        
        filledCount++;
        console.log('✅ Auto-filled tags');
      } else {
        errors.push('No tags available');
        console.warn('⚠️ No tags in data');
      }
      
      // Show notification with details
      if (filledCount > 0) {
        showAutoFillNotification(`✅ Auto-filled ${filledCount} field(s) from SEO analysis`);
      } else {
        const errorMsg = errors.length > 0 ? errors.join(', ') : 'Unknown error';
        showAutoFillNotification(`⚠️ Could not find form fields: ${errorMsg}. Please ensure you are on the video edit page.`);
        console.error('❌ Auto-fill failed. Errors:', errors);
        console.log('📊 Available form elements:', {
          inputs: Array.from(document.querySelectorAll('input')).length,
          textareas: Array.from(document.querySelectorAll('textarea')).length,
          allInputs: Array.from(document.querySelectorAll('input, textarea')).map(el => ({
            tag: el.tagName,
            id: el.id,
            name: el.name,
            ariaLabel: el.getAttribute('aria-label'),
            placeholder: el.getAttribute('placeholder'),
            visible: el.offsetParent !== null
          }))
        });
      }
    }, Math.max(CONFIG.autoFillDelay, 2000)); // Minimum 2 seconds delay for YouTube Studio
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
    
    if (!chrome.runtime || !chrome.runtime.sendMessage) {
      content.innerHTML = '<div class="youtube-seo-empty">Extension runtime not available</div>';
      return;
    }
    
    chrome.runtime.sendMessage({
      action: 'getSimilarVideos',
      videoId: videoId,
      niche: null,
      maxResults: 5
    }, (response) => {
      if (chrome.runtime.lastError) {
        console.error('Runtime error:', chrome.runtime.lastError.message);
        content.innerHTML = '<div class="youtube-seo-empty">Error: ' + chrome.runtime.lastError.message + '</div>';
        return;
      }
      
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
        const errorMsg = response?.error || 'Unknown error';
        content.innerHTML = '<div class="youtube-seo-empty">Error loading similar videos: ' + errorMsg + '</div>';
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
  function injectSEOOverlay(seoData, additionalData = {}) {
    // Remove existing overlay
    const existing = document.getElementById('youtube-seo-overlay');
    if (existing) {
      existing.remove();
    }
    
    // Create and inject new overlay
    const overlay = createSEOOverlay(seoData, additionalData);
    
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
      // Try direct fetch from content script (avoids CORS issues)
      // Content script runs in page context, so it can make cross-origin requests
      const params = new URLSearchParams({
        '_api': 'true',
        'action': 'seo_analyze',
        'video_id': videoId
      });
      
      if (channelHandle) params.append('channel_handle', channelHandle);
      
      const url = `${CONFIG.apiBaseUrl}?${params.toString()}`;
      console.log('Content script: Fetching SEO analysis from:', url);
      
      try {
        const response = await fetch(url, {
          method: 'GET',
          mode: 'cors',
          credentials: 'omit',
          headers: {
            'Accept': 'application/json, text/html, */*'
          }
        });
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        
        const text = await response.text();
        console.log('Content script: Response received, length:', text.length);
        
        // Parse response (same as background script)
        let result;
        try {
          result = JSON.parse(text);
        } catch (e) {
          const jsonMatch = text.match(/<pre[^>]*id=["']json-response["'][^>]*>([\s\S]*?)<\/pre>/);
          if (jsonMatch) {
            result = JSON.parse(jsonMatch[1]);
          } else {
            const scriptMatch = text.match(/window\.apiResponse\s*=\s*({[\s\S]*?});/);
            if (scriptMatch) {
              result = JSON.parse(scriptMatch[1]);
            } else {
              throw new Error('Could not parse JSON from response');
            }
          }
        }
        
        if (result && result.success && result.data) {
          console.log('Content script: SEO analysis received');
          // Load additional data (thumbnail, caption, engagement)
          loadAdditionalData(videoId, result.data, channelHandle);
        } else {
          console.error('Content script: API error:', result?.error || 'Unknown error');
        }
      } catch (fetchError) {
        console.error('Content script: Direct fetch failed, trying background script:', fetchError);
        
        // Fallback to background script if direct fetch fails
        if (!chrome.runtime || !chrome.runtime.sendMessage) {
          console.error('Chrome runtime not available');
          return;
        }
        
        // Request SEO analysis from background script
        chrome.runtime.sendMessage({
          action: 'getSEOAnalysis',
          videoId: videoId,
          channelHandle: channelHandle,
          niche: null,
          isStudio: isYouTubeStudio()
        }, (response) => {
          if (chrome.runtime.lastError) {
            console.error('Runtime error:', chrome.runtime.lastError.message);
            return;
          }
          
          if (response && response.success && response.data) {
            loadAdditionalData(videoId, response.data, channelHandle);
          } else if (response && response.error) {
            console.error('API error:', response.error);
          }
        });
      }
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
    
    // Helper function to safely send messages
    function safeSendMessage(message, callback) {
      if (!chrome.runtime || !chrome.runtime.sendMessage) {
        console.error('Chrome runtime not available');
        callback({ success: false, error: 'Runtime not available' });
        return;
      }
      
      chrome.runtime.sendMessage(message, (response) => {
        if (chrome.runtime.lastError) {
          console.error('Runtime error:', chrome.runtime.lastError.message);
          callback({ success: false, error: chrome.runtime.lastError.message });
          return;
        }
        callback(response || { success: false, error: 'No response' });
      });
    }
    
    // Load thumbnail analysis
    safeSendMessage({
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
    safeSendMessage({
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
    safeSendMessage({
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
    } else if (request.action === 'fetchSEOAnalysis') {
      // Fetch SEO analysis directly from content script (avoids CORS)
      (async () => {
        try {
          const params = new URLSearchParams({
            '_api': 'true',
            'action': 'seo_analyze',
            'video_id': request.videoId
          });
          
          if (request.channelHandle) params.append('channel_handle', request.channelHandle);
          if (request.niche) params.append('niche', request.niche);
          
          const url = `${CONFIG.apiBaseUrl}?${params.toString()}`;
          console.log('Content script: Fetching SEO analysis for popup from:', url);
          
          const response = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            credentials: 'omit',
            headers: {
              'Accept': 'application/json, text/html, */*'
            }
          });
          
          if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
          }
          
          const text = await response.text();
          let result;
          
          try {
            result = JSON.parse(text);
          } catch (e) {
            const jsonMatch = text.match(/<pre[^>]*id=["']json-response["'][^>]*>([\s\S]*?)<\/pre>/);
            if (jsonMatch) {
              result = JSON.parse(jsonMatch[1]);
            } else {
              const scriptMatch = text.match(/window\.apiResponse\s*=\s*({[\s\S]*?});/);
              if (scriptMatch) {
                result = JSON.parse(scriptMatch[1]);
              } else {
                throw new Error('Could not parse JSON from response');
              }
            }
          }
          
          if (result && result.success && result.data) {
            sendResponse({ success: true, data: result.data });
          } else {
            sendResponse({ success: false, error: result?.error || 'Unknown error' });
          }
        } catch (error) {
          console.error('Content script fetch error:', error);
          sendResponse({ success: false, error: error.message });
        }
      })();
      return true; // Keep channel open for async response
    } else if (request.action === 'getChannelHandle') {
      const channelHandle = getChannelHandle();
      sendResponse({ channelHandle: channelHandle });
    } else if (request.action === 'showSEOOverlay') {
      if (request.data) {
        injectSEOOverlay(request.data, request.additionalData || {});
        sendResponse({ success: true });
      }
    } else if (request.action === 'autoFill') {
      if (request.data) {
        autoFillYouTubeStudio(request.data);
        sendResponse({ success: true });
      }
    }
    return true; // Keep channel open for async response
  });
  
})();
