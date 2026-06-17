"""
Knowledge graph: maps free-text company/sector references to NSE/BSE tickers.

In production this would be a graph DB; here it is a curated dictionary that
is fast, transparent, and easy to extend. Each ticker also carries a
'price_sensitivity' (0-1) used by the impact scorer — how much this name
historically reacts to news.
"""

# entity alias (lowercased)  ->  canonical ticker
ALIAS_TO_TICKER = {
    "reliance": "RELIANCE", "reliance industries": "RELIANCE", "ril": "RELIANCE",
    "tcs": "TCS", "tata consultancy": "TCS", "tata consultancy services": "TCS",
    "infosys": "INFY", "infy": "INFY",
    "hdfc bank": "HDFCBANK", "hdfc": "HDFCBANK",
    "icici": "ICICIBANK", "icici bank": "ICICIBANK",
    "sbi": "SBIN", "state bank": "SBIN", "state bank of india": "SBIN",
    "wipro": "WIPRO",
    "adani": "ADANIENT", "adani enterprises": "ADANIENT",
    "tata motors": "TATAMOTORS",
    "bharti airtel": "BHARTIARTL", "airtel": "BHARTIARTL",
    "maruti": "MARUTI", "maruti suzuki": "MARUTI",
    "itc": "ITC",
    "larsen": "LT", "l&t": "LT", "larsen & toubro": "LT",
    "asian paints": "ASIANPAINT",
    "bajaj finance": "BAJFINANCE",
}

TICKER_META = {
    "RELIANCE":   {"name": "Reliance Industries", "sector": "Energy",     "price_sensitivity": 0.8},
    "TCS":        {"name": "Tata Consultancy",     "sector": "IT",         "price_sensitivity": 0.7},
    "INFY":       {"name": "Infosys",              "sector": "IT",         "price_sensitivity": 0.75},
    "HDFCBANK":   {"name": "HDFC Bank",            "sector": "Banking",    "price_sensitivity": 0.7},
    "ICICIBANK":  {"name": "ICICI Bank",           "sector": "Banking",    "price_sensitivity": 0.7},
    "SBIN":       {"name": "State Bank of India",  "sector": "Banking",    "price_sensitivity": 0.75},
    "WIPRO":      {"name": "Wipro",                "sector": "IT",         "price_sensitivity": 0.65},
    "ADANIENT":   {"name": "Adani Enterprises",    "sector": "Conglomerate","price_sensitivity": 0.95},
    "TATAMOTORS": {"name": "Tata Motors",          "sector": "Auto",       "price_sensitivity": 0.85},
    "BHARTIARTL": {"name": "Bharti Airtel",        "sector": "Telecom",    "price_sensitivity": 0.7},
    "MARUTI":     {"name": "Maruti Suzuki",        "sector": "Auto",       "price_sensitivity": 0.7},
    "ITC":        {"name": "ITC",                  "sector": "FMCG",       "price_sensitivity": 0.6},
    "LT":         {"name": "Larsen & Toubro",      "sector": "Infra",      "price_sensitivity": 0.7},
    "ASIANPAINT": {"name": "Asian Paints",         "sector": "Materials",  "price_sensitivity": 0.6},
    "BAJFINANCE": {"name": "Bajaj Finance",        "sector": "NBFC",       "price_sensitivity": 0.85},
}

# sector-level keywords -> all tickers in that sector
SECTOR_KEYWORDS = {
    "it sector": "IT", "software": "IT", "tech stocks": "IT",
    "banking sector": "Banking", "banks": "Banking", "psu banks": "Banking",
    "auto sector": "Auto", "automobile": "Auto",
}


def resolve_entities(text):
    """Return a list of tickers referenced in the text (longest alias wins)."""
    t = text.lower()
    hits = set()

    # direct company aliases (check longer aliases first to avoid partial dupes)
    for alias in sorted(ALIAS_TO_TICKER, key=len, reverse=True):
        if alias in t:
            hits.add(ALIAS_TO_TICKER[alias])

    # sector references expand to every ticker in that sector
    for kw, sector in SECTOR_KEYWORDS.items():
        if kw in t:
            for tk, meta in TICKER_META.items():
                if meta["sector"] == sector:
                    hits.add(tk)

    return sorted(hits)
