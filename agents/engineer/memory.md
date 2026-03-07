# Engineer Memory

## Persistent Principles

**Principle #1 — Attribution:** Every experiment result must be attributed to one of three factors: scanner filter (which tickers enter the universe), entry point (when we buy), or exit point (when we sell). If a finding improves or degrades WR/PnL, state which factor it acts on and why. Attribution operates at test scenario level — when results are mixed, drill into which trades diverged. Tag each finding with [SCANNER], [ENTRY], or [EXIT].

**Principle #2 — Trade Log Interrogation:** Every backtest produces a trade log CSV at `analysis/research/results/`. After every run, report trade log path so Analyst can segment winners vs losers across all three factors. Aggregate metrics alone are insufficient — trade-level analysis is always required.

**Principle #3 — Stage-of-Move Dependency:** High EMA gap AND high volume co-occurrence is ambiguous — it marks momentum confirmation on early-stage runners and exhaustion on late-stage faders. The broad universe contains both cases in roughly equal proportion. Do not frame either indicator as a directional loser filter without controlling for stage of the move. Verified: AND-profile (gap >4% AND vol >5x) showed +1.12pp WR *above* baseline on broad universe (LC-2025-010), opposite of hand-picked findings (EXP-012, EXP-021).

**Principle #4 — Hand-Picked Artefact Warning:** Findings from small hand-picked ticker sets do not reliably transfer to the broad momentum universe. Any finding from fewer than 200 pairs must be treated as directional only until validated on the full momentum universe. Confirmed across 4+ independent cases (EXP-010/011, EXP-012/021, DIAG-A2, IDEA-018). Broad universe is the only valid test for strategy quality.

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
- ATR exit format: top-level parameter `atr_exit: {"period": 14, "multiplier": "2.0"}` — NOT inline in exit_rules array
- Prototype scripts available: batch_historical.py, walk.py (shared walk logic)
- **Engine does not support rejection/blocking logic natively.** AND-gate exclusion cannot be expressed directly. Workaround: invert the condition and use it as a required entry rule (e.g., to test "AND-subset only", add `ema_gap > 4.0` AND `volume_ratio_ema > 5.0` as entry requirements). OR-gate exclusion requires either a prototype script or engine story.

## Cache scale (LC-2025-003 — confirmed 2026-03-07)

- **103,554 ticker-date pairs attempted** across 183 dates (2025-05-29 → 2026-03-04)
- **5,755 pairs pass momentum filter** (≥50% intraday range), avg 31.4/date
- **14 pairs skipped other** (minimal, no data quality concern)
- Distribution: well spread across all 183 dates — no clustering

## Broad Universe Baselines

- **Vol_filter Config A — EMA-only exit (LC-2025-007):** 6,275 trades, 27.98% WR, -5,408.3% PnL, 6.7 avg hold bars (5,745 pairs, 183 dates, momentum_universe=true, skip_first=true) — current canonical baseline
- **Vol_filter Config B — EMA+ATR(14) 2.0x exit (LC-2025-007):** 6,370 trades, 29.62% WR, -4,158.8% PnL, 5.3 avg hold bars — ATR adds +1.64pp WR, +1,249.5pp PnL vs Config A; both remain deeply negative
- **HYP-025 corrected (LC-2025-007):** 12,024 trades, 32.5% WR, +1,889.2% PnL, 4.9 avg hold bars — exit at 0.5% too tight for grinder profile

## ATR Exit — Broad Universe Finding (LC-2025-007)

[EXIT] ATR(14) 2.0x trailing stop on vol_filter broad momentum universe:
- +1.64pp WR improvement (27.98% → 29.62%)
- +1,249.5pp PnL improvement (-5,408.3% → -4,158.8%)
- +95 trades (earlier exits free positions for re-entry)
- -1.4 avg hold bars (5.3 vs 6.7) — ATR fires earlier than EMA exit on losing trades
- Validation target: PASS on direction (both metrics improve). Both configs remain net negative at scale.
- Contrasts with EXP-016 hand-picked finding: +9.9pp PnL on 49 tickers. Effect is real but much smaller on broad universe. Analyst to interpret EXP-016 comparison.

## RVOL Threshold Sensitivity (LC-2025-011)

[ENTRY] volume_ratio_ema threshold on vol_filter broad momentum universe (192 dates, 5,863 pairs, Config B + ATR):

| Threshold | Trades | WR | PnL % |
|-----------|--------|------|-------|
| >= 2.0 | 6,565 | 29.57% | -4,531.0% |
| >= 3.0 | 3,568 | 31.20% | -2,154.2% |
| >= 4.0 | 2,048 | 31.96% | -1,317.9% |
| >= 5.0 | 1,199 | 33.08% | -576.8% |

- Higher threshold = fewer trades + higher WR (stable +0.035pp WR per 1% trade reduction)
- Divergent set (2.0-only trades): 28.80% WR — below baseline, concentrated losers
- All thresholds remain deeply net negative — RVOL is a working knob but insufficient to fix core edge problem
- **dates='all' not supported by _discover_pairs_from_cache** — must pass explicit date list

## IDEA-018 — Combined Overextended Entry Filter (LC-2025-010 — FAIL)

[ENTRY] AND-condition subset (gap >4.0% AND volume_ratio_ema >5.0x simultaneously at entry):
- 316 trades on broad momentum universe (5% of vol_filter entries — rare, not dominant)
- WR: 29.10% — **+1.12pp above Config A baseline** (27.98%)
- Avg hold: 7.4 bars (vs 6.7 baseline) — not fast-reversing spike-chasers
- **Verdict: FAIL.** Hypothesis refuted on its own terms. AND-subset is marginally better than average, not a loser archetype.
- Source findings (EXP-012, EXP-021) were hand-picked artefacts. High gap + high vol co-occurrence is ambiguous — marks exhaustion on hand-picked faders, marks momentum confirmation on true runners. No net loser signal on broad universe.
- IDEA-018 retired. No further testing warranted.

## Experiment patterns

- Common failure modes: tight AND filters produce too few trades for statistical significance
- Data quality issues observed: VWAP noisy on sub-$1 stocks (bid-ask 1-5%), single blocks shift VWAP 0.5-2%
- **Acceleration filter context dependency:** `ema_gap_acceleration < 1.0` passes 46% of trades on grinder-profile hand-picked tickers (DIAG-A2) but only 1.4% on broad momentum universe with vol_filter 3.0% entry (LC-2025-008). Filter belongs in grinder signal context (crosses_above 1.0%), not vol_filter (crosses_above 3.0%). See IDEA-020, IDEA-021.
- **Hand-picked → broad universe collapse pattern (confirmed across LC-2025-005 through LC-2025-010):** EXP-010/011, EXP-014, EXP-016/023, EXP-022, IDEA-018 all showed positive or directional hand-picked results that failed or reversed on the broad momentum universe. Selection bias is the confirmed mechanism. Broad universe is the only valid test for strategy quality.

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
