import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from ingestion.automatic_ingestion import AutomaticIngestor

def main():
    ingestor = AutomaticIngestor()
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    
    print(f"Testing ingestion for {url}...")
    start_time = time.time()
    
    # This will trigger lazy loading of components including models
    summary, success = ingestor.ingest_website(url, max_pages=1)
    
    end_time = time.time()
    
    if success:
        print("\nSUCCESS!")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print("\nSummary generated:")
        print("-" * 50)
        print(summary)
        print("-" * 50)
    else:
        print("\nFAILED!")
        print(f"Error: {summary}")

if __name__ == "__main__":
    main()
