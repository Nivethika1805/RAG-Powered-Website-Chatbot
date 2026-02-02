import streamlit as st
import sys
import os
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.manual_ingestion import ManualIngestor
from ingestion.automatic_ingestion import AutomaticIngestor
from chatbot.rag_chatbot import RAGChatbot

# Enhanced Page configuration
st.set_page_config(
    page_title="🤖 RAG-Powered Website Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for modern, professional design with earthy theme
st.markdown("""
<style>
    /* Main styling with earthy theme */
    .stApp {
        background: linear-gradient(135deg, #E4E0E1 0%, #D6C0B3 50%, #AB886D 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Headers with animation */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #493628, #AB886D, #D6C0B3, #E4E0E1);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(73, 54, 40, 0.1);
        animation: gradientShift 4s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #493628;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .phase-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: linear-gradient(90deg, #493628, #AB886D);
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(73, 54, 40, 0.3);
    }
    
    /* Cards and boxes */
    .success-box {
        background: linear-gradient(135deg, #E4E0E1 0%, #D6C0B3 100%);
        border: 2px solid #AB886D;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #493628;
        box-shadow: 0 8px 32px rgba(73, 54, 40, 0.15);
        font-weight: 500;
    }
    
    .info-box {
        background: linear-gradient(135deg, #D6C0B3 0%, #AB886D 100%);
        border: 2px solid #493628;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #ffffff;
        box-shadow: 0 8px 32px rgba(73, 54, 40, 0.2);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #E4E0E1 0%, #D6C0B3 100%);
        border: 2px solid #493628;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #493628;
        box-shadow: 0 8px 32px rgba(73, 54, 40, 0.15);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #493628, #AB886D);
        color: white;
        border: 2px solid #D6C0B3;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(73, 54, 40, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #AB886D, #D6C0B3);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(73, 54, 40, 0.4);
        border-color: #493628;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(228, 224, 225, 0.9);
        border: 2px solid #AB886D;
        border-radius: 10px;
        padding: 0.75rem;
        color: #493628;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #493628;
        box-shadow: 0 0 0 3px rgba(73, 54, 40, 0.1);
        background: rgba(255, 255, 255, 0.95);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(73, 54, 40, 0.1);
        border-radius: 15px;
        padding: 0.5rem;
        backdrop-filter: blur(10px);
        border: 2px solid #AB886D;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(228, 224, 225, 0.8);
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #493628;
        transition: all 0.3s ease;
        border: 1px solid #AB886D;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #493628, #AB886D);
        color: white;
        border-color: #493628;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #493628 0%, #AB886D 100%);
        padding: 1rem;
        border-right: 3px solid #D6C0B3;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(228, 224, 225, 0.95);
        border: 2px solid #AB886D;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(73, 54, 40, 0.15);
        color: #493628;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(45deg, #493628, #AB886D);
        border-radius: 10px;
        color: white;
        font-weight: 600;
        border: 1px solid #D6C0B3;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(45deg, #493628, #AB886D);
    }
    
    /* Selectbox */
    .stSelectbox > div > div > select {
        background: rgba(228, 224, 225, 0.9);
        border: 2px solid #AB886D;
        border-radius: 10px;
        color: #493628;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(45deg, #493628, #AB886D);
    }
    
    /* Dataframe */
    .dataframe {
        background: rgba(228, 224, 225, 0.9);
        border: 2px solid #AB886D;
        border-radius: 10px;
    }
    
    /* Metrics */
    .stMetric {
        background: rgba(228, 224, 225, 0.9);
        border: 2px solid #AB886D;
        border-radius: 10px;
        padding: 1rem;
        color: #493628;
    }
    
    /* Tooltip */
    .stTooltip {
        background: #493628;
        color: white;
        border: 1px solid #D6C0B3;
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

def main():
    # Enhanced main header with animation effect
    st.markdown('<h1 class="main-header">RAG-Powered Website Chatbot</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, #493628, #AB886D); border-radius: 15px; margin-bottom: 1rem; border: 2px solid #D6C0B3;"><h3 style="color: white; margin: 0;">Navigation</h3></div>', unsafe_allow_html=True)
        
        # Features expandable section
        with st.expander("Features", expanded=True):
            # Manual Content Ingestion
            if st.session_state.selected_tab == 0:
                st.markdown('<div style="background: linear-gradient(45deg, #493628, #AB886D); padding: 0.5rem; border-radius: 10px; margin: 0.25rem 0;">', unsafe_allow_html=True)
                if st.button("Manual Content Ingestion", key="nav_manual", use_container_width=True, type="primary"):
                    st.session_state.selected_tab = 0
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if st.button("Manual Content Ingestion", key="nav_manual", use_container_width=True):
                    st.session_state.selected_tab = 0
                    st.rerun()
            
            # URL Based Website Ingestion
            if st.session_state.selected_tab == 1:
                st.markdown('<div style="background: linear-gradient(45deg, #493628, #AB886D); padding: 0.5rem; border-radius: 10px; margin: 0.25rem 0;">', unsafe_allow_html=True)
                if st.button("URL Based Website Ingestion", key="nav_url", use_container_width=True, type="primary"):
                    st.session_state.selected_tab = 1
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if st.button("URL Based Website Ingestion", key="nav_url", use_container_width=True):
                    st.session_state.selected_tab = 1
                    st.rerun()
            
            # Reusable RAG Chatbot
            if st.session_state.selected_tab == 2:
                st.markdown('<div style="background: linear-gradient(45deg, #493628, #AB886D); padding: 0.5rem; border-radius: 10px; margin: 0.25rem 0;">', unsafe_allow_html=True)
                if st.button("Reusable RAG Chatbot", key="nav_chatbot", use_container_width=True, type="primary"):
                    st.session_state.selected_tab = 2
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if st.button("Reusable RAG Chatbot", key="nav_chatbot", use_container_width=True):
                    st.session_state.selected_tab = 2
                    st.rerun()
    
    # Main content area based on navigation selection
    st.markdown('<div style="background: rgba(228, 224, 225, 0.9); padding: 2rem; border-radius: 15px; border: 2px solid #AB886D; margin: 1rem 0;">', unsafe_allow_html=True)
    
    if st.session_state.selected_tab == 0:
        phase1_interface()
    elif st.session_state.selected_tab == 1:
        phase2_interface()
    elif st.session_state.selected_tab == 2:
        phase3_interface()
    
    st.markdown('</div>', unsafe_allow_html=True)

def phase1_interface():
    st.markdown('<h2 class="phase-header">Manual Content Ingestion & Query</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;"><h3 style="color: white; margin: 0;">Input Text Content</h3></div>', unsafe_allow_html=True)
        
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
            value=default_text,
            placeholder="Paste your website content, documentation, articles, or any text you want to ingest and analyze...",
            help="The text will be processed, chunked, and converted to vector embeddings for intelligent search"
        )
        
        # Character count
        if input_text:
            st.markdown(f'<div style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border-radius: 10px; color: white; text-align: right;">Characters: {len(input_text)} | Words: {len(input_text.split())}</div>', unsafe_allow_html=True)
        
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
            if st.button("Sample Text", use_container_width=True):
                sample_text = """Artificial Intelligence (AI) is transforming the world! AI refers to the simulation of human intelligence in machines that are programmed to think and learn. 

Key AI Technologies:
• Machine Learning - Systems that learn from data
• Neural Networks - Brain-inspired computing
• Natural Language Processing - Understanding human language
• Computer Vision - Interpreting visual information

Applications: Virtual assistants, recommendation systems, autonomous vehicles, medical diagnosis, and more. The future of AI is incredibly exciting!"""
                
                # Store in session state and rerun to populate the text area
                st.session_state.sample_text = sample_text
                st.rerun()
        
        # Remove the separate paste button since we're auto-populating
    
    with col2:
        st.markdown('<div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;"><h3 style="color: white; margin: 0;">Intelligent Query System</h3></div>', unsafe_allow_html=True)
        
        # Enhanced query input
        query = st.text_input(
            "Ask a question about your text:",
            placeholder="e.g., What are the main topics? Explain key concepts...",
            help="The system will find the most relevant text chunks to answer your question"
        )
        
        # Quick query suggestions
        st.markdown("**Quick Questions:**")
        quick_queries = ["What is the main topic?", "What are the key points?", "Explain the concepts mentioned"]
        
        for i, q in enumerate(quick_queries):
            if st.button(f"{q}", key=f"quick_{i}", use_container_width=True):
                query = q
                st.rerun()
        
        # Search button
        if st.button("Search", key="phase1_query", use_container_width=True, type="primary"):
            if query.strip():
                with st.spinner("Searching for relevant information..."):
                    try:
                        manual_ingestor = get_manual_ingestor()
                        results = manual_ingestor.query(query, k=3)
                        
                        if results:
                            st.markdown(f'<div class="success-box">Found {len(results)} relevant text chunks!</div>', unsafe_allow_html=True)
                            
                            for i, result in enumerate(results, 1):
                                with st.expander(f"Result {i} - Most Relevant", expanded=True):
                                    st.markdown(f'<div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; color: white;">{result}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="warning-box">No relevant information found. Try different keywords!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error searching: {str(e)}")
            else:
                st.warning("Please enter a question to search.")

def phase2_interface():
    st.markdown('<h2 class="phase-header">URL Based Website Ingestion</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Website URL Input")
        
        # URL input
        url = st.text_input(
            "Enter website URL:",
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
            if st.button(f"Load Sample {i+1}", key=f"url_{i}", use_container_width=True):
                url = sample_url
                st.rerun()
        
        # Ingest button
        if st.button("Ingest Website", type="primary", use_container_width=True):
            if url.strip():
                with st.spinner("Scraping website and generating AI summary..."):
                    try:
                        auto_ingestor = get_auto_ingestor()
                        summary = auto_ingestor.ingest_url(url)
                        
                        # Update chatbot with this content
                        chatbot = get_chatbot()
                        chatbot.load_from_url(url)
                        
                        st.markdown('<div class="success-box">Website successfully ingested!</div>', unsafe_allow_html=True)
                        st.success(f"Processed website content and generated AI summary")
                        
                        # Display summary prominently
                        if summary:
                            st.markdown('<div class="info-box">Website Summary</div>', unsafe_allow_html=True)
                            st.write(summary)
                            # Store summary in session state for easy access
                            st.session_state.website_summary = summary
                            st.session_state.website_url = url
                    except Exception as e:
                        st.error(f"Error ingesting website: {str(e)}")
            else:
                st.warning("Please enter a URL.")
    
    with col2:
        st.subheader("Query System")
        
        # Show website summary if available
        if 'website_summary' in st.session_state:
            st.markdown("**Website Summary:**")
            st.info(st.session_state.website_summary[:200] + "..." if len(st.session_state.website_summary) > 200 else st.session_state.website_summary)
            st.markdown(f"**Source:** {st.session_state.website_url}")
        
        # Query input
        query = st.text_input("Ask about the website:")
        
        # Sample questions
        st.markdown("**Sample Questions:**")
        sample_questions = [
            "What is the main topic?",
            "What are the key points?",
            "Explain the important concepts"
        ]
        
        for i, q in enumerate(sample_questions):
            if st.button(f"{q}", key=f"sample_q_{i}", use_container_width=True):
                query = q
                st.rerun()
        
        if st.button("Search", key="phase2_query", use_container_width=True, type="primary"):
            if query.strip():
                with st.spinner("Searching for relevant information..."):
                    try:
                        auto_ingestor = get_auto_ingestor()
                        results = auto_ingestor.query(query, k=3)
                        
                        if results:
                            st.success(f"Found {len(results)} relevant chunks:")
                            for i, result in enumerate(results, 1):
                                with st.expander(f"Result {i}"):
                                    st.write(result)
                        else:
                            st.warning("No relevant information found.")
                    except Exception as e:
                        st.error(f"Error searching: {str(e)}")
            else:
                st.warning("Please enter a question.")

def phase3_interface():
    st.markdown('<h2 class="phase-header">Reusable RAG Chatbot</h2>', unsafe_allow_html=True)
    
    # Check if content is loaded
    chatbot = get_chatbot()
    status = chatbot.get_status()
    
    if not status['loaded']:
        st.markdown('<div class="warning-box">No content loaded! Please use Manual Content Ingestion or URL Based Website Ingestion first.</div>', unsafe_allow_html=True)
        
        # Quick load options
        st.subheader("Quick Load Content")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Load Sample Text", type="secondary"):
                sample_text = """
                Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines 
                that can perform tasks that typically require human intelligence. AI systems can learn from experience, 
                adapt to new inputs, and perform human-like tasks.
                
                Key areas of AI include machine learning, neural networks, natural language processing, computer vision, 
                and robotics. These technologies are transforming industries from healthcare to finance, transportation 
                to entertainment.
                """
                chatbot.load_from_text(sample_text, "Sample AI Text")
                st.rerun()
        
        with col2:
            if st.button("Load Wikipedia AI", type="secondary"):
                chatbot.load_from_url("https://en.wikipedia.org/wiki/Artificial_intelligence")
                st.rerun()
    else:
        # Show current status
        st.markdown('<div class="success-box">Content loaded successfully!</div>', unsafe_allow_html=True)
        st.write(f"**Source:** {status['source']}")
        if status['summary']:
            st.write(f"**Summary:** {status['summary'][:200]}...")
        
        # Chat interface
        st.subheader("Ask Questions")
        
        # Chat input
        query = st.text_input("Your question:")
        
        if st.button("Ask", type="primary"):
            if query.strip():
                with st.spinner("Searching..."):
                    try:
                        result = chatbot.ask(query, k=2)
                        st.info(result['answer'])
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a question.")
    
    # Display current content info
    st.info(f"📖 Currently chatting with: {status['source']}")
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask a question about the loaded content:")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get bot response
        with st.spinner("Thinking..."):
            try:
                result = st.session_state.chatbot.ask(user_input)
                bot_response = result['answer']
                
                # Add bot response to history
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                
                # Rerun to display the new messages
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

if __name__ == "__main__":
    main()
