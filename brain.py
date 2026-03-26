import pandas as pd
import numpy as np

# =========================
# UTILIDADES
# =========================

def get_trend(df):
    h1 = df['close'].iloc[-1]
    h2 = df['close'].iloc[-5]

    if h1 > h2:
        return "BULL"
    elif h1 < h2:
        return "BEAR"
    return "RANGE"

def detect_liquidity(df):
    high = df['high'].rolling(20).max()
    low = df['low'].rolling(20).min()
    return high.iloc[-1], low.iloc[-1]

def detect_sweep(price, high, low):
    if price < low:
        return "BUY"
    elif price > high:
        return "SELL"
    return None

def detect_mss(df, direction):
    closes = df['close']

    if direction == "BUY":
        return closes.iloc[-1] > closes.iloc[-2] > closes.iloc[-3]

    if direction == "SELL":
        return closes.iloc[-1] < closes.iloc[-2] < closes.iloc[-3]

    return False

def strong_candle(df):
    open_ = df['open'].iloc[-1]
    close_ = df['close'].iloc[-1]

    return abs(close_ - open_) > (df['high'].iloc[-1] - df['low'].iloc[-1]) * 0.6

def is_volatile(df):
    rng = df['high'].iloc[-1] - df['low'].iloc[-1]
    return rng > df['close'].mean() * 0.001

def pullback_ok(df, direction):
    if direction == "BUY":
        return df['close'].iloc[-2] < df['close'].iloc[-1]
    else:
        return df['close'].iloc[-2] > df['close'].iloc[-1]

# =========================
# SCORE INTELIGENTE
# =========================

def calculate_score(trend, sweep, mss, candle, vol, pullback):
    score = 0

    if trend != "RANGE":
        score += 20

    if sweep:
        score += 25

    if mss:
        score += 20

    if candle:
        score += 15

    if vol:
        score += 10

    if pullback:
        score += 10

    return score

# =========================
# FUNÇÃO PRINCIPAL
# =========================

def generate_signal(df_m5, df_h1):
    price = df_m5['close'].iloc[-1]

    # 🔹 Tendência macro
    trend = get_trend(df_h1)

    # 🔹 Liquidez
    high, low = detect_liquidity(df_m5)

    # 🔹 Sweep
    sweep = detect_sweep(price, high, low)
    if not sweep:
        return None

    # 🔹 MSS
    mss = detect_mss(df_m5, sweep)
    if not mss:
        return None

    # 🔹 Filtros
    candle = strong_candle(df_m5)
    vol = is_volatile(df_m5)
    pullback = pullback_ok(df_m5, sweep)

    # 🔹 Score
    score = calculate_score(trend, sweep, mss, candle, vol, pullback)

    # 🔥 só entra se for forte
    if score < 70:
        return None

    # 🔹 Stop / TP
    stop = low if sweep == "BUY" else high
    entry = price
    rr = 3

    tp = entry + (entry - stop) * rr if sweep == "BUY" else entry - (stop - entry) * rr

    return {
        "type": sweep,
        "entry": float(entry),
        "stop": float(stop),
        "tp": float(tp),
        "confidence": int(score),
        "trend": trend
      }
