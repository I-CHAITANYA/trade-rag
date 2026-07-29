"""
Refine answers for better quality
"""
import re

class AnswerRefiner:
    def __init__(self):
        self.refinement_rules = [
            self._add_structure,
            self._enhance_examples,
            self._add_summary,
            self._check_detailed_explanation
        ]
    
    def refine(self, answer: str) -> str:
        """Apply refinement rules to improve answer"""
        for rule in self.refinement_rules:
            answer = rule(answer)
        return answer
    
    def _add_structure(self, answer: str) -> str:
        """Add structure if missing"""
        # Check if answer has structure markers
        if not any(marker in answer for marker in ['1.', '•', '**']):
            # Try to add structure by splitting on key phrases
            parts = re.split(r'(Definition:|Key Points:|How to Use:|Summary:)', answer)
            if len(parts) > 1:
                structured = ""
                for i in range(0, len(parts)-1, 2):
                    structured += f"\n**{parts[i]}**\n{parts[i+1].strip()}\n"
                return structured.strip()
        return answer
    
    def _enhance_examples(self, answer: str) -> str:
        """Add examples if missing"""
        if 'example' not in answer.lower() and 'for instance' not in answer.lower():
            # Check if we can infer an example
            if 'when' in answer.lower() or 'if' in answer.lower():
                answer += "\n\n**Example:** Consider a scenario where this principle is applied in practice."
        return answer
    
    def _add_summary(self, answer: str) -> str:
        """Add summary section if missing"""
        if not answer.strip().endswith('summary') and 'summary' not in answer.lower():
            # Add a summary if answer is long enough
            if len(answer.split()) > 100:
                # Extract key points for summary
                sentences = [s for s in answer.split('.') if len(s.split()) > 10]
                if sentences:
                    summary_points = sentences[:3]
                    answer += f"\n\n**Summary:** {'. '.join(summary_points)}."
        return answer
    
    def _check_detailed_explanation(self, answer: str) -> str:
        """Ensure answer has sufficient detail"""
        word_count = len(answer.split())
        if word_count < 100:
            answer += "\n\nFor a more detailed explanation, consider exploring the source documents provided above."
        return answer