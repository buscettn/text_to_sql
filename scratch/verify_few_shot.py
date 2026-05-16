import lancedb
import pandas as pd
from pathlib import Path
import sys

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from semantic_layer.config import LANCEDB_PATH
from semantic_layer.providers.embeddings import get_embedding

def inspect_few_shot():
    db = lancedb.connect(str(LANCEDB_PATH))
    table_name = "few_shot_queries"
    
    if table_name not in db.table_names():
        print(f"Table '{table_name}' not found!")
        return

    table = db.open_table(table_name)
    print(f"Table '{table_name}' has {len(table)} rows.\n")
    
    # 1. Show first 3 rows (excluding vector)
    print("--- First 3 Rows ---")
    df = table.head(3).to_pandas()
    print(df.drop(columns=['vector']))
    
    # 2. Test Hybrid Search
    query_text = "Show me the location of customers"
    print(f"\n--- Testing Hybrid Search for: '{query_text}' ---")
    
    query_vector = get_embedding(query_text)
    
    # Search in DOMAIN1 and DOMAIN2 (just to test filtering)
    results = table.search(query_type="hybrid").vector(query_vector).text(query_text).limit(3).to_pandas()
    
    print("\nSearch Results:")
    if not results.empty:
        # Drop vector for display
        print(results.drop(columns=['vector']))
    else:
        print("No results found.")

if __name__ == "__main__":
    inspect_few_shot()
