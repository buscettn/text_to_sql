from typing import List
from core.interfaces import ContextItem

class ContextBuilder:
    def build_context(
        self, 
        schema_context: List[ContextItem],
        few_shot_context: List[ContextItem],
        grounding_context: List[ContextItem]
    ) -> str:
        # Combine all items
        all_items = schema_context + few_shot_context + grounding_context
        
        # Sort by priority (lower is better, e.g. 1 is Critical) and relevance (higher is better)
        all_items.sort(key=lambda x: (x.priority, -x.relevance_score))
        
        # Concatenate
        return "\n\n".join([item.content for item in all_items])

def generate_sql(context: str, query: str) -> str:
    #return query + "\n\n" + context
    return "SELECT * FROM dummy_table;"