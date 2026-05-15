from core.state import TextToSQLState
from semantic_layer.providers.grounding import get_grounding

async def grounding_node(state: TextToSQLState):
    print("Executing grounding_node")
    query = state.get("messages", [])[-1].content if state.get("messages") else ""
    
    # Extract domain names from the data_domain dictionary in the state
    data_domain = state.get("data_domain") or {}
    domains = list(data_domain.keys())
    
    # Fetch grounding context for all identified domains
    grounding_context = get_grounding(query, domains)
    
    return {"grounding_context": grounding_context}