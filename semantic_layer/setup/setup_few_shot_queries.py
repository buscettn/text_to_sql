import lancedb
import pandas as pd
from pathlib import Path
import sys
from tqdm import tqdm

# Add project root to sys.path to allow imports from semantic_layer
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from semantic_layer.config import LANCEDB_PATH, EMBEDDING_MODEL_NAME, LANCEDB_FEW_SHOT_TABLE
from semantic_layer.providers.embeddings import get_embedding

def setup_few_shot():
    # 1. Path Resolution
    XLSX_PATH = PROJECT_ROOT / "data" / "semantic_input" / "few_shot_queries.xlsx"
    
    print(f"Loading few-shot queries from: {XLSX_PATH}")
    
    # 2. Load Excel with Permission Error Handling
    try:
        df = pd.read_excel(XLSX_PATH)
    except PermissionError:
        print(f"Error: Could not access '{XLSX_PATH.name}'.")
        print("Please close the file in Excel or any other application and try again.")
        return
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # 3. Validation & Pre-processing
    required_columns = ["domain", "query", "sql"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"Error: Missing required columns: {missing}")
        return
    
    # Ensure table_name exists even if empty
    if "table_name" not in df.columns:
        df["table_name"] = ""
    
    # Drop rows missing critical values
    original_count = len(df)
    df = df.dropna(subset=required_columns)
    df = df[df[required_columns].astype(str).apply(lambda x: x.str.strip().str.len() > 0).all(axis=1)]
    
    dropped_count = original_count - len(df)
    if dropped_count > 0:
        print(f"Dropped {dropped_count} rows with missing 'domain', 'query', or 'sql'.")

    # De-duplication
    df = df.drop_duplicates(subset=["domain", "query"])
    dedup_count = original_count - dropped_count - len(df)
    if dedup_count > 0:
        print(f"Removed {dedup_count} duplicate rows (same domain and query).")

    # 4. Create search_text
    print("Preparing search text...")
    df["table_name"] = df["table_name"].fillna("").astype(str)
    df["search_text"] = (
        df["domain"].astype(str) + "\n\n" + 
        df["table_name"] + "\n\n" + 
        df["query"].astype(str)
    )

    # 5. Generate Embeddings
    print(f"Generating embeddings using {EMBEDDING_MODEL_NAME}...")
    
    vectors = []
    for text in tqdm(df['search_text'], desc="Embedding"):
        vectors.append(get_embedding(text))
    df['vector'] = vectors

    # 6. Store in LanceDB
    print("Connecting to LanceDB and storing data...")
    db = lancedb.connect(str(LANCEDB_PATH))
    
    # Overwrite the table
    table = db.create_table(LANCEDB_FEW_SHOT_TABLE, data=df, mode="overwrite")
    
    print(f"Creating Full-Text Search (FTS) index on 'search_text'...")
    table.create_fts_index("search_text")
    
    print(f"Data successfully stored in table '{LANCEDB_FEW_SHOT_TABLE}'!")

    # 7. Print Summary
    print("\n--- Load Summary ---")
    summary = df.groupby("domain").size().reset_index(name="count")
    print(summary.to_string(index=False))
    print(f"\nTotal examples loaded: {len(df)}")

if __name__ == "__main__":
    setup_few_shot()
