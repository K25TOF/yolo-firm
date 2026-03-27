# Optimist Memory

## Research Principles

**Attribution matters:** Every experiment result must be attributed to scanner filter (universe), entry point, or exit point. When results are mixed, drill into which trades diverged. Classify before drawing conclusions.

**Trade log interrogation:** Aggregate metrics answer "did this config help?" — trade log analysis answers "what do winning trades look like?" Both are always required. Segment winners vs losers across scanner, entry, and exit factors.

**Stage-of-move dependency:** High EMA gap AND high volume co-occurrence is ambiguous — it marks momentum confirmation on early-stage runners and exhaustion on late-stage faders. The broad universe contains both in roughly equal proportion. Neither indicator is a directional loser filter without controlling for stage of move.

**Survivorship-selection bias discipline:** Any population filtered by full-day outcome (e.g., HOD-LOD ≥ 100%) produces clusters that describe what winners looked like in hindsight, NOT what predicts winners going forward. The forward base rate — what % of days showing pattern X through time T go on to achieve the qualifying outcome — is always required before any actionability claim is valid.

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

## LC-2025-014 — Volume Profile Clustering (100%+ Intraday Movers)

### Population
1,922 ticker-days, 1,056 unique tickers, May 2025–Mar 2026. HOD/LOD ≥ 100% qualification uses full-day data including pre/post market. 110,240 total scanned = 1.7% qualify.

### Six Clusters
1. EARLY_SPIKE (114, 5.9%): >50% vol first 30 min. Med range 140%, $vol $344K, price $1.85. Peak 09:40.
2. MORNING_FRONT (107, 5.6%): First hour >60% vol, not first-30-min concentrated. Med range 145%, $vol $524K, price $2.08. Peak 10:00.
3. MIDDAY_BUILDUP (319, 16.6%): Peak vol 11:00-13:00. Med range 140%, $vol $20.7M, price $3.01. Peak 12:00.
4. AFTERNOON_SURGE (463, 24.1%): >40% vol last hour, 58% final 10-min bucket. Med range 154%, $vol $66.6M, price $3.50. Peak 15:50.
5. MULTI_SPIKE (512, 26.6%): 2+ spikes >10 buckets apart. Med range 150%, $vol $22.8M, price $3.01. Peak 13:10.
6. EVEN_DIST (407, 21.2%): No dominant period, 81% first-half vol. Med range 151%, $vol $20.7M, price $3.25. Peak 11:00.

### Cluster Assessments (Final Revised Positions)

| Cluster | Assessment | Status |
|---|---|---|
| EARLY_SPIKE | Size-constrained — $vol percentile data needed before any scanner work | Provisional |
| MORNING_FRONT | "Highest priority" ranking retracted — requires intra-hour arrival curve + forward base rate | Hypothesis only |
| MIDDAY_BUILDUP | Real liquidity ($20.7M) — second priority provisional pending base rate | Provisional |
| AFTERNOON_SURGE | **Likely artefact (default).** 44x uniform rate in final bucket = structurally dominant, not additive. Disproof required before scanner use | Deprioritised |
| MULTI_SPIKE | Skip-first connection (EXP-022) is hypothesis in good standing, not finding. Requires: bucket definition, price trajectory, EXP-022 universe overlap | Hypothesis |
| EVEN_DIST | Grinder profile connection is hypothesis, not finding. Requires grinder entry criteria cross-check | Hypothesis |

### Key Methodological Findings
- **Survivorship-selection bias:** All clusters selected by full-day outcome. Forward base rate entirely absent — blocks all actionability claims.
- **Peak price times are backward-looking** — scanner timing arguments invalid without volume arrival curves.
- **Clusters describe types of days, not types of stocks** — 1,056 tickers in 1,922 days means same ticker can appear in multiple clusters.
- **Cluster boundaries are threshold-based, not data-derived** — sensitivity to threshold choice unexamined.

### Blocking Data Items (Required Before Any Scanner Design)
1. Forward base rate: what % of days showing cluster X's early-day volume pattern go on to achieve 100%+ range?
2. Intra-hour volume arrival curves: at what intraday timestamp does each cluster's defining pattern become detectable?

### High-Priority Hypotheses for Next Session
- **MULTI_SPIKE × skip-first (EXP-022):** Test requires bucket definition, price trajectory confirmation (does price rise into 2nd spike?), EXP-022 universe overlap check.
- **AFTERNOON_SURGE artefact test:** ETF/index membership cross-reference + intraday price trajectory.
- **EVEN_DIST × grinder:** Apply actual grinder entry criteria (EMA gap 1.0%+ above VWAP) to EVEN_DIST days.
- **Cluster predictability from pre-market conditions:** For tickers appearing in 2+ clusters on different days, cross-tab pre-market $vol / gap % / catalyst type vs. cluster assignment. If cluster is predictable pre-open, survivorship bias is partially resolved.

