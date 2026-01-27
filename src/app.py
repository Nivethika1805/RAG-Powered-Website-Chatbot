import streamlit as st
import time
import random
import sys
import os
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.manual_ingestion import ManualIngestor
from ingestion.automatic_ingestion import AutomaticIngestor
from chatbot.rag_chatbot import RAGChatbot

# State Management Helper
def set_state(key, value):
    st.session_state[key] = value


# Enhanced Page configuration
st.set_page_config(
    page_title="🤖 RAG-Powered Website Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for "Classic Professional" light theme aesthetics
st.markdown("""
<style>
    /* Classic Professional Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@400;700&display=swap');

    :root {
        --bg-color: #DFD8C8;
        --surface-color: #CABFAB;
        --primary-accent: #41444B;
        --primary-hover: #52575D;
        --text-main: #41444B;
        --text-soft: #52575D;
        --border-color: #CABFAB;
        --card-shadow: 0 4px 10px rgba(65, 68, 75, 0.08);
    }

    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Professional Card */
    .human-card {
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: var(--card-shadow);
    }

    /* Clean Headers */
    .brand-header {
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: var(--text-main);
        margin-bottom: 0.5rem;
        text-align: center;
        letter-spacing: -0.5px;
    }

    .brand-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: var(--text-soft);
        text-align: center;
        margin-bottom: 3.5rem;
        font-weight: 400;
    }

    /* Earthy Professional Buttons */
    .stButton > button {
        background-color: var(--primary-accent);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-hover);
        color: white;
        transform: translateY(-1px);
    }

    /* Standard Input Fields - Transparent & Dark Text */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: transparent !important;
        border: 1px solid var(--primary-accent) !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 500;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-accent) !important;
        box-shadow: 0 0 0 2px rgba(65, 68, 75, 0.2) !important;
    }

    /* Input Labels - Dark Color */
    .stTextArea label, .stTextInput label {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Clear Chat Experience */
    .stChatMessage {
        border-radius: 12px !important;
        padding: 0.75rem !important;
    }

    .stChatMessage [data-testid="stChatMessageContent"] {
        background-color: #E6E1D6;
        border: 1px solid var(--border-color);
        border-radius: 12px;
        color: var(--text-main);
        padding: 1rem !important;
    }

    /* Assistant specific styling */
    [data-testid="stChatMessageAssistant"] [data-testid="stChatMessageContent"] {
        background-color: #DFD8C8;
        border-left: 4px solid var(--primary-accent);
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--surface-color);
        border-right: 1px solid var(--border-color);
    }

    /* Success & Info Boxes */
    .success-box {
        background-color: #CABFAB;
        border: 1px solid var(--primary-accent);
        color: var(--text-main);
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        font-weight: 500;
    }

    .info-box {
        background-color: var(--surface-color);
        border: 1px solid var(--primary-accent);
        color: var(--text-soft);
        border-radius: 12px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state - lazy loading to avoid initialization errors
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'manual_ingestor' not in st.session_state:
    st.session_state.manual_ingestor = None
if 'auto_ingestor' not in st.session_state:
    st.session_state.auto_ingestor = None
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = 0

# Lazy initialization functions
def get_chatbot():
    if st.session_state.chatbot is None:
        st.session_state.chatbot = RAGChatbot()
    return st.session_state.chatbot

def get_manual_ingestor():
    if st.session_state.manual_ingestor is None:
        st.session_state.manual_ingestor = ManualIngestor()
    return st.session_state.manual_ingestor

def get_auto_ingestor():
    if st.session_state.auto_ingestor is None:
        st.session_state.auto_ingestor = AutomaticIngestor()
    return st.session_state.auto_ingestor

def simulate_typing(text, speed=0.01):
    """Simulate a human-like typing effect"""
    placeholder = st.empty()
    full_response = ""
    for char in text:
        full_response += char
        placeholder.markdown(full_response + "▌")
        time.sleep(speed)
    placeholder.markdown(full_response)
    return full_response

def get_avatar_style(role):
    if role == "assistant":
        return "https://api.dicebear.com/7.x/bottts/svg?seed=Slate&backgroundColor=41444B"
    return "https://api.dicebear.com/7.x/avataaars/svg?seed=Stone&backgroundColor=CABFAB"

def main():
    # Premium Brand Header
    st.markdown('<h1 class="brand-header">Knowledge Companion</h1>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Your intelligent partner for exploring wisdom and insights</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        # Features expandable section
        with st.expander("Features", expanded=True):
            # Premium Navigation
            nav_items = [
                ("Manual Content Ingestion", 0, "nav_manual"),
                ("URL-Based Website Ingestion", 1, "nav_url"),
                ("Reusable RAG Chatbot", 2, "nav_chatbot")
            ]


            
            for label, tab_index, key in nav_items:
                is_selected = st.session_state.selected_tab == tab_index
                background = "#CABFAB" if is_selected else "transparent"
                
                st.markdown(f"""
                    <div style="background: {background}; border-left: 4px solid {'var(--primary-accent)' if is_selected else 'transparent'}; 
                                border-radius: 8px; margin-bottom: 0.5rem; padding: 4px; transition: all 0.2s ease;">
                """, unsafe_allow_html=True)

                if st.button(label, key=key, use_container_width=True):
                    st.session_state.selected_tab = tab_index
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    
    # Main content area based on navigation selection - Container removed as requested
    
    if st.session_state.selected_tab == 0:
        phase1_interface()
    elif st.session_state.selected_tab == 1:
        phase2_interface()
    elif st.session_state.selected_tab == 2:
        phase3_interface()

    
def phase1_interface():
    st.markdown('<h2 style="font-family: \'Outfit\', sans-serif; font-size: 2.2rem; font-weight: 700; color: var(--primary); margin-bottom: 1.5rem;">Manual Content Ingestion</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 1rem; text-align: center;">Paste any text or articles you\'d like to discuss with me.</div>', unsafe_allow_html=True)
        
        # Enhanced text input area
        # Check if sample text is loaded and use it as default value

        default_text = ""
        if 'sample_text' in st.session_state:
            default_text = st.session_state.sample_text
            # Clear it after using once
            del st.session_state.sample_text
            
        input_text = st.text_area(
            "Enter your text content here:",
            height=250,
            key="phase1_input",
            placeholder="Paste your website content, documentation, articles, or any text you want to ingest and analyze...",
            help="The text will be processed, chunked, and converted to vector embeddings for intelligent search"
        )
        
        # Character count
        if input_text:
            st.markdown(f'<div style="font-size: 0.75rem; color: var(--text-muted); text-align: right; margin-top: 4px;">SYSTEM LOG: {len(input_text)} characters | {len(input_text.split())} words</div>', unsafe_allow_html=True)
        
        # Enhanced ingest button
        col1a, col1b = st.columns([2, 1])
        with col1a:
            if st.button("Ingest Text", type="primary", use_container_width=True):
                if input_text.strip():
                    with st.spinner("Processing text and creating intelligent embeddings..."):
                        try:
                            manual_ingestor = get_manual_ingestor()
                            manual_ingestor.ingest_text(input_text)
                            manual_ingestor.save_index()
                            
                            # Update chatbot with this content
                            chatbot = get_chatbot()
                            chatbot.load_from_text(input_text, "Manual Input")
                            
                            st.markdown('<div class="success-box">Text successfully ingested and processed!</div>', unsafe_allow_html=True)
                            st.success(f"Processed {len(input_text)} characters into searchable vector embeddings")
                        except Exception as e:
                            st.error(f"Error ingesting text: {str(e)}")
                else:
                    st.warning("Please enter some text to ingest.")
        
        with col1b:
            if st.button("Sample Text", use_container_width=True, on_click=set_state, args=("phase1_input", """Artificial Intelligence (AI) is transforming the world! AI refers to the simulation of human intelligence in machines that are programmed to think and learn. 

Key AI Technologies:
• Machine Learning - Systems that learn from data
• Neural Networks - Brain-inspired computing
• Natural Language Processing - Understanding human language
• Computer Vision - Interpreting visual information

Applications: Virtual assistants, recommendation systems, autonomous vehicles, medical diagnosis, and more. The future of AI is incredibly exciting!""")):
                st.rerun()

        
        # Remove the separate paste button since we're auto-populating
    
    with col2:
        st.markdown('<div style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 1rem; text-align: center;">Ask me anything about the text you shared!</div>', unsafe_allow_html=True)
        
        # Enhanced query input
        query = st.text_input(
            "Ask a question about your text:",
            key="phase1_query",
            placeholder="e.g., What are the main topics? Explain key concepts...",
            help="The system will find the most relevant text chunks to answer your question"
        )

        
        # Quick query suggestions
        st.markdown("**Quick Questions:**")
        quick_queries = ["What is the main topic?", "What are the key points?", "Explain the concepts mentioned"]
        
        for i, q in enumerate(quick_queries):
            if st.button(f"{q}", key=f"quick_{i}", use_container_width=True, on_click=set_state, args=("phase1_query", q)):
                st.rerun()

        
        if st.button("Ask AI", key="phase1_ask", use_container_width=True, type="primary"):
            if query.strip():
                with st.spinner("Generating AI answer..."):
                    try:
                        chatbot = get_chatbot()
                        status = chatbot.get_status()
                        if not status['loaded'] or status['source'] == "Manual Input":
                            chatbot.load_from_text(input_text, "Manual Input")
                        
                        result = chatbot.ask(query, k=5)
                        st.session_state.phase1_ai_result = result
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
            else:
                st.warning("Please enter a question for the AI.")

    
    # NEW: Streamlined Result Display Section
    if 'phase1_ai_result' in st.session_state:
        st.markdown('<hr style="border-color: #E2E8F0; margin: 2rem 0;">', unsafe_allow_html=True)
        
        result = st.session_state.phase1_ai_result
        st.markdown('<div class="info-box" style="margin-bottom: 1rem;">AI Synthesized Answer</div>', unsafe_allow_html=True)
        st.write(result['answer'])
        
        if result['context']:
            with st.expander("Show Source Context"):
                for i, ctx in enumerate(result['context'], 1):
                    st.markdown(f"**Source {i}:** {ctx}")



def phase2_interface():
    st.markdown('<h2 style="font-family: \'Outfit\', sans-serif; font-size: 2.2rem; font-weight: 700; color: var(--primary); margin-bottom: 1.5rem;">URL-Based Website Ingestion</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 1rem; text-align: center;">Give me a link, and I\'ll explore the website to help you understand it.</div>', unsafe_allow_html=True)
        
        # URL input
        url = st.text_input(
            "Enter website URL:",
            key="phase2_url",
            placeholder="https://example.com or https://wikipedia.org/topic"
        )
        
        # Sample URLs
        st.markdown("**Sample URLs:**")
        sample_urls = [
            "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "https://en.wikipedia.org/wiki/Machine_learning",
            "https://www.ibm.com/cloud/learn/what-is-artificial-intelligence"
        ]
        
        for i, sample_url in enumerate(sample_urls):
            if st.button(f"Load Sample {i+1}", key=f"url_{i}", use_container_width=True, on_click=set_state, args=("phase2_url", sample_url)):
                st.rerun()

        
        # Ingest button
        if st.button("Ingest Website", type="primary", use_container_width=True):
            if url.strip():
                with st.spinner("Scraping website and generating AI summary..."):
                    try:
                        # Use chatbot directly to load URL - this handles auto_ingestor internally
                        chatbot = get_chatbot()
                        success = chatbot.load_from_url(url)
                        
                        if success:
                            status = chatbot.get_status()
                            st.markdown('<div class="success-box">Website successfully ingested!</div>', unsafe_allow_html=True)
                            
                            # Display summary prominently
                            if status['summary']:
                                st.markdown('<div class="info-box"><div class="stat-label" style="color: var(--indigo-400); margin-bottom: 0.5rem;">Crawler Abstract</div>' + status['summary'] + '</div>', unsafe_allow_html=True)
                                # Store for Phase 2 local display
                                st.session_state.website_summary = status['summary']
                                st.session_state.website_url = url
                        else:
                            st.error("Failed to ingest website. Please check the URL.")
                    except Exception as e:
                        st.error(f"Error ingesting website: {str(e)}")
            else:
                st.warning("Please enter a URL.")
    
    with col2:
        st.markdown('<div style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 1rem; text-align: center;">I\'ve indexed the content. What would you like to know?</div>', unsafe_allow_html=True)
        
        # Show website summary if available
        if 'website_summary' in st.session_state:
            st.markdown("**Website Summary:**")
            st.info(st.session_state.website_summary[:200] + "..." if len(st.session_state.website_summary) > 200 else st.session_state.website_summary)
            st.markdown(f"**Source:** {st.session_state.website_url}")
        
        # Query input
        query = st.text_input("Ask about the website:", key="phase2_query")

        
        # Sample questions
        st.markdown("**Sample Questions:**")
        sample_questions = [
            "What is the main topic?",
            "What are the key points?",
            "Explain the important concepts"
        ]
        
        for i, q in enumerate(sample_questions):
            if st.button(f"{q}", key=f"sample_q_{i}", use_container_width=True, on_click=set_state, args=("phase2_query", q)):
                st.rerun()

        
        if st.button("Ask AI", key="phase2_ask", use_container_width=True, type="primary"):
            if query.strip():
                with st.spinner("Generating AI answer..."):
                    try:
                        chatbot = get_chatbot()
                        result = chatbot.ask(query, k=5)
                        st.session_state.phase2_ai_result = result
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
            else:
                st.warning("Please enter a question.")

    
    # NEW: Streamlined Result Display Section for Phase 2
    if 'phase2_ai_result' in st.session_state:
        st.markdown('<hr style="border-color: #E2E8F0; margin: 2rem 0;">', unsafe_allow_html=True)
        
        result = st.session_state.phase2_ai_result
        st.markdown('<div class="info-box" style="margin-bottom: 1rem;">AI Synthesized Answer</div>', unsafe_allow_html=True)
        st.write(result['answer'])
        
        if result['context']:
            with st.expander("Show Insight Sources"):
                for i, ctx in enumerate(result['context'], 1):
                    st.markdown(f"**Source {i}:** {ctx}")



def phase3_interface():
    st.markdown('<h2 style="font-family: \'Outfit\', sans-serif; font-size: 2.2rem; font-weight: 700; color: var(--primary); margin-bottom: 1.5rem;">Reusable RAG Chatbot</h2>', unsafe_allow_html=True)
    
    chatbot = get_chatbot()
    status = chatbot.get_status()
    
    # Simplified Layout: Direct Download & Embed
    st.markdown('<div style="padding: 1rem 0; text-align: center;">', unsafe_allow_html=True)
    
    st.markdown("### 📦 Your Ready-to-Deploy RAG Agent")
    st.markdown("Download the complete intelligent system or copy the embed code to use it in your application instantly.")
    
    if status['loaded']:
        st.markdown(f'<div style="font-size: 0.9rem; color: #059669; font-weight: 500; margin-bottom: 2rem;">✅ Knowledge Base Synced: {status["source"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size: 0.9rem; color: #64748B; font-weight: 400; margin-bottom: 2rem;">📝 Status: Pre-configured Default Agent Ready</div>', unsafe_allow_html=True)

    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 1. Download Package")
        st.markdown("Get the full RAG system including vector index, model configs, and ingestion logic.")
        if st.button("📥 Download RAG Agent (.zip)", use_container_width=True, type="primary"):
            st.success("Your RAG Agent package is being prepared for download...")
            # Simulation of package prep
            
    with col2:
        st.markdown("#### 2. Get Embed Code")
        st.markdown("Quickly attach the help chatbot to any website using our specialized script.")
        
        # Professional embed code snippet
        source_name = status['source'] if status['source'] else "default_agent"
        embed_id = "rag_" + source_name.lower().replace(" ", "_")[:10]
        snippet = f"""<!-- RAG Help Agent Embed -->
<script src="https://rag-agent.cdn/v1/widget.js" async></script>
<script>
  window.initRAGAgent({{
    agentId: "{embed_id}",
    source: "{source_name}"
  }});
</script>"""
        st.code(snippet, language="html")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="margin-top: 2rem; padding: 1.5rem; background: #f1f5f9; border-radius: 12px; border: 1px dashed #cbd5e1;">
            <p style="color: #475569; font-size: 0.9rem; margin-bottom: 0;"><strong>PRO TIP:</strong> Once downloaded, you can host the agent on your own server or directly attach the script to your website's header to enable the help chatbot instantly.</p>
        </div>
    """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
