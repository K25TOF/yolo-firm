# Risk Policy

_Owner: Boardroom | Approved by: PO | Version: 1.0_

---

## Principles

- Capital preservation takes priority over profit maximisation
- Hard limits are non-negotiable — no overrides without PO approval
- Demo mode must be validated before any real capital is deployed
- All risk parameters reviewed after each PRD release

---

## Position Limits (Placeholder — to be set before live trading)

| Parameter | Current | Notes |
|---|---|---|
| Max open positions | TBD | Simultaneous holdings |
| Max position size | TBD | % of total capital per trade |
| Max daily capital at risk | TBD | % of capital exposed intraday |
| Min price | $0.20 | Scanner filter (active) |
| Max price | TBD | Scanner filter |

---

## Drawdown Triggers (Placeholder)

| Trigger | Action |
|---|---|
| Daily loss > X% | Pause trading, notify PO |
| Weekly loss > X% | Stop all trading, PO review required |
| Consecutive losses > N | Reduce position size or pause |
| Monthly drawdown > X% | Full strategy review |

---

## Kill Switch

- Manual: PO can stop pipeline at any time via CLI (`yolo stop`)
- Automatic: daily loss limit breach triggers automatic pause
- All open positions closed at EOD regardless (force_close_eod = True)
- No overnight positions (current design — RTH only)

---

## Demo → Live Gate

Real capital deployment requires ALL of the following:
1. Strategy validated over minimum 30 trading days in demo
2. Win rate ≥ target threshold (TBD)
3. Max drawdown within policy limits
4. Full security hardening completed
5. Capital policy formally approved by PO
6. Incident management procedures tested

---

## Compliance Rules

- No leveraged instruments
- No short selling (current implementation — long only)
- No overnight positions
- No trading outside RTH without explicit PO approval
- T212 demo account used for all testing
- Real money account accessed only after demo gate passed
- All API keys age-encrypted, root-only access for PRD secrets

---

## IT Security (Basic — v1.0)

- VPS access: SSH key only, no password login
- Secrets: age-encrypted `.env.prd`, root-only read access
- Dev secrets: `.env.dev`, claude user access
- No secrets in git history — `.env*` in `.gitignore`
- GitHub repos: private under K25TOF org
- PRD deployments: root only
- API keys rotated if any suspected exposure

_Note: Full IT security department planned as future phase._
