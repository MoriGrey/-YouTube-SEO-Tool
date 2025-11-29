"""
Input Validation Module
Protects against XSS, SQL injection, and other injection attacks
"""

import re
import html
from typing import Optional, Tuple, List, Dict, Any
import bleach
from urllib.parse import quote, unquote

from src.utils.logger import get_logger

logger = get_logger("input_validator")


class InputValidator:
    """
    Validates and sanitizes user inputs.
    
    Security Features:
    - XSS protection (HTML sanitization)
    - SQL injection protection
    - Path traversal protection
    - Command injection protection
    - Input length validation
    - Special character validation
    """
    
    # Allowed HTML tags (for rich text, if needed)
    ALLOWED_TAGS = ['b', 'i', 'u', 'strong', 'em', 'p', 'br']
    
    # Dangerous patterns
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|SCRIPT)\b)",
        r"(--|#|/\*|\*/)",
        r"(\bOR\b.*=.*)",
        r"(\bAND\b.*=.*)",
        r"('|;|--|/\*|\*/)",
    ]
    
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"<iframe[^>]*>.*?</iframe>",
        r"javascript:",
        r"on\w+\s*=",  # onclick=, onerror=, etc.
        r"<img[^>]*onerror",
        r"<svg[^>]*onload",
    ]
    
    COMMAND_INJECTION_PATTERNS = [
        r"[;&|`$(){}[\]<>]",
        r"\b(cat|ls|pwd|cd|rm|mv|cp|chmod|chown|sudo|su)\b",
        r"\.\./",  # Path traversal
        r"\.\.\\",  # Windows path traversal
    ]
    
    def __init__(self):
        """Initialize input validator."""
        # Compile regex patterns for performance
        self.sql_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.SQL_INJECTION_PATTERNS]
        self.xss_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.XSS_PATTERNS]
        self.command_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.COMMAND_INJECTION_PATTERNS]
    
    def sanitize_html(self, text: str, allow_rich_text: bool = False) -> str:
        """
        Sanitize HTML to prevent XSS attacks.
        
        Args:
            text: Input text that may contain HTML
            allow_rich_text: If True, allow some safe HTML tags
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        if allow_rich_text:
            # Use bleach to sanitize, allowing only safe tags
            cleaned = bleach.clean(
                text,
                tags=self.ALLOWED_TAGS,
                attributes={},
                strip=True
            )
        else:
            # Strip all HTML tags
            cleaned = bleach.clean(text, tags=[], strip=True)
        
        # Additional XSS pattern check
        for pattern in self.xss_patterns:
            if pattern.search(cleaned):
                logger.warning(f"XSS pattern detected in input: {pattern.pattern}")
                cleaned = pattern.sub("", cleaned)
        
        return cleaned
    
    def sanitize_string(self, text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize string input.
        
        Args:
            text: Input string
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not text:
            return ""
        
        # HTML escape
        sanitized = html.escape(text)
        
        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        # Length check
        if max_length and len(sanitized) > max_length:
            logger.warning(f"Input exceeded max length: {len(sanitized)} > {max_length}")
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    def validate_channel_handle(self, handle: str) -> Tuple[bool, Optional[str]]:
        """
        Validate YouTube channel handle.
        
        Args:
            handle: Channel handle (e.g., @anatolianturkishrock)
            
        Returns:
            (is_valid, error_message)
        """
        if not handle:
            return False, "Channel handle cannot be empty"
        
        # Remove @ if present
        handle = handle.lstrip("@").strip()
        
        if not handle:
            return False, "Channel handle cannot be empty"
        
        # Check length
        if len(handle) > 100:
            return False, "Channel handle too long (max 100 characters)"
        
        # Check for dangerous characters
        if not re.match(r'^[a-zA-Z0-9_-]+$', handle):
            return False, "Channel handle contains invalid characters"
        
        # Check for injection patterns
        for pattern in self.sql_patterns:
            if pattern.search(handle):
                logger.security_event("sql_injection_attempt", "SQL injection pattern detected in channel handle")
                return False, "Invalid channel handle format"
        
        for pattern in self.command_patterns:
            if pattern.search(handle):
                logger.security_event("command_injection_attempt", "Command injection pattern detected in channel handle")
                return False, "Invalid channel handle format"
        
        return True, None
    
    def validate_niche(self, niche: str) -> Tuple[bool, Optional[str]]:
        """
        Validate niche input.
        
        Args:
            niche: Niche description
            
        Returns:
            (is_valid, error_message)
        """
        if not niche:
            return False, "Niche cannot be empty"
        
        niche = niche.strip()
        
        # Check length
        if len(niche) > 200:
            return False, "Niche too long (max 200 characters)"
        
        # Sanitize HTML
        niche = self.sanitize_html(niche, allow_rich_text=False)
        
        # Check for dangerous patterns
        for pattern in self.sql_patterns:
            if pattern.search(niche):
                logger.security_event("sql_injection_attempt", "SQL injection pattern detected in niche")
                return False, "Invalid niche format"
        
        for pattern in self.xss_patterns:
            if pattern.search(niche):
                logger.security_event("xss_attempt", "XSS pattern detected in niche")
                return False, "Invalid niche format"
        
        return True, None
    
    def validate_api_key(self, api_key: str) -> Tuple[bool, Optional[str]]:
        """
        Validate API key format.
        
        Args:
            api_key: API key string
            
        Returns:
            (is_valid, error_message)
        """
        if not api_key:
            return False, "API key cannot be empty"
        
        # Remove all whitespace characters (spaces, tabs, newlines, etc.)
        api_key = re.sub(r'\s+', '', api_key.strip())
        
        # Check length (YouTube API keys are typically 39 characters)
        if len(api_key) < 20:
            return False, "API key too short (minimum 20 characters)"
        
        if len(api_key) > 200:
            return False, "API key too long (maximum 200 characters)"
        
        # Check for dangerous characters - YouTube API keys only contain alphanumeric, dash, and underscore
        # Allow only: letters, numbers, dash (-), underscore (_)
        if not re.match(r'^[a-zA-Z0-9_-]+$', api_key):
            return False, f"API key contains invalid characters. Only letters, numbers, dash (-), and underscore (_) are allowed."
        
        # Note: We don't check for SQL injection patterns in API keys because:
        # 1. API keys are not used in SQL queries
        # 2. API keys have a strict format (alphanumeric + dash/underscore only)
        # 3. False positives could block valid API keys
        
        return True, None
    
    def validate_search_query(self, query: str) -> Tuple[bool, Optional[str]]:
        """
        Validate search query.
        
        Args:
            query: Search query string
            
        Returns:
            (is_valid, error_message)
        """
        if not query:
            return False, "Search query cannot be empty"
        
        query = query.strip()
        
        # Check length
        if len(query) > 500:
            return False, "Search query too long (max 500 characters)"
        
        # Sanitize HTML
        query = self.sanitize_html(query, allow_rich_text=False)
        
        # Check for dangerous patterns
        for pattern in self.sql_patterns:
            if pattern.search(query):
                logger.security_event("sql_injection_attempt", "SQL injection pattern detected in search query")
                return False, "Invalid search query format"
        
        for pattern in self.xss_patterns:
            if pattern.search(query):
                logger.security_event("xss_attempt", "XSS pattern detected in search query")
                return False, "Invalid search query format"
        
        return True, None
    
    def validate_url(self, url: str) -> Tuple[bool, Optional[str]]:
        """
        Validate URL input.
        
        Args:
            url: URL string
            
        Returns:
            (is_valid, error_message)
        """
        if not url:
            return False, "URL cannot be empty"
        
        url = url.strip()
        
        # Check length
        if len(url) > 2000:
            return False, "URL too long (max 2000 characters)"
        
        # Basic URL format check
        if not re.match(r'^https?://', url, re.IGNORECASE):
            return False, "URL must start with http:// or https://"
        
        # Check for dangerous patterns
        for pattern in self.xss_patterns:
            if pattern.search(url):
                logger.security_event("xss_attempt", "XSS pattern detected in URL")
                return False, "Invalid URL format"
        
        # Check for javascript: protocol
        if re.search(r'javascript:', url, re.IGNORECASE):
            logger.security_event("xss_attempt", "JavaScript protocol detected in URL")
            return False, "Invalid URL format"
        
        return True, None
    
    def validate_filename(self, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate filename input (prevents path traversal).
        
        Args:
            filename: Filename string
            
        Returns:
            (is_valid, error_message)
        """
        if not filename:
            return False, "Filename cannot be empty"
        
        filename = filename.strip()
        
        # Check for path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            logger.security_event("path_traversal_attempt", "Path traversal detected in filename")
            return False, "Invalid filename: path traversal not allowed"
        
        # Check length
        if len(filename) > 255:
            return False, "Filename too long (max 255 characters)"
        
        # Check for dangerous characters
        if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
            return False, "Filename contains invalid characters"
        
        return True, None
    
    def sanitize_for_logging(self, text: str) -> str:
        """
        Sanitize text for logging (removes sensitive data patterns).
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text safe for logging
        """
        if not text:
            return ""
        
        # Remove potential API keys (AIza...)
        text = re.sub(r'AIza[0-9A-Za-z_-]{35}', 'AIza***MASKED***', text)
        
        # Remove potential passwords (common patterns)
        text = re.sub(r'password["\']?\s*[:=]\s*["\']?([^"\']+)', r'password="***MASKED***"', text, flags=re.IGNORECASE)
        
        # Remove potential tokens
        text = re.sub(r'token["\']?\s*[:=]\s*["\']?([^"\']+)', r'token="***MASKED***"', text, flags=re.IGNORECASE)
        
        return text


# Global validator instance
_validator: Optional[InputValidator] = None

def get_validator() -> InputValidator:
    """
    Get or create global input validator instance.
    
    Returns:
        InputValidator instance
    """
    global _validator
    if _validator is None:
        _validator = InputValidator()
    return _validator

def validate_channel_handle(handle: str) -> Tuple[bool, Optional[str]]:
    """Validate channel handle - convenience function."""
    validator = get_validator()
    return validator.validate_channel_handle(handle)

def validate_niche(niche: str) -> Tuple[bool, Optional[str]]:
    """Validate niche - convenience function."""
    validator = get_validator()
    return validator.validate_niche(niche)

def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize string - convenience function."""
    validator = get_validator()
    return validator.sanitize_string(text, max_length)

