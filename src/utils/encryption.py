"""
Encryption Utilities for Secure API Key Storage
Uses Fernet (symmetric encryption) for API key protection
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Optional
import logging

# Configure logging (without exposing secrets)
logger = logging.getLogger(__name__)

class EncryptionManager:
    """
    Manages encryption/decryption of sensitive data (API keys).
    
    Security Features:
    - Fernet symmetric encryption (AES 128 in CBC mode)
    - Key derivation from password (PBKDF2)
    - Secure key management
    - No secrets in logs
    """
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize encryption manager.
        
        Args:
            encryption_key: Optional encryption key. If not provided, 
                          will try to get from environment or generate new.
        """
        self._fernet = None
        self._encryption_key = encryption_key or self._get_or_create_key()
        self._initialize_fernet()
    
    def _get_or_create_key(self) -> str:
        """
        Get encryption key from environment or create new one.
        
        Returns:
            Encryption key as string
        """
        # Try to get from environment variable
        env_key = os.getenv("ENCRYPTION_KEY")
        if env_key:
            logger.info("Using encryption key from environment variable")
            return env_key
        
        # For web deployment, generate a key based on app instance
        # In production, this should be set as environment variable
        logger.warning("ENCRYPTION_KEY not found in environment. Generating session-based key.")
        logger.warning("For production, set ENCRYPTION_KEY environment variable for persistent encryption.")
        
        # Generate a key (in production, this should be set as env var)
        # For now, we'll use a session-based approach
        # WARNING: This means keys won't persist across app restarts
        # For production, ENCRYPTION_KEY must be set
        key = Fernet.generate_key()
        return key.decode()
    
    def _initialize_fernet(self):
        """Initialize Fernet cipher with encryption key."""
        try:
            # If key is already a Fernet key (base64), use directly
            if isinstance(self._encryption_key, str):
                # Try to decode as base64 Fernet key
                try:
                    key_bytes = self._encryption_key.encode() if not self._encryption_key.startswith('gAAAAA') else base64.urlsafe_b64encode(self._encryption_key.encode())
                    self._fernet = Fernet(key_bytes)
                except Exception:
                    # If not valid Fernet key, derive from password
                    key_bytes = self._derive_key_from_password(self._encryption_key)
                    self._fernet = Fernet(key_bytes)
            else:
                self._fernet = Fernet(self._encryption_key)
        except Exception as e:
            logger.error(f"Failed to initialize Fernet: {e}")
            raise ValueError("Failed to initialize encryption. Invalid encryption key.")
    
    def _derive_key_from_password(self, password: str) -> bytes:
        """
        Derive encryption key from password using PBKDF2.
        
        Args:
            password: Password string
            
        Returns:
            Derived key bytes
        """
        # Use a fixed salt for consistency (in production, use random salt stored separately)
        # For web apps, we can use app instance ID or similar
        salt = os.getenv("ENCRYPTION_SALT", "youtube_seo_agi_tool_salt_2024").encode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext string.
        
        Args:
            plaintext: String to encrypt (e.g., API key)
            
        Returns:
            Encrypted string (base64 encoded)
            
        Raises:
            ValueError: If encryption fails
        """
        if not plaintext:
            return ""
        
        try:
            encrypted_bytes = self._fernet.encrypt(plaintext.encode())
            encrypted_str = encrypted_bytes.decode()
            logger.debug("Data encrypted successfully")
            return encrypted_str
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise ValueError(f"Failed to encrypt data: {e}")
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext string.
        
        Args:
            ciphertext: Encrypted string (base64 encoded)
            
        Returns:
            Decrypted plaintext string
            
        Raises:
            ValueError: If decryption fails
        """
        if not ciphertext:
            return ""
        
        try:
            decrypted_bytes = self._fernet.decrypt(ciphertext.encode())
            decrypted_str = decrypted_bytes.decode()
            logger.debug("Data decrypted successfully")
            return decrypted_str
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise ValueError(f"Failed to decrypt data: {e}")
    
    @staticmethod
    def generate_key() -> str:
        """
        Generate a new Fernet encryption key.
        
        Returns:
            Base64-encoded encryption key
        """
        key = Fernet.generate_key()
        return key.decode()
    
    def is_encrypted(self, data: str) -> bool:
        """
        Check if data appears to be encrypted.
        
        Args:
            data: String to check
            
        Returns:
            True if data looks encrypted, False otherwise
        """
        if not data:
            return False
        
        # Fernet encrypted data starts with 'gAAAAA' (base64 encoded)
        try:
            # Try to decode as base64
            base64.b64decode(data, validate=True)
            # If it's valid base64 and starts with Fernet marker, likely encrypted
            return data.startswith('gAAAAA')
        except Exception:
            return False


# Global encryption manager instance
_encryption_manager: Optional[EncryptionManager] = None

def get_encryption_manager() -> EncryptionManager:
    """
    Get or create global encryption manager instance.
    
    Returns:
        EncryptionManager instance
    """
    global _encryption_manager
    if _encryption_manager is None:
        _encryption_manager = EncryptionManager()
    return _encryption_manager

def encrypt_api_key(api_key: str) -> str:
    """
    Encrypt API key.
    
    Args:
        api_key: Plaintext API key
        
    Returns:
        Encrypted API key
    """
    manager = get_encryption_manager()
    return manager.encrypt(api_key)

def decrypt_api_key(encrypted_key: str) -> str:
    """
    Decrypt API key.
    
    Args:
        encrypted_key: Encrypted API key
        
    Returns:
        Decrypted API key
    """
    manager = get_encryption_manager()
    return manager.decrypt(encrypted_key)

