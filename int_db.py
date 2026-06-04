import pandas as pd
import duckdb

conn = duckdb.connect("data/exercices_sql_tables.duckdb", read_only=False)

df = pd.DataFrame({
    "categorie": ["X", "X", "Y", "Y", "Y"],
    "a": [1, 2, 3, 4, 5],
    "b": [10, 20, 30, 40, 50],
})

conn.register("df_view", df)
conn.execute("""
CREATE TABLE IF NOT EXISTS df AS 
SELECT * FROM df_view
""")

memory_state_df = pd.DataFrame({
    "theme": ["requête SQL"],
    "exercice_name": ["Univers SQL"],
    "table": ["df"],
    "last_reviewed": ["2015-01-01"]
})

conn.register("memory_state_view", memory_state_df)

conn.execute("""
CREATE TABLE IF NOT EXISTS memory_state AS 
SELECT * FROM memory_state_view
""")