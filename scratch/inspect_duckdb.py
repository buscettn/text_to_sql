import duckdb
import os
from pathlib import Path

def inspect_database():
    # Attempt to find the database file relative to project root or use absolute path
    project_root = Path(__file__).resolve().parent.parent
    possible_paths = [
        project_root / "data" / "duckdb" / "test_data.duckdb",
        r"C:\Users\thoma\SynologyDrive\Coding\text_to_sql\data\duckdb\test_data.duckdb"
    ]
    
    db_path = None
    for p in possible_paths:
        if Path(p).exists():
            db_path = str(p)
            break
            
    if not db_path:
        print("Error: Could not find test_data.duckdb in expected locations.")
        return

    print(f"Inspecting database: {db_path}\n")
    conn = duckdb.connect(db_path)
    
    # Get all tables
    try:
        tables = conn.execute("SHOW TABLES").fetchall()
    except Exception as e:
        print(f"Error listing tables: {e}")
        conn.close()
        return
    
    if not tables:
        print("No tables found in the database.")
        conn.close()
        return

    for (table_name,) in tables:
        print("=" * 80)
        print(f"TABLE: {table_name}")
        print("=" * 80)
        
        # Get DDL
        try:
            ddl_query = f"SELECT sql FROM duckdb_tables WHERE table_name = '{table_name}'"
            ddl = conn.execute(ddl_query).fetchone()
            if ddl and ddl[0]:
                print("\n[DDL]")
                print(ddl[0])
            else:
                print("\n[DDL] Not found in duckdb_tables")
        except Exception as e:
            print(f"\n[DDL] Error: {e}")
        
        print("\n[SAMPLE ROWS (5)]")
        try:
            # Attempt to use pandas for pretty printing if available, else fallback
            try:
                import pandas as pd
                df = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf()
                if df.empty:
                    print("Table is empty.")
                else:
                    print(df.to_string(index=False))
            except ImportError:
                # Fallback to standard fetchall and manual formatting
                res = conn.execute(f"SELECT * FROM {table_name} LIMIT 5")
                columns = [desc[0] for desc in res.description]
                rows = res.fetchall()
                
                if not rows:
                    print("Table is empty.")
                else:
                    header = " | ".join(columns)
                    print(header)
                    print("-" * len(header))
                    for row in rows:
                        print(" | ".join(str(val) for val in row))
        except Exception as e:
            print(f"Error fetching rows: {e}")
            
        print("\n")

    conn.close()

if __name__ == "__main__":
    inspect_database()
