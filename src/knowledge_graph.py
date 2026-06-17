"""
Knowledge graph: maps free-text company/sector references to NSE/BSE tickers.
Expanded coverage of Nifty 50 + popular mid-caps.
"""

ALIAS_TO_TICKER = {
    # IT
    "tcs": "TCS", "tata consultancy": "TCS", "tata consultancy services": "TCS",
    "infosys": "INFY", "infy": "INFY",
    "wipro": "WIPRO",
    "hcl tech": "HCLTECH", "hcl technologies": "HCLTECH", "hcltech": "HCLTECH",
    "tech mahindra": "TECHM",
    "ltimindtree": "LTIM", "lti mindtree": "LTIM",
    "persistent": "PERSISTENT", "persistent systems": "PERSISTENT",
    # Banking & Finance
    "hdfc bank": "HDFCBANK", "hdfc": "HDFCBANK",
    "icici": "ICICIBANK", "icici bank": "ICICIBANK",
    "sbi": "SBIN", "state bank": "SBIN", "state bank of india": "SBIN",
    "axis bank": "AXISBANK", "axis": "AXISBANK",
    "kotak": "KOTAKBANK", "kotak bank": "KOTAKBANK", "kotak mahindra": "KOTAKBANK",
    "indusind": "INDUSINDBK", "indusind bank": "INDUSINDBK",
    "bajaj finance": "BAJFINANCE",
    "bajaj finserv": "BAJAJFINSV",
    "sbi life": "SBILIFE",
    "hdfc life": "HDFCLIFE",
    # Energy & Oil
    "reliance": "RELIANCE", "reliance industries": "RELIANCE", "ril": "RELIANCE",
    "ongc": "ONGC", "oil and natural gas": "ONGC",
    "ntpc": "NTPC",
    "power grid": "POWERGRID", "powergrid": "POWERGRID",
    "coal india": "COALINDIA",
    "bpcl": "BPCL", "bharat petroleum": "BPCL",
    "ioc": "IOC", "indian oil": "IOC",
    # Auto
    "tata motors": "TATAMOTORS",
    "maruti": "MARUTI", "maruti suzuki": "MARUTI",
    "mahindra": "M&M", "m&m": "M&M", "mahindra and mahindra": "M&M",
    "bajaj auto": "BAJAJ-AUTO",
    "hero motocorp": "HEROMOTOCO", "hero motors": "HEROMOTOCO",
    "eicher": "EICHERMOT", "eicher motors": "EICHERMOT", "royal enfield": "EICHERMOT",
    # FMCG
    "itc": "ITC",
    "hul": "HINDUNILVR", "hindustan unilever": "HINDUNILVR",
    "nestle": "NESTLEIND", "nestle india": "NESTLEIND",
    "britannia": "BRITANNIA",
    "dabur": "DABUR",
    "godrej consumer": "GODREJCP",
    # Pharma
    "sun pharma": "SUNPHARMA", "sun pharmaceutical": "SUNPHARMA",
    "dr reddy": "DRREDDY", "dr reddys": "DRREDDY", "dr. reddy's": "DRREDDY",
    "cipla": "CIPLA",
    "divis": "DIVISLAB", "divi's lab": "DIVISLAB",
    "apollo hospitals": "APOLLOHOSP",
    # Metals & Materials
    "tata steel": "TATASTEEL",
    "jsw steel": "JSWSTEEL",
    "hindalco": "HINDALCO",
    "ultratech": "ULTRACEMCO", "ultratech cement": "ULTRACEMCO",
    "grasim": "GRASIM",
    "asian paints": "ASIANPAINT",
    # Telecom & Other
    "bharti airtel": "BHARTIARTL", "airtel": "BHARTIARTL",
    "adani": "ADANIENT", "adani enterprises": "ADANIENT",
    "adani ports": "ADANIPORTS",
    "larsen": "LT", "l&t": "LT", "larsen & toubro": "LT",
    "titan": "TITAN", "titan company": "TITAN",
    "nykaa": "NYKAA",
    "zomato": "ZOMATO",
    "paytm": "PAYTM",
    "dmart": "DMART", "avenue supermarts": "DMART",
}

