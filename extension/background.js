// YouTube SEO AGI Tool - Background Service Worker
// Handles API communication and data caching

// API base URL (update with your deployment URL)
// Streamlit Cloud doesn't support separate FastAPI, so we use query params
const API_BASE_URL = 'https://youtoubeseo.streamlit.app'; // Update with actual Streamlit Cloud URL

// Cache for API responses
const cache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

// Helper function to parse Streamlit API response
async function parseStreamlitResponse(response) {
  console.log('Parsing Streamlit response, status:', response.status, response.statusText);
  console.log('Response headers:', Object.fromEntries(response.headers.entries()));
  
  if (!response.ok) {
    const errorText = await response.text();
    console.error('API error response:', errorText.substring(0, 500));
    throw new Error(`API error: ${response.status} ${response.statusText}. Response: ${errorText.substring(0, 200)}`);
  }
  
  const text = await response.text();
  console.log('Response text length:', text.length);
  console.log('Response text preview:', text.substring(0, 500));
  
  let result;
  
  try {
    // Try to parse as JSON first (if Streamlit returns pure JSON)
    result = JSON.parse(text);
    console.log('Successfully parsed as JSON');
  } catch (e) {
    console.log('Not pure JSON, trying to extract from HTML...');
    // If not JSON, try to extract from HTML
    // Look for <pre id="json-response"> tag
    const jsonMatch = text.match(/<pre[^>]*id=["']json-response["'][^>]*>([\s\S]*?)<\/pre>/);
    if (jsonMatch) {
      console.log('Found JSON in <pre> tag');
      try {
        result = JSON.parse(jsonMatch[1]);
        console.log('Successfully parsed JSON from <pre> tag');
      } catch (parseError) {
        console.error('Failed to parse JSON from <pre> tag:', parseError);
        // Try to find JSON in script tag
        const scriptMatch = text.match(/window\.apiResponse\s*=\s*({[\s\S]*?});/);
        if (scriptMatch) {
          console.log('Found JSON in window.apiResponse');
          result = JSON.parse(scriptMatch[1]);
        } else {
          throw new Error('Could not parse JSON from response: ' + parseError.message + '. JSON content: ' + jsonMatch[1].substring(0, 200));
        }
      }
    } else {
      console.log('No <pre> tag found, trying window.apiResponse...');
      // Try to find JSON in script tag
      const scriptMatch = text.match(/window\.apiResponse\s*=\s*({[\s\S]*?});/);
      if (scriptMatch) {
        console.log('Found JSON in window.apiResponse');
        result = JSON.parse(scriptMatch[1]);
      } else {
        // Try to find any JSON object in the text
        const anyJsonMatch = text.match(/\{[\s\S]*"success"[\s\S]*\}/);
        if (anyJsonMatch) {
          console.log('Found JSON object in text');
          result = JSON.parse(anyJsonMatch[0]);
        } else {
          console.error('Could not find JSON in response. Full text:', text);
          throw new Error('Could not parse JSON from response. Response type: ' + response.headers.get('content-type') + '. Text preview: ' + text.substring(0, 500));
        }
      }
    }
  }
  
  console.log('Parsed result:', result);
  return result;
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getVideoData') {
    getVideoData(request.videoId)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep channel open for async response
  }
  
  if (request.action === 'getSEOAnalysis') {
    getSEOAnalysis(request.videoId, request.channelHandle, request.niche)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep channel open for async response
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
      credentials: 'omit',
      headers: {
        'Accept': 'application/json, text/html'
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
    
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || result.status || 'Unknown error');
    }
  } catch (error) {
    console.error('Error fetching video data:', error);
    throw error;
  }
}

// Test API connection
async function testAPIConnection() {
  try {
    const testUrl = `${API_BASE_URL}?_api=true&action=health`;
    console.log('Testing API connection to:', testUrl);
    
    const response = await fetch(testUrl, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Accept': 'application/json, text/html, */*'
      }
    });
    
    console.log('Health check response status:', response.status);
    const text = await response.text();
    console.log('Health check response text:', text.substring(0, 200));
    
    return response.ok;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
}

// Get SEO analysis
async function getSEOAnalysis(videoId, channelHandle, niche) {
  const cacheKey = `seo_${videoId}_${channelHandle}_${niche || ''}`;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  
  // Test connection first (only once per session)
  if (!cache.has('api_connection_tested')) {
    const isConnected = await testAPIConnection();
    cache.set('api_connection_tested', { value: true, timestamp: Date.now() });
    if (!isConnected) {
      throw new Error(`Cannot connect to ${API_BASE_URL}. Please verify:\n1. The Streamlit app is deployed at ${API_BASE_URL}\n2. The app is accessible in your browser\n3. Your internet connection is working`);
    }
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
    console.log('Fetching SEO analysis from:', url);
    
    let response;
    try {
      response = await fetch(url, {
        method: 'GET',
        mode: 'cors',
        credentials: 'omit',
        headers: {
          'Accept': 'application/json, text/html, */*'
        }
      });
      console.log('Fetch response received, status:', response.status);
    } catch (fetchError) {
      console.error('Fetch error details:', {
        name: fetchError.name,
        message: fetchError.message,
        stack: fetchError.stack
      });
      
      // Check if it's a network error
      if (fetchError.name === 'TypeError' && fetchError.message.includes('Failed to fetch')) {
        throw new Error(`Network error: Could not connect to ${API_BASE_URL}. Please verify:\n1. The Streamlit app is deployed and running\n2. The URL is correct: ${API_BASE_URL}\n3. Your internet connection is working\n4. The app is accessible in your browser`);
      }
      throw fetchError;
    }
    
    const result = await parseStreamlitResponse(response);
    
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || result.status || 'Unknown error');
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
        'Accept': 'application/json, text/html'
      }
    });
    
    const result = await parseStreamlitResponse(response);
    
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || result.status || 'Unknown error');
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
      headers: { 'Accept': 'application/json, text/html' }
    });
    
    const result = await parseStreamlitResponse(response);
    
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || result.status || 'Unknown error');
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
      headers: { 'Accept': 'application/json, text/html' }
    });
    
    const result = await parseStreamlitResponse(response);
    
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || result.status || 'Unknown error');
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
      headers: { 'Accept': 'application/json, text/html' }
    });
    
    const result = await parseStreamlitResponse(response);
    
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || result.status || 'Unknown error');
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
      headers: { 'Accept': 'application/json, text/html' }
    });
    
    const result = await parseStreamlitResponse(response);
    
    if (result.success && result.data) {
      cache.set(cacheKey, { data: result.data, timestamp: Date.now() });
      return result.data;
    } else {
      throw new Error(result.error || result.status || 'Unknown error');
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

// Keep service worker alive
chrome.runtime.onConnect.addListener((port) => {
  console.log('Port connected:', port.name);
  port.onDisconnect.addListener(() => {
    console.log('Port disconnected:', port.name);
  });
});

// Periodic wake-up to keep service worker alive
setInterval(() => {
  // This keeps the service worker active
  console.log('Service worker keep-alive ping');
}, 20000); // Every 20 seconds

