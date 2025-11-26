"""
Streamlit API Endpoints
API endpoints that work within Streamlit app for browser extension.

Since Streamlit Cloud doesn't support separate FastAPI apps,
we create API endpoints using Streamlit's own routing.
"""

import streamlit as st
import json
from typing import Dict, Any, Optional
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from src.utils.youtube_client import YouTubeClient, create_client
from src.modules.video_seo_audit import VideoSEOAudit
from src.modules.keyword_researcher import KeywordResearcher
from src.utils.logger import get_logger
from src.utils.rate_limiter import get_rate_limiter, check_rate_limit

logger = get_logger("streamlit_api")


def handle_api_request(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle API requests from browser extension.
    
    Args:
        query_params: Query parameters from request
    
    Returns:
        Response dictionary
    """
    action = query_params.get("action")
    
    if action == "health":
        return {"status": "ok", "service": "YouTube SEO AGI Tool API", "version": "1.0.0"}
    
    elif action == "seo_analyze":
        return handle_seo_analyze(query_params)
    
    elif action == "keywords_suggest":
        return handle_keywords_suggest(query_params)
    
    elif action == "video_data":
        return handle_video_data(query_params)
    
    elif action == "similar_videos_analyze":
        return handle_similar_videos_analyze(query_params)
    
    elif action == "thumbnail_analyze":
        return handle_thumbnail_analyze(query_params)
    
    elif action == "caption_analyze":
        return handle_caption_analyze(query_params)
    
    elif action == "engagement_suggest":
        return handle_engagement_suggest(query_params)
    
    elif action == "compare_videos":
        return handle_compare_videos(query_params)
    
    else:
        return {"error": "Unknown action", "status": "error"}


def handle_seo_analyze(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle SEO analysis request."""
    try:
        video_id = query_params.get("video_id")
        channel_handle = query_params.get("channel_handle")
        niche = query_params.get("niche")
        
        if not video_id:
            return {"error": "video_id required", "status": "error"}
        
        # Get API key from session state or environment
        api_key = st.session_state.get("user_api_key") or os.getenv("YOUTUBE_API_KEY", "")
        if not api_key:
            return {"error": "API key not configured", "status": "error"}
        
        # Initialize client
        client = create_client(api_key=api_key)
        
        # Initialize modules
        keyword_researcher = KeywordResearcher(client)
        from src.modules.title_optimizer import TitleOptimizer
        from src.modules.description_generator import DescriptionGenerator
        from src.modules.tag_suggester import TagSuggester
        
        title_optimizer = TitleOptimizer(keyword_researcher)
        description_generator = DescriptionGenerator()
        tag_suggester = TagSuggester(client)
        
        video_seo_audit = VideoSEOAudit(
            client,
            keyword_researcher,
            title_optimizer,
            description_generator,
            tag_suggester
        )
        
        # Perform audit
        audit_result = video_seo_audit.audit_video(
            video_id=video_id,
            channel_handle=channel_handle,
            niche=niche
        )
        
        # Format response
        return {
            "success": True,
            "data": {
                "video_id": video_id,
                "seo_score": audit_result.get("overall_score", 0),
                "title_score": audit_result.get("title_score", 0),
                "description_score": audit_result.get("description_score", 0),
                "tags_score": audit_result.get("tags_score", 0),
                "thumbnail_score": audit_result.get("thumbnail_score", 0),
                "recommendations": audit_result.get("recommendations", [])[:5],
                "keywords": audit_result.get("suggested_keywords", [])[:10],
                # Auto-fill data
                "title_suggestions": audit_result.get("title_suggestions", [])[:3],
                "description": audit_result.get("optimized_description", ""),
                "tags": audit_result.get("suggested_tags", [])[:15]
            }
        }
    except Exception as e:
        logger.error(f"Error in SEO analyze: {e}")
        return {"error": str(e), "status": "error"}


def handle_keywords_suggest(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle keyword suggestions request."""
    try:
        topic = query_params.get("topic")
        niche = query_params.get("niche")
        
        if not topic:
            return {"error": "topic required", "status": "error"}
        
        api_key = st.session_state.get("user_api_key") or os.getenv("YOUTUBE_API_KEY", "")
        if not api_key:
            return {"error": "API key not configured", "status": "error"}
        
        client = create_client(api_key=api_key)
        keyword_researcher = KeywordResearcher(client)
        
        keywords = [topic]
        if niche:
            keywords.append(niche)
        
        research = keyword_researcher.research_keywords(keywords)
        ranked_keywords = research.get("ranked_keywords", [])[:20]
        
        return {
            "success": True,
            "data": {
                "keywords": [kw.get("keyword") for kw in ranked_keywords],
                "total_found": research.get("total_keywords_found", 0)
            }
        }
    except Exception as e:
        logger.error(f"Error in keywords suggest: {e}")
        return {"error": str(e), "status": "error"}


def handle_video_data(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle video data request."""
    try:
        video_id = query_params.get("video_id")
        
        if not video_id:
            return {"error": "video_id required", "status": "error"}
        
        api_key = st.session_state.get("user_api_key") or os.getenv("YOUTUBE_API_KEY", "")
        if not api_key:
            return {"error": "API key not configured", "status": "error"}
        
        client = create_client(api_key=api_key)
        video_data = client.get_video_by_id(video_id)
        
        if not video_data.get("items"):
            return {"error": "Video not found", "status": "error"}
        
        video = video_data["items"][0]
        return {
            "success": True,
            "data": {
                "video_id": video_id,
                "title": video["snippet"]["title"],
                "description": video["snippet"]["description"],
                "channel_id": video["snippet"]["channelId"],
                "published_at": video["snippet"]["publishedAt"],
                "statistics": video.get("statistics", {}),
                "tags": video["snippet"].get("tags", [])
            }
        }
    except Exception as e:
        logger.error(f"Error in video data: {e}")
        return {"error": str(e), "status": "error"}


def handle_similar_videos_analyze(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle similar videos analysis request."""
    try:
        video_id = query_params.get("video_id")
        niche = query_params.get("niche")
        max_results = int(query_params.get("max_results", 5))
        
        if not video_id:
            return {"error": "video_id required", "status": "error"}
        
        api_key = st.session_state.get("user_api_key") or os.getenv("YOUTUBE_API_KEY", "")
        if not api_key:
            return {"error": "API key not configured", "status": "error"}
        
        client = create_client(api_key=api_key)
        
        # Get current video data
        video_data = client.get_video_by_id(video_id)
        if not video_data.get("items"):
            return {"error": "Video not found", "status": "error"}
        
        current_video = video_data["items"][0]
        current_title = current_video["snippet"]["title"]
        current_tags = current_video["snippet"].get("tags", [])
        
        # Extract keywords from title and tags
        import re
        title_words = [w.lower() for w in re.findall(r'\b\w+\b', current_title) if len(w) > 3]
        search_keywords = title_words[:3] + [tag.lower() for tag in current_tags[:2]]
        if niche:
            search_keywords.append(niche.lower())
        
        # Search for similar videos
        similar_videos = []
        seen_video_ids = {video_id}
        
        for keyword in search_keywords[:3]:  # Use top 3 keywords
            try:
                search_results = client.search_videos(
                    keyword,
                    max_results=10,
                    order="viewCount"
                )
                
                for result in search_results:
                    similar_video_id = result["id"]["videoId"]
                    if similar_video_id in seen_video_ids:
                        continue
                    seen_video_ids.add(similar_video_id)
                    
                    similar_videos.append({
                        "video_id": similar_video_id,
                        "title": result["snippet"]["title"],
                        "channel_title": result["snippet"]["channelTitle"],
                        "published_at": result["snippet"]["publishedAt"],
                        "thumbnail": result["snippet"]["thumbnails"]["high"]["url"]
                    })
                    
                    if len(similar_videos) >= max_results * 2:  # Get more for filtering
                        break
            except Exception as e:
                logger.warning(f"Error searching for keyword {keyword}: {e}")
                continue
            
            if len(similar_videos) >= max_results * 2:
                break
        
        # Get detailed data and calculate SEO scores for similar videos
        if similar_videos:
            video_ids = [v["video_id"] for v in similar_videos]
            detailed_videos = client.get_videos_details(video_ids)
            
            # Initialize SEO audit
            keyword_researcher = KeywordResearcher(client)
            from src.modules.title_optimizer import TitleOptimizer
            from src.modules.description_generator import DescriptionGenerator
            from src.modules.tag_suggester import TagSuggester
            
            title_optimizer = TitleOptimizer(keyword_researcher)
            description_generator = DescriptionGenerator()
            tag_suggester = TagSuggester(client)
            
            video_seo_audit = VideoSEOAudit(
                client,
                keyword_researcher,
                title_optimizer,
                description_generator,
                tag_suggester
            )
            
            # Analyze each similar video
            analyzed_videos = []
            for video_detail in detailed_videos[:max_results]:
                similar_video_id = video_detail["id"]
                try:
                    audit_result = video_seo_audit.audit_video(
                        video_id=similar_video_id,
                        niche=niche
                    )
                    
                    stats = video_detail.get("statistics", {})
                    analyzed_videos.append({
                        "video_id": similar_video_id,
                        "title": video_detail["snippet"]["title"],
                        "channel_title": video_detail["snippet"]["channelTitle"],
                        "seo_score": audit_result.get("overall_score", 0),
                        "title_score": audit_result.get("title_score", 0),
                        "description_score": audit_result.get("description_score", 0),
                        "tags_score": audit_result.get("tags_score", 0),
                        "views": int(stats.get("viewCount", 0)),
                        "likes": int(stats.get("likeCount", 0)),
                        "comments": int(stats.get("commentCount", 0)),
                        "tags": video_detail["snippet"].get("tags", [])[:10],
                        "description_preview": video_detail["snippet"].get("description", "")[:200],
                        "thumbnail": video_detail["snippet"]["thumbnails"]["high"]["url"]
                    })
                except Exception as e:
                    logger.warning(f"Error analyzing similar video {similar_video_id}: {e}")
                    continue
            
            # Sort by SEO score and views
            analyzed_videos.sort(key=lambda x: (x["seo_score"], x["views"]), reverse=True)
            
            # Extract learnings from top videos
            learnings = []
            if analyzed_videos:
                top_video = analyzed_videos[0]
                if top_video["seo_score"] > 70:
                    learnings.append(f"Top video uses: {', '.join(top_video['tags'][:5])}")
                    if top_video["title_score"] > 80:
                        learnings.append(f"Strong title pattern: '{top_video['title'][:50]}...'")
                    if top_video["description_score"] > 80:
                        learnings.append("Well-optimized description with keywords")
            
            return {
                "success": True,
                "data": {
                    "current_video_id": video_id,
                    "current_title": current_title,
                    "similar_videos": analyzed_videos[:max_results],
                    "learnings": learnings,
                    "total_found": len(analyzed_videos)
                }
            }
        else:
            return {
                "success": True,
                "data": {
                    "current_video_id": video_id,
                    "current_title": current_title,
                    "similar_videos": [],
                    "learnings": [],
                    "total_found": 0
                }
            }
    except Exception as e:
        logger.error(f"Error in similar videos analyze: {e}")
        return {"error": str(e), "status": "error"}


def handle_thumbnail_analyze(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle thumbnail analysis request."""
    try:
        video_id = query_params.get("video_id")
        
        if not video_id:
            return {"error": "video_id required", "status": "error"}
        
        api_key = st.session_state.get("user_api_key") or os.getenv("YOUTUBE_API_KEY", "")
        if not api_key:
            return {"error": "API key not configured", "status": "error"}
        
        client = create_client(api_key=api_key)
        
        from src.modules.thumbnail_enhancer import ThumbnailEnhancer
        thumbnail_enhancer = ThumbnailEnhancer(client)
        
        analysis = thumbnail_enhancer.analyze_thumbnail(video_id)
        
        return {
            "success": True,
            "data": {
                "video_id": video_id,
                "thumbnail_score": analysis.get("overall_score", 0),
                "color_score": analysis.get("color_score", 0),
                "contrast_score": analysis.get("contrast_score", 0),
                "text_score": analysis.get("text_score", 0),
                "face_detection": analysis.get("face_detected", False),
                "recommendations": analysis.get("recommendations", [])[:5],
                "ctr_estimate": analysis.get("estimated_ctr", 0)
            }
        }
    except Exception as e:
        logger.error(f"Error in thumbnail analyze: {e}")
        return {"error": str(e), "status": "error"}


def handle_caption_analyze(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle caption analysis request."""
    try:
        video_id = query_params.get("video_id")
        niche = query_params.get("niche")
        
        if not video_id:
            return {"error": "video_id required", "status": "error"}
        
        api_key = st.session_state.get("user_api_key") or os.getenv("YOUTUBE_API_KEY", "")
        if not api_key:
            return {"error": "API key not configured", "status": "error"}
        
        client = create_client(api_key=api_key)
        keyword_researcher = KeywordResearcher(client)
        
        from src.modules.caption_optimizer import CaptionOptimizer
        caption_optimizer = CaptionOptimizer(client, keyword_researcher)
        
        # Get captions and analyze
        captions_data = caption_optimizer.get_video_captions(video_id)
        
        if captions_data.get("error"):
            return {
                "success": True,
                "data": {
                    "video_id": video_id,
                    "caption_score": 0,
                    "has_captions": False,
                    "recommendations": ["Add captions to improve SEO and accessibility"],
                    "keyword_opportunities": []
                }
            }
        
        # Optimize captions
        optimization = caption_optimizer.optimize_captions(
            video_id=video_id,
            niche=niche
        )
        
        return {
            "success": True,
            "data": {
                "video_id": video_id,
                "caption_score": optimization.get("seo_score", 0),
                "has_captions": True,
                "word_count": optimization.get("word_count", 0),
                "keyword_coverage": optimization.get("keyword_coverage", 0),
                "recommendations": optimization.get("recommendations", [])[:5],
                "keyword_opportunities": optimization.get("missing_keywords", [])[:10]
            }
        }
    except Exception as e:
        logger.error(f"Error in caption analyze: {e}")
        return {"error": str(e), "status": "error"}


def handle_engagement_suggest(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle engagement suggestions request."""
    try:
        video_id = query_params.get("video_id")
        niche = query_params.get("niche")
        
        if not video_id:
            return {"error": "video_id required", "status": "error"}
        
        api_key = st.session_state.get("user_api_key") or os.getenv("YOUTUBE_API_KEY", "")
        if not api_key:
            return {"error": "API key not configured", "status": "error"}
        
        client = create_client(api_key=api_key)
        
        from src.modules.engagement_booster import EngagementBooster
        engagement_booster = EngagementBooster(client)
        
        suggestions = engagement_booster.suggest_engagement_elements(
            video_id=video_id,
            niche=niche
        )
        
        return {
            "success": True,
            "data": {
                "video_id": video_id,
                "polls": suggestions.get("polls", [])[:3],
                "cards": suggestions.get("cards", [])[:3],
                "end_screens": suggestions.get("end_screens", [])[:3],
                "recommendations": suggestions.get("recommendations", [])[:5]
            }
        }
    except Exception as e:
        logger.error(f"Error in engagement suggest: {e}")
        return {"error": str(e), "status": "error"}


def handle_compare_videos(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle video comparison request."""
    try:
        video_id = query_params.get("video_id")
        compare_with = query_params.get("compare_with", "").split(",")  # Comma-separated video IDs
        
        if not video_id:
            return {"error": "video_id required", "status": "error"}
        
        if not compare_with or not compare_with[0]:
            return {"error": "compare_with required (comma-separated video IDs)", "status": "error"}
        
        api_key = st.session_state.get("user_api_key") or os.getenv("YOUTUBE_API_KEY", "")
        if not api_key:
            return {"error": "API key not configured", "status": "error"}
        
        client = create_client(api_key=api_key)
        
        # Get all video details
        all_video_ids = [video_id] + compare_with
        videos = client.get_videos_details(all_video_ids)
        
        if not videos:
            return {"error": "Videos not found", "status": "error"}
        
        # Initialize SEO audit
        keyword_researcher = KeywordResearcher(client)
        from src.modules.title_optimizer import TitleOptimizer
        from src.modules.description_generator import DescriptionGenerator
        from src.modules.tag_suggester import TagSuggester
        
        title_optimizer = TitleOptimizer(keyword_researcher)
        description_generator = DescriptionGenerator()
        tag_suggester = TagSuggester(client)
        
        video_seo_audit = VideoSEOAudit(
            client,
            keyword_researcher,
            title_optimizer,
            description_generator,
            tag_suggester
        )
        
        # Analyze each video
        comparison = []
        for video in videos:
            try:
                audit_result = video_seo_audit.audit_video(video_id=video["id"])
                stats = video.get("statistics", {})
                
                comparison.append({
                    "video_id": video["id"],
                    "title": video["snippet"]["title"],
                    "seo_score": audit_result.get("overall_score", 0),
                    "title_score": audit_result.get("title_score", 0),
                    "description_score": audit_result.get("description_score", 0),
                    "tags_score": audit_result.get("tags_score", 0),
                    "thumbnail_score": audit_result.get("thumbnail_score", 0),
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0))
                })
            except Exception as e:
                logger.warning(f"Error analyzing video {video.get('id', 'unknown')}: {e}")
                continue
        
        return {
            "success": True,
            "data": {
                "comparison": comparison,
                "total_videos": len(comparison)
            }
        }
    except Exception as e:
        logger.error(f"Error in compare videos: {e}")
        return {"error": str(e), "status": "error"}

