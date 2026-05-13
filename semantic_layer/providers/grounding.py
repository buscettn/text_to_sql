from core.interfaces import ContextItem

def get_grounding(query: str, domain: str) -> list:
    return [ContextItem(content="Dummy rule: use dummy table.", source="grounding", relevance_score=0.8, priority=3)]