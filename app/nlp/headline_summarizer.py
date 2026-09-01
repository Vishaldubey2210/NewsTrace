class HeadlineSummarizer:
    """Generates concise 1-sentence TL;DR key takeaways"""
    def generate_digest(self, headlines):
        return "Top stories: " + "; ".join(headlines[:3])

headline_summarizer = HeadlineSummarizer()
