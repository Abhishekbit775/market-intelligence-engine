from dotenv import load_dotenv
load_dotenv()
"""
The orchestrator — runs the full five-layer pipeline:

  Ingest news + market data
    -> NLP (dedup, sentiment, NER, categorise)
      -> Impact score + technical indicators
        -> Fusion + calibrated confidence
          -> Decision (Buy/Sell/Hold) + risk plan + explanation
            -> Persist

run_pipeline() returns the list of signal objects and also stores them.
"""
from src.ingestion.news_fetcher import fetch_news
from src.ingestion.market_data import get_ohlcv
from src.nlp.dedup import deduplicate
from src.nlp.sentiment import analyze_sentiment
from src.nlp.ner import extract_entities
from src.signals.indicators import technical_signal
from src.signals.impact_scorer import impact_score
from src.signals.fusion import fuse
from src.decision.engine import decide
from src.storage.db import save_signal


def run_pipeline(capital=100_000, persist=True, limit=20):
    articles = deduplicate(fetch_news(limit=limit))
    signals = []

    for art in articles:
        text = f"{art['headline']}. {art.get('body', '')}"
        ents = extract_entities(text)
        if not ents["tickers"]:
            continue  # no mappable instrument -> skip

        sentiment = analyze_sentiment(text)

        for ent in ents["tickers"]:
            imp = impact_score(
                sentiment, art["source"], ents["category"],
                ent["price_sensitivity"], art.get("published", ""),
            )
            try:
                df = get_ohlcv(ent["ticker"])
                tech = technical_signal(df)
            except Exception:
                continue

            fusion_out = fuse(imp["news_score"], tech["tech_score"])
            sig = decide(
                ticker=ent["ticker"], company=ent["name"],
                headline=art["headline"], source=art["source"],
                category=ents["category"], sentiment=sentiment,
                news_score=imp["news_score"], technicals=tech,
                fusion_out=fusion_out, capital=capital,
            )
            sig["impact_components"] = imp["components"]
            signals.append(sig)
            if persist:
                save_signal(sig)

    # surface actionable signals first, then by confidence
    signals.sort(key=lambda s: (s["action"] == "HOLD", -s["confidence"]))
    return signals


if __name__ == "__main__":
    from src.nlp.sentiment import backend_name
    sigs = run_pipeline(persist=False)
    print(f"Sentiment backend: {backend_name()}")
    print(f"Generated {len(sigs)} signals\n" + "=" * 70)
    for s in sigs[:8]:
        print(f"\n[{s['action']}] {s['ticker']} ({s['company']}) "
              f"conf={s['confidence']}")
        print("  " + s["explanation"])
