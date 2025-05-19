import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# === FUNCIONES AUXILIARES ===
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# === INTERFAZ STREAMLIT ===
st.set_page_config(page_title="RSI en tiempo real", layout="wide")
st.title("📈 Seguimiento RSI en Tiempo Real")

symbol = st.selectbox("Selecciona el símbolo (cripto):", ["ETH-USD", "BTC-USD", "SOL-USD", "ADA-USD"])

# === DESCARGA DE DATOS ===
df = yf.download(symbol, period="1d", interval="5m")

if df.empty:
    st.error("No se encontraron datos para este símbolo.")
    st.stop()

# === Cálculo RSI y señales ===
df["RSI"] = compute_rsi(df["Close"])
df["Signal"] = df["RSI"].apply(lambda x: "BUY" if x < 30 else ("SELL" if x > 70 else None))

# === Gráfico de velas + RSI ===
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
    name="Precio"
))

buy_signals = df[df["Signal"] == "BUY"]
sell_signals = df[df["Signal"] == "SELL"]

fig.add_trace(go.Scatter(
    x=buy_signals.index,
    y=buy_signals["Close"],
    mode="markers",
    name="BUY",
    marker=dict(symbol="triangle-up", color="green", size=10)
))

fig.add_trace(go.Scatter(
    x=sell_signals.index,
    y=sell_signals["Close"],
    mode="markers",
    name="SELL",
    marker=dict(symbol="triangle-down", color="red", size=10)
))

fig.update_layout(title=f"Estrategia RSI - {symbol}", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# === Gráfico RSI ===
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI", line=dict(color="orange")))
fig_rsi.add_hline(y=30, line=dict(dash="dash", color="green"))
fig_rsi.add_hline(y=70, line=dict(dash="dash", color="red"))
fig_rsi.update_layout(title="Indicador RSI", yaxis_range=[0, 100])
st.plotly_chart(fig_rsi, use_container_width=True)
