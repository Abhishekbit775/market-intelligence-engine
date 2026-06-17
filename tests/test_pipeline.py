"""Unit tests — run with: pytest -q"""
import pandas as pd
import numpy as np

from src.knowledge_graph import resolve_entities
from src.nlp.sentiment import analyze_sentiment
from src.nlp.ner import categorize, extract_entities
from src.nlp.dedup import deduplicate
from src.signals.indicators import technical_signal
from src.signals.impact_scorer import impact_score
from src.signals.fusion import fuse
from src.decision.risk import build_risk_plan
from src.pipeline import run_pipeline


def _fake_df():
    n = 60
    close = pd.Series(np.linspace(100, 120, n))
    return pd.DataFrame({
        "open": close, "high": close * 1.01, "low": close * 0.99,
        "close": close, "volume": pd.Series(np.full(n, 1e6)),
    })


def test_entity_resolution():
    assert "RELIANCE" in resolve_entities("Reliance Industries posts profit")
    assert "TCS" in resolve_entities("TCS wins a deal")


def test_sentiment_returns_valid_label():
    r = analyze_sentiment("profit surges, strong growth and record gains")
    assert r["label"] in ("Positive", "Negative", "Neutral")
    assert 0 <= r["score"] <= 1


def test_categorize():
    assert categorize("Q3 earnings and revenue beat") == "earnings"
    assert categorize("SEBI launches probe") == "regulatory"


def test_dedup_removes_reprints():
    arts = [{"headline": "Reliance beats Q3 profit estimates"},
            {"headline": "Reliance beats Q3 profit estimates today"}]
    assert len(deduplicate(arts)) == 1


def test_technical_signal_keys():
    t = technical_signal(_fake_df())
    for k in ("rsi", "macd", "atr", "tech_score", "last_price"):
        assert k in t


def test_impact_score_sign():
    pos = impact_score({"label": "Positive", "score": 0.9}, "Reuters",
                       "earnings", 0.8, "2026-06-09T08:00:00Z")
    assert pos["news_score"] > 0


def test_fusion_confidence_range():
    f = fuse(0.8, 0.5)
    assert 0 <= f["confidence"] <= 1
    assert f["direction"] == "bullish"


def test_risk_plan_reward_risk():
    rp = build_risk_plan("BUY", 100, atr=2.0, confidence=0.7, capital=100000)
    assert rp["stop_loss"] < 100 < rp["profit_target"]
    assert rp["risk_reward"] == 1.67


def test_pipeline_runs():
    sigs = run_pipeline(persist=False, limit=10)
    assert isinstance(sigs, list) and len(sigs) > 0
    assert all("explanation" in s for s in sigs)
