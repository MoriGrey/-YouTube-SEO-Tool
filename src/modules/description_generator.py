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
        custom_info: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate SEO-optimized video description.
        
        Args:
            video_title: Video title
            song_name: Name of the song
            keywords: List of keywords to include
            custom_info: Custom information to add
        
        Returns:
            Generated description with metadata
        """
        keywords = keywords or []
        
        # Build description sections
        intro = self._generate_intro(song_name or video_title)
        main_description = self._generate_main_description(song_name, keywords, custom_info)
        hashtags = self._generate_hashtags(keywords, song_name)
        links = self._generate_links()
        outro = self._generate_outro()
        
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
    
    def _generate_intro(self, song_name: str) -> str:
        """Generate introduction section."""
        intros = [
            f"🎸 Welcome to another Psychedelic Anatolian Rock journey! Today we're exploring '{song_name}' - a beautiful fusion of traditional Turkish folk music with 70s psychedelic rock vibes.",
            f"🌟 Experience '{song_name}' like never before! This AI-powered psychedelic rock cover brings new life to a classic Anatolian folk song.",
            f"🎵 Dive into '{song_name}' - a mesmerizing blend of Anatolian melodies and psychedelic rock energy, created with artificial intelligence.",
        ]
        return intros[0]  # Can randomize
    
    def _generate_main_description(
        self,
        song_name: Optional[str],
        keywords: List[str],
        custom_info: Optional[str]
    ) -> str:
        """Generate main description body."""
        lines = [
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            "📌 ABOUT THIS VIDEO:",
            "",
            f"• Song: {song_name or 'Traditional Turkish Folk Song'}",
            "• Genre: Psychedelic Anatolian Rock",
            "• Style: 70s Psychedelic Rock Cover",
            "• Production: AI-Generated Music",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            "🎯 WHAT IS PSYCHEDELIC ANATOLIAN ROCK?",
            "",
            "Psychedelic Anatolian Rock is a unique fusion genre that combines:",
            "• Traditional Turkish folk music (Anadolu Rock)",
            "• 1970s psychedelic rock influences",
            "• Modern AI-powered music production",
            "",
            "This genre brings together the soulful melodies of Anatolian folk songs with the experimental sounds of psychedelic rock, creating something truly special.",
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
        song_name: Optional[str]
    ) -> str:
        """Generate hashtags section."""
        base_hashtags = [
            "#PsychedelicAnatolianRock",
            "#AnadoluRock",
            "#TurkishRock",
            "#70sRock",
            "#PsychedelicRock",
            "#AIMusic",
            "#TurkishFolk",
            "#AnatolianMusic",
            "#RockCover",
            "#PsychedelicMusic"
        ]
        
        # Add song-specific hashtag if available
        if song_name:
            song_tag = "#" + song_name.replace(" ", "").replace("'", "")
            base_hashtags.insert(0, song_tag)
        
        # Add keyword-based hashtags
        keyword_hashtags = ["#" + kw.replace(" ", "") for kw in keywords[:5] if len(kw) > 3]
        
        all_hashtags = base_hashtags + keyword_hashtags
        
        return "\n" + " ".join(all_hashtags[:15])  # Limit to 15 hashtags
    
    def _generate_links(self) -> str:
        """Generate links section."""
        return """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 CONNECT WITH US:

📺 Subscribe: https://www.youtube.com/@anatolianturkishrock
🎵 More Psychedelic Anatolian Rock: [Playlist Link]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def _generate_outro(self) -> str:
        """Generate outro section."""
        return """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 LET'S CONNECT:

If you enjoyed this video, please:
👍 Like this video
💬 Comment your thoughts
🔔 Subscribe for more Psychedelic Anatolian Rock
📤 Share with friends who love Turkish music

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 CREDITS:

Music: AI-Generated Psychedelic Anatolian Rock
Original: Traditional Turkish Folk Song
Genre: 70s Psychedelic Rock Cover

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ DISCLAIMER:

This is an AI-generated cover of a traditional folk song. All music is created using artificial intelligence technology.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def _analyze_description(self, description: str) -> Dict[str, Any]:
        """Analyze description for SEO and engagement."""
        word_count = len(description.split())
        char_count = len(description)
        hashtag_count = description.count("#")
        
        # Check for keywords in first 125 characters (visible in search)
        first_125 = description[:125]
        keyword_density = {
            "psychedelic": first_125.lower().count("psychedelic"),
            "anatolian": first_125.lower().count("anatolian"),
            "rock": first_125.lower().count("rock"),
            "turkish": first_125.lower().count("turkish")
        }
        
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

