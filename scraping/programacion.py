import pandas as pd
import os
from datetime import datetime
from scraping.elmundo import obtener_desde_elmundo

HISTORICO_CSV = "historico_programacion.csv"

def plantilla_vacia(canal):
    return pd.DataFrame([{
        "fecha": datetime.now().strftime("%Y-%m-%d"),
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

def cargar_historico():
    if os.path.exists(HISTORICO_CSV):
        return pd.read_csv(HISTORICO_CSV)
    return pd.DataFrame()

def guardar_en_historico(df_nueva):
    if df_nueva.empty:
        return
    if os.path.exists(HISTORICO_CSV):
        df_existente = pd.read_csv(HISTORICO_CSV)
        df_combinada = pd.concat([df_existente, df_nueva])
        df_combinada.drop_duplicates(subset=["fecha", "canal", "hora", "programa"], inplace=True)
    else:
        df_combinada = df_nueva
    df_combinada.to_csv(HISTORICO_CSV, index=False)

def obtener_parrilla_web(canal):
    hoy = datetime.now().strftime("%Y-%m-%d")

    # 1. Buscar en histórico local
    df_hist = cargar_historico()
    df_filtro = df_hist[(df_hist["fecha"] == hoy) & (df_hist["canal"] == canal)]
    if not df_filtro.empty:
        return df_filtro

    # 2. Buscar en El Mundo
    df_web = obtener_desde_elmundo(canal)
    if not df_web.empty:
        guardar_en_historico(df_web)
        return df_web

    # 3. Devolver plantilla vacía
    return plantilla_vacia(canal)
