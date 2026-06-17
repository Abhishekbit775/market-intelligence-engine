"""
Central configuration for the Event-Driven Market Intelligence Engine.

All tunables live here so the rest of the codebase reads from one place.
Values can be overridden with environment variables (see .env.example).
"""
import os


def _f(name, default):
    return float(os.getenv(name, default))


def _i(name, default):
    return int(os.getenv(name, default))


class Config:
    # ---- Decision thresholds (from the proposal) ----
    CONFIDENCE_THRESHOLD = _f("CONFIDENCE_THRESHOLD", 0.65)   # min score to act
    SENTIMENT_REVERSAL_EXIT = _f("SENTIMENT_REVERSAL_EXIT", 0.70)

    # ---- Risk management ----
    ATR_STOP_MULT = _f("ATR_STOP_MULT", 1.5)     # stop-loss = 1.5 x ATR
    ATR_TARGET_MULT = _f("ATR_TARGET_MULT", 2.5)  # profit target = 2.5 x ATR
    TIME_EXIT_SESSIONS = _i("TIME_EXIT_SESSIONS", 3)
    RISK_PER_TRADE = _f("RISK_PER_TRADE", 0.02)   # 2% of capital
    HIGH_CONF_RISK_MULT = _f("HIGH_CONF_RISK_MULT", 1.5)
    HIGH_CONF_LEVEL = _f("HIGH_CONF_LEVEL", 0.80)

    # ---- Impact scoring weights (must sum ~1.0) ----
    W_SENTIMENT = _f("W_SENTIMENT", 0.40)
    W_SOURCE = _f("W_SOURCE", 0.15)
    W_CATEGORY = _f("W_CATEGORY", 0.20)
    W_PRICE_SENS = _f("W_PRICE_SENS", 0.15)
    W_RECENCY = _f("W_RECENCY", 0.10)

    # ---- Signal fusion weight (news vs technical) ----
    NEWS_WEIGHT = _f("NEWS_WEIGHT", 0.6)
    TECH_WEIGHT = _f("TECH_WEIGHT", 0.4)

    # ---- Source credibility (0-1) ----
    SOURCE_WEIGHTS = {
        "Reuters": 1.0, "Bloomberg": 1.0, "NSE": 0.95, "BSE": 0.95,
        "RBI": 1.0, "Economic Times": 0.8, "Moneycontrol": 0.75,
        "Twitter": 0.4, "Reddit": 0.3, "Unknown": 0.5,
    }

    # ---- Event-category weights ----
    CATEGORY_WEIGHTS = {
        "earnings": 1.0, "regulatory": 0.9, "macro": 0.85,
        "mna": 0.95, "general": 0.5,
    }

    # ---- Infra ----
    DB_URL = os.getenv("DB_URL", "sqlite:///signals.db")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
    ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY", "")
    USE_FINBERT = os.getenv("USE_FINBERT", "auto")   # auto | on | off


config = Config()
