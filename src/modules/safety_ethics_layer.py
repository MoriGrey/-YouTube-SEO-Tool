"""
Safety & Ethics Layer Module

AGI Paradigm: Safety & Ethics Control Layer
- Filters unsafe or unethical content automatically
- Ensures YouTube Community Guidelines compliance
- Prevents spam/clickbait recommendations
- Provides ethical content suggestions
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import re


class SafetyEthicsLayer:
    """
    Safety and ethics layer for content filtering.
    
    AGI Paradigm: Safety & Ethics Control Layer
    - Automatically filters unsafe or unethical content
    - Ensures compliance with YouTube Community Guidelines
    - Prevents spam/clickbait recommendations
    - Provides ethical content suggestions
    """
    
    # YouTube Community Guidelines violations
    VIOLATION_KEYWORDS = {
        "harmful_content": [
            "violence", "hate speech", "harassment", "bullying",
            "dangerous activities", "harmful challenges"
        ],
        "misinformation": [
            "fake news", "conspiracy", "misleading", "false information",
            "medical misinformation", "election fraud"
        ],
        "spam": [
            "click here now", "free money", "guaranteed views",
            "sub4sub", "view4view", "instant subscribers"
        ],
        "inappropriate": [
            "explicit content", "adult content", "nudity",
            "sexual content", "inappropriate language"
        ],
        "copyright": [
            "copyrighted material", "pirated content", "unauthorized use"
        ]
    }
    
    # Clickbait patterns
    CLICKBAIT_PATTERNS = [
        r"you won't believe",
        r"this will shock you",
        r"number \d+ will blow your mind",
        r"doctors hate this",
        r"one weird trick",
        r"this one secret",
        r"click here to find out",
        r"you'll never guess",
        r"what happens next",
        r"the reason will surprise you"
    ]
    
    # Spam indicators
    SPAM_INDICATORS = [
        r"sub4sub",
        r"view4view",
        r"like4like",
        r"free subscribers",
        r"instant views",
        r"guaranteed viral",
        r"click here now",
        r"limited time offer",
        r"act now"
    ]
    
    # Ethical content guidelines
    ETHICAL_GUIDELINES = {
        "transparency": "Be honest about content and avoid misleading claims",
        "authenticity": "Create original, authentic content",
        "respect": "Respect audience and community",
        "accuracy": "Provide accurate information",
        "responsibility": "Take responsibility for content impact"
    }
    
    def __init__(self, data_dir: str = "data"):
        """Initialize Safety & Ethics Layer."""
        self.data_dir = data_dir
        self.data_file = os.path.join(data_dir, "safety_ethics_history.json")
        self._ensure_data_dir()
        self._load_history()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _load_history(self) -> Dict[str, Any]:
        """Load safety and ethics history."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "filtered_content": [],
            "violations_detected": [],
            "safe_recommendations": [],
            "statistics": {
                "total_checks": 0,
                "violations_found": 0,
                "clickbait_detected": 0,
                "spam_detected": 0,
                "safe_content_count": 0
            }
        }
    
    def _save_history(self, data: Dict[str, Any]):
        """Save safety and ethics history."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving safety history: {e}")
    
    def check_content_safety(
        self,
        title: str,
        description: str = "",
        tags: List[str] = None,
        content_type: str = "video"
    ) -> Dict[str, Any]:
        """
        Check content for safety and ethics compliance.
        
        Args:
            title: Video title
            description: Video description
            tags: List of tags
            content_type: Type of content (video, thumbnail, etc.)
        
        Returns:
            Dictionary with safety check results
        """
        if tags is None:
            tags = []
        
        history = self._load_history()
        history["statistics"]["total_checks"] += 1
        
        # Combine all text for analysis
        full_text = f"{title} {description} {' '.join(tags)}".lower()
        
        # Check for violations
        violations = self._detect_violations(full_text)
        
        # Check for clickbait
        clickbait_score = self._detect_clickbait(title, description)
        
        # Check for spam
        spam_score = self._detect_spam(full_text)
        
        # Calculate overall risk score
        risk_score = self._calculate_risk_score(violations, clickbait_score, spam_score)
        
        # Determine safety status
        if risk_score >= 0.7:
            safety_status = "high_risk"
            recommendation = "Content has high risk of violating guidelines. Major changes required."
        elif risk_score >= 0.5:
            safety_status = "medium_risk"
            recommendation = "Content has moderate risk. Some improvements recommended."
        elif risk_score >= 0.3:
            safety_status = "low_risk"
            recommendation = "Content is mostly safe but could be improved."
        else:
            safety_status = "safe"
            recommendation = "Content appears safe and compliant."
        
        # Update statistics
        if violations:
            history["statistics"]["violations_found"] += 1
        if clickbait_score >= 0.5:
            history["statistics"]["clickbait_detected"] += 1
        if spam_score >= 0.5:
            history["statistics"]["spam_detected"] += 1
        if safety_status == "safe":
            history["statistics"]["safe_content_count"] += 1
        
        # Record check
        check_result = {
            "timestamp": datetime.now().isoformat(),
            "content": {
                "title": title,
                "description": description[:200] + "..." if len(description) > 200 else description,
                "tags": tags,
                "content_type": content_type
            },
            "violations": violations,
            "clickbait_score": clickbait_score,
            "spam_score": spam_score,
            "risk_score": risk_score,
            "safety_status": safety_status,
            "recommendation": recommendation,
            "suggestions": self._generate_safety_suggestions(violations, clickbait_score, spam_score)
        }
        
        # Save to history
        if violations or clickbait_score >= 0.5 or spam_score >= 0.5:
            history["filtered_content"].append(check_result)
            if violations:
                history["violations_detected"].append({
                    "timestamp": check_result["timestamp"],
                    "violations": violations,
                    "content": check_result["content"]
                })
        else:
            history["safe_recommendations"].append(check_result)
        
        # Keep only last 1000 entries
        for key in ["filtered_content", "violations_detected", "safe_recommendations"]:
            if len(history[key]) > 1000:
                history[key] = history[key][-1000:]
        
        self._save_history(history)
        
        return check_result
    
    def _detect_violations(self, text: str) -> Dict[str, List[str]]:
        """Detect YouTube Community Guidelines violations."""
        violations = {}
        
        for violation_type, keywords in self.VIOLATION_KEYWORDS.items():
            found_keywords = []
            for keyword in keywords:
                if keyword.lower() in text:
                    found_keywords.append(keyword)
            
            if found_keywords:
                violations[violation_type] = found_keywords
        
        return violations
    
    def _detect_clickbait(self, title: str, description: str = "") -> float:
        """Detect clickbait patterns in content."""
        text = f"{title} {description}".lower()
        matches = 0
        total_patterns = len(self.CLICKBAIT_PATTERNS)
        
        for pattern in self.CLICKBAIT_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                matches += 1
        
        # Also check for excessive capitalization
        if title:
            caps_ratio = sum(1 for c in title if c.isupper()) / len(title) if title else 0
            if caps_ratio > 0.5 and len(title) > 10:
                matches += 1
                total_patterns += 1
        
        # Check for excessive punctuation
        if title:
            punct_count = sum(1 for c in title if c in "!?")
            if punct_count >= 3:
                matches += 1
                total_patterns += 1
        
        return min(matches / total_patterns if total_patterns > 0 else 0, 1.0)
    
    def _detect_spam(self, text: str) -> float:
        """Detect spam indicators in content."""
        matches = 0
        total_indicators = len(self.SPAM_INDICATORS)
        
        for pattern in self.SPAM_INDICATORS:
            if re.search(pattern, text, re.IGNORECASE):
                matches += 1
        
        # Check for excessive repetition
        words = text.split()
        if len(words) > 0:
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            max_freq = max(word_freq.values()) if word_freq else 0
            if max_freq > len(words) * 0.3:  # More than 30% repetition
                matches += 1
                total_indicators += 1
        
        return min(matches / total_indicators if total_indicators > 0 else 0, 1.0)
    
    def _calculate_risk_score(
        self,
        violations: Dict[str, List[str]],
        clickbait_score: float,
        spam_score: float
    ) -> float:
        """Calculate overall risk score."""
        # Violations have highest weight
        violation_score = min(len(violations) * 0.4, 0.6)
        
        # Clickbait and spam have moderate weight
        clickbait_weight = clickbait_score * 0.2
        spam_weight = spam_score * 0.2
        
        total_score = violation_score + clickbait_weight + spam_weight
        
        return min(total_score, 1.0)
    
    def _generate_safety_suggestions(
        self,
        violations: Dict[str, List[str]],
        clickbait_score: float,
        spam_score: float
    ) -> List[str]:
        """Generate safety improvement suggestions."""
        suggestions = []
        
        if violations:
            for violation_type, keywords in violations.items():
                if violation_type == "harmful_content":
                    suggestions.append("Remove harmful content references. Focus on positive, constructive content.")
                elif violation_type == "misinformation":
                    suggestions.append("Ensure all claims are accurate and verifiable. Avoid spreading misinformation.")
                elif violation_type == "spam":
                    suggestions.append("Remove spam keywords. Focus on authentic, valuable content.")
                elif violation_type == "inappropriate":
                    suggestions.append("Remove inappropriate content. Keep content suitable for all audiences.")
                elif violation_type == "copyright":
                    suggestions.append("Ensure you have rights to use all content. Avoid copyright violations.")
        
        if clickbait_score >= 0.5:
            suggestions.append("Reduce clickbait language. Be honest and transparent about content.")
            suggestions.append("Avoid excessive capitalization and punctuation. Keep titles clear and informative.")
        
        if spam_score >= 0.5:
            suggestions.append("Remove spam indicators. Focus on authentic engagement strategies.")
            suggestions.append("Avoid repetitive keywords. Use diverse, natural language.")
        
        if not suggestions:
            suggestions.append("Content appears safe. Continue following ethical guidelines.")
        
        return suggestions
    
    def filter_recommendations(
        self,
        recommendations: List[str]
    ) -> Dict[str, Any]:
        """
        Filter recommendations for safety and ethics.
        
        Args:
            recommendations: List of recommendation strings
        
        Returns:
            Dictionary with filtered recommendations and safety info
        """
        safe_recommendations = []
        filtered_out = []
        
        for rec in recommendations:
            check_result = self.check_content_safety(
                title=rec,
                description="",
                tags=[],
                content_type="recommendation"
            )
            
            if check_result["safety_status"] in ["safe", "low_risk"]:
                safe_recommendations.append({
                    "recommendation": rec,
                    "risk_score": check_result["risk_score"],
                    "safety_status": check_result["safety_status"]
                })
            else:
                filtered_out.append({
                    "recommendation": rec,
                    "risk_score": check_result["risk_score"],
                    "safety_status": check_result["safety_status"],
                    "reasons": check_result["violations"]
                })
        
        return {
            "safe_recommendations": safe_recommendations,
            "filtered_out": filtered_out,
            "total_checked": len(recommendations),
            "safe_count": len(safe_recommendations),
            "filtered_count": len(filtered_out)
        }
    
    def get_ethical_guidelines(self) -> Dict[str, Any]:
        """Get ethical content guidelines."""
        return {
            "guidelines": self.ETHICAL_GUIDELINES,
            "best_practices": [
                "Be transparent and honest about content",
                "Create original, authentic content",
                "Respect your audience and community",
                "Provide accurate, verifiable information",
                "Take responsibility for content impact",
                "Avoid misleading or deceptive practices",
                "Follow YouTube Community Guidelines",
                "Respect copyright and intellectual property",
                "Promote positive, constructive content"
            ],
            "avoid": [
                "Clickbait titles and thumbnails",
                "Spam and manipulative tactics",
                "Misinformation and false claims",
                "Harmful or dangerous content",
                "Copyright violations",
                "Inappropriate content",
                "Deceptive practices"
            ]
        }
    
    def get_safety_statistics(self) -> Dict[str, Any]:
        """Get safety and ethics statistics."""
        history = self._load_history()
        stats = history.get("statistics", {})
        
        total_checks = stats.get("total_checks", 0)
        if total_checks == 0:
            return {
                "total_checks": 0,
                "violation_rate": 0.0,
                "clickbait_rate": 0.0,
                "spam_rate": 0.0,
                "safety_rate": 0.0
            }
        
        return {
            "total_checks": total_checks,
            "violation_rate": stats.get("violations_found", 0) / total_checks,
            "clickbait_rate": stats.get("clickbait_detected", 0) / total_checks,
            "spam_rate": stats.get("spam_detected", 0) / total_checks,
            "safety_rate": stats.get("safe_content_count", 0) / total_checks,
            "violations_found": stats.get("violations_found", 0),
            "clickbait_detected": stats.get("clickbait_detected", 0),
            "spam_detected": stats.get("spam_detected", 0),
            "safe_content_count": stats.get("safe_content_count", 0)
        }
    
    def get_recent_violations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent violations detected."""
        history = self._load_history()
        violations = history.get("violations_detected", [])
        return violations[-limit:]
    
    def is_content_safe(
        self,
        title: str,
        description: str = "",
        tags: List[str] = None
    ) -> bool:
        """
        Quick check if content is safe.
        
        Returns:
            True if content is safe, False otherwise
        """
        if tags is None:
            tags = []
        
        check_result = self.check_content_safety(title, description, tags)
        return check_result["safety_status"] in ["safe", "low_risk"]

