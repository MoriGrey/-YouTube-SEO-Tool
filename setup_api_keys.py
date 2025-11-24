"""
API Keys Setup Script
Helps configure API keys for YouTube SEO AGI Tool
"""

import os
from pathlib import Path

def setup_api_keys():
    """Interactive setup for API keys."""
    print("=" * 60)
    print("YouTube SEO AGI Tool - API Keys Setup")
    print("=" * 60)
    print()
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    # Check if .env exists
    if env_file.exists():
        print("[INFO] .env file already exists.")
        response = input("Do you want to update it? (y/n): ").lower()
        if response != 'y':
            print("[INFO] Keeping existing .env file.")
            return
    else:
        # Copy from .env.example if it exists
        if env_example.exists():
            print("[INFO] Creating .env from .env.example...")
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
        else:
            print("[ERROR] .env.example not found. Creating basic .env file...")
            with open(env_file, 'w') as f:
                f.write("# YouTube SEO AGI Tool - Environment Variables\n")
    
    print()
    print("Please enter your API keys (press Enter to skip optional ones):")
    print()
    
    # YouTube API Key (Required)
    print("1. YouTube Data API v3 Key (REQUIRED)")
    print("   Get it from: https://console.cloud.google.com/apis/credentials")
    youtube_key = input("   YouTube API Key: ").strip()
    if youtube_key:
        update_env_file(env_file, "YOUTUBE_API_KEY", youtube_key)
    
    print()
    print("2. Reddit API (Optional)")
    print("   Get credentials from: https://www.reddit.com/prefs/apps")
    reddit_client_id = input("   Reddit Client ID: ").strip()
    reddit_client_secret = input("   Reddit Client Secret: ").strip()
    if reddit_client_id:
        update_env_file(env_file, "REDDIT_CLIENT_ID", reddit_client_id)
    if reddit_client_secret:
        update_env_file(env_file, "REDDIT_CLIENT_SECRET", reddit_client_secret)
    
    print()
    print("3. Twitter/X API (Optional)")
    print("   Get credentials from: https://developer.twitter.com/en/portal/dashboard")
    twitter_api_key = input("   Twitter API Key: ").strip()
    twitter_api_secret = input("   Twitter API Secret: ").strip()
    twitter_access_token = input("   Twitter Access Token: ").strip()
    twitter_access_token_secret = input("   Twitter Access Token Secret: ").strip()
    twitter_bearer = input("   Twitter Bearer Token: ").strip()
    
    if twitter_api_key:
        update_env_file(env_file, "TWITTER_API_KEY", twitter_api_key)
    if twitter_api_secret:
        update_env_file(env_file, "TWITTER_API_SECRET", twitter_api_secret)
    if twitter_access_token:
        update_env_file(env_file, "TWITTER_ACCESS_TOKEN", twitter_access_token)
    if twitter_access_token_secret:
        update_env_file(env_file, "TWITTER_ACCESS_TOKEN_SECRET", twitter_access_token_secret)
    if twitter_bearer:
        update_env_file(env_file, "TWITTER_BEARER_TOKEN", twitter_bearer)
    
    print()
    print("4. Target Channel Settings")
    channel_handle = input("   Channel Handle (default: anatolianturkishrock): ").strip()
    if channel_handle:
        update_env_file(env_file, "TARGET_CHANNEL_HANDLE", channel_handle)
    
    print()
    print("=" * 60)
    print("[SUCCESS] API keys configured!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Verify your .env file")
    print("2. Run: python test_api_connections.py")
    print("3. Start the dashboard: streamlit run dashboard.py")

def update_env_file(env_file: Path, key: str, value: str):
    """Update or add a key-value pair in .env file."""
    if not env_file.exists():
        return
    
    lines = []
    key_found = False
    
    # Read existing file
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip().startswith(f"{key}="):
                lines.append(f"{key}={value}\n")
                key_found = True
            else:
                lines.append(line)
    
    # Add if not found
    if not key_found:
        lines.append(f"{key}={value}\n")
    
    # Write back
    with open(env_file, 'w') as f:
        f.writelines(lines)

if __name__ == "__main__":
    setup_api_keys()

