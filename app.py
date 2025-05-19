import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import os

# --- Configuración general ---
st.set_page_config(page_title="Velas Japonesas", page_icon="📉", layout="wide")
st.title("📉 Seguimiento Velas Japonesas en Tiempo Real")
st.subheader("Estrategia Velas - ETHUSDT")

# --- API Key desde variable de entorno (o directamente si prefieres) ---
API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY") or "321df943198bbf65ed2e1043a50321d128519bd0fdefbd855bfe5d2e0b3b60fb"

def obtener_velas(symbol="ETH", currency="USD", limit=30):
    url = f"https://min-api.cryptocompare.com/data/v2/histominute?fsym={symbol}&tsym={currency}&limit={limit}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data["Response"] != "Success":
        return None

    df = pd.DataFrame(data["Data"]["Data"])
    df["datetime"] = pd.to_datetime(df["time"], unit="s")
    return df

# --- Bucle de actualización ---
placeholder = st.empty()

while True:
    df = obtener_velas()
    if df is None or df.empty:
        st.error("❌ No se pudo cargar el gráfico. Verifica la conexión o vuelve a intentarlo.")
        break

    with placeholder.container():
        st.markdown("⏱️ *Actualizando cada segundo...*")

        fig = go.Figure(data=[go.Candlestick(
            x=df["datetime"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            increasing_line_color='green',
            decreasing_line_color='red'
        )])
        fig.update_layout(title="Velas Japonesas ETH/USD", xaxis_title="Hora", yaxis_title="Precio", height=600)
        st.plotly_chart(fig, use_container_width=True)

    time.sleep(1)
