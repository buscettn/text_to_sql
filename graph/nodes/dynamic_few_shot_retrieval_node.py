from core.state import TextToSQLState
from semantic_layer.providers.dynamic_few_shot_retrieval import get_few_shot

async def dynamic_few_shot_retrieval_node(state: TextToSQLState):
    print("Executing dynamic_few_shot_retrieval_node")
    query = state.get("messages", [])[-1].content if state.get("messages") else ""
    domain = state.get("active_domain", "")
    return {"few_shot_context": get_few_shot(query, domain)}