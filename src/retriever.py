import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


from config import (
    VECTORSTORE_PATH,
    EMBEDDING_MODEL,
    TOP_K_RESULTS
)


def load_vectorstore():
    """
    Load existing FAISS vector database
    """

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


    return vectorstore




def retrieve_documents(query, k=3):
    """
    Retrieve top-k relevant documents
    """


    vectorstore = load_vectorstore()


    results = vectorstore.similarity_search(
        query,
        k=k
    )


    return results





def print_results(results):
    """
    Display retrieved documents
    """

    for i, doc in enumerate(results):

        print("\n--------------------")

        print(f"Result {i+1}")

        print("--------------------")

        print(doc.page_content)

        print("\nSource:")
        print(doc.metadata.get("source"))





if __name__ == "__main__":


    query = input(
        "Ask your trading question: "
    )


    results = retrieve_documents(
        query
    )


    print_results(results)