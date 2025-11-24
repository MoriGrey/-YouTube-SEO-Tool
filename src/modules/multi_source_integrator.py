"""
Multi-Source Data Integration Module
Integrates data from multiple sources: Google Trends, Reddit, Twitter, etc.

AGI Paradigm: Omnipresent Data Mining
- Integrates data from multiple open sources
- Synthesizes trends from different platforms
- Identifies viral content opportunities
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sys
import requests
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.youtube_client import YouTubeClient


class MultiSourceIntegrator:
    """
    Integrates data from multiple sources for comprehensive trend analysis.
    
    AGI Paradigm: Omnipresent Data Mining
    - Google Trends
    - Reddit
    - Twitter/X
    - YouTube Analytics
    - Synthesizes all data for viral opportunities
    """
    
    DATA_FILE = "data/multi_source_data.json"
    CACHE_DIR = ".cache/multi_source"
    
    def __init__(self, client: YouTubeClient):
        self.client = client
        self._ensure_data_dir()
        self._load_data()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
        os.makedirs(self.CACHE_DIR, exist_ok=True)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load multi-source data."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "trends_data": {},
            "reddit_data": {},
            "twitter_data": {},
            "synthesized_opportunities": []
        }
    
    def _save_data(self, data: Dict[str, Any]):
        """Save multi-source data."""
        try:
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def get_google_trends(
        self,
        keywords: List[str],
        region: str = "TR",
        timeframe: str = "today 3-m"
    ) -> Dict[str, Any]:
        """
        Get Google Trends data for keywords.
        
        Note: This uses a simple approach. For production, use pytrends library.
        
        Args:
            keywords: List of keywords to search
            region: Region code (TR, US, etc.)
            timeframe: Timeframe for trends
            
        Returns:
            Google Trends data
        """
        try:
            trends_data = {
                "keywords": keywords,
                "region": region,
                "timeframe": timeframe,
                "timestamp": datetime.now().isoformat(),
                "trends": {}
            }
            
            # Try to use pytrends if available
            try:
                from pytrends.request import TrendReq
                pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
                
                # Build payload (pytrends supports up to 5 keywords at once)
                for i in range(0, len(keywords), 5):
                    batch = keywords[i:i+5]
                    pytrends.build_payload(
                        batch,
                        cat=0,
                        timeframe=timeframe,
                        geo=region,
                        gprop=''
                    )
                    
                    # Get interest over time
                    interest_data = pytrends.interest_over_time()
                    if interest_data is not None and not interest_data.empty:
                        for keyword in batch:
                            if keyword in interest_data.columns:
                                avg_interest = interest_data[keyword].mean()
                                trends_data["trends"][keyword] = {
                                    "interest_score": float(avg_interest),
                                    "trending": avg_interest > 50,
                                    "related_queries": [],
                                    "data_source": "pytrends"
                                }
                    
                    # Get related queries
                    try:
                        related = pytrends.related_queries()
                        for keyword in batch:
                            if keyword in related and related[keyword]['top'] is not None:
                                trends_data["trends"][keyword]["related_queries"] = (
                                    related[keyword]['top']['query'].tolist()[:5]
                                )
                    except Exception:
                        pass
                    
                    time.sleep(1)  # Rate limiting
                
            except ImportError:
                # Fallback to simulated data if pytrends not available
                for keyword in keywords:
                    trends_data["trends"][keyword] = {
                        "interest_score": 50,
                        "trending": False,
                        "related_queries": [],
                        "note": "Using simulated data. Install pytrends for real data.",
                        "data_source": "simulated"
                    }
            except Exception as e:
                # If pytrends fails, use simulated data
                for keyword in keywords:
                    trends_data["trends"][keyword] = {
                        "interest_score": 50,
                        "trending": False,
                        "related_queries": [],
                        "error": str(e),
                        "data_source": "simulated"
                    }
            
            # Save data
            data = self._load_data()
            data["trends_data"][timeframe] = trends_data
            self._save_data(data)
            
            return trends_data
            
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_reddit_trends(
        self,
        subreddits: List[str],
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get trending posts from Reddit subreddits.
        
        Args:
            subreddits: List of subreddit names (without r/)
            limit: Number of posts per subreddit
            
        Returns:
            Reddit trending data
        """
        reddit_data = {
            "subreddits": subreddits,
            "timestamp": datetime.now().isoformat(),
            "trending_posts": {}
        }
        
        for subreddit in subreddits:
            try:
                # Try PRAW first if credentials available
                use_praw = False
                try:
                    import praw
                    import os
                    client_id = os.getenv("REDDIT_CLIENT_ID")
                    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
                    
                    if client_id and client_secret and client_id != "your_reddit_client_id_here":
                        reddit = praw.Reddit(
                            client_id=client_id,
                            client_secret=client_secret,
                            user_agent=os.getenv("REDDIT_USER_AGENT", "YouTube-SEO-AGI-Tool/1.0")
                        )
                        use_praw = True
                except ImportError:
                    pass
                except Exception:
                    pass
                
                if use_praw:
                    # Use PRAW for authenticated access
                    sub = reddit.subreddit(subreddit)
                    posts = list(sub.hot(limit=limit))
                    
                    trending_posts = []
                    for post in posts:
                        trending_posts.append({
                            "title": post.title,
                            "score": post.score,
                            "comments": post.num_comments,
                            "created_utc": post.created_utc,
                            "url": post.url,
                            "subreddit": subreddit,
                            "data_source": "praw"
                        })
                    
                    reddit_data["trending_posts"][subreddit] = trending_posts
                else:
                    # Fallback to public API
                    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
                    headers = {
                        "User-Agent": os.getenv("REDDIT_USER_AGENT", "YouTube-SEO-AGI-Tool/1.0")
                    }
                    
                    response = requests.get(url, headers=headers, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        posts = data.get("data", {}).get("children", [])[:limit]
                        
                        trending_posts = []
                        for post in posts:
                            post_data = post.get("data", {})
                            trending_posts.append({
                                "title": post_data.get("title", ""),
                                "score": post_data.get("score", 0),
                                "comments": post_data.get("num_comments", 0),
                                "created_utc": post_data.get("created_utc", 0),
                                "url": post_data.get("url", ""),
                                "subreddit": subreddit,
                                "data_source": "public_api"
                            })
                        
                        reddit_data["trending_posts"][subreddit] = trending_posts
                    else:
                        reddit_data["trending_posts"][subreddit] = []
                        reddit_data["error"] = f"HTTP {response.status_code}"
                    
                    time.sleep(1)  # Rate limiting
                
            except Exception as e:
                reddit_data["trending_posts"][subreddit] = []
                reddit_data["error"] = str(e)
        
        # Save data
        data = self._load_data()
        data["reddit_data"][datetime.now().strftime("%Y-%m-%d")] = reddit_data
        self._save_data(data)
        
        return reddit_data
    
    def get_twitter_trends(
        self,
        keywords: List[str],
        region: str = "Turkey"
    ) -> Dict[str, Any]:
        """
        Get Twitter/X trends for keywords.
        
        Note: Twitter API requires authentication. This is a simplified version.
        
        Args:
            keywords: Keywords to search
            region: Region for trends
            
        Returns:
            Twitter trends data
        """
        twitter_data = {
            "keywords": keywords,
            "region": region,
            "timestamp": datetime.now().isoformat(),
            "trends": {}
        }
        
        # Try to use tweepy if available
        try:
            import tweepy
            import os
            
            bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
            api_key = os.getenv("TWITTER_API_KEY")
            api_secret = os.getenv("TWITTER_API_SECRET")
            access_token = os.getenv("TWITTER_ACCESS_TOKEN")
            access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
            
            if bearer_token and bearer_token != "your_twitter_bearer_token_here":
                # Use Twitter API v2 with Bearer Token
                client = tweepy.Client(bearer_token=bearer_token)
                
                for keyword in keywords:
                    try:
                        # Search recent tweets
                        tweets = client.search_recent_tweets(
                            query=keyword,
                            max_results=10,
                            tweet_fields=['public_metrics', 'created_at']
                        )
                        
                        if tweets and tweets.data:
                            tweet_count = len(tweets.data)
                            total_engagement = sum(
                                tweet.public_metrics.get('like_count', 0) + 
                                tweet.public_metrics.get('retweet_count', 0)
                                for tweet in tweets.data
                            )
                            
                            twitter_data["trends"][keyword] = {
                                "tweet_count": tweet_count,
                                "trending": total_engagement > 100,
                                "total_engagement": total_engagement,
                                "related_hashtags": [],
                                "data_source": "tweepy_v2"
                            }
                        else:
                            twitter_data["trends"][keyword] = {
                                "tweet_count": 0,
                                "trending": False,
                                "related_hashtags": [],
                                "data_source": "tweepy_v2"
                            }
                        
                        time.sleep(1)  # Rate limiting
                    except Exception as e:
                        twitter_data["trends"][keyword] = {
                            "tweet_count": 0,
                            "trending": False,
                            "related_hashtags": [],
                            "error": str(e),
                            "data_source": "tweepy_v2"
                        }
            elif api_key and api_secret and access_token and access_token_secret:
                # Use Twitter API v1.1 with OAuth
                auth = tweepy.OAuthHandler(api_key, api_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth, wait_on_rate_limit=True)
                
                for keyword in keywords:
                    try:
                        tweets = api.search_tweets(q=keyword, count=10, lang='tr')
                        twitter_data["trends"][keyword] = {
                            "tweet_count": len(tweets),
                            "trending": len(tweets) > 5,
                            "related_hashtags": [],
                            "data_source": "tweepy_v1"
                        }
                        time.sleep(1)
                    except Exception as e:
                        twitter_data["trends"][keyword] = {
                            "tweet_count": 0,
                            "trending": False,
                            "related_hashtags": [],
                            "error": str(e),
                            "data_source": "tweepy_v1"
                        }
            else:
                raise ImportError("Twitter credentials not configured")
                
        except ImportError:
            # Fallback to simulated data
            for keyword in keywords:
                twitter_data["trends"][keyword] = {
                    "tweet_count": 0,
                    "trending": False,
                    "related_hashtags": [],
                    "note": "Install tweepy and configure Twitter API for real data",
                    "data_source": "simulated"
                }
        except Exception as e:
            # If Twitter API fails, use simulated data
            for keyword in keywords:
                twitter_data["trends"][keyword] = {
                    "tweet_count": 0,
                    "trending": False,
                    "related_hashtags": [],
                    "error": str(e),
                    "data_source": "simulated"
                }
        
        # Save data
        data = self._load_data()
        data["twitter_data"][datetime.now().strftime("%Y-%m-%d")] = twitter_data
        self._save_data(data)
        
        return twitter_data
    
    def get_youtube_analytics(
        self,
        channel_handle: str,
        metrics: List[str] = ["views", "subscribers", "likes", "comments"]
    ) -> Dict[str, Any]:
        """
        Get detailed YouTube Analytics data.
        
        Note: YouTube Analytics API requires OAuth. This uses Data API v3.
        
        Args:
            channel_handle: Channel handle
            metrics: Metrics to retrieve
            
        Returns:
            YouTube Analytics data
        """
        try:
            channel_data = self.client.get_channel_by_handle(channel_handle)
            if not channel_data.get("items"):
                return {"error": "Channel not found"}
            
            channel = channel_data["items"][0]
            channel_id = channel["id"]
            stats = channel["statistics"]
            
            # Get recent videos for detailed analytics
            videos = self.client.get_channel_videos(channel_id, max_results=10)
            
            analytics = {
                "channel_id": channel_id,
                "channel_handle": channel_handle,
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "subscribers": int(stats.get("subscriberCount", 0)),
                    "total_views": int(stats.get("viewCount", 0)),
                    "total_videos": int(stats.get("videoCount", 0))
                },
                "recent_videos_analytics": []
            }
            
            for video in videos:
                video_stats = video.get("statistics", {})
                analytics["recent_videos_analytics"].append({
                    "video_id": video["id"],
                    "title": video["snippet"]["title"],
                    "views": int(video_stats.get("viewCount", 0)),
                    "likes": int(video_stats.get("likeCount", 0)),
                    "comments": int(video_stats.get("commentCount", 0)),
                    "published_at": video["snippet"].get("publishedAt", "")
                })
            
            return analytics
            
        except Exception as e:
            return {"error": str(e)}
    
    def synthesize_opportunities(
        self,
        keywords: List[str],
        niche: str = "psychedelic anatolian rock"
    ) -> Dict[str, Any]:
        """
        Synthesize data from all sources to identify viral content opportunities.
        
        Args:
            keywords: Keywords to analyze
            niche: Content niche
            
        Returns:
            Synthesized opportunities
        """
        opportunities = {
            "timestamp": datetime.now().isoformat(),
            "keywords": keywords,
            "niche": niche,
            "sources_analyzed": [],
            "viral_opportunities": [],
            "trending_topics": [],
            "recommendations": []
        }
        
        # Get data from all sources
        sources = {}
        
        # Google Trends
        try:
            trends = self.get_google_trends(keywords, region="TR")
            sources["google_trends"] = trends
            opportunities["sources_analyzed"].append("Google Trends")
        except Exception as e:
            sources["google_trends"] = {"error": str(e)}
        
        # Reddit
        try:
            subreddits = ["turkishrock", "psychedelicrock", "music", "listentothis"]
            reddit = self.get_reddit_trends(subreddits, limit=5)
            sources["reddit"] = reddit
            opportunities["sources_analyzed"].append("Reddit")
            
            # Extract trending topics from Reddit
            for subreddit, posts in reddit.get("trending_posts", {}).items():
                for post in posts:
                    if post.get("score", 0) > 100:  # High engagement
                        opportunities["trending_topics"].append({
                            "source": "Reddit",
                            "subreddit": subreddit,
                            "title": post.get("title", ""),
                            "score": post.get("score", 0),
                            "relevance": self._calculate_relevance(post.get("title", ""), niche)
                        })
        except Exception as e:
            sources["reddit"] = {"error": str(e)}
        
        # Twitter
        try:
            twitter = self.get_twitter_trends(keywords)
            sources["twitter"] = twitter
            opportunities["sources_analyzed"].append("Twitter")
        except Exception as e:
            sources["twitter"] = {"error": str(e)}
        
        # YouTube Analytics
        try:
            youtube = self.get_youtube_analytics("anatolianturkishrock")
            sources["youtube"] = youtube
            opportunities["sources_analyzed"].append("YouTube Analytics")
        except Exception as e:
            sources["youtube"] = {"error": str(e)}
        
        # Identify viral opportunities
        viral_opportunities = self._identify_viral_opportunities(sources, keywords, niche)
        opportunities["viral_opportunities"] = viral_opportunities
        
        # Generate recommendations
        recommendations = self._generate_recommendations(sources, viral_opportunities)
        opportunities["recommendations"] = recommendations
        
        # Save synthesized data
        data = self._load_data()
        data["synthesized_opportunities"].append(opportunities)
        if len(data["synthesized_opportunities"]) > 50:
            data["synthesized_opportunities"] = data["synthesized_opportunities"][-50:]
        self._save_data(data)
        
        return opportunities
    
    def _calculate_relevance(self, text: str, niche: str) -> float:
        """Calculate relevance score between text and niche."""
        text_lower = text.lower()
        niche_keywords = niche.lower().split()
        
        matches = sum(1 for keyword in niche_keywords if keyword in text_lower)
        return matches / max(len(niche_keywords), 1)
    
    def _identify_viral_opportunities(
        self,
        sources: Dict[str, Any],
        keywords: List[str],
        niche: str
    ) -> List[Dict[str, Any]]:
        """Identify viral content opportunities from synthesized data."""
        opportunities = []
        
        # Check Reddit for high-engagement posts
        reddit_data = sources.get("reddit", {})
        trending_posts = reddit_data.get("trending_posts", {})
        
        for subreddit, posts in trending_posts.items():
            for post in posts:
                score = post.get("score", 0)
                relevance = self._calculate_relevance(post.get("title", ""), niche)
                
                if score > 500 and relevance > 0.3:
                    opportunities.append({
                        "type": "reddit_trending",
                        "source": "Reddit",
                        "title": post.get("title", ""),
                        "score": score,
                        "relevance": relevance,
                        "opportunity": f"Create content related to: {post.get('title', '')}",
                        "viral_potential": min(score / 1000, 1.0),
                        "subreddit": subreddit
                    })
        
        # Check Google Trends
        trends_data = sources.get("google_trends", {})
        trends = trends_data.get("trends", {})
        
        for keyword, trend_info in trends.items():
            if trend_info.get("trending", False) or trend_info.get("interest_score", 0) > 70:
                opportunities.append({
                    "type": "trending_keyword",
                    "source": "Google Trends",
                    "keyword": keyword,
                    "interest_score": trend_info.get("interest_score", 0),
                    "opportunity": f"Create content using trending keyword: {keyword}",
                    "viral_potential": trend_info.get("interest_score", 0) / 100
                })
        
        # Sort by viral potential
        opportunities.sort(key=lambda x: x.get("viral_potential", 0), reverse=True)
        
        return opportunities[:10]  # Top 10 opportunities
    
    def _generate_recommendations(
        self,
        sources: Dict[str, Any],
        viral_opportunities: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate actionable recommendations from synthesized data."""
        recommendations = []
        
        if viral_opportunities:
            top_opportunity = viral_opportunities[0]
            recommendations.append(
                f"🔥 High viral potential: {top_opportunity.get('opportunity', '')} "
                f"(Potential: {top_opportunity.get('viral_potential', 0):.1%})"
            )
        
        # Check source availability
        available_sources = len([s for s in sources.values() if not s.get("error")])
        if available_sources < 3:
            recommendations.append(
                f"⚠️ Only {available_sources} data sources available. "
                "Configure additional APIs for better insights."
            )
        
        # Reddit recommendations
        reddit_data = sources.get("reddit", {})
        if reddit_data.get("trending_posts"):
            recommendations.append(
                "📊 Monitor Reddit trends regularly for content ideas"
            )
        
        # Google Trends recommendations
        trends_data = sources.get("google_trends", {})
        if trends_data.get("trends"):
            recommendations.append(
                "📈 Use Google Trends to identify rising keywords before they peak"
            )
        
        return recommendations
    
    def get_data_source_status(self) -> Dict[str, Any]:
        """Get status of all data sources."""
        status = {
            "timestamp": datetime.now().isoformat(),
            "sources": {}
        }
        
        # Check each source
        sources = {
            "Google Trends": {
                "status": "partial",
                "note": "Install pytrends for full functionality",
                "configured": False
            },
            "Reddit": {
                "status": "active",
                "note": "Using public Reddit API",
                "configured": True
            },
            "Twitter": {
                "status": "requires_auth",
                "note": "Twitter API requires authentication",
                "configured": False
            },
            "YouTube Analytics": {
                "status": "active",
                "note": "Using YouTube Data API v3",
                "configured": True
            }
        }
        
        status["sources"] = sources
        status["active_sources"] = len([s for s in sources.values() if s.get("configured")])
        status["total_sources"] = len(sources)
        
        return status

