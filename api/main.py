"""
Layer 5 — REST API (FastAPI).

Endpoints:
  GET /health                 -> liveness + active NLP backend
  GET /signals?limit=&action= -> run pipeline, return signals (optional filter)
  GET /signals/stored         -> last persisted signals from DB

Run:  uvicorn api.main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""
from fastapi import FastAPI, Query
from typing import Optional

from src.pipeline import run_pipeline
from src.storage.db import recent_signals
from src.nlp.sentiment import backend_name

app = FastAPI(
    title="Event-Driven Market Intelligence Engine",
    description="AI-based context-aware trading signal API (research use only).",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok", "nlp_backend": backend_name()}


@app.get("/signals")
def get_signals(
    limit: int = Query(20, ge=1, le=100),
    action: Optional[str] = Query(None, description="Filter: BUY, SELL, or HOLD"),
    capital: float = Query(100_000, gt=0),
):
    sigs = run_pipeline(capital=capital, persist=True, limit=limit)
    if action:
        sigs = [s for s in sigs if s["action"] == action.upper()]
    return {"count": len(sigs), "backend": backend_name(), "signals": sigs}


@app.get("/signals/stored")
def get_stored(limit: int = Query(50, ge=1, le=200)):
    return {"signals": recent_signals(limit)}


@app.get("/")
def root():
    return {"message": "Market Intelligence Engine API. See /docs for usage.",
            "disclaimer": "Research/educational prototype. Not investment advice."}
