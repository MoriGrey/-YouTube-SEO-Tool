"""
Notification System Module
Email, in-app, and browser push notifications.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


class NotificationSystem:
    """
    Notification system for various alert types.
    
    AGI Paradigm: Proactive Assistant Interface
    - Sends notifications proactively
    - Supports multiple notification channels
    - Manages notification preferences
    """
    
    def __init__(self, db_path: str = "data/notifications.json"):
        """
        Initialize the notification system.
        
        Args:
            db_path: Path to notification database
        """
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database file and directory exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump({"notifications": [], "preferences": {}}, f, indent=2)
    
    def send_notification(
        self,
        user_id: str,
        notification_type: str,  # "email", "in_app", "browser_push"
        title: str,
        message: str,
        priority: str = "normal",  # "low", "normal", "high", "urgent"
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Send a notification.
        
        Args:
            user_id: User ID
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            priority: Notification priority
            metadata: Optional metadata
        
        Returns:
            Notification ID
        """
        notification_id = f"notif_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(title) % 10000}"
        
        notification = {
            "id": notification_id,
            "user_id": user_id,
            "type": notification_type,
            "title": title,
            "message": message,
            "priority": priority,
            "metadata": metadata or {},
            "sent_at": datetime.now().isoformat(),
            "read": False,
            "read_at": None
        }
        
        # Check user preferences
        preferences = self.get_user_preferences(user_id)
        if not preferences.get(f"{notification_type}_enabled", True):
            return notification_id  # Don't send if disabled
        
        # Send based on type
        if notification_type == "email":
            self._send_email(user_id, title, message, priority)
        elif notification_type == "in_app":
            # Store for in-app display
            pass
        elif notification_type == "browser_push":
            self._send_browser_push(user_id, title, message, priority)
        
        # Save notification
        data = self._load_data()
        data["notifications"].append(notification)
        self._save_data(data)
        
        return notification_id
    
    def _send_email(
        self,
        user_id: str,
        title: str,
        message: str,
        priority: str
    ):
        """Send email notification."""
        # In production, integrate with email service (SendGrid, SMTP, etc.)
        # For now, just log
        print(f"Email notification to {user_id}: {title} - {message}")
    
    def _send_browser_push(
        self,
        user_id: str,
        title: str,
        message: str,
        priority: str
    ):
        """Send browser push notification."""
        # In production, integrate with browser push API
        # For now, just log
        print(f"Browser push to {user_id}: {title} - {message}")
    
    def get_user_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get notifications for a user."""
        data = self._load_data()
        notifications = [
            n for n in data.get("notifications", [])
            if n.get("user_id") == user_id
        ]
        
        if unread_only:
            notifications = [n for n in notifications if not n.get("read", False)]
        
        # Sort by sent_at descending
        notifications.sort(key=lambda x: x.get("sent_at", ""), reverse=True)
        
        return notifications[:limit]
    
    def mark_as_read(self, notification_id: str, user_id: str) -> bool:
        """Mark a notification as read."""
        data = self._load_data()
        
        for notification in data.get("notifications", []):
            if notification.get("id") == notification_id and notification.get("user_id") == user_id:
                notification["read"] = True
                notification["read_at"] = datetime.now().isoformat()
                self._save_data(data)
                return True
        
        return False
    
    def mark_all_as_read(self, user_id: str) -> int:
        """Mark all notifications as read for a user."""
        data = self._load_data()
        count = 0
        
        for notification in data.get("notifications", []):
            if notification.get("user_id") == user_id and not notification.get("read", False):
                notification["read"] = True
                notification["read_at"] = datetime.now().isoformat()
                count += 1
        
        if count > 0:
            self._save_data(data)
        
        return count
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get notification preferences for a user."""
        data = self._load_data()
        preferences = data.get("preferences", {}).get(user_id, {})
        
        # Default preferences
        defaults = {
            "email_enabled": True,
            "in_app_enabled": True,
            "browser_push_enabled": False,
            "competitor_alerts": True,
            "trend_alerts": True,
            "audit_alerts": True,
            "calendar_reminders": True
        }
        
        # Merge with defaults
        return {**defaults, **preferences}
    
    def update_user_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> bool:
        """Update notification preferences for a user."""
        data = self._load_data()
        
        if "preferences" not in data:
            data["preferences"] = {}
        
        if user_id not in data["preferences"]:
            data["preferences"][user_id] = {}
        
        data["preferences"][user_id].update(preferences)
        self._save_data(data)
        
        return True
    
    def send_competitor_alert(
        self,
        user_id: str,
        competitor_name: str,
        video_title: str,
        video_url: str
    ):
        """Send competitor new video alert."""
        self.send_notification(
            user_id=user_id,
            notification_type="in_app",
            title=f"New Video from {competitor_name}",
            message=f"{competitor_name} published: {video_title}",
            priority="normal",
            metadata={
                "type": "competitor_alert",
                "competitor_name": competitor_name,
                "video_title": video_title,
                "video_url": video_url
            }
        )
    
    def send_trend_alert(
        self,
        user_id: str,
        trend_keyword: str,
        trend_score: float
    ):
        """Send trend alert."""
        self.send_notification(
            user_id=user_id,
            notification_type="in_app",
            title="New Trend Detected",
            message=f"'{trend_keyword}' is trending (score: {trend_score:.1f})",
            priority="normal",
            metadata={
                "type": "trend_alert",
                "keyword": trend_keyword,
                "score": trend_score
            }
        )
    
    def send_calendar_reminder(
        self,
        user_id: str,
        video_title: str,
        scheduled_date: str,
        scheduled_time: str
    ):
        """Send content calendar reminder."""
        self.send_notification(
            user_id=user_id,
            notification_type="in_app",
            title="Video Scheduled Today",
            message=f"'{video_title}' is scheduled for {scheduled_date} at {scheduled_time}",
            priority="high",
            metadata={
                "type": "calendar_reminder",
                "video_title": video_title,
                "scheduled_date": scheduled_date,
                "scheduled_time": scheduled_time
            }
        )
    
    def send_audit_alert(
        self,
        user_id: str,
        channel_name: str,
        health_score: float
    ):
        """Send channel audit alert."""
        self.send_notification(
            user_id=user_id,
            notification_type="in_app",
            title="Channel Audit Complete",
            message=f"Audit for {channel_name} completed. Health score: {health_score:.1f}/100",
            priority="normal",
            metadata={
                "type": "audit_alert",
                "channel_name": channel_name,
                "health_score": health_score
            }
        )
    
    def _load_data(self) -> Dict[str, Any]:
        """Load notification data from database."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"notifications": [], "preferences": {}}
    
    def _save_data(self, data: Dict[str, Any]):
        """Save notification data to database."""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

