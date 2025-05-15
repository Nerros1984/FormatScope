# scraping/elmundo.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

CANAL_SLUGS_ELMUNDO = {
    "La 1": "la-1",
    "La 2": "la-2",
    "Antena 3": "antena-3",
    "Cuatro": "cuatro",
    "Telecinco": "telecinco",
    "La Sexta": "la-sexta"
}

def obtener_desde_elmundo(canal: str, fecha: str) -> pd.DataFrame:
    slug = CANAL_SLUGS_ELMUNDO.get(canal)
    if not slug:
        return pd.DataFrame()

    url = f"https://www.elmundo.es/television/programacion-tv/{slug}.html"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return pd.DataFrame()

        soup = BeautifulSoup(response.text, 'html.parser')
        bloques = soup.select("div[data-el='bloque-programa']")

        if not bloques:
            return pd.DataFrame()

        datos = []
        for bloque in bloques:
            hora = bloque.select_one(".hour")
            genero = bloque.select_one(".category")
            nombre = bloque.select_one(".title")
            sinopsis = bloque.select_one(".description")

            datos.append({
                "fecha": fecha,
                "día_semana": datetime.strptime(fecha, "%Y-%m-%d").strftime("%A"),
                "hora": hora.text.strip() if hora else "",
                "programa": nombre.text.strip() if nombre else "",
                "canal": canal,
                "franja": "",  # Puedes derivar de hora si lo necesitas
                "categoría": genero.text.strip() if genero else "",
                "tipo": "",
                "logotipo": "",
                "sinopsis": sinopsis.text.strip() if sinopsis else "",
                "url": ""
            })

        return pd.DataFrame(datos)
    except Exception:
        return pd.DataFrame()
