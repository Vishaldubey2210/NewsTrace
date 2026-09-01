import re

class TimelineExtractor:
    """Extracts chronological event timeline milestones mentioned across a journalist's coverage"""
    def extract_timeline(self, articles):
        events = []
        yp = re.compile(r'\b(20[0-2][0-9]|19[89][0-9])\b')
        for art in articles:
            for y in set(yp.findall(art.get('title', ''))):
                events.append({'year': int(y), 'headline': art.get('title')})
        events.sort(key=lambda x: x['year'])
        return events[:15]

timeline_extractor = TimelineExtractor()
