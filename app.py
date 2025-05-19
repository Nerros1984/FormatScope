# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from binance.client import Client
import os
import time

# Autorefresco cada 10 segundos
st.set_page_config(page_title="Seguimiento RSI en Tiempo Real", layout="wide")

st.title("📉 Seguimiento Velas Japonesas en Tiempo Real")

# Conexión con Binance
api_key = os.getenv("BINANCE_API_KEY", "VexjaLA4Xtx5zAW0qQ8K9NsD9CAd18TVWA3PzMAD0aknEH4I7jdhkpOkVZeSnpWJ")
api_secret = os.getenv("BINANCE_API_SECRET", "KSrlsfavMrFXtWvST5o3XnW0qaCpKHGk6qJ5bJbslQYv1S9uJtuGoeTI7jkzZPzj")
client = Client(api_key, api_secret)

# Selección de símbolo
symbol = st.selectbox("Selecciona el símbolo (cripto)", ["ETHEUR", "ETHUSDT", "BTCUSDT"], index=0)

# Parámetros de velas
interval = Client.KLINE_INTERVAL_1MINUTE
limit = 100

# Obtener datos de Binance
@st.cache_data(ttl=10)
def obtener_datos_binance():
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume", 
            "close_time", "quote_asset_volume", "number_of_trades", 
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        return df
    except Exception as e:
        st.error(f"❌ Error al obtener datos: {e}")
        return pd.DataFrame()

df = obtener_datos_binance()

if not df.empty:
    # Gráfico de velas japonesas
    fig = go.Figure(data=[go.Candlestick(
        x=df["timestamp"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Precio"
    )])
    fig.update_layout(title=f"Velas Japonesas - {symbol}", xaxis_title="Fecha", yaxis_title="Precio")
    st.plotly_chart(fig, use_container_width=True)

    # Detección de patrón básico: 3 picos ascendentes
    ultimos_cierres = df["close"].tail(5).values
    if len(ultimos_cierres) >= 3:
        if ultimos_cierres[-3] < ultimos_cierres[-2] < ultimos_cierres[-1]:
            st.success("✅ Señal de COMPRA: patrón de 3 cierres ascendentes detectado.")
        elif ultimos_cierres[-3] > ultimos_cierres[-2] > ultimos_cierres[-1]:
            st.warning("⚠️ Señal de VENTA: patrón de 3 cierres descendentes detectado.")
        else:
            st.info("ℹ️ Sin señal clara en los últimos 3 minutos.")
else:
    st.warning("Esperando datos válidos para mostrar el gráfico...")

# Forzar actualización automática cada 10 segundos
st.experimental_rerun()
