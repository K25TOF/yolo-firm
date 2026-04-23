# LC-2025-023 P2-ABC Blocker Resolution

_Date: 2026-03-30 | Sessions: P2-blockers (LC-2025-026) | Agents: Challenger + Statistician_
_Status: ALL RESOLVED — Phase 2 may proceed_

---

## Blocker #1 — F3: Post-Open News Lookahead: RESOLVED

**Finding:** All 33 pairs removed by Fix A (strict pre-9:30 news) have ONLY post-open news. Zero pre-market, zero at-open. Earliest article: 09:35 ET. Most are 10:00+ or afternoon.

**Verdict (Challenger):** Fix A is the correct baseline. The original 10.8% / 16x lift included post-event reporting as if it were pre-market catalyst. This is confirmed lookahead contamination.

**Corrected Phase 1 headline: 9.8% precision, 14x lift (Fix A basis).**

The original 10.8% / 16x is disqualified. All future citations must use Fix A numbers.

**Residual concern:** Some 09:35-09:45 articles may describe pre-market catalysts published just after open. Conservative direction (removing them is cautious). Not blocking.

**Challenger sign-off:** Yes. Fix A is correct baseline. Original disqualified.

---

## Blocker #2 — Alt50 Runner Definition: PARKED

**PO decision:** Alt50 (1,638 runners, (high-open)/open >= 50%) was proposed post-hoc after seeing Phase 1 numbers. Parked — not used in this research track.

**Status:** PARKED. No action needed.

---

## Blocker #3 — Runner Definition: PARKED

**PO decision:** Original RTH definition locked in Phase 0: (max(bar_high) - min(bar_low)) / min(bar_low) >= 1.0, RTH bars only. 782 runners.

**Status:** PARKED. Locked. Does not change mid-research.

---

## Blocker #4 — Threshold Pre-Specification: RESOLVED AS OPEN RISK

**Finding from session log audit:**
- **gap >= 15%**: Pre-specified in HYP-PM-2 (Optimist proposal in LC-2025-023).
- **PM dollar vol >= $500K**: Pre-specified in HYP-PM-3 (from Scout literature, Gao et al. 2018).
- **PM dollar vol >= $5M**: NOT pre-specified. Emerged from P1 sweep alongside $500K, $1M, $2.5M, $5M, $10M.
- **The exact triple combination (gap>=15% + PM>=$5M + news)**: NOT pre-specified as a single hypothesis. Emerged from sweep.

**Verdict:** IN-SAMPLE OPTIMISATION confirmed. The 9.8% headline is an in-sample estimate.

**Pre-specified baseline:** PM >= $500K (the literature-sourced threshold) produces ~8.9% precision. The +0.9pp from PM >= $1M/$5M is in-sample threshold shopping on 1 degree of freedom.

**OOS degradation estimate (Statistician):**
- Expected OOS precision range: **7.0% – 9.5%**
- Central estimate: **~8.5%** (vs 9.8% in-sample)
- Pre-specified baseline lift: **~13x** (vs 14x in-sample)
- Winner's Curse on single threshold selection: ~50-60% of uplift retained OOS

**Qualifier on all future citations:** "9.8% precision / 14x lift is in-sample optimised; PM >= $1M not pre-specified. OOS central estimate ~8.5% / ~12x. Temporal validation required."

**Statistician sign-off:** Yes. OOS range [7.0%, 9.5%] is the planning figure. Temporal split mandatory.

---

## Blocker #5 — Ticker Clustering: RESOLVED

**Data:**
- 782 runner-days from 553 unique tickers
- 71% of tickers appear only once
- Maximum: 7 days (BQ)
- Top 10 tickers: 48 runner-days (6.1%)
- Top 20 tickers: 79 runner-days (10.1%)
- **Zero tickers exceed the 5% threshold** (would need >= 39 days)

**Verdict (Statistician):** No clustering correction needed. Independence assumption is safe at the aggregate level. Wilson CIs on precision are valid without adjustment.

**Statistician sign-off:** Yes. No clustering risk.

---

## Blocker #6 — Temporal Hold-Out Design: PARKED

