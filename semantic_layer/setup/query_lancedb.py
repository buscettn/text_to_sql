import lancedb
import pandas as pd
import argparse
from pathlib import Path
from semantic_layer.config import LANCEDB_PATH
from semantic_layer.providers.embeddings import get_embedding

def query_lancedb(query_text: str, k: int, lance_table: str, query_type: str = "semantic"):
    print(f"Connecting to LanceDB at {LANCEDB_PATH}...")
    db = lancedb.connect(str(LANCEDB_PATH))

    if lance_table not in db.list_tables().tables:
        print(f"Error: Table '{lance_table}' not found. Available tables: {db.list_tables().tables}")
        return

    table = db.open_table(lance_table)

    if query_type == "hybrid":
        query_vector = get_embedding(query_text)
        search_query = table.search(query_type="hybrid").vector(query_vector).text(query_text)
    elif query_type == "fts":
        search_query = table.search(query_text, query_type="fts")
    else:  # semantic
        query_vector = get_embedding(query_text)
        search_query = table.search(query_vector)

    results = search_query.limit(k).to_pandas()

    print("\n--- Search Results ---")
    if not results.empty:
        # Drop the raw vector column from the print output for readability if it exists
        cols_to_print = [c for c in results.columns if c != 'vector']
        print(results[cols_to_print])
    else:
        print("No results found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query LanceDB using semantic, hybrid, or FTS search.")
    parser.add_argument("query", type=str, help="The search query text.")
    parser.add_argument("-k", type=int, default=2, help="Number of results to return (default: 2).")
    parser.add_argument("-t", "--table", type=str, default="domain", help="The name of the table to query (default: 'domain').")
    parser.add_argument("--query_type", type=str, choices=["semantic", "hybrid", "fts"], default="semantic", 
                        help="The type of search to perform: 'semantic' (default), 'hybrid', or 'fts'.")

    args = parser.parse_args()

    query_lancedb(args.query, args.k, args.table, args.query_type)