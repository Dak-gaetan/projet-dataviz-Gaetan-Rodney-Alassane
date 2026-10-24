"""Dashboard Streamlit : récit contexte -> constat -> recommandation.

Lit uniquement la couche gold dans PostgreSQL.
"""
import os

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title="Vélib : disponibilité", layout="wide")


@st.cache_resource
def get_engine():
    url = (
        f"postgresql+psycopg2://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ.get('POSTGRES_HOST', 'localhost')}:{os.environ.get('POSTGRES_PORT', '5432')}"
        f"/{os.environ['POSTGRES_DB']}"
    )
    return create_engine(url)


@st.cache_data(ttl=300)
def charger(table: str) -> pd.DataFrame:
    return pd.read_sql(f"SELECT * FROM {table}", get_engine())


st.title("Vélib : où et quand manque-t-il des vélos ?")
st.caption("Persona : [à compléter]. Question principale : [à compléter].")

# --- Filtre interactif (au moins un requis) ---
# TODO : brancher sur les colonnes réelles de la table gold
# arrondissement = st.sidebar.multiselect("Arrondissement", options=[...])

# --- KPI (3 à 5, fiches dans docs/kpi.md) ---
col1, col2, col3 = st.columns(3)
col1.metric("KPI 1", "—")
col2.metric("KPI 2", "—")
col3.metric("KPI 3", "—")

# --- Récit ---
st.header("1. Contexte")
st.info("À compléter après la construction de la couche gold.")

st.header("2. Constat")
# df = charger("gold_penurie_par_heure")
# st.plotly_chart(px.bar(df, x="heure", y="taux_penurie"), use_container_width=True)

st.header("3. Recommandation")
st.info("À compléter.")
