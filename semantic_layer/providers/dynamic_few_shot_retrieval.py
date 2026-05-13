from core.interfaces import ContextItem

def get_few_shot(query: str, domain: str) -> list:
    return [ContextItem(content="SELECT * FROM dummy;", source="few_shot", relevance_score=0.9, priority=2)]