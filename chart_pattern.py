import pandas as pd

def detect_double_top_bottom(df, distance=10, threshold=0.003):
    patterns = []
    for i in range(distance, len(df) - distance):
        lp, mp, rp = df["High"].iloc[i - distance], df["Low"].iloc[i], df["High"].iloc[i + distance]
        if abs(lp - rp) / lp < threshold and mp < lp:
            patterns.append((i, "Double Top"))

        lv, mv, rv = df["Low"].iloc[i - distance], df["High"].iloc[i], df["Low"].iloc[i + distance]
        if abs(lv - rv) / lv < threshold and mv > lv:
            patterns.append((i, "Double Bottom"))
    return patterns
