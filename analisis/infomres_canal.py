import pandas as pd
from collections import Counter
from datetime import datetime

def generar_informe_canal(df, canal):
    if df.empty or "canal" not in df.columns:
        return f"No hay datos disponibles para {canal}."

    df_canal = df[df["canal"] == canal]
    if df_canal.empty:
        return f"No se encontraron emisiones registradas para {canal}."

    # … el resto del análisis como estaba

    total_programas = len(df_canal)
    dias = df_canal["día_semana"].value_counts().to_dict()
    franjas = df_canal["franja"].value_counts().to_dict()
    categorias = df_canal["categoría"].value_counts().to_dict()
    programas = df_canal["programa"].value_counts().head(3).to_dict()

    dia_mas_emisiones = max(dias, key=dias.get)
    franja_dominante = max(franjas, key=franjas.get) if franjas else "-"
    categoria_principal = max(categorias, key=categorias.get) if categorias else "-"

    resumen = f"""
📺 **Informe de canal: {canal}**

- Total de emisiones analizadas: {total_programas}
- Día con más emisiones: {dia_mas_emisiones}
- Franja horaria dominante: {franja_dominante}
- Categoría más frecuente: {categoria_principal}
- Programas más emitidos:
"""
    for nombre, repeticiones in programas.items():
        resumen += f"  - {nombre} ({repeticiones} emisiones)\n"

    return resumen
