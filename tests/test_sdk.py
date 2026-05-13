import asyncio
import pytest
from sdk import TextToSQLEngine, SQLRequest, SQLResponse

def test_sdk_imports_and_execution():
    engine = TextToSQLEngine()
    request = SQLRequest(query="Test SDK execution")
    
    async def run():
        return await engine.ainvoke(request)
        
    response = asyncio.run(run())
    
    assert isinstance(response, SQLResponse)
    assert response.status == "success"
    assert response.sql is not None
