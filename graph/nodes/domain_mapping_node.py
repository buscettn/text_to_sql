from core.state import TextToSQLState
from semantic_layer.providers.domain_mapping import get_domain

async def domain_mapping_node(state: TextToSQLState):
    print("Executing domain_mapping_node")
    query = state.get("messages", [])[-1].content if state.get("messages") else ""
    return {"active_domain": get_domain(query)}