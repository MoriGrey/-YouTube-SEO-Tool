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
    
    def forecast_performance(
        self,
        channel_handle: str,
        days_ahead: int = 30,
        scenarios: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Forecast future performance based on historical data.
        
        Args:
            channel_handle: Channel to forecast
            days_ahead: Number of days to forecast (7, 30, 90, 180, 365)
            scenarios: Optional list of scenarios to analyze (e.g., ["optimistic", "realistic", "pessimistic"])
            
        Returns:
            Performance forecast with projections
        """
        history = self._load_history()
        snapshots = history.get("snapshots", [])
        
        # Filter snapshots for this channel
        relevant_snapshots = [
            s for s in snapshots
            if s.get("channel_handle") == channel_handle
        ]
        
        if len(relevant_snapshots) < 2:
            return {
                "error": "Insufficient data",
                "message": "Need at least 2 snapshots to forecast. Take more snapshots first.",
                "snapshots_count": len(relevant_snapshots)
            }
        
        # Sort by timestamp
        relevant_snapshots.sort(key=lambda x: x["timestamp"])
        
        # Get current metrics
        current = relevant_snapshots[-1]
        current_metrics = current["metrics"]
        
        # Calculate growth rates from historical data
        growth_rates = self._calculate_growth_rates(relevant_snapshots)
        
        # Default scenarios if not provided
        if not scenarios:
            scenarios = ["realistic", "optimistic", "pessimistic"]
        
        # Generate forecasts for each scenario
        forecasts = {}
        for scenario in scenarios:
            forecasts[scenario] = self._generate_scenario_forecast(
                current_metrics,
                growth_rates,
                days_ahead,
                scenario
            )
        
        # Calculate confidence intervals
        confidence = self._calculate_forecast_confidence(relevant_snapshots, growth_rates)
        
        # Generate recommendations based on forecast
        recommendations = self._generate_forecast_recommendations(forecasts, growth_rates)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "channel_handle": channel_handle,
            "forecast_period": {
                "days_ahead": days_ahead,
                "forecast_date": (datetime.now() + timedelta(days=days_ahead)).isoformat()
            },
            "current_metrics": current_metrics,
            "historical_growth_rates": growth_rates,
            "scenarios": forecasts,
            "confidence": confidence,
            "recommendations": recommendations
        }
    
    def _calculate_growth_rates(self, snapshots: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate average growth rates from snapshots."""
        if len(snapshots) < 2:
            return {
                "subscriber_daily": 0.0,
                "view_daily": 0.0,
                "subscriber_weekly": 0.0,
                "view_weekly": 0.0
            }
        
        # Calculate daily growth rates
        subscriber_changes = []
        view_changes = []
        day_diffs = []
        
        for i in range(1, len(snapshots)):
            prev = snapshots[i-1]
            curr = snapshots[i]
            
            sub_change = curr["metrics"]["subscribers"] - prev["metrics"]["subscribers"]
            view_change = curr["metrics"]["total_views"] - prev["metrics"]["total_views"]
            
            prev_date = datetime.fromisoformat(prev["timestamp"])
            curr_date = datetime.fromisoformat(curr["timestamp"])
            days_diff = (curr_date - prev_date).days
            
            if days_diff > 0:
                subscriber_changes.append(sub_change / days_diff)
                view_changes.append(view_change / days_diff)
                day_diffs.append(days_diff)
        
        avg_sub_daily = sum(subscriber_changes) / len(subscriber_changes) if subscriber_changes else 0.0
        avg_view_daily = sum(view_changes) / len(view_changes) if view_changes else 0.0
        
        return {
            "subscriber_daily": avg_sub_daily,
            "view_daily": avg_view_daily,
            "subscriber_weekly": avg_sub_daily * 7,
            "view_weekly": avg_view_daily * 7
        }
    
    def _generate_scenario_forecast(
        self,
        current_metrics: Dict[str, Any],
        growth_rates: Dict[str, float],
        days_ahead: int,
        scenario: str
    ) -> Dict[str, Any]:
        """Generate forecast for a specific scenario."""
        # Scenario multipliers
        multipliers = {
            "optimistic": 1.5,  # 50% better than average
            "realistic": 1.0,  # Average growth
            "pessimistic": 0.5  # 50% worse than average
        }
        
        multiplier = multipliers.get(scenario, 1.0)
        
        # Project subscribers
        daily_sub_growth = growth_rates["subscriber_daily"] * multiplier
        projected_subscribers = current_metrics["subscribers"] + (daily_sub_growth * days_ahead)
        
        # Project views
        daily_view_growth = growth_rates["view_daily"] * multiplier
        projected_views = current_metrics["total_views"] + (daily_view_growth * days_ahead)
        
        # Project videos (assume same upload frequency)
        current_videos = current_metrics.get("total_videos", 0)
        avg_views_per_video = current_metrics.get("average_views_per_video", 0)
        
        # Estimate new videos based on historical upload rate
        # If we have historical data, use it; otherwise estimate conservatively
        estimated_new_videos = max(int(days_ahead / 7), 1)  # Assume at least 1 video per week
        
        projected_videos = current_videos + estimated_new_videos
        projected_avg_views = projected_views / max(projected_videos, 1)
        
        # Calculate conversion rate projection
        projected_conversion_rate = (projected_subscribers / max(projected_views, 1)) * 100
        
        # Calculate days to 1M subscribers
        if daily_sub_growth > 0:
            days_to_1m = max(0, (1_000_000 - projected_subscribers) / daily_sub_growth)
            projected_1m_date = (datetime.now() + timedelta(days=days_ahead + days_to_1m)).isoformat()
        else:
            days_to_1m = None
            projected_1m_date = None
        
        return {
            "subscribers": {
                "current": current_metrics["subscribers"],
                "projected": int(projected_subscribers),
                "change": int(projected_subscribers - current_metrics["subscribers"]),
                "daily_growth": daily_sub_growth
            },
            "views": {
                "current": current_metrics["total_views"],
                "projected": int(projected_views),
                "change": int(projected_views - current_metrics["total_views"]),
                "daily_growth": daily_view_growth
            },
            "videos": {
                "current": current_videos,
                "projected": projected_videos,
                "new_videos": estimated_new_videos
            },
            "metrics": {
                "projected_avg_views_per_video": int(projected_avg_views),
                "projected_conversion_rate": projected_conversion_rate
            },
            "milestone": {
                "days_to_1m": days_to_1m,
                "projected_1m_date": projected_1m_date
            }
        }
    
    def _calculate_forecast_confidence(
        self,
        snapshots: List[Dict[str, Any]],
        growth_rates: Dict[str, float]
    ) -> Dict[str, Any]:
        """Calculate confidence level for forecast."""
        if len(snapshots) < 3:
            return {
                "level": "low",
                "score": 30,
                "reason": "Insufficient historical data (need at least 3 snapshots)"
            }
        
        # More snapshots = higher confidence
        snapshot_count = len(snapshots)
        if snapshot_count >= 10:
            base_confidence = 80
        elif snapshot_count >= 5:
            base_confidence = 60
        else:
            base_confidence = 40
        
        # Check data consistency
        growth_consistency = self._check_growth_consistency(snapshots)
        
        # Adjust confidence based on consistency
        if growth_consistency > 0.7:
            confidence_score = base_confidence + 10
        elif growth_consistency > 0.5:
            confidence_score = base_confidence
        else:
            confidence_score = base_confidence - 10
        
        confidence_score = max(10, min(90, confidence_score))  # Clamp between 10-90
        
        if confidence_score >= 70:
            level = "high"
        elif confidence_score >= 50:
            level = "medium"
        else:
            level = "low"
        
        return {
            "level": level,
            "score": confidence_score,
            "snapshot_count": snapshot_count,
            "growth_consistency": growth_consistency
        }
    
    def _check_growth_consistency(self, snapshots: List[Dict[str, Any]]) -> float:
        """Check how consistent growth rates are (0-1, higher = more consistent)."""
        if len(snapshots) < 3:
            return 0.5
        
        subscriber_values = [s["metrics"]["subscribers"] for s in snapshots]
        
        # Calculate coefficient of variation (std/mean)
        if len(subscriber_values) > 1:
            mean = sum(subscriber_values) / len(subscriber_values)
            if mean > 0:
                variance = sum((x - mean) ** 2 for x in subscriber_values) / len(subscriber_values)
                std = variance ** 0.5
                cv = std / mean
                # Lower CV = more consistent
                consistency = max(0, 1 - min(cv, 1))
                return consistency
        
        return 0.5
    
    def _generate_forecast_recommendations(
        self,
        forecasts: Dict[str, Any],
        growth_rates: Dict[str, float]
    ) -> List[str]:
        """Generate recommendations based on forecast."""
        recommendations = []
        
        realistic = forecasts.get("realistic", {})
        optimistic = forecasts.get("optimistic", {})
        
        if realistic:
            realistic_subs = realistic.get("subscribers", {}).get("projected", 0)
            current_subs = realistic.get("subscribers", {}).get("current", 0)
            
            # Check if growth is positive
            if realistic_subs > current_subs:
                growth_percent = ((realistic_subs - current_subs) / max(current_subs, 1)) * 100
                if growth_percent < 5:
                    recommendations.append("Forecast shows slow growth. Consider increasing upload frequency or improving content quality.")
                elif growth_percent > 20:
                    recommendations.append("Forecast shows strong growth potential. Maintain consistency and scale successful strategies.")
            
            # Check days to 1M
            days_to_1m = realistic.get("milestone", {}).get("days_to_1m")
            if days_to_1m and days_to_1m > 365 * 5:  # More than 5 years
                recommendations.append("At current growth rate, reaching 1M subscribers will take more than 5 years. Consider aggressive growth strategies.")
            elif days_to_1m and days_to_1m < 365:  # Less than 1 year
                recommendations.append("Excellent forecast! At current growth rate, you could reach 1M subscribers within a year. Maintain momentum!")
        
        # Compare scenarios
        if optimistic and realistic:
            opt_subs = optimistic.get("subscribers", {}).get("projected", 0)
            real_subs = realistic.get("subscribers", {}).get("projected", 0)
            
            if opt_subs > real_subs * 1.3:
                recommendations.append("Optimistic scenario shows 30%+ better growth. Focus on implementing best practices to achieve optimistic forecast.")
        
        # Daily growth recommendations
        daily_growth = growth_rates.get("subscriber_daily", 0)
        if daily_growth < 1:
            recommendations.append("Daily subscriber growth is below 1. Focus on improving video discoverability and engagement.")
        elif daily_growth > 10:
            recommendations.append("Strong daily growth! Continue current strategies and consider scaling successful content patterns.")
        
        return recommendations
    
    def analyze_scenario_impact(
        self,
        channel_handle: str,
        strategy_changes: Dict[str, Any],
        days_ahead: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze impact of different strategy changes on future performance.
        
        Args:
            channel_handle: Channel to analyze
            strategy_changes: Dictionary of strategy changes (e.g., {"upload_frequency": 2, "ctr_improvement": 0.1})
            days_ahead: Number of days to project
            
        Returns:
            Impact analysis comparing baseline vs. strategy changes
        """
        # Get baseline forecast
        baseline_forecast = self.forecast_performance(channel_handle, days_ahead, ["realistic"])
        baseline = baseline_forecast.get("scenarios", {}).get("realistic", {})
        
        if baseline_forecast.get("error"):
            return baseline_forecast
        
        # Get current metrics and growth rates
        history = self._load_history()
        snapshots = [
            s for s in history.get("snapshots", [])
            if s.get("channel_handle") == channel_handle
        ]
        snapshots.sort(key=lambda x: x["timestamp"])
        
        if not snapshots:
            return {"error": "No historical data available"}
        
        current_metrics = snapshots[-1]["metrics"]
        growth_rates = self._calculate_growth_rates(snapshots)
        
        # Apply strategy changes
        modified_growth_rates = growth_rates.copy()
        
        # Upload frequency impact
        if "upload_frequency" in strategy_changes:
            freq_multiplier = strategy_changes["upload_frequency"] / 1.0  # Assume baseline is 1 video/week
            modified_growth_rates["subscriber_daily"] *= (1 + (freq_multiplier - 1) * 0.3)  # 30% impact
            modified_growth_rates["view_daily"] *= freq_multiplier
        
        # CTR improvement impact
        if "ctr_improvement" in strategy_changes:
            ctr_boost = strategy_changes["ctr_improvement"]  # e.g., 0.1 = 10% improvement
            modified_growth_rates["view_daily"] *= (1 + ctr_boost)
            modified_growth_rates["subscriber_daily"] *= (1 + ctr_boost * 0.5)  # 50% of CTR impact on subs
        
        # Engagement improvement impact
        if "engagement_improvement" in strategy_changes:
            eng_boost = strategy_changes["engagement_improvement"]
            modified_growth_rates["subscriber_daily"] *= (1 + eng_boost * 0.4)  # 40% impact on subs
        
        # SEO optimization impact
        if "seo_optimization" in strategy_changes:
            seo_boost = strategy_changes["seo_optimization"]
            modified_growth_rates["view_daily"] *= (1 + seo_boost * 0.3)
            modified_growth_rates["subscriber_daily"] *= (1 + seo_boost * 0.2)
        
        # Generate modified forecast
        modified_forecast = self._generate_scenario_forecast(
            current_metrics,
            modified_growth_rates,
            days_ahead,
            "realistic"
        )
        
        # Calculate impact
        baseline_subs = baseline.get("subscribers", {}).get("projected", 0)
        modified_subs = modified_forecast.get("subscribers", {}).get("projected", 0)
        subscriber_impact = modified_subs - baseline_subs
        subscriber_impact_percent = (subscriber_impact / max(baseline_subs, 1)) * 100
        
        baseline_views = baseline.get("views", {}).get("projected", 0)
        modified_views = modified_forecast.get("views", {}).get("projected", 0)
        view_impact = modified_views - baseline_views
        view_impact_percent = (view_impact / max(baseline_views, 1)) * 100
        
        return {
            "timestamp": datetime.now().isoformat(),
            "channel_handle": channel_handle,
            "strategy_changes": strategy_changes,
            "forecast_period_days": days_ahead,
            "baseline": baseline,
            "modified": modified_forecast,
            "impact": {
                "subscribers": {
                    "baseline": baseline_subs,
                    "modified": modified_subs,
                    "change": subscriber_impact,
                    "change_percent": subscriber_impact_percent
                },
                "views": {
                    "baseline": baseline_views,
                    "modified": modified_views,
                    "change": view_impact,
                    "change_percent": view_impact_percent
                }
            },
            "recommendations": self._generate_strategy_recommendations(
                strategy_changes,
                subscriber_impact_percent,
                view_impact_percent
            )
        }
    
    def _generate_strategy_recommendations(
        self,
        strategy_changes: Dict[str, Any],
        sub_impact: float,
        view_impact: float
    ) -> List[str]:
        """Generate recommendations based on strategy impact."""
        recommendations = []
        
        if sub_impact > 10:
            recommendations.append(f"Strategy changes show strong positive impact (+{sub_impact:.1f}% subscribers). Consider implementing these changes.")
        elif sub_impact < -5:
            recommendations.append(f"Strategy changes show negative impact ({sub_impact:.1f}% subscribers). Review and adjust approach.")
        
        if "upload_frequency" in strategy_changes:
            freq = strategy_changes["upload_frequency"]
            if freq > 2:
                recommendations.append(f"Increasing upload frequency to {freq} videos/week could significantly boost growth. Ensure quality is maintained.")
        
        if "ctr_improvement" in strategy_changes:
            ctr = strategy_changes["ctr_improvement"]
            recommendations.append(f"Improving CTR by {ctr*100:.0f}% through better thumbnails and titles could increase views by {view_impact:.0f}%.")
        
        return recommendations

