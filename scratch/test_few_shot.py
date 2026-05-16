import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from semantic_layer.providers.dynamic_few_shot_retrieval import get_few_shot_context

def test_retrieval():
    print("--- Testing Domain Filtered Retrieval (DOMAIN3) ---")
    results = get_few_shot_context("Show me the latest orders", domains=["DOMAIN3"])
    for i, item in enumerate(results):
        print(f"\nResult {i+1} (Score: {item.relevance_score:.4f}, Priority: {item.priority}):")
        print(item.content)

    print("\n\n--- Testing Fallback Retrieval (Empty Domains) ---")
    results = get_few_shot_context("Who are the top customers?", domains=[])
    for i, item in enumerate(results):
        print(f"\nResult {i+1} (Score: {item.relevance_score:.4f}, Priority: {item.priority}):")
        print(item.content)

if __name__ == "__main__":
    test_retrieval()
