"""
Competitor Tracker Module
Continuous competitor monitoring and alerts.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.competitor_analyzer import CompetitorAnalyzer


class CompetitorTracker:
    """
    Competitor tracking system with continuous monitoring.
    
    AGI Paradigm: Continuous Learning Loop
    - Tracks competitor channels continuously
    - Sends alerts for new videos
    - Compares performance metrics
    """
    
    def __init__(
        self,
        client: YouTubeClient,
        competitor_analyzer: CompetitorAnalyzer,
        db_path: str = "data/competitor_tracking.json"
    ):
        self.client = client
        self.competitor_analyzer = competitor_analyzer
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database file and directory exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump({"competitors": []}, f, indent=2)
    
    def add_competitor(
        self,
        channel_id: str,
        channel_name: str,
        alerts_enabled: bool = True,
        tracking_enabled: bool = True
    ) -> bool:
        """Add a competitor to track."""
        competitors = self._load_competitors()
        
        # Check if already exists
        if any(c.get("channel_id") == channel_id for c in competitors):
            return False
        
        competitor = {
            "channel_id": channel_id,
            "channel_name": channel_name,
            "alerts_enabled": alerts_enabled,
            "tracking_enabled": tracking_enabled,
            "added_at": datetime.now().isoformat(),
            "last_check": None,
            "last_video_count": 0,
            "new_videos": []
        }
        
        competitors.append(competitor)
        self._save_competitors(competitors)
        return True
    
    def remove_competitor(self, channel_id: str) -> bool:
        """Remove a competitor from tracking."""
        competitors = self._load_competitors()
        original_count = len(competitors)
        competitors = [c for c in competitors if c.get("channel_id") != channel_id]
        
        if len(competitors) < original_count:
            self._save_competitors(competitors)
            return True
        return False
    
    def get_competitors(self) -> List[Dict[str, Any]]:
        """Get all tracked competitors."""
        return self._load_competitors()
    
    def check_competitors(self) -> Dict[str, Any]:
        """
        Check all competitors for new videos and updates.
        
        Returns:
            Dictionary with check results and new videos
        """
        competitors = self._load_competitors()
        results = {
            "checked_at": datetime.now().isoformat(),
            "competitors_checked": 0,
            "new_videos_found": 0,
            "alerts": []
        }
        
        for competitor in competitors:
            if not competitor.get("tracking_enabled", True):
                continue
            
            channel_id = competitor.get("channel_id")
            channel_name = competitor.get("channel_name", "Unknown")
            
            try:
                # Get channel videos
                videos = self.client.get_channel_videos(channel_id, max_results=10)
                
                if not videos:
                    continue
                
                # Get last video count
                last_count = competitor.get("last_video_count", 0)
                current_count = len(videos)
                
                # Check for new videos
                new_videos = []
                if current_count > last_count or competitor.get("last_check") is None:
                    # Get videos published after last check
                    last_check_str = competitor.get("last_check")
                    if last_check_str:
                        try:
                            last_check = datetime.fromisoformat(last_check_str.replace("Z", "+00:00"))
                        except:
                            last_check = datetime.now() - timedelta(days=7)
                    else:
                        last_check = datetime.now() - timedelta(days=7)
                    
                    for video in videos:
                        pub_date_str = video["snippet"].get("publishedAt", "")
                        if pub_date_str:
                            try:
                                pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                                if pub_date > last_check:
                                    new_videos.append({
                                        "video_id": video["id"],
                                        "title": video["snippet"]["title"],
                                        "published_at": pub_date_str,
                                        "thumbnail": video["snippet"]["thumbnails"].get("high", {}).get("url", ""),
                                        "views": int(video.get("statistics", {}).get("viewCount", 0))
                                    })
                            except:
                                pass
                
                # Update competitor data
                competitor["last_check"] = datetime.now().isoformat()
                competitor["last_video_count"] = current_count
                competitor["new_videos"] = new_videos
                
                # Generate alerts if enabled
                if competitor.get("alerts_enabled", True) and new_videos:
                    for video in new_videos:
                        results["alerts"].append({
                            "type": "new_video",
                            "competitor": channel_name,
                            "channel_id": channel_id,
                            "video": video
                        })
                        results["new_videos_found"] += 1
                
                results["competitors_checked"] += 1
                
            except Exception as e:
                # Log error but continue
                results["alerts"].append({
                    "type": "error",
                    "competitor": channel_name,
                    "channel_id": channel_id,
                    "error": str(e)
                })
        
        # Save updated competitors
        self._save_competitors(competitors)
        
        return results
    
    def compare_performance(
        self,
        your_channel_id: str,
        competitor_channel_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare your channel's performance with competitors.
        
        Args:
            your_channel_id: Your channel ID
            competitor_channel_ids: Optional list of competitor IDs (uses tracked if None)
        
        Returns:
            Performance comparison
        """
        # Get your channel data
        try:
            your_channel = self.client.get_channel_by_id(your_channel_id)
            if not your_channel.get("items"):
                return {"error": "Your channel not found"}
            
            your_stats = your_channel["items"][0]["statistics"]
            your_subs = int(your_stats.get("subscriberCount", 0))
            your_views = int(your_stats.get("viewCount", 0))
            your_videos = int(your_stats.get("videoCount", 0))
        except Exception as e:
            return {"error": f"Failed to fetch your channel: {str(e)}"}
        
        # Get competitor IDs
        if competitor_channel_ids is None:
            competitors = self._load_competitors()
            competitor_channel_ids = [c.get("channel_id") for c in competitors if c.get("tracking_enabled", True)]
        
        # Get competitor data
        competitor_data = []
        for comp_id in competitor_channel_ids:
            try:
                comp_channel = self.client.get_channel_by_id(comp_id)
                if comp_channel.get("items"):
                    comp_stats = comp_channel["items"][0]["statistics"]
                    comp_snippet = comp_channel["items"][0]["snippet"]
                    competitor_data.append({
                        "channel_id": comp_id,
                        "channel_name": comp_snippet.get("title", "Unknown"),
                        "subscribers": int(comp_stats.get("subscriberCount", 0)),
                        "views": int(comp_stats.get("viewCount", 0)),
                        "videos": int(comp_stats.get("videoCount", 0))
                    })
            except Exception:
                continue
        
        if not competitor_data:
            return {"error": "No competitor data available"}
        
        # Calculate averages
        avg_subs = sum(c["subscribers"] for c in competitor_data) / len(competitor_data)
        avg_views = sum(c["views"] for c in competitor_data) / len(competitor_data)
        avg_videos = sum(c["videos"] for c in competitor_data) / len(competitor_data)
        
        # Calculate your position
        subs_rank = sum(1 for c in competitor_data if c["subscribers"] < your_subs) + 1
        views_rank = sum(1 for c in competitor_data if c["views"] < your_views) + 1
        videos_rank = sum(1 for c in competitor_data if c["videos"] < your_videos) + 1
        
        return {
            "your_channel": {
                "channel_id": your_channel_id,
                "subscribers": your_subs,
                "views": your_views,
                "videos": your_videos
            },
            "competitor_averages": {
                "subscribers": avg_subs,
                "views": avg_views,
                "videos": avg_videos
            },
            "your_performance_vs_average": {
                "subscribers_ratio": (your_subs / avg_subs * 100) if avg_subs > 0 else 0,
                "views_ratio": (your_views / avg_views * 100) if avg_views > 0 else 0,
                "videos_ratio": (your_videos / avg_videos * 100) if avg_videos > 0 else 0
            },
            "ranking": {
                "subscribers_rank": f"{subs_rank}/{len(competitor_data) + 1}",
                "views_rank": f"{views_rank}/{len(competitor_data) + 1}",
                "videos_rank": f"{videos_rank}/{len(competitor_data) + 1}"
            },
            "competitors": competitor_data
        }
    
    def _load_competitors(self) -> List[Dict[str, Any]]:
        """Load competitors from database."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("competitors", [])
        except:
            return []
    
    def _save_competitors(self, competitors: List[Dict[str, Any]]):
        """Save competitors to database."""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump({"competitors": competitors}, f, indent=2, ensure_ascii=False)

