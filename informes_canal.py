def generar_informe_canal(df, canal):
    if df.empty or "programa" not in df.columns:
        return "No se puede generar informe: datos insuficientes."
    total = len(df)
    top_categoria = df["categoría"].value_counts().idxmax()
    resumen = f"📊 El canal **{canal}** tiene {total} programas listados hoy.\n"
    resumen += f"🗂️ La categoría más frecuente es **{top_categoria}**."
    return resumen
