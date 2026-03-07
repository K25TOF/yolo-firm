# Analyst Memory

## Persistent Principles

**Principle #1 — Attribution:** Every experiment result must be attributed to one of three factors: scanner filter (which tickers enter the universe), entry point (when we buy), or exit point (when we sell). If a finding improves or degrades WR/PnL, state which factor it acts on and why. Attribution operates at test scenario level — when results are mixed, drill into which trades diverged. Always classify before drawing conclusions.

**Principle #2 — Trade Log Interrogation:** Every backtest produces a trade log CSV at `analysis/research/results/`. After every run, segment winners vs losers and identify patterns across all three factors: scanner (which tickers produced winners), entry conditions (EMA gap magnitude, vol ratio, VWAP distance at entry), and exit conditions (exit_type, hold_bars). Aggregate metrics answer "did this config help?" — trade log analysis answers "what do winning trades look like?" Both required. To understand each factor's contribution, isolate where possible — hold two factors constant to test the third.

**Principle #3 — Stage-of-move dependency:** High EMA gap AND high volume co-occurrence is ambiguous — it marks momentum confirmation on early-stage runners and exhaustion on late-stage faders. The broad universe contains both cases in roughly equal proportion. Do not frame either indicator as a directional loser filter without controlling for stage of the move. Verified: AND-profile (gap >4% AND vol >5x) showed +1.12pp WR *above* baseline on broad universe (LC-2025-010), opposite of hand-picked findings (EXP-012, EXP-021).

**Principle #4 — Hand-Picked Artefact Warning:** Findings from small hand-picked ticker sets do not reliably transfer to the broad momentum universe. Any finding from fewer than 200 pairs must be treated as directional only until validated on the full momentum universe. Confirmed across 4+ independent cases (EXP-010/011, EXP-012/021, DIAG-A2, IDEA-018) — hand-picked sets over-represent late-stage exhaustion trades, producing inflated or misleading results.

## Momentum Universe Filter

When interpreting backtest results, check whether `momentum_universe` was enabled:

- **Definition:** Filters ticker-date pairs to only those with >= 50% intraday range: `(day_high - day_low) / day_low >= 0.50`
- **Impact on results:** Removes low-volatility pairs that would produce no signals anyway. Win rates and PnL are comparable only across experiments using the same universe setting.
- **Standard for momentum strategies:** All vol_filter, grinder, and momentum research should use `momentum_universe: true`. Results without it include noise from non-moving tickers.
- **Check in results:** `pairs_skipped_momentum` shows how many pairs were filtered out. High skip counts are expected and normal.

## Strategy knowledge

- Active strategy: vol_filter_ema10 v2.0.0 (82T, 46% WR, +158.9% on 49 hand-picked tickers — see selection bias note below)
- Known trade profiles: impulse (vol_filter), grinder (IDEA-016/HYP-025)
- Closed hypotheses: none — HYP-025 Phase 1 status revised (see below)

## Research patterns

- What has worked: skip-first filter (+75.2pp improvement EXP-022), non-accelerating gap on hand-picked grinder set only (EXP-021/DIAG-A2 — **not transferable to vol_filter or broad universe**, see LC-2025-008)
- What has failed: HYP-024 VWAP distance filter (inconclusive, +4.2pp below +5pp bar); gap accel filter on vol_filter (LC-2025-008 — accel < 1.0 incompatible with 3.0% entry, 98.6% trade reduction, WR -4.0pp); IDEA-018 combined overextended entry filter (LC-2025-010 — AND-subset +1.12pp WR above baseline, hypothesis refuted, FAIL)
- Indicators not yet tested: squeeze indicators, force index
- Indicators tested: ema_gap_acceleration (registered and working — used in HYP-025 Phase 1)

## Hand-Picked Artefact Pattern — Confirmed Across Four Leads

The following findings all pointed in the same direction on hand-picked or scanner-day datasets, and all failed to transfer to the broad momentum universe:

| Source | Hand-picked finding | Broad universe result |
|---|---|---|
| EXP-010/011 original | vol_filter +80.3%, 50% WR | -40.1%, 32.7% WR |
| EXP-021 | AND-profile (gap >4%, vol >5x) = loser marker | +1.12pp WR above baseline (LC-2025-010) |
| EXP-012 | gap >4% → 27% WR (below baseline) | Same AND-profile +1.12pp above baseline |
| DIAG-A2 | gap accel < 1.0 → +5.8pp WR on grinder set | -4.0pp WR, 98.6% trade reduction on vol_filter (LC-2025-008) |

