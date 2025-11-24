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
        num_variations: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple title variations for A/B testing.
        
        Args:
            base_title: Original or base title
            song_name: Name of the song (if applicable)
            num_variations: Number of variations to generate
        
        Returns:
            List of title variations with SEO scores
        """
        variations = []
        
        # Extract keywords from base title
        keywords = self._extract_keywords(base_title)
        
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
            variation = structure_func(song_name or base_title, keywords)
            
            # Analyze SEO
            seo_analysis = self.keyword_researcher.analyze_title_seo(variation)
            
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
    
    def _extract_keywords(self, title: str) -> List[str]:
        """Extract relevant keywords from title."""
        keywords = []
        base_keywords = [
            "psychedelic", "anatolian", "rock", "turkish", "70s", "cover",
            "türkü", "folk", "music", "song"
        ]
        
        title_lower = title.lower()
        for keyword in base_keywords:
            if keyword in title_lower:
                keywords.append(keyword)
        
        return keywords
    
    def _structure_simple(self, song_name: str, keywords: List[str]) -> str:
        """Simple structure: Song Name | Keywords"""
        if "psychedelic" not in " ".join(keywords).lower():
            keywords.insert(0, "Psychedelic")
        if "anatolian" not in " ".join(keywords).lower():
            keywords.insert(1, "Anatolian")
        if "rock" not in " ".join(keywords).lower():
            keywords.append("Rock")
        
        title = f"{song_name} | {' '.join(keywords[:3])}"
        return title[:60]  # Keep under 60 chars
    
    def _structure_with_pipe(self, song_name: str, keywords: List[str]) -> str:
        """Structure with pipe: Song | Genre | Year"""
        genre = "Psychedelic Anatolian Rock"
        year = "70s"
        title = f"{song_name} | {genre} | {year}"
        return title[:60]
    
    def _structure_with_brackets(self, song_name: str, keywords: List[str]) -> str:
        """Structure with brackets: Song [Genre]"""
        genre = "Psychedelic Anatolian Rock"
        title = f"{song_name} [{genre}]"
        return title[:60]
    
    def _structure_question(self, song_name: str, keywords: List[str]) -> str:
        """Question structure: Have You Heard Song? | Genre"""
        genre = "Psychedelic Anatolian Rock"
        title = f"{song_name} | {genre} Cover"
        return title[:60]
    
    def _structure_emotional(self, song_name: str, keywords: List[str]) -> str:
        """Emotional structure: Amazing Song | Genre"""
        genre = "Psychedelic Anatolian Rock"
        emotional_words = ["Amazing", "Incredible", "Beautiful", "Epic"]
        emotional = random.choice(emotional_words)
        title = f"{emotional} {song_name} | {genre}"
        return title[:60]
    
    def optimize_existing_title(self, title: str) -> Dict[str, Any]:
        """
        Optimize an existing title.
        
        Returns:
            Optimization suggestions and improved version
        """
        analysis = self.keyword_researcher.analyze_title_seo(title)
        
        # Generate optimized version
        keywords = self._extract_keywords(title)
        optimized = self._structure_with_pipe(title, keywords)
        
        optimized_analysis = self.keyword_researcher.analyze_title_seo(optimized)
        
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
                "Song Name | Psychedelic Anatolian Rock Cover"
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

