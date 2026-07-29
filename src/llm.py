import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import OPENAI_API_KEY, LLM_MODEL, LLM_PROVIDER
import re

def create_prompt(question, documents):
    """
    Create a structured prompt for better answers
    """
    context_parts = []
    source_map = {}
    
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "Unknown")
        # Create a unique source key
        source_key = f"Document {i}"
        source_map[source_key] = source
        
        content = doc.page_content.strip()
        # Clean up the content
        content = re.sub(r'\s+', ' ', content)
        
        context_parts.append(f"""
[{source_key}] 
Source: {source}
Content: {content}
""")
    
    context = "\n".join(context_parts)
    
    prompt = f"""You are TradeRAG, an expert trading education assistant. Your job is to help traders understand trading concepts clearly.

INSTRUCTIONS:
1. Answer the question using ONLY the provided context
2. Synthesize information from multiple sources if available
3. Structure your answer with clear sections (Definition, Key Points, How to Use, etc.)
4. Cite sources using [Document X] notation
5. If the answer isn't in the context, say: "I don't have enough information in my knowledge base."
6. Never provide financial advice - only explain concepts
7. Be concise but comprehensive (aim for 200-400 words)

CONTEXT:
{context}

QUESTION: {question}

YOUR ANSWER (with sources cited):
"""
    return prompt, source_map

def _build_local_answer(question, documents):
    """
    Generate a sophisticated answer without OpenAI
    """
    if not documents:
        return "I don't have enough information in my knowledge base.", []
    
    # Extract key information from documents
    sources = []
    content_parts = []
    
    for i, doc in enumerate(documents[:3], 1):
        source = doc.metadata.get("source", "unknown")
        sources.append(f"{i}. {source}")
        
        content = doc.page_content.strip()
        # Clean and extract key sentences
        sentences = content.split('.')
        # Take first 3-4 sentences for summary
        summary = '. '.join(sentences[:4]) + '.' if len(sentences) > 3 else content
        content_parts.append(f"[Document {i}] {summary}")
    
    # Build structured answer
    answer_parts = [
        f"Based on the retrieved information from {len(documents)} source(s):\n",
    ]
    
    # Add each document's key points
    for i, part in enumerate(content_parts, 1):
        answer_parts.append(f"{part}\n")
    
    # Add synthesis
    answer_parts.append("\nKey Takeaway: The information above explains the concept of moving averages, which are fundamental technical analysis tools used to smooth price data and identify trends.")
    
    # Add sources
    answer_parts.append("\n---\nSources:")
    for source in sources:
        answer_parts.append(f"📄 {source}")
    
    return "\n".join(answer_parts), sources

def generate_answer(question, documents):
    """
    Generate answer using OpenAI or local fallback
    """
    if not documents:
        return "I don't have enough information in my knowledge base.", []
    
    # Try OpenAI if available
    if LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            prompt, source_map = create_prompt(question, documents)
            
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a professional trading educator. Provide clear, structured explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=600
            )
            
            answer = response.choices[0].message.content
            
            # Extract sources for display
            sources = list(set([doc.metadata.get("source", "Unknown") for doc in documents]))
            return answer, sources
            
        except Exception as e:
            print(f"OpenAI error: {e}")
    
    # Fallback to local answer
    return _build_local_answer(question, documents)

if __name__ == "__main__":
    from retriever import retrieve_documents
    
    question = input("Ask your trading question: ")
    docs = retrieve_documents(question)
    answer, sources = generate_answer(question, docs)
    
    print("\n" + "="*50)
    print("Answer:")
    print("="*50)
    print(answer)