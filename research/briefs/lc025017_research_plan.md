# YOLO Research Plan — Post LC-2025-017

_Written: LC-2025-017 Part B | Status: DRAFT — PO approval required_
_Source: lc025017_baseline.md + all agent inputs (Scout, Optimist, Challenger, Exec Realist, Statistician)_

---

## Strategic Direction

**Core insight from audit:** We have a credible entry signal (ORB, 56% Good in-sample) and a proven
filter (skip-first) but no production-ready exit and no OOS validation. The research programme has
been exit-obsessed while the higher-EV lever is entry quality filtering.

**Ordering principle:** Run low-effort data queries first (D1A, D2, D6 pre-check).
These unlock the more expensive engine runs (D3, D4). D5 deprioritised — underpowered on current sample.

---

## Phase 0 — Pre-Check (Before All Other Research)

### D0 — Graduation Count

**Question:** Of 132 Good-rated entries, how many held to a natural exit signal vs EOD force-close?

**Why first:** This determines whether exit or entry research has higher EV. If >50% of Good
entries are force-closed at EOD, the dominant "exit" is market close — exit optimisation
research (D4) drops in priority and "how to extract value before 4pm" becomes the real question.

**Method:**
1. For each of 132 Good entries: walk 1-min bars from entry to EOD
2. Check if ema9_5m_d3 exit triggered before RTH close (16:00 ET)
3. Report: N held to exit signal vs N force-closed at EOD
4. For force-closed subset: report mean PnL at force-close vs mean peak PnL during hold

**Population:** 132 Good entries
**Dependencies:** None
**Complexity:** Low (30 minutes)
**Success criterion:** Descriptive — no threshold. Result determines D4 priority.

---

## Phase 1 — Data Queries (No Engine Required)

### D2 — Mechanical Bad Label (FIRST PRIORITY)

**Hypothesis:** A mechanical, reproducible label definition can reproduce PO's Good/Bad
ratings with >=80% precision on the Bad class, enabling scalable OOS testing without PO bottleneck.

**Why first:** Unlocks D3. Without a mechanical label, all OOS validation requires PO time.

**Method:**
1. Walk 1-min bars for each of the 298 PO-rated entries
2. Compute MAE (min low in first N bars after entry) and MFE (max high in first 30 bars)
3. Test 3-5 MAE% thresholds (3%, 5%, 7%, 10%) x 3 MFE% thresholds (2%, 3%, 5%)
4. Compare each mechanical definition to PO label — report concordance curve
5. Select threshold using BH-corrected significance on Bad class precision
6. Report Cohen's kappa + precision/recall per candidate

**Population:** 298 PO-rated entries (adequate — Statistician confirmed)

**Statistical requirements:**
- n=298 (adequate)
- Apply Benjamini-Hochberg correction across 15 MAE/MFE combinations
- Target: >=80% precision on Bad class (95% CI lower bound >=70%)

**Implementation notes:**
- Entry bar alignment: use bar index from backtest CSV, not reconstructed from timestamp
- bar_close[B0] entry is baked in — mechanical label is a POST-HOC OUTCOME PROXY, not an entry-time filter. Thresholds need ~1-2% downward adjustment for live use.
- MFE window: cap at EOD for late-day entries
- [EXEC FLAG] Confirmed: 1-min bars available in cache. No engine needed.

**Success criterion:** At least one MAE/MFE combination achieves >=80% precision on Bad class, survives BH correction, and Cohen's kappa >= 0.60

**Dependencies:** None
**Complexity:** Low (2-3 hours)

---

### D1A — Gap% Stratification (SECOND PRIORITY, parallel with D2)

**Hypothesis:** ORB entries preceded by large gap-from-prior-close (>15-20%) show materially
different Good-entry rates than the 56% baseline. Gap% stratifies entry quality.

**Method:**
1. Pull gap% for each of the 236 tradeable entries from grouped daily bars
2. Stratify into top-2 vs bottom-2 quintiles (merged per Statistician recommendation)
3. Compute Good% per merged group + bootstrap 95% CI
4. Test for monotonic decline across quintiles

**Population:** 236 entries, ~94 per merged group

**Statistical requirements:**
- n~94 per merged group (adequate for detecting >=15pp effects)
- Two-proportion z-test or bootstrap CI on proportion difference
- [STAT FLAG] Cannot detect effects <15pp with current sample

**Implementation notes:**
- Gap% = (entry-day open - prior close) / prior close
- Both values available in grouped daily bars (no new data needed)
- [EXEC FLAG] Verify cache date range covers all 236 entry dates before running
- Sub-$1 stocks: large % gap on small absolute moves — note in analysis

