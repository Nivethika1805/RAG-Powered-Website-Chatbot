import re
from typing import List

class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and preprocess text with sensitivity to structure (bullets, colons, etc.)."""
        # Keep alphanumeric, spaces, and basic formatting symbols that preserve structure
        text = re.sub(r'[^\w\s.,!?-•:*]', ' ', text)
        
        # Remove extra whitespace while keeping paragraph breaks potentially useful
        text = re.sub(r'[ \t]+', ' ', text).strip()
        return text


    
    @staticmethod
    def process_document(text: str) -> str:
        """Process a single document."""
        return TextProcessor.clean_text(text)
