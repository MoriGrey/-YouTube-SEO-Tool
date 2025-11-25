"""
Viral Content Predictor Module
Predicts viral potential of content before publishing.

AGI Paradigm: Viral Content Predictor
- Predicts viral potential before publishing
- Learns from successful viral content patterns
- Identifies viral-worthy content opportunities
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.channel_analyzer import ChannelAnalyzer
from src.modules.keyword_researcher import KeywordResearcher


class ViralPredictor:
    """
    Predicts viral potential of content.
    
    AGI Paradigm: Viral Content Predictor
    - Analyzes content for viral indicators
    - Learns from past viral content
    - Predicts viral potential with confidence scores
    """
    
    DATA_FILE = "data/viral_predictions.json"
    
    # Viral indicators and their weights
    VIRAL_INDICATORS = {
        "trending_keywords": 0.25,
        "emotional_appeal": 0.20,
        "uniqueness": 0.15,
        "timing": 0.15,
        "thumbnail_potential": 0.10,
        "title_clickability": 0.10,
        "shareability": 0.05
    }
    
    def __init__(
        self,
        client: YouTubeClient,
        channel_analyzer: ChannelAnalyzer,
        keyword_researcher: KeywordResearcher
    ):
        self.client = client
        self.channel_analyzer = channel_analyzer
        self.keyword_researcher = keyword_researcher
        self._ensure_data_dir()
        self._load_predictions()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
    
    def _load_predictions(self) -> Dict[str, Any]:
        """Load prediction history."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "predictions": [],
            "viral_content_patterns": {},
            "accuracy_tracking": {}
        }
    
    def _save_predictions(self, data: Dict[str, Any]):
        """Save prediction history."""
        try:
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving predictions: {e}")
    
    def predict_viral_potential(
        self,
        title: str,
        description: str,
        tags: List[str],
        song_name: Optional[str] = None,
        niche: str = "psychedelic anatolian rock"
    ) -> Dict[str, Any]:
        """
        Predict viral potential of content.
        
        Args:
            title: Video title
            description: Video description
            tags: Video tags
            song_name: Optional song name
            niche: Content niche
            
        Returns:
            Viral potential prediction with score and reasons
        """
        # Analyze various viral indicators
        indicators = {
            "trending_keywords": self._analyze_trending_keywords(title, description, tags, niche),
            "emotional_appeal": self._analyze_emotional_appeal(title, description),
            "uniqueness": self._analyze_uniqueness(title, description, niche),
            "timing": self._analyze_timing(),
            "thumbnail_potential": self._analyze_thumbnail_potential(title),
            "title_clickability": self._analyze_title_clickability(title),
            "shareability": self._analyze_shareability(title, description)
        }
        
        # Calculate viral score
        viral_score = sum(
            indicators[key] * self.VIRAL_INDICATORS[key]
            for key in self.VIRAL_INDICATORS
        )
        
        # Determine viral potential level
        if viral_score >= 0.8:
            potential_level = "very_high"
            recommendation = "High viral potential! Publish soon and promote actively."
        elif viral_score >= 0.65:
            potential_level = "high"
            recommendation = "Good viral potential. Optimize and publish."
        elif viral_score >= 0.50:
            potential_level = "medium"
            recommendation = "Moderate viral potential. Consider improvements."
        elif viral_score >= 0.35:
            potential_level = "low"
            recommendation = "Low viral potential. Significant improvements needed."
        else:
            potential_level = "very_low"
            recommendation = "Very low viral potential. Major changes required."
        
        # Generate improvement suggestions
        improvements = self._generate_improvements(indicators, viral_score)
        
        prediction = {
            "timestamp": datetime.now().isoformat(),
            "content": {
                "title": title,
                "description": description[:200] + "..." if len(description) > 200 else description,
                "tags": tags,
                "song_name": song_name
            },
            "viral_score": viral_score,
            "potential_level": potential_level,
            "indicators": indicators,
            "recommendation": recommendation,
            "improvements": improvements,
            "confidence": self._calculate_confidence(indicators)
        }
        
        # Save prediction
        predictions = self._load_predictions()
        predictions["predictions"].append(prediction)
        if len(predictions["predictions"]) > 100:
            predictions["predictions"] = predictions["predictions"][-100:]
        self._save_predictions(predictions)
        
        return prediction
    
    def _analyze_trending_keywords(
        self,
        title: str,
        description: str,
        tags: List[str],
        niche: str
    ) -> float:
        """Analyze if content uses trending keywords."""
        score = 0.0
        
        # Check for trending keywords in niche
        all_text = f"{title} {description} {' '.join(tags)}".lower()
        
        # Generate trending keywords from niche
        niche_words = niche.lower().split()
        trending_keywords = niche_words.copy()
        
        # Add common trending words that work across niches
        common_trending = ["cover", "mix", "remix", "new", "latest", "2024", "2025", "viral", "trending"]
        trending_keywords.extend(common_trending)
        
        # If niche is too short, add some fallback keywords
        if len(trending_keywords) < 5:
            trending_keywords.extend(["music", "song", "video", "audio"])
        
        found_trending = sum(1 for keyword in trending_keywords if keyword in all_text)
        score = min(found_trending / max(len(trending_keywords), 1), 1.0) * 0.8
        
        # Check for numbers/years (often viral)
        if any(char.isdigit() for char in title):
            score += 0.1
        
        # Check for emotional/action words
        emotional_words = ["best", "amazing", "incredible", "epic", "legendary", "classic"]
        if any(word in all_text for word in emotional_words):
            score += 0.1
        
        return min(score, 1.0)
    
    def _analyze_emotional_appeal(self, title: str, description: str) -> float:
        """Analyze emotional appeal of content."""
        score = 0.5  # Base score
        
        text = f"{title} {description}".lower()
        
        # Positive emotional words
        positive_words = [
            "love", "amazing", "beautiful", "incredible", "epic", "legendary",
            "nostalgic", "memories", "classic", "timeless"
        ]
        positive_count = sum(1 for word in positive_words if word in text)
        score += min(positive_count * 0.1, 0.3)
        
        # Question words (engagement)
        if any(word in title.lower() for word in ["what", "why", "how", "when", "where"]):
            score += 0.1
        
        # Exclamation marks (excitement)
        if "!" in title:
            score += 0.1
        
        return min(score, 1.0)
    
    def _analyze_uniqueness(
        self,
        title: str,
        description: str,
        niche: str
    ) -> float:
        """Analyze uniqueness of content."""
        score = 0.6  # Base score
        
        # Check for unique elements
        unique_indicators = [
            "ai", "artificial intelligence", "first", "never before",
            "exclusive", "rare", "unique", "original"
        ]
        
        text = f"{title} {description}".lower()
        unique_count = sum(1 for indicator in unique_indicators if indicator in text)
        score += min(unique_count * 0.15, 0.4)
        
        return min(score, 1.0)
    
    def _analyze_timing(self) -> float:
        """Analyze if timing is optimal for viral content."""
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()  # 0=Monday, 6=Sunday
        
        score = 0.5  # Base score
        
        # Best hours: 19-21 (7-9 PM)
        if 19 <= hour <= 21:
            score += 0.3
        elif 17 <= hour <= 22:
            score += 0.2
        
        # Best days: Thursday-Saturday
        if 3 <= day_of_week <= 5:
            score += 0.2
        
        return min(score, 1.0)
    
    def _analyze_thumbnail_potential(self, title: str) -> float:
        """Analyze thumbnail potential based on title."""
        score = 0.5  # Base score
        
        # Titles that suggest visual appeal
        visual_keywords = [
            "cover", "performance", "live", "studio", "behind the scenes",
            "making of", "process", "creation"
        ]
        
        if any(keyword in title.lower() for keyword in visual_keywords):
            score += 0.3
        
        # Numbers in title (good for thumbnails)
        if any(char.isdigit() for char in title):
            score += 0.2
        
        return min(score, 1.0)
    
    def _analyze_title_clickability(self, title: str) -> float:
        """Analyze how clickable the title is."""
        score = 0.5  # Base score
        
        # Optimal length: 40-60 characters
        length = len(title)
        if 40 <= length <= 60:
            score += 0.3
        elif 30 <= length <= 70:
            score += 0.15
        
        # Power words
        power_words = [
            "ultimate", "complete", "best", "top", "secret", "hidden",
            "revealed", "exposed", "shocking", "amazing"
        ]
        if any(word in title.lower() for word in power_words):
            score += 0.2
        
        return min(score, 1.0)
    
    def _analyze_shareability(self, title: str, description: str) -> float:
        """Analyze how shareable the content is."""
        score = 0.5  # Base score
        
        text = f"{title} {description}".lower()
        
        # Shareable content indicators
        shareable_keywords = [
            "must see", "you need to", "check this out", "share",
            "viral", "trending", "popular"
        ]
        if any(keyword in text for keyword in shareable_keywords):
            score += 0.3
        
        # Hashtags in description
        if "#" in description:
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_confidence(self, indicators: Dict[str, float]) -> float:
        """Calculate confidence in prediction."""
        # Higher confidence if indicators are consistent
        values = list(indicators.values())
        variance = sum((v - sum(values)/len(values))**2 for v in values) / len(values)
        consistency = 1.0 - min(variance, 1.0)
        
        # More data = higher confidence
        predictions = self._load_predictions()
        data_points = len(predictions.get("predictions", []))
        data_confidence = min(data_points / 50, 1.0) * 0.3
        
        return min(consistency * 0.7 + data_confidence, 1.0)
    
    def _generate_improvements(
        self,
        indicators: Dict[str, float],
        viral_score: float
    ) -> List[str]:
        """Generate improvement suggestions."""
        improvements = []
        
        if indicators["trending_keywords"] < 0.5:
            improvements.append("Add more trending keywords to title and description")
        
        if indicators["emotional_appeal"] < 0.5:
            improvements.append("Increase emotional appeal with compelling language")
        
        if indicators["title_clickability"] < 0.6:
            improvements.append("Optimize title length and add power words")
        
        if indicators["timing"] < 0.6:
            improvements.append("Consider publishing during peak hours (7-9 PM)")
        
        if viral_score < 0.5:
            improvements.append("Major improvements needed across multiple areas")
        
        return improvements
    
    def learn_from_viral_content(self, video_id: str) -> Dict[str, Any]:
        """
        Learn patterns from a viral video.
        
        Args:
            video_id: ID of viral video to analyze
            
        Returns:
            Learned patterns
        """
        try:
            videos = self.client.get_videos_details([video_id])
            if not videos:
                return {"status": "not_found", "message": "Video not found"}
            
            video = videos[0]
            snippet = video["snippet"]
            stats = video["statistics"]
            
            views = int(stats.get("viewCount", 0))
            
            # Consider viral if views > 100K
            if views < 100000:
                return {
                    "status": "not_viral",
                    "message": f"Video has {views:,} views, not considered viral (threshold: 100K)"
                }
            
            # Extract patterns
            title = snippet["title"]
            description = snippet.get("description", "")
            tags = snippet.get("tags", [])
            
            patterns = {
                "title_length": len(title),
                "title_has_numbers": any(c.isdigit() for c in title),
                "title_has_emotional_words": any(
                    word in title.lower() for word in 
                    ["amazing", "incredible", "epic", "best", "ultimate"]
                ),
                "description_length": len(description),
                "tag_count": len(tags),
                "published_at": snippet.get("publishedAt", ""),
                "views": views,
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0))
            }
            
            # Save pattern
            predictions = self._load_predictions()
            if "viral_content_patterns" not in predictions:
                predictions["viral_content_patterns"] = []
            
            predictions["viral_content_patterns"].append({
                "video_id": video_id,
                "patterns": patterns,
                "learned_at": datetime.now().isoformat()
            })
            
            # Keep only last 50 patterns
            if len(predictions["viral_content_patterns"]) > 50:
                predictions["viral_content_patterns"] = predictions["viral_content_patterns"][-50:]
            
            self._save_predictions(predictions)
            
            return {
                "status": "learned",
                "patterns": patterns,
                "insights": self._extract_viral_insights(patterns)
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _extract_viral_insights(self, patterns: Dict[str, Any]) -> List[str]:
        """Extract insights from viral patterns."""
        insights = []
        
        title_len = patterns.get("title_length", 0)
        if 40 <= title_len <= 60:
            insights.append(f"Optimal title length: {title_len} characters")
        
        if patterns.get("title_has_numbers"):
            insights.append("Numbers in title can increase click-through rate")
        
        if patterns.get("title_has_emotional_words"):
            insights.append("Emotional words in title enhance appeal")
        
        tag_count = patterns.get("tag_count", 0)
        if 15 <= tag_count <= 30:
            insights.append(f"Good tag count: {tag_count} tags")
        
        return insights

