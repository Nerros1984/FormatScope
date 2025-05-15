def obtener_parrilla_web(canal: str) -> pd.DataFrame:
    df = obtener_desde_teletexto(canal)

    columnas = [
        "fecha", "día_semana", "hora", "programa", "canal", "franja",
        "categoría", "tipo", "logotipo", "sinopsis", "url"
    ]

    if df.empty:
        return pd.DataFrame([{
            "fecha": pd.Timestamp.today().date(),
            "día_semana": "Sin datos",
            "hora": "Sin datos",
            "programa": "No se pudo obtener programación",
            "canal": canal,
            "franja": "",
            "categoría": "",
            "tipo": "",
            "logotipo": "",
            "sinopsis": "",
            "url": ""
        }], columns=columnas)

    return df
