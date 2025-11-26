"""
Content Calendar Module
Video planning and scheduling calendar.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
import csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


class ContentCalendar:
    """
    Content calendar for video planning and scheduling.
    
    AGI Paradigm: Proactive Assistant Interface
    - Plans video content in advance
    - Schedules optimal posting times
    - Manages video series
    - Sends reminders
    """
    
    def __init__(self, db_path: str = "data/content_calendar.json"):
        """
        Initialize the content calendar.
        
        Args:
            db_path: Path to the calendar database file
        """
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database file and directory exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump({"scheduled_videos": [], "series": []}, f, indent=2)
    
    def schedule_video(
        self,
        title: str,
        scheduled_date: str,
        scheduled_time: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        series_id: Optional[str] = None,
        video_idea_id: Optional[str] = None,
        reminder_enabled: bool = True
    ) -> str:
        """
        Schedule a video for publication.
        
        Args:
            title: Video title
            scheduled_date: Scheduled date (YYYY-MM-DD)
            scheduled_time: Scheduled time (HH:MM)
            description: Video description
            tags: Video tags
            series_id: Optional series ID
            video_idea_id: Optional video idea ID
            reminder_enabled: Whether to send reminders
        
        Returns:
            Scheduled video ID
        """
        video_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(title) % 10000}"
        
        scheduled_video = {
            "id": video_id,
            "title": title,
            "description": description or "",
            "tags": tags or [],
            "scheduled_date": scheduled_date,
            "scheduled_time": scheduled_time,
            "scheduled_datetime": f"{scheduled_date}T{scheduled_time}:00",
            "series_id": series_id,
            "video_idea_id": video_idea_id,
            "reminder_enabled": reminder_enabled,
            "status": "scheduled",  # scheduled, published, cancelled
            "created_at": datetime.now().isoformat(),
            "published_at": None,
            "reminders_sent": []
        }
        
        # Load existing schedule
        data = self._load_data()
        data["scheduled_videos"].append(scheduled_video)
        self._save_data(data)
        
        return video_id
    
    def get_scheduled_videos(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[str] = None,
        series_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get scheduled videos with filters."""
        data = self._load_data()
        videos = data.get("scheduled_videos", [])
        
        # Apply filters
        filtered = []
        for video in videos:
            # Date filter
            if start_date and video.get("scheduled_date", "") < start_date:
                continue
            if end_date and video.get("scheduled_date", "") > end_date:
                continue
            
            # Status filter
            if status and video.get("status", "") != status:
                continue
            
            # Series filter
            if series_id and video.get("series_id") != series_id:
                continue
            
            filtered.append(video)
        
        # Sort by scheduled date
        filtered.sort(key=lambda x: x.get("scheduled_datetime", ""))
        
        return filtered
    
    def create_series(
        self,
        series_name: str,
        description: Optional[str] = None,
        total_episodes: Optional[int] = None,
        release_schedule: str = "weekly"  # weekly, bi-weekly, daily
    ) -> str:
        """Create a video series."""
        series_id = f"series_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(series_name) % 10000}"
        
        series = {
            "id": series_id,
            "name": series_name,
            "description": description or "",
            "total_episodes": total_episodes,
            "release_schedule": release_schedule,
            "created_at": datetime.now().isoformat(),
            "episodes": []
        }
        
        data = self._load_data()
        data["series"].append(series)
        self._save_data(data)
        
        return series_id
    
    def add_episode_to_series(
        self,
        series_id: str,
        title: str,
        episode_number: int,
        scheduled_date: Optional[str] = None,
        scheduled_time: Optional[str] = None
    ) -> str:
        """Add an episode to a series."""
        # Get series info
        data = self._load_data()
        series = next((s for s in data["series"] if s.get("id") == series_id), None)
        
        if not series:
            raise ValueError(f"Series {series_id} not found")
        
        # Calculate scheduled date if not provided
        if not scheduled_date:
            # Get last episode date or use today
            episodes = series.get("episodes", [])
            if episodes:
                last_episode = max(episodes, key=lambda e: e.get("scheduled_date", ""))
                last_date = datetime.fromisoformat(last_episode.get("scheduled_date", datetime.now().isoformat()))
                
                # Add based on release schedule
                if series.get("release_schedule") == "weekly":
                    scheduled_date = (last_date + timedelta(days=7)).strftime("%Y-%m-%d")
                elif series.get("release_schedule") == "bi-weekly":
                    scheduled_date = (last_date + timedelta(days=14)).strftime("%Y-%m-%d")
                elif series.get("release_schedule") == "daily":
                    scheduled_date = (last_date + timedelta(days=1)).strftime("%Y-%m-%d")
                else:
                    scheduled_date = (last_date + timedelta(days=7)).strftime("%Y-%m-%d")
            else:
                scheduled_date = datetime.now().strftime("%Y-%m-%d")
        
        if not scheduled_time:
            scheduled_time = "19:00"  # Default optimal time
        
        # Schedule the video
        video_id = self.schedule_video(
            title=title,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            series_id=series_id
        )
        
        # Add to series
        episode = {
            "episode_number": episode_number,
            "video_id": video_id,
            "title": title,
            "scheduled_date": scheduled_date,
            "scheduled_time": scheduled_time
        }
        
        series["episodes"].append(episode)
        self._save_data(data)
        
        return video_id
    
    def get_upcoming_videos(
        self,
        days_ahead: int = 30
    ) -> List[Dict[str, Any]]:
        """Get upcoming scheduled videos."""
        end_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        return self.get_scheduled_videos(
            start_date=datetime.now().strftime("%Y-%m-%d"),
            end_date=end_date,
            status="scheduled"
        )
    
    def get_reminders(
        self,
        days_ahead: int = 7
    ) -> List[Dict[str, Any]]:
        """Get videos that need reminders."""
        upcoming = self.get_upcoming_videos(days_ahead=days_ahead)
        
        reminders = []
        for video in upcoming:
            if not video.get("reminder_enabled", True):
                continue
            
            scheduled_datetime_str = video.get("scheduled_datetime", "")
            if not scheduled_datetime_str:
                continue
            
            try:
                scheduled_datetime = datetime.fromisoformat(scheduled_datetime_str)
                now = datetime.now()
                
                # Remind 1 day before and on the day
                days_until = (scheduled_datetime - now).days
                
                if 0 <= days_until <= 1:
                    reminders.append({
                        "video": video,
                        "days_until": days_until,
                        "reminder_type": "day_of" if days_until == 0 else "day_before"
                    })
            except:
                continue
        
        return reminders
    
    def mark_published(self, video_id: str, published_at: Optional[str] = None):
        """Mark a scheduled video as published."""
        data = self._load_data()
        
        for video in data["scheduled_videos"]:
            if video.get("id") == video_id:
                video["status"] = "published"
                video["published_at"] = published_at or datetime.now().isoformat()
                break
        
        self._save_data(data)
    
    def export_calendar(
        self,
        format: str = "csv",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """
        Export calendar to iCal or CSV format.
        
        Args:
            format: Export format (csv or ical)
            start_date: Start date filter
            end_date: End date filter
        
        Returns:
            Exported calendar content
        """
        videos = self.get_scheduled_videos(start_date=start_date, end_date=end_date)
        
        if format == "csv":
            # Export to CSV
            output = []
            output.append(["Title", "Date", "Time", "Status", "Series", "Description"])
            
            for video in videos:
                output.append([
                    video.get("title", ""),
                    video.get("scheduled_date", ""),
                    video.get("scheduled_time", ""),
                    video.get("status", ""),
                    video.get("series_id", ""),
                    video.get("description", "")[:100]  # Truncate description
                ])
            
            # Convert to CSV string
            import io
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerows(output)
            return csv_buffer.getvalue()
        
        elif format == "ical":
            # Export to iCal format
            ical_lines = [
                "BEGIN:VCALENDAR",
                "VERSION:2.0",
                "PRODID:-//YouTube SEO Tool//Content Calendar//EN",
                "CALSCALE:GREGORIAN",
                "METHOD:PUBLISH"
            ]
            
            for video in videos:
                scheduled_datetime_str = video.get("scheduled_datetime", "")
                if not scheduled_datetime_str:
                    continue
                
                try:
                    dt = datetime.fromisoformat(scheduled_datetime_str.replace("T", " ").replace(":00", ""))
                    dt_end = dt + timedelta(hours=1)  # 1 hour event
                    
                    # Format for iCal (YYYYMMDDTHHMMSS)
                    dt_start_str = dt.strftime("%Y%m%dT%H%M%S")
                    dt_end_str = dt_end.strftime("%Y%m%dT%H%M%S")
                    
                    title = video.get("title", "Untitled Video").replace(",", "\\,").replace(";", "\\;")
                    description = video.get("description", "").replace(",", "\\,").replace(";", "\\;")[:200]
                    
                    ical_lines.extend([
                        "BEGIN:VEVENT",
                        f"DTSTART:{dt_start_str}",
                        f"DTEND:{dt_end_str}",
                        f"SUMMARY:{title}",
                        f"DESCRIPTION:{description}",
                        f"UID:{video.get('id', '')}@youtube-seo-tool",
                        "END:VEVENT"
                    ])
                except:
                    continue
            
            ical_lines.append("END:VCALENDAR")
            return "\n".join(ical_lines)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _load_data(self) -> Dict[str, Any]:
        """Load calendar data from database."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"scheduled_videos": [], "series": []}
    
    def _save_data(self, data: Dict[str, Any]):
        """Save calendar data to database."""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

