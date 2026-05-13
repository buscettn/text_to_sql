from core.state import TextToSQLState
from components.intent import check_intent

async def intent_node(state: TextToSQLState):
    print("Executing intent_node")
    query = state.get("messages", [])[-1].content if state.get("messages") else ""
    is_valid = check_intent(query)
    if not is_valid:
        return {"status": "error", "agent_message": "Invalid intent"}
    return {}