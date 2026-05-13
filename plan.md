I want to plan building a text-to-sql app in python. i have started out with the following technical concept (no methodological details such as which methods to use yet). 

# Text-To-SQL Struktur
endpoint that generates the sql based on a prompt
UI provides chat-interface based on the endpoint

API contract: The endpoint receives a query, an optional data domain, and an optional thread ID for conversational memory.
```python
class SQLrequest(BaseModel):
    query: str
    data_domain: str | None = None # optional in case user knows explicit data domain to be queried
    thread_id: str | None = None   # optional, used to maintain conversation state

class SQLresponse(BaseModel):
    sql: str | None                # The generated SQL (if applicable)
    message: str                   # Agent's response or explanation
    thread_id: str                 # ID to be passed in subsequent requests for chat memory
```

Modular Design: there should be clear modules/parts that separate the components:
    - input: intent_guard (empty node for now)
    - semantic layer (many subparts):
        - domain mapping (empty for now)
        - schema retrieval (empty for now)
        - grounding node (empty for now)
    - pre-generation abstention node (empty for now)
    - generator node (llm call node, empty for now)
    - validator (empty for now)

different abstention points (very beginning "intent guard" and at sql generation for example) are implemented through langgraph nodes and edges, i don't know of a better way to integrate abstention points cleanly yet.

asynchronous definitions for now, but we can always switch to sync if it gets too complicated

validator node: Syntactic (is it SQL?), Structural (does it use real columns?), and Functional (does it run?) validation. impala sql dialect must be ensured.

pytests for everything


## Packages used:
lancedb to store embeddings/retrieval
langgraph/langchain but strictly no telemetry, strictly used for orchestration, no prompt templates
Jinja2 for prompts and context injection
pydantic for structured llm outputs where needed
sqlglot for sql parsing and validation
pytest for testing
python-dotenv
litellm with openai for llm calls
arize pheonix for observability (check for correct cloudera setup)

## Folder Structure:
common modules from other projects:
    - common/logger/ for file-logging
    - common/dap/ for database access
    - common/config/ for yaml config files
must include lancedb local storage
must include a separate module for setup of semantic layer (create embeddings, add to lancedb, ...)
jinja2 templates for prompts and context injection

should have an empty folder for an entity resolution service (named 'mo_service'). this is just a placeholder for now.


more to be decided later

## Extensible Semantic Layer:

```
# core/interfaces.py
from pydantic import BaseModel

class ContextItem(BaseModel):
    content: str
    relevance_score: float  # How confident the provider is
    priority: int           # 1 (Critical) to 5 (Optional)

class SemanticProvider(Protocol):
    def get_context_items(self, user_query: str) -> list[ContextItem]:
        """Returns a list of potential context items, ranked by the provider."""
        pass

```

The ContextBuilder simply loops through registered providers and concatenates their knowledge.
Every semantic provider is responsible for its own context length to reduce context bloat.
But ContextBuilder has a firm grip on context legnth due to being able to rerank based on priority and token_count.

in it's simplest form the contextbuilder just concatenates the context of all providers:
```
# semantic_layer/context_builder.py
class ContextBuilder:
    def __init__(self, providers: list[SemanticProvider]):
        self.providers = providers

    def build_context(self, user_query: str) -> str:
        context_parts = []
        for provider in self.providers:
            context_parts.append(provider.get_context(user_query))
        
        return "\n\n".join(context_parts)
```

## LangGraph State Management

We will use LangGraph's built-in state persistence (via Threads) to enable follow-up chats with the agent. 
- When a user submits a query without a `thread_id`, the backend initializes a new Thread, executes the graph, and returns a new `thread_id` along with the SQL and response.
- If the user asks a follow-up question (e.g., "Why did you join on the user table?"), the UI passes back the `thread_id`.
- LangGraph loads the exact graph state for that thread (including the previously generated SQL, retrieved context, and conversation history), allowing the LLM to seamlessly explain its reasoning or iterate on the query.
- Langgraph checkpointer uses sqlite to store the state (sqlitesaver) - could be replaced for production with something else.

## some details:
core/config.py module to load variables from a .env file (using python-dotenv) to keep secrets out of source control.



 