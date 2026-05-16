from typing import Dict
import lancedb
from semantic_layer.config import LANCEDB_PATH
from semantic_layer.providers.embeddings import get_embedding

def get_domain(query: str, threshold: float = 0.8) -> Dict[str, float]:
    """
    Performs a semantic search on the query to determine relevant domains.
    Returns a dictionary of {DomainCode: Confidence} for matches above the threshold.
    """
    db = lancedb.connect(str(LANCEDB_PATH))
    
    # Check if domain table exists
    if "domain" not in db.list_tables().tables:
        return {}
        
    table = db.open_table("domain")
    
    # Get embedding for the query
    query_vector = get_embedding(query)
    
    # Search for top results using hybrid search (vector + fts)
    results = table.search(query_type="hybrid").vector(query_vector).text(query).limit(5).to_pandas()
    
    if results.empty:
        return {}

    # Convert distance or relevance score to confidence score
    domain_scores = {}
    for _, row in results.iterrows():
        if "_distance" in row:
            # Vector search distance (L2)
            distance = row["_distance"]
            confidence = 1 / (1 + distance)
        elif "_relevance_score" in row:
            # Hybrid search RRF score. Max is approx 2/61 (~0.0328) with default k=60.
            # We scale this to a 0-1 range for the threshold.
            max_rrf = 2 / 61
            confidence = min(1.0, row["_relevance_score"] / max_rrf)
        else:
            confidence = 0
            
        if confidence >= threshold:
            domain_scores[row["DomainCode"]] = confidence
            
    return domain_scores