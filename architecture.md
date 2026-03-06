# Architecture

_Owner: Boardroom | Approved by: PO | Version: 1.0 — sourced from Workshop snapshot_

---

## Infrastructure

| Component | Detail |
|---|---|
| VPS | Hostinger KVM 2 — srv1161923.hstgr.cloud / 72.61.203.132 |
| OS | Ubuntu 24.04 LTS |
| Resources | 2 CPU / 8 GB RAM / 100 GB disk |
| Users | root (PO — infra, secrets) · claude (dev — Docker, Git) |
| Python | 3.12.3 |
| Docker | 28.2.2 |

**Existing non-YOLO services (must not be disrupted):**
| Service | Port | Purpose |
|---|---|---|
| Mosquitto MQTT | 1883 | IoT messaging (Shelly/Puli smart home) |
| SSH | 22 | Remote access |

---

## Running Containers

| Container | Branch | Purpose | Port |
|---|---|---|---|
| yolo-dev | develop/feature | Test & PO review | — |
| yolo-dashboard | develop | Live watchlist monitoring | — |
| yolo-paper | develop | Paper trading (live pipeline) | — |

Port ranges reserved: DEV 8001–8099 · PRD 8100–8199 (assigned at runtime, not in compose)
PRD container: not yet defined (pending strategy validation)

---

## Pipeline Services

### Layer 0 — API Clients
| Service | Integration | Purpose |
|---|---|---|
| T212Client | Trading 212 REST | Orders, positions, account |
| PolygonClient | Polygon.io REST | Snapshots, bars, news |
| PolygonWsFeed | Polygon.io WebSocket | Real-time ticks, quotes, aggregates |
| AnthropicClient | Claude API | LLM advisory (optional, degrades gracefully) |

### Layer 1 — Data Stores
| Service | Storage | Purpose |
|---|---|---|
| WatchlistService | SQLite + in-memory | Candidate lifecycle, observer pattern |
| JournalService | SQLite | Trade history + decision log |
| DDBot | — | Qualitative due diligence (Claude Haiku) |

### Layer 2 — Data Pipeline
| Service | Cadence | Purpose |
|---|---|---|
| PositionMonitor | 5s | T212 position polling |
| CandleEngine | 1-min/5-min | OHLCV aggregation + EMA9 |
| RiskProfileService | Per candidate | 5-factor weighted risk scoring |
| MarketScanner | Per cycle | Two-stage candidate discovery (snapshot → RVOL ≥ 5x) |

### Layer 3 — Exit Pipeline
| Service | Purpose |
|---|---|
| TradingEngine | Rule-based exit (trailing stop, EMA break, liquidity) |
| StrategyBrain | LLM exit advisory (Claude Sonnet, 5-min cycle, optional) |
| OrderManager | Order execution + limit→market escalation |

### Layer 4 — Entry Pipeline
| Service | Purpose |
|---|---|
| AnalystService | LLM candidate evaluation (Claude Haiku) |
| EntryMonitor | Real-time entry condition matching (WebSocket) |
| TraderService | Buy execution with 5 safety rails |

---

## Data Flow

```
Polygon Snapshot API
       │
  MarketScanner ── Stage 1 (price/vol/change) → Stage 2 (RVOL ≥ 5x)
       │
  WatchlistService ── NEW
       │
  AnalystService ── Claude Haiku → APPROVED / REJECTED
       │
  WatchlistService ── WATCHING (triggers + entry conditions)
       │
  EntryMonitor ── WebSocket ticks → entry conditions met → BUYING
       │
  TraderService ── 5 safety rails → T212 market/limit order → HOLDING
       │
  TradingEngine ── 1s eval loop: trailing stop, EMA break, liquidity
       │           StrategyBrain advisory (optional)
  OrderManager ── Sell → T212
       │
  JournalService ── Trade record + decision log → SQLite
```

---

## External APIs

| API | Auth | Purpose |
|---|---|---|
| Polygon.io | Bearer token | Snapshots, 1-min/5-min bars, news, WebSocket ticks |
| Trading 212 | Basic (key+secret) | Account, positions, orders (demo + live) |
| Anthropic (Claude) | API key | Haiku (DD, Analyst) · Sonnet (StrategyBrain) |

Secrets: age-encrypted `.env.prd` (root-only) · `.env.dev` (claude user)

---

## Research Layer

```
analysis/
├── backtester/
│   ├── engine.py           # BacktestEngine class (entry/exit simulation)
│   ├── strategy.py         # Composable rules (Rule + Strategy dataclasses)
│   ├── indicators.py       # 24 registered indicators (per-bar + O(n) series)
│   ├── data.py             # Polygon bar fetcher + JSON cache
│   ├── reports.py          # Missed opportunities, summary stats
│   ├── walk.py             # Deprecated — kept for scratch script compat
│   └── batch_historical.py # Batch backtest across dates/tickers
├── research/
│   ├── research-log.md     # EXP-001 to EXP-023
│   ├── strategies.json     # Strategy registry (active/retired)
│   └── ideas.md            # IDEA-NNN improvement proposals
├── cache/                  # Polygon bar cache ({ticker}_{date}_{tf}.json)
├── results/                # Backtest CSV output
└── scratch_exp*.py         # Experiment scripts
```

**Registered indicators (24):**
ema, sma, rsi, macd_histogram, bb_upper, bb_lower, vwap_session, atr, ema_gap,
volume_ratio, volume_ratio_ema, vwap_distance, price_change_pct, spread_ratio,
bb_width, kc_width, squeeze_on, squeeze_momentum, force_index_2, force_index_13,
kama, ib_high, ib_low, ib_range

---

## Project Structure

```
/home/claude/projects/yolo/
├── CLAUDE.md               # Project context + API contracts
├── DECISIONS.md            # Architectural decisions (DEC-NNN)
├── GLOSSARY.md             # Pipeline statuses, volume semantics
├── Dockerfile              # python:3.12-slim, non-root user
├── docker-compose.yml      # DEV service definition
├── pyproject.toml          # httpx, pydantic, typer, websocket-client, anthropic
├── .env.example            # 75+ configurable settings
├── src/                    # Application code (15 core modules)
├── tests/                  # 989 unit + 109 BDD + 7 regression
├── analysis/               # Research & backtesting layer
├── scripts/                # smoke-test.sh
└── docs/                   # Architecture, changelog, backlog, runbook
```

---

## Key Metrics

| Metric | Value |
|---|---|
| Current version | v0.13.0 |
| Unit tests | 989 |
| BDD scenarios | 109 |
| Regression tests | 7 |
| Registered indicators | 24 |
| Core services | 15 |
| External APIs | 3 |
| CLI commands | 14 |
| Configurable settings | 75+ |

---

## GitHub

| Repo | Visibility | Purpose |
|---|---|---|
| K25TOF/YOLO | Private | Autonomous trading application |
| K25TOF/yolo-firm | Private | Operating model documentation |
