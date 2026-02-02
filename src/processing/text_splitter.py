from typing import List

class TextSplitter:
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or 1000
        self.chunk_overlap = chunk_overlap or 200
        
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap."""
        if len(text) <= self.chunk_size:
            return [text]
            
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # If this is the last chunk, take whatever remains
            if end >= len(text):
                chunks.append(text[start:])
                break
                
            # Try to find a good breaking point (sentence or paragraph)
            chunk = text[start:end]
            
            # Look for sentence endings
            sentence_end = max(
                chunk.rfind('. '),
                chunk.rfind('! '),
                chunk.rfind('? '),
                chunk.rfind('\n\n')
            )
            
            if sentence_end > self.chunk_size * 0.7:  # Only break if we have enough content
                end = start + sentence_end + 2
                chunk = text[start:end]
            
            chunks.append(chunk)
            start = end - self.chunk_overlap
            
        return [chunk.strip() for chunk in chunks if chunk.strip()]
