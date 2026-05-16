import duckdb
import pandas as pd
from typing import Optional

class Database:
    """
    A simple wrapper for DuckDB that supports the context manager protocol.
    """
    def __init__(self, db_path: str = "data/duckdb/test_data.duckdb"):
        self.db_path = db_path
        self.conn: Optional[duckdb.DuckDBPyConnection] = None

    def __enter__(self):
        self.conn = duckdb.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            self.conn = None

    def sql(self, query: str) -> pd.DataFrame:
        """
        Executes a SQL query and returns the result as a Pandas DataFrame.
        """
        if self.conn is None:
            # Fallback if not used as a context manager
            with duckdb.connect(self.db_path) as conn:
                return conn.execute(query).df()
        
        return self.conn.execute(query).df()
