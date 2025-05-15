from scraping.rtv_teletexto import obtener_desde_rtv_teletexto
from scraping.teletexto_com import obtener_desde_teletexto_com
from scraping.movistarplus import obtener_desde_movistarplus
from scraping.elmundo import obtener_desde_elmundo
from scraping.fallback import plantilla_vacia

def obtener_parrilla_web(canal):
    for extractor in [obtener_desde_rtv_teletexto, obtener_desde_teletexto_com, obtener_desde_movistarplus, obtener_desde_elmundo]:
        try:
            df = extractor(canal)
            if not df.empty:
                return df
        except Exception as e:
            print(f"Error en extractor {extractor.__name__}: {e}")
    return plantilla_vacia(canal)
