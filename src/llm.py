import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import OPENAI_API_KEY, LLM_MODEL, LLM_PROVIDER
import re
from typing import List, Tuple, Dict

class AdvancedAnswerGenerator:
    def __init__(self):
        self.domain_knowledge = {
            "position_sizing": {
                "keywords": ["position sizing", "risk per trade", "lot size", "money management"],
                "structure": ["Definition", "Why It Matters", "How to Calculate", "Professional Guidelines", "Common Mistakes"],
                "pro_tips": "Start with 1-2% risk per trade and scale up gradually"
            },
            "rsi": {
                "keywords": ["rsi", "relative strength index", "overbought", "oversold"],
                "structure": ["Definition", "Calculation", "How to Read", "Key Signals", "Limitations"],
                "pro_tips": "Look for divergences for stronger signals"
            }
        }
    
    def generate_structured_answer(self, question: str, documents: List, 
                                   conversation_history: List = None) -> Tuple[str, List]:
        """
        Generate a highly structured and synthesized answer
        """
        # Detect the topic
        topic = self._detect_topic(question)
        
        # Extract and synthesize information
        synthesized_content = self._synthesize_content(question, documents, topic)
        
        # Build structured answer
        answer_parts = []
        
        # 1. Direct answer
        answer_parts.append(f"## 📊 Understanding {topic.replace('_', ' ').title()}\n")
        
        # 2. Structured content based on topic
        if topic == "position_sizing":
            answer_parts.extend(self._format_position_sizing(synthesized_content, documents))
        elif topic == "rsi":
            answer_parts.extend(self._format_indicator(synthesized_content, documents, "RSI"))
        else:
            answer_parts.extend(self._format_general(synthesized_content, documents))
        
        # 3. Add pro tips
        if topic in self.domain_knowledge:
            pro_tip = self.domain_knowledge[topic].get("pro_tips", "")
            if pro_tip:
                answer_parts.append(f"\n💡 **Pro Tip:** {pro_tip}")
        
        # 4. Sources
        answer_parts.append("\n---")
        answer_parts.append("### 📚 Sources Used")
        sources = list(set([doc.metadata.get("source", "Unknown") for doc in documents]))
        for idx, source in enumerate(sources, 1):
            answer_parts.append(f"{idx}. {source}")
        
        return "\n".join(answer_parts), sources
    
    def _detect_topic(self, question: str) -> str:
        """Detect the main topic of the question"""
        q_lower = question.lower()
        
        if "position" in q_lower and ("sizing" in q_lower or "size" in q_lower):
            return "position_sizing"
        elif "rsi" in q_lower:
            return "rsi"
        elif "macd" in q_lower:
            return "macd"
        elif "risk" in q_lower and "management" in q_lower:
            return "risk_management"
        else:
            return "general"
    
    def _synthesize_content(self, question: str, documents: List, topic: str) -> Dict:
        """Synthesize content from multiple documents"""
        synthesis = {
            "definition": "",
            "key_points": [],
            "examples": [],
            "guidelines": [],
            "common_mistakes": []
        }
        
        all_content = " ".join([doc.page_content for doc in documents])
        
        # Extract key sentences based on topic
        if topic == "position_sizing":
            # Look for definition
            if "position sizing" in all_content:
                sentences = [s.strip() for s in all_content.split('.') if "position sizing" in s]
                if sentences:
                    synthesis["definition"] = sentences[0] + "."
            
            # Extract key points
            key_phrases = ["position sizing", "mini lot", "risk", "per trade", "account"]
            for phrase in key_phrases:
                if phrase in all_content:
                    sentences = [s.strip() for s in all_content.split('.') if phrase in s.lower()]
                    if sentences:
                        synthesis["key_points"].extend(sentences[:3])
            
            # Extract guidelines
            if "should" in all_content or "must" in all_content:
                guidelines = [s.strip() for s in all_content.split('.') if any(word in s.lower() for word in ["should", "must", "need to", "important"])]
                synthesis["guidelines"] = guidelines[:3]
        
        return synthesis
    
    def _format_position_sizing(self, content: Dict, documents: List) -> List[str]:
        """Format position sizing answer"""
        parts = []
        
        # 1. Definition
        if content["definition"]:
            parts.append(f"### Definition\n{content['definition']}\n")
        else:
            parts.append("### Definition\nPosition sizing refers to determining how many units of a financial instrument to trade based on your account size and risk tolerance.\n")
        
        # 2. Why it matters
        parts.append("### Why Position Sizing Matters\n")
        parts.append("Position sizing is crucial because it:\n")
        parts.append("✅ **Preserves trading capital** - Prevents catastrophic losses\n")
        parts.append("✅ **Manages risk** - Ensures you don't risk too much on any single trade\n")
        parts.append("✅ **Provides consistency** - Helps maintain steady growth\n")
        parts.append("✅ **Reduces emotional stress** - Smaller positions mean less anxiety\n")
        
        # 3. Key Concepts from the document
        if content["key_points"]:
            parts.append("### Key Concepts\n")
            for point in content["key_points"][:3]:
                if point.strip():
                    parts.append(f"• {point}")
            parts.append("")
        
        # 4. How to calculate (using the document's info)
        parts.append("### How to Calculate Position Size\n")
        parts.append("Based on the information provided:\n")
        parts.append("1. **Know your account balance** (e.g., $250)\n")
        parts.append("2. **Define your risk per trade** (typically 1-2% of account)\n")
        parts.append("3. **Understand lot sizes**:\n")
        parts.append("   - Standard lot = 100,000 units\n")
        parts.append("   - Mini lot = 10,000 units\n")
        parts.append("   - Micro lot = 1,000 units\n")
        if "mini lot" in str(content):
            parts.append("4. **Think in dollars, not pips**: Calculate your position size based on dollar risk\n")
        
        # 5. Professional guidelines
        parts.append("### Professional Guidelines\n")
        parts.append("• Never risk more than 1-2% of your account per trade\n")
        parts.append("• Consider volatility when sizing positions\n")
        parts.append("• Scale position size as your account grows\n")
        parts.append("• Use stop-losses to define your maximum loss\n")
        
        # 6. Common mistakes
        parts.append("### Common Mistakes\n")
        parts.append("❌ Risking too much per trade (gambling)\n")
        parts.append("❌ Not adjusting position size for market conditions\n")
        parts.append("❌ Emotional decision-making leading to oversized positions\n")
        parts.append("❌ Trading with inconsistent position sizing\n")
        
        return parts
    
    def _format_indicator(self, content: Dict, documents: List, indicator_name: str) -> List[str]:
        """Format indicator answers"""
        parts = []
        
        parts.append(f"### What is {indicator_name}?\n")
        parts.append(f"{indicator_name} is a technical analysis tool used by traders to...\n")
        
        parts.append("### How to Use It\n")
        parts.append("• **Entry signals**: Use when...\n")
        parts.append("• **Exit signals**: Look for...\n")
        parts.append("• **Confirmation**: Combine with other indicators\n")
        
        return parts
    
    def _format_general(self, content: Dict, documents: List) -> List[str]:
        """Format general answers"""
        parts = []
        
        parts.append("### Overview\n")
        
        # Extract and format key points
        if content["key_points"]:
            for point in content["key_points"][:4]:
                if point.strip():
                    parts.append(f"• {point}")
        else:
            # Use document content
            for doc in documents[:2]:
                content = doc.page_content.strip()[:200]
                if content:
                    parts.append(f"• {content}...")
        
        return parts
    
    def _extract_key_concepts(self, text: str, num_concepts: int = 5) -> List[str]:
        """Extract key concepts from text"""
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        return sentences[:num_concepts]

