from datetime import datetime
from scraping.movistarplus import obtener_desde_movistarplus
from scraping.tvguia import obtener_desde_tvguia
from utils.helpers import get_day_name_es
import pandas as pd

def obtener_parrilla_web(canal):
    df = obtener_desde_movistarplus(canal)
    if df.empty:
        df = obtener_desde_tvguia(canal)
    if df.empty:
        return pd.DataFrame([{
            "fecha": datetime.now().date().isoformat(),
            "día_semana": get_day_name_es(datetime.now().date().isoformat()),
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
