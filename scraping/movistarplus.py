import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

LOGOS = {
    "La 1": "...",
    "La 2": "...",
    "Antena 3": "...",
    "Cuatro": "...",
    "Telecinco": "...",
    "La Sexta": "...",
    "Canal Sur": "...",
    "TV3": "...",
    "ETB 2": "...",
    "TVG": "...",
    "Telemadrid": "..."
}

SLUGS = {
    "La 1": "la-1", "La 2": "la-2", "Antena 3": "a3", "Cuatro": "cuatro", "Telecinco": "telecinco",
    "La Sexta": "la-sexta", "Canal Sur": "canal-sur", "TV3": "tv3", "ETB 2": "etb-2", "TVG": "tvg", "Telemadrid": "telemadrid"
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

def enriquecer_programa(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        categoria = soup.select_one(".categories").text.strip() if soup.select_one(".categories") else "desconocido"
        tipo = soup.select_one(".content-type").text.strip() if soup.select_one(".content-type") else "desconocido"
        sinopsis = soup.select_one(".long-sinopsis").text.strip() if soup.select_one(".long-sinopsis") else ""
        return categoria, tipo, sinopsis
    except:
        return "desconocido", "desconocido", ""

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
        link_tag = bloque.find("a", href=True)
        if hora_tag and prog_tag:
            hora = hora_tag.text.strip()
            prog = prog_tag.text.strip()
            url_ficha = "https://www.movistarplus.es" + link_tag["href"] if link_tag else None
            categoria, tipo, sinopsis = enriquecer_programa(url_ficha) if url_ficha else ("desconocido", "desconocido", "")
            dia_semana = datetime.strptime(fecha, "%Y-%m-%d").strftime("%A")
            datos.append({
                "fecha": fecha,
                "día_semana": dia_semana,
                "hora": hora,
                "programa": prog,
                "canal": canal,
                "franja": asignar_franja(hora),
                "categoría": categoria,
                "tipo": tipo,
                "logotipo": LOGOS.get(canal, ""),
                "sinopsis": sinopsis
            })

    return pd.DataFrame(datos)