## LC-2025-014 — ORB Breakout Entry Research

### Multibagger Universe (Quality Filter)
450 ticker-days from 1,922 runners surviving: mcap ≥ $10M AND type=CS AND exchange ∈ [XNAS, XNYS, ARCX] AND float_turnover ≥ 0.50x. Float turnover = day_dollar_volume / (free_float × open_price). Natural breakpoint at 0.50x separating genuine momentum from noise. Stored: `analysis/tools/lists/lc025014_multibagger_universe_v1.json`.

### ORB Definition
- ORB window: first 15 min of RTH (09:30–09:44 ET, ts_minute 570–584)
- ORB high = max(bar_high) in ORB window
- ORB low = min(bar_low) in ORB window
- **Critical:** minute_of_day ≠ minutes since RTH open. For RTH bars, minute_of_day starts at ~28. ORB exclusion must use `ts_minute < 585`, NOT `minute_of_day < 15`.

### Entry Conditions (Settled)
1. B0: first bar after 09:45 (ts_minute ≥ 585) where `bar_high ≥ orb_high` AND `vol_ratio ≥ 2.0x`
2. B-1 coil: bar before B0 closes no deeper than -4% below ORB high: `(close[B-1] - orb_high) / orb_high ≥ -0.04`
3. Liquidity gate: dollar volume EMA3 (k=0.5, bars B-2/B-1/B0) ≥ $10K/min at B0

**Ruled out:**
- B+1 confirmation as entry filter: forward bias — bar after entry cannot be observed at entry time
- Time-of-day filters: coincidental, not causal
- EMA3 volume (share count): zero discrimination at full sample

### Entry Signal Files
- **V1 (5-min ORB, ts_minute 570–574, 09:30–09:34 ET) — PRIMARY RESEARCH TRACK.** `analysis/tools/lists/lc025014_orb_confirmed_v1.json` — 128 entries (B0 + B-1 + B+1). **Immutable per policy.**
- **V2 (15-min ORB, ts_minute 570–584, 09:30–09:44 ET) — RETIRED VARIANT.** `analysis/tools/lists/lc025014_orb_entries_v2.json` — 171 entries (B0 + B-1 only; B+1 retired). Generated after ORB window bug fix. Retired: model multiplicity concern (LC-2025-015 FA1), results must not be combined with V1.

### PO Feedback Summary
**V1 / 5-min ORB (128 entries, 54% Good) — PRIMARY:** 69G / 18N / 41B. Good entries: earlier arrival (10:05 vs 10:31 Bad), higher VR (3.9x vs 3.1x). Bad categories: wrong marker (7), robotic/algo (4), fakeout (1), low volume (2), late entry (4), no reason (24).

**V2 / 15-min ORB (170 entries, 48% Good) — RETIRED:** 81G / 15N / 74B. Volume ratio inverted: Bad median 4.0x > Good 3.4x (exhaustion signal at extremes). Bad categories: liquidity (5), late entry (2), robotic (1), no reason (63). Retired due to model multiplicity concern (LC-2025-015 FA1).

### Clean Tradeable Universe (Final State)
298 rated entries (128 V1 + 170 V2) → 236 after $10K/min liquidity gate.
- 132G / 104B / ~28N ≈ 56% Good rate after gate (in-sample, unreconciled — see Challenger caveats)
- Liquidity is a prerequisite filter, not a signal discriminator (Good/Bad ratio unchanged by gate)
- Entry price = orb_high (for backtesting, entry_price is the ORB high level)
- **V1 (5-min) is the primary research track going forward.** V2 (15-min) retired — results must be analysed separately, not combined.

### Key Technical Findings
- **ORB window bug**: `minute_of_day < 15` excludes pre-market, NOT the ORB window. Fix: `ts_minute < 585`.
- **Volume ratio at extremes is ambiguous**: both v1 and v2 show VR is not a monotone quality signal. At very high VR (>4x), exhaustion dominates.
- **Liquidity is neutral**: applying $10K/min gate removes ~21% of entries but does not change Good/Bad ratio — confirms gate is binary prerequisite.
- **~50% Good rate** on 236 tradeable entries is the current baseline for ORB entry research.
