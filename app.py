import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

st.set_page_config(page_title="Velas Japonesas en Tiempo Real", layout="wide")

# === Configuración inicial ===
st.title("📉 Seguimiento Velas Japonesas en Tiempo Real")
SYMBOL = "ETHUSDT"
INTERVAL = "1m"
LIMIT = 50

# === Obtener datos públicos desde Binance ===
@st.cache_data(ttl=1)
def obtener_datos_binance():
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit={LIMIT}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=[
            'time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        df = df[['time', 'open', 'high', 'low', 'close']].astype(float)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        return df
    else:
        return None

# === Mostrar gráfico de velas japonesas ===
def mostrar_grafico(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='green',
        decreasing_line_color='red',
        name='ETH/USDT'
    )])
    fig.update_layout(title='Velas Japonesas ETH/USDT', xaxis_title='Hora', yaxis_title='Precio')
    st.plotly_chart(fig, use_container_width=True)

# === Loop de actualización automática ===
placeholder = st.empty()

while True:
    with placeholder.container():
        df = obtener_datos_binance()
        if df is not None and not df.empty:
            mostrar_grafico(df)
            st.success("✅ Datos en tiempo real actualizados.")
        else:
            st.error("❌ Error al obtener datos desde Binance (público)")

        st.caption("⏳ Actualizando cada segundo...")
        time.sleep(1)
