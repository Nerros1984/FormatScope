import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

SLUGS_ELMUNDO = {
    "La 1": "la-1"
}

def asignar_franja(hora):
    try:
        h = int(hora.split(":")[0])
    except:
        return "desconocida"
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
        print(f"[ERROR] Código {r.status_code} al acceder a {url}")
        return pd.DataFrame()

    soup = BeautifulSoup(r.text, "html.parser")
    bloques = soup.select("li")

    datos = []
    hoy = datetime.now().strftime("%Y-%m-%d")
    dia_semana = datetime.now().strftime("%A")

    for bloque in bloques:
        hora_raw = bloque.find(text=lambda t: t and ":" in t and len(t.strip()) <= 5)
        programa_tag = bloque.select_one("p.nombre-programa a")
        sinopsis_tag = bloque.select_one("div.sinopsis-programa")

        if hora_raw and programa_tag:
            hora = hora_raw.strip()
            programa = programa_tag.text.strip()
            sinopsis = sinopsis_tag.text.strip() if sinopsis_tag else ""
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
                "sinopsis": sinopsis
            })

    return pd.DataFrame(datos)
