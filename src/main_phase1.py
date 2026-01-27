from ingestion.manual_ingestion import ManualIngestor

def main():
    # Initialize the ingestor
    ingestor = ManualIngestor()
    
    # Example website content (in practice, this would be loaded from a file or input)
    sample_text = """
    Artificial Intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural 
    intelligence displayed by animals including humans. AI research has been defined as the field of 
    study of intelligent agents, which refers to any system that perceives its environment and takes 
    actions that maximize its chance of achieving its goals.
    
    Machine learning (ML) is the study of computer algorithms that improve automatically through 
    experience and by the use of data. It is seen as a part of artificial intelligence.
    """
    
    # Ingest the text
    print("Ingesting text...")
    ingestor.ingest_text(sample_text)
    
    # Save the index
    ingestor.save_index()
    
    # Test query
    query = "What is AI?"
    print(f"\nQuery: {query}")
    results = ingestor.query(query)
    
    print("\nRelevant chunks:")
    for i, result in enumerate(results, 1):
        print(f"\nChunk {i}:")
        print(result)

if __name__ == "__main__":
    main()
