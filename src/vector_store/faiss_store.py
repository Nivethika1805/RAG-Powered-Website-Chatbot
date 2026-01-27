import os
import numpy as np
import faiss
import torch
from sentence_transformers import SentenceTransformer
from typing import List, Optional, Tuple
from pathlib import Path

class FAISSStore:
    def __init__(self, model_name: str = None, index_path: str = None):
        # Initialize model with proper device handling to avoid meta tensor issues
        self.model_name = model_name or "sentence-transformers/all-mpnet-base-v2"
        self.model = None
        self.index = None
        self.index_path = index_path
        self.documents = []
        
    def _get_model(self):
        """Lazy load model to avoid initialization issues"""
        if self.model is None:
            try:
                print("Loading SentenceTransformer model...")
                # Force CPU device and avoid meta tensor issues
                self.model = SentenceTransformer(self.model_name, device='cpu')
                # Ensure model is properly initialized
                self.model.eval()
                print(f"Model loaded successfully: {self.model_name}")
                
                # Test the model with a simple embedding
                test_embedding = self.model.encode("test", device='cpu')
                print(f"Test embedding shape: {test_embedding.shape}")
                
            except Exception as e:
                print(f"Error loading model: {e}")
                import traceback
                traceback.print_exc()
                raise
        return self.model
        
    def _create_index(self, dimension: int):
        """Create a new FAISS index."""
        self.index = faiss.IndexFlatL2(dimension)
        
    def add_documents(self, texts: List[str]):
        """Add documents to the vector store."""
        if not texts:
            return
            
        # Generate embeddings using lazy loaded model
        model = self._get_model()
        embeddings = model.encode(texts, show_progress_bar=True, device='cpu')
        
        # Create index if it doesn't exist
        if self.index is None:
            self._create_index(embeddings.shape[1])
            
        # Add to FAISS index
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents.extend(texts)
        
    def score_sentences(self, query: str, sentences: List[str]) -> List[Tuple[float, str]]:
        """Score sentences using semantic similarity to the query."""
        if not sentences:
            return []
            
        model = self._get_model()
        query_embedding = model.encode([query], device='cpu')
        sentence_embeddings = model.encode(sentences, device='cpu')
        
        # Calculate cosine similarity (conceptually, L2 distance is used in FAISS, but cosine is often better for ranking)
        # normalize embeddings for cosine similarity
        query_norm = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        sentence_norms = sentence_embeddings / np.linalg.norm(sentence_embeddings, axis=1, keepdims=True)
        
        scores = np.dot(sentence_norms, query_norm.T).flatten()
        return sorted(zip(scores, sentences), key=lambda x: x[0], reverse=True)
        
    def similarity_search(self, query: str, k: int = 3) -> List[str]:
        """Search for similar documents."""
        if self.index is None:
            return []
            
        # Encode query using lazy loaded model
        model = self._get_model()
        query_embedding = model.encode([query], device='cpu')
        D, I = self.index.search(np.array(query_embedding).astype('float32'), k * 2) # Get more to allow for filtering
        
        # Return unique matching documents
        results = []
        seen = set()
        for i in I[0]:
            if i < len(self.documents):
                doc = self.documents[i]
                if doc not in seen:
                    results.append(doc)
                    seen.add(doc)
            if len(results) >= k:
                break
                
        return results
    
    def save_index(self, path: str = None):
        """Save the FAISS index and documents."""
        path = path or self.index_path
        if path and self.index is not None:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            faiss.write_index(self.index, f"{path}.index")
            with open(f"{path}.docs", "w", encoding="utf-8") as f:
                f.write("\n".join(self.documents))
    
    def load_index(self, path: str = None):
        """Load the FAISS index and documents."""
        path = path or self.index_path
        if path and os.path.exists(f"{path}.index"):
            self.index = faiss.read_index(f"{path}.index")
            if os.path.exists(f"{path}.docs"):
                with open(f"{path}.docs", "r", encoding="utf-8") as f:
                    self.documents = [line.strip() for line in f if line.strip()]
