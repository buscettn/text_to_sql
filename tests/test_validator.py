import pytest
from components.validator import validate_and_fix_sql
from graph.nodes.validator_node import validator_node
from core.state import TextToSQLState

def test_validate_and_fix_sql_valid():
    sql = "SELECT * FROM users WHERE id = 1"
    is_valid, result = validate_and_fix_sql(sql)
    assert is_valid is True
    # The result should be syntactically similar, with potential backticks or formatting
    assert "SELECT" in result
    assert "users" in result
    assert "id" in result

def test_validate_and_fix_sql_invalid():
    sql = "SELECT * FRO users WHERE"
    is_valid, result = validate_and_fix_sql(sql)
    assert is_valid is False
    assert "Parse Error" in result or "SQL Error" in result

def test_validate_and_fix_sql_empty():
    sql = "   "
    is_valid, result = validate_and_fix_sql(sql)
    assert is_valid is False
    assert "Empty SQL query" in result

def test_validate_and_fix_sql_transpile_dialect():
    # Test a function that might be valid in one but gets transpiled to Impala/Hive standard
    # e.g., string concatenation
    sql = "SELECT 'a' || 'b'"
    is_valid, result = validate_and_fix_sql(sql)
    assert is_valid is True
    # In hive/impala, concat is commonly transpiled, or at least the query parses correctly
    assert result is not None

def test_validator_node_valid():
    state = TextToSQLState(
        messages=[],
        requested_domain=None,
        data_domain=None,
        schema_context=[],
        few_shot_context=[],
        grounding_context=[],
        generated_sql="SELECT * FROM table1",
        validation_errors=None,
        generation_attempts=1,
        status="running",
        agent_message=None
    )
    import asyncio
    async def run():
        return await validator_node(state)
    result_state = asyncio.run(run())
    assert result_state["status"] == "success"
    assert result_state["validation_errors"] is None
    assert "SELECT" in result_state["generated_sql"]
    assert "table1" in result_state["generated_sql"]
    assert result_state["agent_message"] == "SQL generated and validated"

def test_validator_node_invalid():
    state = TextToSQLState(
        messages=[],
        requested_domain=None,
        data_domain=None,
        schema_context=[],
        few_shot_context=[],
        grounding_context=[],
        generated_sql="SELECT * FRO table1",
        validation_errors=None,
        generation_attempts=1,
        status="running",
        agent_message=None
    )
    import asyncio
    async def run():
        return await validator_node(state)
    result_state = asyncio.run(run())
    assert result_state["status"] == "error"
    assert result_state["validation_errors"] is not None
    assert "Parse Error" in result_state["validation_errors"] or "SQL Error" in result_state["validation_errors"]

def test_validator_node_no_sql():
    state = TextToSQLState(
        messages=[],
        requested_domain=None,
        data_domain=None,
        schema_context=[],
        few_shot_context=[],
        grounding_context=[],
        generated_sql="",
        validation_errors=None,
        generation_attempts=1,
        status="running",
        agent_message=None
    )
    import asyncio
    async def run():
        return await validator_node(state)
    result_state = asyncio.run(run())
    assert result_state["status"] == "error"
    assert "No SQL generated" in result_state["validation_errors"]
