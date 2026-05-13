from core.interfaces import ContextItem

def get_schema(domain: str) -> list:
    return [ContextItem(content="CREATE TABLE dummy (id INT);", source="schema", relevance_score=1.0, priority=1)]