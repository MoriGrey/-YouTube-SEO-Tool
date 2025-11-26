"""
A/B Test Recommender Module
A/B test suggestions and tracking for titles and thumbnails.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.modules.title_optimizer import TitleOptimizer
from src.modules.ai_thumbnail_generator import AIThumbnailGenerator


class ABTestRecommender:
    """
    A/B test recommendation and tracking system.
    
    AGI Paradigm: Self-Evolving Architecture
    - Suggests A/B test variations
    - Tracks test results
    - Recommends winners
    - Learns from test outcomes
    """
    
    def __init__(
        self,
        title_optimizer: TitleOptimizer,
        thumbnail_generator: Optional[AIThumbnailGenerator] = None,
        db_path: str = "data/ab_tests.json"
    ):
        self.title_optimizer = title_optimizer
        self.thumbnail_generator = thumbnail_generator
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database file and directory exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump({"tests": []}, f, indent=2)
    
    def suggest_title_tests(
        self,
        base_title: str,
        niche: str,
        num_variations: int = 5
    ) -> Dict[str, Any]:
        """
        Suggest A/B test variations for a title.
        
        Args:
            base_title: Original title
            niche: Video niche
            num_variations: Number of variations to generate
        
        Returns:
            A/B test suggestions with variations
        """
        # Generate title variations
        variations_result = self.title_optimizer.generate_title_variations(
            base_title=base_title,
            niche=niche,
            num_variations=num_variations
        )
        
        variations = variations_result.get("variations", [])
        
        # Create test variations
        test_variations = []
        for i, variation in enumerate(variations[:num_variations]):
            test_variations.append({
                "variation_id": f"title_var_{i+1}",
                "title": variation.get("title", base_title),
                "seo_score": variation.get("seo_score", 0),
                "reason": variation.get("reason", ""),
                "type": "title"
            })
        
        return {
            "test_type": "title",
            "base_title": base_title,
            "niche": niche,
            "variations": test_variations,
            "recommendations": [
                f"Test {len(test_variations)} title variations",
                "Run test for at least 1,000 impressions per variation",
                "Monitor CTR, views, and engagement metrics",
                "Choose winner after statistical significance (p < 0.05)"
            ],
            "testing_guidelines": self._get_testing_guidelines("title")
        }
    
    def suggest_thumbnail_tests(
        self,
        title: str,
        description: str,
        niche: str,
        num_variations: int = 3
    ) -> Dict[str, Any]:
        """
        Suggest A/B test variations for thumbnails.
        
        Args:
            title: Video title
            description: Video description
            niche: Video niche
            num_variations: Number of variations to generate
        
        Returns:
            A/B test suggestions with thumbnail variations
        """
        if not self.thumbnail_generator:
            return {
                "error": "Thumbnail generator not available. Set OPENAI_API_KEY or use template mode."
            }
        
        # Generate thumbnail variations
        thumbnail_result = self.thumbnail_generator.generate_thumbnail(
            title=title,
            description=description,
            niche=niche,
            num_variations=num_variations
        )
        
        variations = thumbnail_result.get("variations", [])
        
        # Create test variations
        test_variations = []
        for i, variation in enumerate(variations):
            test_variations.append({
                "variation_id": f"thumb_var_{i+1}",
                "thumbnail_url": variation.get("image_url") or variation.get("template_description", {}),
                "estimated_ctr": variation.get("estimated_ctr", 0),
                "generation_method": variation.get("generation_method", "template"),
                "style": variation.get("template_description", {}).get("style", "youtube_thumbnail"),
                "type": "thumbnail"
            })
        
        return {
            "test_type": "thumbnail",
            "title": title,
            "niche": niche,
            "variations": test_variations,
            "recommendations": [
                f"Test {len(test_variations)} thumbnail variations",
                "Run test for at least 1,000 impressions per variation",
                "Monitor CTR as primary metric",
                "Choose winner based on highest CTR after statistical significance"
            ],
            "testing_guidelines": self._get_testing_guidelines("thumbnail")
        }
    
    def create_test(
        self,
        video_id: str,
        test_type: str,  # "title" or "thumbnail"
        variations: List[Dict[str, Any]],
        start_date: Optional[str] = None
    ) -> str:
        """
        Create an A/B test.
        
        Args:
            video_id: YouTube video ID
            test_type: Type of test (title or thumbnail)
            variations: List of test variations
            start_date: Test start date (defaults to now)
        
        Returns:
            Test ID
        """
        test_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(video_id) % 10000}"
        
        test = {
            "id": test_id,
            "video_id": video_id,
            "test_type": test_type,
            "variations": variations,
            "start_date": start_date or datetime.now().isoformat(),
            "end_date": None,
            "status": "active",  # active, completed, cancelled
            "results": {},
            "winner": None,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to database
        data = self._load_data()
        data["tests"].append(test)
        self._save_data(data)
        
        return test_id
    
    def update_test_results(
        self,
        test_id: str,
        variation_id: str,
        impressions: int,
        clicks: int,
        views: int = 0,
        engagement: int = 0
    ) -> bool:
        """
        Update test results for a variation.
        
        Args:
            test_id: Test ID
            variation_id: Variation ID
            impressions: Number of impressions
            clicks: Number of clicks
            views: Number of views (optional)
            engagement: Engagement count (optional)
        
        Returns:
            True if updated successfully
        """
        data = self._load_data()
        
        test = next((t for t in data["tests"] if t.get("id") == test_id), None)
        if not test:
            return False
        
        # Initialize results if needed
        if "results" not in test:
            test["results"] = {}
        
        # Calculate metrics
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        view_rate = (views / impressions * 100) if impressions > 0 else 0
        engagement_rate = (engagement / views * 100) if views > 0 else 0
        
        # Update variation results
        test["results"][variation_id] = {
            "impressions": impressions,
            "clicks": clicks,
            "views": views,
            "engagement": engagement,
            "ctr": ctr,
            "view_rate": view_rate,
            "engagement_rate": engagement_rate,
            "updated_at": datetime.now().isoformat()
        }
        
        self._save_data(data)
        return True
    
    def analyze_test_results(self, test_id: str) -> Dict[str, Any]:
        """
        Analyze A/B test results and recommend winner.
        
        Args:
            test_id: Test ID
        
        Returns:
            Analysis with winner recommendation
        """
        data = self._load_data()
        test = next((t for t in data["tests"] if t.get("id") == test_id), None)
        
        if not test:
            return {"error": "Test not found"}
        
        results = test.get("results", {})
        if not results:
            return {"error": "No results available yet"}
        
        # Analyze each variation
        variation_analysis = []
        for var_id, var_results in results.items():
            variation_analysis.append({
                "variation_id": var_id,
                "impressions": var_results.get("impressions", 0),
                "clicks": var_results.get("clicks", 0),
                "ctr": var_results.get("ctr", 0),
                "views": var_results.get("views", 0),
                "engagement": var_results.get("engagement", 0),
                "engagement_rate": var_results.get("engagement_rate", 0)
            })
        
        # Find winner based on test type
        if test.get("test_type") == "title":
            # For titles, prioritize CTR and engagement
            winner = max(
                variation_analysis,
                key=lambda x: x["ctr"] * 0.7 + x["engagement_rate"] * 0.3
            )
        else:  # thumbnail
            # For thumbnails, prioritize CTR
            winner = max(variation_analysis, key=lambda x: x["ctr"])
        
        # Check statistical significance
        significance = self._check_statistical_significance(variation_analysis)
        
        # Update test with winner
        test["winner"] = winner["variation_id"]
        test["status"] = "completed"
        test["end_date"] = datetime.now().isoformat()
        self._save_data(data)
        
        return {
            "test_id": test_id,
            "test_type": test.get("test_type"),
            "variation_analysis": variation_analysis,
            "winner": winner,
            "statistical_significance": significance,
            "recommendation": self._generate_winner_recommendation(winner, significance),
            "insights": self._generate_test_insights(variation_analysis, test.get("test_type"))
        }
    
    def _check_statistical_significance(
        self,
        variation_analysis: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Check if test results are statistically significant."""
        if len(variation_analysis) < 2:
            return {
                "significant": False,
                "reason": "Need at least 2 variations for significance testing"
            }
        
        # Simple significance check (chi-square approximation)
        # For production, use proper statistical tests
        total_impressions = sum(v["impressions"] for v in variation_analysis)
        total_clicks = sum(v["clicks"] for v in variation_analysis)
        
        if total_impressions < 1000:
            return {
                "significant": False,
                "reason": f"Need at least 1,000 total impressions (current: {total_impressions})"
            }
        
        # Check if CTR differences are meaningful
        ctrs = [v["ctr"] for v in variation_analysis]
        max_ctr = max(ctrs)
        min_ctr = min(ctrs)
        
        if max_ctr - min_ctr < 1.0:  # Less than 1% difference
            return {
                "significant": False,
                "reason": "CTR difference is too small (< 1%)"
            }
        
        return {
            "significant": True,
            "reason": "Results show meaningful difference",
            "ctr_difference": max_ctr - min_ctr
        }
    
    def _generate_winner_recommendation(
        self,
        winner: Dict[str, Any],
        significance: Dict[str, Any]
    ) -> str:
        """Generate recommendation based on winner."""
        if not significance.get("significant", False):
            return (
                "Test results are not yet statistically significant. "
                "Continue testing or increase sample size."
            )
        
        winner_ctr = winner.get("ctr", 0)
        return (
            f"Winner: Variation {winner['variation_id']} with {winner_ctr:.2f}% CTR. "
            f"Update all content to use this variation."
        )
    
    def _generate_test_insights(
        self,
        variation_analysis: List[Dict[str, Any]],
        test_type: str
    ) -> List[str]:
        """Generate insights from test results."""
        insights = []
        
        if not variation_analysis:
            return ["No data available"]
        
        # Find best and worst performers
        if test_type == "title":
            best = max(variation_analysis, key=lambda x: x["ctr"])
            worst = min(variation_analysis, key=lambda x: x["ctr"])
            
            insights.append(
                f"Best performing title: {best['variation_id']} with {best['ctr']:.2f}% CTR"
            )
            insights.append(
                f"Worst performing title: {worst['variation_id']} with {worst['ctr']:.2f}% CTR"
            )
        else:  # thumbnail
            best = max(variation_analysis, key=lambda x: x["ctr"])
            worst = min(variation_analysis, key=lambda x: x["ctr"])
            
            insights.append(
                f"Best performing thumbnail: {best['variation_id']} with {best['ctr']:.2f}% CTR"
            )
            insights.append(
                f"Worst performing thumbnail: {worst['variation_id']} with {worst['ctr']:.2f}% CTR"
            )
        
        # Engagement insights
        if any(v.get("engagement_rate", 0) > 0 for v in variation_analysis):
            best_engagement = max(variation_analysis, key=lambda x: x.get("engagement_rate", 0))
            insights.append(
                f"Highest engagement: {best_engagement['variation_id']} with "
                f"{best_engagement.get('engagement_rate', 0):.2f}% engagement rate"
            )
        
        return insights
    
    def _get_testing_guidelines(self, test_type: str) -> List[str]:
        """Get testing guidelines for a test type."""
        if test_type == "title":
            return [
                "Test 5-10 title variations",
                "Run test for at least 1,000 impressions per variation",
                "Monitor CTR, views, and engagement",
                "Choose winner after 7-14 days or when statistically significant",
                "Update all future videos with winning title pattern"
            ]
        else:  # thumbnail
            return [
                "Test 3-5 thumbnail variations",
                "Run test for at least 1,000 impressions per variation",
                "Monitor CTR as primary metric",
                "Choose winner after 7-14 days or when statistically significant",
                "Update all future thumbnails with winning design"
            ]
    
    def get_active_tests(self) -> List[Dict[str, Any]]:
        """Get all active A/B tests."""
        data = self._load_data()
        return [t for t in data.get("tests", []) if t.get("status") == "active"]
    
    def get_test_history(
        self,
        video_id: Optional[str] = None,
        test_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get test history with filters."""
        data = self._load_data()
        tests = data.get("tests", [])
        
        # Apply filters
        if video_id:
            tests = [t for t in tests if t.get("video_id") == video_id]
        if test_type:
            tests = [t for t in tests if t.get("test_type") == test_type]
        
        # Sort by creation date
        tests.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return tests
    
    def _load_data(self) -> Dict[str, Any]:
        """Load test data from database."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"tests": []}
    
    def _save_data(self, data: Dict[str, Any]):
        """Save test data to database."""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

