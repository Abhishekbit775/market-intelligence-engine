"""
Layer 3 (Signal) — Multi-source fusion + confidence calibration.

Blends the news impact score with the technical score into a single directional
view, then maps the agreement strength to a calibrated confidence in [0, 1]
via a logistic (a lightweight stand-in for Platt scaling; replace the slope/
intercept with values fitted on backtest data for production calibration).
"""
import math
from config import config


def _logistic(x, slope=4.0, intercept=0.0):
    return 1 / (1 + math.exp(-(slope * x + intercept)))


def fuse(news_score, tech_score):
    """
    Returns dict:
      direction: 'bullish' | 'bearish' | 'neutral'
      fused_score: signed -1..1
      confidence: 0..1 (calibrated)
      agreement: True if news and technical point the same way
    """
    fused = config.NEWS_WEIGHT * news_score + config.TECH_WEIGHT * tech_score
    agreement = (news_score > 0 and tech_score > 0) or (news_score < 0 and tech_score < 0)

    # confidence grows with |fused|, with a bonus when both sources agree
    base_conf = _logistic(abs(fused))
    confidence = min(base_conf * (1.10 if agreement else 0.90), 0.99)

    if fused > 0.05:
        direction = "bullish"
    elif fused < -0.05:
        direction = "bearish"
    else:
        direction = "neutral"

    return {
        "direction": direction,
        "fused_score": round(fused, 4),
        "confidence": round(confidence, 4),
        "agreement": agreement,
    }
