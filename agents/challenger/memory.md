# Challenger Memory

## Known Failure Modes

**Hand-picked artefact pattern (confirmed across 4+ cases):** Findings from small hand-picked ticker sets do not reliably transfer to the broad momentum universe. Hand-picked sets over-represent late-stage exhaustion trades, producing inflated or misleading results. Any finding from fewer than 200 pairs is directional only until validated on the full momentum universe.

| Source | Hand-picked finding | Broad universe result |
|---|---|---|
| EXP-010/011 | vol_filter +80.3%, 50% WR | -40.1%, 32.7% WR |
| EXP-021 | AND-profile = loser marker | +1.12pp WR above baseline |
| DIAG-A2 | gap accel < 1.0 → +5.8pp WR | -4.0pp WR, 98.6% trade reduction |
| IDEA-018 | Combined filter removes losers | AND-subset +1.12pp above baseline |

**Tight AND filters:** Produce too few trades for statistical significance. Common failure mode in hypothesis testing.

**Acceleration filter context dependency:** `ema_gap_acceleration < 1.0` passes 46% of trades on grinder-profile hand-picked tickers but only 1.4% on broad universe with vol_filter 3.0% entry. Filter is structurally incompatible across contexts.

**Arithmetic discrepancy pattern (LC-2025-015, FA4):** When sub-sample rates are provided as percentages without raw counts, weighted averages may not reconcile with reported combined rates. Always demand raw counts (Good N, Bad N, Total N) for every sub-sample. Percentage-only summaries are unauditable. The LC-2025-014 "56% Good rate" could not be reconciled with recalled v1/v2 sub-sample rates (128×54% + 170×48% = 50.6% ≠ 56%).

## Lookahead Bias Patterns to Check

**Threshold selection from outcome buckets:** EXP-021 bucketed outcomes by indicator ranges, then selected thresholds that separated winners from losers. This reverse-engineers from data — fits in-sample perfectly but may be meaningless on new data. Always require out-of-sample validation.

**Design-subset contamination:** If rule threshold X was chosen because it separated outcomes on dates D1, then dates D1 cannot be in the validation dataset. Report design-subset vs held-out-subset results separately. Flag if WR delta > 10pp.

**Selection bias in production readiness claims:** Vol_filter v2.0.0 active status was based on selection-biased results. EXP-023 (+67.4% skip-first, 17 days) is the most honest result — net positive but fragile, driven by 3 outlier trades.

**Entry price = bar_close[B0] (confirmed execution bias):** Using bar close as entry price is not executable. The earliest realistic execution is bar_open[B1]. On fast-moving small-cap stocks, the B0-close to B1-open gap can be 1–3%. This systematically understates entry cost and overstates returns. Standard check for all ORB or breakout research: demand B0/B1 gap distribution before accepting any PnL figure.

**Float_turnover with current-snapshot float (confirmed lookahead):** `ticker_metadata.parquet` is refreshed daily by cron — confirmed current-snapshot, not point-in-time. Float_turnover = volume / current_float uses data not available at trade time. For small-cap multibaggers (frequent secondary offerings), float changes materially. Direction of bias: current float > historical float → computed turnover < actual turnover → filter is more restrictive than intended (false-negative, conservative). Document as known limitation; do not silently accept as valid.

**RVOL baseline construction (unresolved, high risk):** If `rvol_baseline.parquet` is a single static value per ticker computed from full study history, every volume_ratio calculation is lookahead-contaminated. Direction of likely bias: full-history baseline > early-period baseline → computed VR < actual VR → 2.0x threshold is harder to reach than in reality (false-negative, conservative). Must confirm rolling vs static construction before accepting any VR-based finding.

**signal_bars.parquet enrichment (unaudited):** 1.7 GB of pre-computed enriched 1-min bars. Schema not reviewed. Risk: full-dataset normalisation or percentile ranking contaminates early bars. Mitigation: scope audit to columns actually used by the ORB signal (~4 intraday conditions), not full file. Standard check: demand schema + column-use map before accepting any enriched signal pipeline.

**Model multiplicity from untested window variants:** When multiple parameter variants are "both kept" (e.g., 5-min and 15-min ORB), results must be reported separately. Combined datasets obscure which signal is actually working. If one variant was added after seeing results from the other, this is post-hoc development — not exploration.

**PO visual chart review = structural hindsight contamination:** A human reviewing a chart sees post-entry price action. Good/Bad ratings are aesthetically derived, not mechanically measured. The 56% Good rate from LC-2025-014 has never been validated as a mechanical signal quality metric. It is a directional indicator only, with three confirmed qualifications: (1) hindsight contamination present, (2) arithmetic discrepancy unresolved, (3) in-sample only.

**Survivorship bias in multibagger universe:** Universe constructed from stocks confirmed to have moved 100%+ intraday. The outcome variable is built into the selection criterion. Correct reframe: ORB research is capture quality discrimination within a pre-filtered universe (Question B), not multibagger prediction (Question A). This is the correct design for capture quality research. The control group gap (ORB signals on 20–50% movers) remains unaddressed.

**Regime-specificity (unverified, high risk):** Date range of 298 ORB entries is unknown. If concentrated in 2020–2021 high-retail-participation regime, the Good rate may not persist in mean-reversion regimes. Year-by-year entry distribution is a required check before any deployment claim.

**Zero out-of-sample validation (confirmed, LC-2025-014):** Universe construction, threshold selection, ORB window selection, and PO rating were all performed on the same dataset. No held-out period exists. All figures from LC-2025-014 are in-sample only. Label explicitly in every future citation.

