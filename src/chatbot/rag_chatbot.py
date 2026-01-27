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
            # Clear previous content safely
            self.manual_ingestor.clear_index()
            
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
        """
        try:
            # Check if this URL is already loaded to avoid redundant work
            if self.current_source == url and self.auto_ingestor.vector_store and self.auto_ingestor.vector_store.index is not None:
                print(f"URL already loaded: {url}")
                return True

            # Clear previous content before starting new ingestion
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
        Generate a synthesized answer from context using a local LLM or semantic ranking.
        """
        if not context:
            return "I couldn't find any relevant information to help with that."
        
        # 1. Attempt Generative QA (Synthesized Answer)
        try:
            generative_answer = self.summarizer.generate_answer(question, context)
            if generative_answer and len(generative_answer) > 20:
                return f"{generative_answer}\n\n*This answer was intelligently synthesized by the knowledge assistant based on the retrieved context.*"
        except Exception as e:
            print(f"Generative QA failed: {e}")

        # 2. Fallback: Semantic Sentence Ranking (from previous implementation)
        ingestor = self.auto_ingestor if "http" in self.current_source else self.manual_ingestor
        _, _, vector_store = ingestor._get_components()
        
        all_sentences = []
        for chunk in context:
            content = chunk.replace('\n', ' ').strip()
            import re
            sentences = re.split(r'(?<=[.!?])\s+', content)
            all_sentences.extend([s.strip() for s in sentences if len(s.strip()) > 15])
            
        if not all_sentences:
            return f"{context[0]}\n\n*I've picked the most relevant section for you.*"
            
        scored_sentences = vector_store.score_sentences(question, all_sentences)
        
        if scored_sentences:
            best_sentences = []
            seen = set()
            threshold = 0.35
            
            for score, sentence in scored_sentences:
                cleaned = sentence.strip().lower()
                if cleaned not in seen and score > threshold:
                    best_sentences.append(sentence)
                    seen.add(cleaned)
                if len(best_sentences) >= 3:
                    break
            
            if best_sentences:
                main_answer = " ".join(best_sentences)
                if not main_answer.endswith(('.', '!', '?')):
                    main_answer += "."
                return f"{main_answer}\n\n*I've analyzed the knowledge base and extracted these specific details for you.*"
        
        return f"{context[0]}\n\n*This section from the context seems the most relevant.*"

    
    def get_status(self) -> Dict[str, Any]:
        """Get current chatbot status."""
        return {
            "loaded": self.current_source is not None,
            "source": self.current_source,
            "summary": self.current_summary
        }
    
    def clear_content(self):
        """Clear all loaded content."""
        self.manual_ingestor.clear_index()
        self.auto_ingestor.clear_index()
        self.current_source = None
        self.current_summary = None
