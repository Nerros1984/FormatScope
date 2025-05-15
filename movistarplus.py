import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from utils.helpers import get_day_name_es

MOVISTARPLUS_SLUGS = {
    "La 1": "tve", "La 2": "la2", "Antena 3": "a3", "Cuatro": "c4", "Telecinco": "t5",
    "La Sexta": "sexta", "Canal Sur": "canalsur", "TV3": "tv3", "ETB 2": "etb2",
    "TVG": "tvg", "Telemadrid": "telemadrid"
}

def obtener_desde_movistarplus(canal):
    slug = MOVISTARPLUS_SLUGS.get(canal)
    if not slug:
        return pd.DataFrame()
    url = f"https://www.movistarplus.es/programacion-tv/{slug}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        bloques = soup.select(".bloque-programa")
        registros = []
        for bloque in bloques:
            hora = bloque.select_one(".hora")
            titulo = bloque.select_one(".titulo")
            categoria = bloque.select_one(".categoria")
            registros.append({
                "fecha": datetime.now().date().isoformat(),
                "día_semana": get_day_name_es(datetime.now().date()),
                "hora": hora.get_text(strip=True) if hora else "",
                "programa": titulo.get_text(strip=True) if titulo else "",
                "canal": canal,
                "franja": "",
                "categoría": categoria.get_text(strip=True).capitalize() if categoria else "",
                "tipo": "",
                "logotipo": "",
                "sinopsis": "",
                "url": url
            })
        return pd.DataFrame(registros)
    except:
        return pd.DataFrame()
