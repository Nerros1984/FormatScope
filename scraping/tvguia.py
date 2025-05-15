# scraping/tvguia.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

TVGUIA_URLS = {
    "La 1": "https://tvguia.es/tv/programacion-la-1",
    "La 2": "https://tvguia.es/tv/programacion-la-2",
    "Antena 3": "https://tvguia.es/tv/programacion-antena-3",
    "Cuatro": "https://tvguia.es/tv/programacion-cuatro",
    "Telecinco": "https://tvguia.es/tv/programacion-telecinco",
    "La Sexta": "https://tvguia.es/tv/programacion-la-sexta"
    # Puedes ampliar con más canales si ves su patrón
}

def obtener_desde_tvguia(canal):
    url = TVGUIA_URLS.get(canal)
    if not url:
        return pd.DataFrame()

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except Exception:
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    filas = soup.select("table tbody tr")
    if not filas:
        return pd.DataFrame()

    registros = []
    for fila in filas:
        celdas = fila.find_all("td")
        if len(celdas) >= 2:
            hora = celdas[0].get_text(strip=True)
            nombre_elem = celdas[1].find("a")
            nombre = nombre_elem.get_text(strip=True) if nombre_elem else ""
            categoria_elem = celdas[1].find("span")
            categoria = categoria_elem.get_text(strip=True).capitalize() if categoria_elem else ""
            sinopsis = celdas[1].get_text(strip=True).replace(nombre, "").replace(categoria, "").strip()

            registros.append({
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "día_semana": datetime.now().strftime("%A"),
                "hora": hora,
                "programa": nombre,
                "canal": canal,
                "franja": "",  # opcional
                "categoría": categoria,
                "tipo": "",
                "logotipo": "",
                "sinopsis": sinopsis,
                "url": url
            })

    return pd.DataFrame(registros)
