def generar_informe_canal(df, canal):
    if df.empty or "programa" not in df.columns:
        return "No se puede generar informe: datos insuficientes."
    total = len(df)
    top_categoria = df["categoría"].value_counts().idxmax()
    if "canal" not in df.columns:
        return "No se ha podido generar el informe: faltan columnas en los datos."

    df_canal = df[df["canal"] == canal]
    resumen += f"🗂️ La categoría más frecuente es **{top_categoria}**."
    return resumen
