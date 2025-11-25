"""
Structured Logging System
Logs all events while excluding PII (Personally Identifiable Information) and secrets
"""

import logging
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import re

# Patterns to detect and mask sensitive data
SENSITIVE_PATTERNS = [
    r'api[_-]?key["\']?\s*[:=]\s*["\']?([^"\'\s]+)',
    r'password["\']?\s*[:=]\s*["\']?([^"\'\s]+)',
    r'token["\']?\s*[:=]\s*["\']?([^"\'\s]+)',
    r'secret["\']?\s*[:=]\s*["\']?([^"\'\s]+)',
    r'AIzaSy[A-Za-z0-9_-]{35}',  # YouTube API key pattern
    r'[A-Za-z0-9]{32,}',  # Long alphanumeric strings (potential tokens)
]

class SecureFormatter(logging.Formatter):
    """
    Custom formatter that masks sensitive information in log messages.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sensitive_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in SENSITIVE_PATTERNS]
    
    def format(self, record):
        """Format log record and mask sensitive data."""
        # Get the original message
        original_msg = super().format(record)
        
        # Mask sensitive data
        masked_msg = self._mask_sensitive_data(original_msg)
        
        return masked_msg
    
    def _mask_sensitive_data(self, message: str) -> str:
        """Mask sensitive data in message."""
        masked = message
        
        # Mask API keys and tokens
        for pattern in self.sensitive_patterns:
            masked = pattern.sub(self._mask_replacement, masked)
        
        return masked
    
    def _mask_replacement(self, match):
        """Replace matched sensitive data with masked version."""
        matched_text = match.group(0)
        if len(matched_text) > 10:
            # Show first 4 and last 4 characters, mask the rest
            return matched_text[:4] + "***MASKED***" + matched_text[-4:]
        else:
            return "***MASKED***"


class StructuredLogger:
    """
    Structured logger that logs events in JSON format (optional)
    and masks sensitive information.
    """
    
    def __init__(self, name: str, log_file: Optional[str] = None, json_format: bool = False):
        """
        Initialize structured logger.
        
        Args:
            name: Logger name
            log_file: Optional log file path
            json_format: Whether to use JSON format for logs
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        if json_format:
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            formatter = SecureFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if log_file specified)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.logger.critical(self._format_message(message, **kwargs))
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def security_event(self, event_type: str, message: str, **kwargs):
        """
        Log security-related event.
        
        Args:
            event_type: Type of security event (e.g., 'auth_attempt', 'api_key_change')
            message: Event message
            **kwargs: Additional event data (will be sanitized)
        """
        sanitized_kwargs = self._sanitize_data(kwargs)
        event_data = {
            'event_type': event_type,
            'message': message,
            **sanitized_kwargs
        }
        self.logger.info(f"SECURITY_EVENT: {json.dumps(event_data, default=str)}")
    
    def api_usage(self, api_name: str, endpoint: str, status: str, **kwargs):
        """
        Log API usage.
        
        Args:
            api_name: Name of API (e.g., 'youtube', 'reddit')
            endpoint: API endpoint
            status: Request status (success, error, rate_limited)
            **kwargs: Additional data (quota_used, response_time, etc.)
        """
        sanitized_kwargs = self._sanitize_data(kwargs)
        usage_data = {
            'api_name': api_name,
            'endpoint': endpoint,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            **sanitized_kwargs
        }
        self.logger.info(f"API_USAGE: {json.dumps(usage_data, default=str)}")
    
    def audit_trail(self, action: str, user_id: Optional[str] = None, **kwargs):
        """
        Log audit trail event.
        
        Args:
            action: Action performed (e.g., 'api_key_changed', 'channel_analyzed')
            user_id: Optional user identifier (will be hashed if provided)
            **kwargs: Additional audit data
        """
        sanitized_kwargs = self._sanitize_data(kwargs)
        
        # Hash user_id if provided (for privacy)
        if user_id:
            import hashlib
            user_id = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        
        audit_data = {
            'action': action,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            **sanitized_kwargs
        }
        self.logger.info(f"AUDIT_TRAIL: {json.dumps(audit_data, default=str)}")
    
    def _format_message(self, message: str, **kwargs) -> str:
        """Format message with additional context."""
        if kwargs:
            # Sanitize kwargs before adding to message
            sanitized = self._sanitize_data(kwargs)
            context = ", ".join([f"{k}={v}" for k, v in sanitized.items()])
            return f"{message} | {context}"
        return message
    
    def _sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize data by removing/masking sensitive information.
        
        Args:
            data: Dictionary of data to sanitize
            
        Returns:
            Sanitized dictionary
        """
        sanitized = {}
        sensitive_keys = ['api_key', 'password', 'token', 'secret', 'key', 'credential']
        
        for key, value in data.items():
            key_lower = key.lower()
            
            # Check if key contains sensitive terms
            if any(sensitive_term in key_lower for sensitive_term in sensitive_keys):
                sanitized[key] = "***MASKED***"
            elif isinstance(value, str) and len(value) > 20:
                # Check if value looks like a token/key
                if re.match(r'^[A-Za-z0-9_-]{20,}$', value):
                    sanitized[key] = value[:4] + "***MASKED***" + value[-4:]
                else:
                    sanitized[key] = value
            else:
                sanitized[key] = value
        
        return sanitized


# Global logger instance
_logger_instance: Optional[StructuredLogger] = None

def get_logger(name: str = "youtube_seo_agi", log_file: Optional[str] = None) -> StructuredLogger:
    """
    Get or create global logger instance.
    
    Args:
        name: Logger name
        log_file: Optional log file path
        
    Returns:
        StructuredLogger instance
    """
    global _logger_instance
    if _logger_instance is None:
        # Default log file location
        if log_file is None:
            log_file = "logs/app.log"
        _logger_instance = StructuredLogger(name, log_file)
    return _logger_instance

