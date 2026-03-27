# LC-2025-014 — ORB Breakout Strategy: Revised Summary (2026-03-27)

## 1. STRATEGY OVERVIEW

### Universe
- **Runner population:** 1,922 ticker-days where `(max(bar_high) - min(bar_low)) / min(bar_low) >= 1.0` across all bars (incl pre/post market). 1,056 unique tickers, May 2025 – Mar 2026.
- **Multibagger universe:** 450 ticker-days from the 1,922, filtered by:
  - `market_cap >= $10M`
  - `type == "CS"` (common stock only)
  - `primary_exchange in ["XNAS", "XNYS", "ARCX"]`
  - `float_turnover >= 0.50` where `float_turnover = day_dollar_volume / (free_float_shares × open_price)`
- **Tradeable entries:** 236 entries after $10K/min liquidity gate (from 298 PO-rated entries: 128 v1 + 170 v2)

### Entry Rules (ORB 5-Minute Breakout)
- **ORB window:** First 5 minutes of RTH (ts_minute 570–574, 09:30–09:34 ET)
- **ORB high:** `max(bar_high)` across all 1-min bars in ORB window
- **B0 (breakout bar):** First bar at ts_minute >= 575 (09:35 ET) where:
  - `bar_close >= orb_high`
  - `vol_ratio >= 2.0` where `vol_ratio = bar_volume / SMA(volume, 20 prior bars)`
- **B-1 (coil):** `(bar_close[B-1] - orb_high) / orb_high >= -0.04` (bar before B0 closes within 4% below ORB high)
- **Liquidity gate:** `EMA3(bar_volume × bar_close, k=0.5) over bars [B-2, B-1, B0] >= $10,000/min`
- **Entry price:** `bar_close[B0]`

### Exit Rules (Current Baseline + Proven Additions)

**Layer 1 — Hard stop (safety floor):**
- Exit if `(current_close - entry_price) / entry_price <= -10%`
- Always active from entry. Runs alongside all other exit rules.
- Evidence: `-10%` ties with `-7%` for best EV delta (+0.11pp vs no stop), preserves 75% of runners. 96.5% of genuine runners reach +10% profit before hitting this stop. Runners that dip past -10% have bad entries (PO-confirmed).
- Scripts: `zz_phase1_fixed_stop.py`, `zz_stop_evaluation.py`

**Layer 2 — EMA9 trend exit (primary exit):**
- Exit when 4 consecutive 5-min bar closes are each below EMA9(5m)
- `EMA9: ema[i] = close[i] × 0.2 + ema[i-1] × 0.8`, seeded at first bar of day, no intraday reset
- 5-min bars: aggregate 1-min bars into 5-min buckets (close = last 1-min close in bucket)
- Evaluation starts at first 5-min bucket AFTER the bucket containing B0
- Fallback: exit at RTH close (16:00 ET) if never triggered
- This is called `ema9_5m_d3` in the codebase (d3 = delay 3, meaning 3+1=4 consecutive bars)

**Layer 3 — Runner guard (proven on >50pp decline cluster):**
- Activates only on trades that have run significantly above entry
- Exit when ALL three conditions are true simultaneously:
  - `bar_close < EMA5(1m)` (price below 1-minute EMA5)
  - `RSI(14, 1m) < 40` (momentum weak)
  - Price stays below EMA5(1m) for 5 consecutive bars (no recovery)
- Evidence: 14/49 improved, 0/49 hurt, +2.16pp mean on >50pp decline cluster
- Does NOT generalise to 20–50pp cluster (net negative there)
- Script: `zz_phase3j_guard.py`

### Additional Proven Entry Filters (Not Yet Applied)
- **Robotic ticker blacklist:** CIGL, UFG, BCDA, TOPP (always Bad in PO review, zero Good)

### Key Metrics
- **PO-rated entries:** 132 Good / 104 Bad / ~28 Neutral out of 236 tradeable (~56% Good rate)
- **Baseline mean PnL (ema9_5m_d3):** +38.21% on 132 Good entries (Phase 2 sweep)

---

## 2. RESEARCH COMPLETED

### Phase 1 — ATR Trailing Stop Sweep
- **Population:** 132 Good entries
- **Variants:** 20 (ATR periods 5/10/14/20 × multipliers 1.0/1.5/2.0/2.5/3.0)
- **Result:** All underperform baseline. Rank-1 ATR mean +15.29% vs baseline +38.21%. All 132 trades had stop triggered before RTH close. Higher multiplier always better; no dominant period. 78% of per-trade rank-1 go to EMA9.
- **Conclusion:** ATR trailing stops cut runners short. Dropped.

### Phase 1b — Fixed Stop-Loss Sweep (MAE Analysis)
- **Population:** All 236 entries (6,790 total with re-entries)
- **Variants:** -3%, -5%, -7%, -10%, -15%, -20%, -25%, -30%
- **Key results:**

