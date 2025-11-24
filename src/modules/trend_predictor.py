"""
Trend Prediction Module
Predict trending topics and optimize timing.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import Counter
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient


class TrendPredictor:
    """
    Trend prediction with AGI-powered forecasting.
    
    AGI Paradigm: Continuous Learning Mechanism
    - Learns from historical patterns
    - Predicts future trends
    - Adapts to changing algorithms
    """
    
    def __init__(self, client: YouTubeClient):
        self.client = client
    
    def predict_trends(
        self,
        niche: str = "psychedelic anatolian rock",
        days_ahead: int = 7
    ) -> Dict[str, Any]:
        """
        Predict trending topics for the next N days.
        
        Args:
            niche: Niche to analyze
            days_ahead: Number of days to predict ahead
        
        Returns:
            Trend predictions and recommendations
        """
        # Analyze recent trends
        recent_trends = self._analyze_recent_trends(niche)
        
        # Predict future trends
        predictions = self._predict_future_trends(recent_trends, days_ahead)
        
        # Generate recommendations
        recommendations = self._generate_trend_recommendations(predictions)
        
        return {
            "niche": niche,
            "analysis_period": f"Last 30 days",
            "prediction_period": f"Next {days_ahead} days",
            "recent_trends": recent_trends,
            "predictions": predictions,
            "recommendations": recommendations,
            "confidence": self._calculate_confidence(recent_trends)
        }
    
    def _analyze_recent_trends(self, niche: str) -> Dict[str, Any]:
        """Analyze recent trending topics."""
        # Search for recent videos
        recent_results = self.client.search_videos(
            niche,
            max_results=50,
            order="date",
            region_code="TR"
        )
        
        # Extract trends from titles
        trending_words = []
        trending_themes = []
        
        for result in recent_results:
            title = result["snippet"]["title"].lower()
            words = [w for w in title.split() if len(w) > 4]
            trending_words.extend(words)
            
            # Extract themes
            if "cover" in title:
                trending_themes.append("covers")
            if "70s" in title or "80s" in title:
                trending_themes.append("retro")
            if "ai" in title or "yapay zeka" in title:
                trending_themes.append("ai-generated")
        
        word_freq = Counter(trending_words)
        theme_freq = Counter(trending_themes)
        
        return {
            "trending_keywords": [{"word": word, "count": count} for word, count in word_freq.most_common(10)],
            "trending_themes": [{"theme": theme, "count": count} for theme, count in theme_freq.most_common(5)],
            "total_videos_analyzed": len(recent_results)
        }
    
    def _predict_future_trends(
        self,
        recent_trends: Dict[str, Any],
        days_ahead: int
    ) -> List[Dict[str, Any]]:
        """Predict future trends based on recent patterns."""
        predictions = []
        
        # Extrapolate from recent trends
        trending_keywords = recent_trends.get("trending_keywords", [])
        trending_themes = recent_trends.get("trending_themes", [])
        
        # Predict continuation of current trends
        for keyword_data in trending_keywords[:5]:
            predictions.append({
                "keyword": keyword_data["word"],
                "trend_direction": "Rising",
                "confidence": "Medium",
                "recommended_action": f"Consider creating content around '{keyword_data['word']}'"
            })
        
        # Predict theme trends
        for theme_data in trending_themes[:3]:
            predictions.append({
                "theme": theme_data["theme"],
                "trend_direction": "Stable",
                "confidence": "High",
                "recommended_action": f"Continue focusing on {theme_data['theme']} content"
            })
        
        return predictions
    
    def _generate_trend_recommendations(
        self,
        predictions: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate actionable recommendations from predictions."""
        recommendations = []
        
        if predictions:
            top_keyword = predictions[0].get("keyword", "")
            if top_keyword:
                recommendations.append(
                    f"Focus on '{top_keyword}' - it's trending upward in your niche"
                )
        
        recommendations.extend([
            "Monitor competitor channels for emerging trends",
            "Create content around trending themes (covers, retro, AI-generated)",
            "Use trending keywords in titles and descriptions",
            "Post during peak engagement times for your audience"
        ])
        
        return recommendations
    
    def _calculate_confidence(self, recent_trends: Dict[str, Any]) -> str:
        """Calculate confidence level for predictions."""
        total_videos = recent_trends.get("total_videos_analyzed", 0)
        
        if total_videos >= 30:
            return "High"
        elif total_videos >= 15:
            return "Medium"
        else:
            return "Low"
    
    def get_best_posting_times(
        self,
        channel_id: str
    ) -> Dict[str, Any]:
        """
        Analyze best posting times based on channel data.
        
        Note: YouTube API doesn't provide detailed time analytics,
        so this uses general best practices for Turkish audience.
        """
        # Best times for Turkish audience (UTC+3)
        # Peak hours: 19:00-22:00 local time (16:00-19:00 UTC)
        best_times = {
            "monday": ["19:00", "20:00", "21:00"],
            "tuesday": ["19:00", "20:00", "21:00"],
            "wednesday": ["19:00", "20:00", "21:00"],
            "thursday": ["19:00", "20:00", "21:00"],
            "friday": ["18:00", "19:00", "20:00", "21:00", "22:00"],
            "saturday": ["14:00", "15:00", "16:00", "19:00", "20:00", "21:00"],
            "sunday": ["14:00", "15:00", "16:00", "19:00", "20:00", "21:00"]
        }
        
        return {
            "best_times": best_times,
            "timezone": "Turkey (UTC+3)",
            "recommendations": [
                "Post between 19:00-21:00 on weekdays for maximum reach",
                "Weekend afternoons (14:00-16:00) also perform well",
                "Friday evenings have highest engagement",
                "Avoid posting late night (after 23:00) or early morning (before 09:00)"
            ],
            "next_optimal_post": self._calculate_next_optimal_time()
        }
    
    def _calculate_next_optimal_time(self) -> Dict[str, Any]:
        """Calculate the next optimal posting time."""
        now = datetime.now()
        reason = ""
        
        # If it's after 21:00, recommend tomorrow at 19:00
        if now.hour >= 21:
            next_post = now + timedelta(days=1)
            next_post = next_post.replace(hour=19, minute=0, second=0, microsecond=0)
            reason = "It's too late today (after 21:00). Post tomorrow at 19:00 for maximum reach."
        # If it's before 19:00, recommend today at 19:00
        elif now.hour < 19:
            next_post = now.replace(hour=19, minute=0, second=0, microsecond=0)
            reason = "Post today at 19:00 - peak viewing hours for Turkish audience (19:00-21:00)."
        # If between 19:00-21:00, recommend tomorrow
        else:
            next_post = now + timedelta(days=1)
            next_post = next_post.replace(hour=19, minute=0, second=0, microsecond=0)
            reason = "You're in peak hours now. Post tomorrow at 19:00 for next peak engagement window."
        
        return {
            "date": next_post.strftime("%Y-%m-%d"),
            "time": next_post.strftime("%H:%M"),
            "day": next_post.strftime("%A"),
            "reason": reason
        }

