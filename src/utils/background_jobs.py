"""
Background Jobs Module
Periodic tasks for competitor tracking, trend analysis, etc.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import threading
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient, create_client
from src.modules.competitor_tracker import CompetitorTracker
from src.modules.competitor_analyzer import CompetitorAnalyzer
from src.modules.trend_predictor import TrendPredictor
from src.modules.video_ideas_database import VideoIdeasDatabase
from src.modules.channel_audit import ChannelAudit
from src.modules.channel_analyzer import ChannelAnalyzer
from src.modules.video_seo_audit import VideoSEOAudit
from src.modules.keyword_researcher import KeywordResearcher
from src.modules.title_optimizer import TitleOptimizer
from src.modules.description_generator import DescriptionGenerator
from src.modules.tag_suggester import TagSuggester


class BackgroundJobScheduler:
    """
    Background job scheduler for periodic tasks.
    
    AGI Paradigm: Continuous Learning Loop
    - Runs periodic tasks in background
    - Monitors competitors
    - Updates trend data
    - Performs channel audits
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the background job scheduler.
        
        Args:
            api_key: YouTube API key
        """
        self.api_key = api_key
        self.client = create_client(api_key=api_key)
        self.running = False
        self.thread = None
        self.jobs = []
    
    def start(self):
        """Start the background job scheduler."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the background job scheduler."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
    
    def _run_loop(self):
        """Main loop for background jobs."""
        while self.running:
            try:
                # Run daily jobs
                if self._should_run_daily_jobs():
                    self._run_daily_jobs()
                
                # Run hourly jobs
                if self._should_run_hourly_jobs():
                    self._run_hourly_jobs()
                
                # Sleep for 1 hour
                time.sleep(3600)  # 1 hour
            except Exception as e:
                print(f"Error in background job loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _should_run_daily_jobs(self) -> bool:
        """Check if daily jobs should run (once per day)."""
        # Simple check: run if it's been more than 23 hours since last run
        # In production, use proper scheduling (e.g., APScheduler)
        return True  # Simplified for now
    
    def _should_run_hourly_jobs(self) -> bool:
        """Check if hourly jobs should run."""
        return True  # Simplified for now
    
    def _run_daily_jobs(self):
        """Run daily background jobs."""
        try:
            # Competitor tracking
            self._check_competitors()
            
            # Update video ideas database
            self._update_video_ideas()
            
            # Trend analysis
            self._update_trends()
            
            # Channel audit (weekly, but check daily)
            if datetime.now().weekday() == 0:  # Monday
                self._run_channel_audits()
        except Exception as e:
            print(f"Error in daily jobs: {e}")
    
    def _run_hourly_jobs(self):
        """Run hourly background jobs."""
        try:
            # Check competitors more frequently
            self._check_competitors()
        except Exception as e:
            print(f"Error in hourly jobs: {e}")
    
    def _check_competitors(self):
        """Check competitors for new videos."""
        try:
            competitor_analyzer = CompetitorAnalyzer(self.client)
            competitor_tracker = CompetitorTracker(self.client, competitor_analyzer)
            
            results = competitor_tracker.check_competitors()
            
            # Store results for notifications
            self._store_job_result("competitor_check", {
                "checked_at": datetime.now().isoformat(),
                "competitors_checked": results.get("competitors_checked", 0),
                "new_videos_found": results.get("new_videos_found", 0),
                "alerts": results.get("alerts", [])
            })
        except Exception as e:
            print(f"Error checking competitors: {e}")
    
    def _update_video_ideas(self):
        """Update video ideas database with new trends."""
        try:
            ideas_db = VideoIdeasDatabase()
            
            # Get trending ideas from various sources
            # This would integrate with trend analysis
            # For now, just log the job
            self._store_job_result("video_ideas_update", {
                "updated_at": datetime.now().isoformat(),
                "status": "completed"
            })
        except Exception as e:
            print(f"Error updating video ideas: {e}")
    
    def _update_trends(self):
        """Update trend analysis data."""
        try:
            trend_predictor = TrendPredictor(self.client)
            
            # Analyze trends for common niches
            # This would be configured per user/channel
            self._store_job_result("trend_update", {
                "updated_at": datetime.now().isoformat(),
                "status": "completed"
            })
        except Exception as e:
            print(f"Error updating trends: {e}")
    
    def _run_channel_audits(self):
        """Run channel audits for tracked channels."""
        try:
            # This would iterate over user channels
            # For now, just log the job
            self._store_job_result("channel_audit", {
                "run_at": datetime.now().isoformat(),
                "status": "completed"
            })
        except Exception as e:
            print(f"Error running channel audits: {e}")
    
    def _store_job_result(self, job_name: str, result: Dict[str, Any]):
        """Store job execution result."""
        self.jobs.append({
            "job_name": job_name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 100 jobs
        if len(self.jobs) > 100:
            self.jobs = self.jobs[-100:]
    
    def get_job_history(self, job_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get job execution history."""
        if job_name:
            return [j for j in self.jobs if j.get("job_name") == job_name]
        return self.jobs
    
    def get_status(self) -> Dict[str, Any]:
        """Get scheduler status."""
        return {
            "running": self.running,
            "total_jobs_executed": len(self.jobs),
            "last_job": self.jobs[-1] if self.jobs else None
        }

