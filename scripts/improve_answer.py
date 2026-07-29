"""
Script to test and improve answer quality
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.retriever import retrieve_documents
from src.llm import generate_answer
from src.answer_quality import AnswerQualityScorer

def test_answers():
    """Test answers for common questions"""
    test_questions = [
        "What is RSI and how do I use it?",
        "Explain MACD crossover strategy",
        "How do I manage risk in trading?",
        "What's the difference between SMA and EMA?",
        "How to identify trend reversals?"
    ]
    
    quality_scorer = AnswerQualityScorer()
    
    print("=" * 80)
    print("📊 TESTING ANSWER QUALITY")
    print("=" * 80)
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        print("-" * 40)
        
        # Retrieve and generate
        documents = retrieve_documents(question, k=3)
        answer, sources = generate_answer(question, documents)
        
        # Score quality
        quality = quality_scorer.score_answer(answer, question, documents)
        
        # Show results
        print(f"📝 Answer (first 200 chars): {answer[:200]}...")
        print(f"\n📊 Quality Score: {quality['overall_score']:.2%}")
        print(f"   Citations: {quality['scores']['citations']:.2%}")
        print(f"   Relevance: {quality['scores']['relevance']:.2%}")
        print(f"   Clarity: {quality['scores']['clarity']:.2%}")
        print(f"   Completeness: {quality['scores']['completeness']:.2%}")
        print(f"   Actionability: {quality['scores']['actionability']:.2%}")
        
        if quality['overall_score'] < 0.7:
            print("⚠️ Quality issues detected:")
            for metric, detail in quality['details'].items():
                if "No citations" in detail or "brief" in detail.lower():
                    print(f"   - {detail}")
        
        print("-" * 40)
        print()

if __name__ == "__main__":
    test_answers()