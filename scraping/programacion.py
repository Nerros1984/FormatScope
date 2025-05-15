from scraping.teletexto import obtener_desde_teletexto
import pandas as pd

def obtener_parrilla_web(canal: str) -> pd.DataFrame:
    """
    Intenta obtener la parrilla televisiva del canal especificado usando Teletexto.
    Si falla, devuelve un DataFrame vacío con una fila de error.
    """
    df = obtener_desde_teletexto(canal)

    if df.empty:
        return pd.DataFrame([{
            "fecha": pd.Timestamp.today().date(),
            "día_semana": "Sin datos",
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

    return df
