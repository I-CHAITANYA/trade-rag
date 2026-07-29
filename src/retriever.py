import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.knowledge_base import TradingKnowledgeBase

from config import VECTORSTORE_PATH, EMBEDDING_MODEL, TOP_K_RESULTS

# Global knowledge base
knowledge_base = TradingKnowledgeBase()

def load_vectorstore():
    """Load existing FAISS vector database"""
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    return vectorstore

def retrieve_documents(query, k=TOP_K_RESULTS):
    """Retrieve top-k relevant documents with knowledge augmentation"""
    vectorstore = load_vectorstore()
    
    # Get initial results
    results = vectorstore.similarity_search(query, k=k)
    
    # Augment with domain knowledge
    results = knowledge_base.augment_documents(query, results)
    
    return results[:k]  # Return top k after augmentation

def retrieve_with_scores(query, k=TOP_K_RESULTS):
    """Retrieve with similarity scores"""
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=k)
    return results

def print_results(results):
    """Display retrieved documents"""
    for i, doc in enumerate(results):
        print("\n--------------------")
        print(f"Result {i+1}")
        print("--------------------")
        print(doc.page_content)
        print("\nSource:")
        print(doc.metadata.get("source", "Unknown"))
        print("Type:")
        print(doc.metadata.get("type", "General"))

if __name__ == "__main__":
    query = input("Ask your trading question: ")
    results = retrieve_documents(query)
    print_results(results)