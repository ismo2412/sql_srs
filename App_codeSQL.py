import streamlit as st
import pandas as pd
import duckdb

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

conn = duckdb.connect()
conn.register("data_source", df)

# Selectbox avec des requêtes exemples
queries = {
    "Choisir une requête...": "",
    "Tout afficher": "SELECT * FROM data_source",
    "Somme de a": "SELECT SUM(a) AS somme_a FROM data_source",
    "Moyenne de b": "SELECT AVG(b) AS moyenne_b FROM data_source",
    "Filtrer a > 1": "SELECT * FROM data_source WHERE a > 1"
}

selected_query = st.selectbox("📌 Requêtes exemples", list(queries.keys()))

# Pré-remplir le text_area avec la requête choisie
default_query = queries[selected_query]

query = st.text_area("Ton code SQL", value=default_query)

if query:
    st.subheader("🔎 Requête SQL")
    st.code(query, language="sql")

    try:
        result = conn.execute(query).df()

        st.subheader("📊 Résultat")
        st.dataframe(result)

    except Exception as e:
        st.error(f"Erreur SQL : {e}")