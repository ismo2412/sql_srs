import pandas as pd
import duckdb

# Connexion DuckDB
conn = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)

# Données exemple
data = {
    "categorie": ["X", "X", "Y", "Y", "Y"],
    "a": [1, 2, 3, 4, 5],
    "b": [10, 20, 30, 40, 50],
}
df = pd.DataFrame(data)
conn.execute("CREATE TABLE IF NOT EXISTS df AS SELECT * FROM df")

# Name training
data = {
    "theme": ["requête SQL"],
    "exercice_name": ["Univers SQL"],
    "table": ["df"],
    "last_reviewed":["2015-01-01"]
}
memory_state_df = pd.DataFrame(data)
#print(memory_state_df.columns)
#print(memory_state_df)
conn.execute("DROP TABLE IF EXISTS memory_state")
conn.execute(
    "CREATE OR REPLACE TABLE memory_state AS SELECT * FROM memory_state_df"
)

