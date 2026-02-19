import streamlit as st
import os
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

st.sidebar.page_link('pages/1_Dashboard.py', label='Dashboard')
st.sidebar.page_link('pages/2_Teacher.py', label='Teacher')

if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("app.py")

# ============================================================
# Detect Dark / Light Mode
# ============================================================
theme_detector = components.html(
    """
    <script>
    const theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? "dark" : "light";
    window.parent.postMessage({theme: theme}, "*");
    </script>
    """,
    height=0,
)

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

# Fallback (Streamlit doesn’t always catch postMessage immediately)
if st.get_option("theme.base") == "dark":
    st.session_state.theme_mode = "dark"
else:
    st.session_state.theme_mode = "light"

with st.sidebar:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if st.session_state.get("theme_mode", "light") == "dark":
        logo_path = os.path.join(BASE_DIR, "public", "logo.png")
    else:
        logo_path = os.path.join(BASE_DIR, "public", "logo_dark.png")

    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    
    if st.button("Logout"):
        st.session_state.user = False
        st.rerun()



# 1. Configuration de la page
st.set_page_config(page_title="Dashboard Exemple", layout="wide")

# 2. Titre et Description
st.title("📊 Tableau de Bord Interactif")
st.markdown("Exemple de dashboard simple avec Streamlit et Plotly.")

# 3. Chargement des données (Simulation)
@st.cache_data # Mise en cache pour la performance
def load_data():
    data = {
        'Produit': ['A', 'B', 'C', 'A', 'B', 'C'],
        'Ventes': [100, 150, 200, 120, 170, 220],
        'Region': ['Nord', 'Sud', 'Nord', 'Sud', 'Nord', 'Sud'],
        'Mois': ['Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb']
    }
    return pd.DataFrame(data)

df = load_data()

# 4. Sidebar - Filtres
st.sidebar.header("Filtres")
region_filter = st.sidebar.multiselect(
    "Sélectionner la région:",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Application du filtre
df_filtered = df[df["Region"].isin(region_filter)]

# 5. Métriques principales
st.subheader("Métriques Clés")
col1, col2, col3 = st.columns(3)
total_ventes = df_filtered["Ventes"].sum()
col1.metric("Ventes Totales", f"{total_ventes} €")
col2.metric("Produits Uniques", df_filtered["Produit"].nunique())
col3.metric("Régions", len(region_filter))

st.markdown("---")

# 6. Graphiques
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Ventes par Produit")
    fig_bar = px.bar(df_filtered, x="Produit", y="Ventes", color="Region", barmode="group")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    st.subheader("Répartition par Région")
    fig_pie = px.pie(df_filtered, values="Ventes", names="Region")
    st.plotly_chart(fig_pie, use_container_width=True)

# 7. Affichage des données brutes
st.subheader("Données Filtrées")
st.dataframe(df_filtered)

# Pour lancer : streamlit run nom_du_fichier.py
