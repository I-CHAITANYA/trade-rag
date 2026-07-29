"""
Answer quality scoring and validation
"""
import re
from typing import List, Dict

class AnswerQualityScorer:
    def __init__(self):
        self.quality_checks = [
            self._check_citations,
            self._check_relevance,
            self._check_clarity,
            self._check_completeness,
            self._check_actionability
        ]
    
    def score_answer(self, answer: str, question: str, documents: List) -> Dict:
        """Score the answer quality"""
        scores = {}
        details = {}
        
        for check in self.quality_checks:
            score, detail = check(answer, question, documents)
            scores[check.__name__.replace('_check_', '')] = score
            details[check.__name__.replace('_check_', '')] = detail
        
        overall_score = sum(scores.values()) / len(scores)
        
        return {
            "overall_score": overall_score,
            "scores": scores,
            "details": details,
            "is_good_quality": overall_score >= 0.7
        }
    
    def _check_citations(self, answer: str, question: str, documents: List) -> tuple:
        """Check if answer has proper citations"""
        # Look for citation patterns
        citation_patterns = [
            r'\[Document \d+\]',
            r'\[Source:',
            r'Source:',
            r'📄',
            r'According to'
        ]
        
        has_citations = any(re.search(pattern, answer) for pattern in citation_patterns)
        score = 1.0 if has_citations else 0.0
        detail = "Citations present" if has_citations else "No citations found"
        
        # Bonus for multiple citations
        if has_citations:
            citation_count = len(re.findall(r'\[Document \d+\]', answer))
            if citation_count >= 2:
                score = 1.0
                detail += f" ({citation_count} citations)"
        
        return score, detail
    
    def _check_relevance(self, answer: str, question: str, documents: List) -> tuple:
        """Check if answer is relevant to question"""
        # Extract key terms from question
        question_terms = set(re.findall(r'\b\w+\b', question.lower()))
        answer_terms = set(re.findall(r'\b\w+\b', answer.lower()))
        
        # Calculate overlap
        if question_terms:
            overlap = len(question_terms & answer_terms) / len(question_terms)
            score = min(overlap * 1.5, 1.0)  # Cap at 1.0
        else:
            score = 0.5
        
        detail = f"Relevance score: {score:.2f}"
        return score, detail
    
    def _check_clarity(self, answer: str, question: str, documents: List) -> tuple:
        """Check answer clarity"""
        # Check for structure markers
        structure_markers = [
            r'[0-9]\.',  # Numbered lists
            r'•',        # Bullet points
            r'\*\*',     # Bold text for headings
            r'^#{1,3}',  # Markdown headers
            r'Definition:',
            r'Key Points:',
            r'Summary:'
        ]
        
        has_structure = any(re.search(marker, answer, re.MULTILINE) for marker in structure_markers)
        score = 1.0 if has_structure else 0.5
        
        # Check sentence length
        sentences = [s for s in answer.split('.') if len(s.strip()) > 10]
        avg_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # Penalize very long or very short sentences
        if 10 <= avg_length <= 25:
            score = min(score + 0.2, 1.0)
        
        detail = f"Clarity score: {score:.2f} (Avg sentence length: {avg_length:.0f} words)"
        return score, detail
    
    def _check_completeness(self, answer: str, question: str, documents: List) -> tuple:
        """Check if answer is complete"""
        word_count = len(answer.split())
        
        if word_count < 50:
            score = 0.3
            detail = "Answer is too brief"
        elif word_count < 100:
            score = 0.6
            detail = "Answer has moderate detail"
        else:
            score = 1.0
            detail = "Answer is comprehensive"
        
        return score, detail
    
    def _check_actionability(self, answer: str, question: str, documents: List) -> tuple:
        """Check if answer provides actionable information"""
        actionable_keywords = [
            'use', 'apply', 'implement', 'trade', 'buy', 'sell', 
            'enter', 'exit', 'strategy', 'signal', 'indicator',
            'stop loss', 'take profit', 'risk'
        ]
        
        action_count = sum(1 for keyword in actionable_keywords if keyword in answer.lower())
        score = min(action_count / 5, 1.0)
        
        detail = f"Actionable content: {action_count} action terms found"
        return score, detail

def improve_answer(answer: str, quality_score: Dict) -> str:
    """Suggest improvements based on quality score"""
    improvements = []
    
    if quality_score['scores']['citations'] < 0.8:
        improvements.append("Add source citations using [Document X]")
    
    if quality_score['scores']['clarity'] < 0.7:
        improvements.append("Use numbered lists or bullet points for better structure")
    
    if quality_score['scores']['completeness'] < 0.6:
        improvements.append("Add more details and expand on key points")
    
    if quality_score['scores']['actionability'] < 0.6:
        improvements.append("Include more practical advice and actionable steps")
    
    if improvements:
        answer += "\n\n**💡 Suggested Improvements:**\n" + "\n".join(f"- {imp}" for imp in improvements)
    
    return answer