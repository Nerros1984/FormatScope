import pandas as pd

def plantilla_vacia(canal):
    return pd.DataFrame([
        {"fecha": "", "día_semana": "", "hora": "", "programa": "Sin datos", "canal": canal, "franja": "", "categoría": "", "logotipo": ""}
    ])
