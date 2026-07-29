import streamlit as st
from src.retriever import retrieve_documents
from src.llm import generate_answer
import time

# Page configuration
st.set_page_config(
    page_title="TradeRAG - AI Trading Knowledge Assistant",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .source-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #3a7bd5;
    }
    .answer-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    .stChatFloatingInputContainer {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sources" not in st.session_state:
    st.session_state.sources = []

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/stock.png", width=80)
    st.markdown("## 📚 Knowledge Base")
    st.markdown("""
    ### Supported Topics:
    - 📊 Technical Indicators
    - 📈 Trading Strategies
    - ⚖️ Risk Management
    - 🕯️ Candlestick Patterns
    - 🧠 Trading Psychology
    
    ### 📁 Documents Indexed:
    """)
    
    # Show indexed documents (you can make this dynamic)
    indexed_docs = ["swing_trading.pdf", "MACD.pdf", "RSI.pdf", "candlestick.pdf"]
    for doc in indexed_docs:
        st.markdown(f"✅ {doc}")
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    top_k = st.slider("Retrieval depth", 1, 10, 3, 
                      help="Number of documents to retrieve for each query")
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("""
    - Ask specific questions
    - Include indicator names
    - Ask about trading concepts
    - Request strategy explanations
    """)

# Main content
st.markdown('<div class="main-header">📈 TradeRAG</div>', unsafe_allow_html=True)
st.markdown("*AI Trading Knowledge Assistant powered by Retrieval-Augmented Generation*")

# Quick question buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 What is RSI?", use_container_width=True):
        question = "What is RSI and how is it used in trading?"
        st.session_state.messages.append({"role": "user", "content": question})
with col2:
    if st.button("📈 Explain MACD", use_container_width=True):
        question = "How does MACD work and what signals does it generate?"
        st.session_state.messages.append({"role": "user", "content": question})
with col3:
    if st.button("🛡️ Risk Management", use_container_width=True):
        question = "What are the key principles of risk management in trading?"
        st.session_state.messages.append({"role": "user", "content": question})
with col4:
    if st.button("🔄 Moving Average", use_container_width=True):
        question = "What is moving average and how is it calculated?"
        st.session_state.messages.append({"role": "user", "content": question})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if question := st.chat_input("Ask your trading question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching knowledge base..."):
            # Retrieve documents
            documents = retrieve_documents(question, k=top_k)
            
            # Generate answer
            answer, sources = generate_answer(question, documents)
            
            # Display answer with better formatting
            st.markdown('<div class="answer-box">', unsafe_allow_html=True)
            
            # Split answer into paragraphs and display
            paragraphs = answer.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    st.markdown(para)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Store sources
            st.session_state.sources = sources
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Sources section
if st.session_state.sources:
    st.markdown("---")
    st.markdown("### 📚 Sources")
    
    cols = st.columns(min(len(st.session_state.sources), 3))
    for idx, source in enumerate(st.session_state.sources[:6]):
        col = cols[idx % len(cols)]
        with col:
            st.markdown(f'<div class="source-card">📄 {source}</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    ⚠️ Disclaimer: This is an educational tool. Always verify information and consult with a financial advisor.
</div>
""", unsafe_allow_html=True)