import streamlit as st
import plotly.graph_objects as go
from binance.client import Client
import pandas as pd
import time

# Leer claves desde secrets
api_key = st.secrets["binance"]["api_key"]
api_secret = st.secrets["binance"]["api_secret"]

# Inicializar cliente de Binance
client = Client(api_key, api_secret)

# Configuración de la página
st.set_page_config(page_title="Seguimiento Velas Japonesas en Tiempo Real", layout="wide")
st.title("📉 Seguimiento Velas Japonesas en Tiempo Real")

symbol = "ETHUSDT"
st.subheader(f"Estrategia Velas - {symbol}")

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            # Obtener datos de velas
            klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=30)

            df = pd.DataFrame(klines, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
            ])

            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)

            # Crear gráfico de velas
            fig = go.Figure(data=[
                go.Candlestick(
                    x=df["timestamp"],
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"],
                    increasing_line_color='green', decreasing_line_color='red'
                )
            ])

            fig.update_layout(title=f"Velas Japonesas {symbol}", xaxis_title="Hora", yaxis_title="Precio")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("<p style='color: gray;'>🕒 Actualizando cada segundo...</p>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ No se pudo cargar el gráfico. Verifica la conexión o vuelve a intentarlo.\n{e}")

    time.sleep(1)
