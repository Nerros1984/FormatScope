import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# Configuración
st.set_page_config(page_title="RSI en Tiempo Real", layout="wide")
st_autorefresh(interval=1000, key="rsi_refresh")

# Interfaz
st.title("📈 Seguimiento RSI en Tiempo Real")
simbolo = st.selectbox("Selecciona el símbolo (cripto):", ["ETH-USD", "BTC-USD"])

# Funciones RSI y señales
def calcular_rsi(df, periodo=14):
    delta = df["Close"].diff()
    ganancia = delta.where(delta > 0, 0)
    perdida = -delta.where(delta < 0, 0)
    media_ganancia = ganancia.rolling(window=periodo).mean()
    media_perdida = perdida.rolling(window=periodo).mean()
    rs = media_ganancia / media_perdida
    rsi = 100 - (100 / (1 + rs))
    df["RSI"] = rsi
    return df

def detectar_senales(df):
    df["Señal"] = None
    for i in range(1, len(df)):
        if df["RSI"].iloc[i - 1] < 30 and df["RSI"].iloc[i] >= 30:
            df.loc[df.index[i], "Señal"] = "COMPRA"
        elif df["RSI"].iloc[i - 1] > 70 and df["RSI"].iloc[i] <= 70:
            df.loc[df.index[i], "Señal"] = "VENTA"
    return df

# Carga de datos (últimas 2 horas en velas de 1m)
fin = datetime.now()
inicio = fin - timedelta(hours=2)
df = yf.download(tickers=simbolo, start=inicio, end=fin, interval="1m", progress=False)

if df.empty:
    st.error("❌ No se pudieron obtener datos del activo seleccionado.")
    st.stop()

df = calcular_rsi(df)
df = detectar_senales(df)

# Gráfico de Precio + Entradas/Salidas
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Precio"))
fig.add_trace(go.Scatter(x=df[df["Señal"] == "COMPRA"].index, y=df[df["Señal"] == "COMPRA"]["Close"],
                         mode="markers", name="📈 COMPRA", marker=dict(color="green", size=10, symbol="triangle-up")))
fig.add_trace(go.Scatter(x=df[df["Señal"] == "VENTA"].index, y=df[df["Señal"] == "VENTA"]["Close"],
                         mode="markers", name="📉 VENTA", marker=dict(color="red", size=10, symbol="triangle-down")))
fig.update_layout(title=f"Estrategia RSI - {simbolo}", xaxis_title="Fecha", yaxis_title="Precio", height=500)

# Gráfico RSI
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df.index, y=df["RSI"], mode="lines", name="RSI", line=dict(color="orange")))
fig_rsi.add_hline(y=70, line=dict(color="red", dash="dash"))
fig_rsi.add_hline(y=30, line=dict(color="green", dash="dash"))
fig_rsi.update_layout(title="Indicador RSI", xaxis_title="Fecha", yaxis_title="RSI", height=300, yaxis=dict(range=[0, 100]))

# Mostrar
st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(fig_rsi, use_container_width=True)
