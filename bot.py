import requests
import time
import pandas as pd
import yfinance as yf

TOKEN = "8554042171:AAE401PBi0UtEb5hlsrlIpTRd6-yM_fTSqY"
CHAT_ID = "-1003703675419"

def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def get_data():
    df = yf.download(tickers="EURUSD=X", period="1d", interval="1m")
    df = df[['Open','High','Low','Close']]
    return df

def calculate_indicators(df):
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['EMA100'] = df['Close'].ewm(span=100, adjust=False).mean()

    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df

def analyse_signal(df):
    ema50 = df['EMA50'].values[-1]
    ema100 = df['EMA100'].values[-1]
    rsi = df['RSI'].values[-1]
    price = df['Close'].values[-1]

    if ema50 > ema100 and rsi < 40:
        return f"""EUR/USD

📊 SIGNAL
Prix : {price}
Direction : CALL ⬆
Durée : 1 minute"""

    elif ema50 < ema100 and rsi > 60:
        return f"""EUR/USD

📊 SIGNAL
Prix : {price}
Direction : PUT ⬇
Durée : 1 minute"""

    else:
        return "EUR/USD\n\n📊 Pas de signal pour le moment"

while True:
    try:
        data = get_data()
        data = calculate_indicators(data)
        message = analyse_signal(data)
        send_message(message)

    except Exception as e:
        send_message(f"Erreur : {e}")

    time.sleep(300)
