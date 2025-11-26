// YouTube SEO AGI Tool - Background Service Worker
// Handles API communication and data caching

// API base URL (update with your deployment URL)
// Streamlit Cloud doesn't support separate FastAPI, so we use query params
const API_BASE_URL = 'https://your-app-url.streamlit.app'; // TODO: Update with actual URL

// Cache for API responses
const cache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getVideoData') {
    getVideoData(request.videoId)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep channel open for async response
  }
  
  if (request.action === 'getSEOAnalysis') {
    getSEOAnalysis(request.videoId, request.channelHandle)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
  
  if (request.action === 'getKeywordSuggestions') {
    getKeywordSuggestions(request.topic, request.niche)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
  
  if (request.action === 'getSimilarVideos') {
    getSimilarVideos(request.videoId, request.niche, request.maxResults)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
  
  if (request.action === 'getThumbnailAnalysis') {
    getThumbnailAnalysis(request.videoId)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
  
  if (request.action === 'getCaptionAnalysis') {
    getCaptionAnalysis(request.videoId, request.niche)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
  
  if (request.action === 'getEngagementSuggestions') {
    getEngagementSuggestions(request.videoId, request.niche)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
});

// Get video data from API
async function getVideoData(videoId) {
  const cacheKey = `video_${videoId}`;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  
  try {
    // Use query params for Streamlit API
    const url = `${API_BASE_URL}?_api=true&action=video_data&video_id=${videoId}`;
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit'
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const result = await response.json();
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || 'Unknown error');
    }
  } catch (error) {
    console.error('Error fetching video data:', error);
    throw error;
  }
}

// Get SEO analysis
async function getSEOAnalysis(videoId, channelHandle, niche) {
  const cacheKey = `seo_${videoId}_${channelHandle}`;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  
  try {
    // Use query params for Streamlit API (GET request to avoid CORS preflight)
    const params = new URLSearchParams({
      '_api': 'true',
      'action': 'seo_analyze',
      'video_id': videoId
    });
    
    if (channelHandle) params.append('channel_handle', channelHandle);
    if (niche) params.append('niche', niche);
    
    const url = `${API_BASE_URL}?${params.toString()}`;
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const result = await response.json();
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || 'Unknown error');
    }
  } catch (error) {
    console.error('Error fetching SEO analysis:', error);
    throw error;
  }
}

// Get keyword suggestions
async function getKeywordSuggestions(topic, niche) {
  const cacheKey = `keywords_${topic}_${niche}`;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  
  try {
    // Use query params for Streamlit API (GET request to avoid CORS preflight)
    const params = new URLSearchParams({
      '_api': 'true',
      'action': 'keywords_suggest',
      'topic': topic
    });
    
    if (niche) params.append('niche', niche);
    
    const url = `${API_BASE_URL}?${params.toString()}`;
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const result = await response.json();
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || 'Unknown error');
    }
  } catch (error) {
    console.error('Error fetching keyword suggestions:', error);
    throw error;
  }
}

// Clear cache periodically
setInterval(() => {
  const now = Date.now();
  for (const [key, value] of cache.entries()) {
    if (now - value.timestamp > CACHE_DURATION) {
      cache.delete(key);
    }
  }
}, 60000); // Check every minute

// Get similar videos analysis
async function getSimilarVideos(videoId, niche, maxResults = 5) {
  const cacheKey = `similar_${videoId}_${niche}_${maxResults}`;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  
  try {
    const params = new URLSearchParams({
      '_api': 'true',
      'action': 'similar_videos_analyze',
      'video_id': videoId,
      'max_results': maxResults.toString()
    });
    
    if (niche) params.append('niche', niche);
    
    const url = `${API_BASE_URL}?${params.toString()}`;
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: { 'Accept': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const result = await response.json();
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || 'Unknown error');
    }
  } catch (error) {
    console.error('Error fetching similar videos:', error);
    throw error;
  }
}

// Get thumbnail analysis
async function getThumbnailAnalysis(videoId) {
  const cacheKey = `thumbnail_${videoId}`;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  
  try {
    const params = new URLSearchParams({
      '_api': 'true',
      'action': 'thumbnail_analyze',
      'video_id': videoId
    });
    
    const url = `${API_BASE_URL}?${params.toString()}`;
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: { 'Accept': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const result = await response.json();
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || 'Unknown error');
    }
  } catch (error) {
    console.error('Error fetching thumbnail analysis:', error);
    throw error;
  }
}

// Get caption analysis
async function getCaptionAnalysis(videoId, niche) {
  const cacheKey = `caption_${videoId}_${niche}`;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  
  try {
    const params = new URLSearchParams({
      '_api': 'true',
      'action': 'caption_analyze',
      'video_id': videoId
    });
    
    if (niche) params.append('niche', niche);
    
    const url = `${API_BASE_URL}?${params.toString()}`;
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: { 'Accept': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const result = await response.json();
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || 'Unknown error');
    }
  } catch (error) {
    console.error('Error fetching caption analysis:', error);
    throw error;
  }
}

// Get engagement suggestions
async function getEngagementSuggestions(videoId, niche) {
  const cacheKey = `engagement_${videoId}_${niche}`;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  
  try {
    const params = new URLSearchParams({
      '_api': 'true',
      'action': 'engagement_suggest',
      'video_id': videoId
    });
    
    if (niche) params.append('niche', niche);
    
    const url = `${API_BASE_URL}?${params.toString()}`;
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: { 'Accept': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const result = await response.json();
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || 'Unknown error');
    }
  } catch (error) {
    console.error('Error fetching engagement suggestions:', error);
    throw error;
  }
}

// Install/update handler
chrome.runtime.onInstalled.addListener(() => {
  console.log('YouTube SEO AGI Tool Extension installed');
});

