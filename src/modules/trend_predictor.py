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
        predictions = self._predict_future_trends(recent_trends, days_ahead, niche)
        
        # Generate recommendations
        recommendations = self._generate_trend_recommendations(predictions, niche)
        
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
        
        # Extract niche words for theme detection
        niche_words = niche.lower().split()
        
        for result in recent_results:
            title = result["snippet"]["title"].lower()
            words = [w for w in title.split() if len(w) > 4]
            trending_words.extend(words)
            
            # Extract themes based on niche and common patterns
            # Check for niche-specific themes
            for niche_word in niche_words:
                if niche_word in title and len(niche_word) > 3:
                    trending_themes.append(niche_word)
            
            # Common content patterns (dynamic based on what appears in titles)
            common_patterns = {
                "cover": "covers",
                "mix": "mixes",
                "remix": "remixes",
                "live": "live performances",
                "original": "original content"
            }
            
            for pattern, theme in common_patterns.items():
                if pattern in title:
                    trending_themes.append(theme)
            
            # Decade/year patterns
            if any(decade in title for decade in ["70s", "80s", "90s", "2000s", "2010s", "2020s"]):
                trending_themes.append("retro/vintage")
        
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
        days_ahead: int,
        niche: str = ""
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
                "recommended_action": f"Consider creating {niche} content around '{keyword_data['word']}'"
            })
        
        # Predict theme trends
        for theme_data in trending_themes[:3]:
            predictions.append({
                "theme": theme_data["theme"],
                "trend_direction": "Stable",
                "confidence": "High",
                "recommended_action": f"Continue focusing on {theme_data['theme']} {niche} content"
            })
        
        return predictions
    
    def _generate_trend_recommendations(
        self,
        predictions: List[Dict[str, Any]],
        niche: str = ""
    ) -> List[str]:
        """Generate actionable recommendations from predictions."""
        recommendations = []
        
        if predictions:
            top_keyword = predictions[0].get("keyword", "")
            if top_keyword:
                recommendations.append(
                    f"Focus on '{top_keyword}' - it's trending upward in your niche"
                )
        
        # Extract themes from predictions
        themes = []
        for pred in predictions[:3]:
            theme = pred.get("theme", "")
            if theme:
                themes.append(theme)
        
        # Generate niche-specific recommendations
        niche_title = " ".join(word.capitalize() for word in niche.split()) if niche else "your niche"
        
        recommendations.extend([
            f"Monitor competitor channels in {niche_title} for emerging trends",
            f"Create content around trending {niche_title.lower()} themes" + (f" ({', '.join(themes[:3])})" if themes else ""),
            f"Use trending keywords in {niche_title.lower()} titles and descriptions",
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
        channel_id: str,
        timezone: str = "UTC+3",
        analyze_historical: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze best posting times based on channel data with enhanced features.
        
        Args:
            channel_id: Channel ID to analyze
            timezone: Timezone (e.g., "UTC+3", "America/New_York")
            analyze_historical: Whether to analyze historical video performance
        
        Returns:
            Enhanced best posting times analysis
        """
        # Get channel videos for historical analysis
        historical_data = None
        if analyze_historical:
            try:
                videos = self.client.get_channel_videos(channel_id, max_results=50)
                if videos:
                    historical_data = self._analyze_historical_posting_times(videos, timezone)
            except:
                pass
        
        # Base best times (can be overridden by historical data)
        # Best times for Turkish audience (UTC+3) by default
        # Peak hours: 19:00-22:00 local time
        base_best_times = {
            "monday": ["19:00", "20:00", "21:00"],
            "tuesday": ["19:00", "20:00", "21:00"],
            "wednesday": ["19:00", "20:00", "21:00"],
            "thursday": ["19:00", "20:00", "21:00"],
            "friday": ["18:00", "19:00", "20:00", "21:00", "22:00"],
            "saturday": ["14:00", "15:00", "16:00", "19:00", "20:00", "21:00"],
            "sunday": ["14:00", "15:00", "16:00", "19:00", "20:00", "21:00"]
        }
        
        # Use historical data if available
        if historical_data and historical_data.get("optimal_times"):
            best_times = historical_data["optimal_times"]
        else:
            best_times = base_best_times
        
        # Analyze target audience activity
        audience_activity = self._analyze_audience_activity(timezone, historical_data)
        
        # Calculate next optimal post time with timezone support
        next_optimal = self._calculate_next_optimal_time_enhanced(timezone, best_times)
        
        # Generate timezone-aware recommendations
        recommendations = self._generate_timezone_recommendations(
            best_times, timezone, historical_data, audience_activity
        )
        
        return {
            "best_times": best_times,
            "timezone": timezone,
            "timezone_offset": self._get_timezone_offset(timezone),
            "historical_analysis": historical_data,
            "audience_activity": audience_activity,
            "recommendations": recommendations,
            "next_optimal_post": next_optimal,
            "weekly_schedule": self._generate_weekly_schedule(best_times, timezone)
        }
    
    def _calculate_next_optimal_time(self) -> Dict[str, Any]:
        """Calculate the next optimal posting time (legacy method)."""
        return self._calculate_next_optimal_time_enhanced("UTC+3", {
            "monday": ["19:00"], "tuesday": ["19:00"], "wednesday": ["19:00"],
            "thursday": ["19:00"], "friday": ["19:00"], "saturday": ["19:00"], "sunday": ["19:00"]
        })
    
    def _calculate_next_optimal_time_enhanced(
        self,
        timezone: str,
        best_times: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Calculate the next optimal posting time with timezone support."""
        now = datetime.now()
        current_day = now.strftime("%A").lower()
        current_hour = now.hour
        
        # Get best times for today
        today_best_times = best_times.get(current_day, ["19:00"])
        
        # Find next optimal time today
        next_time_today = None
        for time_str in today_best_times:
            hour = int(time_str.split(":")[0])
            if hour > current_hour:
                next_time_today = hour
                break
        
        if next_time_today:
            next_post = now.replace(hour=next_time_today, minute=0, second=0, microsecond=0)
            reason = f"Post today at {next_time_today:02d}:00 - optimal time for your audience."
        else:
            # Find next day with optimal times
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            current_idx = days.index(current_day)
            
            for i in range(1, 8):
                next_day_idx = (current_idx + i) % 7
                next_day = days[next_day_idx]
                if best_times.get(next_day):
                    next_time_str = best_times[next_day][0]
                    next_hour = int(next_time_str.split(":")[0])
                    next_post = now + timedelta(days=i)
                    next_post = next_post.replace(hour=next_hour, minute=0, second=0, microsecond=0)
                    reason = f"Post on {next_day.capitalize()} at {next_time_str} - next optimal posting window."
                    break
            else:
                # Fallback
                next_post = now + timedelta(days=1)
                next_post = next_post.replace(hour=19, minute=0, second=0, microsecond=0)
                reason = "Post tomorrow at 19:00 - general optimal time."
        
        return {
            "date": next_post.strftime("%Y-%m-%d"),
            "time": next_post.strftime("%H:%M"),
            "day": next_post.strftime("%A"),
            "timezone": timezone,
            "reason": reason
        }
    
    def _analyze_historical_posting_times(
        self,
        videos: List[Dict[str, Any]],
        timezone: str
    ) -> Optional[Dict[str, Any]]:
        """Analyze historical video posting times to learn optimal times."""
        if not videos:
            return None
        
        # Group videos by day of week and hour
        day_hour_performance = {}
        
        for video in videos:
            pub_date_str = video["snippet"].get("publishedAt", "")
            if not pub_date_str:
                continue
            
            try:
                pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                day = pub_date.strftime("%A").lower()
                hour = pub_date.hour
                
                stats = video.get("statistics", {})
                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0))
                engagement = views + likes * 10  # Weighted engagement score
                
                key = f"{day}_{hour}"
                if key not in day_hour_performance:
                    day_hour_performance[key] = {
                        "count": 0,
                        "total_views": 0,
                        "total_engagement": 0
                    }
                
                day_hour_performance[key]["count"] += 1
                day_hour_performance[key]["total_views"] += views
                day_hour_performance[key]["total_engagement"] += engagement
            except:
                continue
        
        # Calculate average performance per day/hour
        avg_performance = {}
        for key, data in day_hour_performance.items():
            if data["count"] > 0:
                avg_performance[key] = {
                    "avg_views": data["total_views"] / data["count"],
                    "avg_engagement": data["total_engagement"] / data["count"],
                    "video_count": data["count"]
                }
        
        # Find optimal times (top performing hours per day)
        optimal_times = {}
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
        for day in days:
            day_performances = {
                k: v for k, v in avg_performance.items()
                if k.startswith(day + "_")
            }
            
            if day_performances:
                # Sort by engagement
                sorted_performances = sorted(
                    day_performances.items(),
                    key=lambda x: x[1]["avg_engagement"],
                    reverse=True
                )
                
                # Get top 3 hours
                top_hours = []
                for key, perf in sorted_performances[:3]:
                    hour = int(key.split("_")[1])
                    top_hours.append(f"{hour:02d}:00")
                
                if top_hours:
                    optimal_times[day] = top_hours
        
        return {
            "videos_analyzed": len(videos),
            "optimal_times": optimal_times if optimal_times else None,
            "performance_data": avg_performance,
            "insights": self._generate_historical_insights(avg_performance)
        }
    
    def _generate_historical_insights(
        self,
        performance_data: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """Generate insights from historical performance data."""
        insights = []
        
        if not performance_data:
            return ["No historical data available. Use general best practices."]
        
        # Find best performing day/hour
        best_performance = max(
            performance_data.items(),
            key=lambda x: x[1].get("avg_engagement", 0)
        ) if performance_data else None
        
        if best_performance:
            day_hour = best_performance[0]
            day, hour = day_hour.split("_")
            insights.append(
                f"Your best performing time is {day.capitalize()} at {hour}:00 "
                f"(avg {best_performance[1].get('avg_views', 0):.0f} views)"
            )
        
        return insights
    
    def _analyze_audience_activity(
        self,
        timezone: str,
        historical_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze target audience activity patterns."""
        # General activity patterns by timezone
        timezone_patterns = {
            "UTC+3": {  # Turkey, Middle East
                "peak_hours": ["19:00", "20:00", "21:00"],
                "secondary_hours": ["14:00", "15:00", "16:00"],
                "low_activity": ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00"]
            },
            "UTC+0": {  # UK, Portugal
                "peak_hours": ["18:00", "19:00", "20:00"],
                "secondary_hours": ["12:00", "13:00", "14:00"],
                "low_activity": ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00"]
            },
            "UTC-5": {  # US Eastern
                "peak_hours": ["19:00", "20:00", "21:00"],
                "secondary_hours": ["12:00", "13:00", "14:00"],
                "low_activity": ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00"]
            }
        }
        
        pattern = timezone_patterns.get(timezone, timezone_patterns["UTC+3"])
        
        return {
            "timezone": timezone,
            "peak_hours": pattern["peak_hours"],
            "secondary_hours": pattern["secondary_hours"],
            "low_activity_hours": pattern["low_activity"],
            "recommendation": f"Post during peak hours ({', '.join(pattern['peak_hours'])}) for maximum reach in {timezone} timezone."
        }
    
    def _get_timezone_offset(self, timezone: str) -> int:
        """Get timezone offset in hours."""
        # Simple timezone offset mapping
        offsets = {
            "UTC+3": 3,
            "UTC+0": 0,
            "UTC-5": -5,
            "UTC-8": -8,
            "UTC+1": 1,
            "UTC+2": 2
        }
        
        # Try to extract from format like "UTC+3" or "UTC-5"
        if timezone.startswith("UTC"):
            try:
                offset_str = timezone[3:]
                return int(offset_str)
            except:
                pass
        
        return offsets.get(timezone, 3)  # Default to UTC+3
    
    def _generate_timezone_recommendations(
        self,
        best_times: Dict[str, List[str]],
        timezone: str,
        historical_data: Optional[Dict[str, Any]],
        audience_activity: Dict[str, Any]
    ) -> List[str]:
        """Generate timezone-aware recommendations."""
        recommendations = []
        
        # Historical data recommendations
        if historical_data and historical_data.get("insights"):
            recommendations.extend(historical_data["insights"])
        
        # Audience activity recommendations
        peak_hours = audience_activity.get("peak_hours", [])
        if peak_hours:
            recommendations.append(
                f"Post during peak hours ({', '.join(peak_hours)}) in {timezone} timezone for maximum audience reach."
            )
        
        # General recommendations
        recommendations.extend([
            f"Schedule posts in {timezone} timezone for your target audience.",
            "Weekend afternoons often have higher engagement for entertainment content.",
            "Avoid posting during low-activity hours (midnight to 6 AM).",
            "Test different posting times and analyze performance to find your optimal schedule."
        ])
        
        return recommendations
    
    def _generate_weekly_schedule(
        self,
        best_times: Dict[str, List[str]],
        timezone: str
    ) -> List[Dict[str, Any]]:
        """Generate a weekly posting schedule."""
        schedule = []
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
        for day in days:
            times = best_times.get(day, [])
            schedule.append({
                "day": day.capitalize(),
                "optimal_times": times,
                "timezone": timezone,
                "recommended": len(times) > 0
            })
        
        return schedule