| Stop | Stopped | Failures cut | Runner survival | EV delta |
|---|---|---|---|---|
| -7% | 741 | 513 (67.0%) | 62.9% | +0.11pp |
| -10% | 334 | 248 (32.4%) | 75.0% | +0.11pp |
| -15% | 113 | 71 (9.3%) | 86.1% | +0.07pp |
| -20% | 41 | 27 (3.5%) | 95.0% | +0.05pp |

- **Also tested (stop_eval_summary.csv):** hard_3/5/7/10, ema9_1m_d0/d1, ema9_5m_d0, orb_return. Runner survival to +10% profit: hard_10 = 96.5%, hard_7 = 91.5%, ema9_1m_d0 = 20.1%.
- **Conclusion:** -10% hard stop is safety floor. Ties -7% on EV, better runner survival. PO confirmed runners dipping past -10% had bad entries.

### Phase 2 — EMA9 Exit Sweep
- **Population:** 132 Good entries
- **Variants:** 8 (timeframes 1m/5m × delay values d0/d1/d2/d3)
- **Result:** 5-min beats 1-min by ~10pp on average. Best variant mean +42.72% vs baseline +38.21%. Per-trade optimal variant differs — confirms adaptive exit hypothesis.

### Phase 3 — Ideal Exit Target
- **Population:** 3,664 graduating trades (1-min close >= entry_price × 1.05)
- **Defined:** peak_pnl (highest close between graduation and ema9_5m_d1 exit) as the theoretical ceiling. Prize = peak_pnl - ema9_5m_d3_pnl.

### Phase 3a — Pre-Entry Classification
- **Population:** 3,664 graduating trades
- **Features tested:** gap_pct, vol_ratio, b1_coil_pct, liq_ema3, pm_volume
- **Result:** No single feature reliably classifies runner (MFE>=10%) vs middle (MFE 5-10%) at entry time.
- **Conclusion:** Entry-time prediction dropped. Shifted to in-trade adaptive approach.

### Phase 3b — In-Run Exhaustion Signals
- **Population:** 3,664 graduating trades (separate results for runners/middles)
- **Signals:**
  - A: bars since new high (1-min close). N = 5, 10, 15, 20, 30
  - B: EMA9-5m gap drop from peak ratio. Delta = 0.02, 0.04, 0.06, 0.08, 0.10
  - C: M consecutive 5-min volumes below Y% of graduation-bar volume. Y=20/30/40/50%, M=2/3
- **Results (runners):** A_bars30: -1.02pp vs baseline. C_vol20x3: -0.52pp. B_gap10: -0.66pp.
- **Conclusion:** No signal beat baseline on average. All dropped.

### Phase 3c/3d — Combined Score + Trailing Stop
- **Population:** 3,664 graduating trades
- **Signals:**
  - S1: `close < ATH_since_graduation × (1 - trail_pct)`. Trail: 3-20%
  - S2: `RSI(14, 1m) < threshold`. Threshold: 30, 40, 50, 60
  - S3: bars since new high (wick) > threshold. Threshold: 5, 10, 15
  - S4: N consecutive bars with accelerating negative delta. N = 2, 3
- **Combined:** Each signal = 1 point. Exit when score >= 1/2/3/4.
- **Results (runners):** trail15%: -0.15pp, trail20%: -0.17pp, S4_acc3: -0.88pp.
- **Conclusion:** No combination beat baseline on average. Individual signals noisy. Dropped.

### Phase 3e — Decline Window Measurement
- **Population:** Runners (MFE >= 10%) from graduating trades
- **Defined:** `decline_pp = peak_high_pnl - d3_pnl` (gap between peak wick and EMA9 exit)
- **Clusters:**
  - >50pp: 57 trades (49 with valid data)
  - 20-50pp: 252 trades (237 valid)
  - 10-20pp: 421 trades
  - <10pp: 1,119 trades
- **Insight:** Reframed research from "beat d3 on all trades" to "target specific decline clusters."

### Phase 3f — Signal Calibration on >50pp Cluster
- **Population:** 49 valid trades from >50pp cluster
- **Method:** Find parameters where signal fires in decline but NOT in run-up.
- **Results:**
  - S2 RSI<40: 5/49 run-up FP (10.2%), 45/49 decline TP (91.8%)
  - S2 RSI<30: 1/49 FP (2.0%), 30/49 TP (61.2%)
  - S3 bsh>5: 38/49 FP (77.6%) — too noisy
  - S4 n=2: 48/49 FP (98.0%) — too noisy
- **Conclusion:** RSI is the most selective signal. S3 and S4 too many false positives.

### Phase 3g — RSI-Armed Exit Switch
- **Population:** >50pp cluster (49 valid)
- **Concept:** Once RSI(14,1m) < T, switch from d3 (4 bars) to tighter exit (fewer bars).
- **Top results:** RSI<45 d0: 57.1% improved. RSI<50 d1: 65.3% improved.
- **Conclusion:** Superseded by guard approach (Phase 3j).

### Phase 3h — Profit-Level Arming
- **Extension:** RSI switch only arms above +20/+30/+40/+50% profit.
- **Result:** No improvement over ungated RSI switch.
- **Conclusion:** Profit gating unnecessary. Dropped.

