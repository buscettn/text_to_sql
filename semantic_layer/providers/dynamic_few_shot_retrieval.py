from typing import List
import lancedb
import pandas as pd
from core.interfaces import ContextItem
from semantic_layer.config import (
    LANCEDB_PATH, 
    LANCEDB_FEW_SHOT_TABLE, 
    FEW_SHOT_TOP_K, 
    FEW_SHOT_SEARCH_TYPE, 
    FEW_SHOT_PRIORITY
)
from semantic_layer.providers.embeddings import get_embedding

def get_few_shot_context(query: str, domains: List[str]) -> List[ContextItem]:
    """
    Retrieves the top K few-shot examples from LanceDB, optionally filtered by domain.
    If no domains are provided, searches across all domains with reduced priority.
    """
    db = lancedb.connect(str(LANCEDB_PATH))
    
    # Check if table exists, fail if not
    if LANCEDB_FEW_SHOT_TABLE not in db.list_tables().tables:
        raise FileNotFoundError(
            f"LanceDB table '{LANCEDB_FEW_SHOT_TABLE}' not found. "
            "Please run 'python semantic_layer/setup/setup_few_shot_queries.py' first."
        )
        
    table = db.open_table(LANCEDB_FEW_SHOT_TABLE)
    
    # Determine priority
    priority = FEW_SHOT_PRIORITY
    is_fallback = not domains
    if is_fallback:
        priority -= 2
        
    # Generate query embedding
    query_vector = get_embedding(query)
    
    # Build search
    search = table.search(query_type=FEW_SHOT_SEARCH_TYPE).vector(query_vector).text(query)
    
    # Apply domain filter if provided
    if domains:
        # Construct SQL-like IN clause for LanceDB
        domains_str = ", ".join([f"'{d}'" for d in domains])
        search = search.where(f"domain IN ({domains_str})")
        
    # Execute search
    results = search.limit(FEW_SHOT_TOP_K).to_pandas()
    
    if results.empty:
        return []
        
    context_items = []
    for _, row in results.iterrows():
        # Get relevance score
        relevance_score = 0.0
        if "_distance" in row:
            # For vector search, distance is L2. Convert to similarity.
            relevance_score = 1 / (1 + row["_distance"])
        elif "_relevance_score" in row:
            # For hybrid/fts search, use the relevance score directly
            relevance_score = row["_relevance_score"]
            
        # Format the content in structured markdown
        content = (
            "Sample SQL Example:\n"
            f"- Question: {row['query']}\n"
            "- SQL: ```sql\n"
            f"{row['sql']}\n"
            "```"
        )
        
        context_items.append(
            ContextItem(
                content=content,
                source="few_shot",
                relevance_score=relevance_score,
                priority=priority
            )
        )
        
    return context_items