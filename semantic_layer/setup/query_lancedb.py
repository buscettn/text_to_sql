import lancedb
import pandas as pd
import argparse
from litellm import embedding
from pathlib import Path

# Setup paths relative to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LANCEDB_PATH = BASE_DIR / "data" / "lancedb"

# Configuration
# "ollama/" prefix tells LiteLLM to route this to your local Ollama instance
MODEL_NAME = "ollama/mxbai-embed-large:latest"
OLLAMA_API_BASE = "http://localhost:11434" # Default Ollama port

def get_embedding(text: str) -> list[float]:
    """Generates an embedding vector using LiteLLM and Ollama."""
    response = embedding(
        model=MODEL_NAME,
        input=text,
        api_base=OLLAMA_API_BASE
    )
    # Extract the vector from the LiteLLM response payload
    return response['data'][0]['embedding']

def query_lancedb(query_text: str, k: int, lance_table: str):
    print(f"Connecting to LanceDB at {LANCEDB_PATH}...")
    db = lancedb.connect(str(LANCEDB_PATH))

    if lance_table not in db.list_tables().tables:
        print(f"Error: Table '{lance_table}' not found. Available tables: {db.list_tables().tables}")
        return

    table = db.open_table(lance_table)

    print(f"\nSearching for top {k} results matching: '{query_text}'")

    query_vector = get_embedding(query_text)

    results = table.search(query_vector).limit(k).to_pandas()

    print("\n--- Search Results ---")
    if not results.empty:
        # Drop the raw vector column from the print output for readability if it exists
        cols_to_print = [c for c in results.columns if c != 'vector']
        print(results[cols_to_print])
    else:
        print("No results found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query LanceDB using semantic search.")
    parser.add_argument("query", type=str, help="The search query text.")
    parser.add_argument("-k", type=int, default=2, help="Number of results to return (default: 2).")
    parser.add_argument("-t", "--table", type=str, default="domain", help="The name of the table to query (default: 'domain').")

    args = parser.parse_args()

    query_lancedb(args.query, args.k, args.table)