from core.state import TextToSQLState
from semantic_layer.providers.grounding import get_grounding

async def grounding_node(state: TextToSQLState):
    print("Executing grounding_node")
    query = state.get("messages", [])[-1].content if state.get("messages") else ""
    domain = state.get("active_domain", "")
    return {"grounding_context": get_grounding(query, domain)}