import requests
from bs4 import BeautifulSoup
import pandas as pd

URLS = {
    "Antena 3": "https://www.teletexto.com/programacion/antena-3",
    "Cuatro": "https://www.teletexto.com/programacion/cuatro",
    "Telecinco": "https://www.teletexto.com/programacion/telecinco",
    "La Sexta": "https://www.teletexto.com/programacion/la-sexta",
    "Canal Sur": "https://www.teletexto.com/programacion/canal-sur",
    "TV3": "https://www.teletexto.com/programacion/tv3",
    "ETB": "https://www.teletexto.com/programacion/etb-2",
    "TVG": "https://www.teletexto.com/programacion/tvg",
    "Telemadrid": "https://www.teletexto.com/programacion/telemadrid"
}

def obtener_desde_teletexto_com(canal):
    url = URLS.get(canal)
    if not url:
        return pd.DataFrame()

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    bloques = soup.select("div.grid div.row")
    datos = []

    for bloque in bloques:
        hora = bloque.select_one("div.col-xs-2")
        titulo = bloque.select_one("div.col-xs-10")
        if hora and titulo:
            datos.append({
                "hora": hora.get_text(strip=True),
                "programa": titulo.get_text(strip=True),
                "canal": canal
            })

    return pd.DataFrame(datos)