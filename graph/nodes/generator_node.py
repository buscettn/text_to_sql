from core.state import TextToSQLState
from components.generator import generate_sql, ContextBuilder

async def generator_node(state: TextToSQLState):
    print("Executing generator_node")
    
    schema_context = state.get("schema_context", [])
    few_shot_context = state.get("few_shot_context", [])
    grounding_context = state.get("grounding_context", [])
    
    builder = ContextBuilder()
    context = builder.build_context(schema_context, few_shot_context, grounding_context)
    
    messages = state.get("messages", [])
    query = messages[-1].content if messages else ""
    
    return {
        "generated_sql": generate_sql(context, query), 
        "generation_attempts": state.get("generation_attempts", 0) + 1
    }