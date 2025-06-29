
import streamlit as st
import pandas as pd
from ta.momentum import RSIIndicator
from plot_utils import plot_analysis
from support_resistance import identify_support_resistance
from candlestick_pattern import detect_candlestick_patterns
from chart_pattern import detect_double_top_bottom
from elliott_wave import detect_swing_points, label_elliott_wave

st.set_page_config(layout="wide")
st.title("📊 Forex AI Signal Dashboard")
st.markdown("Upload your MT4-exported CSV file for EUR/USD or XAU/USD")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    pair_name = st.text_input("Pair Name (e.g. EUR/USD)", "EUR/USD")

    # Calculate indicators
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["BB_Mid"] = df["MA20"]
    df["BB_Std"] = df["Close"].rolling(window=20).std()
    df["BB_Upper"] = df["BB_Mid"] + 2 * df["BB_Std"]
    df["BB_Lower"] = df["BB_Mid"] - 2 * df["BB_Std"]
    df["RSI"] = RSIIndicator(close=df["Close"], window=14).rsi()

    # Advanced analysis
    support, resistance = identify_support_resistance(df)
    candle_patterns = detect_candlestick_patterns(df)
    chart_patterns = detect_double_top_bottom(df)
    swings = detect_swing_points(df)
    wave_labels = label_elliott_wave(swings)

    st.subheader("📈 Forex Chart")
    plot_analysis(df, pair_name, support, resistance, wave_labels)

    st.subheader("📌 Technical Signals")
    latest = df.iloc[-1]
    signal = "No clear signal"
    if latest["Close"] > latest["BB_Mid"] and latest["MA20"] > latest["MA50"] and latest["RSI"] < 70:
        signal = f"**BUY Signal** for {pair_name}"
    elif latest["Close"] < latest["BB_Mid"] and latest["MA20"] < latest["MA50"] and latest["RSI"] > 30:
        signal = f"**SELL Signal** for {pair_name}"
    st.markdown(signal)

    st.subheader("🔍 Pattern Summary")
    st.markdown(f"**Recent Candlestick Patterns**: {[p[1] for p in candle_patterns[-3:]]}")
    st.markdown(f"**Chart Patterns Detected**: {[p[1] for p in chart_patterns[-3:]]}")
    st.markdown(f"**Elliott Wave Labels**: {[w[1] for w in wave_labels[-5:]]}")
