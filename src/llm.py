import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import OPENAI_API_KEY, LLM_MODEL, LLM_PROVIDER


def create_prompt(question, documents):
    """
    Create prompt using retrieved context.
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


def _build_local_answer(question, documents):
    """
    Generate a simple answer from the retrieved context without any external API.
    """
    if not documents:
        return "I don't have enough information in my knowledge base."

    context_parts = []
    for doc in documents[:3]:
        source = doc.metadata.get("source", "unknown")
        content = (doc.page_content or "").strip()
        if content:
            context_parts.append(f"- {source}: {content}")

    context_text = "\n".join(context_parts)

    answer = (
        f"Based on the retrieved context, here is a concise answer to your question: \n\n"
        f"{question}\n\n"
        f"{context_text}"
    )

    if len(answer) > 800:
        answer = answer[:800].rstrip() + "..."

    return answer


def generate_answer(question, documents):
    """
    Generate an answer using the local fallback by default.
    """
    if LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=OPENAI_API_KEY)
            prompt = create_prompt(question, documents)
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception:
            pass

    return _build_local_answer(question, documents)


if __name__ == "__main__":
    from retriever import retrieve_documents

    question = input("Ask your trading question: ")
    docs = retrieve_documents(question)
    answer = generate_answer(question, docs)

    print("\nAnswer:")
    print(answer)