"""
YouTube Data API v3 Client
Handles all YouTube API interactions with caching and rate limiting.
"""

import os
from typing import Optional, Dict, Any, List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from diskcache import Cache
import time
import logging

# Initialize logger (lazy import to avoid circular dependency)
_logger = None

def _get_logger():
    """Get logger instance (lazy import)."""
    global _logger
    if _logger is None:
        try:
            from src.utils.logger import get_logger
            _logger = get_logger("youtube_client")
        except Exception:
            # Fallback to standard logging if custom logger not available
            _logger = logging.getLogger("youtube_client")
    return _logger

# Load environment variables
load_dotenv()


class YouTubeClient:
    """
    YouTube API Client with caching and quota management.
    
    AGI Paradigm: Omnipresent Data Mining
    - Unified access to YouTube's knowledge ocean
    - Smart caching reduces redundant API calls
    - Rate limiting respects API quotas
    """
    
    CACHE_DIR = ".cache/youtube"
    CACHE_EXPIRE = 3600  # 1 hour default cache
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize YouTube client with API key."""
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "YouTube API key not found! "
                "Set YOUTUBE_API_KEY environment variable or pass api_key parameter."
            )
        
        self._youtube = None
        self._cache = Cache(self.CACHE_DIR)
        self._quota_used = 0
        self._last_request_time = 0
        
    @property
    def youtube(self):
        """Lazy initialization of YouTube API service."""
        if self._youtube is None:
            self._youtube = build("youtube", "v3", developerKey=self.api_key)
        return self._youtube
    
    def _rate_limit(self, min_interval: float = 0.1):
        """Ensure minimum time between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self._last_request_time = time.time()
    
    def _cached_request(self, cache_key: str, request_func, expire: int = None, endpoint: str = "unknown", quota_cost: int = 1):
        """Execute request with caching, rate limiting and logging."""
        expire = expire or self.CACHE_EXPIRE
        logger = _get_logger()
        
        # Check cache first
        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.api_usage("youtube", endpoint, "cached", cache_hit=True, quota_cost=0)
            return cached
        
        # Check application-level rate limit (DDoS protection)
        try:
            from src.utils.rate_limiter import check_rate_limit
            allowed, error_msg = check_rate_limit("youtube_api")
            if not allowed:
                logger.warning(f"Rate limit exceeded for YouTube API: {error_msg}")
                raise YouTubeAPIError(f"Rate limit exceeded: {error_msg}")
        except ImportError:
            # Rate limiter not available, skip check
            pass
        
        # Rate limit and execute
        self._rate_limit()
        start_time = time.time()
        try:
            result = request_func()
            response_time = time.time() - start_time
            
            # Update quota usage
            self._quota_used += quota_cost
            
            self._cache.set(cache_key, result, expire=expire)
            
            # Log successful API usage
            logger.api_usage(
                "youtube",
                endpoint,
                "success",
                response_time_ms=round(response_time * 1000, 2),
                cache_hit=False,
                quota_cost=quota_cost,
                quota_used=self._quota_used
            )
            
            return result
        except HttpError as e:
            response_time = time.time() - start_time
            error_code = e.resp.status if hasattr(e, 'resp') else None
            
            # Log API error
            logger.api_usage(
                "youtube",
                endpoint,
                "error",
                error_code=error_code,
                error_message=str(e)[:100],  # Truncate long error messages
                response_time_ms=round(response_time * 1000, 2)
            )
            logger.error(f"YouTube API error: {e}", endpoint=endpoint, error_code=error_code)
            
            raise YouTubeAPIError(f"YouTube API Error: {e}")
    
    def get_channel_by_handle(self, handle: str) -> Dict[str, Any]:
        """
        Get channel info by handle (e.g., @anatolianturkishrock).
        
        Returns channel ID, title, description, statistics.
        Quota cost: 1 unit
        """
        # Remove @ if present and strip whitespace
        handle = handle.lstrip("@").strip()
        
        # Validate handle is not empty
        if not handle:
            raise ValueError("Channel handle cannot be empty. Please provide a valid channel handle.")
        
        cache_key = f"channel_handle:{handle}"
        
        def request():
            response = self.youtube.channels().list(
                part="snippet,statistics,contentDetails,brandingSettings",
                forHandle=handle
            ).execute()
            return response
        
        return self._cached_request(cache_key, request, endpoint="channels.list", quota_cost=1)
    
    def get_channel_by_id(self, channel_id: str) -> Dict[str, Any]:
        """
        Get channel info by channel ID.
        
        Quota cost: 1 unit
        """
        cache_key = f"channel_id:{channel_id}"
        
        def request():
            response = self.youtube.channels().list(
                part="snippet,statistics,contentDetails,brandingSettings",
                id=channel_id
            ).execute()
            return response
        
        return self._cached_request(cache_key, request, endpoint="channels.list", quota_cost=1)
    
    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get all videos from a channel.
        
        Quota cost: ~100 units per 50 videos
        """
        cache_key = f"channel_videos:{channel_id}:{max_results}"
        
        def request():
            # First, get uploads playlist ID
            channel_response = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            ).execute()
            
            if not channel_response.get("items"):
                return []
            
            uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            
            # Get videos from uploads playlist
            videos = []
            next_page_token = None
            
            while len(videos) < max_results:
                playlist_response = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=uploads_playlist_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token
                ).execute()
                
                videos.extend(playlist_response.get("items", []))
                next_page_token = playlist_response.get("nextPageToken")
                
                if not next_page_token:
                    break
            
            # Get detailed video statistics
            video_ids = [v["contentDetails"]["videoId"] for v in videos]
            video_details = self.get_videos_details(video_ids)
            
            return video_details
        
        return self._cached_request(cache_key, request, expire=1800)  # 30 min cache
    
    def get_videos_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed info for multiple videos.
        
        Quota cost: 1 unit per 50 videos
        """
        if not video_ids:
            return []
        
        all_videos = []
        
        # Process in batches of 50
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            cache_key = f"videos_details:{','.join(sorted(batch_ids))}"
            
            def request():
                response = self.youtube.videos().list(
                    part="snippet,statistics,contentDetails,topicDetails",
                    id=",".join(batch_ids)
                ).execute()
                return response.get("items", [])
            
            all_videos.extend(self._cached_request(cache_key, request))
        
        return all_videos
    
    def search_videos(
        self,
        query: str,
        max_results: int = 25,
        order: str = "relevance",
        region_code: str = "TR",
        video_category_id: str = "10"  # Music category
    ) -> List[Dict[str, Any]]:
        """
        Search YouTube videos.
        
        Quota cost: 100 units
        """
        cache_key = f"search:{query}:{max_results}:{order}:{region_code}:{video_category_id}"
        
        def request():
            response = self.youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=max_results,
                order=order,
                regionCode=region_code,
                videoCategoryId=video_category_id
            ).execute()
            return response.get("items", [])
        
        return self._cached_request(cache_key, request)
    
    def get_video_comments(self, video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Get comments for a video.
        
        Quota cost: 1 unit per 100 comments
        """
        cache_key = f"comments:{video_id}:{max_results}"
        
        def request():
            try:
                response = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(100, max_results),
                    order="relevance"
                ).execute()
                return response.get("items", [])
            except HttpError as e:
                if "commentsDisabled" in str(e):
                    return []
                raise
        
        return self._cached_request(cache_key, request)
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """
        Get YouTube search autocomplete suggestions.
        Uses unofficial endpoint (no quota cost).
        """
        import httpx
        
        cache_key = f"suggestions:{query}"
        
        cached = self._cache.get(cache_key)
        if cached:
            return cached
        
        try:
            url = f"https://suggestqueries-clients6.youtube.com/complete/search"
            params = {
                "client": "youtube",
                "q": query,
                "hl": "tr",
                "gl": "TR"
            }
            
            response = httpx.get(url, params=params, timeout=5.0)
            
            # Parse JSONP response
            text = response.text
            if text.startswith("window.google.ac.h("):
                import json
                json_str = text[19:-1]
                data = json.loads(json_str)
                suggestions = [item[0] for item in data[1]]
                self._cache.set(cache_key, suggestions, expire=3600)
                return suggestions
        except Exception:
            pass
        
        return []
    
    def clear_cache(self):
        """Clear all cached data."""
        self._cache.clear()
    
    def get_quota_estimate(self) -> Dict[str, int]:
        """
        Get estimated quota usage.
        YouTube API has 10,000 units/day limit.
        """
        return {
            "estimated_used": self._quota_used,
            "daily_limit": 10000,
            "remaining": 10000 - self._quota_used
        }


class YouTubeAPIError(Exception):
    """Custom exception for YouTube API errors."""
    pass


# Convenience function
def create_client(api_key: Optional[str] = None) -> YouTubeClient:
    """Create and return a YouTubeClient instance."""
    return YouTubeClient(api_key)

