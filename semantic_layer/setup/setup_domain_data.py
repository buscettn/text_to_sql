import lancedb
import pandas as pd
from litellm import embedding
from pathlib import Path

# Setup paths relative to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = BASE_DIR / "data" / "semantic_input" / "domain_data.csv"
LANCEDB_PATH = BASE_DIR / "data" / "lancedb"

# Configuration
# "ollama/" prefix tells LiteLLM to route this to your local Ollama instance
MODEL_NAME = "ollama/mxbai-embed-large:latest"
OLLAMA_API_BASE = "http://localhost:11434" # Default Ollama port

df = pd.read_csv(CSV_PATH)
print(f"Loaded {len(df)} rows from CSV.")

def get_embedding(text: str) -> list[float]:
    """Generates an embedding vector using LiteLLM and Ollama."""
    response = embedding(
        model=MODEL_NAME,
        input=text,
        api_base=OLLAMA_API_BASE
    )
    # Extract the vector from the LiteLLM response payload
    return response['data'][0]['embedding']

# ---------------------------------------------------------
# Step 3: Embed the target column
# ---------------------------------------------------------
print(f"Generating embeddings using {MODEL_NAME}...")
df['vector'] = df['DomainText'].apply(get_embedding)

# ---------------------------------------------------------
# Step 4: Store all columns (including embeddings) in LanceDB
# ---------------------------------------------------------
print("Connecting to LanceDB and storing data...")
db = lancedb.connect(str(LANCEDB_PATH))

# Use mode='overwrite' to replace the table if it already exists
table = db.create_table("domain", data=df, mode="overwrite")
print("Data successfully stored in LanceDB!")

# ---------------------------------------------------------
# Step 5: Retrieve top k results based on a query
# ---------------------------------------------------------
query_text = "Tell me about profit and loss"
k = 2

print(f"\nSearching for top {k} results matching: '{query_text}'")

query_vector = get_embedding(query_text)

results = table.search(query_vector).limit(k).to_pandas()

print("\n--- Search Results ---")
print(results.drop(columns=['vector']))