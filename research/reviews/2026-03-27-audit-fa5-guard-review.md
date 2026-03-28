# Session Review: audit-fa5-guard
_Date: 2026-03-27 18:54 UTC | Model: claude-sonnet-4-6_

## Manager Synthesis

## Session Close — LC-2025-015

Both agents have completed their final flags. I now have everything needed to close.

---

## Session Minutes — LC-2025-015

**Session ID:** LC-2025-015
**Focus area:** 5 — Decline Window and Guard Logic (Phases 3e–3k)
**Status:** COMPLETE

---

### Question asked
Do the decline window detection and RSI guard logic (Phases 3e–3k) produce robust, reliable signals — or are the results artefacts of small samples, wick-based measurement inflation, and untested parameter assumptions?

---

### Key contributions

**Optimist:**
- Identified wick inflation as a material gap — 41.59pp mean improvement is measured against an unreachable benchmark; close-based rerun is P1
- Flagged outcome-selection bias in cluster design (49 worst trades, sorted by magnitude)
- Correctly diagnosed "0 hurt" as a low-trigger-rate artefact, not evidence of safety
- Proposed RSI threshold sweep (35/38/40/43/45) and full 3,664-graduate application as P1 tests
- Final flag: Guard C asymmetry hypothesis (works in catastrophic regime, harmful in moderate regime); 9 RSI non-firers may be grinder-profile losers; 16 window-too-short trades may be signal-selection failures not window-length failures

**Challenger:**
- Identified four potential blocking issues: (a) peak as decision input vs benchmark — needs confirmation; (b) d3 selected in-sample on same 49-trade set — design-subset contamination; (c) e5/c1 parameters undefined and selection method unknown; (d) RSI<40 possibly reverse-engineered from outcomes
- Strengthened "0 hurt" critique: 49/237 harmed in 20–50pp cluster directly contradicts the safe-guard narrative
- Flagged: trigger count vs improvement count unresolved (14/49 improved ≠ 14/49 triggered)
- Corrected Optimist: "catastrophic decline guarantees RSI<40" is contradicted by the 9 non-firers within the >50pp cluster — do not treat as established mechanism
- Flagged: no time-based holdout anywhere in Focus Area 5 — all splits are outcome-sorted, not date-sorted; 10–20pp cluster (size unreported) is the best available near-OOS test bed

---

### Decision / outcome

**Overall verdict: DOUBT — research is incomplete, not invalidated.**

| Sub-Q | Verdict | Primary reason |
|---|---|---|
| 5a — Wick inflation | DOUBT | Per-trade distribution absent; outlier check not applied |
| 5b — Cluster cutoffs | DOUBT | Arbitrary cutoffs; 10–20pp unreported; outcome-selection bias |
| 5c — 1m_e5_c1 robustness | DOUBT | e5/c1 undefined; selection pressure unknown; untested on full population |
| 5d — Guard C sample | DOUBT | "0 hurt" tautological; 49/237 harmed in adjacent cluster; trigger vs improvement conflated |
| 5e — Window / RSI non-firers | FLAG | Window length provenance unknown; d3/RSI cross-check missing |
| 5f — 20–50pp failures | FLAG | 40/49 hurt trades unclassified; no RSI sweep; no threshold justification |

---

### Next actions (for PO review)

**Blocking — must resolve before any claim can stand:**
1. Confirm `bar_high` peak is used only as measurement baseline, never as a decision input
2. Confirm whether d3 was selected from d1–d5 on the same 49 trades used in all downstream analysis — if yes, flag as design-subset contamination
3. Define e5 and c1 parameters; document how many variants were tested in Phase 3i and how the winner was selected
4. Confirm when RSI<40 was chosen relative to examining the 49-trade outcomes; document the threshold selection process
5. Resolve trigger count vs improvement count for Guard C: of the 49 >50pp trades, how many triggered RSI<40? Of those, how many improved?

**High priority — required to cite any figures:**

6. Per-trade improvement distribution for the 41.59pp mean: min, max, median, top-3 contribution
7. Apply Guard C and 1m_e5_c1 to all 3,664 graduates — trigger rate, mean delta, false exit rate per cluster
8. Report 10–20pp cluster size and evaluate all three signals there first (best near-OOS evidence available)

**Medium priority:**

9. RSI threshold sweep (35/38/40/43/45) on both clusters — results must be held-out validated, not in-sample optimised
10. Full classification of 49 hurt trades in 20–50pp cluster (not just 9 FP)
11. For 9 RSI non-firers: did d3 fire? For 16 window-too-short: cross-check whether any current signal fires within existing window before concluding extension is needed

---

### New ideas flagged (for ideas.md — PO approval required)

- **IDEA-027:** RSI threshold as continuous parameter — sweep 35–50 in 1pp increments on full 3,664 graduate population; report trigger rate, improvement rate, harm rate, net pp delta per threshold
- **IDEA-028:** Close-based peak as primary measurement in all decline window analyses; wick-based retained as theoretical ceiling only, never cited as achievement benchmark

---

### Memory updates flagged (for PO approval)

**Manager memory — proposed additions:**
- LC-2025-015 session summary: Focus Area 5 verdict = DOUBT. Guard C asymmetry pattern (works in >50pp catastrophic regime, harms 20–50pp moderate regime). Full signal stack (d3 + 1m_e5_c1 + Guard C) potentially all designed on same 49-trade set — design-subset contamination risk unresolved. No time-based holdout in Focus Area 5. 10–20pp cluster is best near-OOS test bed but size unreported. 9 RSI non-firers in >50pp cluster contradict "catastrophic decline guarantees RSI<40" — do not treat as established mechanism.
- Key correction: trigger count ≠ improvement count; 14/49 improved does not establish Guard C precision — trigger denominator unknown.

---

=== SESSION CLOSED ===

[SESSION_COMPLETE]

---
_Session log: session-log/2026-03-27-audit-fa5-guard.md_