**Success criterion:** Top-2 quintile Good% >= 65% AND bottom-2 <= 45% (>=20pp gap), surviving bootstrap CI

**Dependencies:** None
**Complexity:** Low (1-2 hours)

---

### D6 — Retest Pattern Pre-Check (EXPLORATORY, parallel with D1A/D2)

**Hypothesis:** ORB entries where price retested the ORB high level (dipped back to within
+/-0.5% of ib_high) between ORB window close and B0 show higher Good rates than clean-break entries.

**Method:**
1. For each of 236 entries, walk 1-min bars between ORB window close and B0
2. Check if any bar's low touched within +/-0.5% of ib_high (or +/-1.0% for sub-$1)
3. Classify as "clean break" vs "retest break"
4. Report split count FIRST — if retest group n<30, stop here (exploratory only)
5. If n>=30: compare Good% between groups

**Population:** 236 entries. Retest group estimated at 20-30 entries.

**Statistical requirements:**
- [STAT FLAG] If n<30 retest entries: exploratory data query only, no significance claims
- If n>=30: Fisher's exact test. 95% CI on Good% approximately +/-18pp
- Cannot detect effects <20pp with expected sample

**Implementation notes:**
- [EXEC FLAG] ORB window length confirmation needed (5-min for V1)
- [EXEC FLAG] +/-0.5% tolerance may be too tight for sub-$1; use +/-1.0% for price <$1

**Success criterion:** Pre-check: retest group n>=30. If met: retest Good% >= 70% (>=14pp above baseline)

**Dependencies:** None
**Complexity:** Low (2-3 hours)

---

## Phase 2 — Validation (Requires Phase 1 Results)

### D3 — Temporal OOS Validation (REQUIRED before production)

**Hypothesis:** The ~56% Good entry rate holds on a temporally held-out dataset from outside
the LC-2025-014 research window.

**Why required:** All in-sample findings are upper-bound estimates. Without OOS validation,
no finding can be cited as production-ready.

**Method:**
1. Temporal split: use May–Dec 2025 as design set, Jan–Mar 2026 as OOS window.
   The full entry list has 1,845 entries in Jan–Mar 2026 (before ORB/quality filters).
   After multibagger + ORB filtering, this should yield well above n>=95 OOS entries.
2. Run ORB signal detection on OOS dates using BacktestEngine (ib_high entry)
3. Apply mechanical Bad label from D2 to classify OOS entries automatically
4. PO spot-checks n>=50 entries (NOT 20 — Statistician requirement) to confirm label accuracy OOS
5. Report OOS Good rate + 95% CI

**Population:** Target n>=95 OOS entries (Statistician minimum for detecting 10pp degradation from 56%).
Data is available — no need to wait for new data to accumulate.

