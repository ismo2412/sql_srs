import streamlit as st
import pandas as pd
import duckdb

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

conn = duckdb.connect()
conn.register("data_source", df)

query = st.text_area("Ton code SQL")  # mieux que text_input pour SQL

if query:
    st.subheader("🔎 Requête SQL")
    st.code(query, language="sql")

    try:
        result = conn.execute(query).df()

        st.subheader("📊 Résultat")
        st.dataframe(result)

    except Exception as e:
        st.error(f"Erreur SQL : {e}")
