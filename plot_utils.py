import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_analysis(df, pair_name, support=[], resistance=[], waves=[], save_path=None):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Time"]) if "Time" in df.columns else pd.date_range(end=pd.Timestamp.today(), periods=len(df), freq="15min")

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot candlestick body
    for i in range(len(df)):
        color = 'green' if df["Close"].iloc[i] > df["Open"].iloc[i] else 'red'
        ax.plot([df["Date"].iloc[i], df["Date"].iloc[i]],
                [df["Open"].iloc[i], df["Close"].iloc[i]], color=color, linewidth=2)
        ax.vlines(df["Date"].iloc[i], df["Low"].iloc[i], df["High"].iloc[i], color=color, linewidth=1)

    # Moving Averages
    ax.plot(df["Date"], df["MA20"], label="MA20", linewidth=1.2)
    ax.plot(df["Date"], df["MA50"], label="MA50", linewidth=1.2)

    # Bollinger Bands
    if "BB_Upper" in df.columns and "BB_Lower" in df.columns:
        ax.plot(df["Date"], df["BB_Upper"], label="BB Upper", linestyle="--", linewidth=0.8)
        ax.plot(df["Date"], df["BB_Lower"], label="BB Lower", linestyle="--", linewidth=0.8)

    # Support & Resistance
    for idx, price in support[-2:]:
        ax.axhline(price, color="blue", linestyle="--", alpha=0.5, label="Support")
    for idx, price in resistance[-2:]:
        ax.axhline(price, color="orange", linestyle="--", alpha=0.5, label="Resistance")

    # Elliott Waves
    for idx, label in waves[-5:]:
        ax.text(df["Date"].iloc[idx], df["High"].iloc[idx], label, fontsize=9, color="purple")

    ax.set_title(f"Forex Analysis: {pair_name}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax.legend()
    fig.autofmt_xdate()

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()