**Statistical requirements:**
- n>=95 OOS entries for 80% power at alpha=0.05 to detect 10pp degradation
- [STAT FLAG] n=50 OOS (Optimist's original proposal) gives only 55% power — insufficient
- [STAT FLAG] PO spot-check requires n>=50 (not 20) for +/-14pp CI
- One-proportion z-test vs 56% baseline

**Implementation notes:**
- [EXEC FLAG] Date range confirmation needed — what dates does LC-2025-014 cover?
- [EXEC FLAG] D3 cannot start before D2 is complete and validated (hard dependency)
- OOS dates may be in different volatility regime — expected and acceptable

**Success criterion:** OOS Good rate >= 50% (lower bound of in-sample 95% CI). If below 50%, signal is degraded.

**Dependencies:** D2 complete. OOS date range confirmed. Cache has data for OOS dates.
**Complexity:** Medium

---

### D4 — EMA Exit Optimisation (Full Population)

**Hypothesis:** The ema9_5m_d3 exit threshold is not optimal for the ORB universe. A lower
threshold (d2 or d1) captures more of the move on strong runners while still cutting losses.

**Method:**
1. Run BacktestEngine with 3 exit variants (ema9_5m d1, d2, d3) on full 236 entries
2. Stratify results by PO Good/Bad label (NOT filter — use as stratification variable)
3. Report: mean PnL per variant, WR per variant, divergent trade count per pair
4. Apply Bonferroni correction across 3 pairwise comparisons (adjusted alpha=0.0167)

**Population:** 236 tradeable entries. Divergent subset estimated at 35-60 per pair.

**Statistical requirements:**
- [STAT FLAG] Report divergent trade count BEFORE interpreting results
- If <30 trades diverge for any pair: that comparison is underpowered (directional only)
- Wilcoxon signed-rank on divergent trades; Bonferroni x3
- Minimum detectable mean PnL difference: ~3-4pp (assuming std ~12-15pp)

**Implementation notes:**
- [EXEC FLAG] 5-min EMA9 computation method unconfirmed — may require bar aggregation
- Confirm whether BacktestEngine handles 5-min bars natively or needs pre-aggregation
- Results are upper-bound estimates (bar_close[B0] entry)

**Success criterion:** At least one variant shows >=4pp mean PnL improvement over d3 on divergent trades, surviving Bonferroni correction.

**Dependencies:** 5-min bar computation method confirmed
**Complexity:** Low-Medium

---

## Phase 3 — Conditional Research (Depends on Phase 1-2 Results)

### D1B — Pre-Market Volume Enrichment (conditional on D1A cliff)

**Hypothesis:** Adding pre-market dollar volume to gap% creates a stronger combined entry filter.

**Method:** Fetch pre-market bars from Polygon for 236 tickers; compute PM dollar volume; test Gap% x PM Volume interaction.

**Condition:** Only if D1A shows >=15pp gap between merged quintiles.

**Implementation notes:**
- [EXEC FLAG] 236 API calls to Polygon; tier confirmation needed
- [EXEC FLAG] PM volume sparse on sub-$1 stocks — signal may not exist for this segment

**Dependencies:** D1A shows cliff. Polygon tier confirmed.
**Complexity:** Medium-High

---

### D5 — Hard Stop Threshold Sensitivity (ACCUMULATE SAMPLE)

**Hypothesis:** A tighter hard stop (-5% or -7.5%) improves risk-adjusted returns vs -10%.

**Current status:** FA2 found hard stop fires only on tail subset (avg loser -3.4%).

**Statistical reality:**
- [STAT FLAG] Effective sample ~25-35 trades reaching stop level — SEVERELY UNDERPOWERED
- Cannot detect meaningful differences between -5%, -7.5%, -10% on current sample
- Power to detect 3pp WR difference: ~25%

**Recommendation:** Run descriptively only (no significance claims). Mark as "accumulate sample
over time." Do not use results to change production stop threshold without n>=100 effective trades.

**Dependencies:** Larger trade sample (accumulate over D3 OOS + future research)
**Complexity:** Medium (custom walk function likely needed for stop-from-entry)

---

## Second-Look Candidates (Not Active Directions)

| Candidate | Source | Revisit When |
|---|---|---|
| Guard C on Gap%>20% subset | FA5 + Optimist | After D1A confirms gap stratification |
| VR time-of-day interaction | FA6 | After V1/V2 stratification analysis |
| Hard stop -5%/-7.5% | FA2 | After D5 accumulates n>=100 effective |
| Grinder corrected re-test | HYP-025 | Parked (PO approval needed) |

---

## Execution Sequence

```
FIRST (before everything):
  D0 (Graduation count) ← determines D4 priority (30 min)

THEN (parallel):
  D2 (Bad Label)        ← FIRST PRIORITY, unlocks D3
  D1A (Gap%)            ← parallel with D2, zero dependency
  D6 pre-check          ← parallel, exploratory

AFTER D2 COMPLETE:
  D3 (OOS Validation)   ← requires D2 + n>=95 OOS entries

AFTER 5-MIN BAR METHOD CONFIRMED:
  D4 (EMA Exit)         ← can run parallel with D3

CONDITIONAL:
  D1B (PM Volume)       ← only if D1A shows cliff
  D5 (Stop threshold)   ← accumulate sample; descriptive only for now
```

---

## Summary

| Priority | Direction | Key Metric | Sample | Powered? |
|---|---|---|---|---|
| **1** | D2: Bad Label | Cohen's kappa >=0.60 | n=298 | Yes |
| **2** | D1A: Gap% | >=20pp gap between merged quintiles | n=94/group | Marginal |
| **3** | D3: OOS Validation | OOS Good rate >=50% | n>=95 OOS | Requires accumulation |
| **4** | D4: EMA Exit | >=4pp PnL improvement | n~50 divergent | Conditional |
| **5** | D6: Retest | Pre-check split count | n~20-30 | Exploratory only |
| **6** | D5: Stop | Descriptive only | n~25-35 effective | No |

---

_All agents contributed. Scout: literature context. Optimist: research directions. Challenger: bias checks.
Execution Realist: data availability + implementation. Statistician: sample sizes + corrections._

_Total session cost: Part A $0.97 + Part B $0.92 = $1.89_
