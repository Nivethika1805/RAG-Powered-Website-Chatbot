import re
from typing import List

class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and preprocess text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters (keep alphanumeric, spaces, and basic punctuation)
        text = re.sub(r'[^\w\s.,!?]', '', text)
        return text
    
    @staticmethod
    def process_document(text: str) -> str:
        """Process a single document."""
        return TextProcessor.clean_text(text)
