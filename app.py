# app.py
import streamlit as st
import pandas as pd
from openai import OpenAI
from io import BytesIO
import os

# Clave de API desde secretos
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

def obtener_informacion(titulo, campo):
    prompt = f"Proporciona la {campo} del programa de televisión titulado '{titulo}'."
    try:
        st.write(f"🔎 Buscando {campo} para: {titulo}")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        contenido = response.choices[0].message.content.strip()
        return contenido if contenido else f"Sin datos ({campo})"
    except Exception as e:
        return f"Error al obtener {campo}: {e}"

def enriquecer_datos(df):
    for index, fila in df.iterrows():
        if pd.isna(fila.get('sinopsis')):
            df.at[index, 'sinopsis'] = obtener_informacion(fila['titulo'], 'sinopsis')
        if pd.isna(fila.get('tipo')):
            df.at[index, 'tipo'] = obtener_informacion(fila['titulo'], 'tipo de programa')
        if pd.isna(fila.get('primera_emision')):
            df.at[index, 'primera_emision'] = obtener_informacion(fila['titulo'], 'fecha de primera emisión')
        if pd.isna(fila.get('audiencia_media')):
            df.at[index, 'audiencia_media'] = obtener_informacion(fila['titulo'], 'audiencia media estimada')
    return df

def analizar_oportunidades(df):
    st.subheader("🔍 Análisis de oportunidades")
    resumen = ""
    for index, fila in df.iterrows():
        resumen += f"- {fila['titulo']} ({fila['categoria']}): {fila.get('sinopsis', '')}\n"

    prompt = (
        "A partir de esta parrilla televisiva, sugiere líneas de contenido o formatos que podrían funcionar bien "
        "en una televisión nacional o internacional, explicando el porqué.\n\n" + resumen
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        recomendaciones = response.choices[0].message.content.strip()
        st.markdown("### Recomendaciones de nuevos formatos")
        st.write(recomendaciones)
    except Exception as e:
        st.error(f"Error al generar informe: {e}")

def main():
    st.title("📺 FormatScope")

    archivo = st.file_uploader("Sube tu archivo 'parrillas_tv.xlsx'", type=["xlsx"])

    if archivo is not None:
        df = pd.read_excel(archivo)
        st.subheader("Analiza parrillas y sugiere contenidos")
st.subheader("Analiza parrillas y sugiere contenidos")
st.write("Vista previa del archivo cargado:")
st.dataframe(df)

        if st.button("Enriquecer datos del archivo"):
            with st.spinner("Consultando IA para completar campos..."):
                df_enriquecido = enriquecer_datos(df)
                st.success("Enriquecimiento completado")
                st.dataframe(df_enriquecido)

                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_enriquecido.to_excel(writer, index=False, sheet_name='Parrilla Enriquecida')
                output.seek(0)

                st.download_button(
                    label="Descargar archivo enriquecido",
                    data=output,
                    file_name="parrillas_enriquecidas.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                analizar_oportunidades(df_enriquecido)

if __name__ == "__main__":
    main()
