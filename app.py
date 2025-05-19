import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# === Funciones auxiliares ===
def calcular_rsi(data, periodo=14):
    delta = data['Close'].diff()
    ganancia = delta.where(delta > 0, 0.0)
    perdida = -delta.where(delta < 0, 0.0)
    media_ganancia = ganancia.rolling(window=periodo).mean()
    media_perdida = perdida.rolling(window=periodo).mean()
    rs = media_ganancia / media_perdida
    rsi = 100 - (100 / (1 + rs))
    return rsi

def detectar_senal_rsi(data, umbral_compra=30, umbral_venta=70):
    ultima_rsi = data['RSI'].iloc[-1]
    if ultima_rsi < umbral_compra:
        return "compra"
    elif ultima_rsi > umbral_venta:
        return "venta"
    else:
        return None

# === Configuración de la app ===
st.set_page_config(layout="wide")
st.title("⚖️ Señales RSI en tiempo real")

# === Selección de símbolo ===
simbolo = "ETH-EUR"
st.write(f"Visualizando: {simbolo}")

# === Carga de datos ===
data = yf.download(simbolo, interval="1m", period="1d")
if data.empty:
    st.error("No se pudo obtener datos en tiempo real.")
    st.stop()

data['RSI'] = calcular_rsi(data)
senal = detectar_senal_rsi(data)

# === Gráfico ===
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name='Precio'))

if senal == "compra":
    fig.add_trace(go.Scatter(
        x=[data.index[-1]],
        y=[data['Close'].iloc[-1]],
        mode='markers',
        marker=dict(color='green', size=12),
        name='Compra'))
elif senal == "venta":
    fig.add_trace(go.Scatter(
        x=[data.index[-1]],
        y=[data['Close'].iloc[-1]],
        mode='markers',
        marker=dict(color='red', size=12),
        name='Venta'))

fig.update_layout(height=600, xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# === RSI y señal ===
st.subheader("🌎 Estado actual RSI")
st.metric("RSI", round(data['RSI'].iloc[-1], 2))
if senal:
    st.success(f"Señal detectada: {senal.upper()}")
else:
    st.info("Sin señal en este momento")
