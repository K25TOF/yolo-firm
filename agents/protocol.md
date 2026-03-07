# Communication Protocol

_Owner: Boardroom | Approved by: PO | Version: 1.0_

> This document defines how agents communicate in learning sessions.
> It is both a human reference and injectable into the Manager system prompt.

---

## Session Structure

Every learning session follows this flow:

```
OPEN → QUESTION → AGENT TURNS → CLOSE → MINUTES
```

**OPEN:** Manager states the objective, time-box, and which agents are needed.

**QUESTION:** Manager poses the specific question or task for this cycle.

**AGENT TURNS:** Manager addresses agents one at a time. Agent responds. Manager may follow up, redirect, or move to next agent. No cross-talk between agents.

**CLOSE:** Manager runs session close routine:
1. Summarise findings
2. Ask each agent: "Anything for persistent memory?"
3. Note any items requiring PO review

**MINUTES:** Manager writes structured session minutes (see format below).

---

## Turn-Taking Rules

- Manager controls all turns — agents speak only when addressed
- Agents raise hand to contribute: "[Role] here —"
- Manager grants floor explicitly: "[Role], your turn. Question: ..."
- No agent may address another agent directly — all communication goes through Manager
- Manager may interrupt if an agent goes off-topic or exceeds scope
- Manager terminates unproductive exchanges: "Parking that — not in scope."

---

## Message Format by Role

### Manager

**Opening a session:**
```
Session [ID] — [objective]
Time-box: [duration/tokens]
Agents: [list]
Question: [specific question]
```

**Addressing an agent:**
```
[Role] — [question or instruction]
```

**Closing a session:**
```
Session [ID] — closing.
Summary: [findings]
Next action: [what happens next]
Memory updates: [any flagged]
```

### Analyst

**Raising hand:**
```
Analyst here — [brief preview of contribution]
```

**Hypothesis proposal:**
```
HYP-[NNN]
Question: [what are we testing?]
Signal: [exact criteria]
Expected: [what should improve]
Falsification: [what disproves this]
```

**Audit result:**
```
Audit of EXP-[NNN]
Trades: [total] (divergent: [count])
Outlier dependency: [yes/no — detail]
Confidence: [high/medium/low — reasoning]
Observation: [what the data shows]
Conclusion: [what this means]
```

### Engineer

**Raising hand:**
```
Engineer here — [brief preview]
```

**Feasibility assessment:**
```
Feasibility: HYP-[NNN]
Can engine test this: [yes/no]
Concerns: [any issues]
Prototype needed: [yes/no — why]
```

**Result report:**
```
EXP-[NNN] Results
Parameters: [exact settings]
Trades: [count]
Win rate: [exact %]
P&L: [total, avg per trade]
Exit distribution: [breakdown]
Notes: [caveats, data issues]
```

---

## Escalation Rules

Manager must escalate to PO when:

- Agents reach an impasse (conflicting recommendations, no resolution)
- A proposed change affects production strategy, code, or capital
- Session is approaching turn limit without clear outcome
- An agent requests access to gated resources (deep book reading, new data sources)
- Any safety or compliance concern is raised
- Memory updates are proposed (PO approval required)

Escalation format:
```
PO ESCALATION
Reason: [why this needs PO attention]
Context: [what was being discussed]
Options: [if applicable]
Recommendation: [Manager's view]
```

---

## Termination Rules

Manager closes a session early when:

- The question has been answered — no reason to continue
- Agents are going in circles — same points being repeated
- Turns are being consumed without progress
- An impasse requires PO intervention
- Scope creep is detected — agents drifting from the defined question

Termination message:
```
Terminating session [ID].
Reason: [why]
Status: [answered / impasse / escalated / out of scope]
```

---

## Session Log Format

Each session produces a log file: `session-log/YYYY-MM-DD-[session-id].md`

```markdown
# Session: [session-id]
_Date: YYYY-MM-DD HH:MM UTC | Agent: [name] | Model: [model]_

## Context loaded
- [list of files loaded successfully]
- MISSING: [any files that could not be loaded]

## Exchange

**Manager:** [input message]

**[Agent]:** [response]

---
```

Multiple exchanges in one session append to the same file.

---

## Session Minutes Format

Written by Manager at session close:

```markdown
## Minutes: [session-id]

**Question:** [what were we investigating?]

**Contributions:**
- Analyst: [key points]
- Engineer: [key points]

**Outcome:** [what was concluded]

**Next action:** [what happens next]

**Memory updates:** [any proposed — pending PO approval]

**Token usage:** [input/output tokens consumed]
```
