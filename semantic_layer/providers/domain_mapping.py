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
    
    # Search for top results (limit to a reasonable number, e.g., 5)
    results = table.search(query_vector).limit(5).to_pandas()
    
    if results.empty:
        return {}

    # Convert distance to confidence score
    # LanceDB distance is typically L2 (squared distance). 
    # A simple conversion: confidence = 1 / (1 + distance) as it's more stable for varying scales.
    domain_scores = {}
    for _, row in results.iterrows():
        distance = row["_distance"]
        confidence = 1 / (1 + distance)
        
        if confidence >= threshold:
            domain_scores[row["DomainCode"]] = confidence
            
    return domain_scores