# YOLO Org Learning — Agent Definitions

_Owner: Boardroom | Approved by: PO | Version: 1.0_

---

## Purpose

YOLO's Org Learning department consists of three specialised agents that form a virtual research team. They investigate strategy improvements, run experiments, and propose changes — all under PO authority.

No agent can approve changes, deploy code, or modify production systems. Every output routes through PO for approval.

---

## Agents

| Agent | Role | Model | Key constraint |
|---|---|---|---|
| **Manager** | Session orchestrator, facilitator, gatekeeper | Haiku 4.5 | Cannot approve — only routes to PO |
| **Analyst** | Hypothesis definition, result auditing, idea generation | Haiku 4.5 | Cannot run backtests or write code |
| **Engineer** | Backtest execution, prototyping, technical assessment | Haiku 4.5 | Cannot interpret strategy quality |

---

## Agent Boundaries

### What agents CAN do

- Manager: orchestrate sessions, write minutes, flag items for PO review
- Analyst: define hypotheses, audit results (not own), generate ideas, recommend strategy changes
- Engineer: run backtests, write prototype scripts, challenge feasibility, propose engine stories

### What agents CANNOT do

- Approve strategy changes, code changes, or capital decisions
- Modify production engine or deploy code
- Update their own persistent memory without PO approval
- Self-audit (Analyst cannot audit results from own hypotheses)
- Operate without PO triggering the cycle
- Exceed token budget for a cycle
- Communicate directly with each other — Manager mediates all interaction

---

## Session Protocol

### 1. Trigger

PO triggers a learning cycle with a question or objective. No agent operates without a trigger.

### 2. Setup (Manager)

Manager defines:
- The question being investigated
- Time-box and token budget
- Which agents are needed
- Expected outcome format

### 3. Execution (Manager-led)

- Manager addresses agents one at a time — strict turn-taking
- Agents raise hand to contribute — Manager grants floor
- No cross-talk between Analyst and Engineer
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

### Update flow

1. Agent flags a memory update candidate during session close
2. Manager queues the update in session minutes
3. PO reviews and approves or rejects
4. Approved updates are written to the agent's memory file

### Rules

- Agents cannot update their own memory without PO approval
- Memory is concise — bullet points, not paragraphs
- Stale or redundant entries are proposed for removal during session close
- Memory files are reviewed after every PRD release

### Memory files

| Agent | File |
|---|---|
| Manager | `agents/manager/memory-template.md` |
| Analyst | `agents/analyst/memory-template.md` |
| Engineer | `agents/engineer/memory-template.md` |

---

## File Structure

```
agents/
  README.md                     # This file
  manager/
    system-prompt.md            # LLM system prompt — injected at session start
    context-manifest.md         # Documents loaded into context
    memory-template.md          # Persistent memory (PO-approved updates)
  analyst/
    system-prompt.md
    context-manifest.md
    memory-template.md
  engineer/
    system-prompt.md
    context-manifest.md
    memory-template.md
```

---

## Escalation Path

```
Agent flags issue → Manager queues → PO reviews → PO decides
```

No shortcuts. No agent bypasses Manager. No Manager bypasses PO.
