
import pandas as pd
from scraping.teletexto import obtener_desde_teletexto

def obtener_parrilla_web(canal: str, fecha: str = None) -> pd.DataFrame:
    """
    Intenta obtener programación desde Teletexto.com.
    """
    df = obtener_desde_teletexto(canal, fecha)
    if not df.empty:
        return df

    # Si ninguna fuente devuelve datos válidos
    return pd.DataFrame([{
        "fecha": fecha or pd.Timestamp.now().date(),
        "día_semana": pd.Timestamp.now().day_name(locale='es_ES.utf8'),
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
