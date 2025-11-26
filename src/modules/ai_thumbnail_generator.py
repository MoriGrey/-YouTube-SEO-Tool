"""
AI Thumbnail Generator Module
Generate thumbnails using AI (DALL-E/Stable Diffusion) or templates.
"""

from typing import Dict, Any, List, Optional
import os
import sys
import base64
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


class AIThumbnailGenerator:
    """
    AI-powered thumbnail generator.
    
    AGI Paradigm: Self-Evolving Architecture
    - Generates thumbnails using AI APIs
    - Creates A/B test variations
    - Estimates CTR potential
    - Falls back to templates if AI unavailable
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        stable_diffusion_api_key: Optional[str] = None,
        stable_diffusion_url: Optional[str] = None
    ):
        """
        Initialize the AI thumbnail generator.
        
        Args:
            openai_api_key: OpenAI API key for DALL-E
            stable_diffusion_api_key: Stable Diffusion API key (if needed)
            stable_diffusion_url: Stable Diffusion API URL
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.stable_diffusion_api_key = stable_diffusion_api_key
        self.stable_diffusion_url = stable_diffusion_url or "https://api.stability.ai"
        
        # Check if AI services are available
        self.dalle_available = bool(self.openai_api_key)
        self.stable_diffusion_available = bool(self.stable_diffusion_api_key or self.stable_diffusion_url)
        self.ai_available = self.dalle_available or self.stable_diffusion_available
    
    def generate_thumbnail(
        self,
        title: str,
        description: str,
        niche: str,
        num_variations: int = 3,
        style: str = "youtube_thumbnail"
    ) -> Dict[str, Any]:
        """
        Generate thumbnail variations for a video.
        
        Args:
            title: Video title
            description: Video description
            niche: Video niche
            num_variations: Number of variations to generate
            style: Thumbnail style (youtube_thumbnail, minimalist, bold, etc.)
        
        Returns:
            Dictionary with generated thumbnails and metadata
        """
        # Extract key elements from title and description
        key_elements = self._extract_key_elements(title, description, niche)
        
        # Generate prompt for AI
        prompt = self._create_prompt(key_elements, style)
        
        variations = []
        
        # Try AI generation first
        if self.ai_available:
            for i in range(num_variations):
                try:
                    if self.dalle_available:
                        thumbnail_data = self._generate_with_dalle(prompt, variation=i)
                    elif self.stable_diffusion_available:
                        thumbnail_data = self._generate_with_stable_diffusion(prompt, variation=i)
                    else:
                        thumbnail_data = None
                    
                    if thumbnail_data:
                        variations.append(thumbnail_data)
                except Exception as e:
                    # Fall back to template if AI fails
                    thumbnail_data = self._generate_template_thumbnail(
                        key_elements, style, variation=i
                    )
                    thumbnail_data["generation_method"] = "template_fallback"
                    thumbnail_data["error"] = str(e)
                    variations.append(thumbnail_data)
        else:
            # Use template-based generation
            for i in range(num_variations):
                thumbnail_data = self._generate_template_thumbnail(
                    key_elements, style, variation=i
                )
                thumbnail_data["generation_method"] = "template"
                variations.append(thumbnail_data)
        
        # Estimate CTR for each variation
        for variation in variations:
            variation["estimated_ctr"] = self._estimate_ctr(variation, title)
        
        # Sort by estimated CTR
        variations.sort(key=lambda x: x.get("estimated_ctr", 0), reverse=True)
        
        return {
            "title": title,
            "niche": niche,
            "variations": variations,
            "best_variation": variations[0] if variations else None,
            "generation_method": "ai" if self.ai_available else "template",
            "recommendations": self._generate_recommendations(variations, title)
        }
    
    def _extract_key_elements(
        self,
        title: str,
        description: str,
        niche: str
    ) -> Dict[str, Any]:
        """Extract key elements for thumbnail generation."""
        # Extract main keywords from title
        title_words = title.split()
        main_keywords = [w for w in title_words if len(w) > 3][:5]
        
        # Extract emotions/tones from description
        emotions = []
        emotion_keywords = {
            "epic": ["epic", "amazing", "incredible", "unbelievable"],
            "funny": ["funny", "hilarious", "comedy", "laugh"],
            "educational": ["learn", "tutorial", "guide", "how to"],
            "emotional": ["emotional", "touching", "heartfelt", "moving"],
            "exciting": ["exciting", "thrilling", "action", "adventure"]
        }
        
        desc_lower = description.lower()
        for emotion, keywords in emotion_keywords.items():
            if any(kw in desc_lower for kw in keywords):
                emotions.append(emotion)
        
        return {
            "main_keywords": main_keywords,
            "niche": niche,
            "emotions": emotions[:2] if emotions else ["neutral"],
            "title_length": len(title),
            "has_numbers": any(char.isdigit() for char in title)
        }
    
    def _create_prompt(
        self,
        key_elements: Dict[str, Any],
        style: str
    ) -> str:
        """Create a prompt for AI thumbnail generation."""
        keywords = ", ".join(key_elements.get("main_keywords", [])[:3])
        niche = key_elements.get("niche", "")
        emotions = ", ".join(key_elements.get("emotions", []))
        
        style_descriptions = {
            "youtube_thumbnail": "YouTube thumbnail style, bold text overlay, high contrast, eye-catching",
            "minimalist": "Minimalist design, clean, simple, elegant",
            "bold": "Bold design, vibrant colors, strong typography",
            "professional": "Professional design, polished, high-quality",
            "playful": "Playful design, fun colors, creative composition"
        }
        
        style_desc = style_descriptions.get(style, style_descriptions["youtube_thumbnail"])
        
        prompt = (
            f"Create a YouTube thumbnail image for a video about {niche}. "
            f"Main keywords: {keywords}. "
            f"Style: {style_desc}. "
            f"Emotion: {emotions}. "
            f"High contrast, bold text overlay, eye-catching design, "
            f"1280x720 pixels, professional quality, YouTube thumbnail style"
        )
        
        return prompt
    
    def _generate_with_dalle(
        self,
        prompt: str,
        variation: int = 0
    ) -> Optional[Dict[str, Any]]:
        """Generate thumbnail using DALL-E API."""
        try:
            import openai
            
            if not self.openai_api_key:
                return None
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            # Create variation in prompt
            variation_prompt = f"{prompt}, variation {variation + 1}"
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=variation_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            return {
                "image_url": image_url,
                "prompt": variation_prompt,
                "generation_method": "dalle-3",
                "variation": variation,
                "estimated_cost": 0.04  # DALL-E 3 cost per image
            }
        except ImportError:
            return None
        except Exception as e:
            raise Exception(f"DALL-E generation failed: {str(e)}")
    
    def _generate_with_stable_diffusion(
        self,
        prompt: str,
        variation: int = 0
    ) -> Optional[Dict[str, Any]]:
        """Generate thumbnail using Stable Diffusion API."""
        try:
            import requests
            
            # Create variation in prompt
            variation_prompt = f"{prompt}, variation {variation + 1}"
            
            headers = {}
            if self.stable_diffusion_api_key:
                headers["Authorization"] = f"Bearer {self.stable_diffusion_api_key}"
            
            # Use Stability AI API
            url = f"{self.stable_diffusion_url}/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            
            payload = {
                "text_prompts": [{"text": variation_prompt}],
                "cfg_scale": 7,
                "height": 720,
                "width": 1280,
                "samples": 1,
                "steps": 30
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract image (base64 or URL depending on API)
            if "artifacts" in data and data["artifacts"]:
                image_data = data["artifacts"][0].get("base64")
                if image_data:
                    image_url = f"data:image/png;base64,{image_data}"
                else:
                    image_url = data["artifacts"][0].get("url", "")
            else:
                return None
            
            return {
                "image_url": image_url,
                "prompt": variation_prompt,
                "generation_method": "stable-diffusion",
                "variation": variation,
                "estimated_cost": 0.0  # May vary
            }
        except ImportError:
            return None
        except Exception as e:
            raise Exception(f"Stable Diffusion generation failed: {str(e)}")
    
    def _generate_template_thumbnail(
        self,
        key_elements: Dict[str, Any],
        style: str,
        variation: int = 0
    ) -> Dict[str, Any]:
        """Generate a template-based thumbnail (fallback)."""
        keywords = key_elements.get("main_keywords", [])
        niche = key_elements.get("niche", "")
        
        # Create template description
        template_description = {
            "layout": "Text overlay on background",
            "background": f"{niche} themed background",
            "text": " ".join(keywords[:3]) if keywords else niche,
            "colors": self._get_color_scheme(style, variation),
            "style": style
        }
        
        # Generate a template specification (not actual image, but instructions)
        return {
            "template_description": template_description,
            "generation_method": "template",
            "variation": variation,
            "instructions": self._get_template_instructions(template_description),
            "estimated_cost": 0.0
        }
    
    def _get_color_scheme(self, style: str, variation: int) -> List[str]:
        """Get color scheme for template."""
        schemes = {
            "youtube_thumbnail": [
                ["#FF0000", "#FFFFFF", "#000000"],  # Red, white, black
                ["#0000FF", "#FFFFFF", "#FFD700"],  # Blue, white, gold
                ["#FF6B00", "#FFFFFF", "#000000"]   # Orange, white, black
            ],
            "minimalist": [
                ["#FFFFFF", "#000000", "#808080"],  # White, black, gray
                ["#F5F5F5", "#333333", "#CCCCCC"]   # Light gray, dark gray
            ],
            "bold": [
                ["#FF0000", "#FFFF00", "#0000FF"],  # Red, yellow, blue
                ["#00FF00", "#FF00FF", "#00FFFF"]   # Green, magenta, cyan
            ]
        }
        
        scheme = schemes.get(style, schemes["youtube_thumbnail"])
        return scheme[variation % len(scheme)]
    
    def _get_template_instructions(
        self,
        template_description: Dict[str, Any]
    ) -> str:
        """Get instructions for creating template thumbnail."""
        colors = ", ".join(template_description.get("colors", []))
        text = template_description.get("text", "")
        background = template_description.get("background", "")
        
        return (
            f"Create a {template_description.get('style')} thumbnail: "
            f"Background: {background}. "
            f"Text overlay: '{text}' in bold font. "
            f"Color scheme: {colors}. "
            f"Size: 1280x720 pixels. "
            f"High contrast, eye-catching design."
        )
    
    def _estimate_ctr(
        self,
        variation: Dict[str, Any],
        title: str
    ) -> float:
        """Estimate click-through rate for a thumbnail variation."""
        ctr = 5.0  # Base CTR (5%)
        
        # Adjust based on generation method
        method = variation.get("generation_method", "template")
        if method in ["dalle-3", "stable-diffusion"]:
            ctr += 2.0  # AI-generated thumbnails tend to perform better
        
        # Adjust based on style
        style = variation.get("template_description", {}).get("style", "")
        if style == "youtube_thumbnail":
            ctr += 1.0
        elif style == "bold":
            ctr += 1.5
        
        # Adjust based on colors (high contrast = better CTR)
        colors = variation.get("template_description", {}).get("colors", [])
        if colors and len(colors) >= 2:
            # High contrast colors
            if any(c in ["#FF0000", "#0000FF", "#00FF00"] for c in colors):
                ctr += 0.5
        
        # Title length affects CTR
        if 40 <= len(title) <= 60:
            ctr += 0.5
        
        return min(15.0, max(2.0, ctr))  # Clamp between 2% and 15%
    
    def _generate_recommendations(
        self,
        variations: List[Dict[str, Any]],
        title: str
    ) -> List[str]:
        """Generate recommendations for thumbnail selection."""
        recommendations = []
        
        if not variations:
            return ["No variations generated. Check API keys or use template mode."]
        
        # Find best variation
        best = variations[0] if variations else None
        if best:
            best_ctr = best.get("estimated_ctr", 0)
            recommendations.append(
                f"Recommended variation has estimated CTR of {best_ctr:.1f}%"
            )
        
        # A/B testing recommendation
        if len(variations) >= 2:
            recommendations.append(
                f"Test {len(variations)} variations to find the best performer. "
                f"Run A/B test for at least 1,000 impressions each."
            )
        
        # Style recommendations
        if best:
            method = best.get("generation_method", "")
            if method == "template":
                recommendations.append(
                    "Consider using AI generation (DALL-E or Stable Diffusion) "
                    "for better thumbnail quality. Set OPENAI_API_KEY environment variable."
                )
        
        # General best practices
        recommendations.extend([
            "Use high contrast colors for better visibility",
            "Keep text overlay concise and readable",
            "Test different styles to find what works for your audience",
            "Monitor CTR and update thumbnails based on performance"
        ])
        
        return recommendations
    
    def generate_ab_test_variations(
        self,
        title: str,
        description: str,
        niche: str,
        num_tests: int = 5
    ) -> Dict[str, Any]:
        """Generate A/B test variations for thumbnail."""
        # Generate multiple variations with different styles
        styles = ["youtube_thumbnail", "bold", "minimalist", "professional", "playful"]
        
        all_variations = []
        for i, style in enumerate(styles[:num_tests]):
            result = self.generate_thumbnail(
                title=title,
                description=description,
                niche=niche,
                num_variations=1,
                style=style
            )
            
            if result.get("variations"):
                variation = result["variations"][0]
                variation["test_id"] = f"test_{i+1}"
                variation["style"] = style
                all_variations.append(variation)
        
        return {
            "title": title,
            "niche": niche,
            "test_variations": all_variations,
            "recommended_tests": min(3, len(all_variations)),  # Test top 3
            "testing_guidelines": [
                "Test each variation for at least 1,000 impressions",
                "Monitor CTR, views, and engagement",
                "Choose winner based on highest CTR after statistical significance",
                "Update all thumbnails to winning design"
            ]
        }

