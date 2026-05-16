import duckdb
import json

conn = duckdb.connect('data/duckdb/test_data.duckdb')
tables = conn.execute("SHOW TABLES").fetchall()
info = {}
for (t,) in tables:
    sql = conn.execute(f"SELECT sql FROM duckdb_tables WHERE table_name='{t}'").fetchone()[0]
    sample = conn.execute(f"SELECT * FROM {t} LIMIT 1").fetchone()
    cols = [d[0] for d in conn.execute(f"SELECT * FROM {t} LIMIT 0").description]
    info[t] = {"sql": sql, "sample": dict(zip(cols, sample)) if sample else None}

print(json.dumps(info, indent=2))
conn.close()
