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
| Manager | Claude API | Learning cycles, data execution, documentation |
| Optimist | Claude API | Alternative angles, hypothesis refinement |
| Challenger | Claude API | Evidence demands, bias checks, methodology audit |

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

## Research Session Types

**Solo sessions** (Manager only): permitted for pure data retrieval with no interpretation. Output is raw counts/tables only — no recommendations, no priority rankings, no population comparisons.

**Multi-agent sessions** (Challenger + Statistician mandatory): required when output includes priority rankings, strategic recommendations, population comparisons, conclusions about signal quality, or any finding that informs the research plan. The moment Manager writes a sentence recommending an action or ranking a priority, Challenger and Statistician must be invoked in the same session.

---

## Research Discipline

All strategy experiments follow this protocol:

1. **Hypothesis defined** — Optimist (or Boardroom) defines what is being tested and why
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

## Chart Viewer Review Policy

The chart viewer at `http://72.61.203.132:8050` is the human-AI collaboration
interface for visual research review. All agents follow these rules:

**Lists:** Manager creates lists in `analysis/tools/lists/` named
`{research_id}_{description}_v{n}.json`. Multiple parallel lists are permitted.
Never overwrite an active list — increment the version number.
Existing lists (`trades.json`, `runners.json`) are grandfathered.

**List immutability:** A list with PO feedback is frozen. Once
`feedback/{list_name}.json` exists, the corresponding list must never be
regenerated, overwritten, or deleted. Improved logic must produce a new
versioned list (`_v2.json`). No exceptions.

**Feedback:** Manager owns and commits feedback files in
`analysis/tools/feedback/`. Feedback is never deleted.

**Traceability:** Every new list references its research task ID. Anyone can
trace list → feedback → research task without asking.

---

## Session Close Routine

After every story delivery (Workshop) and every research cycle (Optimist, Challenger):

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

## Agent Interaction Model

When Org Learning agents are active:

**Manager leads all sessions:**
- PO triggers cycle (manual for now, scheduled/event-driven later)
- Manager defines the question, time-boxes the cycle, owns token budget
- Manager addresses agents individually — no cross-talk
- Both Optimist and Challenger must be invoked in every session — non-negotiable
- Manager is the sole executor of data tasks (backtests, data queries) — agents analyse results
- Manager injects full data context into every routing message (agents have no memory of prior turns)
- Manager writes concise session minutes after each cycle

**Session close — autonomous:**
- After both agents have responded, Manager synthesises findings (3-5 bullets)
- Lists FLAG FOR CONTEXT items, asks each agent for final flags
- Updates context files and closes — does not wait for further instructions

**PO can:**
- Observe session log in real time
- Interrupt and contribute at any point
- Stop a cycle at any time

**Agents cannot:**
- Implement changes without PO approval
- Modify the production engine or deploy code
- Access data or run backtests directly — Manager provides curated data packages
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
| `research-log.md` | Manager | Every experiment |
| `status-log.md` | Workshop | Every significant action |
| `changelog.md` | Workshop | Every PRD release |

**Rules:**
- Concise over comprehensive — bullet points, not paragraphs
- Update docs as part of the story, not as an afterthought
- No duplication between documents — cross-reference instead
