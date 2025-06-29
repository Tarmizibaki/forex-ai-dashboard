import pandas as pd
import requests

TELEGRAM_TOKEN = "7710942397:AAFKPlFnQ25xUotUk5iS2Phfk1sGr9Mh0Ck"
CHAT_ID = "591316747"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def analyze_pair(filename, pair_name):
    df = pd.read_csv(filename)
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["BB_Mid"] = df["MA20"]
    df["BB_Std"] = df["Close"].rolling(window=20).std()
    df["BB_Upper"] = df["BB_Mid"] + 2 * df["BB_Std"]
    df["BB_Lower"] = df["BB_Mid"] - 2 * df["BB_Std"]

    # RSI
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    latest = df.iloc[-1]
    signal = "No Signal"

    if latest["Close"] > latest["BB_Mid"] and latest["MA20"] > latest["MA50"] and latest["RSI"] < 70:
        signal = "BUY Signal for " + pair_name
    elif latest["Close"] < latest["BB_Mid"] and latest["MA20"] < latest["MA50"] and latest["RSI"] > 30:
        signal = "SELL Signal for " + pair_name

    send_telegram_message(signal)
    print(signal)

if __name__ == "__main__":
    print("Analyzing EUR/USD...")
    analyze_pair("EURUSD_M15.csv", "EUR/USD")
    print("\nAnalyzing XAU/USD...")
    analyze_pair("XAUUSD_M15.csv", "XAU/USD")