## Exit Rule Design Errors

**Exit threshold must be BELOW entry threshold** for fade-from-entry logic:
- vol_filter: entry 3.0%, exit 1.5% ✓
- HYP-025 original: entry 1.0%, exit 2.0% ✗ (inverted — disqualifying)

Inverted exit traps positions to EOD force-close (52–70 bar avg hold). This distorts all PnL and WR results and is a disqualifying error.

**No exit rules in LC-2025-014 ORB research.** Phase 1 (entry development) is complete in scope but unvalidated in quality. Phase 2 (exit design) is not yet started. ATR trailing stop is the primary exit candidate based on prior validation (EXP-009/LC-2025-009). EOD force-close is a baseline comparator, not a default assumption.

## Data Quality Issues

- VWAP noisy on sub-$1 stocks (bid-ask spread 1-5%), single blocks shift VWAP 0.5-2%
- Mid-candle ordering: backtest uses bar close, live uses real-time updates — results may not transfer
- Skip rate ~67% on scanner-flagged universes is structural (cache misses + thin bar counts), not hypothesis-specific
- `ticker_metadata.parquet`: daily cron overwrites with current data — confirmed current-snapshot, not point-in-time. Exchange classification false-positive risk (OTC stocks now uplisted appear as exchange-listed historically). Float false-negative risk (conservative direction).
- Split adjustment risk on small-cap bar cache: if bars cached at different times relative to split events, RVOL baseline and entry-day volume may use different price scales. Intraday ratios (ORB high, coil) are split-neutral (same-day bars). Cross-day comparisons (VR) are at risk.

## Audit Gates (from LC-2025-003)

Standard checks for any new strategy claim:
- Out-of-sample WR must be >= 35%
- Sub-$1 WR must be >= 35%
- Key indicator distribution must show separation on held-out subset
- Top 3 trades must not concentrate in design subset
- No single trade > +15% (outlier dependency check)

**Additional gates from LC-2025-015:**
- Raw Good/Bad counts (not percentages) must be provided for all sub-samples before any combined rate is accepted
- Date range and year-by-year distribution must be provided before any generalisability claim
- RVOL baseline construction must be confirmed (rolling vs static) before any VR-based finding is accepted
- signal_bars schema + ORB column map must be provided before any enriched-pipeline finding is accepted
- Inter-rater reliability (Cohen's Kappa ≥ 0.60) required before any single-rater classification is used as statistical ground truth

## Divergent Trade Analysis Method

When two configs share the same universe but differ in trade count, back-calculate divergent set WR: `divergent_winners = A_winners - B_winners`, `divergent_WR = divergent_winners / (A_trades - B_trades)`. Confirms whether a filter removed losers (good) or removed signal indiscriminately (bad).

## ORB Research Status (LC-2025-014 / LC-2025-015)

**Current state:** Phase 1 entry development. No validated findings. All figures in-sample only.

**Do not cite without qualifications:**
- "56% Good rate on 236 tradeable entries" — unreconciled (arithmetic discrepancy), hindsight-influenced, in-sample only
- "V1: 128 entries, 54% Good; V2: 170 entries, 48% Good" — sub-sample rates unconfirmed against raw counts; weighted average ≠ reported combined rate
- "Liquidity gate removes 21%, ratio unchanged" — unverified memory claim, not confirmed against raw data in LC-2025-015

**Confirmed resolved items:**
- V1 (5-min ORB) is the primary research track; V2 (15-min ORB) is secondary
- Entry price bias (bar_close[B0]) affects PnL only, not signal quality (PO ratings are price-independent)
- Liquidity gate is a binary prerequisite by design (if confirmed — see above caveat)
- Ticker metadata is confirmed current-snapshot (not point-in-time)

**Open blocking items (in priority order):**
1. Arithmetic reconciliation: raw Good/Bad counts for v1, v2, post-gate 236 *(source: FA4 — `2026-03-27-audit-fa4-exhaustion.md`, Q4a; also FA1 — `2026-03-27-audit-fa1-entry-v2.md`)*
2. Date range and year distribution of 298 entries *(source: FA1 — `2026-03-27-audit-fa1-entry-v2.md`, Q4c)*
3. 6 prior FA1 blocking issues — list and resolution status *(source: FA1 — `2026-03-27-audit-fa1-entry-v2.md`, Q1b + consolidated table)*
4. Float data source confirmation *(source: FA1 — `2026-03-27-audit-fa1-entry-v2.md`, Q1b + Q3e)*
5. RVOL baseline construction code snippet *(source: FA1 — `2026-03-27-audit-fa1-entry-v2.md`, Q3b)*
6. signal_bars schema + ORB column map *(source: FA1 — `2026-03-27-audit-fa1-entry-v2.md`, Q3c)*
7. B0-close to B1-open gap distribution for 236 entries *(source: FA1 — `2026-03-27-audit-fa1-entry-v2.md`, Q1e)*
8. RTH-only range recalculation (% of 450 stocks passing on RTH bars alone) *(source: FA1 — `2026-03-27-audit-fa1-entry-v2.md`, Q1a)*
9. Exchange OTC-uplisting cross-reference for 450 stocks *(source: FA1 — `2026-03-27-audit-fa1-entry-v2.md`, Q3e)*
10. Threshold derivation sequence (VR 2.0, coil -4%: before or after outcome analysis?) *(source: FA1 — `2026-03-27-audit-fa1-entry-v2.md`, Q1d)*
