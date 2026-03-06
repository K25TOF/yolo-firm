# Capital Policy

_Owner: Boardroom | Approved by: PO | Version: 1.0 — PLACEHOLDER_

> This document is a placeholder. All values marked TBD must be defined and
> PO-approved before any real capital is deployed. The Demo → Live Gate in
> `compliance.md` blocks live trading until this policy is complete.

---

## Capital Allocation (TBD)

| Parameter | Value | Notes |
|---|---|---|
| Starting capital | TBD | Initial live trading allocation |
| Max capital at risk per trade | TBD | % of total capital |
| Max capital at risk per day | TBD | % of total capital |
| Max simultaneous positions | TBD | Absolute number |
| Capital reserve (untradeable) | TBD | % kept in cash always |

---

## Position Sizing (TBD)

Position sizing logic not yet implemented. Options under consideration:

| Method | Description | Status |
|---|---|---|
| Fixed fractional | Fixed % of capital per trade | Candidate |
| Kelly Criterion | f* = (bp-q)/b based on recent WR and R:R | Candidate (half-Kelly) |
| Fixed size | Same £ amount per trade | Simple baseline |

Decision deferred until strategy is validated and baseline WR/R:R established.

---

## Growth & Reinvestment (TBD)

| Rule | Value |
|---|---|
| Profit reinvestment | TBD |
| Capital withdrawal trigger | TBD |
| Capital increase approval | PO only |
| Capital decrease / withdrawal | PO only |

---

## Drawdown Response (TBD)

| Drawdown level | Action |
|---|---|
| X% daily | Pause trading, notify PO |
| X% weekly | Stop all trading, PO review |
| X% monthly | Full strategy review, capital reassessment |
| X% total | Stop all trading, return to demo |

---

## Review Cadence

Capital policy reviewed:
- After every PRD release
- After any significant drawdown event
- At minimum: monthly once live trading begins
