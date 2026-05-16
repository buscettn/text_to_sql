Based on the setup done in semantic_layer\setup\setup_few_shot_queries.py
Let's build the semantic dynamic few shot retrieval provider (semantic_layer\providers\dynamic_few_shot_retrieval.py) and node (graph\nodes\dynamic_few_shot_retrieval_node.py)

Configuration Changes (`semantic_layer\config.py`):
- `FEW_SHOT_TOP_K`: (int, default 3)
- `FEW_SHOT_SEARCH_TYPE`: (str, default "hybrid")
- `FEW_SHOT_PRIORITY`: (int, default 2)
- `LANCEDB_FEW_SHOT_TABLE`: (str, default "few_shot_queries")

Setup Update (`semantic_layer\setup\setup_few_shot_queries.py`):
- Update to use `LANCEDB_FEW_SHOT_TABLE` from config instead of a hardcoded string.

Retrieval Logic:
- The node should pass the user query and all active domains (from `state["data_domain"]`) to the provider.
- The provider should connect to LanceDB using the table name from config.
- **Error Handling**:
    - If the table does not exist, the provider should **raise an error** (e.g. `FileNotFoundError` or a custom exception) to signal that setup is required.
- **Filtering Logic**:
    - If active domains are provided: Apply a hard filter (SQL `WHERE` clause) to only include rows where the `domain` is in the list of active domains.
    - If NO active domains are provided: Do NOT apply a domain filter (search across all examples).
- **Search Logic**:
    - Perform a search using `FEW_SHOT_SEARCH_TYPE` to retrieve the **global top K** results.
- **Context Item Creation**:
    - For each result, return a `ContextItem` with:
        - `content`: 
          ```
          Sample SQL Example:
          - Question: {query}
          - SQL: ```sql
          {sql}
          ```
          ```
        - `source`: "few_shot"
        - `relevance_score`: The distance/score from LanceDB.
        - `priority`: 
            - If active domains were used: `FEW_SHOT_PRIORITY`.
            - If fallback (no domains) was used: `FEW_SHOT_PRIORITY - 2`.

The node:
- Should update the `few_shot_context` in the state with the list of `ContextItem` objects.
