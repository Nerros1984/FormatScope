# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from scraping.elmundo import obtener_desde_elmundo

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
    hoy = datetime.now().strftime("%Y-%m-%d")
    df = obtener_desde_elmundo(canal, hoy)
    if df.empty or "hora" not in df.columns:
        st.error(f"No se pudo obtener la programación para {canal}.")
        df = pd.DataFrame([{
            "fecha": hoy,
            "día_semana": datetime.now().strftime("%A"),
            "hora": "Sin datos",
            "programa": "No se pudo obtener programación",
            "canal": canal,
            "franja": "",
            "categoría": "",
            "tipo": "",
            "logotipo": "",
            "sinopsis": "",
            "url": ""
        }])
    else:
        st.success(f"Parrilla cargada automáticamente para {canal}")
    st.dataframe(df)

st.markdown("### 🗃️ O sube manualmente un CSV de parrilla")
uploaded_file = st.file_uploader("Drag and drop file here", type=["csv"])
if uploaded_file:
    df_manual = pd.read_csv(uploaded_file)
    st.success("CSV cargado correctamente.")
    st.dataframe(df_manual)

st.markdown("## 📅 Generar histórico de programación (±7 días)")
if st.button("📦 Generar histórico completo"):
    canales = [
        "La 1", "La 2", "Antena 3", "Cuatro", "Telecinco", "La Sexta"
    ]
    hoy = datetime.now().date()
    rango_dias = range(-7, 7)

    registros = []
    progreso = st.progress(0)
    total = len(canales) * len(rango_dias)
    paso = 0

    for canal in canales:
        for delta in rango_dias:
            fecha = (hoy + timedelta(days=delta)).strftime("%Y-%m-%d")
            st.write(f"🔍 Obteniendo {canal} - {fecha}")
            df = obtener_desde_elmundo(canal, fecha)
            if not df.empty:
                registros.append(df)
            paso += 1
            progreso.progress(paso / total)

    if registros:
        df_historico = pd.concat(registros, ignore_index=True)
        st.success(f"✅ Histórico generado con {len(df_historico)} registros.")
        st.dataframe(df_historico)

        csv = df_historico.to_csv(index=False).encode("utf-8")
        st.download_button("💾 Descargar CSV", data=csv, file_name="historico_parrilla.csv", mime="text/csv")
    else:
        st.warning("No se pudieron obtener datos para ningún canal en el rango.")
