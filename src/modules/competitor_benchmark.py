"""
Competitor Benchmarking & Learning Module
Analyzes successful channels (1M+ subscribers) and learns from their strategies.

AGI Paradigm: Competitor Benchmarking & Learning
- Analyzes 1M+ subscriber channels
- Learns successful strategies
- Identifies differentiation opportunities
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.channel_analyzer import ChannelAnalyzer
from src.modules.competitor_analyzer import CompetitorAnalyzer


class CompetitorBenchmark:
    """
    Benchmarks against successful channels and learns from them.
    
    AGI Paradigm: Competitor Benchmarking & Learning
    - Analyzes 10K+ subscriber channels in similar niches
    - Learns what makes them successful
    - Provides actionable insights for growth
    """
    
    DATA_FILE = "data/competitor_benchmarks.json"
    MIN_SUBSCRIBERS_FOR_BENCHMARK = 10000  # 10K subscribers (lowered for more benchmarking opportunities)
    
    def __init__(
        self,
        client: YouTubeClient,
        channel_analyzer: ChannelAnalyzer,
        competitor_analyzer: CompetitorAnalyzer
    ):
        self.client = client
        self.channel_analyzer = channel_analyzer
        self.competitor_analyzer = competitor_analyzer
        self._ensure_data_dir()
        self._load_benchmarks()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
    
    def _load_benchmarks(self) -> Dict[str, Any]:
        """Load benchmark data."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "benchmarked_channels": [],
            "learned_strategies": {},
            "differentiation_opportunities": [],
            "best_practices": []
        }
    
    def _save_benchmarks(self, data: Dict[str, Any]):
        """Save benchmark data."""
        try:
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving benchmarks: {e}")
    
    def benchmark_channel(
        self,
        channel_handle: Optional[str] = None,
        channel_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Benchmark a successful channel.
        
        Args:
            channel_handle: Channel handle (e.g., @channelname)
            channel_id: Channel ID
            
        Returns:
            Benchmark analysis
        """
        try:
            # Get channel data
            if channel_handle:
                channel_data = self.client.get_channel_by_handle(channel_handle)
            elif channel_id:
                channel_data = self.client.get_channel_by_id(channel_id)
            else:
                return {"error": "Either channel_handle or channel_id required"}
            
            if not channel_data.get("items"):
                return {"error": "Channel not found"}
            
            channel = channel_data["items"][0]
            stats = channel["statistics"]
            snippet = channel["snippet"]
            subscribers = int(stats.get("subscriberCount", 0))
            
            # Check if channel meets benchmark criteria
            if subscribers < self.MIN_SUBSCRIBERS_FOR_BENCHMARK:
                return {
                    "status": "below_threshold",
                    "message": f"Channel has {subscribers:,} subscribers. Minimum for benchmark: {self.MIN_SUBSCRIBERS_FOR_BENCHMARK:,}",
                    "subscribers": subscribers
                }
            
            channel_id = channel["id"]
            
            # Get channel videos for analysis
            videos = self.client.get_channel_videos(channel_id, max_results=20)
            
            # Analyze channel
            analysis = self.channel_analyzer.analyze_channel(
                snippet.get("customUrl", "").replace("@", "") or channel_id
            )
            
            # Extract key metrics
            benchmark_data = {
                "channel_id": channel_id,
                "channel_handle": snippet.get("customUrl", ""),
                "channel_name": snippet["title"],
                "subscribers": subscribers,
                "total_views": int(stats.get("viewCount", 0)),
                "total_videos": int(stats.get("videoCount", 0)),
                "average_views_per_video": int(stats.get("viewCount", 0)) / max(int(stats.get("videoCount", 1)), 1),
                "created_at": snippet.get("publishedAt", ""),
                "country": snippet.get("country", "Unknown"),
                "description": snippet.get("description", ""),
                "benchmarked_at": datetime.now().isoformat()
            }
            
            # Analyze content strategy
            content_strategy = self._analyze_content_strategy(videos, analysis)
            benchmark_data["content_strategy"] = content_strategy
            
            # Analyze growth patterns
            growth_patterns = self._analyze_growth_patterns(analysis, videos)
            benchmark_data["growth_patterns"] = growth_patterns
            
            # Extract best practices
            best_practices = self._extract_best_practices(analysis, videos, content_strategy)
            benchmark_data["best_practices"] = best_practices
            
            # Save benchmark
            benchmarks = self._load_benchmarks()
            benchmarks["benchmarked_channels"].append(benchmark_data)
            
            # Keep only last 20 benchmarks
            if len(benchmarks["benchmarked_channels"]) > 20:
                benchmarks["benchmarked_channels"] = benchmarks["benchmarked_channels"][-20:]
            
            self._save_benchmarks(benchmarks)
            
            return {
                "status": "success",
                "benchmark": benchmark_data,
                "insights": self._generate_benchmark_insights(benchmark_data)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_content_strategy(
        self,
        videos: List[Dict[str, Any]],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze content strategy of benchmarked channel."""
        if not videos:
            return {}
        
        # Analyze titles
        titles = [v["snippet"]["title"] for v in videos]
        avg_title_length = sum(len(t) for t in titles) / len(titles)
        
        # Analyze upload frequency
        published_dates = [
            datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
            for v in videos if v["snippet"].get("publishedAt")
        ]
        published_dates.sort()
        
        upload_frequency = None
        if len(published_dates) > 1:
            time_diffs = [
                (published_dates[i+1] - published_dates[i]).days
                for i in range(len(published_dates)-1)
            ]
            upload_frequency = sum(time_diffs) / len(time_diffs) if time_diffs else None
        
        # Analyze video performance
        views = [int(v.get("statistics", {}).get("viewCount", 0)) for v in videos]
        avg_views = sum(views) / len(views) if views else 0
        
        # Analyze engagement
        total_likes = sum(int(v.get("statistics", {}).get("likeCount", 0)) for v in videos)
        total_comments = sum(int(v.get("statistics", {}).get("commentCount", 0)) for v in videos)
        total_views = sum(views)
        engagement_rate = ((total_likes + total_comments) / max(total_views, 1)) * 100
        
        return {
            "average_title_length": avg_title_length,
            "upload_frequency_days": upload_frequency,
            "average_views": avg_views,
            "engagement_rate": engagement_rate,
            "content_themes": self._extract_content_themes(titles),
            "video_count_analyzed": len(videos)
        }
    
    def _extract_content_themes(self, titles: List[str]) -> List[str]:
        """Extract common themes from titles."""
        # Simple keyword extraction
        all_words = []
        for title in titles:
            words = title.lower().split()
            all_words.extend([w for w in words if len(w) > 3])
        
        # Count word frequency
        from collections import Counter
        word_counts = Counter(all_words)
        
        # Return top themes
        return [word for word, count in word_counts.most_common(10)]
    
    def _analyze_growth_patterns(
        self,
        analysis: Dict[str, Any],
        videos: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze growth patterns."""
        stats = analysis.get("statistics", {})
        subscribers = stats.get("subscribers", 0)
        total_views = stats.get("total_views", 0)
        
        # Calculate conversion rate
        conversion_rate = (subscribers / max(total_views, 1)) * 100
        
        # Calculate views per subscriber
        views_per_subscriber = total_views / max(subscribers, 1)
        
        # Analyze video performance distribution
        if videos:
            views = [int(v.get("statistics", {}).get("viewCount", 0)) for v in videos]
            if views:
                views.sort()
                median_views = views[len(views)//2]
                top_10_percent = views[int(len(views)*0.9):] if len(views) > 10 else views[-1:]
                avg_top_10 = sum(top_10_percent) / len(top_10_percent) if top_10_percent else 0
            else:
                median_views = 0
                avg_top_10 = 0
        else:
            median_views = 0
            avg_top_10 = 0
        
        return {
            "conversion_rate": conversion_rate,
            "views_per_subscriber": views_per_subscriber,
            "median_video_views": median_views,
            "top_10_percent_avg_views": avg_top_10,
            "growth_indicators": {
                "high_engagement": analysis.get("engagement_analysis", {}).get("average_engagement_rate", 0) > 3.0,
                "consistent_uploads": True,  # Would need historical data for accurate check
                "viral_content": avg_top_10 > median_views * 5 if median_views > 0 else False
            }
        }
    
    def _extract_best_practices(
        self,
        analysis: Dict[str, Any],
        videos: List[Dict[str, Any]],
        content_strategy: Dict[str, Any]
    ) -> List[str]:
        """Extract best practices from benchmarked channel."""
        practices = []
        
        # Title optimization
        avg_title_len = content_strategy.get("average_title_length", 0)
        if 40 <= avg_title_len <= 60:
            practices.append(f"Optimal title length: {avg_title_len:.0f} characters")
        
        # Upload frequency
        upload_freq = content_strategy.get("upload_frequency_days")
        if upload_freq and upload_freq <= 7:
            practices.append(f"Consistent uploads: ~{upload_freq:.1f} days between videos")
        
        # Engagement
        engagement = content_strategy.get("engagement_rate", 0)
        if engagement > 3.0:
            practices.append(f"High engagement rate: {engagement:.2f}%")
        
        # Video performance
        avg_views = content_strategy.get("average_views", 0)
        if avg_views > 100000:
            practices.append(f"Strong average views: {avg_views:,.0f} per video")
        
        # Content themes
        themes = content_strategy.get("content_themes", [])
        if themes:
            practices.append(f"Focus on themes: {', '.join(themes[:5])}")
        
        return practices
    
    def _generate_benchmark_insights(self, benchmark_data: Dict[str, Any]) -> List[str]:
        """Generate insights from benchmark data."""
        insights = []
        
        subscribers = benchmark_data.get("subscribers", 0)
        avg_views = benchmark_data.get("average_views_per_video", 0)
        content_strategy = benchmark_data.get("content_strategy", {})
        
        insights.append(f"Channel has {subscribers:,} subscribers - excellent benchmark target")
        
        if avg_views > 100000:
            insights.append(f"Strong average views: {avg_views:,.0f} per video")
        
        upload_freq = content_strategy.get("upload_frequency_days")
        if upload_freq and upload_freq <= 7:
            insights.append(f"Consistent upload schedule: ~{upload_freq:.1f} days between videos")
        
        engagement = content_strategy.get("engagement_rate", 0)
        if engagement > 3.0:
            insights.append(f"High engagement rate: {engagement:.2f}% - focus on community building")
        
        return insights
    
    def find_differentiation_opportunities(
        self,
        target_channel_handle: str,
        benchmarked_channels: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Find opportunities to differentiate from successful competitors.
        
        Args:
            target_channel_handle: Your channel handle
            benchmarked_channels: List of benchmarked channels (optional)
            
        Returns:
            Differentiation opportunities
        """
        # Get target channel analysis
        try:
            target_analysis = self.channel_analyzer.analyze_channel(target_channel_handle)
        except Exception:
            return {"error": "Could not analyze target channel"}
        
        # Get benchmarked channels
        if not benchmarked_channels:
            benchmarks = self._load_benchmarks()
            benchmarked_channels = benchmarks.get("benchmarked_channels", [])
        
        if not benchmarked_channels:
            return {
                "status": "no_benchmarks",
                "message": "No benchmarked channels available. Benchmark some successful channels first."
            }
        
        opportunities = []
        
        # Compare content strategy
        target_content = target_analysis.get("content_analysis", {})
        target_title_len = target_content.get("average_title_length", 0)
        
        for benchmark in benchmarked_channels:
            bench_content = benchmark.get("content_strategy", {})
            bench_title_len = bench_content.get("average_title_length", 0)
            
            # Title length opportunity
            if 40 <= bench_title_len <= 60 and not (40 <= target_title_len <= 60):
                opportunities.append({
                    "type": "title_optimization",
                    "opportunity": f"Optimize title length to {bench_title_len:.0f} characters (current: {target_title_len:.0f})",
                    "benchmark": benchmark.get("channel_name"),
                    "priority": "high"
                })
            
            # Upload frequency opportunity
            bench_freq = bench_content.get("upload_frequency_days")
            target_freq = target_analysis.get("growth_analysis", {}).get("average_days_between_videos", 0)
            
            if bench_freq and target_freq > bench_freq * 1.5:
                opportunities.append({
                    "type": "upload_frequency",
                    "opportunity": f"Increase upload frequency (benchmark: {bench_freq:.1f} days, yours: {target_freq:.1f} days)",
                    "benchmark": benchmark.get("channel_name"),
                    "priority": "high"
                })
            
            # Engagement opportunity
            bench_engagement = bench_content.get("engagement_rate", 0)
            target_engagement = target_analysis.get("engagement_analysis", {}).get("average_engagement_rate", 0)
            
            if bench_engagement > target_engagement * 1.5:
                opportunities.append({
                    "type": "engagement",
                    "opportunity": f"Improve engagement rate (benchmark: {bench_engagement:.2f}%, yours: {target_engagement:.2f}%)",
                    "benchmark": benchmark.get("channel_name"),
                    "priority": "medium"
                })
        
        # Remove duplicates and sort by priority
        unique_opportunities = {}
        for opp in opportunities:
            key = f"{opp['type']}_{opp['opportunity']}"
            if key not in unique_opportunities or opp['priority'] == 'high':
                unique_opportunities[key] = opp
        
        sorted_opportunities = sorted(
            unique_opportunities.values(),
            key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 2)
        )
        
        return {
            "total_opportunities": len(sorted_opportunities),
            "high_priority": [o for o in sorted_opportunities if o.get("priority") == "high"],
            "medium_priority": [o for o in sorted_opportunities if o.get("priority") == "medium"],
            "all_opportunities": sorted_opportunities
        }
    
    def get_learned_strategies(self) -> Dict[str, Any]:
        """Get learned strategies from all benchmarked channels."""
        benchmarks = self._load_benchmarks()
        channels = benchmarks.get("benchmarked_channels", [])
        
        if not channels:
            return {
                "status": "no_data",
                "message": "No benchmarked channels yet"
            }
        
        # Aggregate strategies
        strategies = {
            "title_lengths": [],
            "upload_frequencies": [],
            "engagement_rates": [],
            "content_themes": [],
            "best_practices": []
        }
        
        for channel in channels:
            content = channel.get("content_strategy", {})
            
            if content.get("average_title_length"):
                strategies["title_lengths"].append(content["average_title_length"])
            
            if content.get("upload_frequency_days"):
                strategies["upload_frequencies"].append(content["upload_frequency_days"])
            
            if content.get("engagement_rate"):
                strategies["engagement_rates"].append(content["engagement_rate"])
            
            if content.get("content_themes"):
                strategies["content_themes"].extend(content["content_themes"])
            
            if channel.get("best_practices"):
                strategies["best_practices"].extend(channel["best_practices"])
        
        # Calculate averages and most common
        from collections import Counter
        
        learned = {
            "average_title_length": sum(strategies["title_lengths"]) / len(strategies["title_lengths"]) if strategies["title_lengths"] else None,
            "average_upload_frequency": sum(strategies["upload_frequencies"]) / len(strategies["upload_frequencies"]) if strategies["upload_frequencies"] else None,
            "average_engagement_rate": sum(strategies["engagement_rates"]) / len(strategies["engagement_rates"]) if strategies["engagement_rates"] else None,
            "most_common_themes": [theme for theme, count in Counter(strategies["content_themes"]).most_common(10)],
            "common_best_practices": [practice for practice, count in Counter(strategies["best_practices"]).most_common(10)],
            "channels_analyzed": len(channels)
        }
        
        return {
            "learned_strategies": learned,
            "recommendations": self._generate_strategy_recommendations(learned)
        }
    
    def _generate_strategy_recommendations(self, learned: Dict[str, Any]) -> List[str]:
        """Generate recommendations from learned strategies."""
        recommendations = []
        
        avg_title_len = learned.get("average_title_length")
        if avg_title_len:
            recommendations.append(f"Aim for title length around {avg_title_len:.0f} characters")
        
        avg_freq = learned.get("average_upload_frequency")
        if avg_freq:
            recommendations.append(f"Upload every {avg_freq:.1f} days for optimal growth")
        
        avg_engagement = learned.get("average_engagement_rate")
        if avg_engagement:
            recommendations.append(f"Target engagement rate of {avg_engagement:.2f}% or higher")
        
        themes = learned.get("most_common_themes", [])
        if themes:
            recommendations.append(f"Consider focusing on themes: {', '.join(themes[:5])}")
        
        return recommendations

