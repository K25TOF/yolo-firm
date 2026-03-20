# Architecture

_Owner: Boardroom | Approved by: PO | Version: 1.1 — updated 2026-03-08 (Phase 7+8)_

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
├── datastore/              # Centralised data access (Story 8.1)
│   └── __init__.py         # DataStore class — typed read/write for all 7 datasets
├── refresh.py              # Daily pipeline orchestrator (Story 8.2)
├── backtester/
│   ├── engine.py           # BacktestEngine class (entry/exit simulation)
│   ├── strategy.py         # Composable rules (Rule + Strategy dataclasses)
│   ├── indicators.py       # 25 registered indicators (per-bar + O(n) series)
│   ├── data.py             # Polygon bar fetcher + JSON cache + NewsArticle model
│   ├── reports.py          # Missed opportunities, summary stats
│   └── batch_historical.py # Batch backtest across dates/tickers
├── day_simulator.py        # Historical day reconstruction (grouped + 1min bars)
├── signal_bars.py          # Enriched 1-min bars → signal_bars.parquet (1.7 GB)
├── rvol_baseline.py        # Per-ticker RVOL baseline → rvol_baseline.parquet
├── ticker_metadata.py      # Float, sector, exchange → ticker_metadata.parquet
├── research/
│   ├── eod_labeler.py      # EOD % change buckets → eod_performance_labels.parquet
│   ├── research-log.md     # EXP-001 to EXP-026
│   ├── strategies.json     # Strategy registry (active/retired)
│   └── ideas.md            # IDEA-NNN improvement proposals
├── cache/                  # Polygon bar/news cache
├── scripts/
│   └── fetch_news.py       # Historical Benzinga news fetcher
└── logs/                   # Refresh pipeline logs
```

**Registered indicators (25):**
ema, sma, rsi, macd_histogram, bb_upper, bb_lower, vwap_session, atr, ema_gap,
volume_ratio, volume_ratio_ema, vwap_distance, price_change_pct, spread_ratio,
bb_width, kc_width, squeeze_on, squeeze_momentum, force_index_2, force_index_13,
kama, ib_high, ib_low, ib_range, ema_gap_acceleration

**Daily refresh pipeline (cron 02:30 ET Tue–Sat):**
grouped daily → Stage 1 + 1min bars → news + ticker metadata → rvol baseline + eod labels → signal bars

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
├── src/                    # Application code (17 core services)
├── tests/                  # 1314 unit + 115 BDD + 7 regression
├── analysis/               # Research & backtesting layer
├── scripts/                # smoke-test.sh
└── docs/                   # Architecture, changelog, backlog, runbook
```

---

## Key Metrics

| Metric | Value |
|---|---|
| Current version | v0.18.0 (develop) |
| Unit tests | 1314 |
| BDD scenarios | 115 |
| Regression tests | 7 |
| Registered indicators | 25 |
| Core services | 17 |
| External APIs | 3 |
| CLI commands | 14 |
| Configurable settings | 75+ |
| Research experiments | 26 (EXP-001 to EXP-026) |
| Data pipeline | Daily cron (02:30 ET) |

---

## GitHub

| Repo | Visibility | Purpose |
|---|---|---|
| K25TOF/YOLO | Private | Autonomous trading application |
| K25TOF/yolo-firm | Private | Operating model documentation |
