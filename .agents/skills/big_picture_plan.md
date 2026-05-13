I want to plan building a text-to-sql app in python. i have started out with the following technical concept (no methodological details such as which methods to use yet). 

# Text-To-SQL Architecture & Usage

The application is built around a core engine that generates SQL based on a prompt. There are three primary ways to interact with and use the application:
1. **Python SDK**: Direct integration into other Python applications by importing the core modules.
2. **CLI (Command Line Interface)**: A terminal-based application for quick, scriptable interactions.
3. **UI (User Interface)**: A chat-based graphical interface for user-friendly interactions.

The endpoint receives a query, an optional data domain, and an optional thread ID for conversational memory.
```python
class SQLRequest(BaseModel):
    query: str
    data_domain: str | None = None # optional in case user knows explicit data domain to be queried
    thread_id: str | None = None   # optional, used to maintain conversation state, initialized by the backend for new conversations

class SQLResponse(BaseModel):
    sql: str | None                # The generated SQL (if applicable) - generated_sql from state
    message: str                   # Agent's response or explanation
    status: str                    # Status of the request (success, error, abstained)
    thread_id: str                 # ID to be passed in subsequent requests for chat memory
```

Modular Design: there should be clear modules/parts that separate the components:
    - input: intent_guard (Placeholder node to be implemented)
    - semantic layer (many subparts):
        - domain mapping (Placeholder node to be implemented)
        - schema retrieval (Placeholder node to be implemented)
        - grounding node (Placeholder node to be implemented)
        - (...)
    - pre-generation abstention node (Placeholder node to be implemented)
    - generator node (llm call node, Placeholder node to be implemented)
    - validator (Placeholder node to be implemented)

**Separation of Concerns (Hexagonal Architecture):** The system strictly separates core business logic from orchestration. The `components/` directory contains pure Python functions (generation, validation, intent checking) that have zero knowledge of LangGraph. The `graph/nodes/` directory contains thin LangGraph wrappers that merely extract state, call the pure components, and update the state. This ensures maximum testability and framework agnosticism.

different abstention points (very beginning "intent guard" and at sql generation for example) are implemented through langgraph nodes and edges, i don't know of a better way to integrate abstention points cleanly yet.

validator node: Syntactic (is it SQL?), Structural (does it use real columns?), and Functional (does it run?) validation. impala sql dialect must be ensured.

Pytest for everything feasible (no langgraph nodes)

## synchronous but future proof for async:
The orchestration layer (all LangGraph node wrappers) and any I/O-bound core components (e.g., LLM generation via LiteLLM, LanceDB retrieval) will be defined as asynchronous (async def) from the start to ensure the system is non-blocking and scalable. Purely CPU-bound or inherently synchronous business logic (e.g., SQL parsing with sqlglot, simple data formatting in ContextBuilder) will remain standard synchronous functions (def). The async LangGraph nodes will natively await the async components, while executing the synchronous components directly (or via asyncio.to_thread if computationally heavy) to seamlessly bridge the two.

## Packages used:
LanceDB to store embeddings/retrieval
langgraph/langchain but strictly no telemetry, strictly used for orchestration, no prompt templates
Jinja2 for prompts and context injection
pydantic for structured llm outputs where needed
sqlglot for sql parsing and validation, enforce impala dialect.
pytest for testing
python-dotenv
litellm with openai for llm calls

