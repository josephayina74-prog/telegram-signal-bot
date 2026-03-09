import requests
import time

# 🔐 Mets ici tes informations
TOKEN = "8554042171:AAE401PBi0UtEb5hlsrlIpTRd6-yM_fTSqY"
CHAT_ID = "-1003703675419"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

def signal_logic():
    # ⚡ Version simple et sécurisée (exemple)
    # Ici on envoie un signal test toutes les heures
    send_message("📊 Bot actif. Analyse en cours...")

while True:
    signal_logic()
    time.sleep(300)  # 300 secondes = 5 minutes 
