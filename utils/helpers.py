import locale
from datetime import datetime

def get_day_name_es(fecha_iso: str) -> str:
    try:
        # Establecer la localización en español (funciona en local si está instalada)
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        # En muchos entornos (como Streamlit Cloud) esto no funciona, así que se hace a mano
        dias = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        nombre_en = datetime.strptime(fecha_iso, "%Y-%m-%d").strftime('%A')
        return dias.get(nombre_en, nombre_en)
    else:
        return datetime.strptime(fecha_iso, "%Y-%m-%d").strftime('%A').capitalize()
