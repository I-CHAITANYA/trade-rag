"""
Domain knowledge base to supplement retrieved documents
"""
class TradingKnowledgeBase:
    def __init__(self):
        self.knowledge = {
            "position_sizing": {
                "definition": "Position sizing is the process of determining how much of a financial instrument to trade based on your account size and risk tolerance.",
                "formula": "Position Size = (Account Balance × Risk %) / (Stop Loss Distance)",
                "guidelines": [
                    "Risk 1-2% of account per trade",
                    "Use stop-losses to define risk",
                    "Adjust position size based on market volatility",
                    "Scale up gradually as account grows",
                    "Never risk more than you can afford to lose"
                ],
                "common_mistakes": [
                    "Over-leveraging positions",
                    "Inconsistent position sizing",
                    "Emotional decisions leading to oversized trades",
                    "Not factoring in market conditions"
                ],
                "example": "If you have a $10,000 account and risk 1% ($100) with a 50-pip stop loss, your position size would be 2 mini lots."
            },
            "rsi": {
                "definition": "The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements.",
                "formula": "RSI = 100 - (100 / (1 + RS)) where RS = Average Gain / Average Loss",
                "guidelines": [
                    "RSI above 70 indicates overbought",
                    "RSI below 30 indicates oversold",
                    "Divergence signals potential reversals",
                    "50 is the centerline (bullish above, bearish below)"
                ]
            }
        }
    
    def get_knowledge(self, topic: str) -> dict:
        """Get domain knowledge for a topic"""
        return self.knowledge.get(topic, {})
    
    def augment_documents(self, question: str, documents: list) -> list:
        """Add domain knowledge to retrieved documents"""
        # Detect topic
        if "position" in question.lower() and ("sizing" in question.lower() or "size" in question.lower()):
            knowledge = self.knowledge.get("position_sizing", {})
        elif "rsi" in question.lower():
            knowledge = self.knowledge.get("rsi", {})
        else:
            return documents
        
        # Create a knowledge document
        if knowledge:
            knowledge_doc = type('Document', (), {
                'page_content': f"""
                Domain Knowledge for Position Sizing:
                Definition: {knowledge.get('definition', '')}
                
                Key Guidelines:
                {chr(10).join(['- ' + g for g in knowledge.get('guidelines', [])])}
                
                Formula: {knowledge.get('formula', 'N/A')}
                
                Common Mistakes:
                {chr(10).join(['- ' + m for m in knowledge.get('common_mistakes', [])])}
                """,
                'metadata': {'source': 'Knowledge Base', 'type': 'foundational'}
            })
            
            # Add knowledge document to the front
            documents.insert(0, knowledge_doc)
        
        return documents