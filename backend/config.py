"""
Configuration settings for the RAG Chatbot application
"""
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    APP_TITLE: str = "RAG Chatbot API"
    APP_DESCRIPTION: str = "Professional RAG Chatbot with Ollama embeddings"
    APP_VERSION: str = "2.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8050
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    
    # Model Configuration
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1024
    
    EMBEDDING_MODEL: str = "nomic-embed-text"
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # RAG Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    RETRIEVAL_K: int = 4
    
    # File Storage
    TEMP_UPLOAD_DIR: Path = Path("temp_uploads")
    VECTORS_DIR: Path = Path("vectors")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".pdf"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Ensure directories exist
settings.TEMP_UPLOAD_DIR.mkdir(exist_ok=True)
settings.VECTORS_DIR.mkdir(exist_ok=True)
