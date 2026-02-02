from typing import Optional

class TextSummarizer:
    def __init__(self):
        # Skip heavy model loading - use simple text summarization
        self.summarizer = None
        
    def _get_summarizer(self):
        """Skip model loading to avoid download issues"""
        return None
    
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 50) -> Optional[str]:
        """Generate a simple summary of the given text."""
        try:
            # Simple text summarization without ML models
            sentences = text.split('. ')
            
            # Take first few sentences as summary
            if len(sentences) <= 3:
                summary = '. '.join(sentences)
            else:
                # Take first 3 sentences for summary
                summary = '. '.join(sentences[:3]) + '.'
            
            # Truncate if too long
            if len(summary) > max_length * 2:
                summary = summary[:max_length * 2] + "..."
            
            return summary.strip()
            
        except Exception as e:
            print(f"Error in simple summarization: {e}")
            # Fallback: return first 200 characters
            return text[:200] + "..." if len(text) > 200 else text
    
    def summarize_website_content(self, contents: list) -> str:
        """Summarize multiple content pieces from a website."""
        if not contents:
            return "No content available to summarize."
        
        if len(contents) == 1:
            return self.summarize_text(contents[0])
        
        # Combine and summarize multiple pages
        combined_text = " ".join(contents)
        
        # For very long content, create a hierarchical summary
        if len(combined_text) > 2000:
            # First, summarize each page
            page_summaries = []
            for content in contents:
                page_summary = self.summarize_text(content, max_length=100, min_length=30)
                if page_summary:
                    page_summaries.append(page_summary)
            
            # Then summarize the summaries
            combined_summary = " ".join(page_summaries)
            return self.summarize_text(combined_summary, max_length=200, min_length=80)
        else:
            return self.summarize_text(combined_text, max_length=200, min_length=80)
