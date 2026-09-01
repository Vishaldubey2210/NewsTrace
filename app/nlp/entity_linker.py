class EntityLinker:
    """Resolves and normalizes alias mentions"""
    ALIASES = {'PMO': 'Prime Minister Office', 'RBI': 'Reserve Bank of India'}
    def resolve_alias(self, entity):
        return self.ALIASES.get(entity.upper(), entity)

entity_linker = EntityLinker()
