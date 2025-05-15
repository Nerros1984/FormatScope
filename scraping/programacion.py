from scraping.movistarplus import obtener_desde_movistarplus

def obtener_parrilla_web(canal, fecha=None):
    return obtener_desde_movistarplus(canal, fecha)
