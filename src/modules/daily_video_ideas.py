"""
Daily Video Ideas Module
Personalized daily video ideas based on channel niche and trends.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.trend_predictor import TrendPredictor
from src.modules.keyword_researcher import KeywordResearcher
from src.modules.channel_analyzer import ChannelAnalyzer


class DailyVideoIdeas:
    """
    Personalized daily video ideas generator.
    
    AGI Paradigm: Proactive Assistant Interface
    - Generates personalized ideas based on channel data
    - Integrates trend analysis and keyword research
    - Scores ideas by success potential
    """
    
    # Video idea categories
    CATEGORIES = [
        "tutorial",
        "review",
        "vlog",
        "cover",
        "original",
        "compilation",
        "reaction",
        "interview",
        "behind_the_scenes",
        "educational",
        "entertainment",
        "collaboration"
    ]
    
    def __init__(
        self,
        client: YouTubeClient,
        trend_predictor: TrendPredictor,
        keyword_researcher: KeywordResearcher,
        channel_analyzer: Optional[ChannelAnalyzer] = None
    ):
        self.client = client
        self.trend_predictor = trend_predictor
        self.keyword_researcher = keyword_researcher
        self.channel_analyzer = channel_analyzer
    
    def generate_daily_ideas(
        self,
        niche: str,
        channel_handle: Optional[str] = None,
        num_ideas: int = 10,
        categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized daily video ideas.
        
        Args:
            niche: Channel niche
            channel_handle: Optional channel handle for personalization
            num_ideas: Number of ideas to generate
            categories: Optional list of categories to focus on
        
        Returns:
            Dictionary with daily video ideas and metadata
        """
        # Get trend predictions
        trend_data = self.trend_predictor.predict_trends(niche=niche, days_ahead=7)
        
        # Get trending keywords
        trending_keywords = self.keyword_researcher.get_trending_keywords(niche=niche)
        
        # Get channel data if available
        channel_data = None
        if channel_handle and self.channel_analyzer:
            try:
                channel_data = self.channel_analyzer.analyze_channel(channel_handle)
            except:
                pass
        
        # Generate ideas
        ideas = []
        used_titles = set()
        
        # Use specified categories or all categories
        categories_to_use = categories or self.CATEGORIES
        
        # Generate ideas for each category
        ideas_per_category = max(1, num_ideas // len(categories_to_use))
        
        for category in categories_to_use:
            category_ideas = self._generate_category_ideas(
                category=category,
                niche=niche,
                trend_data=trend_data,
                trending_keywords=trending_keywords,
                channel_data=channel_data,
                num_ideas=ideas_per_category
            )
            
            for idea in category_ideas:
                if idea["title"] not in used_titles:
                    ideas.append(idea)
                    used_titles.add(idea["title"])
                    if len(ideas) >= num_ideas:
                        break
            
            if len(ideas) >= num_ideas:
                break
        
        # Score and rank ideas
        scored_ideas = self._score_ideas(ideas, niche, channel_data)
        scored_ideas.sort(key=lambda x: x["success_score"], reverse=True)
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "niche": niche,
            "channel_handle": channel_handle,
            "total_ideas": len(scored_ideas),
            "ideas": scored_ideas[:num_ideas],
            "trend_insights": {
                "top_trending_keywords": trending_keywords[:5],
                "trending_themes": trend_data.get("recent_trends", {}).get("trending_themes", [])[:3]
            },
            "recommendations": self._generate_recommendations(scored_ideas, niche)
        }
    
    def _generate_category_ideas(
        self,
        category: str,
        niche: str,
        trend_data: Dict[str, Any],
        trending_keywords: List[str],
        channel_data: Optional[Dict[str, Any]],
        num_ideas: int
    ) -> List[Dict[str, Any]]:
        """Generate ideas for a specific category."""
        ideas = []
        
        # Get trending keywords for this category
        category_keywords = self._get_category_keywords(category, niche, trending_keywords)
        
        # Get trending themes
        trending_themes = trend_data.get("recent_trends", {}).get("trending_themes", [])
        themes = [t.get("theme", "") for t in trending_themes[:3]]
        
        # Generate idea templates based on category
        templates = self._get_category_templates(category, niche)
        
        for i in range(num_ideas):
            # Select random template
            template = random.choice(templates)
            
            # Select keywords and themes
            keyword = random.choice(category_keywords) if category_keywords else niche.split()[0]
            theme = random.choice(themes) if themes else ""
            
            # Generate title
            title = self._fill_template(template, niche, keyword, theme, category)
            
            # Generate description
            description = self._generate_description(category, niche, keyword, theme)
            
            # Generate tags
            tags = self._generate_tags(category, niche, keyword, theme)
            
            ideas.append({
                "title": title,
                "description": description,
                "category": category,
                "tags": tags,
                "keywords": [keyword] + (niche.split()[:2] if niche else []),
                "theme": theme
            })
        
        return ideas
    
    def _get_category_keywords(
        self,
        category: str,
        niche: str,
        trending_keywords: List[str]
    ) -> List[str]:
        """Get relevant keywords for a category."""
        # Filter trending keywords by category relevance
        category_specific = {
            "tutorial": ["how to", "learn", "guide", "step by step", "tips"],
            "review": ["review", "honest", "opinion", "test", "comparison"],
            "vlog": ["day in my life", "vlog", "behind the scenes", "daily"],
            "cover": ["cover", "version", "remix", "acoustic"],
            "original": ["original", "new", "premiere", "debut"],
            "compilation": ["best of", "compilation", "top 10", "collection"],
            "reaction": ["reaction", "first time", "reviewing"],
            "interview": ["interview", "chat", "conversation", "talk"],
            "behind_the_scenes": ["behind the scenes", "making of", "process"],
            "educational": ["explained", "deep dive", "analysis", "breakdown"],
            "entertainment": ["funny", "entertaining", "epic", "amazing"],
            "collaboration": ["collab", "with", "featuring", "together"]
        }
        
        # Combine category-specific terms with trending keywords
        relevant_keywords = []
        category_terms = category_specific.get(category, [])
        
        for keyword in trending_keywords:
            # Check if keyword is relevant to category
            if any(term in keyword.lower() for term in category_terms):
                relevant_keywords.append(keyword)
            elif any(term in keyword.lower() for term in niche.lower().split()):
                relevant_keywords.append(keyword)
        
        # Add niche keywords if not enough
        if len(relevant_keywords) < 3:
            relevant_keywords.extend(niche.split()[:3])
        
        return relevant_keywords[:10] if relevant_keywords else [niche.split()[0] if niche else "video"]
    
    def _get_category_templates(self, category: str, niche: str) -> List[str]:
        """Get title templates for a category."""
        templates = {
            "tutorial": [
                f"How to Create {niche} Music: Complete Guide",
                f"{niche} Tutorial: Step-by-Step Guide",
                f"Learn {niche}: Beginner's Guide",
                f"Mastering {niche}: Advanced Techniques",
                f"{niche} Explained: Everything You Need to Know"
            ],
            "review": [
                f"Honest Review: Best {niche} Albums of 2024",
                f"{niche} Review: What You Need to Know",
                f"Is {niche} Worth It? Honest Opinion",
                f"{niche} Review: Pros and Cons",
                f"Testing {niche}: Real Experience"
            ],
            "vlog": [
                f"Day in My Life: Creating {niche} Music",
                f"{niche} Vlog: Behind the Scenes",
                f"My {niche} Journey: Daily Vlog",
                f"Creating {niche}: A Day in the Studio",
                f"{niche} Life: What It's Really Like"
            ],
            "cover": [
                f"{niche} Cover: [Song Name]",
                f"Acoustic {niche} Cover",
                f"{niche} Version: [Classic Song]",
                f"Reimagining {niche}: Cover Version",
                f"{niche} Cover with a Twist"
            ],
            "original": [
                f"New {niche} Original: [Song Title]",
                f"{niche} Premiere: My Latest Creation",
                f"Original {niche} Music: [Song Title]",
                f"Brand New {niche}: First Listen",
                f"{niche} Debut: Original Composition"
            ],
            "compilation": [
                f"Best {niche} Songs of All Time",
                f"Top 10 {niche} Tracks You Need to Hear",
                f"{niche} Compilation: Ultimate Playlist",
                f"Greatest {niche} Hits Collection",
                f"{niche} Mix: Best of the Best"
            ],
            "reaction": [
                f"Reacting to {niche} for the First Time",
                f"{niche} Reaction: My Honest Thoughts",
                f"First Time Hearing {niche}",
                f"{niche} Reaction Video",
                f"Reacting to Viral {niche} Video"
            ],
            "interview": [
                f"Interview with {niche} Artist",
                f"{niche} Interview: Deep Conversation",
                f"Chatting with {niche} Creator",
                f"{niche} Interview: Behind the Music",
                f"Exclusive {niche} Interview"
            ],
            "behind_the_scenes": [
                f"Making {niche} Music: Behind the Scenes",
                f"{niche} Production Process Revealed",
                f"How I Create {niche}: BTS",
                f"{niche} Studio Session: Behind the Scenes",
                f"Creating {niche}: The Process"
            ],
            "educational": [
                f"{niche} Explained: Deep Dive",
                f"Understanding {niche}: Complete Guide",
                f"{niche} Breakdown: Everything Explained",
                f"The History of {niche}",
                f"{niche} Analysis: What Makes It Special"
            ],
            "entertainment": [
                f"Epic {niche} Performance",
                f"{niche} That Will Blow Your Mind",
                f"Most Entertaining {niche} Video",
                f"{niche} Fun: You Won't Believe This",
                f"Amazing {niche} Content"
            ],
            "collaboration": [
                f"{niche} Collab with [Artist Name]",
                f"Creating {niche} Together",
                f"{niche} Collaboration: Special Guest",
                f"Featuring {niche} Artist",
                f"{niche} Team Up: Epic Collaboration"
            ]
        }
        
        return templates.get(category, [f"{niche} Video Idea"])
    
    def _fill_template(
        self,
        template: str,
        niche: str,
        keyword: str,
        theme: str,
        category: str
    ) -> str:
        """Fill a template with actual values."""
        title = template
        
        # Replace placeholders
        title = title.replace("[Song Name]", keyword)
        title = title.replace("[Song Title]", keyword)
        title = title.replace("[Artist Name]", keyword)
        title = title.replace("[Classic Song]", keyword)
        
        # Add theme if available
        if theme and theme not in title.lower():
            title = f"{title} ({theme})"
        
        return title
    
    def _generate_description(
        self,
        category: str,
        niche: str,
        keyword: str,
        theme: str
    ) -> str:
        """Generate a description for the video idea."""
        descriptions = {
            "tutorial": f"Learn how to create {niche} music with this comprehensive tutorial. We'll cover everything from basics to advanced techniques.",
            "review": f"Honest review of {niche} content. Get my real opinion and find out if it's worth your time.",
            "vlog": f"Join me for a day in my life creating {niche} music. See what goes on behind the scenes!",
            "cover": f"Check out my {niche} cover of this amazing song. Hope you enjoy!",
            "original": f"New {niche} original composition. This is my latest creation, hope you like it!",
            "compilation": f"Best {niche} songs compilation. A collection of the greatest tracks in this genre.",
            "reaction": f"Reacting to {niche} for the first time. My honest thoughts and reactions!",
            "interview": f"Exclusive interview with {niche} artist. Learn about their journey and creative process.",
            "behind_the_scenes": f"Behind the scenes of creating {niche} music. See how it all comes together!",
            "educational": f"Deep dive into {niche}. Everything you need to know explained in detail.",
            "entertainment": f"Epic {niche} content that will entertain and amaze you!",
            "collaboration": f"Special {niche} collaboration with amazing artists. Don't miss this!"
        }
        
        base_desc = descriptions.get(category, f"New {niche} video idea.")
        
        if keyword:
            base_desc += f" Featuring {keyword}."
        
        if theme:
            base_desc += f" Theme: {theme}."
        
        return base_desc
    
    def _generate_tags(
        self,
        category: str,
        niche: str,
        keyword: str,
        theme: str
    ) -> List[str]:
        """Generate tags for the video idea."""
        tags = [niche, category, keyword]
        
        # Add niche-specific tags
        niche_words = niche.split()
        tags.extend(niche_words)
        
        # Add category-specific tags
        category_tags = {
            "tutorial": ["how to", "tutorial", "guide", "learn"],
            "review": ["review", "opinion", "honest"],
            "vlog": ["vlog", "daily", "lifestyle"],
            "cover": ["cover", "music", "song"],
            "original": ["original", "new", "music"],
            "compilation": ["compilation", "best of", "playlist"],
            "reaction": ["reaction", "first time"],
            "interview": ["interview", "chat", "talk"],
            "behind_the_scenes": ["bts", "behind the scenes"],
            "educational": ["educational", "explained", "analysis"],
            "entertainment": ["entertainment", "fun", "epic"],
            "collaboration": ["collab", "collaboration", "featuring"]
        }
        
        tags.extend(category_tags.get(category, []))
        
        if theme:
            tags.append(theme)
        
        # Remove duplicates and limit
        return list(dict.fromkeys(tags))[:15]
    
    def _score_ideas(
        self,
        ideas: List[Dict[str, Any]],
        niche: str,
        channel_data: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Score ideas by success potential."""
        scored = []
        
        for idea in ideas:
            score = 0
            
            # Title length score (40-60 chars optimal)
            title_len = len(idea["title"])
            if 40 <= title_len <= 60:
                score += 25
            elif 30 <= title_len <= 70:
                score += 15
            else:
                score += 5
            
            # Keyword relevance score
            keywords = idea.get("keywords", [])
            niche_words = niche.lower().split()
            keyword_matches = sum(1 for kw in keywords if any(nw in kw.lower() for nw in niche_words))
            score += keyword_matches * 10
            
            # Category popularity score (some categories perform better)
            category = idea.get("category", "")
            category_scores = {
                "tutorial": 20,
                "review": 18,
                "educational": 17,
                "compilation": 15,
                "original": 15,
                "cover": 14,
                "vlog": 12,
                "reaction": 12,
                "entertainment": 10,
                "collaboration": 10,
                "interview": 8,
                "behind_the_scenes": 8
            }
            score += category_scores.get(category, 10)
            
            # Channel alignment score (if channel data available)
            if channel_data:
                content_analysis = channel_data.get("content_analysis", {})
                top_keywords = [kw.get("word", "") for kw in content_analysis.get("top_keywords", [])[:5]]
                
                # Check if idea keywords match channel's successful keywords
                idea_keywords_lower = [kw.lower() for kw in keywords]
                matches = sum(1 for tk in top_keywords if any(tk.lower() in ik for ik in idea_keywords_lower))
                score += matches * 5
            
            # Tags count score (more tags = better SEO)
            tags_count = len(idea.get("tags", []))
            if tags_count >= 10:
                score += 10
            elif tags_count >= 5:
                score += 5
            
            # Theme relevance score
            if idea.get("theme"):
                score += 5
            
            # Normalize to 0-100
            success_score = min(100, score)
            
            # Determine success level
            if success_score >= 70:
                success_level = "High"
            elif success_score >= 50:
                success_level = "Medium"
            else:
                success_level = "Low"
            
            idea["success_score"] = success_score
            idea["success_level"] = success_level
            scored.append(idea)
        
        return scored
    
    def _generate_recommendations(
        self,
        ideas: List[Dict[str, Any]],
        niche: str
    ) -> List[str]:
        """Generate recommendations based on ideas."""
        recommendations = []
        
        if not ideas:
            return ["No ideas generated. Check your niche and try again."]
        
        # Find top ideas
        top_ideas = sorted(ideas, key=lambda x: x.get("success_score", 0), reverse=True)[:3]
        
        if top_ideas:
            top_categories = [idea.get("category", "") for idea in top_ideas]
            category_counts = {}
            for cat in top_categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            top_category = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else ""
            
            if top_category:
                recommendations.append(
                    f"Focus on {top_category} content - your top ideas are in this category."
                )
        
        # Check for keyword opportunities
        all_keywords = []
        for idea in ideas[:5]:
            all_keywords.extend(idea.get("keywords", []))
        
        if all_keywords:
            unique_keywords = list(dict.fromkeys(all_keywords))[:5]
            recommendations.append(
                f"Use these trending keywords: {', '.join(unique_keywords[:3])}"
            )
        
        # General recommendations
        recommendations.extend([
            f"Create content around {niche} trends for better visibility.",
            "Post consistently to build audience engagement.",
            "Use SEO-optimized titles (40-60 characters) for better search performance."
        ])
        
        return recommendations

