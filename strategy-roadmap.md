# Strategy & Roadmap

_Owner: Boardroom | Approved by: PO | Version: 1.0_

---

## Vision

Build a fully autonomous US stock trading system that generates consistent absolute profit
from intraday momentum opportunities. Operate as a disciplined, self-improving trading firm
with human oversight at all critical decision points.

---

## Guiding Principles

1. **Reliable profit first** — even 1 trade/week at 90% WR beats 50 trades at 50% WR
2. **Bottom-up strategies** — build per ticker/profile, not one-size-fits-all
3. **Isolation testing** — compare only divergent trades between variants
4. **No LLM in critical momentum path** — mechanical fast path for entries
5. **Absolute profit is the objective** — not win rate, not trade count
6. **Don't rely on outlier runners** — strategy must be robust without 1-2 big winners
7. **Simplicity over premature optimisation** — defer complexity until proven necessary

---

## Trade Modes

| Mode | Entry | Exit | Status |
|---|---|---|---|
| Momentum | Fully autonomous | Fully autonomous | Active (paper) |
| Swing | Manual entry | Automated exit | Future |

---

## Current Strategy (Active)

**vol_filter v2.1.0**
- Signal: EMA3/EMA9 gap crosses above 3.0%
- Volume filter: volume_ratio (EMA-10) ≥ 2.0
- Exit: EMA gap crosses below 1.5% OR 2.0x ATR(14) trailing stop
- Session: RTH only (09:30–16:00 ET)
- Force close: EOD
- Skip first entry: per ticker per day

**Research verdict (EXP-023):** Not production ready.
34% WR, profit driven by outlier runners — violates principle #6.
Next focus: Grinder strategy (IDEA-016) and book-derived hypotheses.

---

## Identified Trade Profiles

| Profile | Archetype | Characteristic | Strategy approach |
|---|---|---|---|
| Impulse | MOBX | Sharp EMA gap spike, high RVOL | vol_filter works, fast entry |
| Grinder | MDBX | Steady climb, moderate EMA gap | Needs different strategy (IDEA-016) |

---

## Phases

### ✅ Phase 1 — Foundation
Infrastructure, VPS, Docker, CI/CD, T212 + Polygon integration.

### ✅ Phase 2 — Core Pipeline
Scanner, Watchlist, Analyst, Trader, Monitor, Observer pattern.

### ✅ Phase 3 — Exit Engine
TradingEngine, StrategyBrain, OrderManager, safety rails.

### ✅ Phase 4 — Entry Pipeline (v0.13.0 PRD)
4.1 Scanner · 4.2 Watchlist · 4.3 Analyst · 4.4 Observer
4.5 Monitor · 4.6 Trader + Safety Rails · 4.7 Pipeline Orchestrator
4.8 Smart Rejection

### 🔧 Phase 5 — Triple Loop (Learning)
5.1 — Backtesting Engine (original)
5.2 — Research Knowledge Base
5.3a — Engine Rebuild — clean BacktestEngine class
5.3b — VWAP, RSI, Spread Ratio, snapshot CSV
5.3c — TTM Squeeze, Force Index, KAMA
5.3d — Volume Decay exit, Initial Balance
5.4 🔲 Agent Definitions (Manager, Analyst, Engineer)
5.5 🔲 Session log + communication protocol
5.6 🔲 Manager-led learning cycle
5.7 🔲 PO review document + async approval flow

### 🔲 Phase 6 — Production
Strategy validated → real capital deployment.
Security hardening, capital policy, position sizing.

---

## Backlog (Selected)

| ID | Description | Priority |
|---|---|---|
| IDEA-016 | Grinder strategy | High |
| — | Mechanical fast path (bypass Analyst LLM for momentum) | High |
| — | Position sizing (Kelly or fixed fractional) | Medium |
| — | Multi-timeframe confirmation | Medium |
| — | Adaptive strategy variables mid-trade | Medium |
| — | Benzinga news integration (catalyst confirmation) | Low |
| — | NBBO spread data for slippage modelling | Low |
| — | Value Area / Volume Profile | Parked |
| — | time_of_day_avg volume decay mode | Parked |

---

## Research State

- **Experiments completed:** EXP-001 to EXP-023
- **Active strategy:** vol_filter v2.1.0 (skip-first variant)
- **Book extraction:** Pass 1 TOC complete (~800 books), Pass 2 ~65 books extracted
- **Indicators available:** 25 registered in backtester
- **Next experiment focus:** Grinder strategy (IDEA-016), book-derived hypotheses
