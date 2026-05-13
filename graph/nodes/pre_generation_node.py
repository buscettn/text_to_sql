from core.state import TextToSQLState
from components.pre_generation import check_pre_generation

async def pre_generation_node(state: TextToSQLState):
    print("Executing pre_generation_node")
    is_ready = check_pre_generation(state)
    if not is_ready:
        return {"status": "error", "agent_message": "Pre-generation check failed"}
    return {}