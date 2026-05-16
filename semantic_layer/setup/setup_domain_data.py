import lancedb
import pandas as pd
from pathlib import Path
from semantic_layer.config import LANCEDB_PATH, EMBEDDING_MODEL_NAME
from semantic_layer.providers.embeddings import get_embedding

# Setup paths relative to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = BASE_DIR / "data" / "semantic_input" / "domain_data.csv"

df = pd.read_csv(CSV_PATH)
print(f"Loaded {len(df)} rows from CSV.")

# ---------------------------------------------------------
# Step 3: Embed the target column
# ---------------------------------------------------------
print(f"Generating embeddings using {EMBEDDING_MODEL_NAME}...")
df['vector'] = df['DomainText'].apply(get_embedding)

# ---------------------------------------------------------
# Step 4: Store all columns (including embeddings) in LanceDB
# ---------------------------------------------------------
print("Connecting to LanceDB and storing data...")
db = lancedb.connect(str(LANCEDB_PATH))

# Use mode='overwrite' to replace the table if it already exists
table = db.create_table("domain", data=df, mode="overwrite")
print("Creating Full-Text Search (FTS) index on 'DomainText'...")
table.create_fts_index("DomainText")
print("Data successfully stored in LanceDB!")

# ---------------------------------------------------------
# Step 5: Retrieve top k results based on a query (Hybrid Search)
# ---------------------------------------------------------
query_text = "Tell me about profit and loss"
k = 2

print(f"\nSearching for top {k} results matching: '{query_text}' (Hybrid Search)")

query_vector = get_embedding(query_text)

results = table.search(query_type="hybrid").vector(query_vector).text(query_text).limit(k).to_pandas()

print("\n--- Search Results ---")
print(results.drop(columns=['vector']))