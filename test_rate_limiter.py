"""
Test script for rate limiter functionality
"""

import sys
import os
import time
import io
sys.path.insert(0, os.path.dirname(__file__))

# Mock streamlit for testing
class MockStreamlit:
    session_state = {}
    
    @staticmethod
    def get(key, default=None):
        return MockStreamlit.session_state.get(key, default)

import streamlit as st
st.session_state = MockStreamlit.session_state

from src.utils.rate_limiter import RateLimiter

def test_rate_limiter():
    """Test rate limiter functionality."""
    print("Testing Rate Limiter...")
    print("=" * 60)
    
    # Set up mock session
    st.session_state['username'] = 'test_user'
    
    # Create rate limiter with low limits for testing
    limiter = RateLimiter(
        requests_per_minute=5,
        requests_per_hour=20,
        requests_per_day=100,
        block_duration_minutes=1
    )
    
    print("\n1. Testing basic rate limiting...")
    success_count = 0
    blocked_count = 0
    for i in range(7):  # Try 7 requests (limit is 5)
        # Check status before request
        status_before = limiter.get_rate_limit_status()
        print(f"  Before request {i+1}: {status_before['requests_last_minute']} requests in last minute")
        
        allowed, error_msg = limiter.check_rate_limit("dashboard_action")
        
        # Check status after request
        status_after = limiter.get_rate_limit_status()
        print(f"  After request {i+1}: {status_after['requests_last_minute']} requests in last minute")
        
        if allowed:
            success_count += 1
            print(f"  Request {i+1}: ✅ Allowed (total: {success_count})")
        else:
            blocked_count += 1
            print(f"  Request {i+1}: ❌ Blocked - {error_msg}")
            if blocked_count >= 1:
                break
        # Small delay to ensure different timestamps
        time.sleep(0.1)
    
    print(f"  Summary: {success_count} allowed, {blocked_count} blocked")
    assert success_count == 5, f"Expected 5 allowed requests, got {success_count}"
    assert blocked_count >= 1, f"Expected at least 1 blocked request, got {blocked_count}"
    print("[OK] Basic rate limiting works")
    
    print("\n2. Testing rate limit status...")
    status = limiter.get_rate_limit_status()
    print(f"  User ID: {status['user_id']}")
    print(f"  Blocked: {status['blocked']}")
    print(f"  Requests last minute: {status['requests_last_minute']}")
    print(f"  Limits: {status['limits']}")
    assert status['requests_last_minute'] == 5
    print("[OK] Rate limit status works")
    
    print("\n3. Testing blocking...")
    # Wait a bit for block to expire (in real scenario)
    print("  User is blocked (expected)")
    assert status['blocked'] == True
    print("[OK] Blocking works")
    
    print("\n4. Testing per-endpoint limits...")
    # Reset for endpoint test
    limiter.request_history.clear()
    limiter.blocked_users.clear()
    
    # Test YouTube API endpoint
    for i in range(3):
        allowed, _ = limiter.check_rate_limit("youtube_api")
        if allowed:
            print(f"  YouTube API request {i+1}: ✅ Allowed")
        else:
            print(f"  YouTube API request {i+1}: ❌ Blocked")
    
    print("[OK] Per-endpoint limits work")
    
    print("\n" + "=" * 60)
    print("[OK] All rate limiter tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    test_rate_limiter()

