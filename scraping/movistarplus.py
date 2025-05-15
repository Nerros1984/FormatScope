import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

LOGOS = {
    "La 1": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/La_1_%282019%29.svg/512px-La_1_%282019%29.svg.png",
    "La 2": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/La_2_%282019%29.svg/512px-La_2_%282019%29.svg.png",
    "Antena 3": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Antena_3_logo_2022.svg/512px-Antena_3_logo_2022.svg.png",
    "Cuatro": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Cuatro_logo_2022.svg/512px-Cuatro_logo_2022.svg.png",
    "Telecinco": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Telecinco_logo_2022.svg/512px-Telecinco_logo_2022.svg.png",
    "La Sexta": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/LaSexta_logo.svg/512px-LaSexta_logo.svg.png",
    "Canal Sur": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Logo_Canal_Sur_2020.svg/512px-Logo_Canal_Sur_2020.svg.png",
    "TV3": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/TV3_Catalunya.svg/512px-TV3_Catalunya.svg.png",
    "ETB 2": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/ETB_logo.svg/512px-ETB_logo.svg.png",
    "TVG": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/TVG_logo_2020.svg/512px-TVG_logo_2020.svg.png",
    "Telemadrid": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Telemadrid_Logo.svg/512px-Telemadrid_Logo.svg.png"
}

SLUGS = {
    "La 1": "la-1",
    "La 2": "la-2",
    "Antena 3": "a3",
    "Cuatro": "cuatro",
    "Telecinco": "telecinco",
    "La Sexta": "la-sexta",
    "Canal Sur": "canal-sur",
    "TV3": "tv3",
    "ETB 2": "etb-2",
    "TVG": "tvg",
    "Telemadrid": "telemadrid"
}

def asignar_franja(hora):
    h = int(hora.split(":")[0])
    if h < 6:
        return "madrugada"
    elif h < 12:
        return "morning"
    elif h < 14:
        return "midday"
    elif h < 16:
        return "early afternoon"
    elif h < 20:
        return "late afternoon"
    elif h < 22:
        return "access prime time"
    elif h < 24:
        return "prime time"
    else:
        return "late night"

def obtener_desde_movistarplus(canal, fecha=None):
    if canal not in SLUGS:
        return pd.DataFrame()

    slug = SLUGS[canal]
    if not fecha:
        fecha = datetime.now().strftime("%Y-%m-%d")

    url = f"https://www.movistarplus.es/programacion-tv/{slug}/{fecha}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    bloques = soup.select(".list-programs-item")
    datos = []

    for bloque in bloques:
        hora_tag = bloque.find("time")
        prog_tag = bloque.find("h4")
        if hora_tag and prog_tag:
            hora = hora_tag.text.strip()
            prog = prog_tag.text.strip()
            dia_semana = datetime.strptime(fecha, "%Y-%m-%d").strftime("%A")
            datos.append({
                "fecha": fecha,
                "día_semana": dia_semana,
                "hora": hora,
                "programa": prog,
                "canal": canal,
                "franja": asignar_franja(hora),
                "categoría": "desconocido",
                "logotipo": LOGOS.get(canal, "")
            })

    return pd.DataFrame(datos)