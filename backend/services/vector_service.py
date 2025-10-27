"""
Vector store service for PDF processing and retrieval
"""
from pathlib import Path
from typing import Dict, List, Tuple
import logging

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema import Document

from backend.config import settings

logger = logging.getLogger(__name__)


class VectorStoreService:
    """Service for managing vector stores"""
    
    def __init__(self):
        """Initialize the vector store service"""
        self.embeddings = OllamaEmbeddings(
            model=settings.EMBEDDING_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )
        self.vectorstore_cache: Dict[str, FAISS] = {}
        self.session_metadata: Dict[str, dict] = {}
        
        logger.info(f"VectorStoreService initialized with model: {settings.EMBEDDING_MODEL}")
    
    async def process_pdf(self, pdf_path: str, session_id: str) -> Tuple[int, int]:
        """
        Process PDF file and create vector store
        
        Args:
            pdf_path: Path to PDF file
            session_id: Session identifier
            
        Returns:
            Tuple[int, int]: Number of pages and chunks
            
        Raises:
            Exception: If processing fails
        """
        try:
            # Load PDF
            logger.info(f"Loading PDF: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            if not documents:
                raise ValueError("PDF contains no readable text")
            
            num_pages = len(documents)
            logger.info(f"Loaded {num_pages} pages from PDF")
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            splits = text_splitter.split_documents(documents)
            num_chunks = len(splits)
            
            logger.info(f"Split into {num_chunks} chunks")
            
            # Create vectorstore with embeddings
            logger.info("Creating embeddings...")
            vectorstore = FAISS.from_documents(splits, self.embeddings)
            
            # Save to disk
            vectorstore_path = settings.VECTORS_DIR / session_id
            vectorstore_path.mkdir(exist_ok=True)
            vectorstore.save_local(str(vectorstore_path))
            
            # Cache in memory
            self.vectorstore_cache[session_id] = vectorstore
            
            # Store metadata
            self.session_metadata[session_id] = {
                "pages": num_pages,
                "chunks": num_chunks
            }
            
            logger.info(f"Successfully processed PDF for session {session_id}")
            
            return num_pages, num_chunks
            
        except Exception as e:
            logger.error(f"Failed to process PDF: {str(e)}")
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def get_vectorstore(self, session_id: str) -> FAISS:
        """
        Get or load vectorstore for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            FAISS: Vector store instance
            
        Raises:
            ValueError: If vectorstore not found
        """
        # Check cache first
        if session_id in self.vectorstore_cache:
            logger.info(f"Retrieved vectorstore from cache for session {session_id}")
            return self.vectorstore_cache[session_id]
        
        # Try loading from disk
        vectorstore_path = settings.VECTORS_DIR / session_id
        
        if not vectorstore_path.exists():
            raise ValueError(f"No vectorstore found for session {session_id}")
        
        try:
            logger.info(f"Loading vectorstore from disk for session {session_id}")
            vectorstore = FAISS.load_local(
                str(vectorstore_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
            # Cache for future use
            self.vectorstore_cache[session_id] = vectorstore
            
            return vectorstore
            
        except Exception as e:
            logger.error(f"Failed to load vectorstore: {str(e)}")
            raise ValueError(f"Failed to load vectorstore: {str(e)}")
    
    def has_vectorstore(self, session_id: str) -> bool:
        """
        Check if vectorstore exists for session
        
        Args:
            session_id: Session identifier
            
        Returns:
            bool: True if exists, False otherwise
        """
        return (session_id in self.vectorstore_cache or 
                (settings.VECTORS_DIR / session_id).exists())
    
    def delete_vectorstore(self, session_id: str) -> None:
        """
        Delete vectorstore for a session
        
        Args:
            session_id: Session identifier
        """
        # Remove from cache
        if session_id in self.vectorstore_cache:
            del self.vectorstore_cache[session_id]
        
        if session_id in self.session_metadata:
            del self.session_metadata[session_id]
        
        # Remove from disk
        vectorstore_path = settings.VECTORS_DIR / session_id
        if vectorstore_path.exists():
            import shutil
            shutil.rmtree(vectorstore_path)
            logger.info(f"Deleted vectorstore for session {session_id}")
    
    def get_metadata(self, session_id: str) -> dict:
        """
        Get metadata for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            dict: Session metadata
        """
        return self.session_metadata.get(session_id, {})
    
    def get_active_sessions(self) -> int:
        """
        Get number of active sessions
        
        Returns:
            int: Number of active sessions
        """
        return len(self.vectorstore_cache)


# Global instance
vector_service = VectorStoreService()
