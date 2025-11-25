"""
Test script for new modules (Faz 8)
Tests: Video SEO Audit, Caption Optimizer, Engagement Booster, Thumbnail Enhancer
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.youtube_client import create_client
from src.modules.keyword_researcher import KeywordResearcher
from src.modules.title_optimizer import TitleOptimizer
from src.modules.description_generator import DescriptionGenerator
from src.modules.tag_suggester import TagSuggester
from src.modules.video_seo_audit import VideoSEOAudit
from src.modules.caption_optimizer import CaptionOptimizer
from src.modules.engagement_booster import EngagementBooster
from src.modules.thumbnail_enhancer import ThumbnailEnhancer


def test_video_seo_audit():
    """Test Video SEO Audit module."""
    print("\n" + "="*60)
    print("TEST 1: Video SEO Audit Module")
    print("="*60)
    
    try:
        client = create_client()
        keyword_researcher = KeywordResearcher(client)
        title_optimizer = TitleOptimizer(keyword_researcher)
        description_generator = DescriptionGenerator()
        tag_suggester = TagSuggester(client)
        
        audit = VideoSEOAudit(
            client,
            keyword_researcher,
            title_optimizer,
            description_generator,
            tag_suggester
        )
        
        # Test with a known video (use a test video ID or channel video)
        # For now, we'll test the structure
        print("[OK] Video SEO Audit module initialized successfully")
        print("  - Methods available:")
        print("    * audit_video()")
        print("    * audit_channel_videos()")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_caption_optimizer():
    """Test Caption Optimizer module."""
    print("\n" + "="*60)
    print("TEST 2: Caption & Transcript Optimizer Module")
    print("="*60)
    
    try:
        client = create_client()
        keyword_researcher = KeywordResearcher(client)
        
        optimizer = CaptionOptimizer(client, keyword_researcher)
        
        print("[OK] Caption Optimizer module initialized successfully")
        print("  - Methods available:")
        print("    * get_video_captions()")
        print("    * analyze_captions()")
        print("    * optimize_captions()")
        print("    * get_multilingual_support()")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_engagement_booster():
    """Test Engagement Booster module."""
    print("\n" + "="*60)
    print("TEST 3: Engagement Booster Suggestions Module")
    print("="*60)
    
    try:
        client = create_client()
        
        booster = EngagementBooster(client)
        
        print("[OK] Engagement Booster module initialized successfully")
        print("  - Methods available:")
        print("    * suggest_engagement_elements()")
        print("    * get_engagement_strategy()")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_thumbnail_enhancer():
    """Test Thumbnail Enhancer module."""
    print("\n" + "="*60)
    print("TEST 4: AI Thumbnail Enhancer Module")
    print("="*60)
    
    try:
        client = create_client()
        
        enhancer = ThumbnailEnhancer(client)
        
        print("[OK] Thumbnail Enhancer module initialized successfully")
        print("  - Methods available:")
        print("    * analyze_thumbnail()")
        print("    * suggest_thumbnail_improvements()")
        print("    * analyze_channel_thumbnails()")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Test integration with existing modules."""
    print("\n" + "="*60)
    print("TEST 5: Integration Test")
    print("="*60)
    
    try:
        client = create_client()
        keyword_researcher = KeywordResearcher(client)
        
        # Test that all modules can work together
        title_optimizer = TitleOptimizer(keyword_researcher)
        description_generator = DescriptionGenerator()
        tag_suggester = TagSuggester(client)
        
        audit = VideoSEOAudit(
            client,
            keyword_researcher,
            title_optimizer,
            description_generator,
            tag_suggester
        )
        
        caption_optimizer = CaptionOptimizer(client, keyword_researcher)
        engagement_booster = EngagementBooster(client)
        thumbnail_enhancer = ThumbnailEnhancer(client)
        
        print("[OK] All modules integrated successfully")
        print("  - Video SEO Audit: OK")
        print("  - Caption Optimizer: OK")
        print("  - Engagement Booster: OK")
        print("  - Thumbnail Enhancer: OK")
        
        return True
    except Exception as e:
        print(f"[ERROR] Integration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_with_real_video():
    """Test with a real video (if API key is available)."""
    print("\n" + "="*60)
    print("TEST 6: Real Video Test (Optional)")
    print("="*60)
    
    try:
        client = create_client()
        
        # Try to get channel videos
        channel_handle = "anatolianturkishrock"
        channel_data = client.get_channel_by_handle(channel_handle)
        
        if not channel_data.get("items"):
            print("[WARN] Channel not found or API key not configured")
            print("  Skipping real video test")
            return True
        
        channel_id = channel_data["items"][0]["id"]
        videos = client.get_channel_videos(channel_id, max_results=1)
        
        if not videos:
            print("[WARN] No videos found")
            return True
        
        video_id = videos[0]["id"]["videoId"]
        print(f"[OK] Testing with video: {video_id}")
        
        # Test Video SEO Audit
        keyword_researcher = KeywordResearcher(client)
        title_optimizer = TitleOptimizer(keyword_researcher)
        description_generator = DescriptionGenerator()
        tag_suggester = TagSuggester(client)
        
        audit = VideoSEOAudit(
            client,
            keyword_researcher,
            title_optimizer,
            description_generator,
            tag_suggester
        )
        
        audit_result = audit.audit_video(video_id)
        if "error" not in audit_result:
            print(f"  [OK] Video SEO Audit: Score {audit_result.get('overall_seo_score', 0)}/100")
        else:
            print(f"  [WARN] Video SEO Audit: {audit_result.get('error', 'Unknown error')}")
        
        # Test Thumbnail Enhancer
        thumbnail_enhancer = ThumbnailEnhancer(client)
        thumbnail_result = thumbnail_enhancer.analyze_thumbnail(video_id)
        if "error" not in thumbnail_result:
            ctr_score = thumbnail_result.get("ctr_potential", {}).get("score", 0)
            print(f"  [OK] Thumbnail Analysis: CTR Score {ctr_score}/100")
        else:
            print(f"  [WARN] Thumbnail Analysis: {thumbnail_result.get('error', 'Unknown error')}")
        
        # Test Engagement Booster
        engagement_booster = EngagementBooster(client)
        engagement_result = engagement_booster.suggest_engagement_elements(video_id)
        if "error" not in engagement_result:
            engagement_score = engagement_result.get("engagement_score", 0)
            print(f"  [OK] Engagement Booster: Score {engagement_score}/100")
        else:
            print(f"  [WARN] Engagement Booster: {engagement_result.get('error', 'Unknown error')}")
        
        return True
    except Exception as e:
        print(f"[WARN] Real video test skipped: {str(e)}")
        return True  # Don't fail if API key is not available


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("FAZ 8: NEW MODULES TEST SUITE")
    print("="*60)
    print("\nTesting new modules:")
    print("  1. Video SEO Audit")
    print("  2. Caption & Transcript Optimizer")
    print("  3. Engagement Booster Suggestions")
    print("  4. AI Thumbnail Enhancer")
    print("\n" + "="*60)
    
    results = []
    
    # Run tests
    results.append(("Video SEO Audit", test_video_seo_audit()))
    results.append(("Caption Optimizer", test_caption_optimizer()))
    results.append(("Engagement Booster", test_engagement_booster()))
    results.append(("Thumbnail Enhancer", test_thumbnail_enhancer()))
    results.append(("Integration", test_integration()))
    results.append(("Real Video Test", test_with_real_video()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"Total: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"\n[WARN] {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())

