"""
Layer 3 (Signal) — Event impact scorer.

Combines five factors into one news-impact score in [-1, 1]:
  sentiment polarity strength, source credibility, event category weight,
  entity price-sensitivity, and a recency decay factor.
The sign comes from sentiment direction; the magnitude from the weighted mix.
"""
import math
from datetime import datetime, timezone
from config import config


def _recency_factor(published_iso, half_life_hours=12):
    """1.0 for brand-new news, decaying exponentially with age."""
    try:
        pub = datetime.fromisoformat(published_iso.replace("Z", "+00:00"))
    except Exception:
        return 0.7
    age_h = (datetime.now(timezone.utc) - pub).total_seconds() / 3600
    age_h = max(age_h, 0)
    return math.exp(-math.log(2) * age_h / half_life_hours)


def impact_score(sentiment, source, category, price_sensitivity, published_iso):
    """
    sentiment: dict {label, score}
    Returns dict with the composite news_score (signed, -1..1) and components.
    """
    polarity = {"Positive": 1, "Negative": -1, "Neutral": 0}[sentiment["label"]]
    strength = sentiment["score"]                       # 0-1
    src_w = config.SOURCE_WEIGHTS.get(source, config.SOURCE_WEIGHTS["Unknown"])
    cat_w = config.CATEGORY_WEIGHTS.get(category, config.CATEGORY_WEIGHTS["general"])
    rec = _recency_factor(published_iso)

    magnitude = (
        config.W_SENTIMENT * strength
        + config.W_SOURCE * src_w
        + config.W_CATEGORY * cat_w
        + config.W_PRICE_SENS * price_sensitivity
        + config.W_RECENCY * rec
    )
    news_score = polarity * magnitude   # signed, ~ -1..1

    return {
        "news_score": round(news_score, 4),
        "magnitude": round(magnitude, 4),
        "components": {
            "polarity": polarity,
            "sentiment_strength": round(strength, 4),
            "source_weight": src_w,
            "category_weight": cat_w,
            "price_sensitivity": price_sensitivity,
            "recency": round(rec, 4),
        },
    }
