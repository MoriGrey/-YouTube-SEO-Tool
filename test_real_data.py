"""
Real Data Test Script
Tests the system with real channel data
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

def test_channel_analysis():
    """Test channel analysis with real data."""
    print("[1] Testing Channel Analysis...")
    try:
        from src.utils.youtube_client import create_client
        from src.modules.channel_analyzer import ChannelAnalyzer
        
        client = create_client()
        analyzer = ChannelAnalyzer(client)
        
        channel_handle = os.getenv("TARGET_CHANNEL_HANDLE", "anatolianturkishrock")
        print(f"  Analyzing channel: @{channel_handle}")
        
        analysis = analyzer.analyze_channel(channel_handle)
        
        if analysis:
            print(f"  [OK] Channel analyzed successfully")
            print(f"  - Subscribers: {analysis.get('channel_stats', {}).get('subscribers', 'N/A')}")
            print(f"  - Total Views: {analysis.get('channel_stats', {}).get('total_views', 'N/A')}")
            print(f"  - Video Count: {analysis.get('channel_stats', {}).get('video_count', 'N/A')}")
            return True
        else:
            print("  [FAIL] Analysis returned empty")
            return False
    except Exception as e:
        print(f"  [FAIL] Error: {str(e)}")
        return False

def test_keyword_research():
    """Test keyword research with real data."""
    print("[2] Testing Keyword Research...")
    try:
        from src.utils.youtube_client import create_client
        from src.modules.keyword_researcher import KeywordResearcher
        
        client = create_client()
        researcher = KeywordResearcher(client)
        
        keywords = researcher.research_keywords("anadolu rock", max_results=5)
        
        if keywords and len(keywords) > 0:
            print(f"  [OK] Found {len(keywords)} keywords")
            print(f"  - Top keyword: {keywords[0].get('keyword', 'N/A')}")
            return True
        else:
            print("  [FAIL] No keywords found")
            return False
    except Exception as e:
        print(f"  [FAIL] Error: {str(e)}")
        return False

def test_performance_tracking():
    """Test performance tracking."""
    print("[3] Testing Performance Tracking...")
    try:
        from src.utils.youtube_client import create_client
        from src.modules.performance_tracker import PerformanceTracker
        
        client = create_client()
        tracker = PerformanceTracker(client)
        
        channel_handle = os.getenv("TARGET_CHANNEL_HANDLE", "anatolianturkishrock")
        snapshot = tracker.track_snapshot(channel_handle)
        
        if snapshot:
            print(f"  [OK] Performance snapshot created")
            print(f"  - Timestamp: {snapshot.get('timestamp', 'N/A')}")
            return True
        else:
            print("  [FAIL] Snapshot creation failed")
            return False
    except Exception as e:
        print(f"  [FAIL] Error: {str(e)}")
        return False

def test_multi_source_integration():
    """Test multi-source data integration."""
    print("[4] Testing Multi-Source Integration...")
    try:
        from src.utils.youtube_client import create_client
        from src.modules.multi_source_integrator import MultiSourceIntegrator
        
        client = create_client()
        integrator = MultiSourceIntegrator(client)
        
        # Test Google Trends
        trends = integrator.get_google_trends(["anadolu rock", "turkish rock"], region="TR")
        if trends and not trends.get("error"):
            print(f"  [OK] Google Trends data retrieved")
        else:
            print(f"  [WARN] Google Trends: {trends.get('error', 'No data')}")
        
        # Test Reddit
        reddit = integrator.get_reddit_trends(["turkishrock"], limit=3)
        if reddit and reddit.get("trending_posts"):
            print(f"  [OK] Reddit data retrieved")
        else:
            print(f"  [WARN] Reddit: {reddit.get('error', 'No data')}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Error: {str(e)}")
        return False

def test_safety_ethics():
    """Test safety and ethics layer."""
    print("[5] Testing Safety & Ethics Layer...")
    try:
        from src.modules.safety_ethics_layer import SafetyEthicsLayer
        
        layer = SafetyEthicsLayer()
        
        # Test safe content
        result = layer.check_content_safety(
            title="Anadolu Rock Müzik Koleksiyonu",
            description="Türk rock müziğinin en iyi örnekleri",
            tags=["anadolu rock", "türk müzik"]
        )
        
        if result and result.get("safety_status"):
            print(f"  [OK] Safety check completed")
            print(f"  - Status: {result.get('safety_status')}")
            print(f"  - Risk Score: {result.get('risk_score', 0):.2f}")
            return True
        else:
            print("  [FAIL] Safety check failed")
            return False
    except Exception as e:
        print(f"  [FAIL] Error: {str(e)}")
        return False

def main():
    """Run all real data tests."""
    print("=" * 60)
    print("Real Data Test Suite")
    print("=" * 60)
    print()
    
    results = {
        "channel_analysis": test_channel_analysis(),
        "keyword_research": test_keyword_research(),
        "performance_tracking": test_performance_tracking(),
        "multi_source": test_multi_source_integration(),
        "safety_ethics": test_safety_ethics()
    }
    
    print()
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "[OK]" if result else "[FAIL]"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    passed = sum(results.values())
    total = len(results)
    
    print()
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("[SUCCESS] All tests passed!")
    else:
        print("[WARNING] Some tests failed")
    
    print("=" * 60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

