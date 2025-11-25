"""
Engagement Booster Suggestions Module
Suggest polls, cards, and end screens to boost engagement.

AGI Paradigm: Self-Evolving Architecture
- Analyzes video performance to suggest engagement elements
- Recommends optimal timing and placement
- Learns from successful engagement strategies
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient


class EngagementBooster:
    """
    Engagement booster suggestion system.
    
    AGI Paradigm: Self-Evolving Architecture
    - Suggests polls, cards, and end screens
    - Optimizes timing for maximum engagement
    - Learns from successful strategies
    """
    
    def __init__(self, client: YouTubeClient):
        self.client = client
    
    def suggest_engagement_elements(
        self,
        video_id: str,
        video_duration: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Suggest engagement elements (polls, cards, end screens) for a video.
        
        Args:
            video_id: YouTube video ID
            video_duration: Video duration in seconds (optional)
            
        Returns:
            Engagement suggestions with timing recommendations
        """
        # Get video data
        try:
            videos = self.client.get_videos_details([video_id])
            if not videos:
                return {"error": "Video not found", "video_id": video_id}
            video = videos[0]
        except Exception as e:
            return {"error": f"Failed to fetch video: {str(e)}", "video_id": video_id}
        
        snippet = video.get("snippet", {})
        statistics = video.get("statistics", {})
        content_details = video.get("contentDetails", {})
        
        # Get duration if not provided
        if not video_duration:
            duration_str = content_details.get("duration", "PT0S")
            video_duration = self._parse_duration(duration_str)
        
        title = snippet.get("title", "")
        description = snippet.get("description", "")
        
        # Analyze video for engagement opportunities
        poll_suggestions = self._suggest_polls(title, description, video_duration)
        card_suggestions = self._suggest_cards(title, description, video_duration, statistics)
        end_screen_suggestions = self._suggest_end_screens(title, description, video_duration)
        
        # Calculate engagement score
        engagement_score = self._calculate_engagement_score(
            statistics,
            poll_suggestions,
            card_suggestions,
            end_screen_suggestions
        )
        
        return {
            "video_id": video_id,
            "video_title": title,
            "video_duration_seconds": video_duration,
            "engagement_score": engagement_score,
            "suggestions": {
                "polls": poll_suggestions,
                "cards": card_suggestions,
                "end_screens": end_screen_suggestions
            },
            "priority_actions": self._identify_priority_actions(
                poll_suggestions,
                card_suggestions,
                end_screen_suggestions
            ),
            "best_practices": self._get_best_practices()
        }
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse ISO 8601 duration string to seconds."""
        import re
        # PT1H2M3S format
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    def _suggest_polls(
        self,
        title: str,
        description: str,
        duration: int
    ) -> List[Dict[str, Any]]:
        """Suggest poll questions and timing."""
        suggestions = []
        
        # Determine optimal poll count based on duration
        if duration < 60:  # Under 1 minute
            poll_count = 0
            recommendation = "Video too short for polls"
        elif duration < 180:  # 1-3 minutes
            poll_count = 1
        elif duration < 600:  # 3-10 minutes
            poll_count = 2
        else:  # 10+ minutes
            poll_count = 3
        
        if poll_count == 0:
            return [{
                "recommendation": recommendation,
                "priority": "low"
            }]
        
        # Generate poll suggestions based on content
        title_lower = title.lower()
        description_lower = description.lower()
        
        # Poll 1: Genre/style preference (early in video)
        if any(kw in title_lower or kw in description_lower for kw in ["rock", "psychedelic", "70s"]):
            suggestions.append({
                "question": "What's your favorite style?",
                "options": [
                    "Psychedelic Rock",
                    "Classic Rock",
                    "Folk Rock",
                    "All of the above"
                ],
                "timing_seconds": int(duration * 0.25),  # 25% into video
                "timing_percentage": 25,
                "reason": "Engage viewers early with genre preference",
                "priority": "high"
            })
        
        # Poll 2: Song preference (mid-video)
        if poll_count >= 2:
            suggestions.append({
                "question": "Which song should we cover next?",
                "options": [
                    "More Psychedelic Rock",
                    "Classic Turkish Folk",
                    "70s Rock Covers",
                    "Your suggestion in comments"
                ],
                "timing_seconds": int(duration * 0.50),  # 50% into video
                "timing_percentage": 50,
                "reason": "Gather content ideas and increase engagement",
                "priority": "high"
            })
        
        # Poll 3: Engagement check (late in video)
        if poll_count >= 3:
            suggestions.append({
                "question": "How did you discover this channel?",
                "options": [
                    "YouTube Search",
                    "Recommended Video",
                    "Social Media",
                    "Friend Recommendation"
                ],
                "timing_seconds": int(duration * 0.75),  # 75% into video
                "timing_percentage": 75,
                "reason": "Understand audience acquisition",
                "priority": "medium"
            })
        
        return suggestions
    
    def _suggest_cards(
        self,
        title: str,
        description: str,
        duration: int,
        statistics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Suggest cards (links to other videos/playlists)."""
        suggestions = []
        
        # Determine optimal card count
        if duration < 60:
            card_count = 0
        elif duration < 300:  # Under 5 minutes
            card_count = 2
        elif duration < 600:  # 5-10 minutes
            card_count = 3
        else:  # 10+ minutes
            card_count = 4
        
        if card_count == 0:
            return [{
                "recommendation": "Video too short for cards",
                "priority": "low"
            }]
        
        # Card 1: Related video/playlist (early)
        suggestions.append({
            "type": "video_or_playlist",
            "title": "More Psychedelic Anatolian Rock",
            "description": "Link to playlist or related video",
            "timing_seconds": int(duration * 0.30),
            "timing_percentage": 30,
            "reason": "Keep viewers engaged with related content",
            "priority": "high",
            "best_practices": [
                "Link to your most popular video",
                "Or link to a curated playlist",
                "Place when viewer is engaged (30% mark)"
            ]
        })
        
        # Card 2: Subscribe reminder (mid-video)
        if card_count >= 2:
            suggestions.append({
                "type": "channel",
                "title": "Subscribe for More",
                "description": "Subscribe to channel card",
                "timing_seconds": int(duration * 0.60),
                "timing_percentage": 60,
                "reason": "Convert engaged viewers to subscribers",
                "priority": "high",
                "best_practices": [
                    "Place after viewer has watched 60%",
                    "Only show if viewer is not subscribed",
                    "Use compelling call-to-action"
                ]
            })
        
        # Card 3: Latest video (late)
        if card_count >= 3:
            suggestions.append({
                "type": "video",
                "title": "Check Out Our Latest",
                "description": "Link to most recent video",
                "timing_seconds": int(duration * 0.80),
                "timing_percentage": 80,
                "reason": "Drive traffic to new content",
                "priority": "medium",
                "best_practices": [
                    "Link to your newest video",
                    "Place near end when viewer is committed",
                    "Use thumbnail that stands out"
                ]
            })
        
        # Card 4: Playlist continuation (very late)
        if card_count >= 4:
            suggestions.append({
                "type": "playlist",
                "title": "Continue Watching",
                "description": "Link to playlist to continue watching",
                "timing_seconds": int(duration * 0.90),
                "timing_percentage": 90,
                "reason": "Increase watch time and session duration",
                "priority": "medium",
                "best_practices": [
                    "Link to curated playlist",
                    "Place at 90% mark",
                    "Encourage binge-watching"
                ]
            })
        
        return suggestions
    
    def _suggest_end_screens(
        self,
        title: str,
        description: str,
        duration: int
    ) -> List[Dict[str, Any]]:
        """Suggest end screen elements."""
        suggestions = []
        
        # End screens should appear in last 20 seconds
        end_screen_start = max(duration - 20, int(duration * 0.85))
        
        # Element 1: Subscribe button
        suggestions.append({
            "type": "subscribe",
            "title": "Subscribe",
            "timing_seconds": end_screen_start,
            "duration_seconds": 20,
            "position": "top_left",
            "reason": "Convert viewers to subscribers",
            "priority": "high",
            "best_practices": [
                "Place in top-left corner (most visible)",
                "Show for last 20 seconds",
                "Use channel branding"
            ]
        })
        
        # Element 2: Next video
        suggestions.append({
            "type": "video",
            "title": "Watch Next",
            "description": "Link to next recommended video",
            "timing_seconds": end_screen_start,
            "duration_seconds": 20,
            "position": "top_right",
            "reason": "Increase watch time and session duration",
            "priority": "high",
            "best_practices": [
                "Link to your best-performing video",
                "Or link to next video in series",
                "Use compelling thumbnail"
            ]
        })
        
        # Element 3: Playlist
        suggestions.append({
            "type": "playlist",
            "title": "More Music",
            "description": "Link to playlist",
            "timing_seconds": end_screen_start,
            "duration_seconds": 20,
            "position": "bottom_left",
            "reason": "Encourage playlist watching",
            "priority": "medium",
            "best_practices": [
                "Link to curated playlist",
                "Place in bottom-left",
                "Use playlist thumbnail"
            ]
        })
        
        # Element 4: Channel link (if applicable)
        suggestions.append({
            "type": "channel",
            "title": "Visit Channel",
            "description": "Link to channel page",
            "timing_seconds": end_screen_start,
            "duration_seconds": 20,
            "position": "bottom_right",
            "reason": "Drive traffic to channel",
            "priority": "low",
            "best_practices": [
                "Optional element",
                "Use if you have multiple playlists",
                "Place in bottom-right"
            ]
        })
        
        return suggestions
    
    def _calculate_engagement_score(
        self,
        statistics: Dict[str, Any],
        poll_suggestions: List[Dict[str, Any]],
        card_suggestions: List[Dict[str, Any]],
        end_screen_suggestions: List[Dict[str, Any]]
    ) -> int:
        """Calculate engagement score based on current metrics and suggestions."""
        score = 50  # Base score
        
        # Check current engagement metrics
        view_count = int(statistics.get("viewCount", 0))
        like_count = int(statistics.get("likeCount", 0))
        comment_count = int(statistics.get("commentCount", 0))
        
        # Like ratio (good: >3%)
        if view_count > 0:
            like_ratio = (like_count / view_count) * 100
            if like_ratio >= 3:
                score += 15
            elif like_ratio >= 2:
                score += 10
            elif like_ratio >= 1:
                score += 5
        
        # Comment ratio (good: >0.5%)
        if view_count > 0:
            comment_ratio = (comment_count / view_count) * 100
            if comment_ratio >= 0.5:
                score += 15
            elif comment_ratio >= 0.3:
                score += 10
            elif comment_ratio >= 0.1:
                score += 5
        
        # Engagement elements score
        if len(poll_suggestions) >= 2:
            score += 10
        if len(card_suggestions) >= 2:
            score += 10
        if len(end_screen_suggestions) >= 3:
            score += 10
        
        return min(score, 100)
    
    def _identify_priority_actions(
        self,
        poll_suggestions: List[Dict[str, Any]],
        card_suggestions: List[Dict[str, Any]],
        end_screen_suggestions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify top priority actions for engagement improvement."""
        actions = []
        
        # Check for missing elements
        if not poll_suggestions or poll_suggestions[0].get("recommendation"):
            actions.append({
                "action": "Add Polls",
                "priority": "high",
                "impact": "high",
                "reason": "Polls significantly increase engagement and watch time",
                "quick_start": "Add a poll at 25% mark asking about genre preference"
            })
        
        if not card_suggestions or card_suggestions[0].get("recommendation"):
            actions.append({
                "action": "Add Cards",
                "priority": "high",
                "impact": "high",
                "reason": "Cards drive traffic to other videos and playlists",
                "quick_start": "Add a card at 30% mark linking to your playlist"
            })
        
        if len(end_screen_suggestions) < 3:
            actions.append({
                "action": "Optimize End Screens",
                "priority": "high",
                "impact": "high",
                "reason": "End screens convert viewers to subscribers and increase watch time",
                "quick_start": "Add subscribe button and next video in end screen"
            })
        
        # Prioritize by impact
        high_priority = [a for a in actions if a["priority"] == "high"]
        medium_priority = [a for a in actions if a["priority"] == "medium"]
        
        return high_priority + medium_priority
    
    def _get_best_practices(self) -> Dict[str, Any]:
        """Get best practices for engagement elements."""
        return {
            "polls": [
                "Ask questions relevant to your content",
                "Place polls at 25%, 50%, and 75% marks",
                "Use 4 options for better engagement",
                "Make polls interactive and fun",
                "Respond to poll results in comments"
            ],
            "cards": [
                "Link to your best-performing videos",
                "Place cards when viewer is engaged (30-60% mark)",
                "Don't overuse cards (2-4 per video is optimal)",
                "Use compelling thumbnails for card links",
                "Link to playlists to increase watch time"
            ],
            "end_screens": [
                "Always include subscribe button",
                "Link to next recommended video",
                "Show end screens for last 20 seconds",
                "Use 3-4 end screen elements maximum",
                "Place subscribe button in top-left (most visible)",
                "Link to playlists to encourage binge-watching"
            ],
            "general": [
                "Test different timings and see what works",
                "Monitor engagement metrics after adding elements",
                "Don't overwhelm viewers with too many elements",
                "Focus on quality over quantity",
                "Update suggestions based on performance data"
            ]
        }
    
    def get_engagement_strategy(
        self,
        channel_handle: str,
        video_count: int = 10
    ) -> Dict[str, Any]:
        """
        Get overall engagement strategy for a channel.
        
        Args:
            channel_handle: Channel handle
            video_count: Number of recent videos to analyze
            
        Returns:
            Channel-wide engagement strategy
        """
        try:
            channel_data = self.client.get_channel_by_handle(channel_handle)
            if not channel_data.get("items"):
                return {"error": f"Channel @{channel_handle} not found"}
            
            channel_id = channel_data["items"][0]["id"]
            videos = self.client.get_channel_videos(channel_id, max_results=video_count)
        except Exception as e:
            return {"error": f"Failed to fetch channel videos: {str(e)}"}
        
        # Analyze engagement across videos
        engagement_scores = []
        poll_usage = 0
        card_usage = 0
        end_screen_usage = 0
        
        for video in videos[:video_count]:
            video_id = video["id"]["videoId"]
            try:
                suggestions = self.suggest_engagement_elements(video_id)
                if "engagement_score" in suggestions:
                    engagement_scores.append(suggestions["engagement_score"])
                    
                    # Count suggested elements
                    if suggestions.get("suggestions", {}).get("polls"):
                        poll_usage += 1
                    if suggestions.get("suggestions", {}).get("cards"):
                        card_usage += 1
                    if suggestions.get("suggestions", {}).get("end_screens"):
                        end_screen_usage += 1
            except Exception:
                pass
        
        avg_engagement = sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0
        
        return {
            "channel_handle": channel_handle,
            "videos_analyzed": len(engagement_scores),
            "average_engagement_score": round(avg_engagement, 1),
            "element_usage": {
                "polls": f"{poll_usage}/{len(engagement_scores)} videos",
                "cards": f"{card_usage}/{len(engagement_scores)} videos",
                "end_screens": f"{end_screen_usage}/{len(engagement_scores)} videos"
            },
            "recommendations": [
                "Add polls to increase engagement",
                "Use cards to drive traffic between videos",
                "Optimize end screens for subscriber conversion",
                "Test different timings and measure results"
            ] if avg_engagement < 70 else [
                "Your engagement strategy looks good!",
                "Continue testing and optimizing",
                "Monitor metrics and adjust as needed"
            ]
        }

