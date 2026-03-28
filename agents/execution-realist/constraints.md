# Execution Constraints Reference

> Last updated: 2026-03-28

This is a living reference of known execution constraints for the YOLO trading stack. The Execution Realist agent must reference this document — not assume from memory.

---

## Trading 212 API

- **Order types:** Market and Limit orders only
- **Typical latency:** 100-500ms round-trip for order placement
- **Rate limits:** 30 requests/minute for equity orders
- **Position size:** Minimum notional varies by instrument; fractional shares supported
- **Market hours:** Orders execute during market hours only; queued orders outside hours

## Polygon.io Data

- **1-min bars:** Delayed by aggregation window (bar not available until close of that minute)
- **WebSocket streaming:** Sub-second tick data available but subject to network jitter
- **Known timestamp offsets:** 1-minute offset observed between Polygon timestamps and Webull — T212 alignment is unverified and must be resolved before live trading
- **Data format:** Bars include open, high, low, close, volume, VWAP

## VPS Infrastructure

- **Host:** srv1161923.hstgr.cloud (72.61.203.132)
- **Spec:** 2 CPU cores, 8 GB RAM, 100 GB disk
- **OS:** Ubuntu 24.04 LTS
- **Python:** 3.12+
- **Implication:** No GPU, no sub-millisecond timing guarantees. Strategies requiring sub-second decision-making are not implementable on this stack.

## Entry Price Reality

- **bar_close[B0] is not transactable.** The close price of a signal bar is known only after the bar closes. A real trader cannot enter at bar_close[B0] — they would enter at bar_open[B1] at the earliest.
- **Spread impact:** Market orders fill at ask (buy) or bid (sell), not mid-price. Typical spread for small-cap momentum stocks: 0.5-2.0% of price.
- **Slippage:** Additional slippage on market orders during high-volatility moments (news, open, close).

## Known Open Issues

1. **Polygon-T212 timestamp offset:** 1-minute offset found vs Webull. T212 alignment is unverified. Must be resolved before any live trading decisions rely on cross-source timestamps.
2. **EMA seeding:** EMA9 seeded from first bar of day — confirmed consistent with Webull. Not an issue but worth noting for reproducibility.
