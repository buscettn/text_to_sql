# Test data plan

Set up a local DuckDB database with the full Olist Brazilian E-Commerce Dataset for testing.

### Component: Data Setup
- **Database File**: `data/duckdb/test_data.duckdb`
- **Setup Script**: `data/setup_test_data.py`
- **Dataset**: Olist Brazilian E-Commerce (Full relational schema - ~9 tables).
- **Behavior**: The setup script must be **idempotent**. It should fetch the dataset (e.g., from a GitHub mirror) and load it into DuckDB only if the data doesn't already exist.

### Component: Common Utilities
- **File**: `common/database.py`
- **Wrapper Class**: `Database` (must support context manager protocol: `with Database() as db:`)
- **Method**: `sql(query: str) -> pd.DataFrame`
- **Requirement**: The method must be named `sql` and return a Pandas DataFrame.

