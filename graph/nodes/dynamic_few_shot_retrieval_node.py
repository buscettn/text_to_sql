from core.state import TextToSQLState
from semantic_layer.providers.dynamic_few_shot_retrieval import get_few_shot

async def dynamic_few_shot_retrieval_node(state: TextToSQLState):
    print("Executing dynamic_few_shot_retrieval_node")
    query = state.get("messages", [])[-1].content if state.get("messages") else ""
    domain_scores = state.get("data_domain") or {}
    
    all_few_shots = []
    for domain in domain_scores.keys():
        few_shots = get_few_shot(query, domain)
        if few_shots:
            all_few_shots.extend(few_shots)
            
    return {"few_shot_context": all_few_shots}