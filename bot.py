import requests
import time
import pandas as pd
import numpy as np
import yfinance as yf  # pour récupérer les prix

TOKEN = "8554042171:AAE401PBi0UtEb5hlsrlIpTRd6-yM_fTSqY"
CHAT_ID = "-1003703675419"

def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def get_data():
    # Récupère les dernières 100 minutes d'EUR/USD
    df = yf.download(tickers="EURUSD=X", period="1d", interval="1m")
    df = df[['Close']]
    return df

def calculate_indicators(df):
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['EMA100'] = df['Close'].ewm(span=100, adjust=False).mean()
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -1*delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def analyse_signal(df):
    last = df.iloc[-1]
    if last['EMA50'] > last['EMA100'] and last['RSI'] < 35:
        return "📊 SIGNAL EUR/USD\nDirection : CALL ⬆\nDurée : 1 minute"
    elif last['EMA50'] < last['EMA100'] and last['RSI'] > 65:
        return "📊 SIGNAL EUR/USD\nDirection : PUT ⬇\nDurée : 1 minute"
    else:
        return "📊 Pas de signal pour le moment"

while True:
    try:
        data = get_data()
        data = calculate_indicators(data)
        message = analyse_signal(data)
        send_message(message)
    except Exception as e:
        send_message(f"Erreur : {e}")
    time.sleep(300)  # toutes les 5 minutes pour test
