# scraping/movistarplus.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

CANAL_IFRAME_SLUGS = {
    "La 1": "tve",
    "La 2": "la2",
    "Antena 3": "a3",
    "Cuatro": "c4",
    "Telecinco": "t5",
    "La Sexta": "sexta"
}

def obtener_desde_movistarplus(canal, fecha=None):
    slug = CANAL_IFRAME_SLUGS.get(canal)
    if not slug:
        return pd.DataFrame()

    url = f"https://static.movistarplus.es/recorte/movistarplus/{slug}/programacion.html"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception:
        return pd.DataFrame()

    soup = BeautifulSoup(res.text, "html.parser")
    bloques = soup.find_all("div", class_="bloque")

    registros = []
    hoy = datetime.now().date()
    dia_semana = hoy.strftime("%A")

    for bloque in bloques:
        hora = bloque.find("div", class_="hora")
        titulo = bloque.find("div", class_="titulo")
        categoria = bloque.find("div", class_="categoria")
        tipo = categoria.text if categoria else ""

        if not hora or not titulo:
            continue

        registros.append({
            "fecha": str(hoy),
            "día_semana": dia_semana,
            "hora": hora.text.strip(),
            "programa": titulo.text.strip(),
            "canal": canal,
            "franja": "",
            "categoría": tipo,
            "tipo": "",
            "logotipo": "",
            "sinopsis": "",
            "url": ""
        })

    return pd.DataFrame(registros)
