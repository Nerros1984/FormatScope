import pandas as pd

def generar_informe_canal(df: pd.DataFrame, canal: str) -> str:
    if df.empty:
        return f"No hay datos disponibles para el canal {canal}."

    # Validar que existe la columna 'canal'
    if "canal" not in df.columns:
        return "❌ Error: los datos cargados no contienen columna 'canal'."

    # Filtrar por canal
    df_canal = df[df["canal"] == canal]

    if df_canal.empty:
        return f"No hay datos disponibles para el canal {canal}."

    # Comprobar si hay algún programa válido o solo errores
    if df_canal["programa"].str.contains("No se pudo obtener programación", case=False).all():
        return f"No se pudo obtener la programación real para {canal}."

    total_programas = len(df_canal)
    categorias = df_canal["categoría"].value_counts().to_dict()

    resumen = f"📡 **Resumen del canal {canal}**\n\n"
    resumen += f"- Total de programas registrados: **{total_programas}**\n"
    
    if categorias:
        resumen += "- Distribución por categoría:\n"
        for categoria, cantidad in categorias.items():
            resumen += f"  - {categoria}: {cantidad}\n"
    else:
        resumen += "- No se encontraron categorías clasificadas.\n"

    return resumen
