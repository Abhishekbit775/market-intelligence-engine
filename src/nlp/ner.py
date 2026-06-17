"""
Layer 2 (NLP) — Named Entity Recognition + event categorisation.

Uses spaCy (en_core_web_sm) to pull ORG/GPE entities when available; in all
cases it resolves references to NSE/BSE tickers via the knowledge graph, so
mapping works even without spaCy installed. Also classifies each news item
into an event category used by the impact scorer.
"""
import re
from src.knowledge_graph import resolve_entities, TICKER_META

_NLP = None
_TRIED = False


def _try_load_spacy():
    global _NLP, _TRIED
    if _TRIED:
        return _NLP
    _TRIED = True
    try:
        import spacy
        _NLP = spacy.load("en_core_web_sm")
    except Exception:
        _NLP = None
    return _NLP


_CATEGORY_PATTERNS = {
    "earnings": r"\b(earnings|results|q[1-4]|profit|revenue|net income|guidance|eps)\b",
    "regulatory": r"\b(sebi|rbi|regulator|probe|penalty|fine|approval|ban|compliance|filing)\b",
    "macro": r"\b(inflation|gdp|repo rate|interest rate|fed|cpi|fiscal|monetary|crude|rupee)\b",
    "mna": r"\b(acquire|acquisition|merger|merges|stake|takeover|buyout|deal)\b",
}


def categorize(text):
    t = text.lower()
    for cat, pat in _CATEGORY_PATTERNS.items():
        if re.search(pat, t):
            return cat
    return "general"


def extract_entities(text):
    """
    Return dict with:
      tickers: [{ticker, name, sector, price_sensitivity}, ...]
      category: event category
      raw_orgs: organisations spaCy detected (informational)
    """
    raw_orgs = []
    nlp = _try_load_spacy()
    if nlp is not None:
        try:
            doc = nlp(text)
            raw_orgs = [e.text for e in doc.ents if e.label_ in ("ORG", "GPE")]
        except Exception:
            raw_orgs = []

    tickers = []
    for tk in resolve_entities(text):
        meta = TICKER_META.get(tk, {})
        tickers.append({
            "ticker": tk,
            "name": meta.get("name", tk),
            "sector": meta.get("sector", "Unknown"),
            "price_sensitivity": meta.get("price_sensitivity", 0.6),
        })

    return {"tickers": tickers, "category": categorize(text), "raw_orgs": raw_orgs}
