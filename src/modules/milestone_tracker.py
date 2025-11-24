"""
Growth Milestone Tracker Module
Tracks progress toward 1 million subscriber goal.

AGI Paradigm: Growth Milestone Tracker
- Tracks milestones on the path to 1M subscribers
- Provides milestone-specific strategies
- Learns from each milestone achievement
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient


class MilestoneTracker:
    """
    Tracks growth milestones toward 1M subscribers.
    
    AGI Paradigm: Growth Milestone Tracker
    - Tracks progress through key milestones
    - Provides milestone-specific strategies
    - Learns from milestone achievements
    """
    
    MILESTONES = [
        {"target": 1_000, "name": "1K Subscribers", "level": "beginner"},
        {"target": 10_000, "name": "10K Subscribers", "level": "intermediate"},
        {"target": 50_000, "name": "50K Subscribers", "level": "advanced"},
        {"target": 100_000, "name": "100K Subscribers", "level": "expert"},
        {"target": 500_000, "name": "500K Subscribers", "level": "master"},
        {"target": 1_000_000, "name": "1M Subscribers", "level": "legendary"}
    ]
    
    DATA_FILE = "data/milestone_history.json"
    
    def __init__(self, client: YouTubeClient):
        self.client = client
        self._ensure_data_dir()
        self._load_history()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
    
    def _load_history(self) -> Dict[str, Any]:
        """Load milestone history from file."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "milestones_achieved": [],
            "current_milestone": None,
            "progress_history": [],
            "strategies_used": {},
            "lessons_learned": {}
        }
    
    def _save_history(self, data: Dict[str, Any]):
        """Save milestone history to file."""
        try:
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving milestone history: {e}")
    
    def get_current_status(self, channel_handle: str) -> Dict[str, Any]:
        """
        Get current milestone status.
        
        Args:
            channel_handle: Channel to check
            
        Returns:
            Current milestone status and progress
        """
        try:
            channel_data = self.client.get_channel_by_handle(channel_handle)
            if not channel_data.get("items"):
                raise ValueError(f"Channel @{channel_handle} not found")
            
            stats = channel_data["items"][0]["statistics"]
            current_subscribers = int(stats.get("subscriberCount", 0))
            
            # Find current and next milestone
            current_milestone = None
            next_milestone = None
            achieved_milestones = []
            
            for milestone in self.MILESTONES:
                if current_subscribers >= milestone["target"]:
                    achieved_milestones.append(milestone)
                    current_milestone = milestone
                elif next_milestone is None:
                    next_milestone = milestone
                    break
            
            # Calculate progress to next milestone
            if next_milestone:
                progress_percent = (current_subscribers / next_milestone["target"]) * 100
                subscribers_needed = next_milestone["target"] - current_subscribers
                progress_ratio = current_subscribers / next_milestone["target"]
            else:
                # Already at or past 1M
                progress_percent = 100
                subscribers_needed = 0
                progress_ratio = 1.0
                next_milestone = self.MILESTONES[-1]
            
            # Calculate time estimates
            time_estimates = self._calculate_time_estimates(
                current_subscribers,
                next_milestone["target"] if next_milestone else 1_000_000
            )
            
            # Get milestone-specific strategy
            strategy = self._get_milestone_strategy(
                current_milestone,
                next_milestone,
                current_subscribers
            )
            
            # Record progress
            self._record_progress(channel_handle, current_subscribers, next_milestone)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "channel_handle": channel_handle,
                "current_subscribers": current_subscribers,
                "target_subscribers": 1_000_000,
                "overall_progress_percent": (current_subscribers / 1_000_000) * 100,
                "current_milestone": current_milestone,
                "next_milestone": next_milestone,
                "achieved_milestones": achieved_milestones,
                "progress_to_next": {
                    "percent": progress_percent,
                    "subscribers_needed": subscribers_needed,
                    "ratio": progress_ratio
                },
                "time_estimates": time_estimates,
                "strategy": strategy,
                "motivation": self._get_motivation_message(current_subscribers, next_milestone)
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _calculate_time_estimates(
        self,
        current: int,
        target: int
    ) -> Dict[str, Any]:
        """Calculate time estimates to reach target."""
        subscribers_needed = target - current
        
        # Different growth rate scenarios
        scenarios = {
            "conservative": 1,  # 1 subscriber per day
            "moderate": 5,      # 5 subscribers per day
            "aggressive": 10,  # 10 subscribers per day
            "viral": 50         # 50 subscribers per day (viral growth)
        }
        
        estimates = {}
        for scenario_name, daily_growth in scenarios.items():
            if daily_growth > 0:
                days_needed = subscribers_needed / daily_growth
                estimated_date = datetime.now() + timedelta(days=days_needed)
                estimates[scenario_name] = {
                    "daily_growth": daily_growth,
                    "days_needed": days_needed,
                    "estimated_date": estimated_date.isoformat(),
                    "years": days_needed / 365.25
                }
            else:
                estimates[scenario_name] = {
                    "daily_growth": 0,
                    "days_needed": None,
                    "estimated_date": None,
                    "years": None
                }
        
        return estimates
    
    def _get_milestone_strategy(
        self,
        current_milestone: Optional[Dict[str, Any]],
        next_milestone: Optional[Dict[str, Any]],
        current_subscribers: int
    ) -> Dict[str, Any]:
        """Get milestone-specific strategy."""
        if not next_milestone:
            return {
                "focus": "Maintain and grow",
                "actions": [
                    "Continue creating high-quality content",
                    "Engage with community",
                    "Explore new content formats"
                ]
            }
        
        target = next_milestone["target"]
        level = next_milestone["level"]
        
        strategies = {
            "beginner": {
                "focus": "Build foundation and consistency",
                "key_actions": [
                    "Upload consistently (at least 1 video per week)",
                    "Optimize titles and descriptions for SEO",
                    "Engage with every comment",
                    "Create compelling thumbnails",
                    "Focus on one niche and master it"
                ],
                "content_tips": [
                    "Create content that solves problems or entertains",
                    "Use trending keywords in your niche",
                    "Make first 15 seconds count",
                    "Add clear call-to-actions"
                ],
                "growth_hacks": [
                    "Collaborate with similar channels",
                    "Share on relevant social media",
                    "Engage in community discussions",
                    "Create series to encourage subscriptions"
                ]
            },
            "intermediate": {
                "focus": "Scale and optimize",
                "key_actions": [
                    "Increase upload frequency to 2-3 videos per week",
                    "Analyze which content performs best",
                    "Double down on successful content types",
                    "Build email list for direct communication",
                    "Create playlists to increase watch time"
                ],
                "content_tips": [
                    "A/B test thumbnails and titles",
                    "Create longer-form content (10+ minutes)",
                    "Use end screens and cards effectively",
                    "Create content series with cliffhangers"
                ],
                "growth_hacks": [
                    "Leverage YouTube Shorts for discovery",
                    "Cross-promote on other platforms",
                    "Run giveaways or contests",
                    "Create community posts regularly"
                ]
            },
            "advanced": {
                "focus": "Professionalize and monetize",
                "key_actions": [
                    "Maintain consistent brand identity",
                    "Invest in better equipment and editing",
                    "Build a team or outsource tasks",
                    "Diversify content while staying on-brand",
                    "Engage with larger creator community"
                ],
                "content_tips": [
                    "Create signature content formats",
                    "Collaborate with bigger creators",
                    "Experiment with new formats (live, podcasts)",
                    "Create evergreen content library"
                ],
                "growth_hacks": [
                    "Leverage YouTube algorithm updates",
                    "Create viral-worthy content regularly",
                    "Build partnerships and sponsorships",
                    "Use data analytics to optimize"
                ]
            },
            "expert": {
                "focus": "Dominate niche and expand",
                "key_actions": [
                    "Become the go-to authority in your niche",
                    "Create multiple content series",
                    "Build a media company, not just a channel",
                    "Expand to other platforms strategically",
                    "Mentor or collaborate with smaller creators"
                ],
                "content_tips": [
                    "Create premium, high-production content",
                    "Launch exclusive content for members",
                    "Create merchandise and products",
                    "Host events or meetups"
                ],
                "growth_hacks": [
                    "Leverage press and media coverage",
                    "Create viral moments intentionally",
                    "Build a strong community outside YouTube",
                    "Use advanced SEO and marketing strategies"
                ]
            },
            "master": {
                "focus": "Scale to 1M and beyond",
                "key_actions": [
                    "Maintain quality while scaling production",
                    "Build multiple revenue streams",
                    "Create a recognizable brand",
                    "Expand content to related niches",
                    "Build a sustainable business model"
                ],
                "content_tips": [
                    "Create blockbuster content regularly",
                    "Leverage trends while staying authentic",
                    "Create content that gets shared",
                    "Build anticipation for releases"
                ],
                "growth_hacks": [
                    "Strategic partnerships with major brands",
                    "Cross-platform content strategy",
                    "Leverage influencer networks",
                    "Create viral challenges or trends"
                ]
            },
            "legendary": {
                "focus": "Maintain 1M+ and legacy",
                "key_actions": [
                    "You've reached 1M! Maintain momentum",
                    "Focus on community and legacy",
                    "Mentor next generation of creators",
                    "Expand into new ventures",
                    "Give back to the community"
                ],
                "content_tips": [
                    "Create legacy-defining content",
                    "Document your journey for others",
                    "Create educational content for creators",
                    "Maintain authenticity and connection"
                ],
                "growth_hacks": [
                    "Focus on retention over acquisition",
                    "Build a sustainable long-term brand",
                    "Create impact beyond YouTube",
                    "Leave a lasting legacy"
                ]
            }
        }
        
        return strategies.get(level, strategies["beginner"])
    
    def _get_motivation_message(
        self,
        current: int,
        next_milestone: Optional[Dict[str, Any]]
    ) -> str:
        """Get motivational message."""
        if not next_milestone:
            return "🎉 Congratulations! You've reached 1M subscribers! Focus on maintaining and growing your community."
        
        needed = next_milestone["target"] - current
        percent = (current / next_milestone["target"]) * 100
        
        if percent < 10:
            return f"🚀 Just starting! You're {needed:,} subscribers away from {next_milestone['name']}. Every journey begins with a single step!"
        elif percent < 25:
            return f"💪 Building momentum! {percent:.1f}% to {next_milestone['name']}. Keep creating great content!"
        elif percent < 50:
            return f"🔥 Halfway there! {percent:.1f}% to {next_milestone['name']}. You're making great progress!"
        elif percent < 75:
            return f"⚡ Almost there! {percent:.1f}% to {next_milestone['name']}. The finish line is in sight!"
        else:
            return f"🎯 So close! {percent:.1f}% to {next_milestone['name']}. Push through to the milestone!"
    
    def _record_progress(
        self,
        channel_handle: str,
        current_subscribers: int,
        next_milestone: Optional[Dict[str, Any]]
    ):
        """Record progress snapshot."""
        history = self._load_history()
        
        if "progress_history" not in history:
            history["progress_history"] = []
        
        history["progress_history"].append({
            "timestamp": datetime.now().isoformat(),
            "channel_handle": channel_handle,
            "subscribers": current_subscribers,
            "next_milestone": next_milestone["name"] if next_milestone else "1M+",
            "progress_percent": (current_subscribers / (next_milestone["target"] if next_milestone else 1_000_000)) * 100
        })
        
        # Keep only last 100 records
        if len(history["progress_history"]) > 100:
            history["progress_history"] = history["progress_history"][-100:]
        
        # Update current milestone
        history["current_milestone"] = next_milestone["name"] if next_milestone else "1M+"
        
        self._save_history(history)
    
    def mark_milestone_achieved(
        self,
        channel_handle: str,
        milestone_target: int,
        achievement_date: Optional[datetime] = None
    ):
        """
        Mark a milestone as achieved.
        
        Args:
            channel_handle: Channel that achieved milestone
            milestone_target: Target subscriber count
            achievement_date: Date of achievement (defaults to now)
        """
        history = self._load_history()
        
        milestone = next(
            (m for m in self.MILESTONES if m["target"] == milestone_target),
            None
        )
        
        if milestone:
            achievement = {
                "milestone": milestone,
                "channel_handle": channel_handle,
                "achieved_at": (achievement_date or datetime.now()).isoformat(),
                "subscribers_at_achievement": milestone_target
            }
            
            # Check if already recorded
            existing = [
                a for a in history.get("milestones_achieved", [])
                if (a.get("milestone", {}).get("target") == milestone_target and
                    a.get("channel_handle") == channel_handle)
            ]
            
            if not existing:
                if "milestones_achieved" not in history:
                    history["milestones_achieved"] = []
                history["milestones_achieved"].append(achievement)
                self._save_history(history)
    
    def get_milestone_history(self) -> Dict[str, Any]:
        """Get history of all milestones."""
        history = self._load_history()
        return {
            "achieved_milestones": history.get("milestones_achieved", []),
            "progress_history": history.get("progress_history", []),
            "current_milestone": history.get("current_milestone"),
            "total_milestones": len(self.MILESTONES),
            "achieved_count": len(history.get("milestones_achieved", []))
        }

