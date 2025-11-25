"""
Keyword Research Module
Advanced keyword research and SEO analysis for YouTube.
"""

from typing import Dict, Any, List, Optional
from collections import Counter
import re
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient


class KeywordResearcher:
    """
    Advanced keyword research with AGI-powered discovery.
    
    AGI Paradigm: Fractal Knowledge Acquisition
    - Each keyword leads to more keywords
    - Discovers hidden search opportunities
    - Identifies trending terms
    """
    
    def __init__(self, client: YouTubeClient):
        self.client = client
    
    def research_keywords(
        self,
        base_keywords: List[str],
        max_results_per_keyword: int = 10,
        niche: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Research keywords and related terms.
        
        Args:
            base_keywords: List of base keywords to research
            max_results_per_keyword: Maximum search results per keyword
        
        Returns:
            Dictionary with keyword research results
        """
        all_keywords = set(base_keywords)
        keyword_data = {}
        
        # Get suggestions for each base keyword
        for keyword in base_keywords:
            suggestions = self.client.get_search_suggestions(keyword)
            all_keywords.update(suggestions)
            
            # Search YouTube for this keyword
            search_results = self.client.search_videos(
                keyword,
                max_results=max_results_per_keyword,
                region_code="TR"
            )
            
            keyword_data[keyword] = {
                "suggestions": suggestions[:20],  # Top 20
                "search_volume": len(search_results),
                "competition_level": self._analyze_competition(search_results)
            }
        
        # Extract additional keywords from search results
        extracted_keywords = self._extract_keywords_from_results(keyword_data)
        all_keywords.update(extracted_keywords)
        
        # Rank keywords by potential
        ranked_keywords = self._rank_keywords(list(all_keywords), keyword_data, niche=niche)
        
        return {
            "base_keywords": base_keywords,
            "total_keywords_found": len(all_keywords),
            "keyword_data": keyword_data,
            "ranked_keywords": ranked_keywords[:50],  # Top 50
            "recommendations": self._generate_keyword_recommendations(ranked_keywords)
        }
    
    def _analyze_competition(self, search_results: List[Dict[str, Any]]) -> str:
        """Analyze competition level for a keyword."""
        if not search_results:
            return "Low"
        
        # Check view counts (if available in search results)
        # For now, use result count as proxy
        if len(search_results) < 5:
            return "Low"
        elif len(search_results) < 20:
            return "Medium"
        else:
            return "High"
    
    def _extract_keywords_from_results(self, keyword_data: Dict[str, Any]) -> List[str]:
        """Extract keywords from search result titles."""
        extracted = set()
        
        for data in keyword_data.values():
            # Keywords are already in suggestions
            # Could also parse titles here if needed
            pass
        
        return list(extracted)
    
    def _rank_keywords(
        self,
        keywords: List[str],
        keyword_data: Dict[str, Any],
        niche: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Rank keywords by SEO potential."""
        ranked = []
        
        # Generate base terms from niche if provided
        if niche:
            base_terms = niche.lower().split() + ["music", "song", "cover"]
        else:
            base_terms = ["music", "song", "cover", "video"]
        
        for keyword in keywords:
            # Calculate score
            score = 0
            
            # Length score (40-60 chars optimal)
            length = len(keyword)
            if 40 <= length <= 60:
                score += 10
            elif 30 <= length <= 70:
                score += 5
            
            # Relevance score (contains base keywords)
            relevance = sum(1 for term in base_terms if term.lower() in keyword.lower())
            score += relevance * 5
            
            # Competition score (lower is better)
            competition = "Medium"
            for base_keyword, data in keyword_data.items():
                if base_keyword.lower() in keyword.lower():
                    competition = data.get("competition_level", "Medium")
                    break
            
            if competition == "Low":
                score += 15
            elif competition == "Medium":
                score += 10
            else:
                score += 5
            
            ranked.append({
                "keyword": keyword,
                "score": score,
                "length": length,
                "competition": competition,
                "relevance": relevance
            })
        
        # Sort by score
        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked
    
    def _generate_keyword_recommendations(
        self,
        ranked_keywords: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate keyword usage recommendations."""
        recommendations = []
        
        if ranked_keywords:
            top_keywords = ranked_keywords[:10]
            
            recommendations.append(
                f"Top recommended keywords: {', '.join([k['keyword'] for k in top_keywords[:5]])}"
            )
            
            # Check for long-tail opportunities
            long_tail = [k for k in ranked_keywords if len(k["keyword"]) > 50]
            if long_tail:
                recommendations.append(
                    f"Consider long-tail keywords for less competition: {long_tail[0]['keyword']}"
                )
        
        return recommendations
    
    def get_trending_keywords(self, niche: str = "psychedelic anatolian rock") -> List[str]:
        """Get currently trending keywords in the niche."""
        # Search for recent videos
        recent_results = self.client.search_videos(
            niche,
            max_results=25,
            order="date",
            region_code="TR"
        )
        
        # Extract keywords from titles
        trending = []
        for result in recent_results:
            title = result["snippet"]["title"]
            # Extract meaningful words
            words = re.findall(r'\b\w{4,}\b', title.lower())
            trending.extend(words)
        
        # Count frequency
        word_freq = Counter(trending)
        trending_keywords = [word for word, count in word_freq.most_common(20)]
        
        return trending_keywords
    
    def analyze_title_seo(self, title: str, niche: Optional[str] = None) -> Dict[str, Any]:
        """Analyze SEO potential of a title."""
        length = len(title)
        word_count = len(title.split())
        
        # Check for keywords - generate from niche if provided
        if niche:
            keywords = niche.lower().split() + ["music", "song", "cover"]
        else:
            keywords = ["music", "song", "cover", "video"]
        found_keywords = [kw for kw in keywords if kw.lower() in title.lower()]
        
        # SEO score
        score = 0
        
        # Length score
        if 40 <= length <= 60:
            score += 30
        elif 30 <= length <= 70:
            score += 20
        else:
            score += 10
        
        # Keyword score
        score += len(found_keywords) * 10
        
        # Word count (optimal: 5-8 words)
        if 5 <= word_count <= 8:
            score += 20
        elif 4 <= word_count <= 10:
            score += 10
        
        return {
            "title": title,
            "length": length,
            "word_count": word_count,
            "keywords_found": found_keywords,
            "seo_score": score,
            "recommendation": self._get_title_recommendation(length, word_count, found_keywords, niche=niche)
        }
    
    def _get_title_recommendation(
        self,
        length: int,
        word_count: int,
        found_keywords: List[str],
        niche: Optional[str] = None
    ) -> str:
        """Get recommendation for title optimization."""
        recommendations = []
        
        if length < 40:
            recommendations.append("Title is too short. Add more descriptive keywords.")
        elif length > 60:
            recommendations.append("Title is too long. Keep it under 60 characters.")
        
        if word_count < 5:
            recommendations.append("Add more words for better SEO.")
        elif word_count > 10:
            recommendations.append("Consider shortening the title.")
        
        if len(found_keywords) < 2:
            if niche:
                niche_words = ", ".join(niche.split()[:3])
                recommendations.append(f"Include more niche keywords (e.g., '{niche_words}').")
            else:
                recommendations.append("Include more relevant keywords in your title.")
        
        if not recommendations:
            return "Title looks good! It's optimized for SEO."
        
        return " | ".join(recommendations)

