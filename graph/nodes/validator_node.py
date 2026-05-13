from core.state import TextToSQLState
from components.validator import validate_and_fix_sql

async def validator_node(state: TextToSQLState):
    print("Executing validator_node")
    sql = state.get("generated_sql", "")
    
    if not sql:
        return {"status": "error", "validation_errors": "No SQL generated."}
        
    is_valid, result = validate_and_fix_sql(sql)
    
    if is_valid:
        return {
            "status": "success", 
            "agent_message": "SQL generated and validated",
            "generated_sql": result,
            "validation_errors": None
        }
    else:
        return {
            "status": "error", 
            "validation_errors": result
        }