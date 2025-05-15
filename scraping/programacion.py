import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base (usamos La Vanguardia, fácil de scrapear)
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
    
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    bloques = soup.select(".tv-listing__hour-block")

    datos = []
    for bloque in bloques:
        hora = bloque.select_one(".tv-listing__hour")
        programa = bloque.select_one(".tv-listing__title")
        if hora and programa:
            datos.append({
                "hora": hora.get_text(strip=True),
                "programa": programa.get_text(strip=True),
                "canal": canal
            })

    return pd.DataFrame(datos)
