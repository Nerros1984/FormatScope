# utils/helpers.py
import locale
from datetime import datetime

def get_day_name_es(fecha_str):
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_TIME, 'es_ES')  # fallback
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    return fecha.strftime("%A").capitalize()
