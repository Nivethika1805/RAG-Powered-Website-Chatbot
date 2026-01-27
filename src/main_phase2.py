from ingestion.automatic_ingestion import AutomaticIngestor

def main():
    # Initialize the automatic ingestor
    ingestor = AutomaticIngestor()
    
    # Example website URLs to test
    test_urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://www.ibm.com/cloud/learn/what-is-artificial-intelligence",
        "https://www.techtarget.com/searchenterpriseai/definition/AI-Artificial-Intelligence"
    ]
    
    print("=== PHASE 2: AUTOMATIC WEBSITE CONTENT INGESTION & AI SUMMARIZATION ===\n")
    
    # Test with the first URL
    url = test_urls[0]
    print(f"Testing with URL: {url}")
    print("-" * 80)
    
    # Ingest the website
    summary, success = ingestor.ingest_website(url, max_pages=2)
    
    if success:
        print("\n📄 WEBSITE SUMMARY:")
        print("=" * 50)
        print(summary)
        print("=" * 50)
        
        # Test queries
        test_queries = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "What are the applications of AI?"
        ]
        
        print("\n🔍 TESTING QUERIES:")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            results = ingestor.query(query, k=2)
            
            for i, result in enumerate(results, 1):
                print(f"\nResult {i}:")
                print(result[:300] + "..." if len(result) > 300 else result)
        
        print("\n✅ Phase 2 completed successfully!")
        
    else:
        print(f"❌ Failed to ingest website: {summary}")

if __name__ == "__main__":
    main()
