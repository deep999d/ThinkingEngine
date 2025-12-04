"""REST API server for Thinking Engine - CustomGPT integration."""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from .document_loaders import DocumentLoader, Document
from .llm_orchestrator import LLMOrchestrator
from .blog_generator import BlogGenerator
from .tweet_generator import TweetGenerator

load_dotenv()

# Get base URL from environment variable
# This is required for CustomGPT to know where to make API calls
# Set this in Render environment variables to your actual Render URL
# Example: https://your-app-name.onrender.com
BASE_URL = os.getenv("API_BASE_URL", "")

# Build servers list for OpenAPI schema
# CustomGPT requires the 'servers' field to be present
servers = []
if BASE_URL:
    servers.append({"url": BASE_URL, "description": "Production server"})
else:
    # If not set, add a placeholder that users should replace
    # This ensures OpenAPI schema is valid even if URL not configured
    servers.append({"url": "https://your-app-name.onrender.com", "description": "Set API_BASE_URL environment variable"})

app = FastAPI(
    title="Thinking Engine API",
    description="AI Content Thinking Engine - Generate blog posts and tweets from curated research",
    version="0.1.0",
    servers=servers
)

# Enable CORS for CustomGPT integration
# CustomGPT requires explicit CORS headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for CustomGPT
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "HEAD"],  # Explicitly allow these methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)

# Middleware to add CORS headers to all responses
class CORSHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Add CORS headers to all responses
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, HEAD"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

app.add_middleware(CORSHeaderMiddleware)

# Note: FastAPI's CORSMiddleware automatically handles OPTIONS requests
# We don't need explicit OPTIONS handlers - they cause issues with CustomGPT schema import
# The catch-all OPTIONS handler was removed because CustomGPT doesn't recognize it
# CORS is fully handled by CORSMiddleware and CORSHeaderMiddleware above


# Request/Response Models
class WeekFolderResponse(BaseModel):
    week_folders: List[str]
    count: int


class DocumentInfo(BaseModel):
    title: str
    source: str
    file_path: str
    file_type: str


class WeekDocumentsResponse(BaseModel):
    week_folder: str
    documents: List[DocumentInfo]
    count: int


class GenerateBlogRequest(BaseModel):
    week_folder: str = Field(..., description="Week folder name (e.g., 'week-2025-01-15')")
    return_content: bool = Field(True, description="Whether to return the blog post content in response")


class GenerateBlogResponse(BaseModel):
    success: bool
    week_folder: str
    output_file: str
    citation_count: int
    has_fact_check_issues: bool
    fact_check_issues: List[Dict[str, Any]]
    content: Optional[str] = None
    message: str


class GenerateTweetsRequest(BaseModel):
    week_folder: str = Field(..., description="Week folder name (e.g., 'week-2025-01-15')")
    count: int = Field(25, ge=1, le=100, description="Number of tweet ideas to generate")
    return_content: bool = Field(True, description="Whether to return tweet content in response")


class TweetIdea(BaseModel):
    tweet: str
    hashtags: Optional[str] = None
    source: Optional[str] = None


class GenerateTweetsResponse(BaseModel):
    success: bool
    week_folder: str
    json_file: str
    txt_file: str
    tweet_count: int
    has_fact_check_issues: bool
    fact_check_issues: List[Dict[str, Any]]
    tweets: Optional[List[TweetIdea]] = None
    message: str


class GenerateAllRequest(BaseModel):
    week_folder: str = Field(..., description="Week folder name (e.g., 'week-2025-01-15')")
    tweet_count: int = Field(25, ge=1, le=100, description="Number of tweet ideas to generate")
    return_content: bool = Field(True, description="Whether to return content in response")


class GenerateAllResponse(BaseModel):
    success: bool
    week_folder: str
    blog: Dict[str, Any]
    tweets: Dict[str, Any]
    message: str


class ErrorResponse(BaseModel):
    success: bool
    error: str
    detail: Optional[str] = None


# Helper functions
def _get_loader() -> DocumentLoader:
    """Get DocumentLoader instance."""
    return DocumentLoader()


