"""
Main FastAPI application for RAG Chatbot
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .config import settings
from .api.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["RAG Chatbot"])

# Mount frontend static files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/")
async def serve_frontend():
    """Serve the main HTML chatbot interface"""
    html_file = frontend_path / "index.html"
    if not html_file.exists():
        return {"message": "Frontend not found. Access API docs at /docs"}
    return FileResponse(html_file)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("=" * 60)
    logger.info("🚀 RAG Chatbot API Starting...")
    logger.info("=" * 60)
    logger.info(f"📁 Temp uploads: {settings.TEMP_UPLOAD_DIR}")
    logger.info(f"💾 Vectors storage: {settings.VECTORS_DIR}")
    logger.info(f"🔗 Ollama URL: {settings.OLLAMA_BASE_URL}")
    logger.info(f"🤖 Embedding model: {settings.EMBEDDING_MODEL}")
    logger.info(f"💡 LLM model: {settings.LLM_MODEL}")
    logger.info("=" * 60)
    
    # Test Ollama connection
    try:
        from backend.services.vector_service import vector_service
        test = vector_service.embeddings.embed_query("test")
        logger.info("✅ Ollama connection successful!")
    except Exception as e:
        logger.warning(f"⚠️  Warning: Could not connect to Ollama: {e}")
        logger.warning("   Make sure Ollama is running: 'ollama serve'")
        logger.warning(f"   And pull the model: 'ollama pull {settings.EMBEDDING_MODEL}'")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("🛑 RAG Chatbot API shutting down...")


if __name__ == "__main__":
    import uvicorn
    logger.info(f"\n🎯 Starting server on http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📖 API docs available at http://{settings.HOST}:{settings.PORT}/docs\n")
    
    # Check if running as module or direct
    import sys
    if sys.argv[0].endswith('__main__.py'):
        # Running as: python -m backend.main
        uvicorn.run(
            "backend.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=True
        )
    else:
        # Running as: python main.py
        uvicorn.run(
            app,
            host=settings.HOST,
            port=settings.PORT,
            reload=False
        )
