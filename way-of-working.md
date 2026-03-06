# Way of Working

_Owner: Boardroom | Approved by: PO | Version: 1.0_

> Implementation detail (coding standards, CLI commands, Docker setup, secrets management)
> lives in Workshop's CLAUDE.md files. This document covers firm-level process only.

---

## Roles in Brief

| Role | Tool | Scope |
|---|---|---|
| PO (Kristof) | Any | Approves all changes, gatekeeper |
| Boardroom | Claude.ai | Strategy, stories, AC, documentation |
| Workshop | Claude Code (VPS) | Implementation, testing, deployment |
| Manager | Claude API (future) | Learning cycles, documentation |
| Analyst | Claude API (future) | Strategy research, hypothesis definition |
| Engineer | Claude API (future) | Backtesting, feasibility |

See `raci.md` for full responsibilities and segregation of duties.

---

## Story Lifecycle

Every piece of work — features, fixes, research tooling — follows the same flow:

```
DISCUSS → AGREE (AC) → BUILD → TEST → DEV → PO REVIEW → PRD
```

**DISCUSS (Boardroom + PO):**
- Boardroom challenges scope: can this be simpler? Is it really needed?
- 3-amigos: Boardroom, PO, and Workshop challenge requirements together
- Workshop challenges implementation: scope creep, YAGNI, architecture concerns

**AGREE:**
- Written AC agreed in Boardroom before any work starts
- Handoff to Workshop includes: context, big-picture dependencies, AC, constraints
- Workshop proposes implementation plan — PO approves before build starts

**BUILD → TEST → DEV:**
- Workshop creates feature branch off develop
- TDD/BDD: tests written first, code follows
- Workshop deploys to DEV, smoke test passes, Pushover notification sent to PO

**PO REVIEW:**
- PO reviews delivery summary against AC
- Approves or requests changes

**PRD:**
- PO says "Ship it" — develop merged to main, tagged, deployed
- Multiple approved stories can be batched into one release

Full implementation detail in `~/CLAUDE.md` (10 Commandments).

---

## Research Discipline

All strategy experiments follow this protocol:

1. **Hypothesis defined** — Analyst (or Boardroom) defines what is being tested and why
2. **Experiment scoped** — numbered EXP-NNN, added to `research-log.md` before running
3. **Isolation principle** — when comparing variants, examine only trades where variants diverge
4. **Results logged** — EXP entry updated with stats, observations, decisions
5. **Ideas captured** — any improvement ideas → `ideas.md` (IDEA-NNN)
6. **Strategies updated** — `strategies.json` updated if strategy added, modified, or retired

**Production readiness criteria for any strategy:**
- Minimum 30 trading days validated
- Win rate meets target threshold (TBD)
- Does not rely on outlier runners (guiding principle #6)
- PO approval required before any strategy goes live

Full research discipline in project `CLAUDE.md`.

---

## Session Close Routine

After every story delivery (Workshop) and every research cycle (Analyst, Engineer):

1. Self-check: did this session surface anything not in persistent memory or documentation?
2. If yes: flag to Manager with suggested update
3. Manager queues in PO review document
4. PO approves or rejects

**Agent context health:**
- Memory files reviewed after every PRD release
- Size cap and entry count thresholds defined in `kpis.md` (Layer 5)
- Housekeeping triggered when thresholds exceeded
- Redundant or stale entries proposed for removal, PO approves

---

## Change Management

**All changes require PO approval.** No exceptions.

| Change type | Process |
|---|---|
| Feature / fix | Story lifecycle (above) |
| Architecture decision | Boardroom scopes, PO approves, logged in DECISIONS.md |
| Firm document update | Boardroom authors, PO approves, pushed to yolo-firm repo |
| Agent memory update | Agent flags, Manager queues, PO approves |
| PRD deployment | PO explicit "Ship it" only |
| Live trading enablement | Full demo→live gate (see `risk-policy.md`) |
| API key rotation | Root (PO) only, logged in status-log.md |

---

## Agent Interaction Model (Phase 5+)

When Org Learning agents are active:

**Manager leads all sessions:**
- PO triggers cycle (manual for now, scheduled/event-driven later)
- Manager defines the question, time-boxes the cycle, owns token budget
- Manager addresses agents individually — no cross-talk
- Agents "raise hand" to contribute, Manager grants floor
- Manager writes concise session minutes after each cycle

**PO can:**
- Observe session log in real time
- Interrupt and contribute at any point
- Stop a cycle at any time

**Agents cannot:**
- Implement changes without PO approval
- Modify the production engine or deploy code
- Update their own persistent memory without PO approval

**Token efficiency:**
- No open-ended discussions — Manager defines question, agents respond concisely, Manager closes
- No background activity — agents only active when cycle is triggered
- Manager terminates cycles early if going in circles or burning tokens without progress

---

## Documentation Standards

| Document | Owned by | Updated when |
|---|---|---|
| `yolo-firm/*.md` | Boardroom | Any firm-level change, PO approves |
| `~/CLAUDE.md` | Workshop | Process or infrastructure changes |
| `projects/yolo/CLAUDE.md` | Workshop | Project-specific API or architecture changes |
| `DECISIONS.md` | Workshop | Any architectural decision |
| `GLOSSARY.md` | Workshop | New terms or status changes |
| `research-log.md` | Analyst / Engineer | Every experiment |
| `status-log.md` | Workshop | Every significant action |
| `changelog.md` | Workshop | Every PRD release |

**Rules:**
- Concise over comprehensive — bullet points, not paragraphs
- Update docs as part of the story, not as an afterthought
- No duplication between documents — cross-reference instead
