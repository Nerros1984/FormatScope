import streamlit as st
import pandas as pd
from utils.analisis import evaluar_parrilla
from generador.generador_formatos import generar_propuestas
from scraping.programacion import obtener_parrilla_web

st.set_page_config(page_title="FormatScope", layout="wide")
st.title("📺 FormatScope: Evaluador Inteligente de Parrilla Televisiva")

# === NUEVA SECCIÓN: EXTRACCIÓN AUTOMÁTICA ===
st.sidebar.header("🛰️ Obtener parrilla automáticamente")

tipo_tv = st.sidebar.radio("Tipo de televisión", ["Nacional", "Autonómica"])

canales_nacionales = ["La 1", "Antena 3", "Telecinco", "Cuatro", "La Sexta"]
canales_autonomicas = ["Canal Sur", "TV3", "ETB", "TVG", "Telemadrid"]

canal = st.sidebar.selectbox("Selecciona canal",
                             canales_nacionales if tipo_tv == "Nacional" else canales_autonomicas)

if st.sidebar.button("🔍 Buscar programación"):
    df_auto = obtener_parrilla_web(canal)
    st.success(f"Parrilla cargada automáticamente para {canal}")
    st.dataframe(df_auto)
    df_auto.to_csv("data/parrilla_auto.csv", index=False)

# === CARGA MANUAL ===
uploaded_file = st.file_uploader("📤 O sube manualmente un CSV de parrilla", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Parrilla cargada")
    st.dataframe(df)

    with st.expander("🧠 Evaluación automática"):
        resultado = evaluar_parrilla(df)
        st.write(resultado)

    with st.expander("🎬 Propuestas de nuevos formatos"):
        propuestas = generar_propuestas(df)
        for p in propuestas:
            st.markdown(f"**{p['titulo']}**")
            st.write(p['descripcion'])
