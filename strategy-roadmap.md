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
5.3d — Volume Decay exit, Initial Balance (24 indicators)
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
- **Indicators available:** 25 registered in backtester (incl. ema_gap_acceleration)
- **Operators available:** crosses_above, crosses_below, greater_than, less_than

### LC-2025-006 — Full Re-Validation Synthesis

**Class A re-runs on momentum universe (5,755 pairs, 183 dates):**

| Experiment | Original | Re-run | Verdict |
|---|---|---|---|
| EXP-010/011 | +80.3%, 50% WR | -40.1%, 32.7% WR | **Overturned** — selection bias |
| EXP-014 | +158.9%, 46% WR | -22.3%, 37.0% WR | **Overturned** — selection bias |
| EXP-016/023 | +168.8%/+67.4% | -398.1%, 32.0% WR | **Universe mismatch** — WR stable |
| EXP-022 | +50.7%, 50% WR | -416.4%, 30.8% WR | **Overturned** — selection bias |

**Key findings:**
- Vol_filter has no edge on the broad momentum universe — not production ready
- Original positive results were artefacts of hand-picked ticker sets
- Skip-first is the strongest validated filter (33pp WR gap on scanner universe)
- ATR exit marginally helps (+1.2pp WR) — driven by moderate movers only
- Gap acceleration filter shows consistent promise (+5.8pp WR, multi-source)

**Ranked leads for next phase:**
1. HYP-025 corrected re-test (low effort, high value)
2. Gap acceleration filter on vol_filter (strong evidence)
3. ATR isolation on broad universe (closes open question)
4. Combined overextended entry filter — IDEA-018
5. RVOL threshold sensitivity (3x/4x/5x)
6. VWAP asymmetric threshold — IDEA-017

### HYP-025 — Grinder Strategy Phase 1

**Status: INCONCLUSIVE — config error**

- **Original result:** 653 trades, 28.6% WR, -353.6% P&L — initially classified as FAILED
- **Audit finding (LC-2025-002):** Exit rule `ema_gap crosses_below 2.0` was logically inverted relative to entry `crosses_above 1.0`. Positions trapped to EOD force-close (avg hold 52-70 bars vs 7.5 for vol_filter). All PnL/WR results disqualified.
- **Acceleration filter:** Directionally promising — reduces trades 239→109 (-54%), improves WR by +5.8pp
- **Corrected re-test pending:** Exit changed to `ema_gap crosses_below 0.5` (fade-from-entry logic)
- **Next:** PO to approve corrected re-test config
