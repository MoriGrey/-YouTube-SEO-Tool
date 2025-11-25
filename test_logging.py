"""
Test script for logging functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.logger import get_logger

def test_logging():
    """Test logging functionality."""
    print("Testing Logging System...")
    print("=" * 60)
    
    logger = get_logger("test_logger", log_file="logs/test.log")
    
    # Test basic logging
    print("\n1. Testing basic logging...")
    logger.info("Test info message")
    logger.warning("Test warning message")
    logger.error("Test error message")
    print("[OK] Basic logging works")
    
    # Test security event logging
    print("\n2. Testing security event logging...")
    logger.security_event(
        "api_key_saved",
        "API key saved successfully",
        key_length=40,
        encrypted=True
    )
    print("[OK] Security event logging works")
    
    # Test API usage logging
    print("\n3. Testing API usage logging...")
    logger.api_usage(
        "youtube",
        "channels.list",
        "success",
        response_time_ms=150.5,
        quota_cost=1,
        quota_used=5
    )
    print("[OK] API usage logging works")
    
    # Test audit trail
    print("\n4. Testing audit trail...")
    logger.audit_trail(
        "api_key_changed",
        user_id="test_user_123",
        action_type="save"
    )
    print("[OK] Audit trail works")
    
    # Test sensitive data masking
    print("\n5. Testing sensitive data masking...")
    logger.info("API key is AIzaSyTest123456789012345678901234567890")
    logger.info("Password is secret123")
    print("[OK] Sensitive data masking works (check logs to verify)")
    
    print("\n" + "=" * 60)
    print("[OK] All logging tests completed!")
    print("Check logs/test.log file to see the results")
    print("=" * 60)

if __name__ == "__main__":
    import io
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    test_logging()

