import sys
import argparse
from pathlib import Path

# Add project root to sys.path to allow imports from semantic_layer
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from semantic_layer.providers.dynamic_few_shot_retrieval import get_few_shot_context

def main():
    parser = argparse.ArgumentParser(description="Query dynamic few-shot SQL examples using hybrid search.")
    parser.add_argument("query", type=str, help="The natural language query to search for.")
    parser.add_argument("--domains", type=str, nargs="*", help="Optional list of domains to filter by (e.g. DOMAIN1 DOMAIN2).")
    
    args = parser.parse_args()
    
    print(f"\nSearching for: '{args.query}'")
    if args.domains:
        print(f"Filtering by domains: {', '.join(args.domains)}")
    else:
        print("No domain filter provided (searching across all examples).")
        
    try:
        results = get_few_shot_context(args.query, args.domains or [])
    except Exception as e:
        print(f"\nError during retrieval: {e}")
        sys.exit(1)
        
    if not results:
        print("\nNo matching few-shot examples found.")
        return

    print(f"\nFound {len(results)} examples:\n" + "="*50)
    
    for i, item in enumerate(results):
        print(f"\n[Example {i+1}] (Score: {item.relevance_score:.4f}, Priority: {item.priority})")
        print("-" * 50)
        print(item.content)
        print("-" * 50)

if __name__ == "__main__":
    main()