TICKER_META = {
    # IT
    "TCS":        {"name": "Tata Consultancy",  "sector": "IT",       "price_sensitivity": 0.7},
    "INFY":       {"name": "Infosys",           "sector": "IT",       "price_sensitivity": 0.75},
    "WIPRO":      {"name": "Wipro",             "sector": "IT",       "price_sensitivity": 0.65},
    "HCLTECH":    {"name": "HCL Technologies",  "sector": "IT",       "price_sensitivity": 0.7},
    "TECHM":      {"name": "Tech Mahindra",     "sector": "IT",       "price_sensitivity": 0.7},
    "LTIM":       {"name": "LTIMindtree",       "sector": "IT",       "price_sensitivity": 0.75},
    "PERSISTENT": {"name": "Persistent Systems","sector": "IT",       "price_sensitivity": 0.8},
    # Banking
    "HDFCBANK":   {"name": "HDFC Bank",         "sector": "Banking",  "price_sensitivity": 0.7},
    "ICICIBANK":  {"name": "ICICI Bank",        "sector": "Banking",  "price_sensitivity": 0.7},
    "SBIN":       {"name": "State Bank of India","sector": "Banking", "price_sensitivity": 0.75},
    "AXISBANK":   {"name": "Axis Bank",         "sector": "Banking",  "price_sensitivity": 0.75},
    "KOTAKBANK":  {"name": "Kotak Mahindra Bank","sector": "Banking", "price_sensitivity": 0.7},
    "INDUSINDBK": {"name": "IndusInd Bank",     "sector": "Banking",  "price_sensitivity": 0.8},
    # NBFC & Insurance
    "BAJFINANCE": {"name": "Bajaj Finance",     "sector": "NBFC",     "price_sensitivity": 0.85},
    "BAJAJFINSV": {"name": "Bajaj Finserv",     "sector": "NBFC",     "price_sensitivity": 0.8},
    "SBILIFE":    {"name": "SBI Life",          "sector": "Insurance","price_sensitivity": 0.65},
    "HDFCLIFE":   {"name": "HDFC Life",         "sector": "Insurance","price_sensitivity": 0.65},
    # Energy
    "RELIANCE":   {"name": "Reliance Industries","sector": "Energy",  "price_sensitivity": 0.8},
    "ONGC":       {"name": "ONGC",              "sector": "Energy",   "price_sensitivity": 0.85},
    "NTPC":       {"name": "NTPC",              "sector": "Power",    "price_sensitivity": 0.6},
    "POWERGRID":  {"name": "Power Grid",        "sector": "Power",    "price_sensitivity": 0.55},
    "COALINDIA":  {"name": "Coal India",        "sector": "Energy",   "price_sensitivity": 0.75},
    "BPCL":       {"name": "Bharat Petroleum",  "sector": "Energy",   "price_sensitivity": 0.8},
    "IOC":        {"name": "Indian Oil",        "sector": "Energy",   "price_sensitivity": 0.75},
    # Auto
    "TATAMOTORS": {"name": "Tata Motors",       "sector": "Auto",     "price_sensitivity": 0.85},
    "MARUTI":     {"name": "Maruti Suzuki",     "sector": "Auto",     "price_sensitivity": 0.7},
    "M&M":        {"name": "Mahindra & Mahindra","sector": "Auto",    "price_sensitivity": 0.75},
    "BAJAJ-AUTO": {"name": "Bajaj Auto",        "sector": "Auto",     "price_sensitivity": 0.75},
    "HEROMOTOCO": {"name": "Hero MotoCorp",     "sector": "Auto",     "price_sensitivity": 0.7},
    "EICHERMOT":  {"name": "Eicher Motors",     "sector": "Auto",     "price_sensitivity": 0.8},
    # FMCG
    "ITC":        {"name": "ITC",               "sector": "FMCG",     "price_sensitivity": 0.6},
    "HINDUNILVR": {"name": "Hindustan Unilever","sector": "FMCG",     "price_sensitivity": 0.55},
    "NESTLEIND":  {"name": "Nestle India",      "sector": "FMCG",     "price_sensitivity": 0.5},
    "BRITANNIA":  {"name": "Britannia",         "sector": "FMCG",     "price_sensitivity": 0.55},
    "DABUR":      {"name": "Dabur",             "sector": "FMCG",     "price_sensitivity": 0.6},
    "GODREJCP":   {"name": "Godrej Consumer",   "sector": "FMCG",     "price_sensitivity": 0.6},
    # Pharma
    "SUNPHARMA":  {"name": "Sun Pharma",        "sector": "Pharma",   "price_sensitivity": 0.7},
    "DRREDDY":    {"name": "Dr Reddy's",        "sector": "Pharma",   "price_sensitivity": 0.7},
    "CIPLA":      {"name": "Cipla",             "sector": "Pharma",   "price_sensitivity": 0.7},
    "DIVISLAB":   {"name": "Divi's Labs",       "sector": "Pharma",   "price_sensitivity": 0.8},
    "APOLLOHOSP": {"name": "Apollo Hospitals",  "sector": "Healthcare","price_sensitivity": 0.7},
    # Metals
    "TATASTEEL":  {"name": "Tata Steel",        "sector": "Metals",   "price_sensitivity": 0.9},
    "JSWSTEEL":   {"name": "JSW Steel",         "sector": "Metals",   "price_sensitivity": 0.9},
    "HINDALCO":   {"name": "Hindalco",          "sector": "Metals",   "price_sensitivity": 0.9},
    # Materials
    "ULTRACEMCO": {"name": "UltraTech Cement",  "sector": "Materials","price_sensitivity": 0.7},
    "GRASIM":     {"name": "Grasim",            "sector": "Materials","price_sensitivity": 0.75},
    "ASIANPAINT": {"name": "Asian Paints",      "sector": "Materials","price_sensitivity": 0.6},
    # Telecom & Conglomerate
    "BHARTIARTL": {"name": "Bharti Airtel",     "sector": "Telecom",  "price_sensitivity": 0.7},
    "ADANIENT":   {"name": "Adani Enterprises", "sector": "Conglomerate","price_sensitivity": 0.95},
    "ADANIPORTS": {"name": "Adani Ports",       "sector": "Infra",    "price_sensitivity": 0.85},
    "LT":         {"name": "Larsen & Toubro",   "sector": "Infra",    "price_sensitivity": 0.7},
    # Consumer
    "TITAN":      {"name": "Titan Company",     "sector": "Consumer", "price_sensitivity": 0.7},
    "DMART":      {"name": "DMart",             "sector": "Retail",   "price_sensitivity": 0.65},
    # New Age
    "NYKAA":      {"name": "Nykaa",             "sector": "E-commerce","price_sensitivity": 0.9},
    "ZOMATO":     {"name": "Zomato",            "sector": "E-commerce","price_sensitivity": 0.9},
    "PAYTM":      {"name": "Paytm",             "sector": "FinTech",  "price_sensitivity": 0.95},
}

SECTOR_KEYWORDS = {
    "it sector": "IT", "software": "IT", "tech stocks": "IT", "indian it": "IT",
    "banking sector": "Banking", "banks": "Banking", "psu banks": "Banking",
    "private banks": "Banking",
    "auto sector": "Auto", "automobile": "Auto", "automakers": "Auto",
    "pharma sector": "Pharma", "pharmaceutical": "Pharma", "pharma stocks": "Pharma",
    "fmcg sector": "FMCG", "consumer goods": "FMCG",
    "metal stocks": "Metals", "steel sector": "Metals",
    "energy sector": "Energy", "oil and gas": "Energy", "oil & gas": "Energy",
    "power sector": "Power",
}


def resolve_entities(text):
    """Return a list of tickers referenced in the text (longest alias wins)."""
    t = text.lower()
    hits = set()
    for alias in sorted(ALIAS_TO_TICKER, key=len, reverse=True):
        if alias in t:
            hits.add(ALIAS_TO_TICKER[alias])
    for kw, sector in SECTOR_KEYWORDS.items():
        if kw in t:
            for tk, meta in TICKER_META.items():
                if meta["sector"] == sector:
                    hits.add(tk)
    return sorted(hits)