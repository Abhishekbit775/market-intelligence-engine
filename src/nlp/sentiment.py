"""
Layer 2 (NLP) — Sentiment analysis.

Tries to load FinBERT (ProsusAI/finbert) for true financial sentiment.
If transformers/torch or the model weights are unavailable (e.g. offline),
it falls back to a transparent financial-lexicon scorer so the whole
pipeline still runs end-to-end. The fallback is clearly labelled in output.
"""
from config import config

_FINBERT = None
_BACKEND = None


def _try_load_finbert():
    """Lazy-load FinBERT once. Returns a HF pipeline or None."""
    global _FINBERT, _BACKEND
    if _BACKEND is not None:
        return _FINBERT
    if config.USE_FINBERT == "off":
        _BACKEND = "lexicon"
        return None
    try:
        from transformers import pipeline
        _FINBERT = pipeline(
            "sentiment-analysis",
            model="ProsusAI/finbert",
            tokenizer="ProsusAI/finbert",
            truncation=True,
        )
        _BACKEND = "finbert"
    except Exception:
        _FINBERT = None
        _BACKEND = "lexicon"
    return _FINBERT


# --- transparent lexicon used when FinBERT is unavailable ---
_POS = {
    "beat", "beats", "surge", "surges", "soar", "rally", "gains", "profit",
    "upgrade", "outperform", "record", "strong", "growth", "rises", "jump",
    "bullish", "approval", "expansion", "wins", "boost", "robust", "tops",
    "buyback", "dividend", "raised", "exceeds", "optimistic",
}
_NEG = {
    "miss", "misses", "plunge", "plunges", "fall", "falls", "loss", "losses",
    "downgrade", "underperform", "weak", "decline", "drops", "slump",
    "bearish", "probe", "fraud", "penalty", "fine", "ban", "lawsuit", "cut",
    "warns", "slashed", "disappoints", "default", "crash", "selloff",
}


def _lexicon_score(text):
    words = text.lower().split()
    pos = sum(1 for w in words if w.strip(".,!?:;") in _POS)
    neg = sum(1 for w in words if w.strip(".,!?:;") in _NEG)
    total = pos + neg
    if total == 0:
        return "Neutral", 0.50
    if pos > neg:
        return "Positive", min(0.55 + 0.12 * (pos - neg), 0.95)
    if neg > pos:
        return "Negative", min(0.55 + 0.12 * (neg - pos), 0.95)
    return "Neutral", 0.55


_LABEL_MAP = {"positive": "Positive", "negative": "Negative", "neutral": "Neutral"}


def analyze_sentiment(text):
    """
    Return dict: {label: Positive|Negative|Neutral, score: 0-1, backend: str}
    'score' is the model's probability for the chosen label.
    """
    pipe = _try_load_finbert()
    if pipe is not None:
        try:
            r = pipe(text[:512])[0]
            return {
                "label": _LABEL_MAP.get(r["label"].lower(), "Neutral"),
                "score": round(float(r["score"]), 4),
                "backend": "finbert",
            }
        except Exception:
            pass
    label, score = _lexicon_score(text)
    return {"label": label, "score": round(score, 4), "backend": "lexicon"}


def backend_name():
    _try_load_finbert()
    return _BACKEND or "lexicon"
