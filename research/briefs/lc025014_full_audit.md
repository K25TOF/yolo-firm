# LC-2025-014 Full Audit Brief — Optimist + Challenger

## Objective

Thorough audit of ALL research conducted under LC-2025-014 (ORB 5-minute breakout strategy). Both agents review the same evidence independently, then challenge each other.

**Required outputs per focus area:**
1. **Confirmations** — findings that are methodologically sound and can be trusted
2. **Doubts / flags** — findings with potential errors, forward bias, insufficient evidence, or flawed methodology
3. **Recommendations** — specific next steps (re-test, extend, correct)
4. **New ideas** — actionable strategy ideas not yet explored. Objective: find strategies with a real edge on specific trade types. Quality over quantity. We are NOT looking for a single "fits all" strategy.

**Rules:**
- Every claim must reference specific data (file, number, sample size)
- Flag any conclusion drawn from fewer than 30 trades
- Flag any threshold that was derived from outcome-labelled data
- Flag any finding tested on a single population without out-of-sample validation
- Do not accept "dropped" as final — check if the reason for dropping was valid

---

## Focus Area 1: UNIVERSE AND ENTRY SIGNAL

### What to audit

**1a. Runner universe construction**
- 1,922 ticker-days where `(max(bar_high) - min(bar_low)) / min(bar_low) >= 1.0`
- This uses ALL bars including pre/post market for the range calculation
- Question: Does including pre/post market inflate the range? Would RTH-only ranges change the universe significantly?
- The 100% threshold — is this arbitrary? What's special about 100% vs 80% or 150%?

**1b. Quality filters**
- mcap >= $10M, type=CS, exchange in [XNAS, XNYS, ARCX], float_turnover >= 0.50
- Challenger flagged 6 blocking issues in the original session (per-cluster event counts, $5-10M band, PO review sampling, filter component isolation, unmatched ticker breakdown, survivorship bias)
- Were any of these resolved?
- float_turnover requires real-time float data — was lookahead bias cleared?

**1c. ORB window definition**
- Two variants exist: 5-minute (ts 570-574) and 15-minute (ts 570-584)
- v1 entry list uses 5-min ORB. v2 list uses 15-min ORB.
- The phase 3 exit research uses `lc025014_orb_5min_v1.json` (5-min ORB)
- Was the choice of 5 vs 15 minutes tested? Is there evidence one is better?

