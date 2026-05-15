from typing import TypedDict, Annotated, List, Optional, Dict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from core.interfaces import ContextItem

class TextToSQLState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    requested_domain: Optional[str]
    data_domain: Optional[Dict[str, float]]
    schema_context: List[ContextItem]
    few_shot_context: List[ContextItem]
    grounding_context: List[ContextItem]
    generated_sql: Optional[str]
    validation_errors: Optional[str]
    generation_attempts: int 
    status: str 
    agent_message: Optional[str] 
