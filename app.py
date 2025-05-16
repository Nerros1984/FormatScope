# app.py
import streamlit as st
import pandas as pd
import openai
from io import BytesIO

# Clave de API (usa secrets en Streamlit Cloud)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else ""

def obtener_informacion(titulo, campo):
    prompt = f"Proporciona la {campo} del programa de televisión titulado '{titulo}'."
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return respuesta.choices[0].message['content'].strip()
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

def main():
    st.title("FormatScope - Enriquecimiento de parrilla televisiva")

    archivo = st.file_uploader("Sube tu archivo 'parrillas_tv.xlsx'", type=["xlsx"])

    if archivo is not None:
        df = pd.read_excel(archivo)
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

if __name__ == "__main__":
    main()
