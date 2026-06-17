# Event-Driven Market Intelligence Engine

An AI-based system for context-aware trading decisions. It ingests financial
news, reads it with NLP (FinBERT-style sentiment + entity recognition), fuses
that with technical indicators, and emits **explainable Buy / Sell / Hold
signals** with full risk-management plans.

> ⚠️ **Research / educational prototype only. Not investment advice.**
> Past backtest performance does not guarantee future results.

---

## Why it works out of the box

The system has **graceful fallbacks** at every external dependency, so it runs
end-to-end with zero API keys and zero model downloads — then upgrades
automatically when you add them:

| Component        | Full mode (recommended)        | Fallback (default, offline)      |
|------------------|--------------------------------|----------------------------------|
| Sentiment        | FinBERT (`ProsusAI/finbert`)   | Financial lexicon scorer         |
| Entity extraction| spaCy `en_core_web_sm`         | Knowledge-graph keyword matching |
| Dedup            | FAISS + embeddings             | Token Jaccard similarity         |
| News             | NewsAPI (live)                 | Bundled `data/sample_news.json`  |
| Market data      | yfinance / Alpha Vantage       | Deterministic synthetic OHLCV    |
| Database         | PostgreSQL                     | SQLite (auto-created)            |

The dashboard and `/health` endpoint always show which backend is active.

---

## Architecture (five layers)

```
Layer 1  Ingestion   news_fetcher.py · market_data.py
Layer 2  NLP         sentiment.py · ner.py · dedup.py
Layer 3  Signal      indicators.py · impact_scorer.py · fusion.py
Layer 4  Decision    engine.py · risk.py · explain.py
Layer 5  Persist/UI  storage/db.py · api/main.py · dashboard/app.py
                      + backtest/harness.py
```

`src/pipeline.py` orchestrates all five. `config.py` holds every tunable.

---

## Quick start (local, ~2 minutes)

```bash
# 1. clone / unzip, then enter the folder
cd market-intelligence-engine

# 2. (recommended) virtual environment
python3 -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate

# 3. install core deps
pip install -r requirements.txt

# 4a. run the pipeline once in the terminal
python -m src.pipeline

# 4b. OR launch the dashboard
streamlit run dashboard/app.py            # opens http://localhost:8501

# 4c. OR launch the API
uvicorn api.main:app --reload --port 8000 # docs at http://localhost:8000/docs
```

That's the whole thing running on sample data. No keys needed.

### Enable full AI mode

```bash
pip install transformers torch spacy
python -m spacy download en_core_web_sm
```

The first run downloads FinBERT (~400 MB) from HuggingFace and caches it.
Set `USE_FINBERT=on` in `.env` to require it, or `off` to force the fast
lexicon (handy on machines without a GPU).

### Use live news

Get a free key at newsapi.org, then:

```bash
cp .env.example .env
# edit .env and set NEWSAPI_KEY=your_key
```

---

## API reference

| Endpoint              | What it does                                            |
|-----------------------|---------------------------------------------------------|
| `GET /health`         | Liveness + active NLP backend                           |
| `GET /signals`        | Run the pipeline, return signals. Params: `limit`, `action` (BUY/SELL/HOLD), `capital` |
| `GET /signals/stored` | Last persisted signals from the database                |
| `GET /docs`           | Interactive Swagger UI                                  |

Example:

```bash
curl "http://localhost:8000/signals?action=SELL&capital=200000"
```

---

## Backtesting

```bash
python -m src.backtest.harness
```

This computes win rate, profit factor, annualised Sharpe, max drawdown, and
average holding period, with 0.05% one-way transaction costs modelled.

**Important:** the bundled harness uses *random* entry points on synthetic
price data — it proves the measurement machinery, not the strategy's edge.
For the real validated report you must feed it (a) your actual logged signals
and (b) real archived news + OHLCV (2019–2024). Until then, do **not** put its
numbers on a resume or in the report as if they were the engine's performance.

---

## Deployment options

### Option A — Docker (single command, recommended)

```bash
docker compose up --build
# API       -> http://localhost:8000/docs
# Dashboard -> http://localhost:8501
```

To use Postgres instead of SQLite, uncomment the `db:` block in
`docker-compose.yml` and set `DB_URL=postgresql://mie:mie@db:5432/mie` in `.env`.

### Option B — Streamlit Community Cloud (free, easiest for the dashboard demo)

1. Push this repo to GitHub.
2. Go to share.streamlit.io → "New app" → pick the repo.
3. Set **main file** to `dashboard/app.py`.
4. Add `NEWSAPI_KEY` under the app's *Secrets* if you want live news.
5. Deploy — you get a public URL to share with reviewers.

### Option C — Render / Railway / Fly.io (for the API)

These read the `Dockerfile` directly:

- **Render:** New → Web Service → connect repo → it auto-detects the Dockerfile.
  Start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`.
- **Railway:** New Project → Deploy from repo → add env vars from `.env.example`.
- **Fly.io:** `fly launch` then `fly deploy`.

Add a managed Postgres add-on and set `DB_URL` to its connection string.

### Option D — Any VPS (DigitalOcean / EC2 / your college server)

```bash
git clone <your-repo> && cd market-intelligence-engine
docker compose up -d --build          # runs detached
# put nginx in front for HTTPS if exposing publicly
```

---

## Testing

```bash
pytest -q          # if pytest is installed
```

Covers entity resolution, sentiment, categorisation, dedup, indicators, impact
scoring, fusion, risk plans, and a full pipeline smoke test.

---

## Project layout

```
market-intelligence-engine/
├── config.py                 # all tunables (thresholds, weights, keys)
├── requirements.txt
├── Dockerfile · docker-compose.yml · .env.example
├── data/sample_news.json     # offline demo feed
├── src/
│   ├── knowledge_graph.py     # entity -> NSE/BSE ticker mapping
│   ├── ingestion/             # Layer 1
│   ├── nlp/                   # Layer 2
│   ├── signals/               # Layer 3
│   ├── decision/              # Layer 4
│   ├── storage/               # Layer 5 (persistence)
│   ├── backtest/              # evaluation harness
│   └── pipeline.py            # orchestrator
├── api/main.py                # FastAPI service
├── dashboard/app.py           # Streamlit UI
└── tests/test_pipeline.py
```

---

## How a signal is produced (end to end)

1. **Ingest** headlines + OHLCV.
2. **Dedup** near-identical stories.
3. **Sentiment** (Positive/Negative/Neutral + probability) and **NER**
   (resolve to tickers, classify event category).
4. **Impact score** = weighted blend of sentiment strength, source credibility,
   event category, entity price-sensitivity, and recency decay.
5. **Technical score** from RSI / MACD / Bollinger / volume.
6. **Fuse** the two into a calibrated confidence.
7. **Decide**: BUY/SELL only if confidence ≥ 0.65 *and* a technical indicator
   confirms the direction; otherwise HOLD.
8. **Risk plan**: 1.5×ATR stop, 2.5×ATR target, position sizing, time +
   sentiment-reversal exits.
9. **Explain**: a plain-English rationale is attached to every signal.
10. **Persist** to the database; surface via API and dashboard.

---

## Roadmap (from the proposal)

v1.1 broker API integration · v1.2 Hindi/regional news (mBERT) ·
v2.0 reinforcement learning for strategy selection · v2.1 F&O signals ·
v3.0 global markets · v3.1 portfolio optimisation.
```
