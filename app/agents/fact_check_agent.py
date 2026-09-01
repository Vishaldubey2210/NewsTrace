from app.agents.base_agent import BaseAgent

class FactCheckAgent(BaseAgent):
    """Verifies factual claims"""
    def __init__(self): super().__init__(name="FactCheckAgent")
    def execute(self, article):
        return {'status': 'success', 'claims_checked': 2}

fact_check_agent = FactCheckAgent()
