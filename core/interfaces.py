from pydantic import BaseModel
from typing import Optional

class ContextItem(BaseModel):
    content: str
    source: str
    relevance_score: float
    priority: int

class SQLRequest(BaseModel):
    query: str
    data_domain: Optional[str] = None
    thread_id: Optional[str] = None

class SQLResponse(BaseModel):
    sql: Optional[str]
    message: str
    status: str
    thread_id: str
