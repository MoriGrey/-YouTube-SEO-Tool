"""
Rate Limiting Module
Protects against DDoS attacks and API abuse
"""

import time
from typing import Dict, Optional, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
import streamlit as st

from src.utils.logger import get_logger

logger = get_logger("rate_limiter")


class RateLimiter:
    """
    Rate limiter for API requests and user actions.
    
    Features:
    - Per-user rate limiting
    - Per-endpoint rate limiting
    - Sliding window algorithm
    - DDoS protection
    - Automatic blocking
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        requests_per_day: int = 10000,
        block_duration_minutes: int = 15
    ):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Max requests per minute per user
            requests_per_hour: Max requests per hour per user
            requests_per_day: Max requests per day per user
            block_duration_minutes: Duration to block after exceeding limits
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.requests_per_day = requests_per_day
        self.block_duration_minutes = block_duration_minutes
        
        # Request tracking: {user_id: {timestamp: count}}
        self.request_history: Dict[str, Dict[float, int]] = defaultdict(dict)
        
        # Blocked users: {user_id: block_until_timestamp}
        self.blocked_users: Dict[str, float] = {}
        
        # Per-endpoint limits
        self.endpoint_limits: Dict[str, Dict[str, int]] = {
            'youtube_api': {
                'per_minute': 60,
                'per_hour': 1000
            },
            'dashboard_action': {
                'per_minute': 30,
                'per_hour': 500
            }
        }
    
    def _get_user_id(self) -> str:
        """Get current user identifier."""
        # Try to get from session state
        username = st.session_state.get('username')
        if username:
            return f"user_{username}"
        
        # Fallback to session ID
        session_id = st.session_state.get('session_id')
        if not session_id:
            # Generate session ID
            import hashlib
            session_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
            st.session_state['session_id'] = session_id
        
        return f"session_{session_id}"
    
    def _clean_old_requests(self, user_id: str, window_seconds: int = 3600):
        """Clean old request records outside the time window."""
        current_time = time.time()
        cutoff_time = current_time - window_seconds
        
        if user_id in self.request_history:
            # Remove old entries
            self.request_history[user_id] = {
                timestamp: count
                for timestamp, count in self.request_history[user_id].items()
                if timestamp > cutoff_time
            }
    
    def _check_blocked(self, user_id: str) -> bool:
        """Check if user is currently blocked."""
        if user_id in self.blocked_users:
            block_until = self.blocked_users[user_id]
            if time.time() < block_until:
                return True
            else:
                # Block expired, remove
                del self.blocked_users[user_id]
                logger.info(f"Rate limit block expired for user: {user_id}")
        return False
    
    def _block_user(self, user_id: str, reason: str):
        """Block user for exceeding rate limits."""
        block_until = time.time() + (self.block_duration_minutes * 60)
        self.blocked_users[user_id] = block_until
        
        logger.security_event(
            "rate_limit_exceeded",
            f"User blocked due to rate limit: {reason}",
            user_id=user_id,
            block_until=datetime.fromtimestamp(block_until).isoformat()
        )
        logger.audit_trail("user_blocked", user_id=user_id, reason=reason)
    
    def _count_requests(self, user_id: str, window_seconds: int) -> int:
        """Count requests in time window (including current second)."""
        current_time = time.time()
        cutoff_time = current_time - window_seconds
        
        if user_id not in self.request_history:
            return 0
        
        # Count all requests in the time window
        # Note: We count requests that are >= cutoff_time (inclusive of current second)
        count = sum(
            count
            for timestamp, count in self.request_history[user_id].items()
            if timestamp >= cutoff_time
        )
        return count
    
    def _record_request(self, user_id: str):
        """Record a new request."""
        current_time = time.time()
        
        if user_id not in self.request_history:
            self.request_history[user_id] = {}
        
        # Round to second for grouping
        time_key = int(current_time)
        self.request_history[user_id][time_key] = self.request_history[user_id].get(time_key, 0) + 1
    
    def check_rate_limit(
        self,
        endpoint: Optional[str] = None,
        custom_limits: Optional[Dict[str, int]] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if request is within rate limits.
        
        Args:
            endpoint: Optional endpoint name for per-endpoint limits
            custom_limits: Optional custom limits dict
            
        Returns:
            (allowed, error_message)
        """
        user_id = self._get_user_id()
        current_time = time.time()
        
        # Check if user is blocked
        if self._check_blocked(user_id):
            remaining = self.blocked_users[user_id] - current_time
            minutes = int(remaining / 60)
            return False, f"Rate limit exceeded. Blocked for {minutes} more minutes."
        
        # Clean old requests
        self._clean_old_requests(user_id, window_seconds=86400)  # 24 hours
        
        # Use custom limits or endpoint limits or default limits
        limits = custom_limits
        if not limits and endpoint and endpoint in self.endpoint_limits:
            # Merge endpoint limits with defaults (endpoint can override specific limits)
            endpoint_limits = self.endpoint_limits[endpoint]
            limits = {
                'per_minute': endpoint_limits.get('per_minute', self.requests_per_minute),
                'per_hour': endpoint_limits.get('per_hour', self.requests_per_hour),
                'per_day': endpoint_limits.get('per_day', self.requests_per_day)
            }
        
        if not limits:
            limits = {
                'per_minute': self.requests_per_minute,
                'per_hour': self.requests_per_hour,
                'per_day': self.requests_per_day
            }
        
        # Check limits BEFORE recording this request
        # Check per-minute limit
        if 'per_minute' in limits:
            minute_count = self._count_requests(user_id, 60)
            limit_value = limits['per_minute']
            # If we're at or above the limit, block (we haven't recorded this request yet)
            # Debug: print(f"DEBUG: minute_count={minute_count}, limit={limit_value}, user_id={user_id}")
            if minute_count >= limit_value:
                self._block_user(user_id, f"Exceeded {limit_value} requests per minute")
                return False, f"Rate limit exceeded: {limit_value} requests per minute"
        
        # Check per-hour limit
        if 'per_hour' in limits:
            hour_count = self._count_requests(user_id, 3600)
            if hour_count >= limits['per_hour']:
                self._block_user(user_id, f"Exceeded {limits['per_hour']} requests per hour")
                return False, f"Rate limit exceeded: {limits['per_hour']} requests per hour"
        
        # Check per-day limit
        if 'per_day' in limits:
            day_count = self._count_requests(user_id, 86400)
            if day_count >= limits['per_day']:
                self._block_user(user_id, f"Exceeded {limits['per_day']} requests per day")
                return False, f"Rate limit exceeded: {limits['per_day']} requests per day"
        
        # All checks passed, record this request
        self._record_request(user_id)
        
        return True, None
    
    def get_rate_limit_status(self) -> Dict[str, any]:
        """
        Get current rate limit status for user.
        
        Returns:
            Dictionary with rate limit information
        """
        user_id = self._get_user_id()
        
        # Clean old requests
        self._clean_old_requests(user_id, window_seconds=86400)
        
        status = {
            'user_id': user_id,
            'blocked': self._check_blocked(user_id),
            'requests_last_minute': self._count_requests(user_id, 60),
            'requests_last_hour': self._count_requests(user_id, 3600),
            'requests_last_day': self._count_requests(user_id, 86400),
            'limits': {
                'per_minute': self.requests_per_minute,
                'per_hour': self.requests_per_hour,
                'per_day': self.requests_per_day
            }
        }
        
        if status['blocked']:
            block_until = self.blocked_users[user_id]
            status['blocked_until'] = datetime.fromtimestamp(block_until).isoformat()
            status['blocked_remaining_minutes'] = int((block_until - time.time()) / 60)
        
        return status


# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None

def get_rate_limiter() -> RateLimiter:
    """
    Get or create global rate limiter instance.
    
    Returns:
        RateLimiter instance
    """
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter

def check_rate_limit(endpoint: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Check rate limit - convenience function.
    
    Args:
        endpoint: Optional endpoint name
        
    Returns:
        (allowed, error_message)
    """
    limiter = get_rate_limiter()
    return limiter.check_rate_limit(endpoint)

def require_rate_limit(endpoint: Optional[str] = None):
    """
    Require rate limit check - raises error if exceeded.
    
    Args:
        endpoint: Optional endpoint name
        
    Raises:
        ValueError: If rate limit exceeded
    """
    allowed, error_msg = check_rate_limit(endpoint)
    if not allowed:
        raise ValueError(error_msg or "Rate limit exceeded")

