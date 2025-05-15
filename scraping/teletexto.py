import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from scraping.utils.helpers import get_day_name_es

# Slugs por canal
TELETEXTO_SLUGS = {
    "La 1": "tve1",
    "La 2": "tve2",
    "Antena 3": "antena3",
    "Cuatro": "cuatro",
    "Telecinco": "telecinco",
    "La Sexta": "la6"
}

def obtener_desde_teletexto(canal):
    slug = TELETEXTO_SLUGS.get(canal)
    if not slug:
        return pd.DataFrame()

    url = f"https://www.teletexto.com/teletexto.asp?programacion={slug}&tv=n"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    bloques = soup.select(".programacion")

    registros = []
    fecha_hoy = datetime.now().date().strftime("%Y-%m-%d")
    dia_semana = get_day_name_es(fecha_hoy)

    for fila in soup.select(".hora_programacion"):
        try:
            hora = fila.select_one(".hora").get_text(strip=True)
            nombre = fila.select_one(".titulo").get_text(strip=True)
            categoria = fila.select_one(".genero").get_text(strip=True) if fila.select_one(".genero") else ""
            
            registros.append({
                "fecha": fecha_hoy,
                "día_semana": dia_semana,
                "hora": hora,
                "programa": nombre,
                "canal": canal,
                "franja": "",
                "categoría": categoria,
                "tipo": "",
                "logotipo": "",
                "sinopsis": "",
                "url": url
            })
        except:
            continue

    return pd.DataFrame(registros)
