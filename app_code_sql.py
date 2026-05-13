"""
Application Streamlit pour explorer des données avec DuckDB
et exécuter des requêtes SQL interactives.
"""
import duckdb
import pandas as pd
import streamlit as st

# Données exemple
data = {
    "categorie": ["X", "X", "Y", "Y", "Y"],
    "a": [1, 2, 3, 4, 5],
    "b": [10, 20, 30, 40, 50],
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
        """,
    }

    selected_query = st.selectbox("Requêtes exemples", list(queries.keys()))

    # Aperçu des données
    st.subheader("📊 Données")
    st.dataframe(df)

    # Schéma
    st.subheader("🧱 Schéma")
    schema_df = pd.DataFrame(
        {
            "colonne": df.columns,
            "type": df.dtypes.astype(str),
        }
    )
    st.table(schema_df)

# Valeur par défaut
default_query = queries[selected_query]

# Zone principale
st.title("🧠 Explorateur SQL avec DuckDB")

st.subheader("📂 Table utilisée : data_source")
st.dataframe(df)

query = st.text_area("Ton code SQL", value=default_query)

if query:
    st.subheader("🔎 Requête SQL")
    st.code(query, language="sql")

    try:
        # Sécurité basique
        if "drop" in query.lower() or "delete" in query.lower():
            st.error("Requête non autorisée 🚫")
        else:
            result = conn.execute(query).df()

            st.subheader("📊 Résultat")
            st.dataframe(result)

            # Comparaison
            st.subheader("🆚 Comparaison avec les données source")

            try:
                # Colonnes communes
                common_cols = list(set(df.columns).intersection(result.columns))

                if common_cols:
                    df_base = df[common_cols].reset_index(drop=True)
                    df_res = result[common_cols].reset_index(drop=True)

                    # Vérifier taille identique
                    if df_base.shape == df_res.shape:
                        comparison = df_base.compare(df_res)

                        if comparison.empty:
                            st.success("✅ Aucune différence trouvée")
                        else:
                            st.dataframe(comparison)
                    else:
                        st.info("ℹ️ Impossible de comparer : tailles différentes")
                else:
                    st.info("ℹ️ Aucune colonne commune pour comparaison")

            except Exception as e:  # pylint: disable=broad-exception-caught
                st.warning(f"Erreur lors de la comparaison : {e}")


    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Erreur SQL : {e}")