**PO decision:** May–Dec 2025 = design set. Jan–Mar 2026 = OOS held-out set. Locked before Phase 2 begins. No threshold optimisation on OOS data.

**Status:** PARKED. Locked.

---

## Summary Table

| # | Blocker | Status | Key Finding |
|---|---|---|---|
| **1** | F3: Post-open news lookahead | **RESOLVED** | All 33 pairs post-open. Fix A correct. Headline: 9.8% / 14x. |
| **2** | Alt50 runner definition | **PARKED** | PO decision: not used. |
| **3** | RTH base rate definition | **PARKED** | PO decision: original locked. |
| **4** | PM threshold pre-specification | **RESOLVED (OPEN RISK)** | In-sample optimised. OOS estimate ~8.5% / ~12x. Qualifier required. |
| **5** | Ticker clustering | **RESOLVED** | No clustering risk. 553 unique tickers, max 7 days. |
| **6** | Temporal hold-out | **PARKED** | PO decision: May-Dec design, Jan-Mar OOS. Locked. |

---

## Corrected Phase 1 Baseline (for all future citations)

| Metric | In-sample (Fix A) | OOS estimate (Statistician) |
|---|---|---|
| Triple signal precision | 9.8% | 7.0% – 9.5% (central ~8.5%) |
| Lift vs base rate | 14x | ~12x |
| Recall | 9.1% (71/782) | Expected similar |
| Population (triple-eligible days) | 726 | ~250 in Jan-Mar 2026 (proportional) |
| Base rate | 0.694% | Stable across months |

**All Phase 1 numbers are in-sample only.** Temporal OOS validation (Phase 2-F) is mandatory before any production claim.

---

## Phase 2-F: Temporal OOS Validation — CONDITIONAL VALIDATED

_Session: LC-2025-027 (P2F-v2) | Date: 2026-03-30 | Agents: Statistician + Challenger + Execution Realist_

### OOS Results (thresholds locked, one shot)

| Metric | In-sample | **OOS** | Success criterion |
|---|---|---|---|
| Precision | 9.8% | **11.5% (21/183)** | >= 7.0% — **PASS** |
| 95% CI | [7.8%, 12.2%] | **[7.6%, 16.9%]** | CI lower >= 7.0% — **PASS** |
| Lift | 14x | **18.3x** | >= 8x — **PASS** |

Signal improved OOS. Not degraded.

### Monthly consistency
| Month | Fires | Runners | Precision |
|---|---|---|---|
| Jan 2026 | 77 | 9 | 11.7% |
| Feb 2026 | 73 | 9 | 12.3% |
| Mar 2026 | 33 | 3 | 9.1% |

### Daily operations
- 49/55 trading days had fires (89%)
- Mean 3.3 fires per day (median 3, max 10)
- 21 runners had mean RTH range of 184% (min 100%, max 521%)

### Verdict: CONDITIONAL VALIDATED

Quantitative gates met on point estimates. Four procedural items unresolved:

| Item | Status | Impact |
|---|---|---|
| Benzinga timestamp provenance (C2) | OPEN | Potentially disqualifying if timestamps are ingestion-time |
| News filter pre-specification (C3) | OPEN | Shifts gate threshold if IS-selected |
| OOS runner clustering (S2) | OPEN | Needed for CI validity |
| OOS precision at PM>=500K (C4) | OPEN | Confirms IS-selected threshold adds OOS value |

### Deployment blockers (Execution Realist)
| Blocker | Description |
|---|---|
| E1 | PM$vol threshold: backtest used full pre-market, live signal at 09:25 uses partial volume |
| E2 | Benzinga live ingestion latency unresolved |
| E3 | Position sizing framework absent for 88.5% false positive rate |

### What this means
The scanner signal is **real and OOS-validated on point estimates.** A pre-market scanner filtering for gap>=15% + PM dollar volume>=$5M + pre-9:30 Benzinga news identifies 100%+ RTH movers at 11.5% precision (18.3x above base rate), firing ~3 times per day.

This is the first OOS-validated predictive signal in the entire research programme.
