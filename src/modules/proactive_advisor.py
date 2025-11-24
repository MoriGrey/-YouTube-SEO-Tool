"""
Proactive Advisor Module
AGI-powered proactive suggestions and recommendations.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.channel_analyzer import ChannelAnalyzer
from src.modules.competitor_analyzer import CompetitorAnalyzer


class ProactiveAdvisor:
    """
    Proactive advisor with AGI-powered assistance.
    
    AGI Paradigm: Proactive Assistant Interface
    - Acts without being asked
    - Provides timely suggestions
    - Learns from user behavior
    """
    
    def __init__(
        self,
        client: YouTubeClient,
        channel_analyzer: ChannelAnalyzer,
        competitor_analyzer: CompetitorAnalyzer
    ):
        self.client = client
        self.channel_analyzer = channel_analyzer
        self.competitor_analyzer = competitor_analyzer
    
    def get_proactive_suggestions(
        self,
        channel_handle: str
    ) -> Dict[str, Any]:
        """
        Get proactive suggestions without being asked.
        
        Returns:
            Dictionary with proactive suggestions and alerts
        """
        suggestions = []
        alerts = []
        
        # Analyze channel
        try:
            channel_analysis = self.channel_analyzer.analyze_channel(channel_handle)
            
            # Check upload frequency
            upload_freq = channel_analysis.get("growth_analysis", {}).get("average_days_between_videos", 0)
            if upload_freq > 14:
                alerts.append({
                    "type": "warning",
                    "title": "Upload Frequency Low",
                    "message": f"Last video was {upload_freq:.0f} days ago. Consider uploading more frequently to maintain audience engagement.",
                    "priority": "high"
                })
            
            # Check engagement
            engagement = channel_analysis.get("engagement_analysis", {})
            avg_engagement = engagement.get("average_engagement_rate", 0)
            if avg_engagement < 2.0:
                suggestions.append({
                    "type": "improvement",
                    "title": "Low Engagement Rate",
                    "message": "Your engagement rate is below average. Try asking questions in descriptions or creating more interactive content.",
                    "action": "Review video descriptions and add call-to-actions"
                })
            
            # Check content strategy
            content = channel_analysis.get("content_analysis", {})
            title_length = content.get("average_title_length", 0)
            if title_length < 40 or title_length > 60:
                suggestions.append({
                    "type": "optimization",
                    "title": "Title Length Optimization",
                    "message": f"Your average title length is {title_length:.0f} characters. Optimal is 40-60 characters for better SEO.",
                    "action": "Optimize video titles"
                })
            
            # Performance alerts
            video_perf = channel_analysis.get("video_performance", {})
            avg_views = video_perf.get("average_views", 0)
            if avg_views < 100:
                alerts.append({
                    "type": "info",
                    "title": "Low View Counts",
                    "message": "Your videos are getting low views. Consider improving thumbnails, titles, and promotion strategies.",
                    "priority": "medium"
                })
            
        except Exception as e:
            alerts.append({
                "type": "error",
                "title": "Analysis Error",
                "message": f"Could not analyze channel: {str(e)}",
                "priority": "low"
            })
        
        # Content suggestions
        content_suggestions = self._generate_content_suggestions()
        
        # Timing suggestions
        timing_suggestions = self._generate_timing_suggestions()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "suggestions": suggestions,
            "alerts": alerts,
            "content_ideas": content_suggestions,
            "timing_recommendations": timing_suggestions,
            "priority_actions": self._get_priority_actions(suggestions, alerts)
        }
    
    def _generate_content_suggestions(self) -> List[Dict[str, Any]]:
        """Generate content ideas based on trends."""
        return [
            {
                "idea": "Create a 'Best of Psychedelic Anatolian Rock' compilation",
                "reason": "Compilation videos often perform well and can attract new viewers",
                "difficulty": "Easy"
            },
            {
                "idea": "Cover a trending Turkish folk song with psychedelic twist",
                "reason": "Trending songs get more search traffic",
                "difficulty": "Medium"
            },
            {
                "idea": "Create a 'How AI Creates Music' behind-the-scenes video",
                "reason": "Educational content builds authority and engagement",
                "difficulty": "Hard"
            },
            {
                "idea": "Make a 'Top 10 Psychedelic Anatolian Rock Songs' list",
                "reason": "List videos are highly shareable and searchable",
                "difficulty": "Easy"
            }
        ]
    
    def _generate_timing_suggestions(self) -> Dict[str, Any]:
        """Generate timing recommendations."""
        now = datetime.now()
        day_name = now.strftime("%A")
        hour = now.hour
        
        # Check if it's a good time to post
        good_times = [19, 20, 21]
        is_good_time = hour in good_times
        
        return {
            "current_time": {
                "day": day_name,
                "hour": hour,
                "is_optimal": is_good_time
            },
            "recommendation": "Post between 19:00-21:00 for maximum reach" if not is_good_time else "Now is a good time to post!",
            "next_best_time": "Today at 19:00" if hour < 19 else "Tomorrow at 19:00"
        }
    
    def _get_priority_actions(
        self,
        suggestions: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]]
    ) -> List[str]:
        """Get prioritized action items."""
        actions = []
        
        # High priority alerts first
        high_priority_alerts = [a for a in alerts if a.get("priority") == "high"]
        for alert in high_priority_alerts:
            actions.append(f"URGENT: {alert['title']} - {alert['message']}")
        
        # Then suggestions
        for suggestion in suggestions[:3]:
            actions.append(f"{suggestion['title']}: {suggestion['action']}")
        
        return actions
    
    def check_competitor_activity(
        self,
        competitor_keywords: List[str]
    ) -> Dict[str, Any]:
        """Check what competitors are doing."""
        try:
            competitors = self.competitor_analyzer.find_competitors(
                competitor_keywords,
                max_competitors=5
            )
            
            if competitors:
                latest_activity = []
                for comp in competitors[:3]:
                    latest_activity.append({
                        "channel": comp["title"],
                        "subscribers": comp["subscribers"],
                        "status": "Active" if comp["video_count"] > 10 else "New"
                    })
                
                return {
                    "competitors_found": len(competitors),
                    "latest_activity": latest_activity,
                    "recommendation": "Monitor top competitors for content ideas and trends"
                }
        except Exception:
            pass
        
        return {"message": "Could not analyze competitors at this time"}
    
    def weekly_report_suggestions(self) -> Dict[str, Any]:
        """Generate weekly report suggestions."""
        return {
            "report_type": "Weekly Performance Review",
            "suggestions": [
                "Review video performance metrics",
                "Analyze which titles performed best",
                "Check engagement rates",
                "Compare with previous week",
                "Plan next week's content",
                "Update tags and descriptions for older videos"
            ],
            "automated": True
        }

