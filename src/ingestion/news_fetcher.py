"""
Layer 1 (Ingestion) — News fetcher.

If NEWSAPI_KEY is set it pulls live business headlines; otherwise it loads the
bundled sample feed so the pipeline is fully runnable offline. Each article is
normalised to: {headline, source, published, body}.
"""
import json
import os
from config import config

_SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_news.json")


def _load_sample():
    with open(os.path.abspath(_SAMPLE_PATH)) as f:
        return json.load(f)


def fetch_news(query="India stock market", limit=20):
    if not config.NEWSAPI_KEY:
        return _load_sample()[:limit]
    try:
        import requests
        r = requests.get(
            "https://newsapi.org/v2/everything",
            params={"q": query, "language": "en", "sortBy": "publishedAt",
                    "pageSize": limit, "apiKey": config.NEWSAPI_KEY},
            timeout=10,
        )
        r.raise_for_status()
        out = []
        for a in r.json().get("articles", []):
            out.append({
                "headline": a.get("title", ""),
                "source": (a.get("source") or {}).get("name", "Unknown"),
                "published": a.get("publishedAt", ""),
                "body": a.get("description", "") or "",
            })
        return out or _load_sample()[:limit]
    except Exception:
        return _load_sample()[:limit]
