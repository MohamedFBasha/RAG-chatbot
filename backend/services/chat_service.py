"""
Chat service for RAG-based conversations
"""
from typing import Dict, List, Tuple
import logging

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq

from backend.config import settings
from backend.services.vector_service import vector_service

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing chat conversations with RAG"""
    
    def __init__(self):
        """Initialize the chat service"""
        self.llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS
        )
        self.session_store: Dict[str, BaseChatMessageHistory] = {}
        
        logger.info(f"ChatService initialized with model: {settings.LLM_MODEL}")
    
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """
        Get or create chat message history for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            BaseChatMessageHistory: Chat history for the session
        """
        if session_id not in self.session_store:
            self.session_store[session_id] = ChatMessageHistory()
            logger.info(f"Created new chat history for session {session_id}")
        return self.session_store[session_id]
    
    async def chat(self, prompt: str, session_id: str) -> Tuple[str, List[str]]:
        """
        Process chat message with RAG
        
        Args:
            prompt: User's question
            session_id: Session identifier
            
        Returns:
            Tuple[str, List[str]]: Answer and source documents
            
        Raises:
            ValueError: If no vectorstore exists for session
            Exception: If chat processing fails
        """
        try:
            # Get vectorstore
            vectorstore = vector_service.get_vectorstore(session_id)
            
            # Create retriever
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": settings.RETRIEVAL_K}
            )
            
            # Create context-aware query reformulation
            contextualize_q_prompt = ChatPromptTemplate.from_messages([
                ("system", 
                 "Given a chat history and the latest user question which might reference "
                 "context in the chat history, formulate a standalone question which can be "
                 "understood without the chat history. Do NOT answer the question, just "
                 "reformulate it if needed and otherwise return it as is."),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            
            history_aware_retriever = create_history_aware_retriever(
                self.llm, retriever, contextualize_q_prompt
            )
            
            # Create answer generation chain
            qa_prompt = ChatPromptTemplate.from_messages([
                ("system",
                 "You are a helpful AI assistant. Use the following context from the uploaded PDF "
                 "to answer the user's question accurately and concisely.\n\n"
                 "Important guidelines:\n"
                 "- If the answer is in the context, provide a clear and detailed response\n"
                 "- If you're unsure or the information isn't in the context, say so honestly\n"
                 "- Use bullet points or numbered lists when appropriate for clarity\n"
                 "- Cite specific sections when relevant\n\n"
                 "Context:\n{context}"),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            
            document_chain = create_stuff_documents_chain(self.llm, qa_prompt)
            rag_chain = create_retrieval_chain(history_aware_retriever, document_chain)
            
            # Combine with conversation memory
            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain,
                self.get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )
            
            logger.info(f"Processing chat for session {session_id}")
            
            # Generate response
            response = conversational_rag_chain.invoke(
                {"input": prompt},
                config={"configurable": {"session_id": session_id}},
            )
            
            answer = response["answer"]
            
            # Extract source documents
            sources = []
            if "context" in response and response["context"]:
                sources = [
                    f"Page {doc.metadata.get('page', 'Unknown')}" 
                    for doc in response["context"][:3]
                ]
            
            logger.info(f"Generated response for session {session_id}")
            
            return answer, sources
            
        except ValueError as e:
            logger.error(f"Vectorstore error: {str(e)}")
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Chat processing failed: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def clear_history(self, session_id: str) -> None:
        """
        Clear chat history for a session
        
        Args:
            session_id: Session identifier
        """
        if session_id in self.session_store:
            self.session_store[session_id] = ChatMessageHistory()
            logger.info(f"Cleared chat history for session {session_id}")
    
    def delete_session(self, session_id: str) -> None:
        """
        Delete session from chat service
        
        Args:
            session_id: Session identifier
        """
        if session_id in self.session_store:
            del self.session_store[session_id]
            logger.info(f"Deleted session {session_id} from chat service")
    
    def get_message_count(self, session_id: str) -> int:
        """
        Get number of messages in session history
        
        Args:
            session_id: Session identifier
            
        Returns:
            int: Number of messages
        """
        if session_id not in self.session_store:
            return 0
        return len(self.session_store[session_id].messages)
    
    def session_exists(self, session_id: str) -> bool:
        """
        Check if session exists
        
        Args:
            session_id: Session identifier
            
        Returns:
            bool: True if exists, False otherwise
        """
        return session_id in self.session_store


# Global instance
chat_service = ChatService()
