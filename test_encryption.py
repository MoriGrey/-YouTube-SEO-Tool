"""
Test script for encryption functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.encryption import encrypt_api_key, decrypt_api_key, get_encryption_manager, EncryptionManager

def test_encryption():
    """Test encryption and decryption."""
    print("Testing API Key Encryption...")
    print("=" * 60)
    
    # Test API key
    test_api_key = "AIzaSyTest123456789012345678901234567890"
    
    print(f"Original API Key: {test_api_key[:20]}...")
    
    # Test encryption
    try:
        encrypted = encrypt_api_key(test_api_key)
        print(f"[OK] Encryption successful")
        print(f"Encrypted (first 30 chars): {encrypted[:30]}...")
        
        # Test decryption
        decrypted = decrypt_api_key(encrypted)
        print(f"[OK] Decryption successful")
        print(f"Decrypted: {decrypted[:20]}...")
        
        # Verify
        if decrypted == test_api_key:
            print("[OK] Encryption/Decryption test PASSED")
            return True
        else:
            print("[FAIL] Encryption/Decryption test FAILED - Keys don't match")
            return False
            
    except Exception as e:
        print(f"[FAIL] Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_encryption_manager():
    """Test EncryptionManager class."""
    print("\nTesting EncryptionManager...")
    print("=" * 60)
    
    try:
        manager = EncryptionManager()
        print("[OK] EncryptionManager initialized")
        
        test_data = "test_api_key_12345"
        encrypted = manager.encrypt(test_data)
        decrypted = manager.decrypt(encrypted)
        
        if decrypted == test_data:
            print("[OK] EncryptionManager test PASSED")
            return True
        else:
            print("[FAIL] EncryptionManager test FAILED")
            return False
            
    except Exception as e:
        print(f"[FAIL] Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import io
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("API Key Encryption Test Suite")
    print("=" * 60)
    print()
    
    result1 = test_encryption()
    result2 = test_encryption_manager()
    
    print()
    print("=" * 60)
    if result1 and result2:
        print("[OK] All tests PASSED")
        sys.exit(0)
    else:
        print("[FAIL] Some tests FAILED")
        sys.exit(1)

