# Compliance

_Owner: Boardroom | Approved by: PO | Version: 1.0_

---

## Trading Rules (Non-Negotiable)

| Rule | Status |
|---|---|
| Long only — no short selling | Enforced (current implementation) |
| No leveraged instruments | Policy — never trade leveraged products |
| No overnight positions | Enforced (force_close_eod = True) |
| RTH only (09:30–16:00 ET) | RTH enforced by TraderService market hours safety rail and backtester data walk |
| No trading outside RTH | Requires explicit PO approval to change |
| Demo account for all testing | Enforced (.env.dev always T212_ENV=demo) |
| Real money requires demo gate | See Demo → Live Gate below |

---

## Demo → Live Gate

Real capital deployment is **blocked** until ALL conditions are met:

| Gate | Requirement | Status |
|---|---|---|
| 1 | Strategy validated ≥ 30 trading days in demo | 🔲 Not started |
| 2 | Win rate ≥ target threshold (TBD) | 🔲 Target not set |
| 3 | Max drawdown within risk policy limits | 🔲 Limits not set |
| 4 | Full IT security hardening complete | 🔲 Basic only |
| 5 | Capital policy formally approved by PO | 🔲 Placeholder |
| 6 | Incident management procedures tested | 🔲 Not tested |
| 7 | Explicit PO approval to flip T212_ENV=live | 🔲 Not approved |

**The flip to live trading is a named, standalone release step — never bundled into a feature story.**

---

## Environment Rules

| Environment | T212_ENV | Trades against | Who can change |
|---|---|---|---|
| DEV (.env.dev) | demo | Paper account — permanent | Never change |
| PRD (.env.prd) | demo | Paper account — until gate passed | PO only |
| PRD (live) | live | **Real money** | PO explicit approval only |

DEMO and LIVE require **separate** API key pairs generated from the matching T212 environment.

---

## API Usage Rules

- T212 API: never exceed rate limits (see project CLAUDE.md for limits per endpoint)
- Polygon.io: respect tier limits; batch requests where possible
- Anthropic API: LLM components are optional and degrade gracefully — never block trading on LLM availability
- All API keys: age-encrypted at rest, root-only access for PRD

---

## Data & Privacy

- No personal data stored beyond what T212/Polygon return in API responses
- Trade history stored locally in SQLite (JournalService) — not transmitted externally
- No third-party analytics, tracking, or logging services
- VPS is single-tenant (personal project) — no multi-user data concerns

---

## Change Compliance

Any change to live trading parameters requires PO approval:
- Strategy config changes (entry/exit rules, thresholds)
- Safety rail configuration
- Position limits
- Session hours
- T212 environment (demo → live)

No automated system may change these without a scoped story and PO sign-off.

---

## Audit Trail

All decisions traceable via:
- `DECISIONS.md` — architectural decisions
- `research-log.md` — experiment decisions
- `status-log.md` — operational decisions
- `docs/changelog.md` — release decisions
- `yolo-firm/` repo commit history — firm document changes (PO-approved)
