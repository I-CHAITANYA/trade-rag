import os

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Paths

DATA_PATH = "data"
VECTORSTORE_PATH = "vectorstore/faiss_index"


# Embedding model

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"



def load_documents(data_path):
    """
    Load all PDF documents from data folder
    """

    documents = []


    for root, dirs, files in os.walk(data_path):

        for file in files:

            if file.endswith(".pdf"):

                file_path = os.path.join(root, file)

                print(f"Loading: {file_path}")


                loader = PyMuPDFLoader(file_path)

                docs = loader.load()


                # Add source metadata

                for doc in docs:
                    doc.metadata["source"] = file


                documents.extend(docs)


    return documents



def split_documents(documents):
    """
    Split documents into smaller chunks
    """


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )


    chunks = splitter.split_documents(documents)


    print(f"Total chunks created: {len(chunks)}")


    return chunks




def create_vectorstore(chunks):
    """
    Create FAISS vector database
    """


    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )


    vectorstore.save_local(
        VECTORSTORE_PATH
    )


    print("FAISS vector database created!")





def main():

    print("Starting ingestion...")


    documents = load_documents(DATA_PATH)


    print(
        f"Total documents loaded: {len(documents)}"
    )


    chunks = split_documents(documents)


    create_vectorstore(chunks)


    print("Ingestion completed successfully!")




if __name__ == "__main__":
    main()