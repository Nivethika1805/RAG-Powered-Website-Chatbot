# RAG-Powered Website Chatbot (Antigravity AI)

**A website-agnostic, AI-powered chatbot system designed to be embedded into any website for instant, content-aware customer support.**

---

## 📖 Project Overview

This project implements a reusable AI chatbot that leverages **Retrieval-Augmented Generation (RAG)** to answer user queries based strictly on the content of the website it is embedded in. Designed with versatility in mind, the chatbot effectively acts as an automated support agent, similar to enterprise solutions (e.g., Infosys website chatbot), but accessible for any web platform.

The system is built to dynamically load website content, understand context, and provide accurate, context-aware answers using state-of-the-art LLMs.

## ✨ Features

- **Website Agnostic:** Can be integrated into any website regardless of the underlying technology.
- **RAG-Powered:** Uses Retrieval-Augmented Generation to ground answers in the specific website's data, reducing hallucinations.
- **Automated Content Ingestion:** Capable of scraping and processing website content automatically.
- **AI Exaplainability:** Generates concise summaries and overviews of the ingested website content.
- **Modern Backend:** Built with FastAPI for high performance and easy integration.
- **Vector Search:** Utilizes FAISS for efficient similarity search across document embeddings.

## 🏗️ Project Architecture

The high-level architecture consists of three main components:

1.  **Ingestion Engine:** Crawls the target URL or accepts manual content, cleans the text, and prepares it for processing.
2.  **RAG Pipeline:**
    *   **Embeddings:** Converts text chunks into vector embeddings using Sentence Transformers.
    *   **Vector Store:** Stores embeddings in a FAISS index for fast retrieval.
    *   **LLM Integration:** Retrieves relevant context and generates the final response using the Gemini API.
3.  **API Layer:** A FastAPI backend that exposes endpoints for the frontend widget to communicate with the RAG system.

## 🚀 Phase-wise Implementation

The project is structured into three distinct phases of development:

### Phase 1: Manual Content Ingestion
*   **Goal:** Establish the baseline for question answering.
*   **Method:** Website content is manually provided to the system.
*   **Outcome:** A basic chatbot capable of answering questions from a static text source.

### Phase 2: Automatic Website Content Ingestion & AI Summarization
*   **Goal:** Automate the data acquisition process.
*   **Method:**
    *   Implemented web scraping to load content from a given URL.
    *   Added data cleaning pipelines to extract meaningful text.
    *   integrated an AI model to generate a high-level summary of the website.
*   **Outcome:** One-click onboarding for new websites.

### Phase 3: RAG Backend Implementation (Current)
*   **Goal:** Production-ready RAG system.
*   **Details:**
    *   **Chunking:** Splitting content into optimal segments for retrieval.
    *   **Embeddings:** Generating semantic vectors.
    *   **Similarity Search:** Implementing FAISS for fetching relevant chunks.
    *   **Generation:** Generating the final answered using Gemini.
    *   **API:** exposing the full workflow via FastAPI.

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **API Framework:** FastAPI
*   **LLM / AI:** Google Gemini API
*   **Embeddings:** Sentence Transformers
*   **Vector Database:** FAISS (Facebook AI Similarity Search)
*   **Development Environment:** Google Colab / Local Python Environment
*   **Version Control:** GitHub

## 🏃‍♂️ How to Run

### Prerequisites
*   Python 3.8+ installed.
*   A Google Gemini API Key.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Nivethika1805/RAG-Powered-Website-Chatbot.git
    cd RAG-Powered-Website-Chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn sentence-transformers faiss-cpu google-genai beautifulsoup4 requests
    ```

3.  **Set up Environment Variables:**
    Create a `.env` file (or export variables) with your API key:
    ```bash
    export GEMINI_API_KEY="your_api_key_here"
    ```

4.  **Run the Backend:**
    ```bash
    uvicorn main:app --reload
    ```
    *The API will be available at `http://127.0.0.1:8000`*

## 🔮 Future Enhancements

- **Frontend Widget:** specific JS widget for easy embedding.
- **Multi-page Crawling:** Support for indexing entire sites, not just single pages.
- **Chat History:** Memory implementation for multi-turn conversations.
- **Admin Dashboard:** UI for managing indexed content and customization.

## ⚠️ Disclaimer

This repository does **not** contain API keys. You must provide your own API keys to run the application. Ensure you do not commit your `.env` file or keys to version control.
