import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from utils.helpers import get_day_name_es

# Slugs válidos para Movistar+
MOVISTARPLUS_SLUGS = {
    "La 1": "tve",
    "La 2": "la2",
    "Antena 3": "a3",
    "Cuatro": "c4",
    "Telecinco": "t5",
    "La Sexta": "sexta",
    "Canal Sur": "canalsur",
    "TV3": "tv3",
    "ETB 2": "etb2",
    "TVG": "tvg",
    "Telemadrid": "telemadrid"
}

def obtener_desde_movistarplus(canal, fecha=None):
    slug = MOVISTARPLUS_SLUGS.get(canal)
    if not slug:
        return pd.DataFrame()

    if not fecha:
        fecha = datetime.now().strftime("%Y-%m-%d")

    url = f"https://www.movistarplus.es/programacion-tv/{slug}/{fecha}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception:
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    bloques = soup.select(".bloque-programa")
    if not bloques:
        return pd.DataFrame()

    registros = []
    for bloque in bloques:
        hora = bloque.select_one(".hora")
        titulo = bloque.select_one(".titulo")
        categoria = bloque.select_one(".categoria")

        registros.append({
            "fecha": fecha,
            "día_semana": get_day_name_es(fecha),
            "hora": hora.get_text(strip=True) if hora else "",
            "programa": titulo.get_text(strip=True) if titulo else "",
            "canal": canal,
            "franja": "",  # Opcional, puedes calcular según la hora
            "categoría": categoria.get_text(strip=True).capitalize() if categoria else "",
            "tipo": "",
            "logotipo": "",
            "sinopsis": "",
            "url": url
        })

    return pd.DataFrame(registros)
