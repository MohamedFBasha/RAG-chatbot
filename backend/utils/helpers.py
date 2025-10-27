"""
Utility helper functions for the application
"""
import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
import logging

logger = logging.getLogger(__name__)


def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format
    
    Args:
        session_id: Session identifier to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not session_id or len(session_id) < 5:
        return False
    return session_id.startswith("session_") or session_id.startswith("portfolio_")


def generate_session_id() -> str:
    """
    Generate a unique session ID
    
    Returns:
        str: Unique session identifier
    """
    return f"session_{uuid.uuid4().hex[:12]}"


def cleanup_temp_file(file_path: str) -> None:
    """
    Safely delete temporary file
    
    Args:
        file_path: Path to file to delete
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up temp file: {file_path}")
    except Exception as e:
        logger.warning(f"Could not delete temp file {file_path}: {e}")


async def validate_pdf_upload(file: UploadFile, max_size: int = 10 * 1024 * 1024) -> None:
    """
    Validate uploaded PDF file
    
    Args:
        file: Uploaded file
        max_size: Maximum file size in bytes (default 10MB)
        
    Raises:
        HTTPException: If validation fails
    """
    # Check file extension
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {max_size / (1024*1024):.1f}MB"
        )
    
    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )


async def save_upload_file(upload_file: UploadFile, destination: Path) -> Path:
    """
    Save uploaded file to destination
    
    Args:
        upload_file: File to save
        destination: Destination path
        
    Returns:
        Path: Path to saved file
        
    Raises:
        HTTPException: If save fails
    """
    try:
        with open(destination, "wb") as buffer:
            content = await upload_file.read()
            buffer.write(content)
        logger.info(f"Saved file to: {destination}")
        return destination
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save uploaded file: {str(e)}"
        )


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}TB"
