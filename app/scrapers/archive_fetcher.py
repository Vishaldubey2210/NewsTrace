import requests

class ArchiveFetcher:
    """Fetches historical snapshots from Wayback Machine"""
    def get_snapshot(self, url):
        try:
            r = requests.get("https://archive.org/wayback/available", params={'url': url}, timeout=5)
            if r.status_code == 200:
                return r.json().get('archived_snapshots', {}).get('closest', {}).get('url')
        except Exception:
            pass
        return None

archive_fetcher = ArchiveFetcher()
