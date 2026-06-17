"""
Layer 5 — Streamlit dashboard.

Live signal feed, sector heat-map, confidence gauges, per-signal explanation
cards, and a P&L simulation over the generated signals.

Run:  streamlit run dashboard/app.py
"""
import os
import sys
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import run_pipeline
from src.nlp.sentiment import backend_name
from src.knowledge_graph import TICKER_META

st.set_page_config(page_title="Market Intelligence Engine", layout="wide")

st.title("📈 Event-Driven Market Intelligence Engine")
st.caption("AI-based context-aware trading signals — research prototype, not investment advice.")

with st.sidebar:
    st.header("Controls")
    capital = st.number_input("Capital (₹)", 10_000, 10_000_000, 100_000, step=10_000)
    limit = st.slider("Max news items", 5, 30, 20)
    only_actionable = st.checkbox("Show only BUY/SELL", value=False)
    run = st.button("🔄 Run Pipeline", type="primary")
    st.markdown("---")
    st.write(f"**NLP backend:** `{backend_name()}`")

if run:
    with st.spinner("Running five-layer pipeline..."):
        st.session_state.signals = run_pipeline(capital=capital, persist=True, limit=limit)

signals = st.session_state.get("signals", [])
if only_actionable:
    signals = [s for s in signals if s["action"] != "HOLD"]

# ---- summary metrics ----
buys = sum(s["action"] == "BUY" for s in signals)
sells = sum(s["action"] == "SELL" for s in signals)
holds = sum(s["action"] == "HOLD" for s in signals)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Signals", len(signals))
c2.metric("BUY", buys)
c3.metric("SELL", sells)
c4.metric("HOLD", holds)

# ---- sector heat-map (mentions) ----
st.subheader("Sector Activity Heat-map")
sector_counts = {}
for s in signals:
    sec = TICKER_META.get(s["ticker"], {}).get("sector", "Unknown")
    sector_counts[sec] = sector_counts.get(sec, 0) + 1
if sector_counts:
    st.bar_chart(pd.Series(sector_counts).sort_values(ascending=False))

# ---- P&L simulation ----
st.subheader("P&L Simulation (illustrative)")
pnl_rows = []
running = 0.0
for s in signals:
    if s["action"] in ("BUY", "SELL") and s.get("risk_plan"):
        rp = s["risk_plan"]
        # simple expectancy: win prob ~ confidence, win=target dist, loss=stop dist
        win = abs(rp["profit_target"] - rp["entry_price"]) * rp["position_qty"]
        loss = abs(rp["entry_price"] - rp["stop_loss"]) * rp["position_qty"]
        exp = s["confidence"] * win - (1 - s["confidence"]) * loss
        running += exp
        pnl_rows.append({"ticker": s["ticker"], "action": s["action"],
                         "expected_pnl": round(exp, 2), "cumulative": round(running, 2)})
if pnl_rows:
    df = pd.DataFrame(pnl_rows)
    st.line_chart(df.set_index("ticker")["cumulative"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No actionable BUY/SELL signals in this run to simulate.")

# ---- signal cards ----
st.subheader("Signal Feed")
for s in signals:
    color = {"BUY": "🟢", "SELL": "🔴", "HOLD": "⚪"}[s["action"]]
    with st.expander(f"{color} {s['action']} — {s['ticker']} ({s['company']})  ·  conf {s['confidence']}"):
        st.progress(min(s["confidence"], 1.0), text=f"Confidence {round(s['confidence']*100)}%")
        st.write(f"**News:** {s['headline']}  _( {s['source']} )_")
        st.write(f"**Sentiment:** {s['sentiment']['label']} ({s['sentiment']['score']})  ·  "
                 f"**Category:** {s['category']}  ·  "
                 f"**Direction:** {s['direction']}")
        if s.get("risk_plan"):
            rp = s["risk_plan"]
            a, b, c = st.columns(3)
            a.metric("Entry", rp["entry_price"])
            b.metric("Stop", rp["stop_loss"])
            c.metric("Target", rp["profit_target"])
        st.info(s["explanation"])
