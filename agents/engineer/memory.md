# Engineer Memory

## Momentum Universe Filter

Standard universe filter for all momentum strategy backtesting. Enabled via `momentum_universe: true` in run_backtest config.

- **Threshold:** `(day_high - day_low) / day_low >= 0.50` (hardcoded 50%, not configurable)
- **Price source:** All bars in cached 1-min file (pre-market + RTH + after-hours)
- **Purpose:** Filters to tickers that demonstrated genuine momentum on a given day. Reduces noise from 5,000+ cached tickers to only those with real intraday moves.
- **Always use for momentum strategies** (vol_filter, grinder, etc.). Only omit for non-momentum research.
- **Result fields:** `pairs_evaluated`, `pairs_skipped_momentum`, `pairs_skipped_other` — always report these in experiment results.
- **Yield rate baseline (LC-2025-003):** 5,755 / 103,554 pairs pass (5.6%), 94.4% skip rate across full cache. Avg 31.4 evaluated pairs/date.

## Engine knowledge

- Current indicator set: 25 registered (ema_gap, vwap_session, volume_ratio_ema, atr, bb_width, kc_width, squeeze_on, squeeze_momentum, force_index, kama, etc.)
- Known engine limitations: mid-candle ordering (backtest uses bar close, live uses real-time updates)
- `greater_than` / `less_than` operators: functional — aliases for `>` / `<`. Both forms accepted. Also available: `>=`, `<=`, `crosses_above`, `crosses_below`.
- Prototype scripts available: batch_historical.py, walk.py (shared walk logic)

## Cache scale (LC-2025-003 — confirmed 2026-03-07)

- **103,554 ticker-date pairs attempted** across 183 dates (2025-05-29 → 2026-03-04)
- **5,755 pairs pass momentum filter** (≥50% intraday range), avg 31.4/date
- **14 pairs skipped other** (minimal, no data quality concern)
- Distribution: well spread across all 183 dates — no clustering

## Experiment patterns

- Common failure modes: tight AND filters produce too few trades for statistical significance
- Data quality issues observed: VWAP noisy on sub-$1 stocks (bid-ask 1-5%), single blocks shift VWAP 0.5-2%

## Exit Rule Design Principle (LC-2025-002 Audit)

**Exit threshold must be BELOW entry threshold** to mirror vol_filter fade logic.

- vol_filter: entry `crosses_above 3.0`, exit `crosses_below 1.5` — exit fires when momentum fades below entry level ✓
- HYP-025 error: entry `crosses_above 1.0`, exit `crosses_below 2.0` — exit only fires when momentum STRENGTHENS past 2.0% — inverted logic ✗

The inverted config traps positions to EOD force-close (52–70 bar avg hold vs 7.5 for vol_filter). This distorts all PnL and WR results and is disqualifying for the failure verdict. A `crosses_above 1.0` entry requires an exit like `crosses_below 0.5` — not `crosses_below 2.0`.

**Corrected HYP-025 re-test exit:** `ema_gap crosses_below 0.5` (or equivalent below entry threshold).

## HYP-025 Diagnostic Results (LC-2025-002 — 10-ticker × 16-date universe, skip_first=true)

- DIAG-A1 (`crosses_above 1.0` + VWAP >2%, no accel filter): 239T, 50.2% WR, +230.0% PnL, 52.6 avg hold bars
- DIAG-A2 (same + `accel < 1.0`): 109T, 56.0% WR, +107.3% PnL, 69.9 avg hold bars
- DIAG-A3 (vol_filter baseline — `crosses_above 3.0`, vol>2x): 87T, 34.4% WR, +41.6% PnL, 7.5 avg hold bars

**Acceleration filter effect:** 239→109 (-54% trade reduction), +5.8pp WR improvement — directionally real but insufficient to normalise trade count at a 1.0% entry threshold.

**`crosses_above 1.0` generates ~2.7× more raw crossings than `crosses_above 3.0`** across same universe.

**HYP-025 verdict:** INCONCLUSIVE — config error (inverted exit rule), not a clean failure. Entry signal (ema_gap 1.0% + VWAP 2% + accel < 1.0) has not been fairly evaluated. Corrected re-test warranted.

## Skip Rate Structural Finding (LC-2025-002)

67% skip rate on scanner-flagged universes is STRUCTURAL — not hypothesis-specific:
- Confirmed: identical skip count (98/160 pairs) across all three diagnostic configs on same universe
- Causes: missing cache files or sub-threshold bar counts for ticker-date combinations
- Not a grinder strategy artifact

**Future batch experiment requirement:** Capture cache-miss vs bar-count-too-low breakdown separately in skip reporting. This matters for diagnosing whether skips are a universe selection problem (cache-miss) or a data thinness problem (bar-count).

## Grinder Strategy Backtest Plan (HYP-025)

**Indicators required:**
- ema_gap (registered)
- vwap_session (registered)
- atr (registered)
- ema_gap_acceleration (registered — 3-bar ROC of ema_gap, params: fast/slow/lookback)

**Phase 1 scope (PO-approved — re-test pending PO sign-off on corrected config):**
- Entry: ema_gap 1.0% + VWAP 2% + acceleration < 1%
- Exit (CORRECTED): ema_gap crosses_below 0.5% OR VWAP break OR ATR 1.5x
- Dataset: 49 tickers, Feb 10–Mar 4 (same as EXP-023)
- Target: 40%+ win rate, measurable improvement on vol_filter-skipped tickers
- Original exit (`crosses_below 2.0`) was a config error — disqualifies original results

**Phase 2 (deferred, conditional):**
- Add volume bounds 1.5–4x if Phase 1 validates

**Known risks:**
- Sample size: tight 3-part filter may produce <50 trades across dataset
- VWAP evidence is thin; phased approach mitigates
- Mid-candle gap acceleration in live entry (Phase 4 refinement, not blocking Phase 1)

**Backtest validation requirements (LC-2025-003):**
- min_stabilization_bars must be >= 20 (EMA 3/9 needs ~20 bars; bars 10–19 produce noisy gap_accel)
- Deliver results split by date subset: Feb 10–23 (out-of-sample) vs Feb 24–Mar 3 (design subset)
- Deliver results split by price bucket: sub-$1 / $1–5 / $5+
- Include per-trade gap_accel at entry for post-hoc threshold validation

## Lesson: Threshold Selection From Outcome Buckets Is High-Risk

EXP-021 bucketed outcomes by indicator ranges, then selected thresholds (gap_accel < 1.0%) that separated winners from losers. This is reverse-engineering from data — the threshold fits in-sample perfectly but may be meaningless on new data.

**Validation:** After backtest, compute indicator distributions on out-of-sample subset (Feb 10–23) and check if threshold still separates outcome groups. See LC-2025-003 Risk #1.
