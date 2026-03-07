# Engineer Memory

## Engine knowledge

- Current indicator set: 25 registered (ema_gap, vwap_session, volume_ratio_ema, atr, bb_width, kc_width, squeeze_on, squeeze_momentum, force_index, kama, etc.)
- Known engine limitations: mid-candle ordering (backtest uses bar close, live uses real-time updates)
- Prototype scripts available: batch_historical.py, walk.py (shared walk logic)

## Experiment patterns

- Common failure modes: tight AND filters produce too few trades for statistical significance
- Data quality issues observed: VWAP noisy on sub-$1 stocks (bid-ask 1-5%), single blocks shift VWAP 0.5-2%
- Cache state: 49 tickers cached for Feb 10–Mar 4 period

## Grinder Strategy Backtest Plan (HYP-025)

**Indicators required:**
- ema_gap (registered)
- vwap_session (registered)
- atr (registered)
- ema_gap_acceleration (NEW — 3-bar ROC, 15-min registration effort)

**Phase 1 scope (PO-approved):**
- Entry: ema_gap 1.0% + VWAP 2% + acceleration < 1%
- Exit: ema_gap 2.0% OR VWAP break OR ATR 1.5x
- Dataset: 49 tickers, Feb 10–Mar 4 (same as EXP-023)
- Target: 40%+ win rate, measurable improvement on vol_filter-skipped tickers
- Effort: 45 min walk + 15 min indicator = 60 min

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
