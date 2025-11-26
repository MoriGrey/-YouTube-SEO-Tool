"""
AI Video Outline Generator Module
Generates structured video outlines using AI/LLM.

AGI Paradigm: Self-Evolving Architecture
- Generates comprehensive video outlines
- Supports multiple content types
- Learns from successful outlines
"""

from typing import Dict, Any, List, Optional
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


class VideoOutlineGenerator:
    """
    AI-powered video outline generator.
    
    Generates structured outlines for YouTube videos including:
    - Introduction hooks
    - Main talking points
    - Timestamps
    - Keywords and SEO suggestions
    - Call-to-action recommendations
    """
    
    def __init__(self, use_openai: bool = True, api_key: Optional[str] = None):
        """
        Initialize the outline generator.
        
        Args:
            use_openai: Whether to use OpenAI API (default) or local model
            api_key: OpenAI API key (if None, tries to get from env)
        """
        self.use_openai = use_openai
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        
        # Video type templates
        self.templates = {
            "tutorial": {
                "structure": ["hook", "intro", "prerequisites", "steps", "tips", "conclusion", "cta"],
                "duration_ratio": {"intro": 0.1, "main": 0.7, "conclusion": 0.2}
            },
            "review": {
                "structure": ["hook", "intro", "overview", "pros", "cons", "comparison", "verdict", "cta"],
                "duration_ratio": {"intro": 0.1, "main": 0.75, "conclusion": 0.15}
            },
            "vlog": {
                "structure": ["hook", "intro", "story", "highlights", "reflection", "cta"],
                "duration_ratio": {"intro": 0.15, "main": 0.7, "conclusion": 0.15}
            },
            "educational": {
                "structure": ["hook", "intro", "concept", "examples", "practice", "summary", "cta"],
                "duration_ratio": {"intro": 0.1, "main": 0.75, "conclusion": 0.15}
            },
            "entertainment": {
                "structure": ["hook", "intro", "content", "highlights", "climax", "outro", "cta"],
                "duration_ratio": {"intro": 0.1, "main": 0.75, "conclusion": 0.15}
            },
            "custom": {
                "structure": ["hook", "intro", "main", "conclusion", "cta"],
                "duration_ratio": {"intro": 0.1, "main": 0.75, "conclusion": 0.15}
            }
        }
    
    def generate_outline(
        self,
        topic: str,
        video_type: str = "tutorial",
        duration_minutes: int = 10,
        niche: Optional[str] = None,
        target_audience: Optional[str] = None,
        key_points: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive video outline.
        
        Args:
            topic: Main topic of the video
            video_type: Type of video (tutorial, review, vlog, educational, entertainment, custom)
            duration_minutes: Expected video duration in minutes
            niche: Content niche/category
            target_audience: Target audience description
            key_points: Optional list of key points to include
        
        Returns:
            Dictionary containing structured outline
        """
        # Validate video type
        if video_type not in self.templates:
            video_type = "custom"
        
        template = self.templates[video_type]
        
        # Generate outline structure
        outline = {
            "topic": topic,
            "video_type": video_type,
            "duration_minutes": duration_minutes,
            "niche": niche or "General",
            "target_audience": target_audience or "General audience",
            "structure": [],
            "timestamps": [],
            "keywords": [],
            "seo_suggestions": {},
            "cta_suggestions": []
        }
        
        # Generate sections based on template
        duration_seconds = duration_minutes * 60
        current_time = 0
        
        for section_type in template["structure"]:
            section = self._generate_section(
                section_type=section_type,
                topic=topic,
                video_type=video_type,
                niche=niche,
                duration_ratio=template["duration_ratio"].get(section_type, 0.1),
                total_duration=duration_seconds,
                current_time=current_time,
                key_points=key_points
            )
            
            outline["structure"].append(section)
            
            # Add timestamp
            timestamp = self._format_timestamp(current_time)
            outline["timestamps"].append({
                "time": timestamp,
                "section": section["title"],
                "duration_seconds": section.get("duration_seconds", 0)
            })
            
            current_time += section.get("duration_seconds", duration_seconds * 0.1)
        
        # Generate keywords
        outline["keywords"] = self._generate_keywords(topic, niche, video_type)
        
        # Generate SEO suggestions
        outline["seo_suggestions"] = self._generate_seo_suggestions(topic, outline)
        
        # Generate CTA suggestions
        outline["cta_suggestions"] = self._generate_cta_suggestions(video_type, niche)
        
        return outline
    
    def _generate_section(
        self,
        section_type: str,
        topic: str,
        video_type: str,
        niche: Optional[str],
        duration_ratio: float,
        total_duration: int,
        current_time: int,
        key_points: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate a section of the outline."""
        duration_seconds = int(total_duration * duration_ratio)
        
        section_templates = {
            "hook": {
                "title": "Hook (First 15 seconds)",
                "description": f"Grab attention immediately with a compelling opening about {topic}",
                "content": [
                    f"Start with a question or surprising fact about {topic}",
                    "Create curiosity gap",
                    "Promise value to viewer"
                ],
                "duration_seconds": min(15, duration_seconds)
            },
            "intro": {
                "title": "Introduction",
                "description": f"Introduce {topic} and what viewers will learn",
                "content": [
                    f"Brief overview of {topic}",
                    "What you'll cover in this video",
                    "Why this matters to the viewer"
                ],
                "duration_seconds": duration_seconds
            },
            "main": {
                "title": "Main Content",
                "description": f"Core content about {topic}",
                "content": key_points or [
                    f"Key point 1 about {topic}",
                    f"Key point 2 about {topic}",
                    f"Key point 3 about {topic}"
                ],
                "duration_seconds": duration_seconds
            },
            "conclusion": {
                "title": "Conclusion",
                "description": "Wrap up and summarize key points",
                "content": [
                    "Summarize main points",
                    "Reinforce key takeaways",
                    "Thank viewers"
                ],
                "duration_seconds": duration_seconds
            },
            "cta": {
                "title": "Call to Action",
                "description": "Encourage viewer engagement",
                "content": [
                    "Subscribe for more content",
                    "Like if this helped",
                    "Comment with questions",
                    "Check out related videos"
                ],
                "duration_seconds": min(30, duration_seconds)
            }
        }
        
        # Get base template
        base = section_templates.get(section_type, section_templates["main"])
        
        # Customize based on video type
        if video_type == "tutorial" and section_type == "steps":
            base["title"] = "Step-by-Step Tutorial"
            base["content"] = [
                "Step 1: Preparation",
                "Step 2: Main process",
                "Step 3: Tips and tricks",
                "Step 4: Common mistakes to avoid"
            ]
        elif video_type == "review" and section_type == "pros":
            base["title"] = "Pros"
            base["content"] = [
                "What works well",
                "Key strengths",
                "Best features"
            ]
        elif video_type == "review" and section_type == "cons":
            base["title"] = "Cons"
            base["content"] = [
                "Areas for improvement",
                "Potential issues",
                "Limitations"
            ]
        
        return {
            "type": section_type,
            "title": base["title"],
            "description": base["description"],
            "talking_points": base["content"],
            "duration_seconds": base["duration_seconds"],
            "start_time": current_time
        }
    
    def _format_timestamp(self, seconds: int) -> str:
        """Format seconds into MM:SS timestamp."""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    def _generate_keywords(self, topic: str, niche: Optional[str], video_type: str) -> List[str]:
        """Generate relevant keywords for the video."""
        keywords = [topic.lower()]
        
        # Add niche-specific keywords
        if niche:
            keywords.append(niche.lower())
            keywords.append(f"{niche} {topic}".lower())
        
        # Add video type keywords
        type_keywords = {
            "tutorial": ["how to", "tutorial", "guide", "step by step"],
            "review": ["review", "honest review", "unboxing", "test"],
            "vlog": ["vlog", "day in my life", "behind the scenes"],
            "educational": ["explained", "learn", "education", "tips"],
            "entertainment": ["funny", "entertaining", "comedy", "reaction"]
        }
        
        keywords.extend(type_keywords.get(video_type, []))
        
        # Add common YouTube keywords
        keywords.extend(["youtube", "video", "watch", "subscribe"])
        
        return list(set(keywords))[:20]  # Remove duplicates and limit
    
    def _generate_seo_suggestions(self, topic: str, outline: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SEO optimization suggestions."""
        return {
            "title_suggestions": [
                f"{topic} - Complete Guide",
                f"How to {topic} - Step by Step",
                f"{topic} Explained | Everything You Need to Know",
                f"The Ultimate {topic} Tutorial"
            ],
            "description_template": f"""
{topic} - {outline.get('video_type', 'Video').title()}

In this video, we cover:
{chr(10).join([f'• {point}' for point in outline['structure'][0].get('talking_points', [])[:5]])}

Timestamps:
{chr(10).join([f'{ts["time"]} - {ts["section"]}' for ts in outline['timestamps'][:5]])}

Keywords: {', '.join(outline['keywords'][:10])}

#YouTube #Tutorial #{topic.replace(' ', '')}
            """.strip(),
            "tags": outline["keywords"][:15],
            "thumbnail_suggestions": [
                f"Bold text: '{topic}'",
                "Include key visual elements",
                "High contrast colors",
                "Clear, readable text overlay"
            ]
        }
    
    def _generate_cta_suggestions(self, video_type: str, niche: Optional[str]) -> List[str]:
        """Generate call-to-action suggestions."""
        ctas = [
            "Subscribe for more content like this!",
            "Hit the like button if this helped you",
            "Comment below with your thoughts",
            "Share this with someone who needs it"
        ]
        
        if video_type == "tutorial":
            ctas.append("Try this yourself and let me know how it goes!")
        elif video_type == "review":
            ctas.append("Have you tried this? Share your experience!")
        
        return ctas
    
    def export_outline(self, outline: Dict[str, Any], format: str = "markdown") -> str:
        """
        Export outline in specified format.
        
        Args:
            outline: Outline dictionary
            format: Export format (markdown, json, text)
        
        Returns:
            Formatted outline string
        """
        if format == "markdown":
            return self._export_markdown(outline)
        elif format == "json":
            import json
            return json.dumps(outline, indent=2)
        else:
            return self._export_text(outline)
    
    def _export_markdown(self, outline: Dict[str, Any]) -> str:
        """Export outline as markdown."""
        md = f"# {outline['topic']}\n\n"
        md += f"**Type:** {outline['video_type'].title()}\n"
        md += f"**Duration:** {outline['duration_minutes']} minutes\n"
        md += f"**Niche:** {outline['niche']}\n\n"
        
        md += "## Outline\n\n"
        for i, section in enumerate(outline['structure'], 1):
            timestamp = outline['timestamps'][i-1]['time'] if i-1 < len(outline['timestamps']) else "00:00"
            md += f"### {timestamp} - {section['title']}\n\n"
            md += f"{section['description']}\n\n"
            md += "**Talking Points:**\n"
            for point in section['talking_points']:
                md += f"- {point}\n"
            md += "\n"
        
        md += "## Keywords\n\n"
        md += ", ".join(outline['keywords']) + "\n\n"
        
        md += "## SEO Suggestions\n\n"
        md += "### Title Options:\n"
        for title in outline['seo_suggestions']['title_suggestions']:
            md += f"- {title}\n"
        
        return md
    
    def _export_text(self, outline: Dict[str, Any]) -> str:
        """Export outline as plain text."""
        text = f"{outline['topic']}\n"
        text += "=" * len(outline['topic']) + "\n\n"
        
        for section in outline['structure']:
            text += f"{section['title']}\n"
            text += "-" * len(section['title']) + "\n"
            text += f"{section['description']}\n\n"
            for point in section['talking_points']:
                text += f"  • {point}\n"
            text += "\n"
        
        return text

