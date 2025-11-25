"""
Test script to verify all modules work correctly with different niches.
Tests niche and channel parameter integration across all modules.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.youtube_client import YouTubeClient
from src.modules.keyword_researcher import KeywordResearcher
from src.modules.title_optimizer import TitleOptimizer
from src.modules.description_generator import DescriptionGenerator
from src.modules.tag_suggester import TagSuggester
from src.modules.viral_predictor import ViralPredictor
from src.modules.trend_predictor import TrendPredictor
from src.modules.channel_analyzer import ChannelAnalyzer

# Test niches
TEST_NICHES = [
    "oriental techno music",
    "psychedelic anatolian rock",
    "jazz fusion",
    "electronic dance music",
    "indie folk"
]

TEST_CHANNELS = [
    "mori_grey",
    "anatolianturkishrock",
    "test_channel"
]

# Test data
TEST_TITLE = "ILLUSION"
TEST_SONG_NAME = "ILLUSION"
TEST_DESCRIPTION = "A beautiful track that combines different musical elements."
TEST_TAGS = ["music", "song", "track"]


def test_title_optimizer(niche: str):
    """Test TitleOptimizer with different niches."""
    print(f"\n{'='*60}")
    print(f"Testing TitleOptimizer with niche: '{niche}'")
    print(f"{'='*60}")
    
    try:
        client = YouTubeClient()
        keyword_researcher = KeywordResearcher(client)
        optimizer = TitleOptimizer(keyword_researcher)
        
        variations = optimizer.generate_title_variations(
            base_title=TEST_TITLE,
            song_name=TEST_SONG_NAME,
            num_variations=3,
            niche=niche
        )
        
        # Check if niche appears in variations
        niche_found = False
        niche_words = niche.lower().split()
        
        for var in variations:
            title_lower = var["title"].lower()
            if any(word in title_lower for word in niche_words if len(word) > 3):
                niche_found = True
                print(f"  [OK] Variation contains niche: '{var['title']}'")
                break
        
        if not niche_found:
            print(f"  [WARNING] Niche '{niche}' not found in any variation")
            print(f"  Variations: {[v['title'] for v in variations]}")
        else:
            print(f"  [PASS] TitleOptimizer works with niche '{niche}'")
        
        return niche_found
        
    except Exception as e:
        print(f"  [FAIL] Error testing TitleOptimizer: {e}")
        return False


def test_description_generator(niche: str, channel: str):
    """Test DescriptionGenerator with different niches and channels."""
    print(f"\n{'='*60}")
    print(f"Testing DescriptionGenerator with niche: '{niche}', channel: '{channel}'")
    print(f"{'='*60}")
    
    try:
        generator = DescriptionGenerator()
        
        result = generator.generate_description(
            video_title=TEST_TITLE,
            song_name=TEST_SONG_NAME,
            niche=niche,
            channel_handle=channel
        )
        
        description = result["description"].lower()
        niche_words = niche.lower().split()
        channel_found = channel.lower() in description or f"@{channel}" in description
        
        # Check if niche appears in description
        niche_found = any(word in description for word in niche_words if len(word) > 3)
        
        if niche_found:
            print(f"  [OK] Niche '{niche}' found in description")
        else:
            print(f"  [WARNING] Niche '{niche}' not found in description")
        
        if channel_found:
            print(f"  [OK] Channel '{channel}' found in description")
        else:
            print(f"  [WARNING] Channel '{channel}' not found in description")
        
        if niche_found and channel_found:
            print(f"  [PASS] DescriptionGenerator works with niche '{niche}' and channel '{channel}'")
        else:
            print(f"  [PARTIAL] Some elements missing")
        
        return niche_found and channel_found
        
    except Exception as e:
        print(f"  [FAIL] Error testing DescriptionGenerator: {e}")
        return False


def test_tag_suggester(niche: str):
    """Test TagSuggester with different niches."""
    print(f"\n{'='*60}")
    print(f"Testing TagSuggester with niche: '{niche}'")
    print(f"{'='*60}")
    
    try:
        client = YouTubeClient()
        suggester = TagSuggester(client)
        
        result = suggester.suggest_tags(
            video_title=TEST_TITLE,
            song_name=TEST_SONG_NAME,
            max_tags=10,
            niche=niche
        )
        
        tags = result["suggested_tags"]
        niche_words = niche.lower().split()
        
        # Check if niche appears in tags
        niche_found = False
        for tag in tags:
            tag_lower = tag.lower()
            if any(word in tag_lower for word in niche_words if len(word) > 3):
                niche_found = True
                print(f"  [OK] Niche found in tag: '{tag}'")
                break
        
        if not niche_found:
            print(f"  [WARNING] Niche '{niche}' not found in tags")
            print(f"  Tags: {tags[:5]}")
        else:
            print(f"  [PASS] TagSuggester works with niche '{niche}'")
        
        return niche_found
        
    except Exception as e:
        print(f"  [FAIL] Error testing TagSuggester: {e}")
        return False


def test_viral_predictor(niche: str):
    """Test ViralPredictor with different niches."""
    print(f"\n{'='*60}")
    print(f"Testing ViralPredictor with niche: '{niche}'")
    print(f"{'='*60}")
    
    try:
        client = YouTubeClient()
        channel_analyzer = ChannelAnalyzer(client)
        keyword_researcher = KeywordResearcher(client)
        predictor = ViralPredictor(client, channel_analyzer, keyword_researcher)
        
        prediction = predictor.predict_viral_potential(
            title=TEST_TITLE,
            description=TEST_DESCRIPTION,
            tags=TEST_TAGS,
            song_name=TEST_SONG_NAME,
            niche=niche
        )
        
        # Check if prediction was successful
        if "viral_score" in prediction:
            print(f"  [OK] Viral score calculated: {prediction['viral_score']:.2f}")
            print(f"  [PASS] ViralPredictor works with niche '{niche}'")
            return True
        else:
            print(f"  [FAIL] Viral score not found in prediction")
            return False
        
    except Exception as e:
        print(f"  [FAIL] Error testing ViralPredictor: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_trend_predictor(niche: str):
    """Test TrendPredictor with different niches."""
    print(f"\n{'='*60}")
    print(f"Testing TrendPredictor with niche: '{niche}'")
    print(f"{'='*60}")
    
    try:
        client = YouTubeClient()
        predictor = TrendPredictor(client)
        
        predictions = predictor.predict_trends(
            niche=niche,
            days_ahead=7
        )
        
        # Check if niche is in results
        if predictions.get("niche") == niche:
            print(f"  [OK] Niche correctly stored in results: '{predictions['niche']}'")
            print(f"  [PASS] TrendPredictor works with niche '{niche}'")
            return True
        else:
            print(f"  [WARNING] Niche mismatch. Expected '{niche}', got '{predictions.get('niche')}'")
            return False
        
    except Exception as e:
        print(f"  [FAIL] Error testing TrendPredictor: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("NICHE INTEGRATION TEST SUITE")
    print("="*60)
    print(f"\nTesting {len(TEST_NICHES)} different niches across all modules...")
    
    results = {
        "TitleOptimizer": [],
        "DescriptionGenerator": [],
        "TagSuggester": [],
        "ViralPredictor": [],
        "TrendPredictor": []
    }
    
    # Test each niche
    for niche in TEST_NICHES:
        print(f"\n\n{'#'*60}")
        print(f"# Testing Niche: {niche}")
        print(f"{'#'*60}")
        
        # Test TitleOptimizer
        results["TitleOptimizer"].append(test_title_optimizer(niche))
        
        # Test DescriptionGenerator
        channel = TEST_CHANNELS[0]  # Use first test channel
        results["DescriptionGenerator"].append(test_description_generator(niche, channel))
        
        # Test TagSuggester
        results["TagSuggester"].append(test_tag_suggester(niche))
        
        # Test ViralPredictor
        results["ViralPredictor"].append(test_viral_predictor(niche))
        
        # Test TrendPredictor (may take longer, skip if API issues)
        try:
            results["TrendPredictor"].append(test_trend_predictor(niche))
        except Exception as e:
            print(f"  [WARNING] Skipping TrendPredictor test due to API issue: {e}")
            results["TrendPredictor"].append(False)
    
    # Print summary
    print("\n\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for module_name, module_results in results.items():
        passed = sum(module_results)
        total = len(module_results)
        percentage = (passed / total * 100) if total > 0 else 0
        
        status = "[PASS]" if passed == total else "[PARTIAL]" if passed > 0 else "[FAIL]"
        print(f"\n{module_name}:")
        print(f"  {status}: {passed}/{total} tests passed ({percentage:.1f}%)")
    
    # Overall result
    total_passed = sum(sum(r) for r in results.values())
    total_tests = sum(len(r) for r in results.values())
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"OVERALL: {total_passed}/{total_tests} tests passed ({overall_percentage:.1f}%)")
    print(f"{'='*60}")
    
    if total_passed == total_tests:
        print("\n[SUCCESS] ALL TESTS PASSED! All modules work correctly with different niches.")
    elif total_passed > 0:
        print("\n[WARNING] SOME TESTS FAILED. Check warnings above.")
    else:
        print("\n[ERROR] ALL TESTS FAILED. Check errors above.")


if __name__ == "__main__":
    main()

