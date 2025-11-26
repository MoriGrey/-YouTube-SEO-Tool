"""
Extension API Endpoints
REST API for browser extension communication.

Provides endpoints for:
- Video SEO analysis
- Keyword suggestions
- Competitor comparison
- Real-time analytics
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from src.utils.youtube_client import YouTubeClient, create_client
from src.modules.video_seo_audit import VideoSEOAudit
from src.modules.keyword_researcher import KeywordResearcher
from src.modules.competitor_analyzer import CompetitorAnalyzer
from src.utils.logger import get_logger
from src.utils.rate_limiter import get_rate_limiter, check_rate_limit

# Initialize logger
logger = get_logger("extension_api")

# Initialize FastAPI app
app = FastAPI(
    title="YouTube SEO AGI Tool API",
    description="REST API for browser extension and mobile app",
    version="1.0.0"
)

# CORS middleware (allow extension to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global clients (initialize on startup)
youtube_client: Optional[YouTubeClient] = None
video_seo_audit: Optional[VideoSEOAudit] = None
keyword_researcher: Optional[KeywordResearcher] = None
competitor_analyzer: Optional[CompetitorAnalyzer] = None
rate_limiter = get_rate_limiter()


def get_api_key(authorization: Optional[str] = Header(None)) -> str:
    """Extract and validate API key from header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="API key required")
    
    # Support both "Bearer <token>" and direct token
    if authorization.startswith("Bearer "):
        api_key = authorization[7:]
    else:
        api_key = authorization
    
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return api_key


@app.on_event("startup")
async def startup_event():
    """Initialize clients on startup."""
    global youtube_client, video_seo_audit, keyword_researcher, competitor_analyzer
    
    # Get API key from environment or use default
    api_key = os.getenv("YOUTUBE_API_KEY", "")
    
    if api_key:
        try:
            youtube_client = create_client(api_key=api_key)
            keyword_researcher = KeywordResearcher(youtube_client)
            competitor_analyzer = CompetitorAnalyzer(youtube_client)
            
            # Video SEO Audit requires multiple modules
            from src.modules.title_optimizer import TitleOptimizer
            from src.modules.description_generator import DescriptionGenerator
            from src.modules.tag_suggester import TagSuggester
            
            title_optimizer = TitleOptimizer(keyword_researcher)
            description_generator = DescriptionGenerator()
            tag_suggester = TagSuggester(youtube_client)
            
            video_seo_audit = VideoSEOAudit(
                youtube_client,
                keyword_researcher,
                title_optimizer,
                description_generator,
                tag_suggester
            )
            
            logger.info("Extension API initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing extension API: {e}")
    else:
        logger.warning("No YouTube API key found, some endpoints may not work")


@app.get("/")
async def root():
    """API health check."""
    return {
        "status": "ok",
        "service": "YouTube SEO AGI Tool API",
        "version": "1.0.0"
    }


@app.get("/video/{video_id}")
async def get_video_data(video_id: str, api_key: str = Depends(get_api_key)):
    """Get basic video data."""
    if not youtube_client:
        raise HTTPException(status_code=503, detail="YouTube client not initialized")
    
    # Check rate limit
    allowed, error_msg = check_rate_limit("extension_api")
    if not allowed:
        raise HTTPException(status_code=429, detail=error_msg)
    
    try:
        video_data = youtube_client.get_video_by_id(video_id)
        if not video_data.get("items"):
            raise HTTPException(status_code=404, detail="Video not found")
        
        video = video_data["items"][0]
        return {
            "video_id": video_id,
            "title": video["snippet"]["title"],
            "description": video["snippet"]["description"],
            "channel_id": video["snippet"]["channelId"],
            "published_at": video["snippet"]["publishedAt"],
            "statistics": video.get("statistics", {}),
            "tags": video["snippet"].get("tags", [])
        }
    except Exception as e:
        logger.error(f"Error fetching video data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/seo/analyze")
async def analyze_seo(request: Dict[str, Any], api_key: str = Depends(get_api_key)):
    """Analyze video SEO."""
    if not video_seo_audit:
        raise HTTPException(status_code=503, detail="SEO audit module not initialized")
    
    video_id = request.get("video_id")
    channel_handle = request.get("channel_handle")
    niche = request.get("niche")
    
    if not video_id:
        raise HTTPException(status_code=400, detail="video_id required")
    
    # Check rate limit
    allowed, error_msg = check_rate_limit("extension_api")
    if not allowed:
        raise HTTPException(status_code=429, detail=error_msg)
    
    try:
        audit_result = video_seo_audit.audit_video(
            video_id=video_id,
            channel_handle=channel_handle,
            niche=niche
        )
        
        # Format response for extension with auto-fill data
        return {
            "video_id": video_id,
            "seo_score": audit_result.get("overall_score", 0),
            "title_score": audit_result.get("title_score", 0),
            "description_score": audit_result.get("description_score", 0),
            "tags_score": audit_result.get("tags_score", 0),
            "thumbnail_score": audit_result.get("thumbnail_score", 0),
            "recommendations": audit_result.get("recommendations", [])[:5],  # Top 5
            "keywords": audit_result.get("suggested_keywords", [])[:10],  # Top 10
            # Auto-fill data
            "title_suggestions": audit_result.get("title_suggestions", [])[:3],  # Top 3 titles
            "description": audit_result.get("optimized_description", ""),  # Optimized description
            "tags": audit_result.get("suggested_tags", [])[:15]  # Top 15 tags
        }
    except Exception as e:
        logger.error(f"Error analyzing SEO: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/keywords/suggest")
async def suggest_keywords(request: Dict[str, Any], api_key: str = Depends(get_api_key)):
    """Get keyword suggestions."""
    if not keyword_researcher:
        raise HTTPException(status_code=503, detail="Keyword researcher not initialized")
    
    topic = request.get("topic")
    niche = request.get("niche")
    
    if not topic:
        raise HTTPException(status_code=400, detail="topic required")
    
    # Check rate limit
    allowed, error_msg = check_rate_limit("extension_api")
    if not allowed:
        raise HTTPException(status_code=429, detail=error_msg)
    
    try:
        keywords = [topic]
        if niche:
            keywords.append(niche)
        
        research = keyword_researcher.research_keywords(keywords)
        
        # Return top keywords
        ranked_keywords = research.get("ranked_keywords", [])[:20]
        return {
            "keywords": [kw.get("keyword") for kw in ranked_keywords],
            "total_found": research.get("total_keywords_found", 0)
        }
    except Exception as e:
        logger.error(f"Error suggesting keywords: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "youtube_client": youtube_client is not None,
        "modules_initialized": {
            "video_seo_audit": video_seo_audit is not None,
            "keyword_researcher": keyword_researcher is not None,
            "competitor_analyzer": competitor_analyzer is not None
        }
    }


# Run with: uvicorn src.api.extension_api:app --host 0.0.0.0 --port 8000