**Pattern:** Hand-picked ticker sets are selected after the fact from known movers. They over-represent late-stage exhaustion trades. Broad universe includes genuine early-stage runners where the same signals mean the opposite. Always validate on broad universe before citing a finding as strategy evidence.

## LC-2025-005 Findings — Vol_filter Broad Universe Validation

**Session:** LC-2025-005 (EXP-010, EXP-011, EXP-014 re-runs on momentum universe)

**Core finding (unambiguous):** Vol_filter loses money on the broad momentum universe regardless of config variant:

| Run | Universe | WR | PnL |
|---|---|---|---|
| EXP-010-rerun | 148 pairs, momentum filtered | 32.7% | -40.1% |
| EXP-014-rerun | 180 pairs (date subset, unknown) | 37.0% | -22.3% |
| DIAG no-ATR full range | 435 pairs | 30.8% | -416.4% |

**Selection bias confirmed:** Original EXP-010 (+80.3%, 50% WR) used 6 hand-picked known momentum winners. Original EXP-014 (+158.9%, 46% WR) used 49 hand-picked tickers. Neither result is a valid benchmark for a generalised strategy. Both were artefacts of hand-curation.

**Principle #6 violation confirmed at scale:** Strategy is net positive only when outlier runners appear (NCI, STAK, MOBX). On broad momentum universe, strategy loses money on most tickers/days. Consistent with EXP-023 finding.

**ATR exit (EXP-014-rerun):** Concern raised then withdrawn. EXP-016 (clean 49-ticker test) remains the valid ATR benchmark — combined exit outperformed EMA-only 13:6 on divergent trades. No evidence ATR is degrading results in re-runs. Universe expansion is the dominant driver of PnL degradation.

**Data quality note:** EXP-014-rerun used an unknown date subset (180 pairs vs expected 435 on full 16-date range). Universe mismatch is logged; it does not affect the core finding.

**Implication for strategy assessment:** Vol_filter v2.0.0 active status is based on selection-biased results. Production readiness case was overstated. EXP-023 (+67.4% skip-first, 17 days) is the most honest result to date — net positive but fragile, driven by 3 outlier trades.

## Grinder Profile Characterization (HYP-025)

**Source:** LC-2025-002, EXP-019 slow_grind findings

**Profile markers:**
- EMA gap 1–3% (moderate, early in trend)
- Price >= VWAP + 2% (uptrend confirmation)
- Volume ratio 1.5–4x (sustained, not spiking) — deferred to Phase 2
- EMA gap acceleration < 1% (steady climb, not parabolic)
- Hold duration: 15–30 bars typical (vs vol_filter 7–8 bars)
- Archetype: MDBX Mar 3, 2026 (+29% over 145 bars, entry $0.74 VWAP $0.70)

**Evidence strength:**
- VWAP distance (2%+): Weak — EXP-012 marginal diff, HYP-024 inconclusive
- Volume bounds (1.5–4x): Untested on grinder sample, extrapolated from vol_filter
- Acceleration filter: **Context-dependent** — DIAG-A2 showed +5.8pp WR on hand-picked grinder set (239→109 trades), but LC-2025-008 showed the same filter (accel < 1.0) is structurally incompatible with vol_filter's 3.0% entry (98.6% trade reduction, WR -4.0pp). Filter belongs in grinder context only (IDEA-021).

**Result:** Phase 1 corrected re-test FAILED (LC-2025-007) — 32.5% WR, 4.9 bar avg hold on broad universe. Exit at 0.5% too tight (0.5pp decay room). Grinder concept not invalidated — exit design is proximate cause.

**Exit rule error (LC-2025-002):** Original HYP-025 used `ema_gap crosses_below 2.0` as exit with `crosses_above 1.0` entry. This is logically inverted — exit only fires when gap *strengthens* past 2.0%, causing most positions to be held 50–70 bars to EOD force-close. The WR and PnL results are contaminated and cannot be used as evidence for or against the grinder entry signal.

