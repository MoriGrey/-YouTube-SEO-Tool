"""
Competitor Analysis Module
Analyze competitor channels and strategies.
"""

from typing import Dict, Any, List, Optional
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient


class CompetitorAnalyzer:
    """
    Competitor analysis with AGI-powered insights.
    
    AGI Paradigm: Omnipresent Data Mining
    - Discovers competitor strategies
    - Identifies market gaps
    - Provides competitive intelligence
    """
    
    def __init__(self, client: YouTubeClient):
        self.client = client
    
    def find_competitors(
        self,
        niche_keywords: List[str],
        max_competitors: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find competitor channels in the niche.
        
        Args:
            niche_keywords: Keywords to search for competitors
            max_competitors: Maximum number of competitors to find
        
        Returns:
            List of competitor channel information
        """
        competitors = []
        seen_channels = set()
        
        for keyword in niche_keywords:
            # Search for videos
            results = self.client.search_videos(
                keyword,
                max_results=25,
                order="viewCount",
                region_code="TR"
            )
            
            for result in results:
                channel_id = result["snippet"]["channelId"]
                channel_title = result["snippet"]["channelTitle"]
                
                # Skip if already seen
                if channel_id in seen_channels:
                    continue
                
                seen_channels.add(channel_id)
                
                # Get channel details
                try:
                    channel_data = self.client.get_channel_by_id(channel_id)
                    if channel_data.get("items"):
                        channel = channel_data["items"][0]
                        stats = channel["statistics"]
                        snippet = channel["snippet"]
                        
                        # Get channel handle (customUrl) if available
                        channel_handle = snippet.get("customUrl", "")
                        if channel_handle:
                            channel_handle = channel_handle.lstrip("@")
                        
                        # Calculate relevance score based on subscribers (simple heuristic)
                        subscribers = int(stats.get("subscriberCount", 0))
                        relevance_score = min(subscribers / 1000000, 1.0) if subscribers > 0 else 0.0
                        
                        competitors.append({
                            "channel_id": channel_id,
                            "channel_title": channel_title,  # Keep for backward compatibility
                            "title": channel_title,  # Also add as title
                            "channel_handle": channel_handle or channel_id[:20],  # Use handle or first 20 chars of ID
                            "subscribers": subscribers,
                            "total_views": int(stats.get("viewCount", 0)),
                            "video_count": int(stats.get("videoCount", 0)),
                            "description": snippet.get("description", "")[:200],
                            "relevance_score": relevance_score
                        })
                        
                        if len(competitors) >= max_competitors:
                            break
                except Exception:
                    continue
            
            if len(competitors) >= max_competitors:
                break
        
        # Sort by subscribers
        competitors.sort(key=lambda x: x["subscribers"], reverse=True)
        return competitors
    
    def analyze_competitor(
        self,
        channel_id: str,
        max_videos: int = 20
    ) -> Dict[str, Any]:
        """
        Analyze a specific competitor channel.
        
        Returns:
            Detailed competitor analysis
        """
        # Get channel info
        channel_data = self.client.get_channel_by_id(channel_id)
        if not channel_data.get("items"):
            raise ValueError(f"Channel {channel_id} not found")
        
        channel = channel_data["items"][0]
        stats = channel["statistics"]
        
        # Get videos
        videos = self.client.get_channel_videos(channel_id, max_results=max_videos)
        
        # Analyze video performance
        if videos:
            views = [int(v.get("statistics", {}).get("viewCount", 0)) for v in videos]
            likes = [int(v.get("statistics", {}).get("likeCount", 0)) for v in videos]
            
            avg_views = sum(views) / len(views) if views else 0
            avg_likes = sum(likes) / len(likes) if likes else 0
            
            # Analyze titles
            titles = [v["snippet"]["title"] for v in videos]
            title_patterns = self._analyze_title_patterns(titles)
            
            # Analyze upload frequency
            upload_frequency = self._analyze_upload_frequency(videos)
        else:
            avg_views = 0
            avg_likes = 0
            title_patterns = {}
            upload_frequency = {}
        
        return {
            "channel_info": {
                "id": channel_id,
                "title": channel["snippet"]["title"],
                "subscribers": int(stats.get("subscriberCount", 0)),
                "total_views": int(stats.get("viewCount", 0)),
                "video_count": int(stats.get("videoCount", 0))
            },
            "performance": {
                "average_views": avg_views,
                "average_likes": avg_likes,
                "engagement_rate": (avg_likes / max(avg_views, 1)) * 100 if avg_views > 0 else 0
            },
            "content_strategy": {
                "title_patterns": title_patterns,
                "upload_frequency": upload_frequency
            },
            "strengths": self._identify_strengths(avg_views, avg_likes, upload_frequency),
            "opportunities": self._identify_opportunities(title_patterns, upload_frequency)
        }
    
    def _analyze_title_patterns(self, titles: List[str]) -> Dict[str, Any]:
        """Analyze title patterns used by competitor."""
        if not titles:
            return {}
        
        # Common patterns
        has_pipe = sum(1 for t in "|" in t for t in titles)
        has_brackets = sum(1 for t in "[" in t or "]" in t for t in titles)
        has_numbers = sum(1 for t in any(c.isdigit() for c in t) for t in titles)
        
        # Average length
        avg_length = sum(len(t) for t in titles) / len(titles) if titles else 0
        
        # Common words
        from collections import Counter
        all_words = []
        for title in titles:
            words = title.lower().split()
            all_words.extend([w for w in words if len(w) > 3])
        
        common_words = Counter(all_words).most_common(10)
        
        return {
            "average_length": avg_length,
            "uses_pipe_separator": has_pipe > len(titles) * 0.5,
            "uses_brackets": has_brackets > len(titles) * 0.3,
            "uses_numbers": has_numbers > len(titles) * 0.3,
            "common_words": [{"word": word, "count": count} for word, count in common_words]
        }
    
    def _analyze_upload_frequency(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze upload frequency."""
        if not videos:
            return {}
        
        from datetime import datetime
        
        dates = []
        for video in videos:
            pub_date = video["snippet"].get("publishedAt", "")
            if pub_date:
                try:
                    dates.append(datetime.fromisoformat(pub_date.replace("Z", "+00:00")))
                except:
                    pass
        
        if len(dates) < 2:
            return {"frequency": "Unknown", "days_between": 0}
        
        dates.sort()
        days_between = []
        for i in range(1, len(dates)):
            days_between.append((dates[i] - dates[i-1]).days)
        
        avg_days = sum(days_between) / len(days_between) if days_between else 0
        
        if avg_days < 7:
            frequency = "Very Active (multiple per week)"
        elif avg_days < 14:
            frequency = "Active (weekly)"
        elif avg_days < 30:
            frequency = "Moderate (bi-weekly)"
        else:
            frequency = "Infrequent (monthly or less)"
        
        return {
            "frequency": frequency,
            "average_days_between": avg_days,
            "videos_analyzed": len(videos)
        }
    
    def _identify_strengths(
        self,
        avg_views: float,
        avg_likes: float,
        upload_frequency: Dict[str, Any]
    ) -> List[str]:
        """Identify competitor strengths."""
        strengths = []
        
        if avg_views > 10000:
            strengths.append("High view counts indicate strong content quality or marketing")
        
        if avg_likes / max(avg_views, 1) > 0.02:
            strengths.append("High engagement rate suggests loyal audience")
        
        freq = upload_frequency.get("frequency", "")
        if "Very Active" in freq or "Active" in freq:
            strengths.append("Consistent upload schedule builds audience retention")
        
        return strengths
    
    def _identify_opportunities(
        self,
        title_patterns: Dict[str, Any],
        upload_frequency: Dict[str, Any]
    ) -> List[str]:
        """Identify opportunities based on competitor analysis."""
        opportunities = []
        
        # Title opportunities
        if title_patterns.get("uses_pipe_separator"):
            opportunities.append("Consider using pipe separator (|) in titles for better organization")
        
        if title_patterns.get("average_length", 0) > 50:
            opportunities.append("Competitors use longer titles - test longer, more descriptive titles")
        
        # Upload frequency opportunities
        freq = upload_frequency.get("frequency", "")
        if "Infrequent" in freq:
            opportunities.append("Competitor uploads infrequently - you can gain advantage with consistent uploads")
        
        return opportunities
    
    def compare_with_competitors(
        self,
        your_channel_id: str,
        competitor_ids: List[str]
    ) -> Dict[str, Any]:
        """Compare your channel with competitors."""
        your_analysis = self.analyze_competitor(your_channel_id)
        competitor_analyses = [self.analyze_competitor(cid) for cid in competitor_ids]
        
        # Calculate averages
        avg_subscribers = sum(c["channel_info"]["subscribers"] for c in competitor_analyses) / len(competitor_analyses) if competitor_analyses else 0
        avg_views = sum(c["performance"]["average_views"] for c in competitor_analyses) / len(competitor_analyses) if competitor_analyses else 0
        
        your_subs = your_analysis["channel_info"]["subscribers"]
        your_views = your_analysis["performance"]["average_views"]
        
        return {
            "your_channel": {
                "subscribers": your_subs,
                "average_views": your_views
            },
            "competitor_averages": {
                "subscribers": avg_subscribers,
                "average_views": avg_views
            },
            "comparison": {
                "subscriber_gap": avg_subscribers - your_subs,
                "view_gap": avg_views - your_views,
                "position": "Below Average" if your_subs < avg_subscribers else "Above Average"
            },
            "recommendations": self._generate_comparison_recommendations(
                your_subs, avg_subscribers, your_views, avg_views
            )
        }
    
    def analyze_gaps(
        self,
        your_channel_handle: str,
        competitor_handles: List[str],
        max_videos_per_channel: int = 10
    ) -> Dict[str, Any]:
        """
        Perform detailed gap analysis between your channel and competitors.
        
        Args:
            your_channel_handle: Your channel handle
            competitor_handles: List of competitor channel handles
            max_videos_per_channel: Maximum videos to analyze per channel
            
        Returns:
            Detailed gap analysis with content, keyword, timing, tag, and description gaps
        """
        gaps = {
            "content_gaps": [],
            "keyword_gaps": [],
            "timing_gaps": {},
            "tag_gaps": [],
            "description_gaps": {},
            "thumbnail_gaps": {},
            "opportunities": []
        }
        
        try:
            # Get your channel data
            your_channel_data = self.client.get_channel_by_handle(your_channel_handle)
            if not your_channel_data.get("items"):
                return {"error": f"Channel @{your_channel_handle} not found"}
            
            your_channel_id = your_channel_data["items"][0]["id"]
            your_analysis = self.analyze_competitor(your_channel_id)
            your_videos = self.client.get_channel_videos(your_channel_id, max_results=max_videos_per_channel)
            
            # Analyze competitors
            competitor_data = []
            all_competitor_keywords = set()
            all_competitor_tags = set()
            competitor_upload_times = []
            competitor_descriptions = []
            
            for competitor_handle in competitor_handles:
                try:
                    comp_data = self.client.get_channel_by_handle(competitor_handle)
                    if comp_data.get("items"):
                        comp_id = comp_data["items"][0]["id"]
                        comp_analysis = self.analyze_competitor(comp_id)
                        comp_videos = self.client.get_channel_videos(comp_id, max_results=max_videos_per_channel)
                        
                        competitor_data.append({
                            "handle": competitor_handle,
                            "analysis": comp_analysis,
                            "videos": comp_videos
                        })
                        
                        # Extract keywords from competitor videos
                        for video in comp_videos:
                            title = video.get("snippet", {}).get("title", "")
                            description = video.get("snippet", {}).get("description", "")
                            tags = video.get("snippet", {}).get("tags", [])
                            
                            # Extract keywords from title and description
                            title_words = [w.lower() for w in title.split() if len(w) > 4]
                            desc_words = [w.lower() for w in description.split()[:100] if len(w) > 4]
                            all_competitor_keywords.update(title_words + desc_words)
                            
                            # Collect tags
                            all_competitor_tags.update([t.lower() for t in tags])
                            
                            # Collect upload times
                            published = video.get("snippet", {}).get("publishedAt", "")
                            if published:
                                try:
                                    from datetime import datetime
                                    pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                                    competitor_upload_times.append(pub_date.hour)
                                except:
                                    pass
                            
                            # Collect description patterns
                            if description:
                                desc_length = len(description)
                                desc_word_count = len(description.split())
                                competitor_descriptions.append({
                                    "length": desc_length,
                                    "word_count": desc_word_count,
                                    "has_links": "http" in description.lower(),
                                    "hashtag_count": description.count("#")
                                })
                except Exception as e:
                    continue
            
            # Analyze your channel
            your_keywords = set()
            your_tags = set()
            your_upload_times = []
            your_descriptions = []
            
            for video in your_videos:
                title = video.get("snippet", {}).get("title", "")
                description = video.get("snippet", {}).get("description", "")
                tags = video.get("snippet", {}).get("tags", [])
                
                title_words = [w.lower() for w in title.split() if len(w) > 4]
                desc_words = [w.lower() for w in description.split()[:100] if len(w) > 4]
                your_keywords.update(title_words + desc_words)
                your_tags.update([t.lower() for t in tags])
                
                published = video.get("snippet", {}).get("publishedAt", "")
                if published:
                    try:
                        from datetime import datetime
                        pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                        your_upload_times.append(pub_date.hour)
                    except:
                        pass
                
                if description:
                    desc_length = len(description)
                    desc_word_count = len(description.split())
                    your_descriptions.append({
                        "length": desc_length,
                        "word_count": desc_word_count,
                        "has_links": "http" in description.lower(),
                        "hashtag_count": description.count("#")
                    })
            
            # Content Gaps: Keywords competitors use but you don't
            missing_keywords = all_competitor_keywords - your_keywords
            gaps["keyword_gaps"] = sorted(list(missing_keywords))[:20]  # Top 20 missing keywords
            
            # Tag Gaps: Tags competitors use but you don't
            missing_tags = all_competitor_tags - your_tags
            gaps["tag_gaps"] = sorted(list(missing_tags))[:30]  # Top 30 missing tags
            
            # Timing Gaps: Upload time patterns
            if competitor_upload_times and your_upload_times:
                from collections import Counter
                comp_time_dist = Counter(competitor_upload_times)
                your_time_dist = Counter(your_upload_times)
                
                # Find most common competitor upload times
                most_common_comp_times = comp_time_dist.most_common(3)
                gaps["timing_gaps"] = {
                    "competitor_peak_hours": [hour for hour, count in most_common_comp_times],
                    "your_peak_hours": [hour for hour, count in your_time_dist.most_common(3)],
                    "recommendation": "Consider uploading at competitor peak hours if different"
                }
            
            # Description Gaps
            if competitor_descriptions and your_descriptions:
                avg_comp_length = sum(d["length"] for d in competitor_descriptions) / len(competitor_descriptions)
                avg_your_length = sum(d["length"] for d in your_descriptions) / len(your_descriptions)
                
                avg_comp_words = sum(d["word_count"] for d in competitor_descriptions) / len(competitor_descriptions)
                avg_your_words = sum(d["word_count"] for d in your_descriptions) / len(your_descriptions)
                
                comp_has_links = sum(1 for d in competitor_descriptions if d["has_links"]) / len(competitor_descriptions)
                your_has_links = sum(1 for d in your_descriptions if d["has_links"]) / len(your_descriptions)
                
                avg_comp_hashtags = sum(d["hashtag_count"] for d in competitor_descriptions) / len(competitor_descriptions)
                avg_your_hashtags = sum(d["hashtag_count"] for d in your_descriptions) / len(your_descriptions)
                
                gaps["description_gaps"] = {
                    "length_gap": avg_comp_length - avg_your_length,
                    "word_count_gap": avg_comp_words - avg_your_words,
                    "links_usage_gap": comp_has_links - your_has_links,
                    "hashtag_gap": avg_comp_hashtags - avg_your_hashtags,
                    "recommendations": []
                }
                
                if avg_your_length < avg_comp_length * 0.8:
                    gaps["description_gaps"]["recommendations"].append(
                        f"Expand descriptions - competitors average {int(avg_comp_length)} chars, you average {int(avg_your_length)}"
                    )
                if avg_your_words < avg_comp_words * 0.8:
                    gaps["description_gaps"]["recommendations"].append(
                        f"Increase word count - competitors average {int(avg_comp_words)} words, you average {int(avg_your_words)}"
                    )
                if your_has_links < comp_has_links * 0.8:
                    gaps["description_gaps"]["recommendations"].append(
                        "Add more links to descriptions (channel, playlists, social media)"
                    )
                if avg_your_hashtags < avg_comp_hashtags * 0.8:
                    gaps["description_gaps"]["recommendations"].append(
                        f"Increase hashtags - competitors average {int(avg_comp_hashtags)}, you average {int(avg_your_hashtags)}"
                    )
            
            # Content Gaps: Title patterns
            competitor_title_patterns = []
            your_title_patterns = []
            
            for comp in competitor_data:
                for video in comp.get("videos", []):
                    title = video.get("snippet", {}).get("title", "")
                    if title:
                        competitor_title_patterns.append({
                            "length": len(title),
                            "has_pipe": "|" in title,
                            "has_brackets": "[" in title or "]" in title,
                            "has_question": "?" in title,
                            "has_numbers": any(c.isdigit() for c in title)
                        })
            
            for video in your_videos:
                title = video.get("snippet", {}).get("title", "")
                if title:
                    your_title_patterns.append({
                        "length": len(title),
                        "has_pipe": "|" in title,
                        "has_brackets": "[" in title or "]" in title,
                        "has_question": "?" in title,
                        "has_numbers": any(c.isdigit() for c in title)
                    })
            
            if competitor_title_patterns and your_title_patterns:
                comp_avg_length = sum(t["length"] for t in competitor_title_patterns) / len(competitor_title_patterns)
                your_avg_length = sum(t["length"] for t in your_title_patterns) / len(your_title_patterns)
                
                comp_pipe_usage = sum(1 for t in competitor_title_patterns if t["has_pipe"]) / len(competitor_title_patterns)
                your_pipe_usage = sum(1 for t in your_title_patterns if t["has_pipe"]) / len(your_title_patterns)
                
                gaps["content_gaps"].append({
                    "type": "title_length",
                    "gap": comp_avg_length - your_avg_length,
                    "recommendation": f"Consider longer titles - competitors average {int(comp_avg_length)} chars"
                })
                
                if comp_pipe_usage > your_pipe_usage * 1.2:
                    gaps["content_gaps"].append({
                        "type": "title_formatting",
                        "gap": "Competitors use pipe (|) separator more frequently",
                        "recommendation": "Consider using pipe separator in titles: 'Title | Category | Year'"
                    })
            
            # Generate Opportunities
            opportunities = []
            
            # Keyword opportunities
            if gaps["keyword_gaps"]:
                opportunities.append({
                    "type": "keyword",
                    "priority": "high",
                    "title": "Missing Keywords",
                    "description": f"Competitors use {len(gaps['keyword_gaps'])} keywords you don't",
                    "action": f"Consider adding these keywords: {', '.join(gaps['keyword_gaps'][:5])}"
                })
            
            # Tag opportunities
            if gaps["tag_gaps"]:
                opportunities.append({
                    "type": "tag",
                    "priority": "high",
                    "title": "Missing Tags",
                    "description": f"Competitors use {len(gaps['tag_gaps'])} tags you don't",
                    "action": f"Consider adding these tags: {', '.join(gaps['tag_gaps'][:10])}"
                })
            
            # Timing opportunities
            if gaps["timing_gaps"].get("competitor_peak_hours"):
                opportunities.append({
                    "type": "timing",
                    "priority": "medium",
                    "title": "Upload Timing",
                    "description": "Competitors upload at different times",
                    "action": f"Consider uploading at hours: {', '.join(map(str, gaps['timing_gaps']['competitor_peak_hours']))}"
                })
            
            gaps["opportunities"] = opportunities
            
            return gaps
            
        except Exception as e:
            return {"error": f"Gap analysis failed: {str(e)}"}
    
    def _generate_comparison_recommendations(
        self,
        your_subs: int,
        avg_subs: float,
        your_views: float,
        avg_views: float
    ) -> List[str]:
        """Generate recommendations based on comparison."""
        recommendations = []
        
        if your_subs < avg_subs * 0.5:
            recommendations.append("Focus on subscriber growth - consider collaborations or cross-promotion")
        
        if your_views < avg_views * 0.5:
            recommendations.append("Improve video discoverability - optimize titles, thumbnails, and tags")
        
        if your_views > avg_views * 1.5 and your_subs < avg_subs:
            recommendations.append("High views but low subscribers - add stronger calls-to-action to subscribe")
        
        return recommendations

