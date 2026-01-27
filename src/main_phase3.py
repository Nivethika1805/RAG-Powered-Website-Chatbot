from chatbot.rag_chatbot import RAGChatbot

def main():
    """Demonstration of the reusable RAG chatbot system."""
    
    print("=== PHASE 3: REUSABLE & PLUG-AND-PLAY WEBSITE CHATBOT ===\n")
    
    # Initialize the chatbot
    chatbot = RAGChatbot()
    
    # Demo 1: Load from text
    print("📝 DEMO 1: Loading content from text")
    print("-" * 50)
    
    sample_text = """
    Python is a high-level, interpreted programming language known for its simplicity and readability.
    It was created by Guido van Rossum and first released in 1991. Python supports multiple programming
    paradigms including procedural, object-oriented, and functional programming. It has a large standard
    library and extensive third-party packages for data science, web development, machine learning, and more.
    Popular frameworks include Django, Flask, TensorFlow, and PyTorch. Python is widely used in
    artificial intelligence, scientific computing, web development, and automation.
    """
    
    if chatbot.load_from_text(sample_text, "Python Documentation"):
        print("✅ Successfully loaded text content")
        status = chatbot.get_status()
        print(f"Source: {status['source']}")
        print(f"Summary: {status['summary']}")
        
        # Test questions
        questions = [
            "What is Python?",
            "Who created Python?",
            "What are Python's popular frameworks?"
        ]
        
        print("\n🤖 Testing questions:")
        for q in questions:
            result = chatbot.ask(q)
            print(f"\nQ: {q}")
            print(f"A: {result['answer']}")
    
    print("\n" + "="*80 + "\n")
    
    # Demo 2: Load from URL (if internet is available)
    print("🌐 DEMO 2: Loading content from URL")
    print("-" * 50)
    
    # Using a simple, reliable URL
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    print(f"Attempting to load: {url}")
    
    if chatbot.load_from_url(url, max_pages=1):
        print("✅ Successfully loaded website content")
        status = chatbot.get_status()
        print(f"Source: {status['source']}")
        print(f"Summary: {status['summary'][:200]}...")
        
        # Test questions
        questions = [
            "When was Python created?",
            "What are the main features of Python?",
            "How is Python used in data science?"
        ]
        
        print("\n🤖 Testing questions:")
        for q in questions:
            result = chatbot.ask(q)
            print(f"\nQ: {q}")
            print(f"A: {result['answer'][:300]}...")
    
    print("\n" + "="*80 + "\n")
    
    # Demo 3: Interactive mode
    print("💬 DEMO 3: Interactive Chatbot Mode")
    print("-" * 50)
    print("Type 'quit' to exit, 'status' to check current status, 'clear' to clear content")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye! 👋")
                break
            elif user_input.lower() == 'status':
                status = chatbot.get_status()
                print(f"Status: {status}")
                continue
            elif user_input.lower() == 'clear':
                chatbot.clear_content()
                print("Content cleared. Load new content to continue.")
                continue
            elif user_input.lower().startswith('load '):
                # Simple command to load new text
                text = user_input[5:].strip()
                if text:
                    chatbot.load_from_text(text, "User Input")
                    print("Content loaded successfully!")
                    continue
            
            if user_input:
                result = chatbot.ask(user_input)
                print(f"\n🤖 Bot: {result['answer']}")
                
                if result['context']:
                    print(f"\n📚 Sources used: {len(result['context'])} relevant chunks")
        
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
