from core.state import TextToSQLState
from semantic_layer.providers.schema_retrieval import get_schema

async def schema_retrieval_node(state: TextToSQLState):
    print("Executing schema_retrieval_node")
    domain = state.get("data_domain", "")
    return {"schema_context": get_schema(domain)}