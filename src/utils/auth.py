"""
Authentication Module
Handles user authentication using Streamlit-Authenticator
"""

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from typing import Optional, Dict, Any
import hashlib
import os

from src.utils.logger import get_logger

logger = get_logger("auth")

class AuthenticationManager:
    """
    Manages user authentication for the application.
    
    Security Features:
    - Password hashing (bcrypt)
    - Session-based authentication
    - Cookie-based session management
    - Audit logging
    """
    
    CONFIG_FILE = "config/auth_config.yaml"
    
    def __init__(self):
        """Initialize authentication manager."""
        self.config = self._load_config()
        self.authenticator = None
        self._initialize_authenticator()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load authentication configuration.
        
        Returns:
            Configuration dictionary
        """
        config_path = Path(self.CONFIG_FILE)
        
        # Create default config if doesn't exist
        if not config_path.exists():
            self._create_default_config(config_path)
        
        try:
            with open(config_path, 'r') as file:
                config = yaml.load(file, Loader=SafeLoader)
            return config
        except Exception as e:
            logger.error(f"Failed to load auth config: {e}")
            # Return default config
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default authentication configuration."""
        return {
            'credentials': {
                'usernames': {
                    'admin': {
                        'email': 'admin@example.com',
                        'failed_login_attempts': 0,
                        'logged_in': False,
                        'name': 'Admin User',
                        'password': stauth.Hasher.hash('admin123')  # Default password
                    }
                }
            },
            'cookie': {
                'expiry_days': 30,
                'key': os.getenv('AUTH_COOKIE_KEY', 'youtube_seo_agi_auth_key_2024'),
                'name': 'youtube_seo_agi_auth_cookie'
            },
            'pre-authorized': {
                'emails': []
            }
        }
    
    def _create_default_config(self, config_path: Path):
        """Create default authentication configuration file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate default password hash
        default_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        hashed_password = stauth.Hasher.hash(default_password)
        
        config = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'email': 'admin@example.com',
                        'failed_login_attempts': 0,
                        'logged_in': False,
                        'name': 'Admin User',
                        'password': hashed_password
                    }
                }
            },
            'cookie': {
                'expiry_days': 30,
                'key': os.getenv('AUTH_COOKIE_KEY', 'youtube_seo_agi_auth_key_2024'),
                'name': 'youtube_seo_agi_auth_cookie'
            },
            'pre-authorized': {
                'emails': []
            }
        }
        
        try:
            with open(config_path, 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            logger.info("Default auth config created")
        except Exception as e:
            logger.error(f"Failed to create auth config: {e}")
    
    def _initialize_authenticator(self):
        """Initialize Streamlit Authenticator."""
        try:
            self.authenticator = stauth.Authenticate(
                self.config['credentials'],
                self.config['cookie']['name'],
                self.config['cookie']['key'],
                cookie_expiry_days=self.config['cookie']['expiry_days'],
                pre_authorized=self.config.get('pre-authorized', {})
            )
        except Exception as e:
            logger.error(f"Failed to initialize authenticator: {e}")
            raise
    
    def login(self):
        """
        Handle user login.
        
        Returns:
            True if login successful, False if failed, None if form not submitted yet
        """
        try:
            # Streamlit-Authenticator 0.4.2+ uses location and key parameters
            # This will automatically render the login form
            login_result = self.authenticator.login(
                location='main',
                key='LoginForm'
            )
            
            # Handle None return (form not submitted yet - form is rendered, wait for user input)
            if login_result is None:
                # Form is displayed, return None to indicate waiting for user input
                return None
            
            # Unpack result - should be a tuple (name, authentication_status, username)
            if not isinstance(login_result, tuple) or len(login_result) != 3:
                logger.error(f"Unexpected login result format: {login_result}")
                return None  # Return None to keep form visible
            
            name, authentication_status, username = login_result
            
            if authentication_status:
                # Log successful login
                logger.security_event(
                    "login_success",
                    f"User logged in successfully",
                    username=username,
                    name=name
                )
                logger.audit_trail("user_login", user_id=username, success=True)
                
                # Store in session state
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['user_name'] = name
                
                return True
            elif authentication_status == False:
                # Log failed login
                logger.security_event(
                    "login_failed",
                    "Failed login attempt",
                    username=username if username else "unknown"
                )
                logger.audit_trail("user_login", user_id=username if username else "unknown", success=False)
                
                st.error('Username/password is incorrect')
                return False
            elif authentication_status == None:
                # Login form shown, waiting for input
                return False
            else:
                return False
                
        except Exception as e:
            logger.error(f"Login error: {e}", error_type="login_error")
            st.error(f"Authentication error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def logout(self):
        """Handle user logout."""
        # CRITICAL: Initialize 'logout' key BEFORE calling authenticator.logout()
        # Streamlit-Authenticator's logout() method accesses st.session_state['logout']
        # According to Streamlit docs: https://docs.streamlit.io/develop/concepts/architecture/session-state#initialization
        # We must initialize keys before accessing them
        if 'logout' not in st.session_state:
            st.session_state['logout'] = False
        
        # Initialize other required keys
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'user_name' not in st.session_state:
            st.session_state['user_name'] = None
        
        # Log logout if authenticated
        if st.session_state.get('authenticated'):
            username = st.session_state.get('username', 'unknown')
            
            # Log logout
            logger.security_event("logout", "User logged out", username=username)
            logger.audit_trail("user_logout", user_id=username)
        
        # Clear authentication state BEFORE calling authenticator.logout()
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.session_state['user_name'] = None
        
        # Call authenticator.logout() - ensure 'logout' key exists
        # Note: We initialize 'logout' key at the start of this method
        # But Streamlit-Authenticator may access it internally, so we ensure it exists
        try:
            # Double-check logout key exists (defensive programming)
            if 'logout' not in st.session_state:
                st.session_state['logout'] = False
            
            # Streamlit-Authenticator 0.4.2+ uses location and key parameters
            # The 'logout' key is already initialized above
            self.authenticator.logout(
                location='sidebar',
                key='LogoutButton'
            )
        except (KeyError, AttributeError) as e:
            # Handle missing session state key error
            error_msg = str(e)
            logger.warning(f"Logout key error (handled): {error_msg}")
            
            # Ensure logout key exists
            if 'logout' not in st.session_state:
                st.session_state['logout'] = False
            
            # Try manual logout - authentication already cleared above
            # Set logout flag
            st.session_state['logout'] = True
            
            # Don't raise exception - logout is handled manually
        except Exception as e:
            # If logout fails, authentication is already cleared above
            logger.warning(f"Logout error (handled): {e}")
            # Ensure logout key is set
            if 'logout' not in st.session_state:
                st.session_state['logout'] = False
            st.session_state['logout'] = True
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return st.session_state.get('authenticated', False)
    
    def get_username(self) -> Optional[str]:
        """Get current username."""
        return st.session_state.get('username')
    
    def get_user_name(self) -> Optional[str]:
        """Get current user's display name."""
        return st.session_state.get('user_name')
    
    def require_authentication(self):
        """
        Require authentication - redirect to login if not authenticated.
        Call this at the start of dashboard.
        """
        if not self.is_authenticated():
            # Show login form
            if self.login():
                st.rerun()
            else:
                st.stop()


# Global authentication manager instance
_auth_manager: Optional[AuthenticationManager] = None

def get_auth_manager() -> AuthenticationManager:
    """
    Get or create global authentication manager instance.
    
    Returns:
        AuthenticationManager instance
    """
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthenticationManager()
    return _auth_manager

def require_auth():
    """Require authentication - convenience function."""
    auth_manager = get_auth_manager()
    auth_manager.require_authentication()

