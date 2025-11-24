"""
Continuous Learning Loop Module
Runs 24/7 to continuously learn and discover new trends.

AGI Paradigm: Continuous Learning Mechanism
- Runs 24/7, learning, updating, expanding
- Automatically discovers new trends
- Generates daily/weekly learning reports
- Provides A/B test recommendations
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
import threading
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.performance_tracker import PerformanceTracker
from src.modules.feedback_learner import FeedbackLearner
from src.modules.multi_source_integrator import MultiSourceIntegrator
from src.modules.knowledge_graph import KnowledgeGraph
from src.modules.trend_predictor import TrendPredictor


class ContinuousLearner:
    """
    Continuous learning loop that runs 24/7.
    
    AGI Paradigm: Continuous Learning Mechanism
    - Runs continuously in background
    - Discovers new trends automatically
    - Generates learning reports
    - Provides A/B test recommendations
    """
    
    DATA_FILE = "data/continuous_learning.json"
    LEARNING_INTERVAL = 3600  # 1 hour in seconds
    DAILY_REPORT_TIME = "09:00"  # 9 AM
    
    def __init__(
        self,
        client: YouTubeClient,
        performance_tracker: PerformanceTracker,
        feedback_learner: FeedbackLearner,
        multi_source_integrator: MultiSourceIntegrator,
        knowledge_graph: KnowledgeGraph,
        trend_predictor: TrendPredictor
    ):
        self.client = client
        self.performance_tracker = performance_tracker
        self.feedback_learner = feedback_learner
        self.multi_source_integrator = multi_source_integrator
        self.knowledge_graph = knowledge_graph
        self.trend_predictor = trend_predictor
        self._ensure_data_dir()
        self._load_learning_data()
        self._running = False
        self._thread = None
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
    
    def _load_learning_data(self) -> Dict[str, Any]:
        """Load continuous learning data."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "learning_sessions": [],
            "discovered_trends": [],
            "daily_reports": [],
            "ab_test_recommendations": [],
            "last_learning": None,
            "total_learning_sessions": 0
        }
    
    def _save_learning_data(self, data: Dict[str, Any]):
        """Save continuous learning data."""
        try:
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving learning data: {e}")
    
    def start_learning_loop(self, channel_handle: str = "anatolianturkishrock"):
        """
        Start the continuous learning loop in background.
        
        Args:
            channel_handle: Channel to monitor
        """
        if self._running:
            return {"status": "already_running", "message": "Learning loop is already running"}
        
        self._running = True
        self._channel_handle = channel_handle
        
        def learning_thread():
            while self._running:
                try:
                    self._learning_iteration(channel_handle)
                    time.sleep(self.LEARNING_INTERVAL)
                except Exception as e:
                    print(f"Error in learning loop: {e}")
                    time.sleep(self.LEARNING_INTERVAL)
        
        self._thread = threading.Thread(target=learning_thread, daemon=True)
        self._thread.start()
        
        return {
            "status": "started",
            "message": "Continuous learning loop started",
            "interval_seconds": self.LEARNING_INTERVAL
        }
    
    def stop_learning_loop(self):
        """Stop the continuous learning loop."""
        if not self._running:
            return {"status": "not_running", "message": "Learning loop is not running"}
        
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        
        return {"status": "stopped", "message": "Continuous learning loop stopped"}
    
    def _learning_iteration(self, channel_handle: str):
        """Single learning iteration."""
        session = {
            "timestamp": datetime.now().isoformat(),
            "channel_handle": channel_handle,
            "discoveries": [],
            "updates": []
        }
        
        # 1. Take performance snapshot
        try:
            snapshot = self.performance_tracker.track_snapshot(channel_handle)
            session["updates"].append("Performance snapshot taken")
        except Exception as e:
            session["updates"].append(f"Snapshot error: {str(e)}")
        
        # 2. Discover new trends
        try:
            keywords = ["psychedelic anatolian rock", "turkish rock", "anadolu rock"]
            opportunities = self.multi_source_integrator.synthesize_opportunities(keywords)
            viral_opps = opportunities.get("viral_opportunities", [])
            if viral_opps:
                session["discoveries"].extend([
                    {"type": "viral_opportunity", "data": opp}
                    for opp in viral_opps[:3]
                ])
        except Exception as e:
            session["updates"].append(f"Trend discovery error: {str(e)}")
        
        # 3. Learn from feedback
        try:
            patterns = self.feedback_learner.analyze_patterns()
            if patterns.get("summary", {}).get("total_feedback", 0) > 0:
                session["updates"].append("Feedback patterns analyzed")
        except Exception as e:
            session["updates"].append(f"Feedback analysis error: {str(e)}")
        
        # 4. Update knowledge graph
        try:
            graph_result = self.knowledge_graph.build_graph(channel_handle)
            session["updates"].append(f"Knowledge graph updated ({graph_result.get('nodes_count', 0)} nodes)")
        except Exception as e:
            session["updates"].append(f"Knowledge graph error: {str(e)}")
        
        # 5. Detect contradictions
        try:
            contradictions = self.knowledge_graph.detect_contradictions()
            if contradictions.get("contradictions_count", 0) > 0:
                session["discoveries"].append({
                    "type": "contradiction",
                    "count": contradictions.get("contradictions_count", 0)
                })
        except Exception as e:
            session["updates"].append(f"Contradiction detection error: {str(e)}")
        
        # Save session
        data = self._load_learning_data()
        data["learning_sessions"].append(session)
        data["last_learning"] = datetime.now().isoformat()
        data["total_learning_sessions"] = len(data["learning_sessions"])
        
        # Keep only last 100 sessions
        if len(data["learning_sessions"]) > 100:
            data["learning_sessions"] = data["learning_sessions"][-100:]
        
        self._save_learning_data(data)
    
    def generate_daily_report(self, channel_handle: str = "anatolianturkishrock") -> Dict[str, Any]:
        """
        Generate daily learning report.
        
        Args:
            channel_handle: Channel to report on
            
        Returns:
            Daily learning report
        """
        data = self._load_learning_data()
        
        # Get yesterday's sessions
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_sessions = [
            s for s in data.get("learning_sessions", [])
            if datetime.fromisoformat(s["timestamp"]) >= yesterday
        ]
        
        # Analyze growth trend
        try:
            growth_trend = self.performance_tracker.analyze_growth_trend(channel_handle, days=1)
        except Exception:
            growth_trend = {}
        
        # Get learned patterns
        try:
            patterns = self.feedback_learner.analyze_patterns()
        except Exception:
            patterns = {}
        
        # Get viral opportunities
        try:
            keywords = ["psychedelic anatolian rock", "turkish rock"]
            opportunities = self.multi_source_integrator.synthesize_opportunities(keywords)
            viral_opps = opportunities.get("viral_opportunities", [])[:5]
        except Exception:
            viral_opps = []
        
        # Generate A/B test recommendations
        ab_tests = self._generate_ab_test_recommendations(channel_handle)
        
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "channel_handle": channel_handle,
            "learning_sessions": len(yesterday_sessions),
            "discoveries": sum(len(s.get("discoveries", [])) for s in yesterday_sessions),
            "growth_trend": growth_trend,
            "learned_patterns": patterns.get("summary", {}),
            "viral_opportunities": viral_opps,
            "ab_test_recommendations": ab_tests,
            "key_insights": self._extract_key_insights(yesterday_sessions, growth_trend, patterns),
            "recommendations": self._generate_daily_recommendations(
                yesterday_sessions,
                growth_trend,
                patterns,
                viral_opps
            )
        }
        
        # Save report
        data["daily_reports"].append(report)
        if len(data["daily_reports"]) > 30:
            data["daily_reports"] = data["daily_reports"][-30:]
        self._save_learning_data(data)
        
        return report
    
    def _generate_ab_test_recommendations(self, channel_handle: str) -> List[Dict[str, Any]]:
        """Generate A/B test recommendations."""
        recommendations = []
        
        # Get knowledge graph patterns
        try:
            patterns = self.knowledge_graph.get_subscriber_growth_patterns()
            pattern_data = patterns.get("patterns", {})
            
            # Title A/B test
            title_patterns = pattern_data.get("title_patterns", {})
            if title_patterns.get("average_length"):
                recommendations.append({
                    "type": "title_length",
                    "test": f"Test title length: {title_patterns['average_length']:.0f} vs {title_patterns['average_length'] + 10:.0f} characters",
                    "reason": "Optimize title length based on successful patterns",
                    "priority": "medium"
                })
            
            # Timing A/B test
            timing_patterns = pattern_data.get("timing_patterns", {})
            if timing_patterns.get("best_hour") is not None:
                recommendations.append({
                    "type": "posting_time",
                    "test": f"Test posting at {timing_patterns['best_hour']}:00 vs {timing_patterns['best_hour'] + 2}:00",
                    "reason": "Find optimal posting time for maximum reach",
                    "priority": "high"
                })
            
            # Tag A/B test
            content_patterns = pattern_data.get("content_patterns", {})
            if content_patterns.get("common_tags"):
                recommendations.append({
                    "type": "tags",
                    "test": f"Test tag combinations: {', '.join(content_patterns['common_tags'][:5])} vs alternative tags",
                    "reason": "Optimize tag selection for better discoverability",
                    "priority": "medium"
                })
            
        except Exception as e:
            print(f"Error generating A/B tests: {e}")
        
        return recommendations
    
    def _extract_key_insights(
        self,
        sessions: List[Dict[str, Any]],
        growth_trend: Dict[str, Any],
        patterns: Dict[str, Any]
    ) -> List[str]:
        """Extract key insights from learning data."""
        insights = []
        
        # Learning activity
        if len(sessions) > 0:
            insights.append(f"📊 {len(sessions)} learning sessions completed")
        
        # Growth insights
        if growth_trend.get("status") != "insufficient_data":
            growth_data = growth_trend.get("growth", {}).get("subscribers", {})
            daily_growth = growth_data.get("daily_average", 0)
            if daily_growth > 0:
                insights.append(f"📈 Average daily subscriber growth: {daily_growth:.1f}")
        
        # Pattern insights
        if patterns.get("summary", {}).get("best_performing_type"):
            insights.append(
                f"✅ Best performing recommendation type: {patterns['summary']['best_performing_type']}"
            )
        
        return insights
    
    def _generate_daily_recommendations(
        self,
        sessions: List[Dict[str, Any]],
        growth_trend: Dict[str, Any],
        patterns: Dict[str, Any],
        viral_opps: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate daily recommendations."""
        recommendations = []
        
        # Check growth rate
        if growth_trend.get("status") != "insufficient_data":
            growth_data = growth_trend.get("growth", {}).get("subscribers", {})
            daily_growth = growth_data.get("daily_average", 0)
            
            if daily_growth < 1:
                recommendations.append("⚠️ Daily subscriber growth is below 1. Consider increasing upload frequency or improving content quality.")
            elif daily_growth > 5:
                recommendations.append("🎉 Excellent growth! Maintain consistency and scale successful content patterns.")
        
        # Viral opportunities
        if viral_opps:
            top_opp = viral_opps[0]
            recommendations.append(
                f"🔥 High viral potential opportunity: {top_opp.get('opportunity', 'N/A')} "
                f"(Potential: {top_opp.get('viral_potential', 0):.1%})"
            )
        
        # Pattern-based recommendations
        if patterns.get("insights"):
            recommendations.extend(patterns["insights"][:2])
        
        return recommendations
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get current learning loop status."""
        data = self._load_learning_data()
        
        return {
            "running": self._running,
            "last_learning": data.get("last_learning"),
            "total_sessions": data.get("total_learning_sessions", 0),
            "interval_seconds": self.LEARNING_INTERVAL,
            "channel_handle": getattr(self, "_channel_handle", None)
        }
    
    def get_learning_history(self, days: int = 7) -> Dict[str, Any]:
        """
        Get learning history for specified days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            Learning history
        """
        data = self._load_learning_data()
        cutoff_date = datetime.now() - timedelta(days=days)
        
        sessions = [
            s for s in data.get("learning_sessions", [])
            if datetime.fromisoformat(s["timestamp"]) >= cutoff_date
        ]
        
        # Analyze discoveries
        all_discoveries = []
        for session in sessions:
            all_discoveries.extend(session.get("discoveries", []))
        
        # Count discovery types
        discovery_types = {}
        for disc in all_discoveries:
            disc_type = disc.get("type", "unknown")
            discovery_types[disc_type] = discovery_types.get(disc_type, 0) + 1
        
        return {
            "period_days": days,
            "sessions_count": len(sessions),
            "discoveries_count": len(all_discoveries),
            "discovery_types": discovery_types,
            "sessions": sessions[-20:] if len(sessions) > 20 else sessions  # Last 20 sessions
        }
    
    def get_weekly_report(self, channel_handle: str = "anatolianturkishrock") -> Dict[str, Any]:
        """
        Generate weekly learning report.
        
        Args:
            channel_handle: Channel to report on
            
        Returns:
            Weekly learning report
        """
        data = self._load_learning_data()
        
        # Get last 7 days of reports
        weekly_reports = data.get("daily_reports", [])[-7:]
        
        # Analyze growth over week
        try:
            growth_trend = self.performance_tracker.analyze_growth_trend(channel_handle, days=7)
        except Exception:
            growth_trend = {}
        
        # Aggregate discoveries
        all_discoveries = []
        for report in weekly_reports:
            all_discoveries.extend(report.get("viral_opportunities", []))
        
        # Get learning history
        history = self.get_learning_history(days=7)
        
        report = {
            "week_start": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "week_end": datetime.now().strftime("%Y-%m-%d"),
            "channel_handle": channel_handle,
            "daily_reports_count": len(weekly_reports),
            "total_learning_sessions": history.get("sessions_count", 0),
            "total_discoveries": history.get("discoveries_count", 0),
            "growth_summary": growth_trend,
            "top_discoveries": sorted(
                all_discoveries,
                key=lambda x: x.get("viral_potential", 0),
                reverse=True
            )[:10],
            "weekly_insights": self._generate_weekly_insights(weekly_reports, growth_trend),
            "next_week_recommendations": self._generate_weekly_recommendations(weekly_reports, growth_trend)
        }
        
        return report
    
    def _generate_weekly_insights(
        self,
        weekly_reports: List[Dict[str, Any]],
        growth_trend: Dict[str, Any]
    ) -> List[str]:
        """Generate weekly insights."""
        insights = []
        
        # Growth insights
        if growth_trend.get("status") != "insufficient_data":
            growth_data = growth_trend.get("growth", {}).get("subscribers", {})
            weekly_growth = growth_data.get("change", 0)
            daily_avg = growth_data.get("daily_average", 0)
            
            insights.append(f"📈 Weekly subscriber growth: {weekly_growth:,} (avg: {daily_avg:.1f}/day)")
            
            # Project to 1M
            projection = growth_trend.get("projection", {})
            if projection.get("days_to_1m"):
                insights.append(
                    f"🎯 At current rate, 1M subscribers in {projection['days_to_1m']:,.0f} days"
                )
        
        # Learning activity
        insights.append(f"🧠 {len(weekly_reports)} daily learning reports generated")
        
        # Discoveries
        total_opps = sum(len(r.get("viral_opportunities", [])) for r in weekly_reports)
        if total_opps > 0:
            insights.append(f"🔥 {total_opps} viral opportunities discovered this week")
        
        return insights
    
    def _generate_weekly_recommendations(
        self,
        weekly_reports: List[Dict[str, Any]],
        growth_trend: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations for next week."""
        recommendations = []
        
        # Growth-based recommendations
        if growth_trend.get("status") != "insufficient_data":
            growth_data = growth_trend.get("growth", {}).get("subscribers", {})
            daily_avg = growth_data.get("daily_average", 0)
            
            if daily_avg < 2:
                recommendations.append("Focus on increasing daily subscriber growth to at least 2 subscribers/day")
                recommendations.append("Consider improving video titles and thumbnails for better click-through rates")
        
        # A/B test recommendations
        all_ab_tests = []
        for report in weekly_reports:
            all_ab_tests.extend(report.get("ab_test_recommendations", []))
        
        if all_ab_tests:
            high_priority = [t for t in all_ab_tests if t.get("priority") == "high"]
            if high_priority:
                recommendations.append(
                    f"🧪 Run A/B test: {high_priority[0].get('test', 'N/A')}"
                )
        
        # Viral opportunities
        all_opps = []
        for report in weekly_reports:
            all_opps.extend(report.get("viral_opportunities", []))
        
        if all_opps:
            top_opp = max(all_opps, key=lambda x: x.get("viral_potential", 0))
            recommendations.append(
                f"🔥 Prioritize viral opportunity: {top_opp.get('opportunity', 'N/A')}"
            )
        
        return recommendations

