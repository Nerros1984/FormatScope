import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

SLUGS_ELMUNDO = {
    "La 1": "la-1",
    "La 2": "la-2",
    "Antena 3": "antena-3",
    "Cuatro": "cuatro",
    "Telecinco": "telecinco",
    "La Sexta": "la-sexta"
}

def asignar_franja(hora):
    try:
        h = int(hora.split(":")[0])
    except:
        return "desconocida"
    if h < 6: return "madrugada"
    elif h < 12: return "mañana"
    elif h < 15: return "mediodía"
    elif h < 20: return "tarde"
    elif h < 22: return "access prime time"
    elif h < 24: return "prime time"
    return "desconocida"

def obtener_desde_elmundo(canal):
    slug = SLUGS_ELMUNDO.get(canal)
    if not slug:
        return pd.DataFrame()

    url = f"https://www.elmundo.es/television/programacion-tv/{slug}.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return pd.DataFrame()

    soup = BeautifulSoup(r.text, "html.parser")
    bloques = soup.select("div.guia-programa-item")

    registros = []
    fecha = datetime.now().strftime("%Y-%m-%d")
    dia_semana = datetime.now().strftime("%A")

    for bloque in bloques:
        hora_tag = bloque.select_one("span.hora-programa")
        nombre_tag = bloque.select_one("p.nombre-programa a")
        sinopsis_tag = bloque.select_one("div.sinopsis-programa")

        if not hora_tag or not nombre_tag:
            continue

        hora = hora_tag.text.strip()
        programa = nombre_tag.text.strip()
        sinopsis = sinopsis_tag.text.strip() if sinopsis_tag else ""
        link = nombre_tag.get("href", "")

        registros.append({
            "fecha": fecha,
            "día_semana": dia_semana,
            "hora": hora,
            "programa": programa,
            "canal": canal,
            "franja": asignar_franja(hora),
            "categoría": "desconocido",
            "tipo": "desconocido",
            "logotipo": "",
            "sinopsis": sinopsis,
            "url": link
        })

    return pd.DataFrame(registros)
