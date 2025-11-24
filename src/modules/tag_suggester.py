"""
Tag Suggestion Module
Generate optimized tags for YouTube videos.
"""

from typing import Dict, Any, List, Optional
from collections import Counter
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient


class TagSuggester:
    """
    Tag suggestion system with AGI-powered optimization.
    
    AGI Paradigm: Omnipresent Data Mining
    - Analyzes competitor tags
    - Discovers trending tags
    - Optimizes tag combinations
    """
    
    def __init__(self, client: YouTubeClient):
        self.client = client
    
    def suggest_tags(
        self,
        video_title: str,
        song_name: Optional[str] = None,
        max_tags: int = 30
    ) -> Dict[str, Any]:
        """
        Suggest optimized tags for a video.
        
        Args:
            video_title: Video title
            song_name: Name of the song
            max_tags: Maximum number of tags to suggest
        
        Returns:
            Tag suggestions with analysis
        """
        # Base tags (always include)
        base_tags = [
            "psychedelic anatolian rock",
            "anadolu rock",
            "turkish rock",
            "70s rock",
            "psychedelic rock",
            "turkish music",
            "anatolian music",
            "folk rock",
            "psychedelic music",
            "rock cover"
        ]
        
        # Song-specific tags
        song_tags = []
        if song_name:
            song_tags.append(song_name.lower())
            # Extract words from song name
            words = song_name.lower().split()
            song_tags.extend([f"{word} cover" for word in words if len(word) > 3])
        
        # Title-based tags
        title_tags = self._extract_tags_from_title(video_title)
        
        # Competitor tags (analyze similar videos)
        competitor_tags = self._get_competitor_tags(video_title)
        
        # Combine and rank
        all_tags = base_tags + song_tags + title_tags + competitor_tags
        ranked_tags = self._rank_tags(all_tags, max_tags)
        
        # Analyze
        analysis = self._analyze_tags(ranked_tags)
        
        return {
            "suggested_tags": ranked_tags,
            "tag_count": len(ranked_tags),
            "categories": self._categorize_tags(ranked_tags),
            "analysis": analysis,
            "best_practices": self._get_best_practices()
        }
    
    def _extract_tags_from_title(self, title: str) -> List[str]:
        """Extract potential tags from video title."""
        tags = []
        title_lower = title.lower()
        
        # Common patterns
        patterns = [
            r"(\w+\s+rock)",
            r"(\w+\s+cover)",
            r"(\d+s)",
            r"(psychedelic\s+\w+)",
            r"(anatolian\s+\w+)",
            r"(turkish\s+\w+)"
        ]
        
        import re
        for pattern in patterns:
            matches = re.findall(pattern, title_lower)
            tags.extend(matches)
        
        # Extract individual meaningful words
        words = title_lower.split()
        meaningful_words = [w for w in words if len(w) > 4 and w not in ["with", "from", "this", "that"]]
        tags.extend(meaningful_words[:5])
        
        return list(set(tags))
    
    def _get_competitor_tags(self, query: str, max_results: int = 5) -> List[str]:
        """Get tags from competitor videos."""
        try:
            results = self.client.search_videos(query, max_results=max_results)
            
            # Note: YouTube API doesn't return tags directly
            # We can extract from titles and descriptions
            tags = []
            for result in results:
                title = result["snippet"]["title"]
                description = result["snippet"].get("description", "")
                
                # Extract potential tags
                title_words = [w for w in title.lower().split() if len(w) > 4]
                tags.extend(title_words[:3])
            
            return list(set(tags))
        except Exception:
            return []
    
    def _rank_tags(self, tags: List[str], max_tags: int) -> List[str]:
        """Rank tags by relevance and importance."""
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower not in seen:
                seen.add(tag_lower)
                unique_tags.append(tag)
        
        # Score tags
        scored_tags = []
        for tag in unique_tags:
            score = 0
            tag_lower = tag.lower()
            
            # Base keywords get higher score
            if any(kw in tag_lower for kw in ["psychedelic", "anatolian", "rock", "turkish", "70s"]):
                score += 10
            
            # Length score (optimal: 2-3 words)
            word_count = len(tag.split())
            if 2 <= word_count <= 3:
                score += 5
            elif word_count == 1:
                score += 3
            
            # Character length (optimal: 10-30 chars)
            char_len = len(tag)
            if 10 <= char_len <= 30:
                score += 3
            
            scored_tags.append((tag, score))
        
        # Sort by score
        scored_tags.sort(key=lambda x: x[1], reverse=True)
        
        # Return top tags
        return [tag for tag, score in scored_tags[:max_tags]]
    
    def _categorize_tags(self, tags: List[str]) -> Dict[str, List[str]]:
        """Categorize tags by type."""
        categories = {
            "genre": [],
            "style": [],
            "song_specific": [],
            "general": []
        }
        
        for tag in tags:
            tag_lower = tag.lower()
            
            if any(kw in tag_lower for kw in ["rock", "psychedelic", "folk", "music"]):
                categories["genre"].append(tag)
            elif any(kw in tag_lower for kw in ["cover", "70s", "80s", "style"]):
                categories["style"].append(tag)
            elif len(tag.split()) == 1 or any(char.isupper() for char in tag):
                categories["song_specific"].append(tag)
            else:
                categories["general"].append(tag)
        
        return categories
    
    def _analyze_tags(self, tags: List[str]) -> Dict[str, Any]:
        """Analyze tag quality and optimization."""
        total_chars = sum(len(tag) for tag in tags)
        avg_length = total_chars / len(tags) if tags else 0
        
        # Check for keyword coverage
        keywords = ["psychedelic", "anatolian", "rock", "turkish", "70s"]
        coverage = sum(1 for kw in keywords if any(kw in tag.lower() for tag in tags))
        
        return {
            "total_tags": len(tags),
            "average_length": avg_length,
            "keyword_coverage": f"{coverage}/{len(keywords)}",
            "total_characters": total_chars,
            "optimization_score": self._calculate_optimization_score(tags, coverage)
        }
    
    def _calculate_optimization_score(self, tags: List[str], coverage: int) -> int:
        """Calculate overall optimization score."""
        score = 0
        
        # Tag count (optimal: 20-30)
        if 20 <= len(tags) <= 30:
            score += 30
        elif 15 <= len(tags) < 20:
            score += 20
        elif 30 < len(tags) <= 40:
            score += 20
        
        # Keyword coverage
        score += coverage * 10
        
        # Average length (optimal: 10-20 chars)
        avg_len = sum(len(t) for t in tags) / len(tags) if tags else 0
        if 10 <= avg_len <= 20:
            score += 20
        elif 8 <= avg_len <= 25:
            score += 10
        
        return min(score, 100)
    
    def _get_best_practices(self) -> List[str]:
        """Get tag optimization best practices."""
        return [
            "Use 20-30 tags for optimal discoverability",
            "Include both broad and specific tags",
            "Mix genre tags with song-specific tags",
            "Use natural language (how people search)",
            "Include variations of main keywords",
            "Don't repeat the same keyword multiple times",
            "Use tags that appear in your title and description",
            "Research what tags competitors use",
            "Update tags based on performance data"
        ]

