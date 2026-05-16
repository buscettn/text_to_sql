import os
import duckdb
import pandas as pd
from pathlib import Path

# Base URL for the Olist dataset (GitHub mirror)
BASE_URL = "https://raw.githubusercontent.com/Steffin12-git/Brazilian-E-Commerce-project/main/Raw%20dataset/"

# List of files to load and their corresponding table names
DATASET_FILES = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "product_category_name_translation"
}

def setup_database():
    # Setup paths
    project_root = Path(__file__).resolve().parent.parent
    db_dir = project_root / "data" / "duckdb"
    db_path = db_dir / "test_data.duckdb"

    # Ensure directory exists
    db_dir.mkdir(parents=True, exist_ok=True)

    print(f"Connecting to DuckDB at {db_path}...")
    conn = duckdb.connect(str(db_path))

    # Get list of existing tables
    existing_tables = [row[0] for row in conn.execute("SHOW TABLES").fetchall()]
    
    for filename, table_name in DATASET_FILES.items():
        if table_name in existing_tables:
            print(f"Table '{table_name}' already exists. Skipping.")
            continue

        print(f"Loading table '{table_name}' from {filename}...")
        url = f"{BASE_URL}{filename}"
        
        try:
            # Load CSV directly into DuckDB from URL using Pandas as intermediate
            # Note: DuckDB can read directly from URL but sometimes requires extensions/permissions.
            # Pandas is reliable for small-to-medium files like these.
            df = pd.read_csv(url)
            conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
            print(f"Successfully loaded '{table_name}'.")
        except Exception as e:
            print(f"Error loading '{table_name}': {e}")

    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()
