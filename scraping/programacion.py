from scraping.movistarplus import obtener_desde_movistarplus
from scraping.tvguia import obtener_desde_tvguia

def obtener_parrilla_web(canal, fecha=None):
    # 1. Intenta con Movistar Plus
    df = obtener_desde_movistarplus(canal, fecha)
    if not df.empty:
        return df

    # 2. Si falla, intenta con TVGuia
    df = obtener_desde_tvguia(canal, fecha)
    if not df.empty:
        return df

    # 3. Si todo falla, devuelve DataFrame vacío con estructura
    import pandas as pd
    from datetime import datetime
    return pd.DataFrame([{
        "fecha": fecha if fecha else datetime.now().strftime("%Y-%m-%d"),
        "día_semana": "",
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
