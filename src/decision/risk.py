"""
Layer 4 (Decision) — Risk management.

Implements the proposal's risk rules:
  stop-loss   = 1.5 x ATR from entry
  profit tgt  = 2.5 x ATR from entry  (>= 1:1.5 reward-risk)
  position    = risk 1-2% of capital, scaled 1.5x for high-confidence signals
  time exit   = close after N sessions
  reversal    = exit if opposing sentiment > 0.70
"""
from config import config


def build_risk_plan(action, entry_price, atr, confidence, capital):
    """
    action: 'BUY' or 'SELL'. Returns a full risk prescription dict.
    For SELL (short), stop is above entry and target below.
    """
    stop_dist = config.ATR_STOP_MULT * atr
    target_dist = config.ATR_TARGET_MULT * atr

    if action == "BUY":
        stop_loss = entry_price - stop_dist
        profit_target = entry_price + target_dist
    else:  # SELL / short
        stop_loss = entry_price + stop_dist
        profit_target = entry_price - target_dist

    # position sizing off risk-per-trade
    risk_pct = config.RISK_PER_TRADE
    if confidence >= config.HIGH_CONF_LEVEL:
        risk_pct *= config.HIGH_CONF_RISK_MULT
    risk_amount = capital * risk_pct
    per_share_risk = abs(entry_price - stop_loss)
    qty = int(risk_amount / per_share_risk) if per_share_risk > 0 else 0

    rr = round(target_dist / stop_dist, 2) if stop_dist > 0 else None

    return {
        "entry_price": round(entry_price, 2),
        "stop_loss": round(stop_loss, 2),
        "profit_target": round(profit_target, 2),
        "risk_reward": rr,
        "position_qty": qty,
        "capital_at_risk": round(risk_amount, 2),
        "risk_pct_of_capital": round(risk_pct * 100, 2),
        "time_exit_sessions": config.TIME_EXIT_SESSIONS,
        "reversal_exit_threshold": config.SENTIMENT_REVERSAL_EXIT,
        "atr": round(atr, 4),
    }
