"""
Layer 3 (Signal) — Technical indicators.

Pure-pandas implementations of RSI, MACD, Bollinger Bands and ATR so there is
no dependency on TA-Lib (which is painful to install). Each returns the latest
value plus a directional read used by the fusion module.
"""
import numpy as np
import pandas as pd


def rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).iloc[-1]


def macd(close, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    line = ema_fast - ema_slow
    sig = line.ewm(span=signal, adjust=False).mean()
    return line.iloc[-1], sig.iloc[-1]


def bollinger(close, period=20, n_std=2):
    ma = close.rolling(period).mean()
    sd = close.rolling(period).std()
    upper = ma + n_std * sd
    lower = ma - n_std * sd
    return upper.iloc[-1], ma.iloc[-1], lower.iloc[-1]


def atr(high, low, close, period=14):
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean().iloc[-1]


def technical_signal(df):
    """
    df: DataFrame with columns [open, high, low, close, volume].
    Returns dict with indicator values, an ATR, and a tech_score in [-1, 1]
    (positive = bullish, negative = bearish).
    """
    close = df["close"]
    _rsi = rsi(close)
    macd_line, macd_sig = macd(close)
    up, mid, low_b = bollinger(close)
    _atr = atr(df["high"], df["low"], close)
    last = close.iloc[-1]

    votes = []
    # RSI: oversold bullish, overbought bearish
    if not np.isnan(_rsi):
        if _rsi < 30:
            votes.append(1)
        elif _rsi > 70:
            votes.append(-1)
        else:
            votes.append((50 - _rsi) / 50 * 0.5)
    # MACD cross
    votes.append(1 if macd_line > macd_sig else -1)
    # Bollinger position
    if last <= low_b:
        votes.append(1)
    elif last >= up:
        votes.append(-1)
    else:
        votes.append((mid - last) / (up - mid) if up != mid else 0)
    # Volume anomaly confirmation (magnitude only)
    vol_z = (df["volume"].iloc[-1] - df["volume"].mean()) / (df["volume"].std() + 1e-9)

    tech_score = float(np.clip(np.mean(votes), -1, 1))
    return {
        "rsi": round(float(_rsi), 2) if not np.isnan(_rsi) else None,
        "macd": round(float(macd_line), 4),
        "macd_signal": round(float(macd_sig), 4),
        "bollinger": {"upper": round(float(up), 2), "lower": round(float(low_b), 2)},
        "atr": round(float(_atr), 4),
        "volume_z": round(float(vol_z), 2),
        "tech_score": round(tech_score, 4),
        "last_price": round(float(last), 2),
    }
