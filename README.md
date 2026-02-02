# RAG-Powered Website Chatbot

A complete, modular Retrieval-Augmented Generation (RAG) chatbot system for website content with three implementation phases.

## 🚀 Features

- **Phase 1**: Manual text ingestion and similarity search
- **Phase 2**: Automatic website scraping and AI summarization  
- **Phase 3**: Reusable, plug-and-play chatbot system
- **FAISS Vector Storage**: Efficient similarity search
- **Hugging Face Models**: Text summarization and embeddings
- **Modular Architecture**: Easy to extend and customize

## 📁 Project Structure

```
rag_chatbot/
├── config/
│   └── config.py              # Configuration settings
├── data/
│   └── raw/                   # Raw data storage
├── src/
│   ├── ingestion/             # Data ingestion modules
│   │   ├── manual_ingestion.py
│   │   ├── automatic_ingestion.py
│   │   └── web_scraper.py
│   ├── processing/            # Text processing modules
│   │   ├── text_processor.py
│   │   ├── text_splitter.py
│   │   └── summarizer.py
│   ├── vector_store/          # Vector storage modules
│   │   └── faiss_store.py
│   ├── chatbot/               # Reusable chatbot system
│   │   └── rag_chatbot.py
│   ├── utils/                 # Utility functions
│   ├── main_phase1.py         # Phase 1 demo
│   ├── main_phase2.py         # Phase 2 demo
│   ├── main_phase3.py         # Phase 3 demo
│   └── demo.py                # Complete interactive demo
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🛠️ Installation

1. **Install Python 3.8+**
2. **Clone/Download the project**
3. **Install dependencies:**
   ```bash
   cd rag_chatbot
   pip install -r requirements.txt
   ```

## 🎯 Quick Start

### Option 1: Interactive Demo (Recommended)
```bash
cd src
python demo.py
```
This will show a menu with all phases and interactive demos.

### Option 2: Run Individual Phases

**Phase 1 - Manual Text Ingestion:**
```bash
cd src
python main_phase1.py
```

**Phase 2 - Automatic Website Ingestion:**
```bash
cd src
python main_phase2.py
```

**Phase 3 - Interactive Chatbot:**
```bash
cd src
python main_phase3.py
```

## 📋 Phase Breakdown

### Phase 1: Manual Website Content Ingestion ✅
- ✅ Accept raw website text as input
- ✅ Clean and preprocess text
- ✅ Split content into overlapping chunks
- ✅ Generate vector embeddings
- ✅ Store in FAISS vector database
- ✅ Enable similarity search

### Phase 2: Automatic Website Content Ingestion & AI Summarization ✅
- ✅ Accept website URL as input
- ✅ Automatically scrape main content
- ✅ Clean and preprocess extracted text
- ✅ Generate AI-powered summaries using Hugging Face
- ✅ Create chunks and vector embeddings
- ✅ Store in FAISS with summary display

### Phase 3: Reusable & Plug-and-Play Website Chatbot System ✅
- ✅ Design as reusable module
- ✅ Dynamic content loading (text or URL)
- ✅ Automatic vector store rebuilding
- ✅ RAG-based question answering
- ✅ Content-based responses (no hallucinations)
- ✅ Easy integration as support chatbot

## 💻 Usage Examples

### Using the Reusable Chatbot
```python
from chatbot.rag_chatbot import RAGChatbot

# Initialize chatbot
chatbot = RAGChatbot()

# Load from text
chatbot.load_from_text("Your website content here...", "Source Name")

# Or load from URL
chatbot.load_from_url("https://example.com", max_pages=3)

# Ask questions
result = chatbot.ask("What is this about?")
print(result['answer'])
```

### Manual Ingestion
```python
from ingestion.manual_ingestion import ManualIngestor

ingestor = ManualIngestor()
ingestor.ingest_text(your_text)
ingestor.save_index()
results = ingestor.query("Your question")
```

### Automatic Website Ingestion
```python
from ingestion.automatic_ingestion import AutomaticIngestor

ingestor = AutomaticIngestor()
summary, success = ingestor.ingest_website("https://example.com")
if success:
    print(f"Summary: {summary}")
    results = ingestor.query("Your question")
```

## 🔧 Configuration

Edit `config/config.py` to customize:
- Chunk size and overlap
- Embedding models
- FAISS index paths
- Model parameters

## 📊 Performance Notes

- **First run**: Downloads embedding models (~500MB)
- **Subsequent runs**: Uses cached models
- **Memory usage**: Depends on content size
- **Speed**: Fast similarity search with FAISS

## 🐛 Troubleshooting

**Import Errors**: Make sure you're running from the `src/` directory
```bash
cd src
python your_script.py
```

**Model Download Issues**: Check internet connection for first-time downloads
**Memory Issues**: Reduce `CHUNK_SIZE` in config for large documents

## 🚀 Next Steps

- Add more sophisticated LLM integration
- Implement web interface (Flask/FastAPI)
- Add support for document formats (PDF, DOCX)
- Implement conversation memory
- Add multi-language support

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Built with ❤️ using LangChain, FAISS, and Hugging Face**
