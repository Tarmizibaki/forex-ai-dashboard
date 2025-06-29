import pandas as pd

def identify_support_resistance(df, window=20):
    support, resistance = [], []
    for i in range(window, len(df) - window):
        low_range = df["Low"][i - window:i + window]
        high_range = df["High"][i - window:i + window]
        if df["Low"].iloc[i] == min(low_range):
            support.append((i, df["Low"].iloc[i]))
        if df["High"].iloc[i] == max(high_range):
            resistance.append((i, df["High"].iloc[i]))
    return support, resistance
