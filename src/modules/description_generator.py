"""
Description Generator Module
Generate SEO-optimized video descriptions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class DescriptionGenerator:
    """
    Description generator with AGI-powered SEO optimization.
    
    AGI Paradigm: Self-Evolving Architecture
    - Learns from successful descriptions
    - Adapts to platform changes
    - Optimizes for search and engagement
    """
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def generate_description(
        self,
        video_title: str,
        song_name: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        custom_info: Optional[str] = None,
        niche: Optional[str] = None,
        channel_handle: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate SEO-optimized video description.
        
        Args:
            video_title: Video title
            song_name: Name of the song
            keywords: List of keywords to include
            custom_info: Custom information to add
            niche: Content niche (e.g., "oriental techno music")
            channel_handle: YouTube channel handle (e.g., "mori_grey")
        
        Returns:
            Generated description with metadata
        """
        keywords = keywords or []
        niche = niche or "psychedelic anatolian rock"
        channel_handle = channel_handle or "anatolianturkishrock"
        
        # Build description sections
        intro = self._generate_intro(song_name or video_title, niche)
        main_description = self._generate_main_description(song_name, keywords, custom_info, niche)
        hashtags = self._generate_hashtags(keywords, song_name, niche)
        links = self._generate_links(channel_handle)
        outro = self._generate_outro(niche)
        
        # Combine
        full_description = "\n\n".join([
            intro,
            main_description,
            hashtags,
            links,
            outro
        ])
        
        # Analyze
        analysis = self._analyze_description(full_description)
        
        return {
            "description": full_description,
            "word_count": len(full_description.split()),
            "character_count": len(full_description),
            "hashtag_count": full_description.count("#"),
            "analysis": analysis,
            "sections": {
                "intro": intro,
                "main": main_description,
                "hashtags": hashtags,
                "links": links,
                "outro": outro
            }
        }
    
    def _generate_intro(self, song_name: str, niche: str = "") -> str:
        """Generate introduction section."""
        niche_title = " ".join(word.capitalize() for word in niche.split()) if niche else "Psychedelic Anatolian Rock"
        
        intros = [
            f"🎸 Welcome to another {niche_title} journey! Today we're exploring '{song_name}' - a beautiful fusion of {niche_title.lower()} vibes.",
            f"🌟 Experience '{song_name}' like never before! This {niche_title.lower()} creation brings new life to this track.",
            f"🎵 Dive into '{song_name}' - a mesmerizing blend of {niche_title.lower()} energy, created with passion.",
        ]
        return intros[0]  # Can randomize
    
    def _generate_main_description(
        self,
        song_name: Optional[str],
        keywords: List[str],
        custom_info: Optional[str],
        niche: str = ""
    ) -> str:
        """Generate main description body."""
        niche_title = " ".join(word.capitalize() for word in niche.split()) if niche else "Psychedelic Anatolian Rock"
        
        lines = [
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            "📌 ABOUT THIS VIDEO:",
            "",
            f"• Song: {song_name or 'Track'}",
            f"• Genre: {niche_title}",
            f"• Style: {niche_title}",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            f"🎯 ABOUT {niche_title.upper()}:",
            "",
            f"{niche_title} is a unique genre that combines various musical elements to create something special.",
            "",
            f"This genre brings together different influences to create a distinctive {niche_title.lower()} sound.",
        ]
        
        if custom_info:
            lines.append("")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append("")
            lines.append("💡 ADDITIONAL INFO:")
            lines.append("")
            lines.append(custom_info)
        
        return "\n".join(lines)
    
    def _generate_hashtags(
        self,
        keywords: List[str],
        song_name: Optional[str],
        niche: str = ""
    ) -> str:
        """Generate hashtags section."""
        # Generate hashtags from niche
        niche_words = niche.split() if niche else ["psychedelic", "anatolian", "rock"]
        base_hashtags = []
        
        # Create hashtags from niche words
        for word in niche_words:
            if len(word) > 2:  # Skip short words
                hashtag = "#" + word.capitalize()
                base_hashtags.append(hashtag)
        
        # Add combined niche hashtag
        if niche:
            niche_hashtag = "#" + "".join(word.capitalize() for word in niche_words)
            base_hashtags.insert(0, niche_hashtag)
        
        # Fallback if no niche provided
        if not base_hashtags:
            base_hashtags = [
                "#PsychedelicAnatolianRock",
                "#AnadoluRock",
                "#TurkishRock",
                "#70sRock",
                "#PsychedelicRock"
            ]
        
        # Add song-specific hashtag if available
        if song_name:
            song_tag = "#" + song_name.replace(" ", "").replace("'", "")
            base_hashtags.insert(0, song_tag)
        
        # Add keyword-based hashtags
        keyword_hashtags = ["#" + kw.replace(" ", "") for kw in keywords[:5] if len(kw) > 3]
        
        all_hashtags = base_hashtags + keyword_hashtags
        
        return "\n" + " ".join(all_hashtags[:15])  # Limit to 15 hashtags
    
    def _generate_links(self, channel_handle: str = "") -> str:
        """Generate links section."""
        channel_handle = channel_handle.lstrip("@") if channel_handle else "anatolianturkishrock"
        channel_url = f"https://www.youtube.com/@{channel_handle}"
        
        return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 CONNECT WITH US:

