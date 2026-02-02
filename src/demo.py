"""
Complete RAG Chatbot Demo - All Phases
This script demonstrates all three phases of the RAG chatbot system.
"""

def show_menu():
    """Display the main menu."""
    print("\n" + "="*60)
    print("RAG-POWERED WEBSITE CHATBOT SYSTEM")
    print("="*60)
    print("1. Phase 1: Manual Text Ingestion & Query")
    print("2. Phase 2: Automatic Website Ingestion & Summarization")
    print("3. Phase 3: Interactive Reusable Chatbot")
    print("4. Quick Demo (All Phases)")
    print("5. Exit")
    print("-"*60)

def phase1_demo():
    """Run Phase 1 demonstration."""
    print("\nPHASE 1: MANUAL TEXT INGESTION")
    print("-"*40)
    
    from ingestion.manual_ingestion import ManualIngestor
    
    ingestor = ManualIngestor()
    
    # Sample text about machine learning
    text = """
    Machine Learning is a subset of artificial intelligence that enables systems to learn and improve
    from experience without being explicitly programmed. It focuses on developing computer programs
    that can access data and use it to learn for themselves. The process of learning begins with
    observations or data, such as examples, direct experience, or instruction, in order to look for
    patterns in data and make better decisions in the future based on the examples that we provide.
    
    The main types of machine learning are:
    1. Supervised Learning: Learning with labeled data
    2. Unsupervised Learning: Learning with unlabeled data
    3. Reinforcement Learning: Learning through rewards and punishments
    
    Common applications include image recognition, natural language processing, recommendation systems,
    and autonomous vehicles.
    """
    
    print("Ingesting text about Machine Learning...")
    ingestor.ingest_text(text)
    ingestor.save_index()
    
    # Test queries
    queries = ["What is machine learning?", "What are the types of ML?", "What are ML applications?"]
    
    for query in queries:
        print(f"\nQuery: {query}")
        results = ingestor.query(query, k=2)
        for i, result in enumerate(results, 1):
            print(f"  Result {i}: {result[:200]}...")
    
    input("\nPress Enter to continue...")

def phase2_demo():
    """Run Phase 2 demonstration."""
    print("\nPHASE 2: AUTOMATIC WEBSITE INGESTION")
    print("-"*40)
    
    from ingestion.automatic_ingestion import AutomaticIngestor
    
    ingestor = AutomaticIngestor()
    
    # Use a reliable website for demo
    url = "https://en.wikipedia.org/wiki/Machine_learning"
    print(f"Scraping website: {url}")
    
    summary, success = ingestor.ingest_website(url, max_pages=1)
    
    if success:
        print("\nAI-Generated Summary:")
        print("-"*30)
        print(summary)
        
        # Test queries
        queries = ["What is machine learning?", "How does ML work?"]
        
        print("\nTESTING QUERIES:")
        for query in queries:
            print(f"\nQuery: {query}")
            results = ingestor.query(query, k=2)
            for i, result in enumerate(results, 1):
                print(f"  Result {i}: {result[:200]}...")
    else:
        print(f"Failed: {summary}")
    
    input("\nPress Enter to continue...")

def phase3_demo():
    """Run Phase 3 demonstration."""
    print("\nPHASE 3: INTERACTIVE REUSABLE CHATBOT")
    print("-"*40)
    
    from chatbot.rag_chatbot import RAGChatbot
    
    chatbot = RAGChatbot()
    
    # Load some content
    ai_text = """
    Artificial Intelligence (AI) refers to the simulation of human intelligence in machines
    that are programmed to think and learn. It is a broad field of computer science that includes
    machine learning, neural networks, natural language processing, computer vision, and robotics.
    
    AI applications include:
    - Virtual assistants (Siri, Alexa)
    - Recommendation systems (Netflix, Amazon)
    - Autonomous vehicles
    - Medical diagnosis
    - Financial trading
    - Game playing (Chess, Go)
    """
    
    chatbot.load_from_text(ai_text, "AI Overview")
    print("Loaded AI content")
    
    # Interactive chat
    print("\nAsk questions about AI (type 'quit' to exit):")
    
    while True:
        question = input("\nYou: ").strip()
        if question.lower() == 'quit':
            break
        
        result = chatbot.ask(question)
        print(f"\nBot: {result['answer']}")
    
    input("\nPress Enter to continue...")

def quick_demo():
    """Run a quick demo of all phases."""
    print("\nQUICK DEMO - ALL PHASES")
    print("-"*40)
    
    # Phase 1
    print("\n1. Phase 1: Manual Ingestion")
    from ingestion.manual_ingestion import ManualIngestor
    ingestor = ManualIngestor()
    ingestor.ingest_text("Data Science combines statistics, programming, and domain knowledge.")
    results = ingestor.query("What is data science?")
    print(f"   Result: {results[0][:100]}...")
    
    # Phase 2
    print("\n2. Phase 2: Auto Ingestion (simulated)")
    print("   Would scrape website and generate summary...")
    
    # Phase 3
    print("\n3. Phase 3: Reusable Chatbot")
    from chatbot.rag_chatbot import RAGChatbot
    chatbot = RAGChatbot()
    chatbot.load_from_text("Blockchain is a distributed ledger technology.", "Blockchain Info")
    result = chatbot.ask("What is blockchain?")
    print(f"   Answer: {result['answer'][:100]}...")
    
    print("\nAll phases demonstrated!")
    input("\nPress Enter to continue...")

def main():
    """Main demo function."""
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                phase1_demo()
            elif choice == '2':
                phase2_demo()
            elif choice == '3':
                phase3_demo()
            elif choice == '4':
                quick_demo()
            elif choice == '5':
                print("\nThank you for using the RAG Chatbot System!")
                break
            else:
                print("Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
