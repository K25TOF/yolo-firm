# Optimist Memory

## Research Principles

**Attribution matters:** Every experiment result must be attributed to scanner filter (universe), entry point, or exit point. When results are mixed, drill into which trades diverged. Classify before drawing conclusions.

**Trade log interrogation:** Aggregate metrics answer "did this config help?" — trade log analysis answers "what do winning trades look like?" Both are always required. Segment winners vs losers across scanner, entry, and exit factors.

**Stage-of-move dependency:** High EMA gap AND high volume co-occurrence is ambiguous — it marks momentum confirmation on early-stage runners and exhaustion on late-stage faders. The broad universe contains both in roughly equal proportion. Neither indicator is a directional loser filter without controlling for stage of move.

## Strategy Knowledge

- Active strategy: vol_filter_ema10 v2.0.0 — net positive on hand-picked sets, net negative on broad momentum universe
- Known trade profiles: impulse (vol_filter), grinder (IDEA-016/HYP-025)
- Skip-first filter: +75.2pp improvement (EXP-022) — strongest confirmed edge
- ATR exit: confirmed directionally positive (+1.64pp WR on broad universe), real but smaller than hand-picked results

## Alternative Angles Not Yet Explored

- Squeeze indicators (untested)
- Force index (untested)
- Time-of-day entry segmentation
- Multi-timeframe confirmation
- Grinder profile with corrected exit rule (entry 1.0%, exit 0.5%) — original test had inverted exit rule, results contaminated

## Momentum Universe

Standard filter: `(day_high - day_low) / day_low >= 0.50`. Yields ~5.6% of cached pairs (5,755 / 103,554). All momentum strategy research must use this filter. Results without it include noise from non-moving tickers.

## What Has Worked (Directionally)

- Skip-first filter: strongest confirmed edge
- ATR trailing stop: marginal but real improvement on broad universe
- RVOL threshold: higher threshold = fewer trades + higher WR (stable +0.035pp WR per 1% trade reduction)
- Grinder entry signal (ema_gap 1.0% + VWAP 2%) has not been fairly evaluated due to inverted exit rule error

## Session History Highlights

- LC-2025-009: ATR isolation — PASS (marginal), confirmed EXP-016 direction
- LC-2025-011: RVOL sensitivity — working knob but insufficient alone
- HYP-025: Grinder concept not invalidated — exit design was proximate cause of failure, not entry signal