def _get_llm() -> LLMOrchestrator:
    """Get LLMOrchestrator instance."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OPENAI_API_KEY not set in environment"
        )
    return LLMOrchestrator()


# API Endpoints
@app.get("/", tags=["Info"])
async def root():
    """API root endpoint."""
    return JSONResponse(
        content={
            "name": "Thinking Engine API",
            "version": "0.1.0",
            "description": "AI Content Thinking Engine - Generate blog posts and tweets from curated research",
            "status": "online",
            "endpoints": {
                "list_weeks": "/api/weeks",
                "get_week_documents": "/api/weeks/{week_folder}/documents",
                "generate_blog": "/api/generate/blog",
                "generate_tweets": "/api/generate/tweets",
                "generate_all": "/api/generate/all"
            }
        }
    )


@app.get("/test", tags=["Info"])
async def test_endpoint():
    """Simple test endpoint to verify API is accessible."""
    return JSONResponse(
        content={
            "status": "ok",
            "message": "API is accessible",
            "timestamp": "2025-01-15"
        }
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for deployment monitoring."""
    try:
        # Quick check if data directory exists
        data_path = Path("data")
        has_data = data_path.exists()
        
        # Check if OpenAI API key is configured
        api_key_configured = bool(os.getenv("OPENAI_API_KEY"))
        
        return {
            "status": "healthy",
            "data_directory_exists": has_data,
            "api_key_configured": api_key_configured,
            "version": "0.1.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.get("/api/weeks", response_model=WeekFolderResponse, tags=["Weeks"])
async def list_week_folders():
    """List all available week folders."""
    try:
        loader = _get_loader()
        folders = loader.list_week_folders()
        return WeekFolderResponse(week_folders=folders, count=len(folders))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing week folders: {str(e)}"
        )


@app.get("/api/weeks/{week_folder}/documents", response_model=WeekDocumentsResponse, tags=["Weeks"])
async def get_week_documents(week_folder: str):
    """Get documents in a specific week folder."""
    try:
        loader = _get_loader()
        docs = loader.load_week_folder(week_folder)
        
        document_info = [
            DocumentInfo(
                title=doc.title,
                source=doc.source,
                file_path=doc.file_path,
                file_type=doc.file_type
            )
            for doc in docs
        ]
        
        return WeekDocumentsResponse(
            week_folder=week_folder,
            documents=document_info,
            count=len(document_info)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading documents: {str(e)}"
        )


@app.post("/api/generate/blog", response_model=GenerateBlogResponse, tags=["Generation"])
async def generate_blog(request: GenerateBlogRequest):
    """Generate a blog post from curated documents in a week folder."""
    try:
        loader = _get_loader()
        docs = loader.load_week_folder(request.week_folder)
        
        if not docs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No documents found in week folder: {request.week_folder}"
            )
        
        llm = _get_llm()
        blog_gen = BlogGenerator(llm)
        
        output_path = f"output/{request.week_folder}/blog-post.md"
        result = blog_gen.generate(docs, output_path)
        
        content = None
        if request.return_content:
            output_file = Path(result['output_file'])
            if output_file.exists():
                content = output_file.read_text(encoding='utf-8')
        
        return GenerateBlogResponse(
            success=True,
            week_folder=request.week_folder,
            output_file=result['output_file'],
            citation_count=result['fact_check']['citation_count'],
            has_fact_check_issues=result['fact_check']['has_issues'],
            fact_check_issues=result['fact_check'].get('issues', []),
            content=content,
            message="Blog post generated successfully"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating blog post: {str(e)}"
        )


