"""
Test script for input validator functionality
"""

import sys
import os
import io
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.input_validator import InputValidator

def test_input_validator():
    """Test input validator functionality."""
    print("Testing Input Validator...")
    print("=" * 60)
    
    validator = InputValidator()
    
    print("\n1. Testing channel handle validation...")
    # Valid handles
    valid_handles = ["anatolianturkishrock", "@anatolianturkishrock", "test_channel-123"]
    for handle in valid_handles:
        is_valid, error = validator.validate_channel_handle(handle)
        assert is_valid, f"Valid handle rejected: {handle}"
        print(f"  ✅ '{handle}' - Valid")
    
    # Invalid handles
    invalid_handles = [
        ("", "empty"),
        ("../../etc/passwd", "path traversal"),
        ("'; DROP TABLE users; --", "SQL injection"),
        ("<script>alert('xss')</script>", "XSS"),
    ]
    for handle, reason in invalid_handles:
        is_valid, error = validator.validate_channel_handle(handle)
        assert not is_valid, f"Invalid handle accepted: {handle} ({reason})"
        print(f"  ❌ '{handle[:30]}...' - Rejected ({reason})")
    
    print("[OK] Channel handle validation works")
    
    print("\n2. Testing niche validation...")
    # Valid niches
    valid_niches = ["psychedelic rock", "Turkish music", "70s rock"]
    for niche in valid_niches:
        is_valid, error = validator.validate_niche(niche)
        assert is_valid, f"Valid niche rejected: {niche}"
        print(f"  ✅ '{niche}' - Valid")
    
    # Invalid niches
    invalid_niches = [
        ("<script>alert('xss')</script>", "XSS"),
        ("'; DROP TABLE users; --", "SQL injection"),
    ]
    for niche, reason in invalid_niches:
        is_valid, error = validator.validate_niche(niche)
        assert not is_valid, f"Invalid niche accepted: {niche} ({reason})"
        print(f"  ❌ '{niche[:30]}...' - Rejected ({reason})")
    
    print("[OK] Niche validation works")
    
    print("\n3. Testing HTML sanitization...")
    xss_input = "<script>alert('xss')</script>Hello"
    sanitized = validator.sanitize_html(xss_input)
    assert "<script>" not in sanitized, "XSS not sanitized"
    print(f"  Input: {xss_input}")
    print(f"  Sanitized: {sanitized}")
    print("[OK] HTML sanitization works")
    
    print("\n4. Testing API key validation...")
    # Valid API keys
    valid_keys = ["AIzaSyTest123456789012345678901234567890", "test_key_12345678901234567890"]
    for key in valid_keys:
        is_valid, error = validator.validate_api_key(key)
        assert is_valid, f"Valid API key rejected: {key[:20]}... (error: {error})"
        print(f"  ✅ '{key[:20]}...' - Valid")
    
    # Invalid API keys
    invalid_keys = [
        ("short", "too short"),
        ("'; DROP TABLE users; --", "SQL injection"),
    ]
    for key, reason in invalid_keys:
        is_valid, error = validator.validate_api_key(key)
        assert not is_valid, f"Invalid API key accepted: {key} ({reason})"
        print(f"  ❌ '{key[:30]}...' - Rejected ({reason})")
    
    print("[OK] API key validation works")
    
    print("\n" + "=" * 60)
    print("[OK] All input validator tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    test_input_validator()

