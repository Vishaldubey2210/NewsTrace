from app.agents.base_agent import BaseAgent

class DigestAgent(BaseAgent):
    """Compiles executive morning news briefing"""
    def __init__(self): super().__init__(name="DigestAgent")
    def execute(self, data):
        return {'summary': 'Daily media intelligence briefing generated.'}

digest_agent = DigestAgent()
