import streamlit as st
import pandas as pd
from scraping.programacion import obtener_parrilla_web
from analisis.informes_canal import generar_informe_canal

st.set_page_config(page_title="FormatScope", page_icon="📺")
st.title("📺 FormatScope: Evaluador Inteligente de Parrilla Televisiva")

canales = ["La 1", "La 2", "Antena 3", "Cuatro", "Telecinco", "La Sexta", "Canal Sur", "TV3", "ETB 2", "TVG", "Telemadrid"]
canal = st.sidebar.selectbox("Selecciona un canal", canales)

if st.sidebar.button("🔍 Analizar programación"):
    df = obtener_parrilla_web(canal)
    st.write("Contenido del DataFrame devuelto:", df)
    if df.empty:
        st.error(f"No se pudo obtener la programación para {canal}.")
    else:
        st.success(f"Programación obtenida para {canal}")
        st.dataframe(df)
        st.markdown("### 🧠 Informe de tendencias")
        st.markdown(generar_informe_canal(df, canal))
