# Session: orb-feedback-analysis
_Date: 2026-03-24 21:19 UTC | Agent: manager | Model: claude-sonnet-4-6_

## Context loaded
- raci.md
- way-of-working.md
- strategy-roadmap.md
- kpis.md
- architecture.md
- risk-policy.md
- compliance.md
- costs.md
- analysis/research/ideas.md
- agents/README.md
- agents/manager/memory.md

## Exchange

**Manager:** PO has triggered a research session.

Question: LC-2025-014 — PO Feedback on 128 Confirmed ORB Entries

RESEARCH QUESTION: What separates Good from Bad entries, and how can the signal be refined?

DATA CONTEXT:

G/N/B DISTRIBUTION (all 128 rated):
  Good:    69 (53.9%)
  Neutral: 18 (14.1%)
  Bad:     41 (32.0%)

ENTRY TIME BY RATING:
  Good:    median 10:05 ET, 42% before 10:00
  Bad:     median 10:31 ET, 22% before 10:00
  Neutral: median 10:14 ET, 33% before 10:00

VOLUME RATIO AT ENTRY:
  Good:    median 3.9x
  Bad:     median 3.1x
  Neutral: median 2.8x

BAD-RATED BREAKDOWN (41 total):
  Wrong/strange entry marker: 7 — PO says the BUY marker doesn't match where the breakout actually is
  Robotic/algorithmic pattern: 4 — stocks with anomalous candle patterns (CIGL, UFG, BCDA, TOPP)
  Fakeout: 1 (DFLI)
  Low volume: 2
  Real breakout was later: 4 — script caught a false ORB break, real one came later
  No reason given: 24

GOOD-RATED HIGHLIGHTS:
  17 explicitly called 'excellent' or 'perfect'
  PO noted 'follow-on ORB' concept (OPAD) — second breakout on more volume after first entry
  PRLD: 'creeping above ORB on little volume but then taking off steep on massive volume' — noted 15:20 as better entry

INVESTIGATION FLAGS (entry marker placement issues):
  MSW 2025-07-14: 'doesnt match the rule we agreed'
  BETR 2025-09-22: 'buy position doesnt make sense'
  TVRD 2025-10-13: 'strange buy position - why?'
  LGO 2025-10-15: 'ORB breakout is around 9:56 (1.26) - why is the marker in wrong place?'
  GRAN 2026-02-24: 'strange buy position during heavy downtrend'
  ALDX 2026-03-17: 'entry is actually not bad but flagging for investigation why marker is here and not earlier'

KEY OBSERVATIONS:
1. 54% Good rate is strong for an out-of-sample test (training set was 22 PO-rated)
2. Good stocks enter 26 min earlier than Bad (10:05 vs 10:31)
3. Good stocks have higher VR at entry (3.9x vs 3.1x)
4. 7/41 Bad entries may be script bugs (wrong marker placement) — could flip to Good/Neutral if fixed
5. 4/41 Bad are 'robotic patterns' — anomalous stocks that should be excluded from universe
6. 24/41 Bad have no comment — we don't know why they're bad

Optimist — what signal refinements would improve the Good rate? Which Bad categories are filterable?
Challenger — is 54% Good rate meaningful on n=128 out-of-sample? What are the risks of refining based on this feedback?

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** ## 3 Amigos Confirmation

**My understanding:** PO has provided structured feedback on 128 out-of-sample ORB (Opening Range Breakout) entries rated Good/Neutral/Bad. The question is what separates Good from Bad entries and how the signal can be refined. This is a qualitative analysis session — no new backtests are required unless agents identify a specific testable hypothesis that warrants one.

**I will:**
- Open session LC-2025-014 with defined scope and time-box
- Consult Optimist on signal refinement opportunities from the data patterns
- Consult Challenger on statistical validity and overfitting risk
- Synthesise findings and route conclusions to PO
- Write session minutes and flag memory updates

**I will NOT:**
- Run backtests unless a specific, well-scoped hypothesis emerges that both agents agree warrants testing within this session
- Approve any signal changes or strategy updates — all proposals route to PO
- Pursue the "24 Bad with no comment" gap as a blocker — we work with what we have

**Success looks like:**
- A ranked list of filterable Bad categories with estimated improvement to Good rate
- A clear statistical assessment of whether 54% on n=128 is meaningful
- At least one concrete, testable refinement hypothesis ready for PO approval
- Session minutes with memory update candidates

**Confirm to proceed?**

---
