import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from binance.client import Client
from datetime import datetime, timedelta
import pytz

# Configurar API de Binance
API_KEY = "VexjaLA4Xtx5zAW0qQ8K9NsD9CAd18TVWA3PzMAD0aknEH4I7jdhkpOkVZeSnpWJ"
API_SECRET = "KSrlsfavMrFXtWvST5o3XnW0qaCpKHGk6qJ5bJbslQYv1S9uJtuGoeTI7jkzZPzj"
client = Client(API_KEY, API_SECRET)

# Configurar la app
st.set_page_config(page_title="Seguimiento RSI", layout="wide")
st.title("📉 Seguimiento RSI en Tiempo Real")

# Seleccionar símbolo
symbol = st.selectbox("Selecciona el símbolo (cripto):", ["ETHUSDT", "BTCUSDT", "BNBUSDT"])

# Obtener datos recientes (última hora, velas de 1 minuto)
def obtener_datos(symbol):
    now = datetime.utcnow()
    past = now - timedelta(hours=1)
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, past.strftime("%d %b %Y %H:%M:%S"))
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("Europe/Madrid")
    df["close"] = pd.to_numeric(df["close"])
    return df

# Calcular RSI
def calcular_rsi(df, periodo=14):
    delta = df["close"].diff()
    ganancia = delta.where(delta > 0, 0)
    perdida = -delta.where(delta < 0, 0)
    media_ganancia = ganancia.rolling(window=periodo).mean()
    media_perdida = perdida.rolling(window=periodo).mean()
    rs = media_ganancia / media_perdida
    rsi = 100 - (100 / (1 + rs))
    df["rsi"] = rsi
    return df

# Dibujar gráficos
def mostrar_graficos(df):
    fig_precio = go.Figure()
    fig_precio.add_trace(go.Scatter(x=df["timestamp"], y=df["close"], mode="lines", name="Precio"))

    # RSI con líneas de sobrecompra y sobreventa
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df["timestamp"], y=df["rsi"], line=dict(color='orange'), name="RSI"))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")

    st.subheader(f"Estrategia RSI - {symbol}")
    st.plotly_chart(fig_precio, use_container_width=True)
    st.subheader("Indicador RSI")
    st.plotly_chart(fig_rsi, use_container_width=True)

# Ejecutar lógica de actualización
try:
    df = obtener_datos(symbol)
    df = calcular_rsi(df)
    if not df.empty:
        mostrar_graficos(df)
    else:
        st.warning("No hay datos disponibles para mostrar el gráfico.")
except Exception as e:
    st.error(f"Error al obtener o procesar los datos: {e}")

# Autorefresco cada 1 segundo (sin botón manual)
st.experimental_rerun()
