from openai import OpenAI

from config import OPENAI_API_KEY, LLM_MODEL


client = OpenAI(
    api_key=OPENAI_API_KEY
)



def create_prompt(question, documents):
    """
    Create prompt using retrieved context
    """


    context = ""


    for doc in documents:

        context += (
            "\nSource: "
            + doc.metadata.get("source", "unknown")
            + "\n"
        )

        context += doc.page_content

        context += "\n\n"



    prompt = f"""

You are TradeRAG, an AI assistant
specialized in trading education.

Answer the user's question using only
the provided context.

If the answer is not present in the
context, say:

"I don't have enough information
in my knowledge base."

Do not provide financial advice.
Only explain concepts.

Context:

{context}


Question:

{question}


Answer:

"""


    return prompt





def generate_answer(question, documents):
    """
    Generate answer using LLM
    """


    prompt = create_prompt(
        question,
        documents
    )


    response = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        temperature=0.2
    )


    answer = (
        response
        .choices[0]
        .message
        .content
    )


    return answer





if __name__ == "__main__":

    from retriever import retrieve_documents


    question = input(
        "Ask your trading question: "
    )


    docs = retrieve_documents(
        question
    )


    answer = generate_answer(
        question,
        docs
    )


    print("\nAnswer:")
    print(answer)