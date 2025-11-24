"""
Feedback Learning System Module
Learns from user feedback and recommendation performance.

AGI Paradigm: Feedback Learning System
- Learns from user feedback
- Tracks successful/failed recommendations
- Correlates video performance with recommendation success
- Updates algorithms based on learned patterns
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.performance_tracker import PerformanceTracker


class FeedbackLearner:
    """
    Feedback learning system that learns from user actions and video performance.
    
    AGI Paradigm: Feedback Learning System
    - Learns which recommendations are accepted/rejected
    - Correlates recommendations with video performance
    - Identifies patterns in successful strategies
    - Updates recommendation algorithms based on feedback
    """
    
    DATA_FILE = "data/feedback_history.json"
    
    def __init__(self, client: YouTubeClient, performance_tracker: PerformanceTracker):
        self.client = client
        self.performance_tracker = performance_tracker
        self._ensure_data_dir()
        self._load_feedback()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
    
    def _load_feedback(self) -> Dict[str, Any]:
        """Load feedback history from file."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "feedback_entries": [],
            "learned_patterns": {},
            "correlation_analysis": {},
            "algorithm_updates": []
        }
    
    def _save_feedback(self, data: Dict[str, Any]):
        """Save feedback history to file."""
        try:
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving feedback: {e}")
    
    def record_feedback(
        self,
        recommendation_id: str,
        feedback_type: str,
        feedback_data: Dict[str, Any],
        video_id: Optional[str] = None
    ):
        """
        Record user feedback on a recommendation.
        
        Args:
            recommendation_id: ID of the recommendation
            feedback_type: Type of feedback (accepted, rejected, modified, applied)
            feedback_data: Additional feedback data
            video_id: Optional video ID if feedback is for a specific video
        """
        feedback = self._load_feedback()
        
        entry = {
            "recommendation_id": recommendation_id,
            "feedback_type": feedback_type,
            "feedback_data": feedback_data,
            "video_id": video_id,
            "timestamp": datetime.now().isoformat(),
            "user_notes": feedback_data.get("notes", ""),
            "rating": feedback_data.get("rating", None)  # 1-5 scale
        }
        
        feedback["feedback_entries"].append(entry)
        
        # Keep only last 1000 entries
        if len(feedback["feedback_entries"]) > 1000:
            feedback["feedback_entries"] = feedback["feedback_entries"][-1000:]
        
        self._save_feedback(feedback)
        
        # Update performance tracker
        status_map = {
            "accepted": "applied",
            "rejected": "rejected",
            "modified": "applied",
            "applied": "applied"
        }
        self.performance_tracker.update_recommendation_status(
            recommendation_id,
            status_map.get(feedback_type, "pending"),
            feedback_data
        )
    
    def correlate_with_performance(
        self,
        recommendation_id: str,
        video_id: Optional[str] = None,
        days_after: int = 7
    ) -> Dict[str, Any]:
        """
        Correlate recommendation with video performance.
        
        Args:
            recommendation_id: ID of recommendation
            video_id: Video ID to check performance
            days_after: Days after recommendation to check performance
            
        Returns:
            Correlation analysis
        """
        feedback = self._load_feedback()
        
        # Find feedback entry
        entry = next(
            (e for e in feedback["feedback_entries"] 
             if e.get("recommendation_id") == recommendation_id),
            None
        )
        
        if not entry:
            return {
                "status": "no_feedback",
                "message": "No feedback found for this recommendation"
            }
        
        # Get video performance if video_id provided
        performance_data = None
        if video_id:
            try:
                videos = self.client.get_videos_details([video_id])
                if videos:
                    video = videos[0]
                    stats = video.get("statistics", {})
                    performance_data = {
                        "views": int(stats.get("viewCount", 0)),
                        "likes": int(stats.get("likeCount", 0)),
                        "comments": int(stats.get("commentCount", 0)),
                        "subscriber_gain": None  # Would need historical data
                    }
            except Exception:
                pass
        
        # Get recommendation from performance tracker
        history = self.performance_tracker._load_history()
        recommendation = history.get("recommendations", {}).get(recommendation_id, {})
        
        correlation = {
            "recommendation_id": recommendation_id,
            "feedback_type": entry.get("feedback_type"),
            "feedback_rating": entry.get("rating"),
            "recommendation_type": recommendation.get("type"),
            "recommendation_data": recommendation.get("data"),
            "video_performance": performance_data,
            "correlation_score": self._calculate_correlation_score(entry, performance_data),
            "timestamp": entry.get("timestamp")
        }
        
        return correlation
    
    def _calculate_correlation_score(
        self,
        feedback_entry: Dict[str, Any],
        performance_data: Optional[Dict[str, Any]]
    ) -> float:
        """Calculate correlation score between feedback and performance."""
        score = 0.0
        
        # Base score from feedback type
        feedback_type = feedback_entry.get("feedback_type", "")
        if feedback_type == "accepted" or feedback_type == "applied":
            score += 0.5
        elif feedback_type == "rejected":
            score -= 0.3
        elif feedback_type == "modified":
            score += 0.2
        
        # Rating impact
        rating = feedback_entry.get("rating")
        if rating:
            score += (rating - 3) * 0.1  # -0.2 to +0.2
        
        # Performance impact (if available)
        if performance_data:
            views = performance_data.get("views", 0)
            if views > 1000:
                score += 0.2
            elif views > 500:
                score += 0.1
            
            engagement = (
                performance_data.get("likes", 0) + 
                performance_data.get("comments", 0)
            ) / max(views, 1)
            if engagement > 0.05:  # 5% engagement
                score += 0.1
        
        return min(max(score, -1.0), 1.0)  # Clamp between -1 and 1
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """
        Analyze patterns from all feedback to learn what works.
        
        Returns:
            Learned patterns and insights
        """
        feedback = self._load_feedback()
        entries = feedback.get("feedback_entries", [])
        
        if not entries:
            return {
                "status": "no_data",
                "message": "No feedback data available yet"
            }
        
        # Group by recommendation type
        by_type = {}
        by_feedback_type = {}
        successful_combinations = []
        
        for entry in entries:
            rec_id = entry.get("recommendation_id")
            feedback_type = entry.get("feedback_type")
            rating = entry.get("rating")
            
            # Get recommendation details
            history = self.performance_tracker._load_history()
            recommendation = history.get("recommendations", {}).get(rec_id, {})
            rec_type = recommendation.get("type", "unknown")
            
            # Group by type
            if rec_type not in by_type:
                by_type[rec_type] = {
                    "total": 0,
                    "accepted": 0,
                    "rejected": 0,
                    "average_rating": 0,
                    "ratings": []
                }
            
            by_type[rec_type]["total"] += 1
            if feedback_type in ["accepted", "applied"]:
                by_type[rec_type]["accepted"] += 1
            elif feedback_type == "rejected":
                by_type[rec_type]["rejected"] += 1
            
            if rating:
                by_type[rec_type]["ratings"].append(rating)
            
            # Group by feedback type
            if feedback_type not in by_feedback_type:
                by_feedback_type[feedback_type] = 0
            by_feedback_type[feedback_type] += 1
            
            # Track successful combinations
            if feedback_type in ["accepted", "applied"] and rating and rating >= 4:
                successful_combinations.append({
                    "type": rec_type,
                    "data": recommendation.get("data"),
                    "rating": rating
                })
        
        # Calculate statistics
        type_stats = {}
        for rec_type, stats in by_type.items():
            if stats["total"] > 0:
                acceptance_rate = (stats["accepted"] / stats["total"]) * 100
                avg_rating = sum(stats["ratings"]) / len(stats["ratings"]) if stats["ratings"] else 0
                
                type_stats[rec_type] = {
                    "total_feedback": stats["total"],
                    "acceptance_rate": acceptance_rate,
                    "rejection_rate": (stats["rejected"] / stats["total"]) * 100,
                    "average_rating": avg_rating,
                    "success_score": (acceptance_rate / 100) * 0.7 + (avg_rating / 5) * 0.3
                }
        
        # Identify best patterns
        best_patterns = sorted(
            type_stats.items(),
            key=lambda x: x[1].get("success_score", 0),
            reverse=True
        )[:5]
        
        # Update learned patterns
        feedback["learned_patterns"] = {
            "by_type": type_stats,
            "best_patterns": [{"type": t, "stats": s} for t, s in best_patterns],
            "feedback_distribution": by_feedback_type,
            "successful_combinations": successful_combinations[:10],
            "last_updated": datetime.now().isoformat(),
            "total_feedback_entries": len(entries)
        }
        
        self._save_feedback(feedback)
        
        return {
            "summary": {
                "total_feedback": len(entries),
                "types_analyzed": len(type_stats),
                "best_performing_type": best_patterns[0][0] if best_patterns else None
            },
            "by_type": type_stats,
            "best_patterns": best_patterns,
            "insights": self._generate_insights(type_stats, best_patterns)
        }
    
    def _generate_insights(
        self,
        type_stats: Dict[str, Any],
        best_patterns: List[tuple]
    ) -> List[str]:
        """Generate insights from pattern analysis."""
        insights = []
        
        if not type_stats:
            return ["No data available for insights yet. Start providing feedback to learn patterns."]
        
        # Best performing type
        if best_patterns:
            best_type, best_stats = best_patterns[0]
            success_score = best_stats.get("success_score", 0)
            if success_score > 0.7:
                insights.append(
                    f"✅ {best_type} recommendations are highly successful "
                    f"(success score: {success_score:.2f}). Continue using this approach."
                )
        
        # Worst performing type
        worst_patterns = sorted(
            type_stats.items(),
            key=lambda x: x[1].get("success_score", 1),
            reverse=False
        )
        if worst_patterns:
            worst_type, worst_stats = worst_patterns[0]
            success_score = worst_stats.get("success_score", 0)
            if success_score < 0.4:
                insights.append(
                    f"⚠️ {worst_type} recommendations need improvement "
                    f"(success score: {success_score:.2f}). Review and refine this approach."
                )
        
        # Overall acceptance rate
        total_accepted = sum(s.get("accepted", 0) for s in type_stats.values())
        total_feedback = sum(s.get("total_feedback", 0) for s in type_stats.values())
        overall_acceptance = (total_accepted / max(total_feedback, 1)) * 100
        
        if overall_acceptance > 70:
            insights.append(
                f"🎉 Excellent! Overall acceptance rate is {overall_acceptance:.1f}%. "
                "Your recommendations are well-aligned with user needs."
            )
        elif overall_acceptance < 50:
            insights.append(
                f"📊 Acceptance rate is {overall_acceptance:.1f}%. "
                "Consider improving recommendation quality or better understanding user preferences."
            )
        
        return insights
    
    def get_recommendation_improvements(
        self,
        recommendation_type: str
    ) -> Dict[str, Any]:
        """
        Get improvement suggestions for a specific recommendation type.
        
        Args:
            recommendation_type: Type of recommendation (title, description, tags, etc.)
            
        Returns:
            Improvement suggestions based on learned patterns
        """
        patterns = self.analyze_patterns()
        type_stats = patterns.get("by_type", {}).get(recommendation_type, {})
        
        if not type_stats:
            return {
                "status": "insufficient_data",
                "message": f"Not enough feedback data for {recommendation_type} recommendations yet"
            }
        
        improvements = []
        success_score = type_stats.get("success_score", 0)
        acceptance_rate = type_stats.get("acceptance_rate", 0)
        avg_rating = type_stats.get("average_rating", 0)
        
        if success_score < 0.5:
            improvements.append("Consider different approaches or formats for this recommendation type")
        
        if acceptance_rate < 60:
            improvements.append("Improve recommendation relevance and alignment with user needs")
        
        if avg_rating < 3.5:
            improvements.append("Enhance recommendation quality and usefulness")
        
        # Get successful combinations
        feedback = self._load_feedback()
        learned = feedback.get("learned_patterns", {})
        successful = [
            c for c in learned.get("successful_combinations", [])
            if c.get("type") == recommendation_type
        ]
        
        return {
            "recommendation_type": recommendation_type,
            "current_performance": {
                "success_score": success_score,
                "acceptance_rate": acceptance_rate,
                "average_rating": avg_rating
            },
            "improvements": improvements,
            "successful_examples": successful[:5],
            "recommendations": self._get_specific_improvements(recommendation_type, type_stats)
        }
    
    def _get_specific_improvements(
        self,
        recommendation_type: str,
        stats: Dict[str, Any]
    ) -> List[str]:
        """Get specific improvement recommendations."""
        improvements = []
        
        if recommendation_type == "title":
            if stats.get("acceptance_rate", 0) < 70:
                improvements.append("Focus on creating more compelling, SEO-optimized titles")
                improvements.append("Test different title formats and structures")
        elif recommendation_type == "description":
            if stats.get("acceptance_rate", 0) < 70:
                improvements.append("Improve description templates with better structure")
                improvements.append("Add more relevant keywords and call-to-actions")
        elif recommendation_type == "tags":
            if stats.get("acceptance_rate", 0) < 70:
                improvements.append("Research trending tags in your niche")
                improvements.append("Balance specific and general tags better")
        
        return improvements
    
    def learn_subscriber_growth_patterns(self) -> Dict[str, Any]:
        """
        Learn which recommendation patterns lead to subscriber growth.
        
        Returns:
            Patterns that correlate with subscriber growth
        """
        feedback = self._load_feedback()
        entries = feedback.get("feedback_entries", [])
        
        # Get channel snapshots to track subscriber growth
        history = self.performance_tracker._load_history()
        snapshots = history.get("snapshots", [])
        
        if len(snapshots) < 2:
            return {
                "status": "insufficient_data",
                "message": "Need at least 2 snapshots to analyze subscriber growth patterns"
            }
        
        # Analyze which recommendations were applied before subscriber growth
        growth_periods = []
        for i in range(1, len(snapshots)):
            prev = snapshots[i-1]
            curr = snapshots[i]
            
            subscriber_growth = (
                curr["metrics"]["subscribers"] - 
                prev["metrics"]["subscribers"]
            )
            
            if subscriber_growth > 0:
                # Find recommendations applied in this period
                period_start = datetime.fromisoformat(prev["timestamp"])
                period_end = datetime.fromisoformat(curr["timestamp"])
                
                applied_recommendations = []
                for entry in entries:
                    entry_time = datetime.fromisoformat(entry["timestamp"])
                    if period_start <= entry_time <= period_end:
                        if entry.get("feedback_type") in ["accepted", "applied"]:
                            rec_id = entry.get("recommendation_id")
                            rec = history.get("recommendations", {}).get(rec_id, {})
                            if rec:
                                applied_recommendations.append({
                                    "type": rec.get("type"),
                                    "data": rec.get("data")
                                })
                
                if applied_recommendations:
                    growth_periods.append({
                        "period": f"{prev['timestamp']} to {curr['timestamp']}",
                        "subscriber_growth": subscriber_growth,
                        "recommendations": applied_recommendations
                    })
        
        # Identify patterns
        pattern_counts = {}
        for period in growth_periods:
            for rec in period["recommendations"]:
                rec_type = rec.get("type", "unknown")
                if rec_type not in pattern_counts:
                    pattern_counts[rec_type] = {
                        "count": 0,
                        "total_growth": 0,
                        "periods": []
                    }
                pattern_counts[rec_type]["count"] += 1
                pattern_counts[rec_type]["total_growth"] += period["subscriber_growth"]
                pattern_counts[rec_type]["periods"].append(period["subscriber_growth"])
        
        # Calculate average growth per recommendation type
        growth_patterns = {}
        for rec_type, data in pattern_counts.items():
            avg_growth = data["total_growth"] / max(data["count"], 1)
            growth_patterns[rec_type] = {
                "times_used": data["count"],
                "average_subscriber_growth": avg_growth,
                "total_growth": data["total_growth"],
                "growth_per_period": data["periods"]
            }
        
        # Sort by average growth
        best_growth_patterns = sorted(
            growth_patterns.items(),
            key=lambda x: x[1].get("average_subscriber_growth", 0),
            reverse=True
        )
        
        return {
            "growth_periods_analyzed": len(growth_periods),
            "patterns_identified": len(growth_patterns),
            "best_growth_patterns": [
                {"type": t, "stats": s} for t, s in best_growth_patterns[:5]
            ],
            "insights": self._generate_growth_insights(best_growth_patterns)
        }
    
    def _generate_growth_insights(self, patterns: List[tuple]) -> List[str]:
        """Generate insights about subscriber growth patterns."""
        insights = []
        
        if not patterns:
            return ["No growth patterns identified yet. Continue applying recommendations and tracking performance."]
        
        best_type, best_stats = patterns[0]
        avg_growth = best_stats.get("average_subscriber_growth", 0)
        
        if avg_growth > 5:
            insights.append(
                f"🚀 {best_type} recommendations are highly effective for subscriber growth "
                f"(avg: {avg_growth:.1f} subscribers per application). "
                "Prioritize this type of recommendation."
            )
        elif avg_growth > 1:
            insights.append(
                f"✅ {best_type} recommendations show positive subscriber growth "
                f"(avg: {avg_growth:.1f} subscribers). Continue using this approach."
            )
        
        return insights

