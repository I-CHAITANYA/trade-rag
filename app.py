import streamlit as st
from src.retriever import retrieve_documents
from src.llm import generate_answer
import time

st.set_page_config(
    page_title="TradeRAG - AI Trading Assistant",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for better formatting
st.markdown("""
<style>
    .answer-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .source-tag {
        background-color: #e8f0fe;
        padding: 0.2rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        color: #1a73e8;
        display: inline-block;
        margin: 0.2rem;
    }
    .section-header {
        font-weight: 600;
        color: #1a73e8;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .pro-tip {
        background-color: #f0f9ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1a73e8;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("## 📊 TradeRAG")
    st.markdown("*Intelligent Trading Assistant*")
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    top_k = st.slider("Documents to retrieve", 1, 5, 3)
    
    st.markdown("---")
    st.markdown("### 📚 Knowledge Base")
    st.markdown("""
    - ✅ Technical Indicators
    - ✅ Trading Strategies
    - ✅ Risk Management
    - ✅ Candlestick Patterns
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Example Questions")
    if st.button("📊 Position Sizing"):
        question = "What is proper position sizing?"
        st.session_state.messages.append({"role": "user", "content": question})
    if st.button("📈 RSI Indicator"):
        question = "How does RSI work and how do I use it?"
        st.session_state.messages.append({"role": "user", "content": question})
    if st.button("🛡️ Risk Management"):
        question = "What are the key principles of risk management?"
        st.session_state.messages.append({"role": "user", "content": question})

# Main content
st.markdown("# 📈 TradeRAG")
st.markdown("*Your AI-powered trading knowledge assistant*")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if question := st.chat_input("Ask your trading question..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    
    # Generate and display response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching knowledge base..."):
            # Retrieve and generate
            documents = retrieve_documents(question, k=top_k)
            
            # Show retrieved documents count
            st.caption(f"📚 Retrieved {len(documents)} documents")
            
            # Generate answer
            answer, sources = generate_answer(question, documents)
            
            # Display answer
            st.markdown(answer)
    
    # Add to session
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    ⚠️ Educational purposes only. Trading involves significant risk.
</div>
""", unsafe_allow_html=True)