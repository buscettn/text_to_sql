from core.state import TextToSQLState
from semantic_layer.providers.domain_mapping import get_domain

async def domain_mapping_node(state: TextToSQLState):
    print("Executing domain_mapping_node")
    
    # Prioritize requested domain if provided
    requested_domain = state.get("requested_domain")
    if requested_domain:
        # If a single domain is requested, we treat it as 100% confidence
        return {"data_domain": {requested_domain: 1.0}}

    query = state.get("messages", [])[-1].content if state.get("messages") else ""
    domain_scores = get_domain(query)
    return {"data_domain": domain_scores}
