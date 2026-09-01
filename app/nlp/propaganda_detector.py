import re

class PropagandaDetector:
    """Identifies common propaganda and persuasive rhetorical techniques in news articles"""
    def __init__(self):
        self.techniques = {
            'Loaded Language': re.compile(r'\b(monstrous|tyrannical|pure evil|barbaric)\b', re.IGNORECASE),
            'Name Calling': re.compile(r'\b(puppet|clown|traitor|fascist)\b', re.IGNORECASE),
            'Appeal to Fear': re.compile(r'\b(imminent doom|existential threat|wipe out)\b', re.IGNORECASE)
        }

    def detect_techniques(self, text):
        if not text:
            return {'flagged': False, 'detected_techniques': []}
        found = []
        for name, pattern in self.techniques.items():
            matches = pattern.findall(text)
            if matches:
                found.append({'technique': name, 'count': len(matches)})
        return {'flagged': len(found) > 0, 'detected_techniques': found}

propaganda_detector = PropagandaDetector()
