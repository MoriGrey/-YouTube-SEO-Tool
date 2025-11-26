"""
Video Ideas Database Module
Database of trending video ideas with pattern learning.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


class VideoIdeasDatabase:
    """
    Video ideas database with pattern learning.
    
    AGI Paradigm: Continuous Learning Mechanism
    - Stores successful video patterns
    - Learns from trending ideas
    - Scores ideas by success potential
    """
    
    def __init__(self, db_path: str = "data/video_ideas_db.jsonl"):
        """
        Initialize the video ideas database.
        
        Args:
            db_path: Path to the JSONL database file
        """
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database file and directory exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            # Create empty database
            with open(self.db_path, 'w', encoding='utf-8') as f:
                pass
    
    def add_idea(
        self,
        title: str,
        description: str,
        category: str,
        niche: str,
        keywords: List[str],
        tags: List[str],
        success_score: float = 0.0,
        trend_score: float = 0.0,
        estimated_views: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add a video idea to the database.
        
        Returns:
            Idea ID
        """
        idea_id = f"idea_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(title) % 10000}"
        
        idea = {
            "id": idea_id,
            "title": title,
            "description": description,
            "category": category,
            "niche": niche,
            "success_score": success_score,
            "trend_score": trend_score,
            "keywords": keywords,
            "tags": tags,
            "estimated_views": estimated_views,
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        # Append to JSONL file
        with open(self.db_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(idea, ensure_ascii=False) + '\n')
        
        return idea_id
    
    def get_ideas(
        self,
        niche: Optional[str] = None,
        category: Optional[str] = None,
        min_score: float = 0.0,
        max_results: int = 50,
        sort_by: str = "success_score"
    ) -> List[Dict[str, Any]]:
        """
        Get ideas from the database with filters.
        
        Args:
            niche: Filter by niche
            category: Filter by category
            min_score: Minimum success score
            max_results: Maximum number of results
            sort_by: Sort field (success_score, trend_score, created_at)
        
        Returns:
            List of ideas
        """
        ideas = []
        
        # Read all ideas from JSONL file
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            idea = json.loads(line)
                            ideas.append(idea)
                        except json.JSONDecodeError:
                            continue
        
        # Apply filters
        filtered = []
        for idea in ideas:
            # Niche filter
            if niche and idea.get("niche", "").lower() != niche.lower():
                continue
            
            # Category filter
            if category and idea.get("category", "").lower() != category.lower():
                continue
            
            # Score filter
            if idea.get("success_score", 0) < min_score:
                continue
            
            filtered.append(idea)
        
        # Sort
        reverse = True if sort_by in ["success_score", "trend_score", "created_at"] else False
        filtered.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
        
        return filtered[:max_results]
    
    def get_trending_ideas(
        self,
        niche: Optional[str] = None,
        days: int = 30,
        max_results: int = 20
    ) -> List[Dict[str, Any]]:
        """Get trending ideas from recent period."""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        ideas = self.get_ideas(niche=niche, max_results=1000)
        
        # Filter by date and sort by trend score
        recent_ideas = []
        for idea in ideas:
            created_at = idea.get("created_at", "")
            if created_at:
                try:
                    idea_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    if idea_date.timestamp() >= cutoff_date:
                        recent_ideas.append(idea)
                except:
                    pass
        
        # Sort by trend score
        recent_ideas.sort(key=lambda x: x.get("trend_score", 0), reverse=True)
        
        return recent_ideas[:max_results]
    
    def get_category_ideas(
        self,
        category: str,
        niche: Optional[str] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """Get ideas for a specific category."""
        return self.get_ideas(
            niche=niche,
            category=category,
            max_results=max_results,
            sort_by="success_score"
        )
    
    def learn_from_patterns(
        self,
        successful_videos: List[Dict[str, Any]],
        niche: str
    ) -> Dict[str, Any]:
        """
        Learn patterns from successful videos.
        
        Args:
            successful_videos: List of successful video data
            niche: Niche to learn patterns for
        
        Returns:
            Learned patterns
        """
        if not successful_videos:
            return {}
        
        # Analyze common patterns
        categories = {}
        keywords = {}
        title_lengths = []
        tag_counts = []
        
        for video in successful_videos:
            # Category analysis
            cat = video.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
            
            # Keyword analysis
            video_keywords = video.get("keywords", [])
            for kw in video_keywords:
                keywords[kw] = keywords.get(kw, 0) + 1
            
            # Title length analysis
            title = video.get("title", "")
            if title:
                title_lengths.append(len(title))
            
            # Tag count analysis
            tags = video.get("tags", [])
            tag_counts.append(len(tags))
        
        # Calculate averages
        avg_title_length = sum(title_lengths) / len(title_lengths) if title_lengths else 0
        avg_tag_count = sum(tag_counts) / len(tag_counts) if tag_counts else 0
        
        # Top categories
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Top keywords
        top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        
        patterns = {
            "niche": niche,
            "total_videos_analyzed": len(successful_videos),
            "top_categories": [{"category": cat, "count": count} for cat, count in top_categories],
            "top_keywords": [{"keyword": kw, "count": count} for kw, count in top_keywords],
            "average_title_length": avg_title_length,
            "average_tag_count": avg_tag_count,
            "learned_at": datetime.now().isoformat()
        }
        
        return patterns
    
    def suggest_ideas(
        self,
        niche: str,
        category: Optional[str] = None,
        num_suggestions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Suggest ideas based on learned patterns.
        
        Args:
            niche: Target niche
            category: Optional category filter
            num_suggestions: Number of suggestions
        
        Returns:
            List of suggested ideas
        """
        # Get trending ideas
        trending = self.get_trending_ideas(niche=niche, days=30, max_results=20)
        
        # Get category-specific ideas if category specified
        if category:
            category_ideas = self.get_category_ideas(category, niche=niche, max_results=10)
            # Combine and deduplicate
            all_ideas = {idea["id"]: idea for idea in trending + category_ideas}
            suggestions = list(all_ideas.values())[:num_suggestions]
        else:
            suggestions = trending[:num_suggestions]
        
        # Score suggestions
        for suggestion in suggestions:
            # Calculate suggestion score based on multiple factors
            score = suggestion.get("success_score", 0) * 0.6
            score += suggestion.get("trend_score", 0) * 0.4
            
            suggestion["suggestion_score"] = score
        
        # Sort by suggestion score
        suggestions.sort(key=lambda x: x.get("suggestion_score", 0), reverse=True)
        
        return suggestions[:num_suggestions]
    
    def update_idea_score(
        self,
        idea_id: str,
        success_score: Optional[float] = None,
        trend_score: Optional[float] = None,
        estimated_views: Optional[int] = None
    ) -> bool:
        """
        Update an idea's scores.
        
        Returns:
            True if updated, False if not found
        """
        # Read all ideas
        ideas = []
        updated = False
        
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            idea = json.loads(line)
                            if idea.get("id") == idea_id:
                                # Update scores
                                if success_score is not None:
                                    idea["success_score"] = success_score
                                if trend_score is not None:
                                    idea["trend_score"] = trend_score
                                if estimated_views is not None:
                                    idea["estimated_views"] = estimated_views
                                idea["updated_at"] = datetime.now().isoformat()
                                updated = True
                            ideas.append(idea)
                        except json.JSONDecodeError:
                            continue
        
        # Write back if updated
        if updated:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                for idea in ideas:
                    f.write(json.dumps(idea, ensure_ascii=False) + '\n')
        
        return updated
    
    def get_statistics(self, niche: Optional[str] = None) -> Dict[str, Any]:
        """Get database statistics."""
        ideas = self.get_ideas(niche=niche, max_results=10000)
        
        if not ideas:
            return {
                "total_ideas": 0,
                "niches": [],
                "categories": {},
                "average_score": 0
            }
        
        # Count by niche
        niches = {}
        categories = {}
        scores = []
        
        for idea in ideas:
            idea_niche = idea.get("niche", "unknown")
            niches[idea_niche] = niches.get(idea_niche, 0) + 1
            
            idea_category = idea.get("category", "unknown")
            categories[idea_category] = categories.get(idea_category, 0) + 1
            
            scores.append(idea.get("success_score", 0))
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            "total_ideas": len(ideas),
            "niches": [{"niche": n, "count": c} for n, c in sorted(niches.items(), key=lambda x: x[1], reverse=True)],
            "categories": {cat: count for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)},
            "average_score": avg_score,
            "top_niche": max(niches.items(), key=lambda x: x[1])[0] if niches else None
        }

