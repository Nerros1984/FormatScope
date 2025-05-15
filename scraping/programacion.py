import requests
from bs4 import BeautifulSoup
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

def obtener_parrilla_web(canal):
    url = URLS.get(canal)
    if not url:
        return pd.DataFrame(columns=["hora", "programa", "canal"])

    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    bloques = soup.find_all("li", class_="tv-listing__item")

    datos = []
    for bloque in bloques:
        hora_tag = bloque.find("span", class_="tv-listing__hour")
        titulo_tag = bloque.find("span", class_="tv-listing__title")
        if hora_tag and titulo_tag:
            datos.append({
                "hora": hora_tag.text.strip(),
                "programa": titulo_tag.text.strip(),
                "canal": canal
            })

    return pd.DataFrame(datos)