### Phase 3i — EMA Variant Reverse Engineering
- **Population:** >50pp cluster (49 valid)
- **Variants:** 32 (5-min periods 3/5/9/12/20 × c1-c4 = 20; 1-min periods 5/9/20 × c1-c4 = 12)
- **Results (top 5):**

| Variant | Rank-1 count (/49) | Mean pp_saved |
|---|---|---|
| 1m_e5_c1 | 31 | 41.59pp |
| 1m_e5_c2 | 7 | 34.71pp |
| 1m_e9_c1 | 1 | 33.99pp |
| 5m_e3_c1 | 6 | 29.74pp |
| 1m_e9_c2 | 0 | 28.67pp |

- **Conclusion:** 1m_e5_c1 (1-min EMA5, 1 bar below → exit) is the best raw exit for runners, but fires during run-up. Needs a guard.

### Phase 3j — Guard Logic for 1m_e5_c1
- **Population:** >50pp cluster (49 valid)
- **Approaches tested:**
  - A: RSI gate only (exit when 1m_e5_c1 AND RSI < T)
  - B: Recovery window (wait M bars; cancel if recovers above EMA5)
  - C: AND gate (RSI < T AND no recovery for M bars)
  - D: Tiered (different response by RSI level)
- **Sweep:** A: T=30/35/40/45/50. B: M=2/3/5/8. C: T×M = 9 combos. D: 3 tier combos.
- **Winner:** Approach C, RSI<40, M=5 → 14/49 improved, 0/49 hurt, +2.16pp mean

### Phase 3k — Diagnosis and Cluster Validation
- **Q1 — Why 35/49 unchanged by guard:**
  - 16 window_too_short: RSI fired but <5 bars before d3 exit (min RSI 33-39)
  - 9 rsi_never_fires: RSI bottomed 41-50 in decline
  - 9 always_recovered: price bounced above EMA5 within 5 bars each time
  - 1 unknown
- **Q2 — Second layer candidates (on 35 unchanged only):**
  - C rsi<45 M=5: 3 run-up FP, 17 TP, +4.20pp combined
  - C rsi<45 M=8: 1 FP, 6 TP, +1.86pp combined
  - No zero-FP candidate exists
- **Q3 — Guard on 20-50pp cluster (237 valid):**
  - 53/237 improved, 49/237 hurt, 9/237 run-up FP, mean -0.60pp
  - Guard does NOT generalise from >50pp to 20-50pp

---

## 3. ENTRY QUALITY FINDINGS

### B+1 Bar Divergence (from PO chart review, 22 Good + 10 Bad/Neutral)

| Bar | Good close vs ORB | Bad close vs ORB | Good % green | Bad % green |
|---|---|---|---|---|
| B-5 | -3.05% | -6.70% | 57% | 40% |
| B-1 | -1.25% | -1.66% | 73% | 90% |
| B0 | +2.74% | +3.11% | 95% | 90% |
| B+1 | +3.94% | +1.94% | 68% | 20% |
| B+2 | +4.18% | +0.91% | 36% | 30% |

- B0 does NOT discriminate. B+1 is strongest divergence (48pp green-rate gap).
- Good stocks approach ORB gradually (B-5: -3.05%); Bad come from further below (-6.70%).
- Sample size: 32 trades. Not yet validated on full 236.

### Time of Day
- Good entries median: 10:05 ET. Bad median: 10:31 ET.
- Not yet validated with distribution analysis or held-out data.

### VR at Extremes
- v2 review: Bad median VR 4.0x > Good 3.4x (possible exhaustion at very high VR).
- Full distribution not analysed. Flagged as blocking issue by Challenger.

---

## 4. TOPICS DROPPED AND WHY

| Topic | Phase | Data reason |
|---|---|---|
| ATR trailing stop | Phase 1 | All 20 variants mean +15.29% vs baseline +38.21%. Stops always fire. |
| Pre-entry classification | 3a | No single feature reliable for runner vs middle classification |
| Exhaustion signals A/B/C | 3b | All negative delta vs baseline. Best: -0.52pp. |
| Combined score | 3c/3d | No combination beat baseline on average |
| S4 accelerating velocity | 3f | 48/49 run-up FP (98%) |
| S3 bars-since-high standalone | 3f | 38/49 run-up FP (77.6%) |
| Profit-level arming | 3h | No improvement over ungated switch |
| RSI-armed d3 switch | 3g | Superseded by 1m_e5_c1 guard approach (Phase 3j) |

---

## 5. OPEN LEADS

1. **Guard for 20-50pp cluster** — 237 trades, needs separate calibration. >50pp parameters don't transfer.
2. **16 "window too short" trades** — RSI correctly fires but M=5 can't complete. Shorter M + stricter RSI?
3. **B+1 green as entry filter** — 48pp green-rate gap. Needs validation on full 236 entries.
4. **Fixed target for middle trades (MFE 5-10%)** — Quick pops that d3 lets evaporate. +7% target?
5. **Time-of-day filter** — Good median 10:05 vs Bad 10:31. Needs distribution analysis.
6. **VR ceiling** — Bad VR 4.0x > Good 3.4x at extremes. Needs full distribution.
