from dotenv import load_dotenv
load_dotenv()

import yfinance as yf
import pandas as pd
import hashlib
import numpy as np


def get_ohlcv(ticker, days=120):
    """
    Fetch real OHLCV data from NSE via yfinance.
    NSE tickers need .NS suffix (e.g. RELIANCE -> RELIANCE.NS)
    Falls back to synthetic data if ticker not found.
    """
    try:
        nse_ticker = ticker + ".NS"
        df = yf.download(
            nse_ticker,
            period="6mo",
            interval="1d",
            progress=False,
            auto_adjust=True
        )

        if df is None or df.empty:
            print(f"No data for {nse_ticker}, using synthetic")
            return _synthetic(ticker)

        # flatten multi-level columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0].lower() for col in df.columns]
        else:
            df.columns = [col.lower() for col in df.columns]

        # keep only what we need
        df = df[["open", "high", "low", "close", "volume"]].dropna()

        if len(df) < 30:
            return _synthetic(ticker)

        print(f"Real data loaded for {ticker}: latest close = {df['close'].iloc[-1]:.2f}")
        return df

    except Exception as e:
        print(f"yfinance error for {ticker}: {e}")
        return _synthetic(ticker)


def _synthetic(ticker):
    """Fallback synthetic data."""
    h = hashlib.md5(ticker.encode()).hexdigest()
    seed = int(h[:8], 16)
    rng = np.random.default_rng(seed)
    n = 120
    base = 500 + (seed % 2000)
    rets = rng.normal(0.0005, 0.018, n)
    close = base * np.cumprod(1 + rets)
    high = close * (1 + abs(rng.normal(0, 0.01, n)))
    low = close * (1 - abs(rng.normal(0, 0.01, n)))
    open_ = close * (1 + rng.normal(0, 0.005, n))
    volume = rng.integers(1_000_000, 8_000_000, n)
    idx = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=n, freq="B"
    )
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low,
         "close": close, "volume": volume},
        index=idx
    )