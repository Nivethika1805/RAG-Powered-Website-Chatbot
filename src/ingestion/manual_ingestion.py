from typing import List, Optional
from pathlib import Path
from processing.text_processor import TextProcessor
from processing.text_splitter import TextSplitter
from vector_store.faiss_store import FAISSStore
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import config

class ManualIngestor:
    def __init__(self):
        self.text_processor = None
        self.text_splitter = None
        self.vector_store = None
        
    def _get_components(self):
        """Lazy load components to avoid initialization issues"""
        if self.text_processor is None:
            self.text_processor = TextProcessor()
            self.text_splitter = TextSplitter(
                chunk_size=config.CHUNK_SIZE,
                chunk_overlap=config.CHUNK_OVERLAP
            )
            self.vector_store = FAISSStore(
                model_name=config.EMBEDDING_MODEL,
                index_path=config.FAISS_INDEX_PATH
            )
        return self.text_processor, self.text_splitter, self.vector_store
        
    def ingest_text(self, text: str) -> None:
        """Ingest and process a single text document."""
        # Get lazy loaded components
        text_processor, text_splitter, vector_store = self._get_components()
        
        # Process the text
        cleaned_text = text_processor.process_document(text)
        
        # Split into chunks
        chunks = text_splitter.split_text(cleaned_text)
        
        # Add to vector store
        vector_store.add_documents(chunks)
        
    def save_index(self, path: Optional[str] = None):
        """Save the vector store index."""
        _, _, vector_store = self._get_components()
        vector_store.save_index(path)
        
    def query(self, question: str, k: int = 3) -> List[str]:
        """Query the vector store for relevant chunks."""
        _, _, vector_store = self._get_components()
        return vector_store.similarity_search(question, k)
