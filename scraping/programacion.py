import pandas as pd
from scraping.elmundo import obtener_desde_elmundo
from scraping.movistarplus import obtener_desde_movistarplus
from scraping.fallback import plantilla_vacia

# Capa 1: histórico local (si decides implementarlo en el futuro)
# Capa 2: El Mundo
# Capa 3: Movistar Plus

def obtener_parrilla_web(canal, fecha=None):
    # 1. Intentamos El Mundo
    df = obtener_desde_elmundo(canal, fecha)
    if not df.empty:
        return df

    # 2. Intentamos Movistar Plus
    df = obtener_desde_movistarplus(canal, fecha)
    if not df.empty:
        return df

    # 3. Nada disponible, retornamos plantilla vacía
    return plantilla_vacia(canal, fecha)