## Folder Structure:
text_to_sql/
├── common/                       # Reusable modules will be imported from other projects
│   ├── config/                   # YAML configuration files & loaders
│   ├── dap/                      # Database access patterns / connections
│   └── logger/                   # File-logging utilities
│
├── core/                         # Core system definitions
│   ├── config.py                 # Loads environment variables (.env) via python-dotenv
│   ├── model_config.py           # LLM model setup
│   ├── interfaces.py             # Pydantic models & Protocols (e.g. ContextItem, SQLRequest, SQLResponse)
│   └── state.py                  # LangGraph state definitions (Thread state, conversational memory)
│
├── ui/                           # The chat-interface frontend
│   └── ...                       # (tbd if using streamlit or flask or something else)
│
├── cli/                          # Command Line Interface application
│   └── app.py                    # CLI entry point (e.g. Typer/argparse)
│
├── sdk/                          # Python SDK for external integration
│   └── client.py                 # Easy-to-use Python client wrapping the core engine
│
├── data/                         # Local storage layer (Contents ignored by git)
│   ├── lancedb/                  # LanceDB local storage for embeddings
│   ├── semantic_input/           # Additional input data for the semantic layer
│   │   ├── ground_truth/   
│   │   └── semantic_input/
│   └── sqlite/                   # SQLite database for LangGraph checkpointer memory
│
├── templates/                    # Jinja2 templates for prompts
│   ├── prompts/                  # Base prompts for the generator/intent nodes
│   └── context/                  # Templates for injecting context snippets
│
├── semantic_layer/               # All context gathering & retrieval logic
│   ├── providers/                # Implementations of SemanticProvider interface
│   │   ├── domain_mapping.py     
│   │   ├── schema_retrieval.py   
│   │   ├── dynamic_few_shot_retrieval.py   
│   │   └── grounding.py          
│   └──  setup/                   # Scripts to create embeddings and populate LanceDB
│
├── components/                   # Pure business logic (No LangGraph imports here)
│   ├── intent.py                 # Core logic for checking intent & initial abstention
│   ├── pre_generation.py         # Core logic for checking readiness before generation
│   ├── generator.py              # LiteLLM/OpenAI call logic for SQL generation
│   └── validator.py              # Syntactic, Structural, Functional validation via sqlglot
│
├── graph/                              # Orchestration layer
│   ├── nodes/                          # Thin LangGraph node wrappers around components
│   │   ├── intent_node.py              # Wrapper for components/intent.py
│   │   ├── domain_mapping_node.py      # Wrapper for semantic_layer/providers/domain_mapping.py
│   │   ├── schema_retrieval_node.py    # Wrapper for semantic_layer/providers/schema_retrieval.py
│   │   ├── dynamic_few_shot_retrieval_node.py # Wrapper for semantic_layer/providers/dynamic_few_shot_retrieval.py
│   │   ├── grounding_node.py           # Wrapper for semantic_layer/providers/grounding.py
│   │   ├── pre_generation_node.py      # Wrapper for components/pre_generation.py
│   │   ├── generator_node.py           # Wrapper for components/generator.py
│   │   └── validator_node.py           # Wrapper for components/validator.py
│   └── workflow.py                     # Defines LangGraph edges, nodes, and checkpointer integration
│
├── evaluation/                   # evaluation script
│
├── tests/                        # Pytest directory
│   ├── semantic_layer/
│   ├── components/
│   └── graph/
│
├── .env                          # Environment secrets (ignored in git)
├── .gitignore
└── requirements.txt              # (or pyproject.toml) Dependencies


## Extensible Semantic Layer:
The semantic layer is a broad term used for all the logic that gathers and injects knowledge into the LLM. 

```python
# core/interfaces.py
from pydantic import BaseModel

class ContextItem(BaseModel):
    content: str
    source: str             # schema, few_shot, grounding, etc...
    relevance_score: float  # How confident the provider is
    priority: int           # 1 (Critical) to 5 (Optional)
```

Every semantic node is in principle responsible for its own context length to reduce context bloat, so completely irrelevant results should not be returned. But by returning priority and relevance_score the ContextBuilder can have a firm grip on context length due to being able to rerank based on priority and token_count.

To maintain strict separation of concerns (Hexagonal Architecture), the `ContextBuilder` does NOT depend on LangGraph state. Instead, it accepts pure Python lists of `ContextItem` objects. A LangGraph node wrapper extracts these lists from the `TextToSQLState` and passes them to the pure `ContextBuilder`, which then concatenates and reranks them.

`ContextBuilder` is treated as a utility called inside `generator_node.py`. The node wrapper retrieves the lists from the state, calls `ContextBuilder.build_context()`, and passes the resulting string directly to the pure generator component.

```python
# context_builder.py
from typing import List
from core.interfaces import ContextItem

class ContextBuilder:
    def build_context(
        self, 
        schema_context: List[ContextItem],
        few_shot_context: List[ContextItem],
        grounding_context: List[ContextItem]
    ) -> str:
        # 1. Combine all items
        all_items = schema_context + few_shot_context + grounding_context
        
        # 2. Sort by priority and relevance
        all_items.sort(key=lambda x: (x.priority, -x.relevance_score))
        
        # 3. optional cutoff to manage token limits

        # 4. Concatenate
        return "\n\n".join([item.content for item in all_items])
```

The semantic layer is setup by running the setup scripts. These scripts will create the embeddings and populate LanceDB with metadata and embeddings (overwriting existing data). once populated it remains static (unless run again).

## Langgraph

### LangGraph Workflow

Preliminary Langgraph workflow:
    1. Intent Guard
        - if intent is not to generate SQL or follow up question regarding SQL -> end with message
    2. Domain Mapping
    3. Schema Retrieval
    4. Dynamic Few-Shot Retrieval
    5. Grounding
    6. Pre-Generation Check, conditional:
        - if abstains -> end with message
        - else -> sql generation
    7. SQL Generation
    8. Validation, conditional:
        - if invalid AND generation_attempts < MAX_ATTEMPTS -> sql generation
        - else -> end with error message/status error

