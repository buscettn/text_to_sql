# PRD: Core Engine Facade

## 1. Objective
Establish a clean, framework-agnostic entry point for the Text-to-SQL system that encapsulates all LangGraph orchestration. This ensures that external interfaces (UI, CLI, SDK) interact exclusively through pure Python Pydantic models (`SQLRequest`, `SQLResponse`) without ever being exposed to LangChain/LangGraph-specific types (like `HumanMessage` or `TextToSQLState`).

## 2. Problem Statement
Currently, to run the graph (as seen in `main.py`), the caller must import LangChain message classes (`HumanMessage`) and manually construct the LangGraph state dictionary. This violates Hexagonal Architecture principles by leaking orchestration framework details into the presentation and access layers. If the UI, CLI, or SDK depend on LangChain, the system becomes tightly coupled and harder to test or swap frameworks in the future.

## 3. Proposed Solution
Create an `Engine` class (e.g., in `core/engine.py`) that serves as the single "front door" to the application. 
- The `Engine` accepts an `SQLRequest` from `core.interfaces`.
- It maps the `SQLRequest` properties into primitive dictionary representations (LangGraph natively supports raw `{"role": "user", "content": "..."}` dicts, avoiding the need for `HumanMessage` imports in the core).
- It executes the LangGraph workflow (`create_workflow()`).
- It extracts the results from the final graph state and constructs a clean `SQLResponse`.

By using raw dictionaries for the message history, the `Engine` itself does not even need to import LangChain or LangGraph (other than executing the compiled `app` returned by `create_workflow`).

## 4. Technical Design

### 4.1 Component: `core/engine.py`
The module will define a `TextToSQLEngine` class.

**Dependencies:**
- `core.interfaces` (`SQLRequest`, `SQLResponse`)
- `graph.workflow` (`create_workflow`)
- *No LangChain or LangGraph imports.*

**Class Structure:**
```python
from core.interfaces import SQLRequest, SQLResponse
from graph.workflow import create_workflow
import uuid

class TextToSQLEngine:
    def __init__(self):
        # Initialize the LangGraph app once
        self.app = create_workflow()

    async def ainvoke(self, request: SQLRequest) -> SQLResponse:
        """
        Single-turn execution. Waits for the workflow to complete and returns the final response.
        """
        pass

    async def astream(self, request: SQLRequest):
        """
        Streaming execution. Yields status updates for the UI/CLI, and finally yields the SQLResponse.
        """
        pass
```

### 4.2 State Translation Layer
The Engine handles translation to and from the graph state purely through primitive Python types:

**Request -> State:**
```python
thread_id = request.thread_id or str(uuid.uuid4())
initial_state = {
    # Using primitive dict instead of HumanMessage avoids Langchain imports
    "messages": [{"role": "user", "content": request.query}],
    "requested_domain": request.data_domain,
    # default other state fields...
}
config = {"configurable": {"thread_id": thread_id}}
```

**State -> Response:**
```python
# Assuming 'final_state' is the dictionary output from app.ainvoke
response = SQLResponse(
    sql=final_state.get("generated_sql"),
    message=final_state.get("agent_message", "No response generated."),
    status=final_state.get("status", "error"),
    thread_id=thread_id
)
```

## 5. Acceptance Criteria
1. **Single Entry Point:** `core/engine.py` provides the only interface needed to interact with the system.
2. **Framework Isolation:** The `ui/`, `cli/`, `sdk/`, and `core/engine.py` directories contain absolutely zero imports from `langchain`, `langchain_core`, or `langgraph`.
3. **Data Contracts:** The entry point strictly accepts `SQLRequest` and returns `SQLResponse`.
4. **Thread Management:** The engine automatically generates a `thread_id` if one is not provided in the `SQLRequest`, and returns it in the `SQLResponse` for conversational memory.
5. **Streaming Support:** The engine provides an asynchronous streaming method so the UI can hook into LangGraph's event stream for progress indicators, without importing LangGraph.
