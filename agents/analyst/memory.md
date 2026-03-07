# Analyst Memory

## Momentum Universe Filter

When interpreting backtest results, check whether `momentum_universe` was enabled:

- **Definition:** Filters ticker-date pairs to only those with >= 50% intraday range: `(day_high - day_low) / day_low >= 0.50`
- **Impact on results:** Removes low-volatility pairs that would produce no signals anyway. Win rates and PnL are comparable only across experiments using the same universe setting.
- **Standard for momentum strategies:** All vol_filter, grinder, and momentum research should use `momentum_universe: true`. Results without it include noise from non-moving tickers.
- **Check in results:** `pairs_skipped_momentum` shows how many pairs were filtered out. High skip counts are expected and normal.

## Strategy knowledge

- Active strategy: vol_filter_ema10 v2.0.0 (82T, 46% WR, +158.9% on 49 tickers)
- Known trade profiles: impulse (vol_filter), grinder (IDEA-016/HYP-025)
- Closed hypotheses: none — HYP-025 Phase 1 status revised (see below)

## Research patterns

- What has worked: skip-first filter (+75.2pp improvement EXP-022), non-accelerating gap (EXP-021)
- What has failed: HYP-024 VWAP distance filter (inconclusive, +4.2pp below +5pp bar)
- Indicators not yet tested: squeeze indicators, force index
- Indicators tested: ema_gap_acceleration (registered and working — used in HYP-025 Phase 1)

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
- Acceleration filter: Strong — EXP-021 showed accelerating gap predicts -54.9% PnL; DIAG-A2 (LC-2025-002 audit) confirmed +5.8pp WR improvement from filter (239→109 trades, 50.2%→56.0%)

**Result:** Phase 1 INCONCLUSIVE — config error (exit rule inversion) prevents fair evaluation. Original -353.6% P&L / 28.6% WR verdict does not stand. Re-test required.

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

## Book knowledge (key extracts)

- (populated over sessions)
