import os
import sys
from pathlib import Path
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DATA_PATH, VECTORSTORE_PATH, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import pickle

def load_documents(data_path):
    """
    Load all PDF documents with progress tracking
    """
    documents = []
    pdf_files = []
    
    # Collect all PDF files
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    
    print(f"Found {len(pdf_files)} PDF files")
    
    # Load each PDF with progress bar
    for file_path in tqdm(pdf_files, desc="Loading PDFs"):
        try:
            loader = PyMuPDFLoader(file_path)
            docs = loader.load()
            
            # Add metadata
            for doc in docs:
                doc.metadata["source"] = os.path.basename(file_path)
                doc.metadata["filepath"] = file_path
                doc.metadata["category"] = os.path.basename(os.path.dirname(file_path))
            
            documents.extend(docs)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return documents

def split_documents(documents):
    """
    Split documents with better chunking
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""],
        length_function=len,
    )
    
    chunks = splitter.split_documents(documents)
    
    # Add chunk metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        chunk.metadata["chunk_count"] = len(chunks)
    
    return chunks

def create_vectorstore(chunks):
    """
    Create FAISS vector database with progress
    """
    print("Initializing embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    print("Creating vectorstore...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Save vectorstore
    os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)
    vectorstore.save_local(VECTORSTORE_PATH)
    
    # Save document metadata for BM25 (optional)
    metadata = [doc.metadata for doc in chunks]
    with open(os.path.join(os.path.dirname(VECTORSTORE_PATH), "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)
    
    print(f"✅ Vectorstore saved to {VECTORSTORE_PATH}")
    return vectorstore

def main():
    print("=" * 60)
    print("📊 TradeRAG - Document Ingestion")
    print("=" * 60)
    
    # Load documents
    print(f"\n📁 Loading documents from: {DATA_PATH}")
    documents = load_documents(DATA_PATH)
    print(f"✅ Loaded {len(documents)} document pages")
    
    # Split into chunks
    print("\n✂️ Splitting documents into chunks...")
    chunks = split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    
    # Create vectorstore
    print("\n🧠 Creating vector database...")
    create_vectorstore(chunks)
    
    print("\n" + "=" * 60)
    print("✅ Ingestion completed successfully!")
    print("=" * 60)
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"  - Documents: {len(documents)} pages")
    print(f"  - Chunks: {len(chunks)}")
    print(f"  - Chunk size: {CHUNK_SIZE} characters")
    print(f"  - Overlap: {CHUNK_OVERLAP} characters")
    print(f"  - Embedding model: {EMBEDDING_MODEL}")
    print(f"  - Vectorstore: {VECTORSTORE_PATH}")

if __name__ == "__main__":
    main()