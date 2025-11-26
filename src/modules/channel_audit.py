"""
Channel Audit Module
Comprehensive channel audit report on a single page.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.channel_analyzer import ChannelAnalyzer
from src.modules.video_seo_audit import VideoSEOAudit
from src.modules.competitor_analyzer import CompetitorAnalyzer
from src.modules.keyword_researcher import KeywordResearcher
from src.modules.title_optimizer import TitleOptimizer
from src.modules.description_generator import DescriptionGenerator
from src.modules.tag_suggester import TagSuggester


class ChannelAudit:
    """
    Comprehensive channel audit system.
    
    AGI Paradigm: Self-Evolving Architecture
    - Analyzes entire channel performance
    - Identifies optimization opportunities
    - Provides actionable recommendations
    """
    
    def __init__(
        self,
        client: YouTubeClient,
        channel_analyzer: ChannelAnalyzer,
        video_seo_audit: VideoSEOAudit,
        competitor_analyzer: CompetitorAnalyzer
    ):
        self.client = client
        self.channel_analyzer = channel_analyzer
        self.video_seo_audit = video_seo_audit
        self.competitor_analyzer = competitor_analyzer
    
    def perform_audit(
        self,
        channel_handle: str,
        niche: str,
        include_competitors: bool = True,
        max_videos: int = 50
    ) -> Dict[str, Any]:
        """
        Perform comprehensive channel audit.
        
        Args:
            channel_handle: Channel handle to audit
            niche: Channel niche
            include_competitors: Whether to include competitor comparison
            max_videos: Maximum number of videos to analyze
        
        Returns:
            Comprehensive audit report
        """
        # Get channel analysis
        channel_analysis = self.channel_analyzer.analyze_channel(channel_handle)
        
        # Get channel videos for SEO audit
        channel_data = self.client.get_channel_by_handle(channel_handle)
        if not channel_data.get("items"):
            raise ValueError(f"Channel @{channel_handle} not found")
        
        channel_id = channel_data["items"][0]["id"]
        videos = self.client.get_channel_videos(channel_id, max_results=max_videos)
        
        # Perform SEO audit on all videos
        seo_audits = []
        seo_scores = []
        
        for video in videos[:max_videos]:
            video_id = video["id"]
            try:
                audit_result = self.video_seo_audit.audit_video(
                    video_id=video_id,
                    channel_handle=channel_handle,
                    niche=niche
                )
                seo_audits.append({
                    "video_id": video_id,
                    "title": video["snippet"]["title"],
                    "seo_score": audit_result.get("overall_score", 0),
                    "recommendations": audit_result.get("recommendations", [])
                })
                seo_scores.append(audit_result.get("overall_score", 0))
            except Exception as e:
                # Skip videos that fail audit
                continue
        
        # Calculate SEO health score
        avg_seo_score = sum(seo_scores) / len(seo_scores) if seo_scores else 0
        
        # Identify content gaps
        content_gaps = self._identify_content_gaps(videos, niche)
        
        # Find optimization opportunities
        optimization_opportunities = self._find_optimization_opportunities(
            channel_analysis, seo_audits, videos
        )
        
        # Competitor comparison (if requested)
        competitor_comparison = None
        if include_competitors:
            try:
                competitors = self.competitor_analyzer.find_competitors(
                    niche_keywords=[niche],
                    max_competitors=5
                )
                if competitors:
                    competitor_comparison = self._compare_with_competitors(
                        channel_analysis, competitors
                    )
            except Exception:
                pass
        
        # Generate action items
        action_items = self._generate_action_items(
            channel_analysis,
            seo_audits,
            content_gaps,
            optimization_opportunities,
            competitor_comparison
        )
        
        # Calculate overall channel health score
        health_score = self._calculate_health_score(
            channel_analysis,
            avg_seo_score,
            seo_audits,
            optimization_opportunities
        )
        
        return {
            "audit_date": datetime.now().isoformat(),
            "channel_info": channel_analysis.get("channel_info", {}),
            "channel_statistics": channel_analysis.get("statistics", {}),
            "overall_health_score": health_score,
            "seo_health": {
                "average_seo_score": avg_seo_score,
                "seo_score_distribution": self._calculate_score_distribution(seo_scores),
                "videos_audited": len(seo_audits),
                "top_performers": sorted(seo_audits, key=lambda x: x["seo_score"], reverse=True)[:5],
                "needs_improvement": sorted(seo_audits, key=lambda x: x["seo_score"])[:5]
            },
            "video_performance": channel_analysis.get("video_performance", {}),
            "growth_analysis": channel_analysis.get("growth_analysis", {}),
            "engagement_analysis": channel_analysis.get("engagement_analysis", {}),
            "content_analysis": channel_analysis.get("content_analysis", {}),
            "content_gaps": content_gaps,
            "optimization_opportunities": optimization_opportunities,
            "competitor_comparison": competitor_comparison,
            "action_items": action_items,
            "recommendations": channel_analysis.get("recommendations", [])
        }
    
    def _identify_content_gaps(
        self,
        videos: List[Dict[str, Any]],
        niche: str
    ) -> List[Dict[str, Any]]:
        """Identify content gaps in the channel."""
        gaps = []
        
        if not videos:
            gaps.append({
                "type": "no_content",
                "description": "Channel has no videos. Start creating content!",
                "priority": "high"
            })
            return gaps
        
        # Analyze video titles for content types
        titles = [v["snippet"]["title"].lower() for v in videos]
        
        # Check for common content types
        content_types = {
            "tutorial": ["how to", "tutorial", "guide", "learn"],
            "review": ["review", "honest", "opinion"],
            "compilation": ["best of", "top 10", "compilation"],
            "behind_the_scenes": ["behind the scenes", "bts", "making of"],
            "collaboration": ["collab", "with", "featuring"]
        }
        
        found_types = set()
        for title in titles:
            for content_type, keywords in content_types.items():
                if any(kw in title for kw in keywords):
                    found_types.add(content_type)
                    break
        
        # Identify missing content types
        missing_types = set(content_types.keys()) - found_types
        for missing_type in missing_types:
            gaps.append({
                "type": "missing_content_type",
                "content_type": missing_type,
                "description": f"Channel lacks {missing_type} content. Consider creating {missing_type} videos.",
                "priority": "medium"
            })
        
        # Check for seasonal/trending content
        gaps.append({
            "type": "trending_opportunity",
            "description": "Consider creating content around current trends in your niche.",
            "priority": "high"
        })
        
        return gaps
    
    def _find_optimization_opportunities(
        self,
        channel_analysis: Dict[str, Any],
        seo_audits: List[Dict[str, Any]],
        videos: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Find optimization opportunities."""
        opportunities = []
        
        # SEO opportunities
        low_seo_videos = [a for a in seo_audits if a["seo_score"] < 60]
        if low_seo_videos:
            opportunities.append({
                "type": "seo_optimization",
                "description": f"{len(low_seo_videos)} videos have low SEO scores. Optimize titles, descriptions, and tags.",
                "priority": "high",
                "affected_videos": len(low_seo_videos)
            })
        
        # Title optimization
        content_analysis = channel_analysis.get("content_analysis", {})
        avg_title_length = content_analysis.get("average_title_length", 0)
        if avg_title_length < 40 or avg_title_length > 60:
            opportunities.append({
                "type": "title_optimization",
                "description": f"Average title length is {avg_title_length:.0f} characters. Optimal is 40-60 characters.",
                "priority": "medium"
            })
        
        # Engagement opportunities
        engagement_analysis = channel_analysis.get("engagement_analysis", {})
        avg_engagement = engagement_analysis.get("average_engagement_rate", 0)
        if avg_engagement < 3.0:
            opportunities.append({
                "type": "engagement_improvement",
                "description": f"Engagement rate is {avg_engagement:.2f}%. Try asking questions, using polls, and creating interactive content.",
                "priority": "high"
            })
        
        # Upload frequency
        growth_analysis = channel_analysis.get("growth_analysis", {})
        avg_days_between = growth_analysis.get("average_days_between_videos", 0)
        if avg_days_between > 14:
            opportunities.append({
                "type": "upload_frequency",
                "description": f"Average {avg_days_between:.0f} days between videos. Consider posting more frequently (weekly or bi-weekly).",
                "priority": "medium"
            })
        
        return opportunities
    
    def _compare_with_competitors(
        self,
        channel_analysis: Dict[str, Any],
        competitors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compare channel with competitors."""
        if not competitors:
            return {}
        
        channel_stats = channel_analysis.get("statistics", {})
        channel_subs = channel_stats.get("subscribers", 0)
        channel_views = channel_stats.get("total_views", 0)
        channel_videos = channel_stats.get("total_videos", 0)
        
        # Calculate competitor averages
        competitor_subs = [c.get("subscribers", 0) for c in competitors]
        competitor_views = [c.get("total_views", 0) for c in competitors]
        competitor_videos = [c.get("video_count", 0) for c in competitors]
        
        avg_competitor_subs = sum(competitor_subs) / len(competitor_subs) if competitor_subs else 0
        avg_competitor_views = sum(competitor_views) / len(competitor_views) if competitor_views else 0
        avg_competitor_videos = sum(competitor_videos) / len(competitor_videos) if competitor_videos else 0
        
        # Calculate performance ratios
        sub_ratio = (channel_subs / avg_competitor_subs * 100) if avg_competitor_subs > 0 else 0
        views_ratio = (channel_views / avg_competitor_views * 100) if avg_competitor_views > 0 else 0
        videos_ratio = (channel_videos / avg_competitor_videos * 100) if avg_competitor_videos > 0 else 0
        
        return {
            "competitors_analyzed": len(competitors),
            "subscriber_comparison": {
                "your_subscribers": channel_subs,
                "average_competitor_subscribers": avg_competitor_subs,
                "percentage_of_average": sub_ratio
            },
            "views_comparison": {
                "your_views": channel_views,
                "average_competitor_views": avg_competitor_views,
                "percentage_of_average": views_ratio
            },
            "content_volume_comparison": {
                "your_videos": channel_videos,
                "average_competitor_videos": avg_competitor_videos,
                "percentage_of_average": videos_ratio
            },
            "insights": self._generate_competitor_insights(
                sub_ratio, views_ratio, videos_ratio
            )
        }
    
    def _generate_competitor_insights(
        self,
        sub_ratio: float,
        views_ratio: float,
        videos_ratio: float
    ) -> List[str]:
        """Generate insights from competitor comparison."""
        insights = []
        
        if sub_ratio < 50:
            insights.append("Subscriber count is below average. Focus on subscriber growth strategies.")
        elif sub_ratio > 150:
            insights.append("Subscriber count is above average. Great job!")
        
        if views_ratio < 50:
            insights.append("Total views are below average. Improve SEO and content quality.")
        elif views_ratio > 150:
            insights.append("Total views are above average. Your content is performing well!")
        
        if videos_ratio < 50:
            insights.append("You have fewer videos than competitors. Consider increasing upload frequency.")
        elif videos_ratio > 150:
            insights.append("You have more videos than competitors. Focus on quality over quantity.")
        
        if not insights:
            insights.append("Your channel performance is on par with competitors. Keep up the good work!")
        
        return insights
    
    def _calculate_score_distribution(self, scores: List[float]) -> Dict[str, int]:
        """Calculate SEO score distribution."""
        if not scores:
            return {}
        
        distribution = {
            "excellent_90_100": sum(1 for s in scores if s >= 90),
            "good_70_89": sum(1 for s in scores if 70 <= s < 90),
            "fair_50_69": sum(1 for s in scores if 50 <= s < 70),
            "poor_below_50": sum(1 for s in scores if s < 50)
        }
        
        return distribution
    
    def _generate_action_items(
        self,
        channel_analysis: Dict[str, Any],
        seo_audits: List[Dict[str, Any]],
        content_gaps: List[Dict[str, Any]],
        optimization_opportunities: List[Dict[str, Any]],
        competitor_comparison: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate prioritized action items."""
        action_items = []
        
        # High priority items
        high_priority_gaps = [g for g in content_gaps if g.get("priority") == "high"]
        high_priority_opps = [o for o in optimization_opportunities if o.get("priority") == "high"]
        
        for gap in high_priority_gaps:
            action_items.append({
                "priority": "high",
                "category": "content",
                "action": gap.get("description", ""),
                "estimated_impact": "high"
            })
        
        for opp in high_priority_opps:
            action_items.append({
                "priority": "high",
                "category": "optimization",
                "action": opp.get("description", ""),
                "estimated_impact": "high"
            })
        
        # Medium priority items
        medium_priority_opps = [o for o in optimization_opportunities if o.get("priority") == "medium"]
        for opp in medium_priority_opps:
            action_items.append({
                "priority": "medium",
                "category": "optimization",
                "action": opp.get("description", ""),
                "estimated_impact": "medium"
            })
        
        # Competitor insights
        if competitor_comparison:
            insights = competitor_comparison.get("insights", [])
            for insight in insights[:2]:  # Top 2 insights
                action_items.append({
                    "priority": "medium",
                    "category": "competitive",
                    "action": insight,
                    "estimated_impact": "medium"
                })
        
        return action_items
    
    def _calculate_health_score(
        self,
        channel_analysis: Dict[str, Any],
        avg_seo_score: float,
        seo_audits: List[Dict[str, Any]],
        optimization_opportunities: List[Dict[str, Any]]
    ) -> float:
        """Calculate overall channel health score (0-100)."""
        score = 0
        
        # SEO score component (40%)
        score += (avg_seo_score / 100) * 40
        
        # Engagement component (20%)
        engagement_analysis = channel_analysis.get("engagement_analysis", {})
        avg_engagement = engagement_analysis.get("average_engagement_rate", 0)
        engagement_score = min(100, (avg_engagement / 5.0) * 100)  # 5% engagement = 100
        score += (engagement_score / 100) * 20
        
        # Growth component (20%)
        growth_analysis = channel_analysis.get("growth_analysis", {})
        avg_days_between = growth_analysis.get("average_days_between_videos", 0)
        if avg_days_between > 0:
            consistency_score = max(0, 100 - (avg_days_between / 30) * 100)  # 30 days = 0, 0 days = 100
            score += (consistency_score / 100) * 20
        
        # Optimization opportunities component (20%)
        # Fewer opportunities = higher score
        opp_count = len(optimization_opportunities)
        opp_score = max(0, 100 - (opp_count * 10))  # Each opportunity reduces score by 10
        score += (opp_score / 100) * 20
        
        return min(100, max(0, score))
    
    def export_report(
        self,
        audit_result: Dict[str, Any],
        format: str = "html"
    ) -> str:
        """
        Export audit report to HTML or JSON.
        
        Args:
            audit_result: Audit result from perform_audit
            format: Export format (html or json)
        
        Returns:
            Exported report content
        """
        if format == "json":
            import json
            return json.dumps(audit_result, indent=2, ensure_ascii=False)
        
        elif format == "html":
            # Generate HTML report
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Channel Audit Report - {audit_result.get('channel_info', {}).get('title', 'Channel')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #555; border-bottom: 2px solid #ddd; padding-bottom: 10px; }}
        .score {{ font-size: 48px; font-weight: bold; color: #4CAF50; }}
        .metric {{ margin: 15px 0; padding: 10px; background: #f9f9f9; border-radius: 4px; }}
        .action-item {{ margin: 10px 0; padding: 15px; border-left: 4px solid #2196F3; background: #e3f2fd; }}
        .high-priority {{ border-left-color: #f44336; background: #ffebee; }}
        .medium-priority {{ border-left-color: #ff9800; background: #fff3e0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Channel Audit Report</h1>
        <p><strong>Date:</strong> {audit_result.get('audit_date', 'N/A')}</p>
        <p><strong>Channel:</strong> {audit_result.get('channel_info', {}).get('title', 'N/A')}</p>
        
        <h2>Overall Health Score</h2>
        <div class="score">{audit_result.get('overall_health_score', 0):.1f}/100</div>
        
        <h2>Channel Statistics</h2>
        <div class="metric">
            <strong>Subscribers:</strong> {audit_result.get('channel_statistics', {}).get('subscribers', 0):,}<br>
            <strong>Total Views:</strong> {audit_result.get('channel_statistics', {}).get('total_views', 0):,}<br>
            <strong>Total Videos:</strong> {audit_result.get('channel_statistics', {}).get('total_videos', 0)}
        </div>
        
        <h2>SEO Health</h2>
        <div class="metric">
            <strong>Average SEO Score:</strong> {audit_result.get('seo_health', {}).get('average_seo_score', 0):.1f}/100<br>
            <strong>Videos Audited:</strong> {audit_result.get('seo_health', {}).get('videos_audited', 0)}
        </div>
        
        <h2>Action Items</h2>
        {"".join([
            f'<div class="action-item {"high-priority" if item.get("priority") == "high" else "medium-priority"}">'
            f'<strong>{item.get("category", "").upper()}</strong>: {item.get("action", "")}'
            f'</div>'
            for item in audit_result.get('action_items', [])
        ])}
        
        <h2>Recommendations</h2>
        <ul>
            {"".join([f'<li>{rec}</li>' for rec in audit_result.get('recommendations', [])])}
        </ul>
    </div>
</body>
</html>
            """
            return html
        
        else:
            raise ValueError(f"Unsupported format: {format}")

