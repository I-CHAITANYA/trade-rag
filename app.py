import streamlit as st

from src.retriever import retrieve_documents
from src.llm import generate_answer



# Page configuration

st.set_page_config(
    page_title="Trade-RAG",
    page_icon="📈",
    layout="centered"
)



# Title

st.title("📈 Trade-RAG")

st.write(
    "AI Trading Knowledge Assistant powered by RAG"
)



# User input

question = st.text_input(
    "Ask your trading question:"
)



if question:


    with st.spinner(
        "Searching trading knowledge base..."
    ):


        # Retrieve relevant documents

        documents = retrieve_documents(
            question
        )


        # Generate answer

        answer = generate_answer(
            question,
            documents
        )



    st.subheader(
        "Answer"
    )


    st.write(answer)



    # Display sources

    st.subheader(
        "Sources"
    )


    for doc in documents:

        st.write(
            "📄",
            doc.metadata.get(
                "source",
                "Unknown"
            )
        )
