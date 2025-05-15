import streamlit as st
import pandas as pd
from utils.analisis import evaluar_parrilla
from generador.generador_formatos import generar_propuestas

st.set_page_config(page_title="FormatScope", layout="wide")
st.title("📺 FormatScope: Evaluador Inteligente de Parrilla Televisiva")

uploaded_file = st.file_uploader("📤 Sube tu parrilla televisiva en CSV", type=["csv"])
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