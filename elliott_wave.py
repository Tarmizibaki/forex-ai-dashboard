import pandas as pd

def detect_swing_points(df, lookback=5):
    swings = []
    for i in range(lookback, len(df) - lookback):
        if df["High"].iloc[i] == max(df["High"].iloc[i - lookback:i + lookback + 1]):
            swings.append((i, "Swing High"))
        elif df["Low"].iloc[i] == min(df["Low"].iloc[i - lookback:i + lookback + 1]):
            swings.append((i, "Swing Low"))
    return swings

def label_elliott_wave(swings):
    wave_labels = []
    wave_count, mode = 1, "impulse"
    for idx, _ in swings:
        if wave_count <= 5 and mode == "impulse":
            wave_labels.append((idx, f"Wave {wave_count}"))
            wave_count += 1
            if wave_count > 5:
                wave_count = 1
                mode = "correction"
        elif mode == "correction":
            wave_labels.append((idx, f"Wave {chr(64 + wave_count)}"))
            wave_count += 1
            if wave_count > 3:
                break
    return wave_labels
