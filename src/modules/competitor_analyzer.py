"""
Competitor Analysis Module
Analyze competitor channels and strategies.
"""

from typing import Dict, Any, List, Optional
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient


class CompetitorAnalyzer:
    """
    Competitor analysis with AGI-powered insights.
    
    AGI Paradigm: Omnipresent Data Mining
    - Discovers competitor strategies
    - Identifies market gaps
    - Provides competitive intelligence
    """
    
    def __init__(self, client: YouTubeClient):
        self.client = client
    
    def find_competitors(
        self,
        niche_keywords: List[str],
        max_competitors: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find competitor channels in the niche.
        
        Args:
            niche_keywords: Keywords to search for competitors
            max_competitors: Maximum number of competitors to find
        
        Returns:
            List of competitor channel information
        """
        competitors = []
        seen_channels = set()
        
        for keyword in niche_keywords:
            # Search for videos
            results = self.client.search_videos(
                keyword,
                max_results=25,
                order="viewCount",
                region_code="TR"
            )
            
            for result in results:
                channel_id = result["snippet"]["channelId"]
                channel_title = result["snippet"]["channelTitle"]
                
                # Skip if already seen
                if channel_id in seen_channels:
                    continue
                
                seen_channels.add(channel_id)
                
                # Get channel details
                try:
                    channel_data = self.client.get_channel_by_id(channel_id)
                    if channel_data.get("items"):
                        channel = channel_data["items"][0]
                        stats = channel["statistics"]
                        snippet = channel["snippet"]
                        
                        # Get channel handle (customUrl) if available
                        channel_handle = snippet.get("customUrl", "")
                        if channel_handle:
                            channel_handle = channel_handle.lstrip("@")
                        
                        # Calculate relevance score based on subscribers (simple heuristic)
                        subscribers = int(stats.get("subscriberCount", 0))
                        relevance_score = min(subscribers / 1000000, 1.0) if subscribers > 0 else 0.0
                        
                        competitors.append({
                            "channel_id": channel_id,
                            "channel_title": channel_title,  # Keep for backward compatibility
                            "title": channel_title,  # Also add as title
                            "channel_handle": channel_handle or channel_id[:20],  # Use handle or first 20 chars of ID
                            "subscribers": subscribers,
                            "total_views": int(stats.get("viewCount", 0)),
                            "video_count": int(stats.get("videoCount", 0)),
                            "description": snippet.get("description", "")[:200],
                            "relevance_score": relevance_score
                        })
                        
                        if len(competitors) >= max_competitors:
                            break
                except Exception:
                    continue
            
            if len(competitors) >= max_competitors:
                break
        
        # Sort by subscribers
        competitors.sort(key=lambda x: x["subscribers"], reverse=True)
        return competitors
    
    def analyze_competitor(
        self,
        channel_id: str,
        max_videos: int = 20
    ) -> Dict[str, Any]:
        """
        Analyze a specific competitor channel.
        
        Returns:
            Detailed competitor analysis
        """
        # Get channel info
        channel_data = self.client.get_channel_by_id(channel_id)
        if not channel_data.get("items"):
            raise ValueError(f"Channel {channel_id} not found")
        
        channel = channel_data["items"][0]
        stats = channel["statistics"]
        
        # Get videos
        videos = self.client.get_channel_videos(channel_id, max_results=max_videos)
        
        # Analyze video performance
        if videos:
            views = [int(v.get("statistics", {}).get("viewCount", 0)) for v in videos]
            likes = [int(v.get("statistics", {}).get("likeCount", 0)) for v in videos]
            
            avg_views = sum(views) / len(views) if views else 0
            avg_likes = sum(likes) / len(likes) if likes else 0
            
            # Analyze titles
            titles = [v["snippet"]["title"] for v in videos]
            title_patterns = self._analyze_title_patterns(titles)
            
            # Analyze upload frequency
            upload_frequency = self._analyze_upload_frequency(videos)
        else:
            avg_views = 0
            avg_likes = 0
            title_patterns = {}
            upload_frequency = {}
        
        return {
            "channel_info": {
                "id": channel_id,
                "title": channel["snippet"]["title"],
                "subscribers": int(stats.get("subscriberCount", 0)),
                "total_views": int(stats.get("viewCount", 0)),
                "video_count": int(stats.get("videoCount", 0))
            },
            "performance": {
                "average_views": avg_views,
                "average_likes": avg_likes,
                "engagement_rate": (avg_likes / max(avg_views, 1)) * 100 if avg_views > 0 else 0
            },
            "content_strategy": {
                "title_patterns": title_patterns,
                "upload_frequency": upload_frequency
            },
            "strengths": self._identify_strengths(avg_views, avg_likes, upload_frequency),
            "opportunities": self._identify_opportunities(title_patterns, upload_frequency)
        }
    
    def _analyze_title_patterns(self, titles: List[str]) -> Dict[str, Any]:
        """Analyze title patterns used by competitor."""
        if not titles:
            return {}
        
        # Common patterns
        has_pipe = sum(1 for t in "|" in t for t in titles)
        has_brackets = sum(1 for t in "[" in t or "]" in t for t in titles)
        has_numbers = sum(1 for t in any(c.isdigit() for c in t) for t in titles)
        
        # Average length
        avg_length = sum(len(t) for t in titles) / len(titles) if titles else 0
        
        # Common words
        from collections import Counter
        all_words = []
        for title in titles:
            words = title.lower().split()
            all_words.extend([w for w in words if len(w) > 3])
        
        common_words = Counter(all_words).most_common(10)
        
        return {
            "average_length": avg_length,
            "uses_pipe_separator": has_pipe > len(titles) * 0.5,
            "uses_brackets": has_brackets > len(titles) * 0.3,
            "uses_numbers": has_numbers > len(titles) * 0.3,
            "common_words": [{"word": word, "count": count} for word, count in common_words]
        }
    
    def _analyze_upload_frequency(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze upload frequency."""
        if not videos:
            return {}
        
        from datetime import datetime
        
        dates = []
        for video in videos:
            pub_date = video["snippet"].get("publishedAt", "")
            if pub_date:
                try:
                    dates.append(datetime.fromisoformat(pub_date.replace("Z", "+00:00")))
                except:
                    pass
        
        if len(dates) < 2:
            return {"frequency": "Unknown", "days_between": 0}
        
        dates.sort()
        days_between = []
        for i in range(1, len(dates)):
            days_between.append((dates[i] - dates[i-1]).days)
        
        avg_days = sum(days_between) / len(days_between) if days_between else 0
        
        if avg_days < 7:
            frequency = "Very Active (multiple per week)"
        elif avg_days < 14:
            frequency = "Active (weekly)"
        elif avg_days < 30:
            frequency = "Moderate (bi-weekly)"
        else:
            frequency = "Infrequent (monthly or less)"
        
        return {
            "frequency": frequency,
            "average_days_between": avg_days,
            "videos_analyzed": len(videos)
        }
    
    def _identify_strengths(
        self,
        avg_views: float,
        avg_likes: float,
        upload_frequency: Dict[str, Any]
    ) -> List[str]:
        """Identify competitor strengths."""
        strengths = []
        
        if avg_views > 10000:
            strengths.append("High view counts indicate strong content quality or marketing")
        
        if avg_likes / max(avg_views, 1) > 0.02:
            strengths.append("High engagement rate suggests loyal audience")
        
        freq = upload_frequency.get("frequency", "")
        if "Very Active" in freq or "Active" in freq:
            strengths.append("Consistent upload schedule builds audience retention")
        
        return strengths
    
    def _identify_opportunities(
        self,
        title_patterns: Dict[str, Any],
        upload_frequency: Dict[str, Any]
    ) -> List[str]:
        """Identify opportunities based on competitor analysis."""
        opportunities = []
        
        # Title opportunities
        if title_patterns.get("uses_pipe_separator"):
            opportunities.append("Consider using pipe separator (|) in titles for better organization")
        
        if title_patterns.get("average_length", 0) > 50:
            opportunities.append("Competitors use longer titles - test longer, more descriptive titles")
        
        # Upload frequency opportunities
        freq = upload_frequency.get("frequency", "")
        if "Infrequent" in freq:
            opportunities.append("Competitor uploads infrequently - you can gain advantage with consistent uploads")
        
        return opportunities
    
    def compare_with_competitors(
        self,
        your_channel_id: str,
        competitor_ids: List[str]
    ) -> Dict[str, Any]:
        """Compare your channel with competitors."""
        your_analysis = self.analyze_competitor(your_channel_id)
        competitor_analyses = [self.analyze_competitor(cid) for cid in competitor_ids]
        
        # Calculate averages
        avg_subscribers = sum(c["channel_info"]["subscribers"] for c in competitor_analyses) / len(competitor_analyses) if competitor_analyses else 0
        avg_views = sum(c["performance"]["average_views"] for c in competitor_analyses) / len(competitor_analyses) if competitor_analyses else 0
        
        your_subs = your_analysis["channel_info"]["subscribers"]
        your_views = your_analysis["performance"]["average_views"]
        
        return {
            "your_channel": {
                "subscribers": your_subs,
                "average_views": your_views
            },
            "competitor_averages": {
                "subscribers": avg_subscribers,
                "average_views": avg_views
            },
            "comparison": {
                "subscriber_gap": avg_subscribers - your_subs,
                "view_gap": avg_views - your_views,
                "position": "Below Average" if your_subs < avg_subscribers else "Above Average"
            },
            "recommendations": self._generate_comparison_recommendations(
                your_subs, avg_subscribers, your_views, avg_views
            )
        }
    
    def _generate_comparison_recommendations(
        self,
        your_subs: int,
        avg_subs: float,
        your_views: float,
        avg_views: float
    ) -> List[str]:
        """Generate recommendations based on comparison."""
        recommendations = []
        
        if your_subs < avg_subs * 0.5:
            recommendations.append("Focus on subscriber growth - consider collaborations or cross-promotion")
        
        if your_views < avg_views * 0.5:
            recommendations.append("Improve video discoverability - optimize titles, thumbnails, and tags")
        
        if your_views > avg_views * 1.5 and your_subs < avg_subs:
            recommendations.append("High views but low subscribers - add stronger calls-to-action to subscribe")
        
        return recommendations