@app.post("/api/generate/tweets", response_model=GenerateTweetsResponse, tags=["Generation"])
async def generate_tweets(request: GenerateTweetsRequest):
    """Generate tweet ideas from curated documents in a week folder."""
    try:
        loader = _get_loader()
        docs = loader.load_week_folder(request.week_folder)
        
        if not docs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No documents found in week folder: {request.week_folder}"
            )
        
        llm = _get_llm()
        tweet_gen = TweetGenerator(llm, count=request.count)
        
        output_dir = f"output/{request.week_folder}"
        result = tweet_gen.generate(docs, output_dir)
        
        tweets = None
        if request.return_content:
            import json
            json_file = Path(result['json_file'])
            if json_file.exists():
                data = json.loads(json_file.read_text(encoding='utf-8'))
                tweets = [TweetIdea(**tweet) for tweet in data.get('tweets', [])]
        
        return GenerateTweetsResponse(
            success=True,
            week_folder=request.week_folder,
            json_file=result['json_file'],
            txt_file=result['txt_file'],
            tweet_count=result['tweet_count'],
            has_fact_check_issues=result['fact_check']['has_issues'],
            fact_check_issues=result['fact_check'].get('issues', []),
            tweets=tweets,
            message=f"Generated {result['tweet_count']} tweet ideas successfully"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating tweets: {str(e)}"
        )


@app.post("/api/generate/all", response_model=GenerateAllResponse, tags=["Generation"])
async def generate_all(request: GenerateAllRequest):
    """Generate both blog post and tweet ideas for a week folder."""
    try:
        loader = _get_loader()
        docs = loader.load_week_folder(request.week_folder)
        
        if not docs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No documents found in week folder: {request.week_folder}"
            )
        
        llm = _get_llm()
        
        # Generate blog post
        blog_gen = BlogGenerator(llm)
        blog_output_path = f"output/{request.week_folder}/blog-post.md"
        blog_result = blog_gen.generate(docs, blog_output_path)
        
        blog_response = {
            "output_file": blog_result['output_file'],
            "citation_count": blog_result['fact_check']['citation_count'],
            "has_fact_check_issues": blog_result['fact_check']['has_issues'],
            "fact_check_issues": blog_result['fact_check'].get('issues', [])
        }
        
        if request.return_content:
            blog_file = Path(blog_result['output_file'])
            if blog_file.exists():
                blog_response['content'] = blog_file.read_text(encoding='utf-8')
        
        # Generate tweets
        tweet_gen = TweetGenerator(llm, count=request.tweet_count)
        tweet_output_dir = f"output/{request.week_folder}"
        tweet_result = tweet_gen.generate(docs, tweet_output_dir)
        
        tweet_response = {
            "json_file": tweet_result['json_file'],
            "txt_file": tweet_result['txt_file'],
            "tweet_count": tweet_result['tweet_count'],
            "has_fact_check_issues": tweet_result['fact_check']['has_issues'],
            "fact_check_issues": tweet_result['fact_check'].get('issues', [])
        }
        
        if request.return_content:
            import json
            json_file = Path(tweet_result['json_file'])
            if json_file.exists():
                data = json.loads(json_file.read_text(encoding='utf-8'))
                tweet_response['tweets'] = [TweetIdea(**tweet) for tweet in data.get('tweets', [])]
        
        return GenerateAllResponse(
            success=True,
            week_folder=request.week_folder,
            blog=blog_response,
            tweets=tweet_response,
            message="Blog post and tweet ideas generated successfully"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating content: {str(e)}"
        )


@app.get("/api/files/{week_folder}/blog-post", tags=["Files"])
async def get_blog_post_file(week_folder: str):
    """Download the generated blog post file."""
    file_path = Path(f"output/{week_folder}/blog-post.md")
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog post not found for week folder: {week_folder}"
        )
    return FileResponse(
        path=str(file_path),
        filename=f"blog-post-{week_folder}.md",
        media_type="text/markdown"
    )


@app.get("/api/files/{week_folder}/tweet-ideas", tags=["Files"])
async def get_tweet_ideas_file(week_folder: str, format: str = "json"):
    """Download the generated tweet ideas file."""
    if format == "json":
        file_path = Path(f"output/{week_folder}/tweet-ideas.json")
        media_type = "application/json"
        filename = f"tweet-ideas-{week_folder}.json"
    else:
        file_path = Path(f"output/{week_folder}/tweet-ideas.txt")
        media_type = "text/plain"
        filename = f"tweet-ideas-{week_folder}.txt"
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet ideas file not found for week folder: {week_folder}"
        )
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type=media_type
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

