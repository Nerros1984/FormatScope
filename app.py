import streamlit as st
import pandas as pd
import requests
import time
import plotly.graph_objects as go
from datetime import datetime

# Configuracion inicial
st.set_page_config(page_title="Seguimiento Velas Japonesas en Tiempo Real", layout="wide")
st.title("📉 Seguimiento Velas Japonesas en Tiempo Real")

symbol = st.selectbox("Selecciona el símbolo (cripto):", ["ETHEUR", "BTCUSDT", "ETHUSDT"])

st.markdown(f"### Estrategia Velas - {symbol.upper()}")
status = st.empty()
chart = st.empty()

# Funcion para obtener velas sin autenticar
def obtener_velas_binance(symbol="ETHEUR", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"])
        df["timestamp"] = pd.to_datetime(df["open_time"], unit="ms")
        df["close"] = df["close"].astype(float)
        return df[["timestamp", "close"]]
    else:
        return pd.DataFrame()

# Bucle de actualizacion
while True:
    status.info("🔄 Cargando datos en tiempo real...")

    df = obtener_velas_binance(symbol)

    if df.empty:
        status.error("❌ Error al obtener datos desde Binance (público)")
        break

    # Grafico de precio
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["close"], mode="lines+markers", name="Precio"))
    fig.update_layout(
        xaxis_title="Hora",
        yaxis_title="Precio",
        showlegend=True,
        height=500
    )

    chart.plotly_chart(fig, use_container_width=True)
    status.success("✅ Datos actualizados")
    time.sleep(5)  # Actualiza cada 5 segundos
