"""
Code Self-Improvement Module
Optimizes algorithms based on performance metrics and learned patterns.

AGI Paradigm: Code Self-Improvement
- Optimizes algorithm parameters based on performance
- Updates code based on discovered patterns
- Measures and tracks improvements
- Self-evolving architecture
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
import copy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.performance_tracker import PerformanceTracker
from src.modules.feedback_learner import FeedbackLearner
from src.modules.knowledge_graph import KnowledgeGraph
from src.modules.viral_predictor import ViralPredictor


class CodeSelfImprover:
    """
    Self-improving code optimizer.
    
    AGI Paradigm: Code Self-Improvement
    - Optimizes algorithm parameters based on performance metrics
    - Updates weights and thresholds based on learned patterns
    - Tracks measurable improvements
    - Suggests code updates based on discoveries
    """
    
    DATA_FILE = "data/code_improvements.json"
    CONFIG_FILE = "data/optimized_config.json"
    
    def __init__(
        self,
        client: YouTubeClient,
        performance_tracker: PerformanceTracker,
        feedback_learner: FeedbackLearner,
        knowledge_graph: KnowledgeGraph,
        viral_predictor: ViralPredictor
    ):
        self.client = client
        self.performance_tracker = performance_tracker
        self.feedback_learner = feedback_learner
        self.knowledge_graph = knowledge_graph
        self.viral_predictor = viral_predictor
        self._ensure_data_dir()
        self._load_improvements()
        self._load_optimized_config()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
    
    def _load_improvements(self) -> Dict[str, Any]:
        """Load code improvement history."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "improvements": [],
            "optimizations": {},
            "performance_baseline": {},
            "improvement_history": []
        }
    
    def _save_improvements(self, data: Dict[str, Any]):
        """Save code improvement history."""
        try:
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving improvements: {e}")
    
    def _load_optimized_config(self) -> Dict[str, Any]:
        """Load optimized configuration."""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "viral_predictor_weights": {},
            "algorithm_parameters": {},
            "thresholds": {},
            "last_optimized": None
        }
    
    def _save_optimized_config(self, config: Dict[str, Any]):
        """Save optimized configuration."""
        try:
            config["last_optimized"] = datetime.now().isoformat()
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def optimize_viral_predictor_weights(self) -> Dict[str, Any]:
        """
        Optimize viral predictor indicator weights based on actual performance.
        
        Returns:
            Optimization results with new weights
        """
        # Get feedback patterns
        try:
            patterns = self.feedback_learner.analyze_patterns()
            feedback_data = patterns.get("by_type", {})
        except Exception:
            feedback_data = {}
        
        # Get knowledge graph patterns
        try:
            kg_patterns = self.knowledge_graph.get_subscriber_growth_patterns()
            growth_patterns = kg_patterns.get("patterns", {})
        except Exception:
            growth_patterns = {}
        
        # Current weights
        current_weights = copy.deepcopy(self.viral_predictor.VIRAL_INDICATORS)
        
        # Analyze which indicators correlate with success
        # This is a simplified optimization - in production, use more sophisticated methods
        
        # Optimize based on feedback
        optimized_weights = copy.deepcopy(current_weights)
        
        # If title recommendations are successful, increase title_clickability weight
        title_feedback = feedback_data.get("title", {})
        if title_feedback and title_feedback.get("success_score", 0) > 0.7:
            optimized_weights["title_clickability"] = min(
                current_weights["title_clickability"] * 1.2,
                0.25
            )
        
        # If timing is important (from patterns), increase timing weight
        timing_patterns = growth_patterns.get("timing_patterns", {})
        if timing_patterns.get("best_hour") is not None:
            optimized_weights["timing"] = min(
                current_weights["timing"] * 1.15,
                0.25
            )
        
        # Normalize weights to sum to 1.0
        total = sum(optimized_weights.values())
        if total > 0:
            optimized_weights = {k: v / total for k, v in optimized_weights.items()}
        
        # Calculate improvement
        improvement = self._calculate_weight_improvement(current_weights, optimized_weights)
        
        # Save optimization
        config = self._load_optimized_config()
        config["viral_predictor_weights"] = optimized_weights
        self._save_optimized_config(config)
        
        # Record improvement
        improvement_record = {
            "timestamp": datetime.now().isoformat(),
            "module": "viral_predictor",
            "optimization_type": "weight_optimization",
            "before": current_weights,
            "after": optimized_weights,
            "improvement_score": improvement,
            "reason": "Optimized based on feedback patterns and growth patterns"
        }
        
        data = self._load_improvements()
        data["improvements"].append(improvement_record)
        if len(data["improvements"]) > 100:
            data["improvements"] = data["improvements"][-100:]
        self._save_improvements(data)
        
        return {
            "status": "optimized",
            "module": "viral_predictor",
            "before": current_weights,
            "after": optimized_weights,
            "improvement_score": improvement,
            "changes": self._get_weight_changes(current_weights, optimized_weights)
        }
    
    def _calculate_weight_improvement(
        self,
        before: Dict[str, float],
        after: Dict[str, float]
    ) -> float:
        """Calculate improvement score for weight changes."""
        # Simple metric: sum of absolute changes
        total_change = sum(abs(after.get(k, 0) - before.get(k, 0)) for k in before.keys())
        return total_change
    
    def _get_weight_changes(
        self,
        before: Dict[str, float],
        after: Dict[str, float]
    ) -> Dict[str, Dict[str, float]]:
        """Get detailed weight changes."""
        changes = {}
        for key in before.keys():
            old_val = before.get(key, 0)
            new_val = after.get(key, 0)
            change = new_val - old_val
            change_percent = (change / old_val * 100) if old_val > 0 else 0
            
            changes[key] = {
                "before": old_val,
                "after": new_val,
                "change": change,
                "change_percent": change_percent
            }
        return changes
    
    def optimize_algorithm_parameters(self) -> Dict[str, Any]:
        """
        Optimize algorithm parameters across all modules.
        
        Returns:
            Optimization results
        """
        optimizations = {}
        
        # 1. Optimize title length thresholds
        try:
            patterns = self.knowledge_graph.get_subscriber_growth_patterns()
            title_patterns = patterns.get("patterns", {}).get("title_patterns", {})
            
            if title_patterns.get("average_length"):
                optimal_length = title_patterns["average_length"]
                optimizations["title_length"] = {
                    "optimal_min": max(optimal_length - 10, 30),
                    "optimal_max": min(optimal_length + 10, 70),
                    "optimal_target": optimal_length,
                    "reason": "Based on successful video title patterns"
                }
        except Exception as e:
            optimizations["title_length"] = {"error": str(e)}
        
        # 2. Optimize engagement thresholds
        try:
            perf_history = self.performance_tracker._load_history()
            snapshots = perf_history.get("snapshots", [])
            
            if len(snapshots) >= 2:
                # Calculate average engagement from snapshots
                engagement_rates = []
                for snapshot in snapshots[-10:]:  # Last 10 snapshots
                    videos = snapshot.get("recent_videos", [])
                    for video in videos:
                        views = video.get("views", 0)
                        likes = video.get("likes", 0)
                        comments = video.get("comments", 0)
                        if views > 0:
                            engagement = ((likes + comments) / views) * 100
                            engagement_rates.append(engagement)
                
                if engagement_rates:
                    avg_engagement = sum(engagement_rates) / len(engagement_rates)
                    optimizations["engagement_threshold"] = {
                        "low_threshold": avg_engagement * 0.7,
                        "medium_threshold": avg_engagement,
                        "high_threshold": avg_engagement * 1.5,
                        "reason": "Based on actual engagement data"
                    }
        except Exception as e:
            optimizations["engagement_threshold"] = {"error": str(e)}
        
        # 3. Optimize posting time
        try:
            patterns = self.knowledge_graph.get_subscriber_growth_patterns()
            timing_patterns = patterns.get("patterns", {}).get("timing_patterns", {})
            
            if timing_patterns.get("best_hour") is not None:
                optimizations["posting_time"] = {
                    "best_hour": timing_patterns["best_hour"],
                    "best_day": timing_patterns.get("best_day"),
                    "reason": "Based on successful video posting patterns"
                }
        except Exception as e:
            optimizations["posting_time"] = {"error": str(e)}
        
        # Save optimizations
        config = self._load_optimized_config()
        config["algorithm_parameters"] = optimizations
        self._save_optimized_config(config)
        
        return {
            "status": "optimized",
            "optimizations": optimizations,
            "timestamp": datetime.now().isoformat()
        }
    
    def suggest_code_updates(self) -> Dict[str, Any]:
        """
        Suggest code updates based on discovered patterns.
        
        Returns:
            Code update suggestions
        """
        suggestions = []
        
        # Analyze patterns for code update opportunities
        try:
            patterns = self.knowledge_graph.get_subscriber_growth_patterns()
            pattern_data = patterns.get("patterns", {})
            
            # Title pattern suggestions
            title_patterns = pattern_data.get("title_patterns", {})
            if title_patterns.get("average_length"):
                current_min = 40  # Assumed current min
                current_max = 60  # Assumed current max
                optimal = title_patterns["average_length"]
                
                if not (current_min <= optimal <= current_max):
                    suggestions.append({
                        "module": "title_optimizer",
                        "type": "threshold_update",
                        "suggestion": f"Update title length validation: {optimal - 10:.0f}-{optimal + 10:.0f} characters",
                        "current": f"{current_min}-{current_max}",
                        "recommended": f"{optimal - 10:.0f}-{optimal + 10:.0f}",
                        "reason": "Based on successful video title patterns",
                        "priority": "medium"
                    })
            
            # Timing pattern suggestions
            timing_patterns = pattern_data.get("timing_patterns", {})
            if timing_patterns.get("best_hour") is not None:
                suggestions.append({
                    "module": "trend_predictor",
                    "type": "default_value_update",
                    "suggestion": f"Update default posting time recommendation to {timing_patterns['best_hour']}:00",
                    "reason": "Based on successful posting time patterns",
                    "priority": "low"
                })
            
            # Tag pattern suggestions
            content_patterns = pattern_data.get("content_patterns", {})
            if content_patterns.get("common_tags"):
                suggestions.append({
                    "module": "tag_suggester",
                    "type": "base_tags_update",
                    "suggestion": f"Add frequently successful tags to base tags: {', '.join(content_patterns['common_tags'][:5])}",
                    "reason": "These tags appear frequently in successful videos",
                    "priority": "medium"
                })
            
        except Exception as e:
            suggestions.append({
                "type": "error",
                "message": f"Error analyzing patterns: {str(e)}"
            })
        
        # Analyze feedback for algorithm improvements
        try:
            patterns = self.feedback_learner.analyze_patterns()
            by_type = patterns.get("by_type", {})
            
            # Find underperforming recommendation types
            for rec_type, stats in by_type.items():
                success_rate = stats.get("success_rate", 0)
                if success_rate < 50:
                    suggestions.append({
                        "module": f"{rec_type}_optimizer",
                        "type": "algorithm_improvement",
                        "suggestion": f"Improve {rec_type} recommendation algorithm (current success rate: {success_rate:.1f}%)",
                        "reason": f"Low success rate indicates algorithm needs improvement",
                        "priority": "high"
                    })
        except Exception as e:
            pass
        
        return {
            "suggestions_count": len(suggestions),
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        }
    
    def measure_improvement(self, days: int = 7) -> Dict[str, Any]:
        """
        Measure improvement in algorithm performance.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Improvement metrics
        """
        # Get baseline performance
        data = self._load_improvements()
        baseline = data.get("performance_baseline", {})
        
        # Get current performance
        try:
            growth_trend = self.performance_tracker.analyze_growth_trend("anatolianturkishrock", days=days)
            current_performance = {
                "daily_growth": growth_trend.get("growth", {}).get("subscribers", {}).get("daily_average", 0),
                "conversion_rate": growth_trend.get("metrics", {}).get("conversion_rate_percent", 0)
            }
        except Exception:
            current_performance = {}
        
        # Get feedback success rate
        try:
            patterns = self.feedback_learner.analyze_patterns()
            current_success_rate = patterns.get("summary", {}).get("success_rate", 0)
        except Exception:
            current_success_rate = 0
        
        # Calculate improvements
        improvements = {}
        
        if baseline.get("daily_growth") and current_performance.get("daily_growth"):
            growth_improvement = (
                (current_performance["daily_growth"] - baseline["daily_growth"]) /
                max(baseline["daily_growth"], 1)
            ) * 100
            improvements["daily_growth"] = {
                "baseline": baseline["daily_growth"],
                "current": current_performance["daily_growth"],
                "improvement_percent": growth_improvement
            }
        
        if baseline.get("success_rate") and current_success_rate:
            success_improvement = current_success_rate - baseline["success_rate"]
            improvements["success_rate"] = {
                "baseline": baseline["success_rate"],
                "current": current_success_rate,
                "improvement_percent": success_improvement
            }
        
        return {
            "baseline": baseline,
            "current": {
                **current_performance,
                "success_rate": current_success_rate
            },
            "improvements": improvements,
            "overall_improvement": self._calculate_overall_improvement(improvements)
        }
    
    def _calculate_overall_improvement(self, improvements: Dict[str, Any]) -> float:
        """Calculate overall improvement score."""
        if not improvements:
            return 0.0
        
        scores = []
        for key, data in improvements.items():
            improvement = data.get("improvement_percent", 0)
            scores.append(improvement)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def set_performance_baseline(self) -> Dict[str, Any]:
        """
        Set current performance as baseline for future comparisons.
        
        Returns:
            Baseline data
        """
        try:
            # Get current metrics
            growth_trend = self.performance_tracker.analyze_growth_trend("anatolianturkishrock", days=7)
            patterns = self.feedback_learner.analyze_patterns()
            
            baseline = {
                "timestamp": datetime.now().isoformat(),
                "daily_growth": growth_trend.get("growth", {}).get("subscribers", {}).get("daily_average", 0),
                "conversion_rate": growth_trend.get("metrics", {}).get("conversion_rate_percent", 0),
                "success_rate": patterns.get("summary", {}).get("success_rate", 0),
                "subscribers": self.client.get_channel_by_handle("anatolianturkishrock")["items"][0]["statistics"].get("subscriberCount", 0)
            }
            
            # Save baseline
            data = self._load_improvements()
            data["performance_baseline"] = baseline
            self._save_improvements(data)
            
            return {
                "status": "baseline_set",
                "baseline": baseline
            }
        except Exception as e:
            return {"error": str(e)}
    
    def apply_optimizations(self) -> Dict[str, Any]:
        """
        Apply optimized configurations to modules.
        
        Returns:
            Application results
        """
        config = self._load_optimized_config()
        applied = []
        errors = []
        
        # Apply viral predictor weights
        viral_weights = config.get("viral_predictor_weights", {})
        if viral_weights:
            try:
                # Update viral predictor weights
                self.viral_predictor.VIRAL_INDICATORS.update(viral_weights)
                applied.append({
                    "module": "viral_predictor",
                    "optimization": "weights",
                    "status": "applied"
                })
            except Exception as e:
                errors.append({
                    "module": "viral_predictor",
                    "error": str(e)
                })
        
        return {
            "applied_count": len(applied),
            "applied": applied,
            "errors": errors,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_optimization_history(self) -> Dict[str, Any]:
        """Get history of all optimizations."""
        data = self._load_improvements()
        config = self._load_optimized_config()
        
        return {
            "total_improvements": len(data.get("improvements", [])),
            "recent_improvements": data.get("improvements", [])[-10:],
            "current_config": config,
            "performance_baseline": data.get("performance_baseline", {})
        }

