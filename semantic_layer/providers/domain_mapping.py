import lancedb
from semantic_layer.config import LANCEDB_PATH
from semantic_layer.providers.embeddings import get_embedding

def get_domain(query: str) -> str:
    """
    Performs a semantic search on the query to determine the most likely domain.
    Returns the DomainCode of the top match.
    """
    db = lancedb.connect(str(LANCEDB_PATH))
    
    # Check if domain table exists
    if "domain" not in db.list_tables().tables:
        # Fallback or error
        return "unknown_domain"
        
    table = db.open_table("domain")
    
    # Get embedding for the query
    query_vector = get_embedding(query)
    
    # Search for the top result
    results = table.search(query_vector).limit(1).to_pandas()
    
    if not results.empty:
        return results.iloc[0]["DomainCode"]
    
    return "unknown_domain"