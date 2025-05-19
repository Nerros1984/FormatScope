import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="Seguimiento ETHUSD en Tiempo Real", layout="wide")
st.title("📈 Seguimiento Velas Japonesas en Tiempo Real")

# Solo trabajaremos con este símbolo
symbol = "ETHUSDT"
st.markdown(f"### Estrategia Velas - {symbol}")

# Cargar los datos
@st.cache_data(ttl=60)
def obtener_datos_binance(symbol="ETHUSDT", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)

        return df[["timestamp", "open", "high", "low", "close"]]
    except Exception as e:
        st.error(f"❌ Error al obtener datos desde Binance: {e}")
        return pd.DataFrame()

with st.spinner("⏳ Cargando datos en tiempo real..."):
    df = obtener_datos_binance(symbol)

if not df.empty:
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name="ETHUSDT"
    ))
    fig.update_layout(
        title=f"Velas Japonesas - {symbol}",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        xaxis_rangeslider_visible=False,
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("❌ No se pudo cargar el gráfico. Verifica la conexión o vuelve a intentarlo.")
