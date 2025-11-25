"""
Setup script for authentication
Creates default users and configuration
"""

import os
import sys
from pathlib import Path
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def setup_auth():
    """Setup authentication configuration."""
    print("=" * 60)
    print("YouTube SEO AGI Tool - Authentication Setup")
    print("=" * 60)
    print()
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "auth_config.yaml"
    
    # Check if config exists
    if config_file.exists():
        print(f"[INFO] Auth config already exists at: {config_file}")
        response = input("Do you want to update it? (y/n): ").lower()
        if response != 'y':
            print("[INFO] Keeping existing config.")
            return
    
    print("Setting up authentication...")
    print()
    
    # Get admin credentials
    print("Admin User Setup:")
    admin_username = input("Admin username (default: admin): ").strip() or "admin"
    admin_email = input("Admin email (default: admin@example.com): ").strip() or "admin@example.com"
    admin_name = input("Admin display name (default: Admin User): ").strip() or "Admin User"
    admin_password = input("Admin password (default: admin123): ").strip() or "admin123"
    
    # Hash password
    hashed_password = stauth.Hasher.hash(admin_password)
    
    # Get cookie key
    cookie_key = os.getenv('AUTH_COOKIE_KEY', 'youtube_seo_agi_auth_key_2024')
    print(f"\n[INFO] Using cookie key from environment or default")
    
    # Create config
    config = {
        'credentials': {
            'usernames': {
                admin_username: {
                    'email': admin_email,
                    'failed_login_attempts': 0,
                    'logged_in': False,
                    'name': admin_name,
                    'password': hashed_password
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': cookie_key,
            'name': 'youtube_seo_agi_auth_cookie'
        },
        'pre-authorized': {
            'emails': []
        }
    }
    
    # Save config
    try:
        with open(config_file, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        print(f"\n[OK] Auth config created at: {config_file}")
        print(f"\n[INFO] Default credentials:")
        print(f"  Username: {admin_username}")
        print(f"  Password: {admin_password}")
        print(f"\n[WARNING] Change the default password after first login!")
    except Exception as e:
        print(f"\n[ERROR] Failed to create config: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import io
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    success = setup_auth()
    if success:
        print("\n" + "=" * 60)
        print("[OK] Authentication setup completed!")
        print("=" * 60)
    else:
        print("\n[FAIL] Authentication setup failed!")
        sys.exit(1)

