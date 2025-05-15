def evaluar_parrilla(df):
    resumen = {}
    resumen["Total de programas"] = len(df)
    if 'genero' in df.columns:
        resumen["Géneros más comunes"] = df['genero'].value_counts().head(3).to_dict()
    if 'franja' in df.columns and 'programa' in df.columns:
        resumen["Franjas vacías"] = list(df[df['programa'].isna()]["franja"].unique())
    return resumen