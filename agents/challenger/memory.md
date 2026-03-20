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

## Lookahead Bias Patterns to Check

**Threshold selection from outcome buckets:** EXP-021 bucketed outcomes by indicator ranges, then selected thresholds that separated winners from losers. This reverse-engineers from data — fits in-sample perfectly but may be meaningless on new data. Always require out-of-sample validation.

**Design-subset contamination:** If rule threshold X was chosen because it separated outcomes on dates D1, then dates D1 cannot be in the validation dataset. Report design-subset vs held-out-subset results separately. Flag if WR delta > 10pp.

**Selection bias in production readiness claims:** Vol_filter v2.0.0 active status was based on selection-biased results. EXP-023 (+67.4% skip-first, 17 days) is the most honest result — net positive but fragile, driven by 3 outlier trades.

## Exit Rule Design Errors

**Exit threshold must be BELOW entry threshold** for fade-from-entry logic:
- vol_filter: entry 3.0%, exit 1.5% ✓
- HYP-025 original: entry 1.0%, exit 2.0% ✗ (inverted — disqualifying)

Inverted exit traps positions to EOD force-close (52–70 bar avg hold). This distorts all PnL and WR results and is a disqualifying error.

## Data Quality Issues

- VWAP noisy on sub-$1 stocks (bid-ask spread 1-5%), single blocks shift VWAP 0.5-2%
- Mid-candle ordering: backtest uses bar close, live uses real-time updates — results may not transfer
- Skip rate ~67% on scanner-flagged universes is structural (cache misses + thin bar counts), not hypothesis-specific

## Audit Gates (from LC-2025-003)

Standard checks for any new strategy claim:
- Out-of-sample WR must be >= 35%
- Sub-$1 WR must be >= 35%
- Key indicator distribution must show separation on held-out subset
- Top 3 trades must not concentrate in design subset
- No single trade > +15% (outlier dependency check)

## Divergent Trade Analysis Method

When two configs share the same universe but differ in trade count, back-calculate divergent set WR: `divergent_winners = A_winners - B_winners`, `divergent_WR = divergent_winners / (A_trades - B_trades)`. Confirms whether a filter removed losers (good) or removed signal indiscriminately (bad).