**1d. Entry conditions**
- `bar_close >= orb_high` — why close, not high? Does this miss breakouts where the wick breaks out but close doesn't?
- `vol_ratio >= 2.0` — threshold source? Was 1.5x or 3.0x tested? The orb-threshold session flagged survivorship bias risk in the 2.0x selection.
- B-1 coil >= -4% — threshold source? Was this calibrated from outcomes?
- Liquidity gate $10K/min — neutral per analysis (doesn't change Good/Bad ratio). Is it still needed?

**1e. Entry price**
- Entry at `bar_close[B0]` — in live trading, can we actually get this price? By the time we detect B0 has closed above orb_high, the next bar has started. Is there slippage bias?

### Evidence files
- `analysis/tools/lists/lc025014_orb_5min_v1.json` — 236 entries
- `analysis/tools/lists/lc025014_orb_entries_v2.json` — 171 entries (15-min ORB)
- `analysis/tools/lists/lc025014_multibagger_universe_v1.json` — 450 universe
- `analysis/scratch/zz_orb_5min_list.py` — 5-min ORB entry generation
- `analysis/scratch/zz_orb_entries_v2.py` — 15-min ORB entry generation
- `analysis/scratch/zz_runner_mcap_float.py` — quality filter logic
- `analysis/scratch/zz_runner_turnover.py` — float turnover computation

---

## Focus Area 2: HARD STOP ANALYSIS

### What to audit

**2a. Fixed stop sweep methodology**
- `zz_phase1_fixed_stop.py` tested -3% to -30% stops on 236 entries
- `zz_stop_evaluation.py` tested hard_3/5/7/10 + EMA variants on 6,790 entries
- Question: Why do these two scripts report different population sizes (236 vs 6,790)? Are re-entries counted separately?

**2b. -10% selection**
- -10% and -7% both show +0.11pp EV delta — tied
- -10% chosen over -7% because it preserves 75% vs 62.9% of runners
- PO confirmed runners dipping past -10% had bad entries
- Question: How was "bad entries" determined? Is this circular with the PO rating? Did we verify the specific trades that get stopped at -10% but survive at -20%?

**2c. Runner survival metric**
- 96.5% of runners survive to +10% profit before hitting -10% stop
- The 3.5% that don't — are these genuinely bad entries or just volatile runners?
- Is there a systematic pattern in the 70 runners stopped at -10%?

**2d. Interaction with other exits**
- Hard stop runs alongside EMA9 exit and guard. Has the combined effect been tested?
- Could a trade hit EMA9 exit before the hard stop, making the stop irrelevant for some trades?

### Evidence files
- `analysis/scratch/phase1_fixed_stop.csv` — sweep summary
- `analysis/scratch/phase1_mae.csv` — per-entry MAE data
- `analysis/scratch/stop_eval_summary.csv` — runner survival by graduation level
- `analysis/scratch/stop_eval_per_entry.csv` — per-entry stop results
- `analysis/scratch/zz_phase1_fixed_stop.py` — sweep script
- `analysis/scratch/zz_stop_evaluation.py` — evaluation script

---

## Focus Area 3: EMA EXIT RESEARCH (Phases 1-2)

### What to audit

**3a. ATR trailing stop dismissal**
- 20 variants all underperformed. Mean +15.29% vs baseline +38.21%.
- All 132 trades had stop triggered — stops always fire, cutting runners.
- Question: Was the ATR computed correctly? Wilder ATR with EMA3 smoothing — is this standard? Could a different ATR formulation (e.g., simple ATR, longer lookback) perform differently?
- Higher multiplier always better — does this suggest the issue is the multiplier range, not ATR itself? Was 4.0x or 5.0x tested?

**3b. EMA9 sweep**
- 8 variants: 1m/5m × d0/d1/d2/d3
- 5-min beats 1-min by ~10pp
- Best variant: +42.72% vs baseline +38.21%
- Per-trade optimal varies — "confirms adaptive exit hypothesis"
- Question: The +42.72% is cherry-picked (best variant). What's the variance? Is the improvement statistically significant across 132 trades?
- Was the 132-trade population (Good entries only) the right choice? What about all 236 entries?

**3c. EMA period choice**
- Only EMA9 was tested in Phase 2. Phase 3i later tested EMA3/5/9/12/20.
- Phase 3i found 1m_e5_c1 is rank-1 in 31/49 trades. But Phase 3i only tested on 49 trades (>50pp cluster).
- Was 1m_e5_c1 tested on the full 3,664 graduating trades? On the 132 Good entries?

### Evidence files
- `analysis/scratch/zz_orb_atr_sweep.py` — ATR sweep logic
- `analysis/scratch/orb_atr_sweep_trades.csv` — per-trade ATR results
- `analysis/scratch/zz_orb_ema9_sweep.py` — EMA9 sweep logic
- `analysis/scratch/orb_ema9_sweep_trades.csv` — per-trade EMA9 results
- `analysis/scratch/orb_exit_sweep_merged.csv` — all 28 strategies merged
- `analysis/scratch/zz_phase3i_ema_variants.py` — 32-variant sweep

---

## Focus Area 4: EXHAUSTION SIGNALS (Phases 3b-3d)

### What to audit

**4a. Were signals tested fairly?**
- Phase 3b tested A (bars since high), B (EMA gap drop), C (volume decay)
- All showed negative delta vs baseline
- Question: These were tested on ALL 3,664 graduating trades. But the problem we're solving (big give-back) only applies to runners with large declines. Testing on all trades dilutes the signal. Were these ever re-tested on just the >50pp or >20pp clusters?

**4b. Combined score approach**
- Phase 3c/3d combined S1/S2/S3/S4 into a score
- No combination beat baseline
- Question: Equal weighting assumed. Was weighted scoring tested? Was any signal combination tested specifically on the high-decline clusters?

**4c. Premature dismissal risk**
- S2 (RSI) was "kept separate" in phase3d because it "behaves identically to others"
- But RSI later became the key signal in phases 3f-3j
- Were S1 (trailing stop) and S3 (bars since high) dismissed too early? S1 at 15-20% trail showed -0.15pp to -0.17pp on all trades — what about on runners only?

### Evidence files
- `analysis/scratch/phase3b_summary.csv` — signal performance summary
- `analysis/scratch/phase3c_isolation.csv` — per-signal isolation results
- `analysis/scratch/phase3c_combos.csv` — combination sweep results
- `analysis/scratch/phase3d_summary.csv` — trailing stop + signal results
- `analysis/scratch/zz_phase3b_exhaustion.py`
- `analysis/scratch/zz_phase3c_score.py`
- `analysis/scratch/zz_phase3d_trailing.py`

---

## Focus Area 5: DECLINE WINDOW AND GUARD LOGIC (Phases 3e-3k)

### What to audit

**5a. Decline window framing**
- peak = highest bar_high (wick) between entry and d3 exit
- decline_pp = peak_high_pnl - d3_pnl
- Question: Using the wick high as peak is the theoretical maximum we could never actually capture (we can't sell at the wick). Should peak be highest close instead? Does this change the cluster membership?

**5b. Cluster cutoffs**
- 50pp, 20pp, 10pp — where do these boundaries come from? Are they arbitrary?
- The >50pp cluster has only 49 valid trades. Is this sufficient for reliable conclusions?

**5c. Phase 3i — EMA variant selection**
- 1m_e5_c1 was rank-1 in 31/49 trades with 41.59pp mean pp_saved
- But this was measured against the wick high peak — unreachable in practice
- Question: What's 1m_e5_c1's mean pp_saved if measured against highest CLOSE instead of highest HIGH?
- Also: 1m_e5_c1 was only tested on the >50pp cluster (49 trades). How does it rank on the full runner population?

**5d. Guard logic (Phase 3j)**
- Winner: C rsi<40 M=5. 14/49 improved, 0/49 hurt, +2.16pp mean.
- Question: +2.16pp mean across all 49 trades. What's the mean across just the 14 improved trades? Are the improvements concentrated in a few outliers or distributed?
- The guard was tested only on >50pp. Was it ever tested on all 3,664 graduating trades?

**5e. Phase 3k diagnosis**
- 16 trades: "window too short" — RSI fires but can't complete 5 bars before d3
- Question: If d3 fires soon after RSI<40, that means d3 is already doing its job on these trades. Is the guard actually needed here, or is d3 sufficient?
- 9 trades: "RSI never fires" (bottoms 41-50) — these are the most interesting. What's different about these trades? Higher volume? Different time of day? Different gap_pct?

**5f. 20-50pp cluster failure**
- Guard C rsi<40 M=5 hurt 49/237 trades, helped 53, net -0.60pp
- 9 run-up FP out of 237
- Question: Were the 9 run-up FP trades examined? What caused the guard to fire during run-up? Were different parameters tested on this cluster?

### Evidence files
- `analysis/scratch/phase3e_decline.csv` — decline window per trade
- `analysis/scratch/phase3f_signal_cal.csv` — signal calibration
- `analysis/scratch/phase3f_trades.csv` — per-trade signal firing detail
- `analysis/scratch/phase3i_variants.csv` — variant rankings
- `analysis/scratch/phase3i_trades.csv` — per-trade rank detail
- `analysis/scratch/phase3j_guard.csv` — guard combo summary
- `analysis/scratch/phase3j_trades.csv` — guard per-trade detail
- `analysis/scratch/phase3k_diagnosis.csv` — unchanged trade classification
- `analysis/scratch/phase3k_layer2.csv` — second layer candidates
- `analysis/scratch/phase3k_2050.csv` — 20-50pp cluster results
- `analysis/scratch/zz_phase3e_decline_window.py`
- `analysis/scratch/zz_phase3j_guard.py`
- `analysis/scratch/zz_phase3k_diagnose.py`

---

## Focus Area 6: ENTRY QUALITY SIGNALS

### What to audit

**6a. B+1 bar divergence**
- 68% green for Good vs 20% for Bad/Neutral at B+1
- Sample: 22 Good + 10 Bad/Neutral = 32 trades total
- Question: 32 trades is far below the 30-trade minimum for EACH group (we have only 10 Bad). Is this finding reliable or noise? Has this been validated on the other 204 entries?
- The v1 entry list HAD a B+1 confirmation requirement (green + above ORB). It was retired in v2. Why? What happened to entry quality when B+1 was dropped?

**6b. Pre-entry approach pattern**
- Good at B-5: -3.05% vs Bad: -6.70% below ORB
- Interpretation: Good stocks "coil near ORB" while Bad "snap up from far below"
- Question: Same 32-trade sample size concern. Also — is this just restating the B-1 coil filter? If B-1 >= -4% is already required, does B-5 add information?

**6c. Time-of-day signal**
- Good median 10:05 vs Bad 10:31
- Question: Medians with no distribution shown. What's the overlap? What % of Good entries are after 10:30? What % of Bad are before 10:00? Without this, no threshold is justified.

**6d. VR at extremes**
- v2: Bad median VR 4.0x > Good 3.4x
- v1: Good median VR 3.9x > Bad 3.1x
- These CONTRADICT each other across versions. Is VR a signal at all, or is this noise?

### Evidence files
- Session log: `agents/session-log/2026-03-24-entry-context.md`
- Session log: `agents/session-log/2026-03-24-orb-feedback-v2.md`
- Session log: `agents/session-log/2026-03-24-orb-feedback-analysis.md`
- Session log: `agents/session-log/2026-03-24-orb-threshold.md`

---

## Focus Area 7: METHODOLOGY AND FORWARD BIAS

### What to audit

**7a. Population leakage**
- Entry lists were generated, then PO rated entries as Good/Bad/Neutral
- Phase 1-2 exit research uses only 132 Good entries
- Phase 3 uses all 3,664 graduating trades (from signal_bars.parquet matching tickers in the entry list)
- Question: The entry list was constructed by scanning the multibagger universe (450 selected ON OUTCOME — they're 100%+ movers). Is this survivorship bias? We're testing an ORB entry on stocks we already know had a massive move that day.

**7b. Graduation threshold**
- A trade "graduates" at +5% (1-min close >= entry_price × 1.05)
- Phase 3 research only applies to graduates
- Question: What about the non-graduates? How many of the 236 entries never reach +5%? These are the trades where the hard stop matters most. Are we ignoring the failure population in exit research?

**7c. Decline pp measurement**
- Uses peak bar_high (wick) as the ideal target
- You can't sell at the wick in practice
- The entire phase 3 research optimises toward an unreachable target
- Question: How much does this inflate the "prize"? Should all results be recalculated using peak close instead of peak high?

**7d. ema9_5m_d3 as baseline**
- All phase 3 research measures improvement vs ema9_5m_d3
- But ema9_5m_d3 was itself selected from a sweep (Phase 2)
- Question: Is ema9_5m_d3 the right baseline? Phase 2 showed best variant was +42.72% vs d3's +38.21%. Should phase 3 compare against ema9_5m_d2 or the per-trade best from phase 2?

**7e. No out-of-sample testing**
- All findings are in-sample (tested and "validated" on the same population)
- The only partial exception: v1 and v2 entry lists are separate but from overlapping time periods
- Question: Should any finding be trusted without a held-out test set? What would proper out-of-sample look like here?

---

## Focus Area 8: MISSED OPPORTUNITIES AND NEW IDEAS

### What agents should consider

**8a. Strategies not yet explored:**
- Partial position management: enter with half size, add on confirmation (B+1 green?)
- Time-based exits: close position after N minutes if not at +X%
- Intraday trend following: ride EMA5(1m) with tight trail instead of waiting for d3
- Multi-timeframe confirmation: 1m and 5m must agree before exit
- Volume profile during hold: exit on volume spike + red bar (selling climax)
- Re-entry: if stopped out at -10%, is there a re-entry signal worth testing?

**8b. Unexplored data angles:**
- What do the 104 Bad entries have in common? Beyond the 4 robotic tickers.
- The "no reason" Bad category (24 v1 + 63 v2) — can we characterise these?
- What happens to entries on days with multiple ORB breakouts (same ticker)?
- Gap_pct distribution for Good vs Bad — never analysed
- Pre-market volume for Good vs Bad — never analysed beyond phase3a's inconclusive single-feature test

**8c. Strategy combinations:**
- Current thinking is sequential layers (hard stop → EMA9 → guard)
- Alternative: parallel strategies per trade archetype (fast runner, slow grinder, failure)
- Could we classify trade type in real-time (not at entry) and switch strategy?

**8d. The core edge question:**
- 56% Good rate at entry means 44% of entries are bad
- Best exit research saves ~2pp on 49 extreme trades
- Is the biggest opportunity in entry filtering (reduce Bad from 44% to 30%) rather than exit optimisation?
- What's the EV impact of removing 10% of Bad entries vs saving 2pp on exits?

---

## Session Structure

Run as 8 separate focus areas. For each:
1. Optimist presents assessment (confirmations, concerns, ideas)
2. Challenger audits Optimist's assessment + adds own flags
3. Manager synthesises into confirmations / doubts / recommendations / new ideas

No turn limits, no cost limits. Thoroughness over speed.
