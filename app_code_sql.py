"""
Application Streamlit pour explorer des données avec DuckDB
et exécuter des requêtes SQL interactives.
"""

import pandas as pd
import duckdb
import streamlit as st

# =========================
# Connexion DuckDB
# =========================

conn = duckdb.connect(
    database="data/exercices_sql_tables.duckdb",
    read_only=False
)

# =========================
# Chargement memory_state
# =========================

memory_state = conn.execute(
    "SELECT * FROM memory_state"
).df()

# Nom de la table à explorer
table_name = memory_state.loc[0, "table"]

# Chargement des données
df = conn.execute(
    f"SELECT * FROM {table_name}"
).df()

# =========================
# Sidebar
# =========================

with st.sidebar:
    st.title("📌 Menu")

    st.subheader("📝 Exercice")

    if not memory_state.empty:
        st.write(f"**Thème :** {memory_state.loc[0, 'theme']}")
        st.write(f"**Exercice :** {memory_state.loc[0, 'exercice_name']}")
        st.write(f"**Table :** {memory_state.loc[0, 'table']}")
        st.write(
            f"**Dernière révision :** "
            f"{memory_state.loc[0, 'last_reviewed']}"
        )

    queries = {
        "Choisir une requête...": "",
        "Tout afficher":
            f"SELECT * FROM {table_name}",

        "Somme de a":
            f"SELECT SUM(a) AS somme_a FROM {table_name}",

        "Moyenne de b":
            f"SELECT AVG(b) AS moyenne_b FROM {table_name}",

        "Filtrer a > 1":
            f"SELECT * FROM {table_name} WHERE a > 1",

        "Somme par catégorie": f"""
            SELECT
                categorie,
                SUM(a) AS total_a,
                AVG(b) AS moyenne_b
            FROM {table_name}
            GROUP BY categorie
        """
    }

    selected_query = st.selectbox(
        "Requêtes exemples",
        list(queries.keys())
    )

    st.subheader("📊 Données source")
    st.dataframe(df)

    st.subheader("🧱 Schéma")

    schema_df = pd.DataFrame({
        "colonne": df.columns,
        "type": df.dtypes.astype(str)
    })

    st.table(schema_df)

# =========================
# Zone principale
# =========================

default_query = queries[selected_query]

st.title("🧠 Explorateur SQL avec DuckDB")

st.subheader(f"📂 Table utilisée : {table_name}")

st.dataframe(df)

query = st.text_area(
    "Ton code SQL",
    value=default_query,
    height=150
)

# =========================
# Exécution SQL
# =========================

if query.strip():

    st.subheader("🔎 Requête SQL")
    st.code(query, language="sql")

    try:

        forbidden = ["drop", "delete", "truncate"]

        if any(word in query.lower() for word in forbidden):
            st.error("Requête non autorisée 🚫")

        else:

            result = conn.execute(query).df()

            st.subheader("📊 Résultat")
            st.dataframe(result)

            st.subheader("🆚 Comparaison avec les données source")

            try:

                common_cols = list(
                    set(df.columns).intersection(result.columns)
                )

                if common_cols:

                    df_base = df[common_cols].reset_index(drop=True)
                    df_res = result[common_cols].reset_index(drop=True)

                    if df_base.shape == df_res.shape:

                        comparison = df_base.compare(df_res)

                        if comparison.empty:
                            st.success(
                                "✅ Aucune différence trouvée"
                            )
                        else:
                            st.dataframe(comparison)

                    else:
                        st.info(
                            "ℹ️ Impossible de comparer : "
                            "tailles différentes"
                        )

                else:
                    st.info(
                        "ℹ️ Aucune colonne commune pour comparaison"
                    )

            except Exception as e:
                st.warning(
                    f"Erreur lors de la comparaison : {e}"
                )

    except Exception as e:
        st.error(f"Erreur SQL : {e}")