### models in nodes
every node defines it's own model that it's using (so intent guard can use its own small model for quick abstraction  and generation the fancy model)
The model configurations (e.g., LiteLLM setup, models to use) will be defined via core/model_config.py and passed into the pure Python functions inside components/ (like generator.py and intent.py). The LangGraph node wrappers must remain completely unaware of which LLM is being used, merely passing the config and state to the pure functions.

### LangGraph State Management

We will use LangGraph's built-in state persistence (via Threads) to enable follow-up chats with the agent. 
- When a user submits a query without a `thread_id`, the backend initializes a new Thread, executes the graph, and returns a new `thread_id` along with the SQL and response.
- LangGraph loads the exact graph state for that thread (including the previously generated SQL, retrieved context, and conversation history), allowing the LLM to seamlessly explain its reasoning or iterate on the query.
    - Langgraph checkpointer uses sqlite to store the state (sqlitesaver) - could be replaced for production with something else.

### Status Propagation (UI, CLI, SDK)

To propagate "what the system is doing right now" (e.g., to show loading spinners for specific steps), the system will use **LangGraph's built-in async streaming** (`.astream_events()` or `stream_mode="updates"`). 

**Why this is the recommended approach:**
1. **Zero State Clutter:** We do not need to add ephemeral `current_status` fields to the `TextToSQLState`.
2. **Strict Hexagonal Architecture:** Pure business components and LangGraph nodes remain completely unaware of the UI. They do not need custom callback functions passed down to them.
3. **Versatility:** This approach naturally supports token-by-token streaming for the LLM generation later.

**Effect on CLI and SDK:**
Because the streaming is handled entirely by LangGraph's execution engine (and not hardcoded into our business logic), it is strictly **additive**. The core engine can expose two ways to run a query:
- **Blocking/Synchronous (`.invoke()` or `.ainvoke()`):** The SDK and CLI can use this to simply send a query and wait for the final `SQLResponse`. The CLI can just show a generic "Loading..." spinner.
- **Streaming (`.astream_events()`):** The UI (or a fancy CLI using a library like `rich`) can consume the stream to show real-time progress (e.g., "Retrieving schema..."). The SDK will expose a `stream_query()` method.

### Langgraph State
```python
import operator
from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from core.interfaces import ContextItem # Based on your plan.md

class TextToSQLState(TypedDict):
    # ==========================================
    # 1. CORE INPUTS & MEMORY
    # ==========================================
    # LangGraph's built-in message reducer. 
    # Holds the conversation history for follow-up questions.
    # The latest HumanMessage is the current user query.
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Optional explicitly provided domain from the API request
    requested_domain: Optional[str]
    
    # ==========================================
    # 2. SEMANTIC LAYER (CONTEXT ACCUMULATION)
    # ==========================================
    # The domain determined by the Domain Mapping node
    active_domain: Optional[str]
    
    # separate context items
    schema_context: List[ContextItem]
    few_shot_context: List[ContextItem]
    grounding_context: List[ContextItem]
    
    # ==========================================
    # 3. GENERATION & VALIDATION LOOP
    # ==========================================
    # The SQL currently drafted by the generator node
    # at the end this field will hold the FINAL sql (if generated)
    generated_sql: Optional[str]
    
    # Feedback from the validator node. 
    validation_errors: Optional[str]
    
    # Crucial for preventing infinite LLM loops (Generator <-> Validator)
    generation_attempts: int 
    
    # ==========================================
    # 4. FINAL OUTPUTS
    # ==========================================
    # success, error, abstained
    status: str 

    # The final natural language response or abstention explanation
    agent_message: Optional[str] 
```


## miscellaneous:
- pip+requirements.txt for requirements
- core engine will be directly imported by ui and cli 
- cli is stateless thus not conversational. might be changed in the future but fixed for now.
- validator auto-fixing: using sqlglot.transpile(sql, write="impala") inside the pure validator.py component. If the translation succeeds, update the generated_sql directly and bypass the need to ask the LLM to fix the dialect. Only send it back to the LLM for missing columns or logical errors.
- core/config.py module to load variables from a .env file (using python-dotenv) to keep secrets out of source control.
- currently no authentication or authorization is implemented.

## Extendability:
currently only linear sql generation, no cycles of user questions possible. this could be extended by the intent_guard node checking for question intent and calling the graph again with an adapted prompt or additional routing in the future.


 