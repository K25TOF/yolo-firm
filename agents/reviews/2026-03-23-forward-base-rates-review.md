# Session Review: forward-base-rates
_Date: 2026-03-23 21:57 UTC | Model: claude-sonnet-4-6_

## Manager Synthesis

## LC-2025-014 CONTINUATION — Synthesis & Close

Both agents have delivered their final turns. I now have everything needed to close.

---

### 5-Bullet Synthesis

1. **MORNING_FRONT and EARLY_SPIKE are the lead candidates** — 14.3x and 8.8x lift respectively, statistically reliable CIs (n=118, n=141). Both agents agree these are worth pursuing. No disagreement on verdict.

2. **Three questions must be resolved before any lift figures are presented to PO** — Q3 (threshold origin), Q1 (vol_ratio denominator), Q2 (runner definition). Challenger ranks Q3 as the most severe: a bad resolution invalidates the entire forward base rate exercise, not just a parameter. These are not administrative clarifications — they are validity gates.

3. **Parallel design on Components 1 and 2 is conditionally approved** — detection logic structure and position sizing can proceed without resolving Q1-Q3, but every design document must carry explicit unresolved flags on vol_ratio denominator, runner definition, and threshold origin. No clean sign-off until resolution.

4. **MIDDAY_BUILDUP and EVEN_DIST: do not retire, but no finding yet** — high apparent lift (19.9x–21.7x) is interesting but n=13/17 is not a finding. Additionally, both have unresolved lookahead questions (Q5, Q7) that must be cleared before any further work. More data collection is the correct path.

5. **MULTI_SPIKE: retire current formulation** — 1.70% lift at n=176 is a reliable null result, but Challenger's caveat stands: "price continuation" may be a lookahead filter that corrupted the measurement. Retire the verdict for now; do not conclude "no signal" from a potentially invalid base rate.

---

### FLAG FOR CONTEXT Items

From both agents — all flagged for PO review:

| # | Flag | Source | Action Required |
|---|---|---|---|
| F1 | Q3 — threshold origin: if thresholds derived on same 109,380 ticker-days, all lift figures are in-sample | Challenger | PO to provide analysis sequence before any PO presentation of lift figures |
| F2 | Q1 — vol_ratio denominator: if intraday beyond detection bar, all five cluster base rates invalid | Challenger | PO/Workshop to confirm formula — one line of code |
| F3 | Q2 — runner definition: if includes pre-detection gap-up opens, base rates inflated | Challenger | PO to confirm exact runner definition — one sentence |
| F4 | MORNING_FRONT and EARLY_SPIKE conditionally actionable — parallel design approved with unresolved flags | Both | Design doc must carry explicit flags; no clean sign-off until Q1/Q2/Q3 resolved |
| F5 | MIDDAY_BUILDUP "new HOD after min 90" — implementation unconfirmed, potentially blocking | Both | Manager to provide code/pseudocode before cluster is used further |
| F6 | MULTI_SPIKE "price continuation" — may be lookahead; 1.70% base rate suspect | Challenger | Confirm implementation before concluding null result |
| F7 | EVEN_DIST "no 10-min bucket > 25% of what?" — volume denominator unspecified | Challenger | Confirm formula before cluster is used further |
| F8 | Ticker independence — if top-3 tickers account for >30% of MORNING_FRONT/EARLY_SPIKE detections, Wilson CIs are optimistic | Challenger | Provide unique ticker counts for detected sets |
| F9 | Daily trigger frequency — ~2/day estimate on 2K-ticker universe unvalidated; need date range + daily ticker count | Optimist | Confirm before scanner operational design |
| F10 | Cluster mutual exclusivity — confirmed for EARLY_SPIKE/MORNING_FRONT only; not verified across all five | Challenger | Confirm counts of overlapping days |

---

### Decision Required from PO

**Option A — Resolve blocking questions first, then design**
PO provides answers to Q1, Q2, Q3 (and ideally Q5, Q6, Q7 for the gated clusters). Design begins after resolution. Cleanest path — no rework risk.

**Option B — Begin parallel design now, gate backtest**
Components 1+2 of MORNING_FRONT and EARLY_SPIKE scanner design begin immediately. All design documents carry explicit flags on Q1/Q2/Q3. Exit rules wait for Q2. Backtest waits for Q1/Q3. Faster but carries rework risk if any of the three questions resolves badly.

**Manager's assessment:** Q3 (threshold origin) is the highest-severity question. If PO can answer it immediately, it either clears the path entirely or resets the analysis — in either case, it is the first question to ask. I recommend PO answer Q3 before any design work begins.

---

### Memory Updates — Flagged for PO Approval

**Proposed update to manager memory.md:**

- Add LC-2025-014 to session history
- Record cluster verdicts: MORNING_FRONT and EARLY_SPIKE conditionally actionable; MIDDAY_BUILDUP and EVEN_DIST needs-more-data (high lift, low n, unresolved lookahead); MULTI_SPIKE retired (current formulation)
- Record the 3 priority blocking questions (Q3 threshold origin, Q1 vol_ratio denominator, Q2 runner definition)
- Record parallel design approval conditions

PO approval required before memory write.

---

### Next Action

**Immediate:** PO to answer Q3 (threshold origin) — single question, single answer. This either clears the path or resets the analysis. All other work waits on this.

**Then:** Q1 (vol_ratio denominator formula) and Q2 (runner definition — one sentence). Together, these three answers determine whether MORNING_FRONT and EARLY_SPIKE are production-ready hypotheses or promising-but-unvalidated patterns.

**Pending PO decision on Option A vs B.**

=== SESSION CLOSED ===

[SESSION_COMPLETE]

---
_Session log: session-log/2026-03-23-forward-base-rates.md_
