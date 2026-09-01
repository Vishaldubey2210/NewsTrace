class BylineNetworkBuilder:
    """Builds co-authorship collaboration networks"""
    def build_pairs(self, articles):
        pairs = []
        for a in articles:
            auths = a.get('authors', [])
            if len(auths) > 1:
                pairs.append({'author_1': auths[0], 'author_2': auths[1]})
        return pairs

byline_network_builder = BylineNetworkBuilder()
