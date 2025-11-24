"""
Channel Analysis Module
Deep analysis of YouTube channel performance and metrics.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient


class ChannelAnalyzer:
    """
    Comprehensive channel analysis with AGI-powered insights.
    
    AGI Paradigm: Self-Evolving Architecture
    - Analyzes patterns in channel growth
    - Identifies optimization opportunities
    - Provides actionable recommendations
    """
    
    def __init__(self, client: YouTubeClient):
        self.client = client
    
    def analyze_channel(self, channel_handle: str) -> Dict[str, Any]:
        """
        Perform comprehensive channel analysis.
        
        Returns:
            Dictionary with analysis results including:
            - Basic stats
            - Growth metrics
            - Content performance
            - Engagement analysis
            - Recommendations
        """
        # Get channel data
        channel_data = self.client.get_channel_by_handle(channel_handle)
        if not channel_data.get("items"):
            raise ValueError(f"Channel @{channel_handle} not found")
        
        channel = channel_data["items"][0]
        channel_id = channel["id"]
        
        # Get all videos
        videos = self.client.get_channel_videos(channel_id, max_results=50)
        
        # Basic statistics
        stats = channel["statistics"]
        snippet = channel["snippet"]
        
        # Calculate metrics
        total_views = int(stats.get("viewCount", 0))
        total_subscribers = int(stats.get("subscriberCount", 0))
        total_videos = int(stats.get("videoCount", 0))
        
        # Video performance analysis
        video_analysis = self._analyze_videos(videos)
        
        # Growth analysis
        growth_analysis = self._analyze_growth(videos, snippet.get("publishedAt"))
        
        # Engagement analysis
        engagement_analysis = self._analyze_engagement(videos)
        
        # Content strategy analysis
        content_analysis = self._analyze_content_strategy(videos)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            video_analysis,
            engagement_analysis,
            content_analysis,
            total_subscribers
        )
        
        return {
            "channel_info": {
                "id": channel_id,
                "title": snippet["title"],
                "description": snippet.get("description", ""),
                "created": snippet.get("publishedAt", ""),
                "country": snippet.get("country", "Unknown")
            },
            "statistics": {
                "subscribers": total_subscribers,
                "total_views": total_views,
                "total_videos": total_videos,
                "average_views_per_video": total_views / max(total_videos, 1),
                "views_per_subscriber": total_views / max(total_subscribers, 1)
            },
            "video_performance": video_analysis,
            "growth_analysis": growth_analysis,
            "engagement_analysis": engagement_analysis,
            "content_analysis": content_analysis,
            "recommendations": recommendations
        }
    
    def _analyze_videos(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze video performance metrics."""
        if not videos:
            return {}
        
        views = [int(v.get("statistics", {}).get("viewCount", 0)) for v in videos]
        likes = [int(v.get("statistics", {}).get("likeCount", 0)) for v in videos]
        comments = [int(v.get("statistics", {}).get("commentCount", 0)) for v in videos]
        
        # Calculate engagement rates
        total_views = sum(views)
        total_engagement = sum(likes) + sum(comments)
        engagement_rate = (total_engagement / max(total_views, 1)) * 100
        
        # Best performing video
        best_video = max(videos, key=lambda v: int(v.get("statistics", {}).get("viewCount", 0)))
        
        return {
            "total_videos": len(videos),
            "total_views": sum(views),
            "total_likes": sum(likes),
            "total_comments": sum(comments),
            "average_views": sum(views) / len(videos),
            "average_likes": sum(likes) / len(videos),
            "average_comments": sum(comments) / len(videos),
            "engagement_rate": engagement_rate,
            "best_performing": {
                "title": best_video["snippet"]["title"],
                "views": int(best_video.get("statistics", {}).get("viewCount", 0)),
                "video_id": best_video["id"]
            },
            "views_distribution": {
                "min": min(views) if views else 0,
                "max": max(views) if views else 0,
                "median": sorted(views)[len(views)//2] if views else 0
            }
        }
    
    def _analyze_growth(self, videos: List[Dict[str, Any]], channel_created: str) -> Dict[str, Any]:
        """Analyze channel growth patterns."""
        if not videos or not channel_created:
            return {}
        
        # Parse dates
        try:
            channel_date = datetime.fromisoformat(channel_created.replace("Z", "+00:00"))
            now = datetime.now(channel_date.tzinfo)
            days_active = (now - channel_date).days
            
            # Video upload frequency
            video_dates = []
            for video in videos:
                pub_date = video["snippet"].get("publishedAt", "")
                if pub_date:
                    try:
                        video_dates.append(datetime.fromisoformat(pub_date.replace("Z", "+00:00")))
                    except:
                        pass
            
            if video_dates:
                video_dates.sort()
                days_between_videos = []
                for i in range(1, len(video_dates)):
                    days_between_videos.append((video_dates[i] - video_dates[i-1]).days)
                
                avg_days_between = sum(days_between_videos) / len(days_between_videos) if days_between_videos else 0
            else:
                avg_days_between = 0
            
            return {
                "days_active": days_active,
                "videos_per_week": len(videos) / max(days_active / 7, 1),
                "average_days_between_videos": avg_days_between,
                "upload_consistency": "Good" if avg_days_between < 14 else "Needs Improvement"
            }
        except Exception:
            return {}
    
    def _analyze_engagement(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze audience engagement."""
        if not videos:
            return {}
        
        engagement_data = []
        for video in videos:
            stats = video.get("statistics", {})
            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))
            
            if views > 0:
                like_rate = (likes / views) * 100
                comment_rate = (comments / views) * 100
                total_engagement = likes + comments
                engagement_rate = (total_engagement / views) * 100
                
                engagement_data.append({
                    "like_rate": like_rate,
                    "comment_rate": comment_rate,
                    "engagement_rate": engagement_rate
                })
        
        if engagement_data:
            avg_like_rate = sum(d["like_rate"] for d in engagement_data) / len(engagement_data)
            avg_comment_rate = sum(d["comment_rate"] for d in engagement_data) / len(engagement_data)
            avg_engagement_rate = sum(d["engagement_rate"] for d in engagement_data) / len(engagement_data)
            
            return {
                "average_like_rate": avg_like_rate,
                "average_comment_rate": avg_comment_rate,
                "average_engagement_rate": avg_engagement_rate,
                "benchmark_comparison": {
                    "like_rate": "Above Average" if avg_like_rate > 2.0 else "Below Average",
                    "comment_rate": "Above Average" if avg_comment_rate > 0.5 else "Below Average"
                }
            }
        
        return {}
    
    def _analyze_content_strategy(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content strategy and patterns."""
        if not videos:
            return {}
        
        titles = [v["snippet"]["title"] for v in videos]
        descriptions = [v["snippet"].get("description", "") for v in videos]
        
        # Title analysis
        title_lengths = [len(t) for t in titles]
        avg_title_length = sum(title_lengths) / len(title_lengths) if title_lengths else 0
        
        # Keyword frequency in titles
        common_words = {}
        for title in titles:
            words = title.lower().split()
            for word in words:
                if len(word) > 3:  # Ignore short words
                    common_words[word] = common_words.get(word, 0) + 1
        
        top_keywords = sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "average_title_length": avg_title_length,
            "title_length_status": "Optimal" if 40 <= avg_title_length <= 60 else "Needs Optimization",
            "top_keywords": [{"word": word, "frequency": freq} for word, freq in top_keywords],
            "has_consistent_branding": len(set([t.split("|")[0].strip() if "|" in t else "" for t in titles])) <= 2
        }
    
    def _generate_recommendations(
        self,
        video_analysis: Dict[str, Any],
        engagement_analysis: Dict[str, Any],
        content_analysis: Dict[str, Any],
        subscribers: int
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Engagement recommendations
        if engagement_analysis:
            if engagement_analysis.get("average_engagement_rate", 0) < 3.0:
                recommendations.append(
                    "Engagement rate is below average. Try asking questions in video descriptions "
                    "or creating more interactive content."
                )
        
        # Content recommendations
        if content_analysis:
            if content_analysis.get("average_title_length", 0) < 40:
                recommendations.append(
                    "Titles are too short. Aim for 40-60 characters to improve SEO and click-through rates."
                )
            elif content_analysis.get("average_title_length", 0) > 60:
                recommendations.append(
                    "Titles are too long. Keep them under 60 characters for better visibility in search results."
                )
        
        # Growth recommendations
        if subscribers < 100:
            recommendations.append(
                "Focus on consistent uploads (at least once per week) to build momentum and subscriber base."
            )
        
        # Video performance recommendations
        if video_analysis:
            avg_views = video_analysis.get("average_views", 0)
            if avg_views < 100:
                recommendations.append(
                    "Consider improving thumbnails and titles to increase click-through rates. "
                    "Study your best-performing video for patterns."
                )
        
        if not recommendations:
            recommendations.append("Keep up the good work! Continue creating consistent, high-quality content.")
        
        return recommendations

