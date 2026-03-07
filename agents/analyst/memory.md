# Analyst Memory

## Strategy knowledge

- Active strategy: vol_filter_ema10 v2.0.0 (82T, 46% WR, +158.9% on 49 tickers)
- Known trade profiles: impulse (vol_filter), grinder (IDEA-016/HYP-025)
- Open hypotheses: HYP-025 Phase 1 (grinder entry/exit, PO-approved, awaiting backtest)

## Research patterns

- What has worked: skip-first filter (+75.2pp improvement EXP-022), non-accelerating gap (EXP-021)
- What has failed: HYP-024 VWAP distance filter (inconclusive, +4.2pp below +5pp bar)
- Indicators not yet tested: ema_gap_acceleration (needed for HYP-025), squeeze indicators, force index

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
- Acceleration filter: Strong — EXP-021 showed accelerating gap predicts -54.9% PnL

**Next:** Phase 1 backtest to validate core entry. Phase 2 (volume refinement) conditional.

## Lesson: Rule Design Must Be Segregated From Rule Validation

HYP-025 entry rules were designed using EXP-021 data (Feb 24–Mar 3). Using the same date range as validation (Feb 10–Mar 4) includes the design subset, inflating confidence.

**Pattern:** If rule threshold X was chosen because it separated outcomes on dates D1, then dates D1 cannot be part of the validation dataset. Always report design-subset vs held-out-subset results separately. Flag if WR delta > 10pp. See LC-2025-003 Risk #1.

**HYP-025 audit gate (LC-2025-003):**
- Feb 10–23 WR must be >= 35% (true out-of-sample)
- Sub-$1 WR must be >= 35% (validates VWAP rule isn't slippage artifact)
- Gap_accel distribution on Feb 10–23 must show separation at 1.0% threshold
- Top 3 trades must not concentrate in Feb 24–Mar 3 (design subset)
- No single trade > +15% (outlier dependency check)

## Book knowledge (key extracts)

- (populated over sessions)