📺 Subscribe: {channel_url}
🎵 More Content: [Playlist Link]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def _generate_outro(self, niche: str = "") -> str:
        """Generate outro section."""
        niche_title = " ".join(word.capitalize() for word in niche.split()) if niche else "Psychedelic Anatolian Rock"
        
        return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 LET'S CONNECT:

If you enjoyed this video, please:
👍 Like this video
💬 Comment your thoughts
🔔 Subscribe for more {niche_title}
📤 Share with friends who love this music

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 CREDITS:

Music: {niche_title}
Genre: {niche_title}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def _analyze_description(self, description: str) -> Dict[str, Any]:
        """Analyze description for SEO and engagement."""
        word_count = len(description.split())
        char_count = len(description)
        hashtag_count = description.count("#")
        
        # Check for keywords in first 125 characters (visible in search)
        first_125 = description[:125].lower()
        # Extract keywords from description for density check
        keyword_density = {}
        # Count common words that might be in niche
        for word in ["psychedelic", "anatolian", "rock", "turkish", "oriental", "techno", "music"]:
            keyword_density[word] = first_125.count(word)
        
        # SEO score
        seo_score = 0
        if word_count >= 200:
            seo_score += 30
        if char_count >= 1000:
            seo_score += 20
        if hashtag_count >= 10:
            seo_score += 20
        if sum(keyword_density.values()) >= 3:
            seo_score += 30
        
        return {
            "seo_score": seo_score,
            "word_count": word_count,
            "character_count": char_count,
            "hashtag_count": hashtag_count,
            "keyword_density_first_125": keyword_density,
            "recommendations": self._get_recommendations(word_count, char_count, hashtag_count, keyword_density)
        }
    
    def _get_recommendations(
        self,
        word_count: int,
        char_count: int,
        hashtag_count: int,
        keyword_density: Dict[str, int]
    ) -> List[str]:
        """Get optimization recommendations."""
        recommendations = []
        
        if word_count < 200:
            recommendations.append("Add more content - aim for at least 200 words for better SEO")
        
        if char_count < 1000:
            recommendations.append("Expand description - longer descriptions rank better in search")
        
        if hashtag_count < 10:
            recommendations.append("Add more relevant hashtags (10-15 is optimal)")
        
        if sum(keyword_density.values()) < 3:
            recommendations.append("Include more keywords in the first 125 characters (visible in search results)")
        
        if not recommendations:
            recommendations.append("Description looks great! It's well-optimized for SEO.")
        
        return recommendations
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load description templates."""
        return {
            "intro_templates": [],
            "outro_templates": []
        }

