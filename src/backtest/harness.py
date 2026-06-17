"""
Layer 5 — Backtesting harness.

A lightweight, walk-forward-style backtester that replays the pipeline's
signals against forward price moves and computes the proposal's headline
metrics: win rate, profit factor, Sharpe, max drawdown, avg holding period.

This is a demonstration harness on synthetic/historical OHLCV — wire it to
real archived news + prices (2019-2024) for the validated report. Costs and
slippage are modelled per the proposal (0.05% one-way).
"""
import numpy as np
import pandas as pd
from config import config
from src.ingestion.market_data import get_ohlcv


COST_ONE_WAY = 0.0005  # 0.05%


def _simulate_trade(df, entry_idx, action, atr, entry_price):
    """Walk forward up to TIME_EXIT_SESSIONS; return realised return (after costs)."""
    stop_dist = config.ATR_STOP_MULT * atr
    target_dist = config.ATR_TARGET_MULT * atr
    horizon = min(entry_idx + config.TIME_EXIT_SESSIONS, len(df) - 1)

    for i in range(entry_idx + 1, horizon + 1):
        hi, lo = df["high"].iloc[i], df["low"].iloc[i]
        if action == "BUY":
            if lo <= entry_price - stop_dist:
                ret = -stop_dist / entry_price
                return ret - 2 * COST_ONE_WAY, i - entry_idx
            if hi >= entry_price + target_dist:
                ret = target_dist / entry_price
                return ret - 2 * COST_ONE_WAY, i - entry_idx
        else:  # SELL / short
            if hi >= entry_price + stop_dist:
                ret = -stop_dist / entry_price
                return ret - 2 * COST_ONE_WAY, i - entry_idx
            if lo <= entry_price - target_dist:
                ret = target_dist / entry_price
                return ret - 2 * COST_ONE_WAY, i - entry_idx

    # time exit at close
    exit_price = df["close"].iloc[horizon]
    raw = (exit_price - entry_price) / entry_price
    ret = raw if action == "BUY" else -raw
    return ret - 2 * COST_ONE_WAY, horizon - entry_idx


def backtest(tickers=None, trades_per_ticker=20, seed=7):
    """
    Generates synthetic signal entries across tickers and evaluates them.
    Replace the entry generation with your real signal log for a true backtest.
    """
    from src.knowledge_graph import TICKER_META
    from src.signals.indicators import atr as atr_fn

    tickers = tickers or list(TICKER_META.keys())
    rng = np.random.default_rng(seed)
    returns, holds = [], []

    for tk in tickers:
        df = get_ohlcv(tk, days=200).reset_index(drop=True)
        idxs = rng.integers(30, len(df) - config.TIME_EXIT_SESSIONS - 1,
                            size=trades_per_ticker)
        for ei in idxs:
            window = df.iloc[: ei + 1]
            a = atr_fn(window["high"], window["low"], window["close"])
            if np.isnan(a) or a <= 0:
                continue
            entry_price = df["close"].iloc[ei]
            action = "BUY" if rng.random() > 0.45 else "SELL"
            r, h = _simulate_trade(df, ei, action, a, entry_price)
            returns.append(r)
            holds.append(h)

    return _metrics(np.array(returns), np.array(holds))


def _metrics(returns, holds):
    if len(returns) == 0:
        return {"error": "no trades"}
    wins = returns[returns > 0]
    losses = returns[returns < 0]
    win_rate = len(wins) / len(returns)
    profit_factor = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else float("inf")
    sharpe = (returns.mean() / (returns.std() + 1e-9)) * np.sqrt(252 / max(holds.mean(), 1))
    equity = np.cumprod(1 + returns)
    peak = np.maximum.accumulate(equity)
    max_dd = ((equity - peak) / peak).min()

    return {
        "trades": int(len(returns)),
        "win_rate": round(win_rate, 4),
        "profit_factor": round(float(profit_factor), 3),
        "sharpe_annualised": round(float(sharpe), 3),
        "max_drawdown": round(float(max_dd), 4),
        "avg_holding_sessions": round(float(holds.mean()), 2),
        "mean_return_per_trade": round(float(returns.mean()), 5),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(backtest(), indent=2))
