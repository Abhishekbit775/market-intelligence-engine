# 📈 Event-Driven Market Intelligence Engine

> An AI-powered trading decision-support system that reads real financial news,
> understands it using FinBERT, and generates explainable Buy/Sell/Hold signals
> with full risk management — live on the Indian stock market (NSE/BSE).

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FinBERT](https://img.shields.io/badge/NLP-FinBERT-orange)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red?logo=streamlit)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🔴 Live Demo

**[market-intelligence-engine-lfyxprugagvgxgjace4mv2.streamlit.app](https://market-intelligence-engine-lfyxprugagvgxgjace4mv2.streamlit.app)**

Click **Run Pipeline** to see real-time AI trading signals generated from today's news.

---

## 🧠 What It Does

Most trading systems only look at price charts. This system reads the **news** and
**understands** it — then combines that with technical indicators to make trading decisions.

**End-to-end pipeline:**

```
Real News → FinBERT Sentiment → Entity Mapping → Impact Score
    → Technical Indicators → Signal Fusion → BUY/SELL/HOLD
        → Risk Plan → Plain-English Explanation → Dashboard
```

**Example signal generated from today's news:**

| Field | Value |
|-------|-------|
| Action | 🟢 BUY |
| Stock | RELIANCE (Reliance Industries) |
| Confidence | 99% |
| News Trigger | "RIL shares jump 6% in 3 days" — Times of India |
| Sentiment | Positive (0.9459) via FinBERT |
| Entry | ₹1,332.70 (real NSE price) |
| Stop-Loss | ₹1,291.47 |
| Target | ₹1,401.42 |
| Risk:Reward | 1.67:1 |

---

## ⚙️ Architecture (5 Layers)

| Layer | What It Does | Tech |
|-------|-------------|------|
| 1 — Ingestion | Pulls live news + NSE/BSE prices | NewsAPI, yfinance |
| 2 — NLP | Reads sentiment, finds company names | FinBERT, spaCy |
| 3 — Signal | Scores impact, calculates indicators | RSI, MACD, Bollinger, ATR |
| 4 — Decision | Emits BUY/SELL/HOLD + risk plan | Threshold engine, XAI |
| 5 — Output | Stores signals, serves API + dashboard | SQLite, FastAPI, Streamlit |

---

## 🚀 Run It Locally

```bash
# 1. Clone
git clone https://github.com/Abhishekbit775/market-intelligence-engine.git
cd market-intelligence-engine

# 2. Setup
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# 3. Install
pip install -r requirements.txt
pip install transformers torch spacy
python -m spacy download en_core_web_sm

# 4. Add your keys
cp .env.example .env
# Edit .env and add your NewsAPI key (free at newsapi.org)

# 5. Run dashboard
streamlit run dashboard/app.py

# 6. Or run API
uvicorn api.main:app --port 8000
```

Works offline too — falls back to sample news and synthetic prices automatically.

---

## 🐳 Deploy with Docker

```bash
docker compose up --build
# Dashboard → http://localhost:8501
# API docs  → http://localhost:8000/docs
```

---

## 📊 Stock Coverage

Covers **50 NSE-listed stocks** across 10 sectors:

| Sector | Example Stocks |
|--------|---------------|
| IT | TCS, Infosys, Wipro, HCL Tech, Tech Mahindra |
| Banking | HDFC Bank, ICICI Bank, SBI, Axis Bank, Kotak |
| Energy | Reliance, ONGC, BPCL, Coal India, NTPC |
| Auto | Maruti, Tata Motors, M&M, Bajaj Auto, Hero |
| Pharma | Sun Pharma, Dr Reddy's, Cipla, Divi's Labs |
| FMCG | ITC, HUL, Nestle, Britannia, Dabur |
| Metals | Tata Steel, JSW Steel, Hindalco |
| Infra | L&T, Adani Ports |
| Consumer | Titan, DMart |
| FinTech | Bajaj Finance, Paytm, Nykaa, Zomato |

---

## 🛠️ Tech Stack

```
Python 3.11 · FinBERT (HuggingFace) · spaCy · FastAPI
Streamlit · yfinance · NewsAPI · SQLite · Docker · GitHub Actions
```

---

## 📁 Project Structure

```
market-intelligence-engine/
├── src/
│   ├── ingestion/        # News fetcher + market data
│   ├── nlp/              # FinBERT sentiment + NER + dedup
│   ├── signals/          # Technical indicators + impact scorer + fusion
│   ├── decision/         # Buy/Sell/Hold engine + risk + XAI explainer
│   ├── storage/          # SQLite persistence
│   ├── backtest/         # Walk-forward backtesting harness
│   └── pipeline.py       # Master orchestrator
├── api/main.py           # FastAPI REST service
├── dashboard/app.py      # Streamlit UI
├── config.py             # All tunables in one place
└── tests/                # Unit tests
```

---

## ⚠️ Disclaimer

This system is a research prototype and decision-support tool built for the
**SN Bose Summer Internship 2026 at NIT Silchar**.
Past performance does not guarantee future results.
Always consult a registered financial advisor before making investment decisions.

---

## 👨‍💻 Author

**Abhishek Kumar** — NIT Silchar (Roll No. 2313156)
Summer Intern, Satyendra Nath Bose National Centre for Basic Sciences, 2026