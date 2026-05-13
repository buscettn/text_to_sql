import pytest
import asyncio
from core.engine import TextToSQLEngine
from core.interfaces import SQLRequest, SQLResponse

def test_engine_ainvoke():
    engine = TextToSQLEngine()
    request = SQLRequest(query="Show me all users")
    
    async def run():
        return await engine.ainvoke(request)
    
    response = asyncio.run(run())
    
    assert isinstance(response, SQLResponse)
    assert response.thread_id is not None
    assert response.status == "success"
    assert "SELECT" in response.sql and "dummy_table" in response.sql

def test_engine_astream():
    engine = TextToSQLEngine()
    request = SQLRequest(query="Show me all users")
    
    async def run():
        events = []
        async for output in engine.astream(request):
            events.append(output)
        return events
        
    events = asyncio.run(run())
    final_response = events[-1]
    
    assert isinstance(final_response, SQLResponse)
    assert final_response.thread_id is not None
    assert final_response.status == "success"
    assert "SELECT" in final_response.sql and "dummy_table" in final_response.sql
    # the rest of the events should be dicts (state updates)
    assert all(isinstance(e, dict) for e in events[:-1])

