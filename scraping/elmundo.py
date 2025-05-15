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
    h = int(hora.split(":")[0])
    if h < 6: return "madrugada"
    elif h < 12: return "morning"
    elif h < 14: return "midday"
    elif h < 16: return "early afternoon"
    elif h < 20: return "late afternoon"
    elif h < 22: return "access prime time"
    elif h < 24: return "prime time"
    return "late night"

def obtener_desde_elmundo(canal):
    slug = SLUGS_ELMUNDO.get(canal)
    if not slug:
        return pd.DataFrame()

    url = f"https://www.elmundo.es/television/programacion-tv/{slug}.html"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code != 200:
        return pd.DataFrame()

    soup = BeautifulSoup(r.text, "html.parser")
    bloques = soup.select(".ue-c-article__body ul li")

    datos = []
    hoy = datetime.now().strftime("%Y-%m-%d")
    dia_semana = datetime.now().strftime("%A")

    for bloque in bloques:
        hora_tag = bloque.select_one("strong")
        programa_tag = bloque.select_one("span")
        if hora_tag and programa_tag:
            hora = hora_tag.text.strip().replace("h", ":00")  # ejemplo 08h → 08:00
            programa = programa_tag.text.strip()
            datos.append({
                "fecha": hoy,
                "día_semana": dia_semana,
                "hora": hora,
                "programa": programa,
                "canal": canal,
                "franja": asignar_franja(hora),
                "categoría": "desconocido",
                "tipo": "desconocido",
                "logotipo": "",
                "sinopsis": ""
            })

    return pd.DataFrame(datos)