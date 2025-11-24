"""
Test API Connections
Tests all configured API connections
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_youtube_api():
    """Test YouTube API connection."""
    print("[1] Testing YouTube API...")
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    if not api_key or api_key == "your_youtube_api_key_here":
        print("  [SKIP] YouTube API key not configured")
        return False
    
    try:
        from src.utils.youtube_client import create_client
        client = create_client()
        
        # Test with a simple search
        request = client.youtube.search().list(
            part="snippet",
            q="test",
            maxResults=1
        )
        response = request.execute()
        
        if response:
            print("  [OK] YouTube API connection successful")
            return True
        else:
            print("  [FAIL] YouTube API returned empty response")
            return False
    except Exception as e:
        print(f"  [FAIL] YouTube API error: {str(e)}")
        return False

def test_google_trends():
    """Test Google Trends (pytrends)."""
    print("[2] Testing Google Trends...")
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='en-US', tz=360)
        
        # Test with a simple query
        pytrends.build_payload(['test'], cat=0, timeframe='today 3-m', geo='', gprop='')
        data = pytrends.interest_over_time()
        
        if data is not None:
            print("  [OK] Google Trends connection successful")
            return True
        else:
            print("  [WARN] Google Trends returned no data (may be rate limited)")
            return False
    except ImportError:
        print("  [SKIP] pytrends not installed. Run: pip install pytrends")
        return False
    except Exception as e:
        print(f"  [WARN] Google Trends error: {str(e)}")
        return False

def test_reddit_api():
    """Test Reddit API connection."""
    print("[3] Testing Reddit API...")
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    
    if not client_id or client_id == "your_reddit_client_id_here":
        print("  [SKIP] Reddit API credentials not configured (using public API)")
        # Test public API
        try:
            import requests
            response = requests.get(
                "https://www.reddit.com/r/turkishrock/hot.json",
                headers={"User-Agent": "YouTube-SEO-AGI-Tool/1.0"},
                timeout=5
            )
            if response.status_code == 200:
                print("  [OK] Reddit public API accessible")
                return True
            else:
                print(f"  [WARN] Reddit public API returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"  [WARN] Reddit API error: {str(e)}")
            return False
    
    try:
        import praw
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=os.getenv("REDDIT_USER_AGENT", "YouTube-SEO-AGI-Tool/1.0")
        )
        
        # Test with a simple subreddit access
        subreddit = reddit.subreddit("turkishrock")
        posts = list(subreddit.hot(limit=1))
        
        if posts:
            print("  [OK] Reddit API connection successful")
            return True
        else:
            print("  [WARN] Reddit API returned no posts")
            return False
    except ImportError:
        print("  [SKIP] praw not installed. Run: pip install praw")
        return False
    except Exception as e:
        print(f"  [FAIL] Reddit API error: {str(e)}")
        return False

def test_twitter_api():
    """Test Twitter/X API connection."""
    print("[4] Testing Twitter/X API...")
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    api_key = os.getenv("TWITTER_API_KEY")
    
    if not bearer_token or bearer_token == "your_twitter_bearer_token_here":
        print("  [SKIP] Twitter API credentials not configured")
        return False
    
    try:
        import tweepy
        client = tweepy.Client(bearer_token=bearer_token)
        
        # Test with a simple search
        tweets = client.search_recent_tweets(query="test", max_results=1)
        
        if tweets:
            print("  [OK] Twitter API connection successful")
            return True
        else:
            print("  [WARN] Twitter API returned no tweets")
            return False
    except ImportError:
        print("  [SKIP] tweepy not installed. Run: pip install tweepy")
        return False
    except Exception as e:
        print(f"  [FAIL] Twitter API error: {str(e)}")
        return False

def main():
    """Run all API connection tests."""
    print("=" * 60)
    print("API Connection Tests")
    print("=" * 60)
    print()
    
    results = {
        "youtube": test_youtube_api(),
        "google_trends": test_google_trends(),
        "reddit": test_reddit_api(),
        "twitter": test_twitter_api()
    }
    
    print()
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for service, result in results.items():
        status = "[OK]" if result else "[SKIP/FAIL]"
        print(f"{status} {service.replace('_', ' ').title()}")
    
    print()
    required_ok = results["youtube"]
    optional_ok = sum([results["google_trends"], results["reddit"], results["twitter"]])
    
    if required_ok:
        print("[SUCCESS] Required API (YouTube) is configured!")
    else:
        print("[ERROR] Required API (YouTube) is not configured!")
        print("        Run: python setup_api_keys.py")
    
    if optional_ok > 0:
        print(f"[INFO] {optional_ok}/3 optional APIs configured")
    else:
        print("[INFO] No optional APIs configured (tool will work with limited features)")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

