from typing import List, Optional, Tuple, Dict, Any
from ingestion.manual_ingestion import ManualIngestor
from ingestion.automatic_ingestion import AutomaticIngestor
from processing.summarizer import TextSummarizer
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import config

class RAGChatbot:
    """
    Reusable RAG-powered chatbot that can work with any website content.
    """
    
    def __init__(self):
        self.manual_ingestor = ManualIngestor()
        self.auto_ingestor = AutomaticIngestor()
        self.summarizer = TextSummarizer()
        self.current_source = None
        self.current_summary = None
        
    def load_from_text(self, text: str, source_name: str = "Manual Text") -> bool:
        """
        Load content from raw text.
        
        Args:
            text: Raw text content
            source_name: Name identifier for the content source
            
        Returns:
            bool: Success status
        """
        try:
            # Clear previous content
            self.manual_ingestor.vector_store = self.manual_ingestor.vector_store.__class__(
                model_name=config.EMBEDDING_MODEL,
                index_path=config.FAISS_INDEX_PATH
            )
            
            # Ingest new content
            self.manual_ingestor.ingest_text(text)
            self.manual_ingestor.save_index()
            
            self.current_source = source_name
            self.current_summary = f"Loaded {len(text)} characters of text from {source_name}"
            
            return True
            
        except Exception as e:
            print(f"Error loading text: {e}")
            return False
    
    def load_from_url(self, url: str, max_pages: int = 3) -> bool:
        """
        Load content from a website URL.
        
        Args:
            url: Website URL to load
            max_pages: Maximum number of pages to scrape
            
        Returns:
            bool: Success status
        """
        try:
            # Clear previous content
            self.auto_ingestor.clear_index()
            
            # Ingest website content
            summary, success = self.auto_ingestor.ingest_website(url, max_pages)
            
            if success:
                self.current_source = url
                self.current_summary = summary
                return True
            else:
                print(f"Failed to load from URL: {summary}")
                return False
                
        except Exception as e:
            print(f"Error loading from URL: {e}")
            return False
    
    def ask(self, question: str, k: int = 3) -> Dict[str, Any]:
        """
        Ask a question to the chatbot.
        
        Args:
            question: User's question
            k: Number of relevant chunks to retrieve
            
        Returns:
            Dict containing answer and context
        """
        if not self.current_source:
            return {
                "answer": "No content loaded. Please load content first using load_from_text() or load_from_url().",
                "context": [],
                "source": None,
                "summary": None
            }
        
        try:
            # Get relevant chunks
            if "http" in self.current_source:
                context = self.auto_ingestor.query(question, k)
            else:
                context = self.manual_ingestor.query(question, k)
            
            if not context:
                return {
                    "answer": "I couldn't find relevant information in the loaded content to answer your question.",
                    "context": [],
                    "source": self.current_source,
                    "summary": self.current_summary
                }
            
            # Generate answer based on context
            answer = self._generate_answer(question, context)
            
            return {
                "answer": answer,
                "context": context,
                "source": self.current_source,
                "summary": self.current_summary
            }
            
        except Exception as e:
            return {
                "answer": f"Error processing question: {str(e)}",
                "context": [],
                "source": self.current_source,
                "summary": self.current_summary
            }
    
    def _generate_answer(self, question: str, context: List[str]) -> str:
        """
        Generate an answer based on the retrieved context.
        This is a simple implementation - in production, you'd use an LLM here.
        """
        if not context:
            return "I don't have enough information to answer that question."
        
        # Simple answer generation based on context
        # In a real implementation, you'd use an LLM like GPT-3/4
        combined_context = " ".join(context)
        
        # For now, return the most relevant chunk
        if context:
            return f"Based on the loaded content: {context[0][:500]}..."
        
        return "I found some relevant information but couldn't generate a complete answer."
    
    def get_status(self) -> Dict[str, Any]:
        """Get current chatbot status."""
        return {
            "loaded": self.current_source is not None,
            "source": self.current_source,
            "summary": self.current_summary
        }
    
    def clear_content(self):
        """Clear all loaded content."""
        self.manual_ingestor.vector_store = self.manual_ingestor.vector_store.__class__(
            model_name=config.EMBEDDING_MODEL,
            index_path=config.FAISS_INDEX_PATH
        )
        self.auto_ingestor.clear_index()
        self.current_source = None
        self.current_summary = None
