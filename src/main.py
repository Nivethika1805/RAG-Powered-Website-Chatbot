from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
import sys

# Add parent directory to path for imports if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chatbot.rag_chatbot import RAGChatbot

# Initialize FastAPI app
app = FastAPI(
    title="RAG-Powered Website Chatbot API",
    description="API for the Antigravity AI RAG Chatbot",
    version="1.0.0"
)

# Initialize Chatbot
chatbot = RAGChatbot()

# Pydantic models for request validation
class TextIngestRequest(BaseModel):
    text: str
    source_name: str = "Manual Input"

class URLIngestRequest(BaseModel):
    url: str
    max_pages: int = 1

class QuestionRequest(BaseModel):
    question: str
    k: int = 3

# Endpoints

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "message": "RAG Chatbot API is running. Documentation available at /docs"
    }

@app.get("/status")
async def get_status():
    """Get current chatbot status."""
    return chatbot.get_status()

@app.post("/ingest/text")
async def ingest_text(request: TextIngestRequest):
    """Ingest raw text content."""
    try:
        success = chatbot.load_from_text(request.text, request.source_name)
        if success:
            return {
                "status": "success",
                "message": "Text ingested successfully",
                "details": chatbot.get_status()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to ingest text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest/url")
async def ingest_url(request: URLIngestRequest):
    """Ingest content from a URL."""
    try:
        # Note: In a real production app, this should be a background task
        # But for simplicity in this demo, we'll await it
        success = chatbot.load_from_url(request.url, request.max_pages)
        if success:
            return {
                "status": "success",
                "message": f"Website {request.url} ingested successfully",
                "details": chatbot.get_status()
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to ingest website. Please check the URL.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing URL: {str(e)}")

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question to the chatbot."""
    try:
        response = chatbot.ask(request.question, request.k)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear")
async def clear_content():
    """Clear all ingested content."""
    chatbot.clear_content()
    return {"status": "success", "message": "All content cleared"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
