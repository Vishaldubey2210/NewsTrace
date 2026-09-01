class PaywallDetector:
    """Detects paywalled articles"""
    def is_paywalled(self, text):
        return any(m in (text or "").lower() for m in ['subscribe to read', 'premium article', 'members only'])

paywall_detector = PaywallDetector()
