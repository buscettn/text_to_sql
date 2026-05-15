from core.state import TextToSQLState
from semantic_layer.providers.schema_retrieval import get_schema

async def schema_retrieval_node(state: TextToSQLState):
    print("Executing schema_retrieval_node")
    domain_scores = state.get("data_domain") or {}
    
    all_schemas = []
    for domain in domain_scores.keys():
        schemas = get_schema(domain)
        if schemas:
            all_schemas.extend(schemas)
            
    return {"schema_context": all_schemas}