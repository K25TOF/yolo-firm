# RACI — Roles, Responsibilities & Accountability

_Owner: Boardroom | Approved by: PO | Version: 1.0_

---

## Roles

### PO (Kristof)
The firm's owner and sole decision-maker. Final approval on all changes, capital deployment, strategy, and agent memory updates. Acts as gatekeeper for all transitions from research to live trading.

### Boardroom (Claude.ai)
Strategic advisor and operating model owner. Defines stories, agrees AC, maintains all firm documentation, shapes vision and roadmap. Does not execute code or deploy.

### Manager (Claude API — future)
Orchestrates learning cycles. Owns token budget, session minutes, decision log, idea log, and all agent documentation. Initiates research cycles on PO trigger. Routes proposals to PO review. Runs session close routine after every cycle.

### Optimist (Claude API)
Finds alternative angles, never accepts defeat. Proposes unexplored hypotheses, challenges premature conclusions, suggests refinements. Does not run backtests or access data directly — receives curated data packages from Manager.

### Challenger (Claude API)
Demands evidence, finds errors, checks for lookahead bias. Audits methodology, identifies data quality issues, enforces statistical rigour. Does not run backtests or access data directly — receives curated data packages from Manager.

### Workshop (Claude Code — VPS)
Implements all stories. Owns codebase, TDD/BDD discipline, git branching, Docker. Delivers against agreed AC. Never deploys to PRD without PO approval. Performs session close self-check after each story delivery.

---

## RACI Matrix

| Activity | PO | Boardroom | Manager | Optimist | Challenger | Workshop |
|---|---|---|---|---|---|---|
| Define vision & strategy | A | R | I | I | I | I |
| Approve story AC | A | R | I | — | — | C |
| Implement stories | I | — | — | — | — | R/A |
| Deploy to PRD | A | — | — | — | — | R |
| Initiate learning cycle | A | — | R | I | I | — |
| Define hypothesis | I | — | C | R | C | — |
| Run backtest | I | — | R/A | — | — | — |
| Audit backtest results | I | — | C | C | R/A | — |
| Propose strategy change | A | — | R | C | C | — |
| Approve memory updates | A | — | C | — | — | — |
| Maintain firm documents | A | R | C | — | — | — |
| Session close routine | I | — | R | C | C | C |
| Capital deployment | A/R | — | — | — | — | — |
| IT security & secrets | A/R | — | — | — | — | — |

_R=Responsible, A=Accountable, C=Consulted, I=Informed_

---

## Segregation of Duties

| Concern | Separation |
|---|---|
| Strategy research vs live execution | Optimist/Challenger (research) vs Workshop/pipeline (execution) |
| Code change vs deployment approval | Workshop (implements) vs PO (approves PRD) |
| Hypothesis vs audit | Optimist proposes, Challenger audits — separated by design |
| Data execution vs analysis | Manager runs backtests, Optimist/Challenger analyse results |
| Document authoring vs approval | Boardroom authors, PO approves all changes |
| Agent memory vs updates | Agents flag candidates, PO approves all memory changes |

---

## Session Close Routine

After every story delivery (Workshop) and every research cycle (Optimist, Challenger):

1. Self-check: did this session surface anything not already in persistent memory or documentation?
2. If yes: flag to Manager with suggested memory update
3. Manager queues in PO review document
4. PO approves or rejects

This prevents knowledge rot between sessions.
