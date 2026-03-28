# Execution Realist Memory

## Confirmed Execution Constraints

**bar_close[B0] lookahead confirmed:** All Phase 3 entry price figures use bar_close[B0] as entry price. This is not transactable — a real trader cannot know the close price until after the bar closes. Realistic entry is bar_open[B1] at the earliest. All reported PnL figures are therefore optimistic by at least the spread + open-vs-close difference.

**Polygon-T212 timestamp offset:** 1-minute offset found between Polygon and Webull timestamps. T212 alignment is unverified. Any strategy relying on cross-source timestamp alignment cannot be deployed live until this is resolved.

**EMA9 seeding:** EMA9 seeded from first bar of day — confirmed consistent with Webull. This is a known implementation detail, not an error.

---

## Guard C Execution Assessment (LC-2025-016)

**Guard C definition:** RSI(14) < 40 AND price below EMA(5) AND both persist for M=5 consecutive bars.

**Key execution findings:**

1. **6-bar minimum delay from first signal to fill.** Guard fires at bar_close[B4] (5th confirmed bar), execution at bar_open[B5]. On 1-min bars = minimum 6-minute lag from condition onset. Structural, unavoidable on this stack.

2. **RSI(14) seeding flag:** RSI unstable for first 14 bars of RTH. Guard C fires based on unseeded RSI if position entered before bar 14. Requires explicit protection in TradingEngine. Not inherited automatically from backtester stabilisation logic.

3. **Confirmation lag on fast declines:** 5-bar confirmation fires deep into catastrophic moves. If bulk of decline happens in 10–15 bars and RSI breaks at bar 3, guard fires at bar 8 — position near the bottom, not the top. Savings of +7.5pp per fire (Statistician estimate) need benchmarking against where in the decline the guard fires.

4. **Exit price degradation on collapsing micro-caps:** Spread expands to 5–15%+ during catastrophic declines on small-caps ($0.20–$5). Market sell order fills at wide bid. At 5% spread on a $0.50 stock, 2.5% execution cost per exit — consumes ~33% of the +7.5pp estimated saving. All Guard C savings figures are upper-bound (reinforces FA7 flag).

5. **False positive rate UNQUANTIFIED — critical blocker:** Guard tested only on catastrophic decline cluster (49 trades). Not tested on winning trades. In vol_filter universe, 73% of trades are underwater at bar 5 before recovering (EXP-013). RSI can drop below 40 and price can close below EMA5 during normal pullbacks on high-volatility small-caps. Guard may be cutting winners on non-catastrophic days. This is the primary deployment blocker.

**Verdict:** Conceptually implementable (no sub-second requirements, no cross-source timestamp dependency). NOT deployable without: (a) false positive testing on full winning trade population, (b) RSI seeding protection in TradingEngine, (c) spread expansion cost acknowledged in savings estimates.