**Corrected exit rule for re-test:** Exit threshold must be *below* entry threshold (fade-from-entry logic). Suggested: `ema_gap crosses_below 0.5` — mirrors vol_filter's pattern (entry 3.0%, exit 1.5%; grinder entry 1.0%, exit ~0.5%).

## Lesson: Rule Design Must Be Segregated From Rule Validation

HYP-025 entry rules were designed using EXP-021 data (Feb 24–Mar 3). Using the same date range as validation (Feb 10–Mar 4) includes the design subset, inflating confidence.

**Pattern:** If rule threshold X was chosen because it separated outcomes on dates D1, then dates D1 cannot be part of the validation dataset. Always report design-subset vs held-out-subset results separately. Flag if WR delta > 10pp. See LC-2025-003 Risk #1.

**HYP-025 audit gate (LC-2025-003):**
- Feb 10–23 WR must be >= 35% (true out-of-sample)
- Sub-$1 WR must be >= 35% (validates VWAP rule isn't slippage artifact)
- Gap_accel distribution on Feb 10–23 must show separation at 1.0% threshold
- Top 3 trades must not concentrate in Feb 24–Mar 3 (design subset)
- No single trade > +15% (outlier dependency check)

## Lesson: Exit Rule Must Mirror Entry Logic (fade-from-entry)

For any momentum strategy using EMA gap: exit threshold must be *below* entry threshold. The gap must fade from entry level before exit fires — not strengthen. Violation of this principle causes positions to be held indefinitely (until EOD force-close), contaminating all WR and PnL results.

- vol_filter: entry 3.0%, exit 1.5% ✓
- HYP-025 original: entry 1.0%, exit 2.0% ✗ (inverted — disqualifying)
- HYP-025 corrected: entry 1.0%, exit ~0.5% (to be validated)

## Lesson: Hand-Picked Universe Creates Selection Bias

Any backtest run on a hand-curated ticker set (tickers selected because they were known to move) produces inflated results. This is not a valid benchmark for production readiness.

**Pattern to flag:** If `pairs_evaluated` is small (< 50) and tickers were hand-selected by the researcher, treat WR and PnL as upper-bound estimates only. Require momentum universe validation before citing results as strategy evidence.

**Affected experiments:** EXP-001 through EXP-013 (all hand-picked sets, pre-engine), EXP-014 original (49 hand-picked), EXP-010 original (6 hand-picked).

## Analytical Methods

**Divergent trade back-calculation:** When two configs share the same universe but differ in trade count, back-calculate the divergent set's WR from aggregates: `divergent_winners = A_winners - B_winners`, `divergent_WR = divergent_winners / (A_trades - B_trades)`. Confirms whether a filter removed losers (good) or removed signal indiscriminately (bad). Used successfully in LC-2025-008.

## Session History (Recent)

- LC-2025-007: HYP-025 corrected re-test — FAILED. 32.5% WR (12,024T), 4.9 bar avg hold. Exit too tight.
- LC-2025-008: Gap accel filter on vol_filter — FAILED. accel < 1.0 incompatible with 3.0% entry. Divergent trade WR ~28.0% (filter removed signal, not noise). Lead #2 retired.
- LC-2025-009: ATR isolation on broad universe — PASS (marginal). [EXIT] +1.63pp WR, +1,186.9pp PnL. EXP-016 direction confirmed, magnitude smaller. ATR valid component but does not fix core edge problem.
- LC-2025-010: IDEA-018 combined overextended entry filter — FAILED. AND-subset (gap >4% AND vol >5x, 316 trades) showed +1.12pp WR *above* baseline (29.10% vs 27.98%). Hypothesis refuted. Source findings EXP-012/EXP-021 confirmed as hand-picked artefacts. IDEA-018 retired.
- LC-2025-011: RVOL threshold sensitivity — marginal PASS on direction, FAIL on magnitude. [ENTRY] Higher volume_ratio_ema threshold (2.0→5.0) improves WR +3.51pp but all thresholds net negative. Stable +0.035pp WR per 1% trade reduction. Divergent set (2.0-only) WR 28.80%. RVOL is a working knob but cannot fix core edge problem.

## Book knowledge (key extracts)

- (populated over sessions)
