import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from utils.helpers import get_day_name_es

URL_BASE = "https://tvguia.es/tv/programacion-{slug}"

TVGUIA_SLUGS = {
    "La 1": "la-1",
    "La 2": "la-2",
    "Antena 3": "antena-3",
    "Cuatro": "cuatro",
    "Telecinco": "telecinco",
    "La Sexta": "la-sexta",
    "Canal Sur": "canalsur-andalucia",
    "TV3": "tv3-cataluna",
    "ETB 2": "etb-2",
    "TVG": "tvg",
    "Telemadrid": "telemadrid"
}

def obtener_desde_tvguia(canal):
    slug = TVGUIA_SLUGS.get(canal)
    if not slug:
        return pd.DataFrame()

    url = URL_BASE.format(slug=slug)
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception:
        return pd.DataFrame()

    soup = BeautifulSoup(res.text, "html.parser")
    filas = soup.select("div.programacion div.row")

    if not filas:
        return pd.DataFrame()

    registros = []
    for fila in filas:
        try:
            hora = fila.select_one("div.hora").text.strip()
            titulo = fila.select_one("div.titulo").text.strip()
            categoria = fila.select_one("div.categoria").text.strip().capitalize()
            registros.append({
                "fecha": datetime.now().date().isoformat(),
                "día_semana": get_day_name_es(datetime.now().date().isoformat()),
                "hora": hora,
                "programa": titulo,
                "canal": canal,
                "franja": "",
                "categoría": categoria,
                "tipo": "",
                "logotipo": "",
                "sinopsis": "",
                "url": url
            })
        except Exception:
            continue

    return pd.DataFrame(registros)
