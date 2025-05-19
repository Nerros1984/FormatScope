# app.py
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Seguimiento RSI en Tiempo Real", layout="wide")

st.markdown("## 📉 Seguimiento RSI en Tiempo Real")
symbol = st.selectbox("Selecciona el símbolo (cripto):", options=["ETH-USD", "BTC-USD", "ADA-USD"], index=0)

# Carga de datos en tiempo real
@st.cache_data(ttl=60)
def cargar_datos(symbol):
    try:
        df = yf.download(tickers=symbol, interval="1m", period="1d", progress=False)
        df = df[["Close"]].copy()
        df.reset_index(inplace=True)
        df.rename(columns={"Close": "Precio", "Datetime": "timestamp"}, inplace=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

df = cargar_datos(symbol)

# Validación
if df.empty or len(df) < 15:
    st.warning("⚠️ No se han encontrado suficientes datos para mostrar el gráfico.")
    st.stop()

# RSI
delta = df["Precio"].diff()
ganancia = delta.where(delta > 0, 0)
perdida = -delta.where(delta < 0, 0)
media_ganancia = ganancia.rolling(window=14).mean()
media_perdida = perdida.rolling(window=14).mean()
rs = media_ganancia / media_perdida
rsi = 100 - (100 / (1 + rs))
df["RSI"] = rsi

# Señales
df["señal"] = ""
df.loc[df["RSI"] < 30, "señal"] = "compra"
df.loc[df["RSI"] > 70, "señal"] = "venta"

# === GRÁFICO PRECIO ===
fig_precio = go.Figure()
fig_precio.add_trace(go.Scatter(x=df["timestamp"], y=df["Precio"], mode="lines", name="Precio", line=dict(color="blue")))

# Marcar señales
compra = df[df["señal"] == "compra"]
venta = df[df["señal"] == "venta"]

fig_precio.add_trace(go.Scatter(x=compra["timestamp"], y=compra["Precio"], mode="markers", name="COMPRA", marker=dict(color="green", symbol="triangle-up", size=10)))
fig_precio.add_trace(go.Scatter(x=venta["timestamp"], y=venta["Precio"], mode="markers", name="VENTA", marker=dict(color="red", symbol="triangle-down", size=10)))

fig_precio.update_layout(title=f"Estrategia RSI - {symbol}", xaxis_title="Fecha", yaxis_title="Precio")

# === GRÁFICO RSI ===
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df["timestamp"], y=df["RSI"], mode="lines", name="RSI", line=dict(color="orange")))
fig_rsi.add_shape(type="line", x0=df["timestamp"].iloc[0], x1=df["timestamp"].iloc[-1], y0=70, y1=70, line=dict(dash="dash", color="red"))
fig_rsi.add_shape(type="line", x0=df["timestamp"].iloc[0], x1=df["timestamp"].iloc[-1], y0=30, y1=30, line=dict(dash="dash", color="green"))
fig_rsi.update_layout(title="Indicador RSI", xaxis_title="Fecha", yaxis_title="RSI")

# === VISUALIZACIÓN ===
st.plotly_chart(fig_precio, use_container_width=True)
st.plotly_chart(fig_rsi, use_container_width=True)
