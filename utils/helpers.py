import calendar
from datetime import datetime

def get_day_name_es(fecha_iso):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    if isinstance(fecha_iso, str):
        fecha = datetime.fromisoformat(fecha_iso)
    else:
        fecha = fecha_iso
    return dias[fecha.weekday()]
