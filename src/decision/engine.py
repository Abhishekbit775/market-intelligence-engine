"""
Layer 4 (Decision) — Buy / Sell / Hold engine.

Applies threshold logic: a directional trade is only emitted when the fused
confidence clears CONFIDENCE_THRESHOLD *and* a technical indicator confirms the
sentiment direction. Otherwise the engine returns HOLD. Produces the full
signal object (with risk plan + explanation) consumed by storage, API, and UI.
"""
from config import config
from src.decision.risk import build_risk_plan
from src.decision.explain import explain


def decide(*, ticker, company, headline, source, category, sentiment,
           news_score, technicals, fusion_out, capital=100_000):
    direction = fusion_out["direction"]
    confidence = fusion_out["confidence"]
    tech_score = technicals["tech_score"]

    # technical confirmation: indicator must align with sentiment direction
    confirmed = (
        (direction == "bullish" and tech_score > 0)
        or (direction == "bearish" and tech_score < 0)
    )

    if direction == "bullish" and confidence >= config.CONFIDENCE_THRESHOLD and confirmed:
        action = "BUY"
    elif direction == "bearish" and confidence >= config.CONFIDENCE_THRESHOLD and confirmed:
        action = "SELL"
    else:
        action = "HOLD"

    signal = {
        "ticker": ticker,
        "company": company,
        "headline": headline,
        "source": source,
        "category": category,
        "sentiment": sentiment,
        "news_score": news_score,
        "tech_score": tech_score,
        "technicals": technicals,
        "direction": direction,
        "confidence": confidence,
        "agreement": fusion_out["agreement"],
        "action": action,
        "threshold": config.CONFIDENCE_THRESHOLD,
        "risk_plan": None,
    }

    if action in ("BUY", "SELL"):
        signal["risk_plan"] = build_risk_plan(
            action, technicals["last_price"], technicals["atr"], confidence, capital
        )

    signal["explanation"] = explain(signal)
    return signal
