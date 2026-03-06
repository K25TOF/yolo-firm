# KPI Framework

_Owner: Boardroom | Approved by: PO | Version: 1.0_

---

## Overview

KPIs are stored as structured JSON in `analysis/kpis/` on the VPS.
Updated by the pipeline after each session. Readable by all LLM agents.
Targets TBD — establish baselines first, then set targets and priorities.

---

## Layer 1 — Financial Performance

_Tracked: daily, weekly, monthly_

| KPI | Description | Unit |
|---|---|---|
| Absolute P&L | Net profit/loss | GBP |
| P&L vs target | Once target set | GBP / % |
| Win rate | Winning trades / total trades | % |
| Avg win / avg loss | Reward:risk ratio | ratio |
| Profit factor | Gross profit / gross loss | ratio |
| Max drawdown | Peak-to-trough loss | % |
| Max drawdown duration | Consecutive losing days | days |
| Sharpe ratio | Risk-adjusted return | annualised |

---

## Layer 2 — Strategy Quality

_Tracked: per trade, daily, weekly_

**Entry quality:**
| KPI | Description |
|---|---|
| Signal-to-trade conversion | Signals fired vs trades taken |
| Entry timing | Bars from signal to fill |
| Entry price vs signal price | Slippage proxy |

**Exit quality:**
| KPI | Description |
|---|---|
| Exit reason distribution | % EMA / ATR / EOD / volume_decay |
| Average hold duration | Bars and minutes |
| MAE | Maximum Adverse Excursion — how far against us before exit |
| MFE | Maximum Favourable Excursion — max profit available |
| MFE capture rate | Exit P&L / MFE — are we leaving money on table? |

**Scanner quality:**
| KPI | Description |
|---|---|
| Candidates per session | Raw scanner output |
| Candidate → watchlist rate | % progressing |
| Watchlist → trade rate | % resulting in entry |
| Ticker diversity | Concentration in same tickers |

---

## Layer 3 — Operational Excellence

_Tracked: per minute (stability), per session, daily_

**Pipeline reliability:**
| KPI | Description |
|---|---|
| Session uptime % | Did pipeline run full RTH session? |
| Component error rate | Errors per service per session |
| Pipeline restart frequency | Unexpected restarts |

**Execution integrity:**
| KPI | Description |
|---|---|
| Order submission latency | Signal → T212 order (ms) |
| Order fill latency | Submission → confirmed fill (ms) |
| Rejected order rate | % rejected by T212 or safety rails |
| Safety rail trigger frequency | Which rails fire, how often |

**Data integrity:**
| KPI | Description |
|---|---|
| Polygon API error rate | Failed requests per session |
| Cache hit rate | % data served from cache vs API |
| Missing bar frequency | Gaps in 1-min data |
| Polygon vs T212 price sync | Spot check — same bar, same price? |
| Timestamp offset | Flag if consistent offset detected |

**System health:**
| KPI | Description |
|---|---|
| VPS CPU / memory | Usage % |
| Container restart frequency | Unexpected restarts |
| API rate limit hits | Polygon, T212, Anthropic |

---

## Layer 4 — Risk Management

_Tracked: per trade, daily_

| KPI | Description |
|---|---|
| Largest single loss | Absolute (GBP) and % |
| Consecutive losing trades | Current streak and max streak |
| Daily loss limit breaches | Once limits defined |
| Position concentration | % capital in single position |
| Exposure time | % of session with open position |

---

## Layer 5 — Agent Health

_Tracked: after each PRD release and on-demand_

| KPI | Agent | Threshold |
|---|---|---|
| Memory file size | All | TBD per agent |
| Memory entry count | All | TBD |
| Age of oldest entry | All | Flag if > 90 days unreferenced |
| Last housekeeping date | All | Must not exceed release cadence |

**Housekeeping triggers:**
- Memory file exceeds size cap → Manager flags to PO for pruning
- Entry older than threshold and unreferenced → candidate for removal
- After every PRD release → full memory review

---

## Storage

```
analysis/kpis/
  financial.json     — P&L, win rate, profit factor, drawdown
  strategy.json      — entry/exit quality, scanner metrics
  operational.json   — latency, errors, uptime, API health
  risk.json          — loss streaks, concentration, exposure
  agent-health.json  — memory file sizes, entry counts, housekeeping dates
```
