"""
Video SEO Audit Module
Automated SEO scoring and analysis for YouTube videos.

AGI Paradigm: Self-Evolving Architecture
- Analyzes all SEO elements (title, description, tags, thumbnail)
- Provides comprehensive SEO score (0-100)
- Generates actionable improvement recommendations
"""

from typing import Dict, Any, List, Optional
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.title_optimizer import TitleOptimizer
from src.modules.description_generator import DescriptionGenerator
from src.modules.tag_suggester import TagSuggester
from src.modules.keyword_researcher import KeywordResearcher


class VideoSEOAudit:
    """
    Comprehensive video SEO audit system.
    
    AGI Paradigm: Self-Evolving Architecture
    - Analyzes all SEO elements holistically
    - Provides actionable recommendations
    - Learns from successful optimizations
    """
    
    def __init__(
        self,
        client: YouTubeClient,
        keyword_researcher: KeywordResearcher,
        title_optimizer: TitleOptimizer,
        description_generator: DescriptionGenerator,
        tag_suggester: TagSuggester
    ):
        self.client = client
        self.keyword_researcher = keyword_researcher
        self.title_optimizer = title_optimizer
        self.description_generator = description_generator
        self.tag_suggester = tag_suggester
    
    def audit_video(
        self,
        video_id: str,
        channel_handle: Optional[str] = None,
        niche: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive SEO audit for a video.
        
        Args:
            video_id: YouTube video ID
            channel_handle: Channel handle (optional, for context)
            
        Returns:
            Complete SEO audit report with scores and recommendations
        """
        # Get video data
        try:
            videos = self.client.get_videos_details([video_id])
            if not videos:
                return {
                    "error": "Video not found",
                    "video_id": video_id
                }
            video = videos[0]
        except Exception as e:
            return {
                "error": f"Failed to fetch video: {str(e)}",
                "video_id": video_id
            }
        
        snippet = video.get("snippet", {})
        statistics = video.get("statistics", {})
        
        # Extract video elements
        title = snippet.get("title", "")
        description = snippet.get("description", "")
        tags = snippet.get("tags", [])
        thumbnail_url = snippet.get("thumbnails", {}).get("high", {}).get("url", "")
        
        # Analyze each element
        title_audit = self._audit_title(title, niche)
        description_audit = self._audit_description(description)
        tags_audit = self._audit_tags(tags, title, niche)
        thumbnail_audit = self._audit_thumbnail(thumbnail_url, title)
        
        # Calculate overall SEO score
        overall_score = self._calculate_overall_score(
            title_audit,
            description_audit,
            tags_audit,
            thumbnail_audit
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            title_audit,
            description_audit,
            tags_audit,
            thumbnail_audit,
            overall_score
        )
        
        # Priority actions
        priority_actions = self._identify_priority_actions(
            title_audit,
            description_audit,
            tags_audit,
            thumbnail_audit
        )
        
        return {
            "video_id": video_id,
            "video_title": title,
            "timestamp": video.get("snippet", {}).get("publishedAt", ""),
            "overall_seo_score": overall_score,
            "seo_grade": self._get_seo_grade(overall_score),
            "audit_details": {
                "title": title_audit,
                "description": description_audit,
                "tags": tags_audit,
                "thumbnail": thumbnail_audit
            },
            "recommendations": recommendations,
            "priority_actions": priority_actions,
            "improvement_potential": self._calculate_improvement_potential(
                title_audit,
                description_audit,
                tags_audit,
                thumbnail_audit
            )
        }
    
    def _audit_title(self, title: str, niche: Optional[str] = None) -> Dict[str, Any]:
        """Audit video title for SEO."""
        if not title:
            return {
                "score": 0,
                "status": "missing",
                "issues": ["Title is missing"],
                "recommendations": ["Add a title to your video"]
            }
        
        # Analyze title SEO
        try:
            seo_analysis = self.keyword_researcher.analyze_title_seo(title, niche=niche)
        except Exception:
            seo_analysis = {
                "seo_score": 0,
                "length": len(title),
                "keywords_found": [],
                "recommendation": "Unable to analyze title"
            }
        
        # Calculate score
        score = 0
        issues = []
        recommendations = []
        
        # Length check (optimal: 40-60 chars)
        length = len(title)
        if 40 <= length <= 60:
            score += 30
        elif 30 <= length < 40:
            score += 20
            recommendations.append("Consider expanding title to 40-60 characters for better SEO")
        elif 60 < length <= 70:
            score += 20
            recommendations.append("Title is slightly long - consider shortening to 60 characters")
        else:
            issues.append(f"Title length ({length} chars) is outside optimal range (40-60)")
            if length < 30:
                recommendations.append("Title is too short - expand to at least 40 characters")
            else:
                recommendations.append("Title is too long - shorten to 60 characters or less")
        
        # SEO score from keyword researcher
        seo_score = seo_analysis.get("seo_score", 0)
        score += min(seo_score, 40)  # Max 40 points from keyword analysis
        
        # Keyword presence
        keywords_found = seo_analysis.get("keywords_found", [])
        if len(keywords_found) >= 2:
            score += 20
        elif len(keywords_found) == 1:
            score += 10
            recommendations.append("Add more relevant keywords to title")
        else:
            issues.append("No relevant keywords found in title")
            if niche:
                recommendations.append(f"Include niche keywords (e.g., '{niche.title()}')")
            else:
                recommendations.append("Include relevant niche keywords in title")
        
        # First 30 characters check (most important for search)
        first_30 = title[:30].lower()
        # Generate keywords from niche if provided
        if niche:
            niche_keywords = niche.lower().split()
            has_keywords_in_first_30 = any(kw in first_30 for kw in niche_keywords)
        else:
            # Fallback to general music keywords
            has_keywords_in_first_30 = any(
                kw in first_30 for kw in ["music", "song", "cover", "video"]
            )
        if has_keywords_in_first_30:
            score += 10
        else:
            recommendations.append("Include main keywords in first 30 characters of title")
        
        # Final score (0-100)
        final_score = min(score, 100)
        
        # Status
        if final_score >= 80:
            status = "excellent"
        elif final_score >= 60:
            status = "good"
        elif final_score >= 40:
            status = "needs_improvement"
        else:
            status = "poor"
        
        return {
            "score": final_score,
            "status": status,
            "title": title,
            "length": length,
            "keywords_found": keywords_found,
            "seo_analysis": seo_analysis,
            "issues": issues,
            "recommendations": recommendations if recommendations else ["Title looks good!"]
        }
    
    def _audit_description(self, description: str) -> Dict[str, Any]:
        """Audit video description for SEO."""
        if not description:
            return {
                "score": 0,
                "status": "missing",
                "issues": ["Description is missing"],
                "recommendations": ["Add a description to your video - it's crucial for SEO"]
            }
        
        word_count = len(description.split())
        char_count = len(description)
        hashtag_count = description.count("#")
        
        # Check first 125 characters (visible in search)
        first_125 = description[:125]
        keyword_density = {
            "psychedelic": first_125.lower().count("psychedelic"),
            "anatolian": first_125.lower().count("anatolian"),
            "rock": first_125.lower().count("rock"),
            "turkish": first_125.lower().count("turkish")
        }
        
        # Calculate score
        score = 0
        issues = []
        recommendations = []
        
        # Word count (optimal: 200+ words)
        if word_count >= 200:
            score += 25
        elif word_count >= 150:
            score += 15
            recommendations.append("Expand description to at least 200 words for better SEO")
        elif word_count >= 100:
            score += 10
            recommendations.append("Description is too short - aim for 200+ words")
        else:
            issues.append(f"Description is too short ({word_count} words)")
            recommendations.append("Significantly expand description - aim for 200+ words")
        
        # Character count (optimal: 1000+ chars)
        if char_count >= 1000:
            score += 20
        elif char_count >= 500:
            score += 10
            recommendations.append("Expand description to 1000+ characters")
        else:
            issues.append(f"Description is too short ({char_count} characters)")
            recommendations.append("Expand description to at least 1000 characters")
        
        # Hashtag count (optimal: 10-15)
        if 10 <= hashtag_count <= 15:
            score += 15
        elif 5 <= hashtag_count < 10:
            score += 10
            recommendations.append("Add more hashtags (10-15 is optimal)")
        elif hashtag_count > 15:
            score += 10
            recommendations.append("Consider reducing hashtags to 10-15 for better focus")
        else:
            issues.append(f"Not enough hashtags ({hashtag_count})")
            recommendations.append("Add 10-15 relevant hashtags")
        
        # Keyword density in first 125 chars
        total_keywords = sum(keyword_density.values())
        if total_keywords >= 3:
            score += 20
        elif total_keywords >= 2:
            score += 10
            recommendations.append("Include more keywords in first 125 characters (visible in search)")
        else:
            issues.append("Low keyword density in first 125 characters")
            recommendations.append("Add more keywords to the beginning of description")
        
        # Links check
        has_links = "http" in description.lower() or "youtube.com" in description.lower()
        if has_links:
            score += 10
        else:
            recommendations.append("Add links to your channel, playlists, or social media")
        
        # Structure check (sections, formatting)
        has_structure = any(marker in description for marker in ["━━━", "---", "###", "**"])
        if has_structure:
            score += 10
        else:
            recommendations.append("Use formatting (dividers, sections) to improve readability")
        
        # Final score
        final_score = min(score, 100)
        
        # Status
        if final_score >= 80:
            status = "excellent"
        elif final_score >= 60:
            status = "good"
        elif final_score >= 40:
            status = "needs_improvement"
        else:
            status = "poor"
        
        return {
            "score": final_score,
            "status": status,
            "word_count": word_count,
            "character_count": char_count,
            "hashtag_count": hashtag_count,
            "keyword_density_first_125": keyword_density,
            "has_links": has_links,
            "has_structure": has_structure,
            "issues": issues,
            "recommendations": recommendations if recommendations else ["Description looks good!"]
        }
    
    def _audit_tags(self, tags: List[str], title: str, niche: Optional[str] = None) -> Dict[str, Any]:
        """Audit video tags for SEO."""
        if not tags:
            return {
                "score": 0,
                "status": "missing",
                "issues": ["Tags are missing"],
                "recommendations": ["Add tags to your video - they help with discoverability"]
            }
        
        tag_count = len(tags)
        total_chars = sum(len(tag) for tag in tags)
        avg_length = total_chars / tag_count if tag_count > 0 else 0
        
        # Check keyword coverage - generate from niche if provided
        if niche:
            keywords = niche.lower().split()
        else:
            # Fallback to general music keywords
            keywords = ["music", "song", "cover", "video"]
        coverage = sum(1 for kw in keywords if any(kw in tag.lower() for tag in tags))
        
        # Calculate score
        score = 0
        issues = []
        recommendations = []
        
        # Tag count (optimal: 20-30)
        if 20 <= tag_count <= 30:
            score += 30
        elif 15 <= tag_count < 20:
            score += 20
            recommendations.append("Add more tags (20-30 is optimal)")
        elif 30 < tag_count <= 40:
            score += 20
            recommendations.append("Consider reducing tags to 20-30 for better focus")
        else:
            if tag_count < 15:
                issues.append(f"Not enough tags ({tag_count})")
                recommendations.append("Add more tags - aim for 20-30 tags")
            else:
                recommendations.append("Too many tags - consider reducing to 20-30")
        
        # Keyword coverage
        coverage_score = (coverage / len(keywords)) * 30
        score += coverage_score
        if coverage < len(keywords):
            missing = [kw for kw in keywords if not any(kw in tag.lower() for tag in tags)]
            if missing:
                recommendations.append(f"Add tags with keywords: {', '.join(missing)}")
        
        # Average length (optimal: 10-20 chars)
        if 10 <= avg_length <= 20:
            score += 20
        elif 8 <= avg_length <= 25:
            score += 10
        else:
            recommendations.append("Optimize tag lengths (10-20 characters is optimal)")
        
        # Tag relevance (check if tags match title)
        title_lower = title.lower()
        relevant_tags = sum(1 for tag in tags if any(word in title_lower for word in tag.lower().split()))
        relevance_score = min((relevant_tags / max(tag_count, 1)) * 20, 20)
        score += relevance_score
        
        if relevance_score < 15:
            recommendations.append("Ensure tags are relevant to your video title")
        
        # Final score
        final_score = min(score, 100)
        
        # Status
        if final_score >= 80:
            status = "excellent"
        elif final_score >= 60:
            status = "good"
        elif final_score >= 40:
            status = "needs_improvement"
        else:
            status = "poor"
        
        return {
            "score": final_score,
            "status": status,
            "tag_count": tag_count,
            "tags": tags,
            "average_length": avg_length,
            "keyword_coverage": f"{coverage}/{len(keywords)}",
            "relevance_score": relevance_score,
            "issues": issues,
            "recommendations": recommendations if recommendations else ["Tags look good!"]
        }
    
    def _audit_thumbnail(self, thumbnail_url: str, title: str) -> Dict[str, Any]:
        """Audit video thumbnail for SEO and CTR."""
        if not thumbnail_url:
            return {
                "score": 50,  # Default score if no thumbnail URL available
                "status": "unknown",
                "issues": ["Thumbnail URL not available"],
                "recommendations": ["Ensure thumbnail is eye-catching and relevant to title"]
            }
        
        # Basic thumbnail analysis (can be enhanced with image processing)
        score = 50  # Base score
        issues = []
        recommendations = []
        
        # Note: Full thumbnail analysis would require image processing
        # For now, we provide general recommendations
        
        recommendations.extend([
            "Use high contrast colors for visibility",
            "Include text overlay with main keywords",
            "Show faces or recognizable elements",
            "Use bright, eye-catching colors",
            "Ensure thumbnail is clear even at small sizes",
            "Make thumbnail relevant to video title"
        ])
        
        return {
            "score": score,
            "status": "needs_manual_review",
            "thumbnail_url": thumbnail_url,
            "issues": issues,
            "recommendations": recommendations,
            "note": "Full thumbnail analysis requires image processing. Use these general guidelines."
        }
    
    def _calculate_overall_score(
        self,
        title_audit: Dict[str, Any],
        description_audit: Dict[str, Any],
        tags_audit: Dict[str, Any],
        thumbnail_audit: Dict[str, Any]
    ) -> int:
        """Calculate overall SEO score (weighted average)."""
        # Weights (title is most important)
        weights = {
            "title": 0.35,
            "description": 0.30,
            "tags": 0.25,
            "thumbnail": 0.10
        }
        
        title_score = title_audit.get("score", 0)
        description_score = description_audit.get("score", 0)
        tags_score = tags_audit.get("score", 0)
        thumbnail_score = thumbnail_audit.get("score", 0)
        
        overall = (
            title_score * weights["title"] +
            description_score * weights["description"] +
            tags_score * weights["tags"] +
            thumbnail_score * weights["thumbnail"]
        )
        
        return int(overall)
    
    def _get_seo_grade(self, score: int) -> str:
        """Get SEO grade from score."""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B+"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C+"
        elif score >= 40:
            return "C"
        else:
            return "D"
    
    def _generate_recommendations(
        self,
        title_audit: Dict[str, Any],
        description_audit: Dict[str, Any],
        tags_audit: Dict[str, Any],
        thumbnail_audit: Dict[str, Any],
        overall_score: int
    ) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations."""
        recommendations = []
        
        # Collect all recommendations with priority
        if title_audit.get("score", 0) < 60:
            recommendations.append({
                "priority": "high",
                "category": "title",
                "message": "Title needs improvement",
                "details": title_audit.get("recommendations", [])
            })
        
        if description_audit.get("score", 0) < 60:
            recommendations.append({
                "priority": "high",
                "category": "description",
                "message": "Description needs improvement",
                "details": description_audit.get("recommendations", [])
            })
        
        if tags_audit.get("score", 0) < 60:
            recommendations.append({
                "priority": "medium",
                "category": "tags",
                "message": "Tags need optimization",
                "details": tags_audit.get("recommendations", [])
            })
        
        if thumbnail_audit.get("score", 0) < 60:
            recommendations.append({
                "priority": "medium",
                "category": "thumbnail",
                "message": "Thumbnail could be improved",
                "details": thumbnail_audit.get("recommendations", [])
            })
        
        # Overall recommendations
        if overall_score < 60:
            recommendations.append({
                "priority": "high",
                "category": "overall",
                "message": "Overall SEO needs significant improvement",
                "details": [
                    "Focus on improving title and description first (highest impact)",
                    "Add more relevant tags",
                    "Optimize thumbnail for better click-through rate"
                ]
            })
        
        return recommendations
    
    def _identify_priority_actions(
        self,
        title_audit: Dict[str, Any],
        description_audit: Dict[str, Any],
        tags_audit: Dict[str, Any],
        thumbnail_audit: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify top priority actions for improvement."""
        actions = []
        
        # Find lowest scoring element
        scores = {
            "title": title_audit.get("score", 0),
            "description": description_audit.get("score", 0),
            "tags": tags_audit.get("score", 0),
            "thumbnail": thumbnail_audit.get("score", 0)
        }
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        
        for element, score in sorted_scores[:3]:  # Top 3 priorities
            if score < 80:
                if element == "title":
                    actions.append({
                        "action": "Optimize Title",
                        "priority": "high",
                        "current_score": score,
                        "impact": "high",
                        "quick_fix": title_audit.get("recommendations", [])[0] if title_audit.get("recommendations") else "Review title optimization guidelines"
                    })
                elif element == "description":
                    actions.append({
                        "action": "Improve Description",
                        "priority": "high",
                        "current_score": score,
                        "impact": "high",
                        "quick_fix": description_audit.get("recommendations", [])[0] if description_audit.get("recommendations") else "Expand description to 200+ words"
                    })
                elif element == "tags":
                    actions.append({
                        "action": "Optimize Tags",
                        "priority": "medium",
                        "current_score": score,
                        "impact": "medium",
                        "quick_fix": tags_audit.get("recommendations", [])[0] if tags_audit.get("recommendations") else "Add 20-30 relevant tags"
                    })
                elif element == "thumbnail":
                    actions.append({
                        "action": "Enhance Thumbnail",
                        "priority": "medium",
                        "current_score": score,
                        "impact": "medium",
                        "quick_fix": thumbnail_audit.get("recommendations", [])[0] if thumbnail_audit.get("recommendations") else "Use high contrast, eye-catching thumbnail"
                    })
        
        return actions
    
    def _calculate_improvement_potential(
        self,
        title_audit: Dict[str, Any],
        description_audit: Dict[str, Any],
        tags_audit: Dict[str, Any],
        thumbnail_audit: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate potential improvement if all recommendations are followed."""
        current_scores = {
            "title": title_audit.get("score", 0),
            "description": description_audit.get("score", 0),
            "tags": tags_audit.get("score", 0),
            "thumbnail": thumbnail_audit.get("score", 0)
        }
        
        # Estimate potential scores (assuming optimizations are applied)
        potential_scores = {
            "title": min(current_scores["title"] + 30, 100),
            "description": min(current_scores["description"] + 25, 100),
            "tags": min(current_scores["tags"] + 20, 100),
            "thumbnail": min(current_scores["thumbnail"] + 15, 100)
        }
        
        # Calculate potential overall score
        weights = {
            "title": 0.35,
            "description": 0.30,
            "tags": 0.25,
            "thumbnail": 0.10
        }
        
        current_overall = sum(
            current_scores[k] * weights[k] for k in current_scores
        )
        
        potential_overall = sum(
            potential_scores[k] * weights[k] for k in potential_scores
        )
        
        improvement = potential_overall - current_overall
        
        return {
            "current_overall_score": int(current_overall),
            "potential_overall_score": int(potential_overall),
            "improvement_points": int(improvement),
            "improvement_percentage": round((improvement / max(current_overall, 1)) * 100, 1),
            "element_improvements": {
                k: {
                    "current": current_scores[k],
                    "potential": potential_scores[k],
                    "gain": potential_scores[k] - current_scores[k]
                }
                for k in current_scores
            }
        }
    
    def audit_channel_videos(
        self,
        channel_handle: str,
        max_videos: int = 10
    ) -> Dict[str, Any]:
        """
        Audit multiple videos from a channel.
        
        Args:
            channel_handle: Channel handle
            max_videos: Maximum number of videos to audit
            
        Returns:
            Summary of audits for all videos
        """
        try:
            channel_data = self.client.get_channel_by_handle(channel_handle)
            if not channel_data.get("items"):
                return {"error": f"Channel @{channel_handle} not found"}
            
            channel_id = channel_data["items"][0]["id"]
            videos = self.client.get_channel_videos(channel_id, max_results=max_videos)
        except Exception as e:
            return {"error": f"Failed to fetch channel videos: {str(e)}"}
        
        audits = []
        for video in videos[:max_videos]:
            video_id = video["id"]["videoId"]
            try:
                audit = self.audit_video(video_id, channel_handle)
                audits.append(audit)
            except Exception as e:
                audits.append({
                    "video_id": video_id,
                    "error": str(e)
                })
        
        # Calculate averages
        successful_audits = [a for a in audits if "overall_seo_score" in a]
        if successful_audits:
            avg_score = sum(a["overall_seo_score"] for a in successful_audits) / len(successful_audits)
            avg_grade = self._get_seo_grade(int(avg_score))
        else:
            avg_score = 0
            avg_grade = "N/A"
        
        return {
            "channel_handle": channel_handle,
            "total_videos_audited": len(audits),
            "successful_audits": len(successful_audits),
            "average_seo_score": round(avg_score, 1),
            "average_grade": avg_grade,
            "audits": audits,
            "summary": {
                "excellent_videos": sum(1 for a in successful_audits if a["overall_seo_score"] >= 80),
                "good_videos": sum(1 for a in successful_audits if 60 <= a["overall_seo_score"] < 80),
                "needs_improvement": sum(1 for a in successful_audits if a["overall_seo_score"] < 60)
            }
        }

