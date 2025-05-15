import streamlit as st
import pandas as pd
from scraping.programacion import obtener_parrilla_web

st.set_page_config(page_title="FormatScope", page_icon="📺")
st.title("📺 FormatScope: Evaluador Inteligente de Parrilla Televisiva")

st.sidebar.markdown("## 🧭 Obtener parrilla automáticamente")
tipo_tv = st.sidebar.radio("Tipo de televisión", ["Nacional", "Autonómica"])

if tipo_tv == "Nacional":
    canales = ["La 1", "La 2", "Antena 3", "Cuatro", "Telecinco", "La Sexta"]
else:
    canales = ["TV3", "ETB 2", "TVG", "Canal Sur", "Telemadrid"]

canal = st.sidebar.selectbox("Selecciona canal", canales)

if st.sidebar.button("🔍 Buscar programación"):
    df = obtener_parrilla_web(canal)
    if df.empty or "hora" not in df.columns:
        st.error(f"No se pudo obtener la programación para {canal}.")
    else:
        st.success(f"Parrilla cargada automáticamente para {canal}")
        st.dataframe(df)

st.markdown("### 🗃️ O sube manualmente un CSV de parrilla")
uploaded_file = st.file_uploader("Drag and drop file here", type=["csv"])
if uploaded_file:
    df_manual = pd.read_csv(uploaded_file)
    st.success("CSV cargado correctamente.")
    st.dataframe(df_manual)
