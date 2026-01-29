from typing import Optional, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import config

class TextSummarizer:
    def __init__(self):
        self.summarizer = None
        self.qa_pipeline = None
        
    def _get_qa_pipeline(self):
        """Lazy load the QA pipeline to avoid early overhead"""
        if self.qa_pipeline is None:
            try:
                from transformers import pipeline
                print(f"Initializing generative QA pipeline with {config.GENERATOR_MODEL}...")
                self.qa_pipeline = pipeline(
                    "text2text-generation", 
                    model=config.GENERATOR_MODEL,
                    device="cpu"
                )
            except Exception as e:
                print(f"Error loading QA model: {e}")
                return None
        return self.qa_pipeline
    
    def generate_answer(self, question: str, context: List[str]) -> Optional[str]:
        """Generate a synthesized answer from context using a local LLM."""
        pipeline = self._get_qa_pipeline()
        if not pipeline:
            return None
            
        try:
            # Combine context for the prompt
            combined_context = " ".join(context[:3]) # Limit context to avoid token issues
            # Stronger prompt with explicit instructions
            prompt = (
                f"Fact-Checking Task: Use the following knowledge base segments to answer the question. "
                f"Rule 1: Answer ONLY based on the provided context. "
                f"Rule 2: If the answer is not in the context, say 'I don't have enough information about that.' "
                f"Evidence: {combined_context} "
                f"Query: {question} "
                f"Synthesized Answer:"
            )
            
            result = pipeline(prompt, max_length=150, min_length=30, do_sample=False, temperature=0.3)

            return result[0]['generated_text'].strip()

        except Exception as e:
            print(f"Error in generative QA: {e}")
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
            
            return summary.strip() if summary else "No summary available."
            
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

