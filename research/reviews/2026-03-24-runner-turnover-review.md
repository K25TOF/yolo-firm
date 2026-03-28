# Session Review: runner-turnover
_Date: 2026-03-24 13:04 UTC | Model: claude-sonnet-4-6_

## Manager Synthesis

## LC-2025-014 — Synthesis

Both agents have been consulted. Closing the session.

---

### Key Findings (3-5 bullets)

- **Cluster split is directionally real but evidence is incomplete.** EARLY_SPIKE (0.06x) and MORNING_FRONT (0.13x) P50s sit well below all other clusters (0.81x–2.75x). The structural separation is plausible but unconfirmed — per-cluster N counts and upper percentile distributions (P75/P90) are required before "separation" is defensible.

- **FT ≥ 0.25x is a reasonable candidate threshold, not a defensible recommendation.** Optimist's rationale is internally coherent; Challenger's audit identified a factual framing error ("ceiling" vs "median" for MORNING_FRONT P50=0.13x) and three blocking gaps before the threshold can advance.

- **Lookahead bias risk is unresolved and blocking.** Float turnover requires a float figure of known provenance. If float was pulled post-hoc (e.g. from a static data provider after the trading date), every FT ratio in the dataset is contaminated. This must be confirmed before any filter decision.

- **Additionality claim is weaker than presented.** The 0.597 correlation confirms FT and $vol are non-redundant as *metrics* — not that FT adds *predictive signal*. No outcome variable (WR, PnL) has been tested against FT. "Additive as a metric" ≠ "additive as a signal."

- **Four data requests must be resolved before threshold recommendation routes to PO.** (1) Float data source and timestamp confirmed as real-time compatible. (2) Per-cluster N counts. (3) Per-cluster P75/P90 distributions. (4) $vol lift decomposed: mcap filter contribution vs FT filter contribution independently.

---

### FLAG FOR CONTEXT Items

1. **[BLOCKING — Lookahead bias]** Float sourcing method not confirmed. If float figures are post-hoc (static provider, end-of-day or later pull), the FT dataset cannot be used as-is. Requires Workshop or PO to confirm data pipeline float sourcing method.

2. **[FACTUAL CORRECTION]** "MORNING_FRONT ceiling = 0.13x" is incorrect framing. 0.13x is the cluster P50, not a ceiling. Per-cluster upper percentiles are required to confirm FT ≥ 0.25x actually excludes the target clusters rather than merely sitting above their median.

3. **[OPEN QUESTION — Filter executability]** FT is a cumulative intraday metric. At signal fire time (e.g. 09:35), cumulative $vol may be insufficient to confirm FT ≥ 0.25x on higher-float names. This is an implementation constraint, not a regime question. Needs intraday FT confirmation timing analysis before the filter is implementable.

4. **[OPEN QUESTION — Regime stability]** Date range of the 1,404 runner-days unknown. If concentrated in 2020–2021, threshold calibration may be non-transferable to current conditions. Year-by-year FT distribution summary needed.

5. **[THRESHOLD ARBITRARINESS]** No outcome data distinguishes FT ≥ 0.25x from 0.5x or 1.0x. The 1.0x level lifts median $vol 60% more (to $135M) at 50% retention. Without WR/PnL breakdown by FT bucket, the 0.25x selection is not supportable over alternatives.

---

### Decision / Outcome

**Status: DEFERRED — threshold candidate identified, not approved.**

FT ≥ 0.25x remains a live candidate pending resolution of four data requests. Session has produced a clear checklist for what is needed before this can route to PO as a recommendation.

---

### Required Actions (for PO)

| # | Action | Owner | Priority |
|---|---|---|---|
| 1 | Confirm float data source and pull timestamp in the research pipeline — real-time compatible? | Workshop / PO | Blocking |
| 2 | Provide per-cluster N counts for all clusters in the runner universe | Manager / next session | Required |
| 3 | Provide per-cluster P75/P90 float turnover distributions | Manager / next session | Required |
| 4 | Decompose $vol lift: mcap ≥$10M filter alone vs combined with FT filter | Manager / next session | Required |
| 5 | Provide FT bucket WR/PnL breakdown (e.g. <0.25x, 0.25–1.0x, 1.0–5.0x, >5.0x) | Manager / next session | Before threshold approval |

---

### Memory Updates (for PO approval)

**Proposed update to manager memory.md:**

Add to session history:
> LC-2025-014 (float turnover threshold): FT ≥ 0.25x identified as candidate threshold — deferred. Blocking issue: float data sourcing not confirmed as real-time compatible (lookahead bias risk). Four data requests outstanding before threshold routes to PO. Key finding: cluster P50 gap is directionally real (EARLY_SPIKE 0.06x, MORNING_FRONT 0.13x vs others 0.81x+) but within-cluster distributions unknown. Additionality claim (correlation 0.597) confirmed as metric non-redundancy only — signal additionality unproven without outcome data.

Add to key lessons:
> **Correlation ≠ signal additionality.** A bivariate correlation between two input metrics (e.g. FT × $vol = 0.597) confirms they are non-redundant as measurements — it does not confirm incremental predictive value. Signal additionality requires outcome data (WR/PnL by bucket or regression R² increment).

> **Cluster P50 ≠ cluster ceiling.** When setting a filter threshold to exclude a cluster, the threshold must clear the cluster's upper percentile distribution (P75/P90), not just its median. Setting a threshold above a cluster median may still pass 25–40% of that cluster's members.

---

No doc updates to `strategy-roadmap.md` or `kpis.md` required — session produced deferred decision, no strategy state change.

=== SESSION CLOSED ===

[SESSION_COMPLETE]

---
_Session log: session-log/2026-03-24-runner-turnover.md_
