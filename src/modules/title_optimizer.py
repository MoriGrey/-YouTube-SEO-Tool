"""
Title Optimization Module
Generate SEO-optimized titles for YouTube videos.
"""

from typing import Dict, Any, List, Optional
import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.modules.keyword_researcher import KeywordResearcher


class TitleOptimizer:
    """
    Title optimization engine with AGI-powered suggestions.
    
    AGI Paradigm: Quantum Knowledge Synthesis
    - Synthesizes multiple title variations
    - Optimizes for search and click-through
    - A/B tests different approaches
    """
    
    def __init__(self, keyword_researcher: KeywordResearcher):
        self.keyword_researcher = keyword_researcher
    
    def generate_title_variations(
        self,
        base_title: str,
        song_name: Optional[str] = None,
        num_variations: int = 5,
        niche: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple title variations for A/B testing.
        
        Args:
            base_title: Original or base title
            song_name: Name of the song (if applicable)
            num_variations: Number of variations to generate
            niche: Content niche (e.g., "oriental techno music", "psychedelic anatolian rock")
        
        Returns:
            List of title variations with SEO scores
        """
        variations = []
        
        # Use provided niche or empty string (no hardcoded default)
        niche = niche or ""
        
        # Extract keywords from base title and niche
        keywords = self._extract_keywords(base_title, niche)
        
        # Generate different title structures
        structures = [
            self._structure_simple,
            self._structure_with_pipe,
            self._structure_with_brackets,
            self._structure_question,
            self._structure_emotional
        ]
        
        for i in range(num_variations):
            structure_func = random.choice(structures)
            variation = structure_func(song_name or base_title, keywords, niche)
            
            # Analyze SEO
            seo_analysis = self.keyword_researcher.analyze_title_seo(variation, niche=niche)
            
            variations.append({
                "title": variation,
                "seo_score": seo_analysis["seo_score"],
                "length": seo_analysis["length"],
                "keywords_found": seo_analysis["keywords_found"],
                "recommendation": seo_analysis["recommendation"],
                "structure": structure_func.__name__.replace("_structure_", "")
            })
        
        # Sort by SEO score
        variations.sort(key=lambda x: x["seo_score"], reverse=True)
        return variations
    
    def _extract_keywords(self, title: str, niche: str = "") -> List[str]:
        """
        Extract relevant keywords from title and niche.
        
        Args:
            title: Video title
            niche: Content niche (e.g., "oriental techno music")
        
        Returns:
            List of extracted keywords
        """
        keywords = []
        
        # Extract keywords from niche (split by space and filter meaningful words)
        niche_keywords = []
        if niche:
            # Split niche into words and capitalize appropriately
            niche_words = niche.lower().split()
            # Filter out common stop words
            stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
            niche_keywords = [word for word in niche_words if word not in stop_words and len(word) > 2]
        
        # Also check title for keywords
        title_lower = title.lower()
        
        # Combine niche keywords and check if they appear in title
        all_keywords = niche_keywords + ["music", "song", "cover", "70s", "80s", "90s"]
        
        for keyword in all_keywords:
            if keyword in title_lower:
                keywords.append(keyword)
        
        # If no keywords found from title, use niche keywords
        if not keywords and niche_keywords:
            keywords = niche_keywords[:3]  # Take first 3 keywords from niche
        
        return keywords
    
    def _structure_simple(self, song_name: str, keywords: List[str], niche: str = "") -> str:
        """Simple structure: Song Name | Keywords"""
        # Use niche keywords if available
        if niche:
            niche_words = niche.split()
            # Capitalize niche words properly
            niche_title = " ".join(word.capitalize() for word in niche_words[:3])
            title = f"{song_name} | {niche_title}"
        else:
            # Fallback to keywords if no niche
            if keywords:
                keywords_capitalized = [kw.capitalize() for kw in keywords[:3]]
                title = f"{song_name} | {' '.join(keywords_capitalized)}"
            else:
                title = song_name
        
        return title[:60]  # Keep under 60 chars
    
    def _structure_with_pipe(self, song_name: str, keywords: List[str], niche: str = "") -> str:
        """Structure with pipe: Song | Genre"""
        if niche:
            # Capitalize niche properly
            genre = " ".join(word.capitalize() for word in niche.split())
            title = f"{song_name} | {genre}"
        else:
            title = f"{song_name}"
        return title[:60]
    
    def _structure_with_brackets(self, song_name: str, keywords: List[str], niche: str = "") -> str:
        """Structure with brackets: Song [Genre]"""
        if niche:
            # Capitalize niche properly
            genre = " ".join(word.capitalize() for word in niche.split())
        else:
            genre = "Music"  # Generic fallback
        
        title = f"{song_name} [{genre}]"
        return title[:60]
    
    def _structure_question(self, song_name: str, keywords: List[str], niche: str = "") -> str:
        """Question structure: Have You Heard Song? | Genre"""
        if niche:
            # Capitalize niche properly
            genre = " ".join(word.capitalize() for word in niche.split())
        else:
            genre = "Music"  # Generic fallback
        
        title = f"{song_name} | {genre} Cover"
        return title[:60]
    
    def _structure_emotional(self, song_name: str, keywords: List[str], niche: str = "") -> str:
        """Emotional structure: Amazing Song | Genre"""
        if niche:
            # Capitalize niche properly
            genre = " ".join(word.capitalize() for word in niche.split())
        else:
            genre = "Music"  # Generic fallback
        
        emotional_words = ["Amazing", "Incredible", "Beautiful", "Epic"]
        emotional = random.choice(emotional_words)
        title = f"{emotional} {song_name} | {genre}"
        return title[:60]
    
    def optimize_existing_title(self, title: str, niche: Optional[str] = None) -> Dict[str, Any]:
        """
        Optimize an existing title.
        
        Args:
            title: Original title
            niche: Content niche (optional)
        
        Returns:
            Optimization suggestions and improved version
        """
        analysis = self.keyword_researcher.analyze_title_seo(title, niche=niche)
        
        # Generate optimized version
        if not niche:
            niche = ""  # Use empty string instead of hardcoded default
        keywords = self._extract_keywords(title, niche)
        optimized = self._structure_with_pipe(title, keywords, niche)
        
        optimized_analysis = self.keyword_researcher.analyze_title_seo(optimized, niche=niche)
        
        return {
            "original": {
                "title": title,
                "seo_score": analysis["seo_score"],
                "length": analysis["length"]
            },
            "optimized": {
                "title": optimized,
                "seo_score": optimized_analysis["seo_score"],
                "length": optimized_analysis["length"]
            },
            "improvement": optimized_analysis["seo_score"] - analysis["seo_score"],
            "suggestions": analysis["recommendation"]
        }
    
    def get_title_best_practices(self) -> Dict[str, Any]:
        """Get title optimization best practices."""
        return {
            "optimal_length": "40-60 characters",
            "keyword_placement": "Include main keyword in first 30 characters",
            "structures": [
                "Song Name | Genre | Year",
                "Song Name [Genre]",
                "Song Name | Music Cover"
            ],
            "avoid": [
                "Clickbait without substance",
                "Titles over 60 characters",
                "Missing genre keywords",
                "All caps titles"
            ],
            "tips": [
                "Use pipe (|) to separate sections",
                "Include year/decade (70s) for nostalgia",
                "Mention 'Cover' if it's a cover",
                "Use emotional words sparingly"
            ]
        }

