from typing import List, Optional, Tuple
from processing.text_processor import TextProcessor
from processing.text_splitter import TextSplitter
from processing.summarizer import TextSummarizer
from vector_store.faiss_store import FAISSStore
from .web_scraper import WebScraper
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import config

class AutomaticIngestor:
    def __init__(self):
        self.web_scraper = None
        self.text_processor = None
        self.text_splitter = None
        self.summarizer = None
        self.vector_store = None
        
    def _get_components(self):
        """Lazy load components to avoid initialization issues"""
        if self.web_scraper is None:
            self.web_scraper = WebScraper()
            self.text_processor = TextProcessor()
            self.text_splitter = TextSplitter(
                chunk_size=config.CHUNK_SIZE,
                chunk_overlap=config.CHUNK_OVERLAP
            )
            self.summarizer = TextSummarizer()
            self.vector_store = FAISSStore(
                model_name=config.EMBEDDING_MODEL,
                index_path=config.FAISS_INDEX_PATH
            )
        return self.web_scraper, self.text_processor, self.text_splitter, self.summarizer, self.vector_store
        
    def ingest_website(self, url: str, max_pages: int = 3) -> Tuple[str, bool]:
        """
        Ingest website content automatically.
        
        Args:
            url: Website URL to ingest
            max_pages: Maximum number of pages to scrape
            
        Returns:
            Tuple of (summary, success_status)
        """
        try:
            # Get lazy loaded components
            web_scraper, text_processor, text_splitter, summarizer, vector_store = self._get_components()
            
            print(f"Starting website ingestion for: {url}")
            
            # Scrape website content
            print("Step 1: Scraping website content...")
            contents = web_scraper.scrape_multiple_pages(url, max_pages)
            
            if not contents:
                error_msg = "Failed to scrape website content. Please check the URL and try again."
                print(error_msg)
                return error_msg, False
            
            print(f"Step 1 Complete: Successfully scraped {len(contents)} page(s)")
            
            # Process and combine all content
            all_processed_text = ""
            all_chunks = []
            
            print("Step 2: Processing and chunking content...")
            for i, content in enumerate(contents):
                print(f"Processing page {i+1}...")
                
                # Clean the text
                processed_text = text_processor.process_document(content)
                all_processed_text += processed_text + "\n\n"
                
                # Split into chunks
                chunks = text_splitter.split_text(processed_text)
                all_chunks.extend(chunks)
                print(f"Page {i+1}: Created {len(chunks)} chunks")
            
            print(f"Step 2 Complete: Total {len(all_chunks)} text chunks created")
            
            # Generate summary
            print("Step 3: Generating AI summary...")
            try:
                summary = summarizer.summarize_website_content(contents)
                print(f"Step 3 Complete: Summary generated ({len(summary)} characters)")
            except Exception as e:
                print(f"Warning: Summary generation failed: {e}")
                summary = f"Successfully processed {len(contents)} pages with {len(all_chunks)} content chunks. Unable to generate AI summary due to processing error."
            
            # Add to vector store
            print("Step 4: Creating vector embeddings...")
            try:
                vector_store.add_documents(all_chunks)
                print("Step 4 Complete: Vector embeddings created")
                
                # Test the vector store immediately
                test_results = vector_store.similarity_search("test", k=1)
                print(f"Vector store test: Found {len(test_results)} results for test query")
                
            except Exception as e:
                print(f"Error creating embeddings: {e}")
                import traceback
                traceback.print_exc()
                return f"Error creating embeddings: {str(e)}", False
            
            # Save the index
            print("Step 5: Saving index...")
            try:
                self.save_index()
                print("Step 5 Complete: Index saved")
            except Exception as e:
                print(f"Warning: Failed to save index: {e}")
            
            print(f"SUCCESS: Website ingestion completed! Processed {len(all_chunks)} text chunks")
            
            return summary, True
            
        except Exception as e:
            error_msg = f"Error during website ingestion: {str(e)}"
            print(error_msg)
            return error_msg, False
    
    def save_index(self, path: Optional[str] = None):
        """Save the vector store index."""
        _, _, _, _, vector_store = self._get_components()
        vector_store.save_index(path)
        
    def query(self, question: str, k: int = 3) -> List[str]:
        """Query the vector store for relevant chunks."""
        print(f"Querying for: '{question}' with k={k}")
        try:
            _, _, _, _, vector_store = self._get_components()
            
            # Check if vector store has content
            if vector_store.index is None:
                print("Vector store index is None - no content loaded")
                return []
            
            if len(vector_store.documents) == 0:
                print("Vector store has no documents")
                return []
            
            print(f"Vector store has {len(vector_store.documents)} documents")
            
            results = vector_store.similarity_search(question, k)
            print(f"Query returned {len(results)} results")
            
            return results
        except Exception as e:
            print(f"Error in query: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def ingest_url(self, url: str, max_pages: int = 3) -> str:
        """
        Ingest website content automatically (alias for ingest_website).
        
        Args:
            url: Website URL to ingest
            max_pages: Maximum number of pages to scrape
            
        Returns:
            Summary if successful, error message if failed
        """
        summary, success = self.ingest_website(url, max_pages)
        if success:
            return summary
        else:
            raise Exception(summary)
    
    def clear_index(self):
        """Clear the current vector store."""
        self.vector_store = FAISSStore(
            model_name=config.EMBEDDING_MODEL,
            index_path=config.FAISS_INDEX_PATH
        )
