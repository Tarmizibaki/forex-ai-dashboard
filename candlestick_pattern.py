import pandas as pd

def detect_candlestick_patterns(df):
    patterns = []
    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        if prev["Close"] < prev["Open"] and curr["Close"] > curr["Open"]:
            if curr["Close"] > prev["Open"] and curr["Open"] < prev["Close"]:
                patterns.append((i, "Bullish Engulfing"))

        if prev["Close"] > prev["Open"] and curr["Close"] < curr["Open"]:
            if curr["Open"] > prev["Close"] and curr["Close"] < prev["Open"]:
                patterns.append((i, "Bearish Engulfing"))

        if abs(curr["Close"] - curr["Open"]) <= (curr["High"] - curr["Low"]) * 0.1:
            patterns.append((i, "Doji"))

        if curr["Close"] > curr["Open"]:
            body = abs(curr["Close"] - curr["Open"])
            lower_shadow = curr["Open"] - curr["Low"]
            upper_shadow = curr["High"] - curr["Close"]
            if lower_shadow > body * 2 and upper_shadow < body * 0.5:
                patterns.append((i, "Hammer"))

        if curr["Open"] > curr["Close"]:
            body = abs(curr["Open"] - curr["Close"])
            upper_shadow = curr["High"] - curr["Open"]
            lower_shadow = curr["Close"] - curr["Low"]
            if upper_shadow > body * 2 and lower_shadow < body * 0.5:
                patterns.append((i, "Shooting Star"))
    return patterns
