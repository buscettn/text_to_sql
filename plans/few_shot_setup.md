Write /semantic_layer/setup/setup_few_shot_queries.py:
It should take /data/semantic_input/few_shot_queries.xlsx

Path Resolution:
- Use Path(__file__).resolve() to determine project root and locate files relatively.

The columns in the xlsx are: 
domain, table_name, query, sql

Validation & Pre-processing:
- Use a try-except block when reading the Excel file to handle permission errors (e.g., if the file is open in Excel).
- Fail if "domain", "query", or "sql" columns are missing.
- "table_name" is optional and can be empty.
- Drop rows with null or empty values in "domain", "query", or "sql".
- Remove duplicate rows based on the combination of (domain, query).

Write all the columns (including a new "search_text" column) to the lancedb table "few_shot_queries".
The "search_text" column should be the concatenation of (domain +"\n\n"+ table_name +"\n\n"+ query).
The embedding should be generated from the "search_text" column.
Use the example for embedding in semantic_layer\setup\setup_domain_data.py

Setup should be made to also allow for full text search as well as hybrid search on the "search_text" column.
When the script is run it should:
- Compeletely overwrite the existing table.
- Print a summary of the number of examples loaded per domain.

