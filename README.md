# Text-to-SQL Engine

A modular, extensible Text-to-SQL system built with Python, LangGraph, and SqlGlot. The project strictly adheres to Hexagonal Architecture (Ports and Adapters) principles to ensure clear separation of concerns between orchestration, business logic, and external interfaces.

## Architecture

The system is designed with a decoupled architecture to facilitate maintainability and testability:

- **Core Engine (`core/`)**: Provides a framework-agnostic facade (`TextToSQLEngine`) that serves as the primary entry point for all external interfaces (CLI, SDK, UI). It manages the underlying execution lifecycle without exposing orchestration specifics. Interfaces are strictly defined using Pydantic models.
- **Orchestration (`graph/`)**: Utilizes LangGraph to manage the workflow and state of the Text-to-SQL process (e.g., semantic retrieval, SQL generation, and validation).
- **Business Logic (`components/`)**: Contains pure business logic modules decoupled from the orchestration layer. Graph nodes invoke these components to perform data transformations.
- **Semantic Layer (`semantic_layer/`)**: Responsible for domain-specific context retrieval and prompt construction to ground the SQL generation process.

## Key Features

- **Hexagonal Architecture**: Business logic is isolated from the orchestration framework (LangGraph) and external entry points.
- **State Orchestration**: LangGraph-powered state machine for managing the end-to-end pipeline (Pre-generation, Generation, Validation).
- **SQL Validation & Transpilation**: Integration with `sqlglot` to syntactically validate generated SQL and automatically transpile it to target dialects (e.g., Impala).
- **Real-time Progress Monitoring**: Architecture supports status notifications for streaming real-time feedback to front-end clients.

## Entry Points

The system is designed to support multiple consumption methods:
- **Python SDK**: For programmatic integration into other Python applications.
- **CLI**: Command-line interface for local execution and testing.
- **UI (Planned)**: Front-end application for user interaction.

## Development

### Prerequisites

- Python 3.10+
- Install dependencies:

```bash
pip install -r requirements.txt
```

### Running Tests

The project uses `pytest` for unit testing and validation.

```bash
pytest
```

## Dependencies

- `langgraph`: Workflow orchestration and state management.
- `sqlglot`: SQL parsing, validation, and transpilation.
- `pydantic`: Data validation and interface definitions.
- `pytest` & `pytest-asyncio`: Testing framework.

