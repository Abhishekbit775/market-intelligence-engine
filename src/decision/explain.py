"""
Layer 4 (Decision) — Explainable AI rationale generator.

Turns the numeric trail behind a signal into a plain-English explanation.
This is the system's core differentiator: every recommendation is auditable.
(Production can swap/augment this with LIME or attention-weight attributions;
the template here is deterministic and always available.)
"""


def explain(signal):
    s = signal
    parts = []

    parts.append(
        f"{s['action']} signal for {s['ticker']} ({s['company']}) "
        f"with {round(s['confidence'] * 100)}% confidence."
    )

    sent = s["sentiment"]
    parts.append(
        f"Triggered by news from {s['source']}: \"{s['headline']}\". "
        f"FinBERT-style sentiment read this as {sent['label']} "
        f"(prob {sent['score']}, backend={sent['backend']}), "
        f"classified as a {s['category']} event."
    )

    parts.append(
        f"News impact score {s['news_score']} was fused with a technical score "
        f"of {s['tech_score']} (RSI {s['technicals'].get('rsi')}, "
        f"MACD {'>' if s['technicals']['macd'] > s['technicals']['macd_signal'] else '<'} signal). "
        f"News and technicals "
        f"{'agree' if s['agreement'] else 'disagree'} on direction."
    )

    if s["action"] == "HOLD":
        if s["direction"] == "neutral":
            reason = "the combined view is directionally neutral"
        elif not s["agreement"]:
            reason = ("the technical indicators do not confirm the news "
                      "direction (required to avoid false positives)")
        elif s["confidence"] < s["threshold"]:
            reason = (f"confidence {s['confidence']} is below the "
                      f"{s['threshold']} action threshold")
        else:
            reason = "entry conditions were not fully met"
        parts.append(f"No trade is recommended because {reason}.")
    else:
        r = s["risk_plan"]
        parts.append(
            f"Risk plan: entry around {r['entry_price']}, stop-loss {r['stop_loss']}, "
            f"target {r['profit_target']} (reward:risk {r['risk_reward']}:1). "
            f"Position sized to risk {r['risk_pct_of_capital']}% of capital "
            f"({r['position_qty']} shares). Auto-exit after "
            f"{r['time_exit_sessions']} sessions or on opposing sentiment "
            f"> {r['reversal_exit_threshold']}."
        )

    return " ".join(parts)
