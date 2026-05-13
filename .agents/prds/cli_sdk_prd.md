# PRD: CLI and SDK Implementation

## 1. Objective
Establish the primary usage interfaces for the Text-to-SQL system as defined in the system architecture. The SDK will provide a clean programmatic interface for Python developers, while the CLI will provide a terminal-based interface for end-users to generate SQL from natural language. Both will interact exclusively with the `core.engine.TextToSQLEngine`.

## 2. SDK Design
The SDK serves as the public Python API for the application. Since the `TextToSQLEngine` already abstracts away LangChain/LangGraph orchestration, the SDK simply needs to expose these core components cleanly.

**Implementation:**
- Create `sdk/__init__.py`.
- Expose `TextToSQLEngine`, `SQLRequest`, and `SQLResponse` so users can import them directly from `sdk`.
```python
# Usage Example
from sdk import TextToSQLEngine, SQLRequest

engine = TextToSQLEngine()
response = await engine.ainvoke(SQLRequest(query="Show me all users"))
```

## 3. CLI Design
The CLI provides a command-line interface for testing and interacting with the system without writing code.

**Implementation:**
- Create `cli/main.py` containing the CLI logic.
- Use `argparse` to handle command-line arguments.
- Supported Arguments:
  - `query` (positional or `--query`): The natural language query to translate.
  - `--domain`: (Optional) The specific data domain to target.
  - `--stream`: (Optional, boolean flag) If provided, the CLI will stream progress updates from the engine's `astream` method. Otherwise, it will use `ainvoke`.
- The CLI must handle the `asyncio` event loop setup.

## 4. Refactoring `main.py`
Currently, `main.py` hardcodes a specific execution flow. It should be refactored to act as the primary entry point for the CLI.

**Implementation:**
- `main.py` will import the CLI runner and execute it.
```python
import sys
from cli.main import run_cli

if __name__ == "__main__":
    run_cli()
```

## 5. Acceptance Criteria
1. **SDK Accessibility**: Developers can import `TextToSQLEngine`, `SQLRequest`, and `SQLResponse` directly from the `sdk` package.
2. **CLI Functionality**: The CLI correctly parses arguments, invokes the engine, and prints the result.
3. **Streaming Support**: The CLI supports both synchronous invocation and streaming progress updates via a `--stream` flag.
4. **Root Entry Point**: Running `python main.py "My query"` successfully executes the CLI.
5. **Testing**: Both the CLI and SDK integration pass basic execution tests.
