from typing import Dict, Any
import os

class Config:
    # Text processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # FAISS settings
    EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
    FAISS_INDEX_PATH = os.path.join("data", "faiss_index")
    
    # Model settings
    MODEL_NAME = "gpt-3.5-turbo"
    TEMPERATURE = 0.7
    MAX_TOKENS = 500

config = Config()
