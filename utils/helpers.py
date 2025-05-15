import locale
from datetime import datetime

def get_day_name_es(fecha_str):
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux/Mac
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')  # Windows
        except:
            return "Día"

    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    return fecha.strftime("%A").capitalize()