# Global instance
answer_generator = AdvancedAnswerGenerator()

def generate_answer(question, documents, conversation_history=None):
    """Generate improved structured answer"""
    if not documents:
        return "I don't have enough information in my knowledge base. Please add more documents about this topic.", []
    
    # Try OpenAI if available
    if LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            # Use the structured generator
            prompt = _create_advanced_prompt(question, documents)
            
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": """You are a professional trading educator. 
                    Structure your answers with clear sections, use markdown formatting, 
                    and provide practical, actionable advice. 
                    Always cite sources."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            answer = response.choices[0].message.content
            sources = list(set([doc.metadata.get("source", "Unknown") for doc in documents]))
            return answer, sources
            
        except Exception as e:
            print(f"OpenAI error: {e}")
    
    # Fallback to structured local answer
    return answer_generator.generate_structured_answer(question, documents, conversation_history)

def _create_advanced_prompt(question: str, documents: List) -> str:
    """Create an advanced prompt for OpenAI"""
    context = ""
    for i, doc in enumerate(documents, 1):
        context += f"""
[Document {i}] Source: {doc.metadata.get('source', 'Unknown')}
{doc.page_content}
"""
    
    return f"""
You are a professional trading educator. Answer the following question using ONLY the provided context.

Question: {question}

Context:
{context}

Requirements for your answer:
1. Start with a clear definition
2. Use markdown formatting (headers, bullet points, bold)
3. Structure with sections: Definition, Why It Matters, How to Use, Key Takeaways
4. Include practical, actionable advice
5. End with a summary
6. Cite sources using [Document X]

Your answer:
"""