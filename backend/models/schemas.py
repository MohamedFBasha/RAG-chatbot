"""
Pydantic models for request and response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    prompt: str = Field(..., min_length=1, max_length=5000, description="User's question")
    session_id: str = Field(..., min_length=5, description="Unique session identifier")
    
    @validator('prompt')
    def prompt_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Prompt cannot be empty or whitespace')
        return v.strip()
    
    @validator('session_id')
    def validate_session_format(cls, v):
        if not (v.startswith('session_') or v.startswith('portfolio_')):
            raise ValueError('Session ID must start with "session_" or "portfolio_"')
        return v


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str = Field(..., description="AI generated answer")
    sources: Optional[List[str]] = Field(default=None, description="Source documents")
    session_id: str = Field(..., description="Session identifier")


class UploadResponse(BaseModel):
    """Response model for PDF upload endpoint"""
    message: str
    filename: str
    pages: int
    chunks: int
    session_id: str


class SessionInfo(BaseModel):
    """Session information response"""
    session_id: str
    pdf_info: Optional[dict] = None
    message_count: int
    has_vectorstore: bool


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    ollama_status: str
    embedding_model: str
    llm_model: str
    active_sessions: int


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    error_type: Optional[str] = None
