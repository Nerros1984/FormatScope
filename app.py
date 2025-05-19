import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Seguimiento RSI en Tiempo Real", layout="wide")

# Función para obtener datos OHLC desde Binance
def obtener_datos_binance(symbol="ETHUSDT", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = df["close"].astype(float)
    return df[["timestamp", "close"]]

# Cálculo de RSI
def calcular_rsi(series, periodo=14):
    delta = series.diff()
    ganancia = np.where(delta > 0, delta, 0)
    perdida = np.where(delta < 0, -delta, 0)

    ganancia_ema = pd.Series(ganancia).ewm(span=periodo, adjust=False).mean()
    perdida_ema = pd.Series(perdida).ewm(span=periodo, adjust=False).mean()

    rs = ganancia_ema / perdida_ema
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Detección de señales
def detectar_senales(df, rsi):
    señales = []
    for i in range(1, len(rsi)):
        if rsi[i-1] < 30 and rsi[i] >= 30:
            señales.append(("BUY", df["timestamp"].iloc[i], df["close"].iloc[i]))
        elif rsi[i-1] > 70 and rsi[i] <= 70:
            señales.append(("SELL", df["timestamp"].iloc[i], df["close"].iloc[i]))
    return señales

# Título
st.title("📈 Seguimiento RSI en Tiempo Real")

# Selector de símbolo (de momento ETH-USDT fijo)
simbolo = st.selectbox("Selecciona el símbolo (cripto):", ["ETHUSDT"])

# Obtener y procesar datos
df = obtener_datos_binance(simbolo)
rsi = calcular_rsi(df["close"])
df["RSI"] = rsi

# Detectar señales
senales = detectar_senales(df, rsi)

# Gráfico principal
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["timestamp"], y=df["close"], mode="lines", name="Precio", line=dict(color="deepskyblue")))

for tipo, fecha, precio in senales:
    color = "green" if tipo == "BUY" else "red"
    fig.add_trace(go.Scatter(x=[fecha], y=[precio],
                             mode="markers+text",
                             name=tipo,
                             text=[tipo],
                             textposition="top center",
                             marker=dict(color=color, size=10)))

fig.update_layout(title=f"Estrategia RSI - {simbolo}",
                  xaxis_title="Hora",
                  yaxis_title="Precio USDT",
                  height=500)

st.plotly_chart(fig, use_container_width=True)

# Gráfico de RSI
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df["timestamp"], y=df["RSI"], mode="lines", name="RSI", line=dict(color="orange")))
fig_rsi.add_shape(type="line", x0=df["timestamp"].iloc[0], x1=df["timestamp"].iloc[-1],
                  y0=70, y1=70, line=dict(color="red", dash="dash"))
fig_rsi.add_shape(type="line", x0=df["timestamp"].iloc[0], x1=df["timestamp"].iloc[-1],
                  y0=30, y1=30, line=dict(color="green", dash="dash"))
fig_rsi.update_layout(title="Indicador RSI",
                      xaxis_title="Hora",
                      yaxis_title="RSI",
                      height=300)

st.plotly_chart(fig_rsi, use_container_width=True)

# Refrescar automáticamente cada 5 segundos
st.experimental_rerun() if st.button("🔁 Refrescar ahora") else time.sleep(5)
st.experimental_rerun()
