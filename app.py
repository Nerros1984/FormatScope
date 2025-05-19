import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from binance.client import Client
import time
import datetime
import numpy as np

# === Config ===
st.set_page_config(page_title="Seguimiento RSI en Tiempo Real", layout="wide")
st.title("📈 Seguimiento RSI en Tiempo Real")

# === Parámetros ===
API_KEY = "VexjaLA4Xtx5zAW0qQ8K9NsD9CAd18TVWA3PzMAD0aknEH4I7jdhkpOkVZeSnpWJ"
API_SECRET = "KSrlsfavMrFXtWvST5o3XnW0qaCpKHGk6qJ5bJbslQYv1S9uJtuGoeTI7jkzZPzj"
symbol = st.selectbox("Selecciona el símbolo (cripto):", ["ETHUSDT", "BTCUSDT", "BNBUSDT"])
timeframe = "1m"
lookback = 100

# === Funciones ===
def get_binance_data(symbol, interval, limit):
    client = Client(API_KEY, API_SECRET)
    candles = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(candles, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.astype(float)
    return df

def calcular_rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi
    return df

def detectar_senales(df):
    buy_signals = []
    sell_signals = []
    for i in range(1, len(df)):
        if df['RSI'].iloc[i] < 30 and df['RSI'].iloc[i - 1] >= 30:
            buy_signals.append(df['close'].iloc[i])
            sell_signals.append(np.nan)
        elif df['RSI'].iloc[i] > 70 and df['RSI'].iloc[i - 1] <= 70:
            buy_signals.append(np.nan)
            sell_signals.append(df['close'].iloc[i])
        else:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)
    df['Buy'] = buy_signals
    df['Sell'] = sell_signals
    return df

# === Ejecución ===
st.write(f"### Estrategia RSI - {symbol}")
data_load_state = st.empty()
data_load_state.text("🔄 Cargando datos en tiempo real...")

# === Loop en tiempo real ===
data = get_binance_data(symbol, timeframe, lookback)
data = calcular_rsi(data)
data = detectar_senales(data)
data_load_state.text("✅ Datos cargados")

# === Gráfico de precios ===
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['close'], mode='lines', name='Precio'))
fig.add_trace(go.Scatter(x=data.index, y=data['Buy'], mode='markers', name='COMPRA', marker=dict(color='green', size=10, symbol='triangle-up')))
fig.add_trace(go.Scatter(x=data.index, y=data['Sell'], mode='markers', name='VENTA', marker=dict(color='red', size=10, symbol='triangle-down')))
fig.update_layout(title=f'Precio {symbol}', xaxis_title='Fecha', yaxis_title='Precio', height=400)
st.plotly_chart(fig, use_container_width=True)

# === Gráfico RSI ===
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI', line=dict(color='orange')))
fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
fig_rsi.update_layout(title='Indicador RSI', xaxis_title='Fecha', yaxis_title='RSI', height=300)
st.plotly_chart(fig_rsi, use_container_width=True)

# === Auto-refresh ===
time.sleep(5)
st.experimental_rerun()
