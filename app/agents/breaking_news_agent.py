from app.agents.base_agent import BaseAgent

class BreakingNewsAgent(BaseAgent):
    """Monitors live news spikes"""
    def __init__(self): super().__init__(name="BreakingNewsAgent")
    def execute(self, feed):
        return {'breaking': [f for f in feed if 'breaking' in f.get('title', '').lower()]}

breaking_news_agent = BreakingNewsAgent()
