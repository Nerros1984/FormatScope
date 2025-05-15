import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import unicodedata

# Mapa para traducir nombres de días al español
dias_semana_es = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

def obtener_desde_elmundo(canal: str, fecha: str = None) -> pd.DataFrame:
    canal_slug = {
        "La 1": "la-1",
        "La 2": "la-2",
        "Antena 3": "antena-3",
        "Cuatro": "cuatro",
        "Telecinco": "telecinco",
        "La Sexta": "la-sexta",
    }.get(canal, None)

    if canal_slug is None:
        return pd.DataFrame(columns=["fecha", "día_semana", "hora", "programa", "canal", "franja", "categoría", "tipo", "logotipo", "sinopsis", "url"])

    url = f"https://www.elmundo.es/television/programacion-tv/{canal_slug}.html"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        bloques = soup.find_all("li", class_="hora-emision")
        filas = []

        for bloque in bloques:
            hora_tag = bloque.find("time")
            nombre_tag = bloque.find("a")
            categoria_tag = bloque.find("strong")
            sinopsis_tag = bloque.find_next_sibling("p")

            if not hora_tag or not nombre_tag:
                continue

            hora = hora_tag.text.strip()
            programa = nombre_tag.text.strip()
            url_programa = nombre_tag["href"] if nombre_tag.has_attr("href") else ""
            categoria = categoria_tag.text.strip() if categoria_tag else ""
            sinopsis = sinopsis_tag.text.strip() if sinopsis_tag else ""

            # Datos de contexto
            hoy = datetime.now().date()
            dia_semana = dias_semana_es.get(hoy.strftime('%A'), hoy.strftime('%A'))

            fila = {
                "fecha": hoy.isoformat(),
                "día_semana": dia_semana,
                "hora": hora,
                "programa": programa,
                "canal": canal,
                "franja": "",
                "categoría": categoria,
                "tipo": "",
                "logotipo": "",
                "sinopsis": sinopsis,
                "url": url_programa,
            }
            filas.append(fila)

        if not filas:
            return pd.DataFrame([{
                "fecha": datetime.now().date().isoformat(),
                "día_semana": dias_semana_es.get(datetime.now().strftime('%A'), datetime.now().strftime('%A')),
                "hora": "Sin datos",
                "programa": "No se pudo obtener programación",
                "canal": canal,
                "franja": "",
                "categoría": "",
                "tipo": "",
                "logotipo": "",
                "sinopsis": "",
                "url": ""
            }])

        return pd.DataFrame(filas)

    except Exception as e:
        return pd.DataFrame([{
            "fecha": datetime.now().date().isoformat(),
            "día_semana": dias_semana_es.get(datetime.now().strftime('%A'), datetime.now().strftime('%A')),
            "hora": "Sin datos",
            "programa": f"Error al acceder a elmundo.es: {str(e)}",
            "canal": canal,
            "franja": "",
            "categoría": "",
            "tipo": "",
            "logotipo": "",
            "sinopsis": "",
            "url": ""
        }])
