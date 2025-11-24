"""
Knowledge Graph & Contradiction Resolution Module
Creates unified knowledge graph from all data sources and resolves contradictions.

AGI Paradigm: Quantum Knowledge Synthesis
- Non-linear entangled states: All data interconnected
- Superposition memory: Dynamic knowledge graph
- Wave-function collapse: Precise recommendations from multi-dimensional data
"""

from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient
from src.modules.performance_tracker import PerformanceTracker
from src.modules.feedback_learner import FeedbackLearner
from src.modules.multi_source_integrator import MultiSourceIntegrator
from src.modules.competitor_benchmark import CompetitorBenchmark


class KnowledgeGraph:
    """
    Unified knowledge graph that integrates all data sources.
    
    AGI Paradigm: Quantum Knowledge Synthesis
    - Integrates video performance, trends, competitor strategies
    - Resolves contradictory recommendations
    - Identifies patterns for subscriber growth
    - Creates unified, contradiction-resolved knowledge base
    """
    
    DATA_FILE = "data/knowledge_graph.json"
    
    def __init__(
        self,
        client: YouTubeClient,
        performance_tracker: PerformanceTracker,
        feedback_learner: FeedbackLearner,
        multi_source_integrator: MultiSourceIntegrator,
        competitor_benchmark: CompetitorBenchmark
    ):
        self.client = client
        self.performance_tracker = performance_tracker
        self.feedback_learner = feedback_learner
        self.multi_source_integrator = multi_source_integrator
        self.competitor_benchmark = competitor_benchmark
        self._ensure_data_dir()
        self._load_graph()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
    
    def _load_graph(self) -> Dict[str, Any]:
        """Load knowledge graph from file."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "nodes": {},
            "edges": [],
            "patterns": {},
            "contradictions": [],
            "resolved_contradictions": [],
            "last_updated": None
        }
    
    def _save_graph(self, graph: Dict[str, Any]):
        """Save knowledge graph to file."""
        try:
            graph["last_updated"] = datetime.now().isoformat()
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(graph, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving knowledge graph: {e}")
    
    def build_graph(self, channel_handle: str) -> Dict[str, Any]:
        """
        Build unified knowledge graph from all data sources.
        
        Args:
            channel_handle: Channel to build graph for
            
        Returns:
            Knowledge graph structure
        """
        graph = self._load_graph()
        
        # Initialize graph structure
        nodes = graph.get("nodes", {})
        edges = graph.get("edges", [])
        
        # 1. Add video performance nodes
        try:
            videos = self.client.get_channel_videos(
                self.client.get_channel_by_handle(channel_handle)["items"][0]["id"],
                max_results=20
            )
            for video in videos:
                video_id = video["id"]
                stats = video.get("statistics", {})
                snippet = video["snippet"]
                
                nodes[f"video_{video_id}"] = {
                    "type": "video",
                    "id": video_id,
                    "title": snippet["title"],
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "published_at": snippet.get("publishedAt", ""),
                    "tags": snippet.get("tags", []),
                    "description": snippet.get("description", "")[:200]
                }
        except Exception as e:
            print(f"Error adding videos: {e}")
        
        # 2. Add recommendation nodes
        try:
            perf_history = self.performance_tracker._load_history()
            recommendations = perf_history.get("recommendations", {})
            
            for rec_id, rec_data in recommendations.items():
                nodes[f"recommendation_{rec_id}"] = {
                    "type": "recommendation",
                    "id": rec_id,
                    "rec_type": rec_data.get("type"),
                    "data": rec_data.get("data"),
                    "status": rec_data.get("status"),
                    "video_id": rec_data.get("video_id"),
                    "created_at": rec_data.get("created_at")
                }
                
                # Add edge from recommendation to video
                if rec_data.get("video_id"):
                    edges.append({
                        "from": f"recommendation_{rec_id}",
                        "to": f"video_{rec_data['video_id']}",
                        "type": "applies_to",
                        "weight": 1.0
                    })
        except Exception as e:
            print(f"Error adding recommendations: {e}")
        
        # 3. Add trend nodes
        try:
            multi_source_data = self.multi_source_integrator._load_data()
            opportunities = multi_source_data.get("synthesized_opportunities", [])
            
            for opp in opportunities[-5:]:  # Last 5 opportunities
                opp_id = f"trend_{datetime.now().timestamp()}"
                nodes[opp_id] = {
                    "type": "trend",
                    "id": opp_id,
                    "keywords": opp.get("keywords", []),
                    "viral_opportunities": opp.get("viral_opportunities", []),
                    "timestamp": opp.get("timestamp")
                }
        except Exception as e:
            print(f"Error adding trends: {e}")
        
        # 4. Add competitor strategy nodes
        try:
            benchmark_data = self.competitor_benchmark._load_benchmarks()
            benchmarked = benchmark_data.get("benchmarked_channels", [])
            
            for bench in benchmarked[-5:]:  # Last 5 benchmarks
                bench_id = f"competitor_{bench.get('channel_id', 'unknown')}"
                nodes[bench_id] = {
                    "type": "competitor",
                    "id": bench_id,
                    "channel_name": bench.get("channel_name"),
                    "subscribers": bench.get("subscribers", 0),
                    "strategy": bench.get("content_strategy", {}),
                    "best_practices": bench.get("best_practices", [])
                }
        except Exception as e:
            print(f"Error adding competitors: {e}")
        
        # 5. Add pattern nodes
        patterns = self._extract_patterns(nodes, edges)
        for pattern_id, pattern_data in patterns.items():
            nodes[pattern_id] = pattern_data
        
        # Update graph
        graph["nodes"] = nodes
        graph["edges"] = edges
        graph["patterns"] = patterns
        
        self._save_graph(graph)
        
        return {
            "nodes_count": len(nodes),
            "edges_count": len(edges),
            "patterns_count": len(patterns),
            "graph": graph
        }
    
    def _extract_patterns(
        self,
        nodes: Dict[str, Any],
        edges: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract patterns from knowledge graph."""
        patterns = {}
        
        # Pattern 1: Successful title patterns
        successful_videos = [
            n for n in nodes.values()
            if n.get("type") == "video" and n.get("views", 0) > 1000
        ]
        
        if successful_videos:
            title_lengths = [len(v.get("title", "")) for v in successful_videos]
            avg_title_length = sum(title_lengths) / len(title_lengths) if title_lengths else 0
            
            patterns["pattern_title_length"] = {
                "type": "pattern",
                "id": "pattern_title_length",
                "pattern_type": "title_length",
                "value": avg_title_length,
                "confidence": 0.8,
                "description": f"Successful videos have average title length of {avg_title_length:.0f} characters"
            }
        
        # Pattern 2: Recommendation success patterns
        successful_recommendations = [
            n for n in nodes.values()
            if n.get("type") == "recommendation" and n.get("status") == "success"
        ]
        
        if successful_recommendations:
            rec_types = [r.get("rec_type") for r in successful_recommendations]
            from collections import Counter
            type_counts = Counter(rec_types)
            most_common = type_counts.most_common(1)[0] if type_counts else None
            
            if most_common:
                patterns["pattern_successful_rec_type"] = {
                    "type": "pattern",
                    "id": "pattern_successful_rec_type",
                    "pattern_type": "recommendation_type",
                    "value": most_common[0],
                    "confidence": most_common[1] / len(successful_recommendations),
                    "description": f"Most successful recommendation type: {most_common[0]}"
                }
        
        # Pattern 3: Timing patterns
        videos_with_timing = [
            n for n in nodes.values()
            if n.get("type") == "video" and n.get("published_at")
        ]
        
        if videos_with_timing:
            # Extract hour from published_at
            hours = []
            for v in videos_with_timing:
                try:
                    pub_time = datetime.fromisoformat(v["published_at"].replace("Z", "+00:00"))
                    hours.append(pub_time.hour)
                except:
                    pass
            
            if hours:
                from collections import Counter
                hour_counts = Counter(hours)
                best_hour = hour_counts.most_common(1)[0][0] if hour_counts else None
                
                if best_hour:
                    patterns["pattern_best_posting_hour"] = {
                        "type": "pattern",
                        "id": "pattern_best_posting_hour",
                        "pattern_type": "posting_time",
                        "value": best_hour,
                        "confidence": hour_counts[best_hour] / len(hours),
                        "description": f"Best posting hour: {best_hour}:00"
                    }
        
        return patterns
    
    def detect_contradictions(self) -> Dict[str, Any]:
        """
        Detect contradictory recommendations and patterns.
        
        Returns:
            List of detected contradictions
        """
        graph = self._load_graph()
        nodes = graph.get("nodes", {})
        patterns = graph.get("patterns", {})
        contradictions = []
        
        # Check for contradictory patterns
        title_pattern = patterns.get("pattern_title_length")
        if title_pattern:
            title_length = title_pattern.get("value", 0)
            
            # Check if recommendations contradict this pattern
            recommendations = [
                n for n in nodes.values()
                if n.get("type") == "recommendation" and n.get("rec_type") == "title"
            ]
            
            for rec in recommendations:
                rec_data = rec.get("data", {})
                if isinstance(rec_data, dict):
                    rec_title = rec_data.get("title", "")
                    rec_length = len(rec_title) if rec_title else 0
                    
                    # Contradiction if title length differs significantly
                    if abs(rec_length - title_length) > 20:
                        contradictions.append({
                            "type": "title_length_contradiction",
                            "pattern": f"Optimal title length: {title_length:.0f}",
                            "recommendation": f"Recommended title length: {rec_length}",
                            "severity": "medium",
                            "recommendation_id": rec.get("id"),
                            "pattern_id": "pattern_title_length"
                        })
        
        # Check for contradictory recommendation types
        successful_rec_type = patterns.get("pattern_successful_rec_type")
        if successful_rec_type:
            best_type = successful_rec_type.get("value")
            
            # Check if other types are being recommended more
            all_recommendations = [
                n for n in nodes.values()
                if n.get("type") == "recommendation"
            ]
            
            type_counts = defaultdict(int)
            for rec in all_recommendations:
                type_counts[rec.get("rec_type")] += 1
            
            if type_counts and best_type:
                most_recommended = max(type_counts.items(), key=lambda x: x[1])
                if most_recommended[0] != best_type:
                    contradictions.append({
                        "type": "recommendation_type_contradiction",
                        "pattern": f"Most successful type: {best_type}",
                        "reality": f"Most recommended type: {most_recommended[0]}",
                        "severity": "high",
                        "pattern_id": "pattern_successful_rec_type"
                    })
        
        # Update graph
        graph["contradictions"] = contradictions
        self._save_graph(graph)
        
        return {
            "contradictions_count": len(contradictions),
            "contradictions": contradictions,
            "severity_breakdown": self._analyze_severity(contradictions)
        }
    
    def _analyze_severity(self, contradictions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze contradiction severity."""
        severity_counts = defaultdict(int)
        for contr in contradictions:
            severity_counts[contr.get("severity", "unknown")] += 1
        return dict(severity_counts)
    
    def resolve_contradictions(self) -> Dict[str, Any]:
        """
        Resolve detected contradictions using evidence-based approach.
        
        Returns:
            Resolution results
        """
        graph = self._load_graph()
        contradictions = graph.get("contradictions", [])
        resolved = []
        
        for contr in contradictions:
            resolution = self._resolve_single_contradiction(contr, graph)
            if resolution:
                resolved.append({
                    "contradiction": contr,
                    "resolution": resolution,
                    "resolved_at": datetime.now().isoformat()
                })
        
        # Update graph
        graph["resolved_contradictions"].extend(resolved)
        graph["contradictions"] = []  # Clear resolved contradictions
        self._save_graph(graph)
        
        return {
            "resolved_count": len(resolved),
            "resolutions": resolved
        }
    
    def _resolve_single_contradiction(
        self,
        contradiction: Dict[str, Any],
        graph: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Resolve a single contradiction."""
        contr_type = contradiction.get("type")
        
        if contr_type == "title_length_contradiction":
            # Resolve by using pattern (more reliable)
            return {
                "action": "use_pattern",
                "reason": "Pattern based on successful videos is more reliable",
                "recommendation": "Follow the pattern: optimal title length"
            }
        
        elif contr_type == "recommendation_type_contradiction":
            # Resolve by prioritizing successful type
            return {
                "action": "prioritize_successful_type",
                "reason": "Successful type has proven track record",
                "recommendation": "Focus recommendations on the most successful type"
            }
        
        return None
    
    def get_subscriber_growth_patterns(self) -> Dict[str, Any]:
        """
        Identify patterns that lead to subscriber growth.
        
        Returns:
            Patterns correlated with subscriber growth
        """
        graph = self._load_graph()
        nodes = graph.get("nodes", {})
        
        # Get video performance data
        videos = [
            n for n in nodes.values()
            if n.get("type") == "video"
        ]
        
        if not videos:
            return {
                "status": "insufficient_data",
                "message": "Need video data to analyze patterns"
            }
        
        # Analyze patterns
        patterns = {
            "title_patterns": self._analyze_title_patterns(videos),
            "timing_patterns": self._analyze_timing_patterns(videos),
            "content_patterns": self._analyze_content_patterns(videos),
            "recommendation_patterns": self._analyze_recommendation_patterns(nodes)
        }
        
        return {
            "patterns": patterns,
            "insights": self._generate_growth_insights(patterns)
        }
    
    def _analyze_title_patterns(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze title patterns from successful videos."""
        if not videos:
            return {}
        
        # Sort by views
        sorted_videos = sorted(videos, key=lambda v: v.get("views", 0), reverse=True)
        top_videos = sorted_videos[:5] if len(sorted_videos) >= 5 else sorted_videos
        
        title_lengths = [len(v.get("title", "")) for v in top_videos]
        avg_length = sum(title_lengths) / len(title_lengths) if title_lengths else 0
        
        # Extract common words
        all_titles = " ".join([v.get("title", "").lower() for v in top_videos])
        from collections import Counter
        words = [w for w in all_titles.split() if len(w) > 3]
        common_words = [word for word, count in Counter(words).most_common(5)]
        
        return {
            "average_length": avg_length,
            "optimal_range": f"{avg_length - 10:.0f}-{avg_length + 10:.0f}",
            "common_words": common_words,
            "top_videos_analyzed": len(top_videos)
        }
    
    def _analyze_timing_patterns(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze posting timing patterns."""
        videos_with_time = [
            v for v in videos
            if v.get("published_at")
        ]
        
        if not videos_with_time:
            return {}
        
        hours = []
        days_of_week = []
        
        for v in videos_with_time:
            try:
                pub_time = datetime.fromisoformat(v["published_at"].replace("Z", "+00:00"))
                hours.append(pub_time.hour)
                days_of_week.append(pub_time.weekday())
            except:
                pass
        
        if not hours:
            return {}
        
        from collections import Counter
        hour_counts = Counter(hours)
        day_counts = Counter(days_of_week)
        
        best_hour = hour_counts.most_common(1)[0][0] if hour_counts else None
        best_day = day_counts.most_common(1)[0][0] if day_counts else None
        
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        return {
            "best_hour": best_hour,
            "best_day": day_names[best_day] if best_day is not None else None,
            "hour_distribution": dict(hour_counts),
            "day_distribution": {day_names[k]: v for k, v in dict(day_counts).items()}
        }
    
    def _analyze_content_patterns(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content patterns."""
        if not videos:
            return {}
        
        # Analyze tags
        all_tags = []
        for v in videos:
            tags = v.get("tags", [])
            if isinstance(tags, list):
                all_tags.extend(tags)
        
        from collections import Counter
        tag_counts = Counter(all_tags)
        common_tags = [tag for tag, count in tag_counts.most_common(10)]
        
        # Analyze description length
        desc_lengths = [len(v.get("description", "")) for v in videos if v.get("description")]
        avg_desc_length = sum(desc_lengths) / len(desc_lengths) if desc_lengths else 0
        
        return {
            "common_tags": common_tags,
            "average_description_length": avg_desc_length,
            "tag_count_analysis": {
                "min": min([len(v.get("tags", [])) for v in videos]) if videos else 0,
                "max": max([len(v.get("tags", [])) for v in videos]) if videos else 0,
                "avg": sum([len(v.get("tags", [])) for v in videos]) / len(videos) if videos else 0
            }
        }
    
    def _analyze_recommendation_patterns(self, nodes: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze recommendation patterns."""
        recommendations = [
            n for n in nodes.values()
            if n.get("type") == "recommendation"
        ]
        
        if not recommendations:
            return {}
        
        # Group by type and status
        by_type = defaultdict(lambda: {"total": 0, "success": 0, "failure": 0})
        
        for rec in recommendations:
            rec_type = rec.get("rec_type", "unknown")
            status = rec.get("status", "pending")
            
            by_type[rec_type]["total"] += 1
            if status == "success":
                by_type[rec_type]["success"] += 1
            elif status == "failure":
                by_type[rec_type]["failure"] += 1
        
        # Calculate success rates
        success_rates = {}
        for rec_type, stats in by_type.items():
            if stats["total"] > 0:
                success_rates[rec_type] = {
                    "success_rate": (stats["success"] / stats["total"]) * 100,
                    "total": stats["total"],
                    "success": stats["success"],
                    "failure": stats["failure"]
                }
        
        return {
            "by_type": success_rates,
            "best_performing_type": max(
                success_rates.items(),
                key=lambda x: x[1].get("success_rate", 0)
            )[0] if success_rates else None
        }
    
    def _generate_growth_insights(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate insights from patterns."""
        insights = []
        
        title_patterns = patterns.get("title_patterns", {})
        if title_patterns.get("average_length"):
            insights.append(
                f"📝 Optimal title length: {title_patterns['average_length']:.0f} characters "
                f"({title_patterns.get('optimal_range', 'N/A')})"
            )
        
        timing_patterns = patterns.get("timing_patterns", {})
        if timing_patterns.get("best_hour") is not None:
            insights.append(
                f"⏰ Best posting time: {timing_patterns['best_hour']}:00"
            )
        if timing_patterns.get("best_day"):
            insights.append(
                f"📅 Best posting day: {timing_patterns['best_day']}"
            )
        
        content_patterns = patterns.get("content_patterns", {})
        if content_patterns.get("common_tags"):
            insights.append(
                f"🏷️ Most effective tags: {', '.join(content_patterns['common_tags'][:5])}"
            )
        
        rec_patterns = patterns.get("recommendation_patterns", {})
        best_type = rec_patterns.get("best_performing_type")
        if best_type:
            insights.append(
                f"✅ Best performing recommendation type: {best_type}"
            )
        
        return insights
    
    def query_graph(
        self,
        query_type: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query the knowledge graph.
        
        Args:
            query_type: Type of query (videos, recommendations, patterns, etc.)
            filters: Optional filters
            
        Returns:
            Query results
        """
        graph = self._load_graph()
        nodes = graph.get("nodes", {})
        
        if query_type == "videos":
            videos = [n for n in nodes.values() if n.get("type") == "video"]
            if filters:
                if filters.get("min_views"):
                    videos = [v for v in videos if v.get("views", 0) >= filters["min_views"]]
            return {"results": videos, "count": len(videos)}
        
        elif query_type == "recommendations":
            recommendations = [n for n in nodes.values() if n.get("type") == "recommendation"]
            if filters:
                if filters.get("status"):
                    recommendations = [r for r in recommendations if r.get("status") == filters["status"]]
            return {"results": recommendations, "count": len(recommendations)}
        
        elif query_type == "patterns":
            patterns = graph.get("patterns", {})
            return {"results": patterns, "count": len(patterns)}
        
        elif query_type == "contradictions":
            contradictions = graph.get("contradictions", [])
            return {"results": contradictions, "count": len(contradictions)}
        
        return {"error": f"Unknown query type: {query_type}"}

