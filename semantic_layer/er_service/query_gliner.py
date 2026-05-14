import argparse
import os
from gliner import GLiNER

def main():
    parser = argparse.ArgumentParser(description="Query GLiNER model for bank entities.")
    parser.add_argument("query", type=str, help="The text query to analyze.")
    parser.add_argument("--model", type=str, default="data/gliner/models/gliner_mfi_finetuned", help="Path to the fine-tuned model.")
    parser.add_argument("--threshold", type=float, default=0.3, help="Score threshold for extraction.")
    args = parser.parse_args()

    if not os.path.exists(args.model):
        print(f"Error: Model not found at {args.model}. Please run fine_tune_gliner.py first.")
        return

    # Load model
    # print(f"Loading model from {args.model}...")
    model = GLiNER.from_pretrained(args.model)

    # Labels we want to extract
    labels = ["bank"]

    # Inference
    entities = model.predict_entities(args.query, labels, threshold=args.threshold)

    # Output only the list of entity names for simplicity or formatted output
    if not entities:
        print("No entities found.")
    else:
        # print(f"Found {len(entities)} entities:")
        for entity in entities:
            print(f"{entity['text']}")

if __name__ == "__main__":
    main()
