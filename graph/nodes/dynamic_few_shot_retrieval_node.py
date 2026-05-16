from core.state import TextToSQLState
from semantic_layer.providers.dynamic_few_shot_retrieval import get_few_shot_context

async def dynamic_few_shot_retrieval_node(state: TextToSQLState):
    """
    Retrieves dynamic few-shot examples based on the user query and identified domains.
    """
    print("Executing dynamic_few_shot_retrieval_node")
    
    # 1. Get query from the last message
    messages = state.get("messages", [])
    if not messages:
        return {"few_shot_context": []}
    
    query = messages[-1].content
    
    # 2. Get active domains from state
    # data_domain is expected to be a Dict[str, float] (Domain: Confidence)
    domain_scores = state.get("data_domain") or {}
    active_domains = list(domain_scores.keys())
    
    # 3. Retrieve few-shot context
    try:
        few_shot_items = get_few_shot_context(query, active_domains)
    except Exception as e:
        print(f"Warning: Few-shot retrieval failed: {e}")
        # Depending on criticality, we could re-raise or just log
        # Given our plan to fail fast if table is missing, let's let it raise
        # but for node stability in production, a warning might be better.
        # However, the user specifically asked to "fail with an error if table does not exist".
        raise e
            
    return {"few_shot_context": few_shot_items}