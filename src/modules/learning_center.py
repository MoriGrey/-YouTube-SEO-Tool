"""
Learning Center Module
Manages educational content, tutorials, and learning resources.

AGI Paradigm: Omnipresent Learning
- Provides structured learning paths
- Tracks user progress
- Offers interactive examples
"""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
import markdown


class LearningCenter:
    """
    Learning center for educational resources.
    
    Manages:
    - Tutorial content (Markdown-based)
    - Learning paths
    - Progress tracking
    - Interactive examples
    """
    
    def __init__(self, content_dir: Optional[str] = None):
        """
        Initialize learning center.
        
        Args:
            content_dir: Directory containing tutorial markdown files
        """
        if content_dir is None:
            # Default to content/tutorials in project root
            project_root = Path(__file__).parent.parent.parent
            content_dir = project_root / "content" / "tutorials"
        
        self.content_dir = Path(content_dir)
        self.tutorials = {}
        self.categories = {
            "getting-started": "Getting Started",
            "seo-basics": "SEO Basics",
            "advanced": "Advanced Features",
            "optimization": "Optimization",
            "analytics": "Analytics",
            "growth": "Growth Strategies"
        }
        
        # Load tutorials
        self._load_tutorials()
    
    def _load_tutorials(self):
        """Load all tutorial markdown files."""
        if not self.content_dir.exists():
            return
        
        for file_path in self.content_dir.glob("*.md"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Parse frontmatter if present
                tutorial = self._parse_tutorial(file_path.stem, content)
                self.tutorials[tutorial["id"]] = tutorial
            except Exception as e:
                print(f"Error loading tutorial {file_path}: {e}")
    
    def _parse_tutorial(self, tutorial_id: str, content: str) -> Dict[str, Any]:
        """Parse tutorial markdown file."""
        # Check for frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
                
                # Parse YAML frontmatter (simple)
                metadata = {}
                for line in frontmatter.strip().split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        metadata[key.strip()] = value.strip().strip('"').strip("'")
            else:
                body = content
                metadata = {}
        else:
            body = content
            metadata = {}
        
        # Extract title from first heading or metadata
        title = metadata.get("title", tutorial_id.replace("-", " ").title())
        
        # Convert markdown to HTML
        html_content = markdown.markdown(body, extensions=['fenced_code', 'tables'])
        
        return {
            "id": tutorial_id,
            "title": title,
            "content": html_content,
            "markdown": body,
            "category": metadata.get("category", "general"),
            "difficulty": metadata.get("difficulty", "beginner"),
            "duration": metadata.get("duration", "5 min"),
            "tags": metadata.get("tags", "").split(",") if metadata.get("tags") else []
        }
    
    def get_tutorial(self, tutorial_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific tutorial by ID."""
        return self.tutorials.get(tutorial_id)
    
    def list_tutorials(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all tutorials, optionally filtered by category."""
        tutorials = list(self.tutorials.values())
        
        if category:
            tutorials = [t for t in tutorials if t.get("category") == category]
        
        return sorted(tutorials, key=lambda x: x.get("title", ""))
    
    def get_categories(self) -> Dict[str, str]:
        """Get available tutorial categories."""
        return self.categories
    
    def search_tutorials(self, query: str) -> List[Dict[str, Any]]:
        """Search tutorials by title or content."""
        query_lower = query.lower()
        results = []
        
        for tutorial in self.tutorials.values():
            if (query_lower in tutorial["title"].lower() or
                query_lower in tutorial["markdown"].lower()):
                results.append(tutorial)
        
        return results
    
    def get_learning_path(self, path_name: str) -> List[Dict[str, Any]]:
        """
        Get a structured learning path.
        
        Args:
            path_name: Name of the learning path (e.g., "beginner", "advanced")
        """
        paths = {
            "beginner": [
                "01-getting-started",
                "02-keyword-research",
                "03-seo-optimization"
            ],
            "intermediate": [
                "02-keyword-research",
                "03-seo-optimization",
                "04-advanced-features"
            ],
            "advanced": [
                "04-advanced-features",
                "05-analytics",
                "06-growth-strategies"
            ]
        }
        
        tutorial_ids = paths.get(path_name, [])
        return [self.tutorials[tid] for tid in tutorial_ids if tid in self.tutorials]

