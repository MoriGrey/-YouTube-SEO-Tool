"""
Caption & Transcript Optimizer Module
Optimize video captions and transcripts for SEO and discoverability.

AGI Paradigm: Self-Evolving Architecture
- Analyzes captions for SEO opportunities
- Optimizes keyword placement in captions
- Supports multilingual optimization
"""

from typing import Dict, Any, List, Optional
import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.keyword_researcher import KeywordResearcher


class CaptionOptimizer:
    """
    Caption and transcript optimization system.
    
    AGI Paradigm: Self-Evolving Architecture
    - Optimizes captions for SEO
    - Integrates keywords naturally
    - Supports multiple languages
    """
    
    def __init__(
        self,
        client: YouTubeClient,
        keyword_researcher: KeywordResearcher
    ):
        self.client = client
        self.keyword_researcher = keyword_researcher
    
    def get_video_captions(
        self,
        video_id: str,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get captions for a video.
        
        Args:
            video_id: YouTube video ID
            language: Language code (optional, e.g., 'en', 'tr')
            
        Returns:
            Caption data with transcript
        """
        try:
            # Get caption tracks
            caption_tracks = self.client.youtube.captions().list(
                part="snippet",
                videoId=video_id
            ).execute()
            
            if not caption_tracks.get("items"):
                return {
                    "error": "No captions found",
                    "video_id": video_id,
                    "recommendation": "Add captions to your video for better SEO and accessibility"
                }
            
            # Filter by language if specified
            tracks = caption_tracks.get("items", [])
            if language:
                tracks = [t for t in tracks if t["snippet"].get("language") == language]
            
            if not tracks:
                return {
                    "error": f"No captions found for language: {language}",
                    "video_id": video_id,
                    "available_languages": [t["snippet"].get("language") for t in caption_tracks.get("items", [])]
                }
            
            # Get first track (or specified language)
            track = tracks[0]
            track_id = track["id"]
            track_language = track["snippet"].get("language", "unknown")
            is_auto_generated = track["snippet"].get("trackKind") == "ASR"
            
            # Download caption content
            transcript = None
            download_error = None
            try:
                # Note: captions().download() returns bytes, not a dict
                # We need to use http request directly or parse bytes
                import io
                from googleapiclient.http import MediaIoBaseDownload
                
                # Alternative: Use get_media() for text format
                request = self.client.youtube.captions().download(
                    id=track_id,
                    tfmt="srt"
                )
                
                # Execute and decode
                caption_bytes = request.execute()
                if isinstance(caption_bytes, bytes):
                    caption_content = caption_bytes.decode('utf-8')
                else:
                    caption_content = str(caption_bytes)
                
                # Parse SRT content
                transcript = self._parse_srt(caption_content)
            except Exception as e:
                # If download fails, store error for better messaging
                download_error = str(e)
                transcript = None
                
                # Check if it's an OAuth2 requirement (401 error)
                if "401" in download_error or "Login Required" in download_error or "OAuth2" in download_error or "API keys are not supported" in download_error:
                    return {
                        "error": "OAuth2 authentication required",
                        "video_id": video_id,
                        "language": track_language,
                        "is_auto_generated": is_auto_generated,
                        "error_type": "oauth2_required",
                        "recommendation": (
                            "YouTube Captions API requires OAuth2 authentication (not just API key). "
                            "This means you can only download captions for videos you own. "
                            "To use this feature:\n"
                            "1. You must be the owner of the video\n"
                            "2. OAuth2 authentication must be set up (currently not implemented)\n"
                            "3. Alternatively, you can manually copy captions from YouTube Studio\n\n"
                            "**Note:** This is a YouTube API limitation - caption downloads require video ownership and OAuth2."
                        ),
                        "workaround": (
                            "**Workaround:**\n"
                            "- Go to YouTube Studio → Videos → Select your video → Subtitles\n"
                            "- Copy the transcript manually\n"
                            "- Or use YouTube's built-in caption editor to optimize captions"
                        )
                    }
                # Check if it's a permission issue
                elif "403" in download_error or "Forbidden" in download_error:
                    return {
                        "error": "Cannot download captions - permission denied",
                        "video_id": video_id,
                        "language": track_language,
                        "is_auto_generated": is_auto_generated,
                        "recommendation": "The video owner may have restricted caption downloads, or you may need additional permissions. Try using auto-generated captions if available."
                    }
                elif "404" in download_error or "Not Found" in download_error:
                    return {
                        "error": "Caption track not found or no longer available",
                        "video_id": video_id,
                        "language": track_language,
                        "recommendation": "The caption track may have been removed. Try checking if captions are enabled for this video."
                    }
            
            # If transcript is None, return helpful error message
            if transcript is None:
                error_msg = download_error or "Unknown error"
                return {
                    "error": "No transcript available",
                    "video_id": video_id,
                    "language": track_language,
                    "is_auto_generated": is_auto_generated,
                    "track_id": track_id,
                    "download_error": error_msg,
                    "recommendation": f"Failed to download captions: {error_msg}. This may be due to: 1) Caption track restrictions, 2) API permissions, 3) Caption format issues. Try checking if the video has captions enabled in YouTube Studio."
                }
            
            return {
                "video_id": video_id,
                "language": track_language,
                "is_auto_generated": is_auto_generated,
                "track_id": track_id,
                "transcript": transcript,
                "word_count": len(transcript.split()) if transcript else 0,
                "character_count": len(transcript) if transcript else 0
            }
        except Exception as e:
            return {
                "error": f"Failed to fetch captions: {str(e)}",
                "video_id": video_id
            }
    
    def _parse_srt(self, srt_content: str) -> str:
        """Parse SRT format and extract text."""
        # Simple SRT parser
        lines = srt_content.split('\n')
        text_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # Skip sequence numbers and timestamps
            if line.isdigit() or '-->' in line:
                i += 1
                continue
            
            # Collect text lines
            if line:
                text_lines.append(line)
            i += 1
        
        return ' '.join(text_lines)
    
    def analyze_captions(
        self,
        video_id: str,
        keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze captions for SEO optimization.
        
        Args:
            video_id: YouTube video ID
            keywords: List of target keywords
            
        Returns:
            Analysis with SEO recommendations
        """
        # Get captions
        caption_data = self.get_video_captions(video_id)
        
        if "error" in caption_data:
            return caption_data
        
        transcript = caption_data.get("transcript", "")
        if not transcript:
            return {
                "error": "No transcript available",
                "video_id": video_id,
                "recommendation": "Ensure captions are available and downloadable"
            }
        
        # Default keywords if not provided
        if not keywords:
            keywords = ["psychedelic", "anatolian", "rock", "turkish", "70s", "music"]
        
        # Analyze keyword presence
        transcript_lower = transcript.lower()
        keyword_analysis = {}
        for keyword in keywords:
            count = transcript_lower.count(keyword.lower())
            keyword_analysis[keyword] = {
                "count": count,
                "density": round((count / max(len(transcript.split()), 1)) * 100, 2),
                "present": count > 0
            }
        
        # Calculate SEO score
        seo_score = self._calculate_caption_seo_score(transcript, keyword_analysis, keywords)
        
        # Check first 200 words (important for SEO)
        first_200_words = ' '.join(transcript.split()[:200])
        keywords_in_first_200 = sum(
            1 for kw in keywords if kw.lower() in first_200_words.lower()
        )
        
        # Generate recommendations
        recommendations = self._generate_caption_recommendations(
            transcript,
            keyword_analysis,
            keywords,
            keywords_in_first_200
        )
        
        return {
            "video_id": video_id,
            "language": caption_data.get("language"),
            "is_auto_generated": caption_data.get("is_auto_generated"),
            "word_count": len(transcript.split()),
            "character_count": len(transcript),
            "seo_score": seo_score,
            "keyword_analysis": keyword_analysis,
            "keywords_in_first_200": keywords_in_first_200,
            "total_keywords": len(keywords),
            "recommendations": recommendations,
            "transcript_preview": transcript[:500] + "..." if len(transcript) > 500 else transcript
        }
    
    def _calculate_caption_seo_score(
        self,
        transcript: str,
        keyword_analysis: Dict[str, Dict[str, Any]],
        keywords: List[str]
    ) -> int:
        """Calculate SEO score for captions."""
        score = 0
        
        # Keyword presence (max 40 points)
        keywords_present = sum(1 for kw, data in keyword_analysis.items() if data["present"])
        keyword_coverage = (keywords_present / max(len(keywords), 1)) * 40
        score += keyword_coverage
        
        # Keyword density (max 30 points)
        avg_density = sum(data["density"] for data in keyword_analysis.values()) / max(len(keyword_analysis), 1)
        if 1.0 <= avg_density <= 3.0:  # Optimal density
            score += 30
        elif 0.5 <= avg_density < 1.0 or 3.0 < avg_density <= 5.0:
            score += 20
        else:
            score += 10
        
        # Word count (max 20 points)
        word_count = len(transcript.split())
        if word_count >= 500:
            score += 20
        elif word_count >= 300:
            score += 15
        elif word_count >= 200:
            score += 10
        else:
            score += 5
        
        # Natural keyword placement (max 10 points)
        # Check if keywords appear in natural contexts
        natural_placement = self._check_natural_placement(transcript, keywords)
        score += natural_placement * 10
        
        return min(int(score), 100)
    
    def _check_natural_placement(self, transcript: str, keywords: List[str]) -> float:
        """Check if keywords are placed naturally (not keyword stuffing)."""
        transcript_lower = transcript.lower()
        
        # Check for keyword stuffing patterns
        stuffing_patterns = []
        for keyword in keywords:
            # Check if keyword appears too frequently in short spans
            keyword_lower = keyword.lower()
            positions = [i for i, word in enumerate(transcript_lower.split()) if keyword_lower in word]
            
            if len(positions) > 1:
                # Check spacing between occurrences
                for i in range(len(positions) - 1):
                    gap = positions[i + 1] - positions[i]
                    if gap < 10:  # Keywords too close together
                        stuffing_patterns.append(keyword)
        
        # Score based on natural placement
        if not stuffing_patterns:
            return 1.0  # Perfect
        elif len(stuffing_patterns) <= len(keywords) * 0.3:
            return 0.7  # Mostly natural
        else:
            return 0.3  # Keyword stuffing detected
    
    def _generate_caption_recommendations(
        self,
        transcript: str,
        keyword_analysis: Dict[str, Dict[str, Any]],
        keywords: List[str],
        keywords_in_first_200: int
    ) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []
        
        # Check keyword coverage
        missing_keywords = [
            kw for kw, data in keyword_analysis.items()
            if not data["present"]
        ]
        if missing_keywords:
            recommendations.append(
                f"Add missing keywords to captions: {', '.join(missing_keywords[:3])}"
            )
        
        # Check keyword density
        avg_density = sum(data["density"] for data in keyword_analysis.values()) / max(len(keyword_analysis), 1)
        if avg_density < 1.0:
            recommendations.append(
                "Increase keyword density in captions (aim for 1-3% density)"
            )
        elif avg_density > 3.0:
            recommendations.append(
                "Reduce keyword density to avoid keyword stuffing (aim for 1-3%)"
            )
        
        # Check first 200 words
        if keywords_in_first_200 < len(keywords) * 0.5:
            recommendations.append(
                "Include more keywords in the first 200 words of captions (important for SEO)"
            )
        
        # Word count check
        word_count = len(transcript.split())
        if word_count < 300:
            recommendations.append(
                "Expand captions with more detailed descriptions (aim for 300+ words)"
            )
        
        # Natural placement
        if self._check_natural_placement(transcript, keywords) < 0.7:
            recommendations.append(
                "Ensure keywords are placed naturally in context, not forced"
            )
        
        if not recommendations:
            recommendations.append("Captions are well-optimized for SEO!")
        
        return recommendations
    
    def optimize_captions(
        self,
        video_id: str,
        keywords: Optional[List[str]] = None,
        target_language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate optimized caption suggestions.
        
        Args:
            video_id: YouTube video ID
            keywords: Target keywords
            target_language: Target language code
            
        Returns:
            Optimization suggestions and improved transcript
        """
        # Analyze current captions
        analysis = self.analyze_captions(video_id, keywords)
        
        if "error" in analysis:
            return analysis
        
        transcript = analysis.get("transcript_preview", "")
        if not transcript or len(transcript) < 100:
            return {
                "error": "Insufficient transcript data",
                "video_id": video_id
            }
        
        # Generate optimization suggestions
        if not keywords:
            keywords = ["psychedelic", "anatolian", "rock", "turkish", "70s"]
        
        # Create optimized version (suggestions only, not actual modification)
        optimization_suggestions = []
        
        # Check each keyword
        transcript_lower = transcript.lower()
        for keyword in keywords:
            if keyword.lower() not in transcript_lower:
                optimization_suggestions.append({
                    "keyword": keyword,
                    "action": "add",
                    "suggestion": f"Add '{keyword}' naturally in the transcript",
                    "example": f"Consider adding: '...{keyword} music...' or '...{keyword} style...'"
                })
        
        # Check keyword density
        keyword_analysis = analysis.get("keyword_analysis", {})
        for keyword, data in keyword_analysis.items():
            density = data.get("density", 0)
            if density < 1.0:
                optimization_suggestions.append({
                    "keyword": keyword,
                    "action": "increase_density",
                    "current_density": density,
                    "target_density": 1.5,
                    "suggestion": f"Increase mentions of '{keyword}' naturally in context"
                })
            elif density > 3.0:
                optimization_suggestions.append({
                    "keyword": keyword,
                    "action": "reduce_density",
                    "current_density": density,
                    "target_density": 2.0,
                    "suggestion": f"Reduce excessive mentions of '{keyword}' to avoid keyword stuffing"
                })
        
        return {
            "video_id": video_id,
            "current_seo_score": analysis.get("seo_score", 0),
            "optimization_suggestions": optimization_suggestions,
            "estimated_improvement": {
                "potential_score": min(analysis.get("seo_score", 0) + 20, 100),
                "improvement_points": min(20, 100 - analysis.get("seo_score", 0))
            },
            "best_practices": [
                "Include keywords naturally in spoken content",
                "Mention keywords in first 200 words of transcript",
                "Maintain 1-3% keyword density",
                "Avoid keyword stuffing",
                "Use keywords in context (e.g., 'psychedelic rock music')",
                "Ensure captions are accurate and readable"
            ]
        }
    
    def get_multilingual_support(
        self,
        video_id: str
    ) -> Dict[str, Any]:
        """
        Check multilingual caption support.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Available languages and recommendations
        """
        try:
            caption_tracks = self.client.youtube.captions().list(
                part="snippet",
                videoId=video_id
            ).execute()
            
            tracks = caption_tracks.get("items", [])
            if not tracks:
                return {
                    "video_id": video_id,
                    "available_languages": [],
                    "recommendation": "Add captions in multiple languages for better reach"
                }
            
            languages = []
            for track in tracks:
                snippet = track.get("snippet", {})
                languages.append({
                    "language": snippet.get("language", "unknown"),
                    "language_name": snippet.get("name", "Unknown"),
                    "is_auto_generated": snippet.get("trackKind") == "ASR",
                    "is_default": snippet.get("isDefault", False)
                })
            
            # Recommended languages for Anatolian Rock niche
            recommended_languages = ["tr", "en", "de", "nl", "fr", "es"]
            missing_languages = [
                lang for lang in recommended_languages
                if lang not in [l["language"] for l in languages]
            ]
            
            return {
                "video_id": video_id,
                "available_languages": languages,
                "language_count": len(languages),
                "recommended_languages": recommended_languages,
                "missing_languages": missing_languages,
                "recommendations": [
                    f"Add captions in: {', '.join(missing_languages[:3])}" if missing_languages else "Good multilingual support!",
                    "Prioritize Turkish (TR) and English (EN) for Anatolian Rock niche",
                    "Consider German (DE) and Dutch (NL) for European audience"
                ]
            }
        except Exception as e:
            return {
                "error": f"Failed to check multilingual support: {str(e)}",
                "video_id": video_id
            }

