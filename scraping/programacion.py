import requests
from bs4 import BeautifulSoup
from scraping.rtv_teletexto import obtener_desde_rtv_teletexto
from scraping.teletexto_com import obtener_desde_teletexto_com
from scraping.fallback import plantilla_vacia

import pandas as pd

URLS = {
    "Antena 3": "https://www.lavanguardia.com/television/programacion-tv/antena-3",
    "La 1": "https://www.lavanguardia.com/television/programacion-tv/la-1",
    "Telecinco": "https://www.lavanguardia.com/television/programacion-tv/telecinco",
    "Cuatro": "https://www.lavanguardia.com/television/programacion-tv/cuatro",
    "La Sexta": "https://www.lavanguardia.com/television/programacion-tv/la-sexta",
    "Canal Sur": "https://www.lavanguardia.com/television/programacion-tv/canal-sur",
    "TV3": "https://www.lavanguardia.com/television/programacion-tv/tv3",
    "ETB": "https://www.lavanguardia.com/television/programacion-tv/etb-2",
    "TVG": "https://www.lavanguardia.com/television/programacion-tv/tvg",
    "Telemadrid": "https://www.lavanguardia.com/television/programacion-tv/telemadrid",
}

from scraping.rtv_teletexto import obtener_desde_rtv_teletexto
from scraping.teletexto_com import obtener_desde_teletexto_com
from scraping.fallback import plantilla_vacia

def obtener_parrilla_web(canal):
    for extractor in [obtener_desde_rtv_teletexto, obtener_desde_teletexto_com]:
        try:
            df = extractor(canal)
            if not df.empty:
                return df
        except Exception as e:
            print(f"Error en extractor {extractor.__name__}: {e}")
    return plantilla_vacia(canal)
