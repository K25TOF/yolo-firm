# YOLO Org Learning — Agent Definitions

_Owner: Boardroom | Approved by: PO | Version: 1.0_

---

## Purpose

YOLO's Org Learning department consists of six specialised agents that form a virtual research team. They investigate strategy improvements, run experiments, challenge findings, and check external literature — all under PO authority.

No agent can approve changes, deploy code, or modify production systems. Every output routes through PO for approval.

---

## Agents

| Agent | Role | Tools | Key constraint |
|---|---|---|---|
| **Manager** | SPOC, data execution, session facilitator | run_backtest, update_memory | Cannot approve — only routes to PO |
| **Optimist** | Finds alternative angles, never accepts defeat | update_memory | Cannot run backtests or access data directly |
| **Challenger** | Demands evidence, finds errors, checks lookahead bias | update_memory | Cannot run backtests or access data directly |
| **Statistician** | Sample sizes, CIs, multiple comparison correction | update_memory | Cannot run backtests; flags as [STAT FLAG] |
| **Execution Realist** | Execution feasibility, price reality, stack constraints | update_memory | Cannot run backtests; flags as [EXEC FLAG] |
| **Scout** | External literature search via web | web_search, update_memory | Cannot run backtests; only agent with web access |

---

## Agent Boundaries

### What agents CAN do

- Manager: orchestrate sessions, run backtests, execute data tasks, write minutes, flag items for PO review
- Optimist: propose alternative angles, find unexplored hypotheses, challenge premature conclusions, recommend strategy directions
- Challenger: demand evidence for claims, find errors in methodology, check for lookahead bias, identify data quality issues
- Statistician: calculate sample sizes, confidence intervals, flag multiple comparison issues, assess statistical significance
- Execution Realist: assess execution feasibility, flag latency/slippage issues, check entry price reality against stack constraints
- Scout: search external academic and practitioner literature, report findings with citations, flag contradictions with internal research

### What agents CANNOT do

- Approve strategy changes, code changes, or capital decisions
- Modify production engine or deploy code
- Write to another agent's memory (identity enforcement)
- Operate without PO triggering the cycle
- Communicate directly with each other — Manager mediates all interaction
- Access data or run backtests directly (Optimist/Challenger) — Manager is the sole data executor

---

## Session Protocol

### 1. Trigger

PO triggers a learning cycle with a question or objective. No agent operates without a trigger.

### 2. Setup (Manager)

Manager defines:
- The question being investigated
- Time-box and turn limit
- Which agents are needed
- Expected outcome format

### 3. Execution (Manager-led)

- Manager addresses agents one at a time — strict turn-taking
- Both Optimist and Challenger must be invoked in every session — no exceptions
- Manager injects full data context into every routing message (agents have no memory of prior turns)
- No cross-talk between Optimist and Challenger
- Manager can redirect, challenge, or terminate at any point
- If agents reach impasse, Manager terminates and escalates to PO

### 4. Close (Manager)

Manager writes session minutes:
- **Question asked:** What were we investigating?
- **Key contributions:** What did each agent provide?
- **Decision/outcome:** What was concluded?
- **Next action:** What happens next?
- **Memory updates:** Any flagged updates for PO approval

### 5. Review (PO)

PO reviews session minutes and:
- Approves or rejects proposed strategy changes
- Approves or rejects memory updates
- Approves or rejects engine extension stories
- May trigger follow-up cycles

---

## Context Loading

Each agent loads a specific set of documents at session start, defined in their `context-manifest.md`. Documents come from two sources:

- **Firm documents:** `yolo-firm/*.md` — strategy, process, compliance
- **Research documents:** `yolo/analysis/research/` — experiment logs, strategies, ideas

Context manifests use file paths relative to their source repo root for programmatic loading.

---

## Memory Protocol

Each agent has persistent memory that accumulates over sessions.

### Auto-Memory (update_memory tool)

Agents can write to their own memory file directly using the `update_memory` tool during sessions. Identity is enforced — an agent can only write to its own memory file.

### Rules

- Each agent can only write to its own `memory.md` via `update_memory`
- Memory is concise — bullet points, not paragraphs
- The tool replaces the entire file — agents must include all existing content they want to keep
- Memory files are reviewed after every PRD release

### Memory files

| Agent | File |
|---|---|
| Manager | `agents/manager/memory.md` |
| Optimist | `agents/optimist/memory.md` |
| Challenger | `agents/challenger/memory.md` |
| Statistician | `agents/statistician/memory.md` |
| Execution Realist | `agents/execution-realist/memory.md` |
| Scout | `agents/scout/memory.md` |

---

## File Structure

```
agents/                         # Agent definitions + framework code
  README.md                     # This file
  manager/
    system-prompt.md            # LLM system prompt — injected at session start
    context-manifest.md         # Documents loaded into context
    memory.md                   # Persistent memory
  optimist/                     # Same 3-file pattern
  challenger/
  statistician/
  execution-realist/
    constraints.md              # Living reference doc (stack constraints)
  scout/
  _retired/                     # Archived agent definitions (analyst, engineer)

research/                       # Research outputs (separate from agent definitions)
  session-log/                  # Session execution logs + index.json
  reviews/                      # Post-session PO review documents
  briefs/                       # Research audit briefs and plans
  reports/                      # Manager-authored research reports
```

---

## Escalation Path

```
Agent flags issue → Manager queues → PO reviews → PO decides
```

No shortcuts. No agent bypasses Manager. No Manager bypasses PO.
