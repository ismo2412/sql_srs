import streamlit as st
import pandas as pd
import duckdb

# Données exemple
data = {
    "categorie": ["X", "X", "Y", "Y", "Y"],
    "a": [1, 2, 3, 4, 5],
    "b": [10, 20, 30, 40, 50]
}
df = pd.DataFrame(data)

# Connexion DuckDB
conn = duckdb.connect()
conn.register("data_source", df)

# Sidebar
with st.sidebar:
    st.title("📌 Menu")

    queries = {
        "Choisir une requête...": "",
        "Tout afficher": "SELECT * FROM data_source",
        "Somme de a": "SELECT SUM(a) AS somme_a FROM data_source",
        "Moyenne de b": "SELECT AVG(b) AS moyenne_b FROM data_source",
        "Filtrer a > 1": "SELECT * FROM data_source WHERE a > 1",
        "Somme par catégorie": """
            SELECT 
                categorie,
                SUM(a) AS total_a,
                AVG(b) AS moyenne_b
            FROM data_source
            GROUP BY categorie
        """
    }

    selected_query = st.selectbox("Requêtes exemples", list(queries.keys()))

    # 👇 Aperçu des données dans la sidebar
    st.subheader("📊 Données")
    st.dataframe(df)

    # 👇 Schéma
    st.subheader("🧱 Schéma")
    schema_df = pd.DataFrame({
        "colonne": df.columns,
        "type": df.dtypes.astype(str)
    })
    st.table(schema_df)

# Valeur par défaut
default_query = queries[selected_query]

# Zone principale
st.title("🧠 Explorateur SQL avec DuckDB")

# 👇 Affichage de la table principale
st.subheader("📂 Table utilisée : data_source")
st.dataframe(df)

query = st.text_area("Ton code SQL", value=default_query)

if query:
    st.subheader("🔎 Requête SQL")
    st.code(query, language="sql")

    try:
        # Petite sécurité
        if "drop" in query.lower() or "delete" in query.lower():
            st.error("Requête non autorisée 🚫")
        else:
            result = conn.execute(query).df()

            st.subheader("📊 Résultat")
            st.dataframe(result)

    except Exception as e:
        st.error(f"Erreur code SQL : {e}")
