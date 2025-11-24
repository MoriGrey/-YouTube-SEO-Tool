"""
Performance Tracking & Self-Improvement Module
Tracks performance of recommendations and learns from successes/failures.

AGI Paradigm: Performance Tracking & Self-Improvement
- Tracks real performance of recommendations
- Learns successful strategies automatically
- Optimizes subscriber growth rate
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient

try:
    from diskcache import Cache
except ImportError:
    # Fallback if diskcache not available
    Cache = None


class PerformanceTracker:
    """
    Performance tracking with self-improvement capabilities.
    
    AGI Paradigm: Performance Tracking & Self-Improvement
    - Tracks recommendation performance over time
    - Learns which strategies work best
    - Optimizes for subscriber growth
    """
    
    CACHE_DIR = ".cache/performance"
    DATA_FILE = "data/performance_history.json"
    
    def __init__(self, client: YouTubeClient):
        self.client = client
        self._cache = Cache(self.CACHE_DIR) if Cache else None
        self._ensure_data_dir()
        self._load_history()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
    
    def _load_history(self) -> Dict[str, Any]:
        """Load performance history from file."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "snapshots": [],
            "recommendations": {},
            "learned_patterns": {},
            "success_metrics": {}
        }
    
    def _save_history(self, data: Dict[str, Any]):
        """Save performance history to file."""
        try:
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving performance history: {e}")
    
    def track_snapshot(self, channel_handle: str) -> Dict[str, Any]:
        """
        Take a snapshot of current channel performance.
        
        Args:
            channel_handle: Channel handle to track
            
        Returns:
            Snapshot data with metrics
        """
        try:
            channel_data = self.client.get_channel_by_handle(channel_handle)
            if not channel_data.get("items"):
                raise ValueError(f"Channel @{channel_handle} not found")
            
            channel = channel_data["items"][0]
            stats = channel["statistics"]
            channel_id = channel["id"]
            
            # Get recent videos for analysis
            videos = self.client.get_channel_videos(channel_id, max_results=10)
            
            snapshot = {
                "timestamp": datetime.now().isoformat(),
                "channel_handle": channel_handle,
                "channel_id": channel_id,
                "metrics": {
                    "subscribers": int(stats.get("subscriberCount", 0)),
                    "total_views": int(stats.get("viewCount", 0)),
                    "total_videos": int(stats.get("videoCount", 0)),
                    "average_views_per_video": int(stats.get("viewCount", 0)) / max(int(stats.get("videoCount", 1)), 1)
                },
                "recent_videos": []
            }
            
            # Track recent video performance
            for video in videos[:5]:
                video_stats = video.get("statistics", {})
                snapshot["recent_videos"].append({
                    "video_id": video["id"],
                    "title": video["snippet"]["title"],
                    "views": int(video_stats.get("viewCount", 0)),
                    "likes": int(video_stats.get("likeCount", 0)),
                    "comments": int(video_stats.get("commentCount", 0)),
                    "published_at": video["snippet"].get("publishedAt", "")
                })
            
            # Save snapshot
            history = self._load_history()
            history["snapshots"].append(snapshot)
            
            # Keep only last 100 snapshots
            if len(history["snapshots"]) > 100:
                history["snapshots"] = history["snapshots"][-100:]
            
            self._save_history(history)
            
            return snapshot
            
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def track_recommendation(
        self,
        recommendation_id: str,
        recommendation_type: str,
        recommendation_data: Dict[str, Any],
        video_id: Optional[str] = None
    ):
        """
        Track a recommendation that was made.
        
        Args:
            recommendation_id: Unique ID for this recommendation
            recommendation_type: Type (title, description, tags, etc.)
            recommendation_data: The recommendation data
            video_id: Optional video ID if recommendation is for a specific video
        """
        history = self._load_history()
        
        if "recommendations" not in history:
            history["recommendations"] = {}
        
        history["recommendations"][recommendation_id] = {
            "type": recommendation_type,
            "data": recommendation_data,
            "video_id": video_id,
            "created_at": datetime.now().isoformat(),
            "status": "pending",  # pending, applied, rejected, success, failure
            "performance": None
        }
        
        self._save_history(history)
    
    def update_recommendation_status(
        self,
        recommendation_id: str,
        status: str,
        performance_data: Optional[Dict[str, Any]] = None
    ):
        """
        Update status of a recommendation.
        
        Args:
            recommendation_id: ID of recommendation
            status: New status (applied, rejected, success, failure)
            performance_data: Optional performance metrics
        """
        history = self._load_history()
        
        if recommendation_id in history.get("recommendations", {}):
            history["recommendations"][recommendation_id]["status"] = status
            history["recommendations"][recommendation_id]["updated_at"] = datetime.now().isoformat()
            
            if performance_data:
                history["recommendations"][recommendation_id]["performance"] = performance_data
            
            self._save_history(history)
    
    def analyze_growth_trend(self, channel_handle: str, days: int = 30) -> Dict[str, Any]:
        """
        Analyze growth trend over time.
        
        Args:
            channel_handle: Channel to analyze
            days: Number of days to look back
            
        Returns:
            Growth trend analysis
        """
        history = self._load_history()
        snapshots = history.get("snapshots", [])
        
        # Filter snapshots for this channel and time period
        cutoff_date = datetime.now() - timedelta(days=days)
        relevant_snapshots = [
            s for s in snapshots
            if s.get("channel_handle") == channel_handle
            and datetime.fromisoformat(s["timestamp"]) >= cutoff_date
        ]
        
        if len(relevant_snapshots) < 2:
            return {
                "status": "insufficient_data",
                "message": "Need at least 2 snapshots to analyze growth",
                "snapshots_count": len(relevant_snapshots)
            }
        
        # Sort by timestamp
        relevant_snapshots.sort(key=lambda x: x["timestamp"])
        
        # Calculate growth metrics
        first = relevant_snapshots[0]
        last = relevant_snapshots[-1]
        
        subscriber_growth = last["metrics"]["subscribers"] - first["metrics"]["subscribers"]
        view_growth = last["metrics"]["total_views"] - first["metrics"]["total_views"]
        days_elapsed = (datetime.fromisoformat(last["timestamp"]) - 
                      datetime.fromisoformat(first["timestamp"])).days
        
        subscriber_growth_rate = (subscriber_growth / max(first["metrics"]["subscribers"], 1)) * 100 if days_elapsed > 0 else 0
        daily_subscriber_growth = subscriber_growth / max(days_elapsed, 1)
        
        # Calculate conversion rate
        conversion_rate = (last["metrics"]["subscribers"] / max(last["metrics"]["total_views"], 1)) * 100
        
        # Project to 1M subscribers
        if daily_subscriber_growth > 0:
            days_to_1m = (1_000_000 - last["metrics"]["subscribers"]) / daily_subscriber_growth
            projected_date = datetime.now() + timedelta(days=days_to_1m)
        else:
            days_to_1m = None
            projected_date = None
        
        return {
            "period": {
                "start": first["timestamp"],
                "end": last["timestamp"],
                "days": days_elapsed
            },
            "growth": {
                "subscribers": {
                    "start": first["metrics"]["subscribers"],
                    "end": last["metrics"]["subscribers"],
                    "change": subscriber_growth,
                    "growth_rate_percent": subscriber_growth_rate,
                    "daily_average": daily_subscriber_growth
                },
                "views": {
                    "start": first["metrics"]["total_views"],
                    "end": last["metrics"]["total_views"],
                    "change": view_growth
                }
            },
            "metrics": {
                "conversion_rate_percent": conversion_rate,
                "views_per_subscriber": last["metrics"]["total_views"] / max(last["metrics"]["subscribers"], 1)
            },
            "projection": {
                "current_subscribers": last["metrics"]["subscribers"],
                "target_subscribers": 1_000_000,
                "daily_growth_needed": daily_subscriber_growth,
                "days_to_1m": days_to_1m,
                "projected_date": projected_date.isoformat() if projected_date else None
            },
            "recommendations": self._generate_growth_recommendations(
                subscriber_growth_rate,
                daily_subscriber_growth,
                conversion_rate
            )
        }
    
    def _generate_growth_recommendations(
        self,
        growth_rate: float,
        daily_growth: float,
        conversion_rate: float
    ) -> List[str]:
        """Generate recommendations based on growth metrics."""
        recommendations = []
        
        if growth_rate < 5:
            recommendations.append("Subscriber growth rate is low. Focus on improving video titles and thumbnails to increase click-through rate.")
        
        if daily_growth < 1:
            recommendations.append("Daily subscriber growth is below 1. Consider increasing upload frequency or improving content quality.")
        
        if conversion_rate < 1:
            recommendations.append("Conversion rate (subscribers/views) is low. Improve call-to-actions in video descriptions and end screens.")
        
        if growth_rate > 10 and daily_growth > 5:
            recommendations.append("Great growth! Maintain consistency and consider scaling successful content patterns.")
        
        return recommendations
    
    def learn_from_recommendations(self) -> Dict[str, Any]:
        """
        Learn patterns from tracked recommendations.
        
        Returns:
            Learned patterns and insights
        """
        history = self._load_history()
        recommendations = history.get("recommendations", {})
        
        if not recommendations:
            return {
                "status": "no_data",
                "message": "No recommendations tracked yet"
            }
        
        # Analyze successful recommendations
        successful = [
            r for r in recommendations.values()
            if r.get("status") == "success"
        ]
        
        failed = [
            r for r in recommendations.values()
            if r.get("status") == "failure"
        ]
        
        # Group by type
        by_type = {}
        for rec in recommendations.values():
            rec_type = rec.get("type", "unknown")
            if rec_type not in by_type:
                by_type[rec_type] = {"total": 0, "success": 0, "failure": 0}
            by_type[rec_type]["total"] += 1
            if rec.get("status") == "success":
                by_type[rec_type]["success"] += 1
            elif rec.get("status") == "failure":
                by_type[rec_type]["failure"] += 1
        
        # Calculate success rates
        success_rates = {}
        for rec_type, stats in by_type.items():
            if stats["total"] > 0:
                success_rates[rec_type] = {
                    "success_rate": (stats["success"] / stats["total"]) * 100,
                    "total": stats["total"],
                    "success": stats["success"],
                    "failure": stats["failure"]
                }
        
        # Update learned patterns
        history["learned_patterns"] = {
            "success_rates": success_rates,
            "total_recommendations": len(recommendations),
            "successful": len(successful),
            "failed": len(failed),
            "last_updated": datetime.now().isoformat()
        }
        
        self._save_history(history)
        
        return {
            "summary": {
                "total_recommendations": len(recommendations),
                "successful": len(successful),
                "failed": len(failed),
                "success_rate": (len(successful) / max(len(recommendations), 1)) * 100
            },
            "by_type": success_rates,
            "insights": self._generate_insights(success_rates)
        }
    
    def _generate_insights(self, success_rates: Dict[str, Any]) -> List[str]:
        """Generate insights from success rates."""
        insights = []
        
        if not success_rates:
            return ["No data available for insights yet. Start tracking recommendations to learn patterns."]
        
        # Find best performing type
        best_type = max(success_rates.items(), key=lambda x: x[1].get("success_rate", 0))
        if best_type[1]["success_rate"] > 70:
            insights.append(f"{best_type[0]} recommendations are performing very well ({best_type[1]['success_rate']:.1f}% success rate). Continue using this strategy.")
        
        # Find worst performing type
        worst_type = min(success_rates.items(), key=lambda x: x[1].get("success_rate", 100))
        if worst_type[1]["success_rate"] < 30:
            insights.append(f"{worst_type[0]} recommendations need improvement ({worst_type[1]['success_rate']:.1f}% success rate). Review and refine this approach.")
        
        # Overall success rate
        avg_success = sum(s["success_rate"] for s in success_rates.values()) / len(success_rates)
        if avg_success >= 80:
            insights.append(f"Excellent overall performance! Average success rate is {avg_success:.1f}%. System is learning effectively.")
        elif avg_success < 50:
            insights.append(f"Success rate is below target ({avg_success:.1f}%). Review recommendation strategies and improve data quality.")
        
        return insights
    
    def get_performance_summary(self, channel_handle: str) -> Dict[str, Any]:
        """
        Get comprehensive performance summary.
        
        Args:
            channel_handle: Channel to summarize
            
        Returns:
            Performance summary
        """
        # Get latest snapshot
        latest_snapshot = self.track_snapshot(channel_handle)
        
        # Analyze growth trend
        growth_trend = self.analyze_growth_trend(channel_handle, days=30)
        
        # Learn from recommendations
        learned_patterns = self.learn_from_recommendations()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "channel_handle": channel_handle,
            "current_metrics": latest_snapshot.get("metrics", {}),
            "growth_trend": growth_trend,
            "learned_patterns": learned_patterns,
            "recommendations": growth_trend.get("recommendations", [])
        }

