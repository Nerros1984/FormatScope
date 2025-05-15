import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from scraping.utils.helpers import get_day_name_es

TELETEXTO_URLS = {
    "La 1": "https://www.teletexto.com/teletexto.asp?programacion=tve1&tv=n",
    "La 2": "https://www.teletexto.com/teletexto.asp?programacion=tve2&tv=n",
    "Antena 3": "https://www.teletexto.com/teletexto.asp?programacion=antena3&tv=n",
    "Cuatro": "https://www.teletexto.com/teletexto.asp?programacion=cuatro&tv=n",
    "Telecinco": "https://www.teletexto.com/teletexto.asp?programacion=telecinco&tv=n",
    "La Sexta": "https://www.teletexto.com/teletexto.asp?programacion=lasexta&tv=n"
}

def obtener_desde_teletexto(canal: str) -> pd.DataFrame:
    url = TELETEXTO_URLS.get(canal)
    if not url:
        return pd.DataFrame()

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception:
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    filas = soup.select("td[valign='top']")

    registros = []
    for i in range(0, len(filas), 3):
        try:
            hora = filas[i].get_text(strip=True)
            titulo = filas[i + 1].get_text(strip=True)
            categoria = filas[i + 2].get_text(strip=True)

            registros.append({
                "fecha": datetime.today().strftime("%Y-%m-%d"),
                "día_semana": get_day_name_es(datetime.today()),
                "hora": hora,
                "programa": titulo,
                "canal": canal,
                "franja": "",  # A implementar
                "categoría": categoria,
                "tipo": "",
                "logotipo": "",
                "sinopsis": "",
                "url": url
            })
        except IndexError:
            continue

    return pd.DataFrame(registros)
