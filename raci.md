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

### Analyst (Claude API — future)
Trading specialist. Defines hypotheses, audits backtest results, self-educates via book knowledge base. Does not run backtests or write code. Raises hand to Manager when contributing.

### Engineer (Claude API — future)
Runs backtests using the engine. Writes one-off prototype scripts when engine cannot support a hypothesis. Proposes engine changes via story scope when prototypes prove value. Does not modify the production engine or deploy code.

### Workshop (Claude Code — VPS)
Implements all stories. Owns codebase, TDD/BDD discipline, git branching, Docker. Delivers against agreed AC. Never deploys to PRD without PO approval. Performs session close self-check after each story delivery.

---

## RACI Matrix

| Activity | PO | Boardroom | Manager | Analyst | Engineer | Workshop |
|---|---|---|---|---|---|---|
| Define vision & strategy | A | R | I | I | I | I |
| Approve story AC | A | R | I | — | — | C |
| Implement stories | I | — | — | — | — | R/A |
| Deploy to PRD | A | — | — | — | — | R |
| Initiate learning cycle | A | — | R | I | I | — |
| Define hypothesis | I | — | C | R/A | — | — |
| Run backtest | I | — | C | C | R/A | — |
| Audit backtest results | I | — | C | R/A | — | — |
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
| Strategy research vs live execution | Analyst/Engineer (research) vs Workshop/pipeline (execution) |
| Code change vs deployment approval | Workshop (implements) vs PO (approves PRD) |
| Hypothesis vs audit | Analyst defines, Engineer runs, Analyst audits — no self-auditing |
| Document authoring vs approval | Boardroom authors, PO approves all changes |
| Agent memory vs updates | Agents flag candidates, PO approves all memory changes |

---

## Session Close Routine

After every story delivery (Workshop) and every research cycle (Analyst, Engineer):

1. Self-check: did this session surface anything not already in persistent memory or documentation?
2. If yes: flag to Manager with suggested memory update
3. Manager queues in PO review document
4. PO approves or rejects

This prevents knowledge rot between sessions.
