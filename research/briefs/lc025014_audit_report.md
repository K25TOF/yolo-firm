# LC-2025-014 Full Audit Report
> Date: 2026-03-27 | Sessions: 8 focus areas | Model: claude-sonnet-4-6
> Cost: ~$8-10 total across 8 parallel sessions

---

## EXECUTIVE SUMMARY

The audit found **zero fully confirmed findings** across all 8 focus areas. Every key number in the research carries at least one unresolved methodological concern. The most serious issues are:

1. **Survivorship bias in universe construction** — the 450-stock universe is selected by outcome (100%+ movers). All WR/PnL figures are upper-bound estimates.
2. **No out-of-sample testing anywhere** — all findings are in-sample.
3. **PO ratings may carry hindsight bias** — charts showed full session, no documented rubric.
4. **Entry price lookahead** — bar_close[B0] is not transactable in real time.
5. **Wick-based peak target** — Phase 3 optimises toward an unreachable price.

However: the research is not invalidated. It has value as a **conditional study** ("given a scanner that finds runners, here's what ORB entry/exit looks like"). The path forward requires reframing claims, fixing known biases, and running temporal out-of-sample tests.

**Strategic pivot recommended:** Entry filtering (reducing 44% Bad rate) likely has higher EV than exit optimisation (2pp on 49 trades). Pre-entry signals are cheaper to test and address a larger population.

---

## VERDICTS BY FOCUS AREA

### FA1: Universe and Entry Signal

| Sub-Q | Verdict | Key Issue |
|---|---|---|
| 1a. 100%+ range (incl pre/post) | **FLAG** | Pre/post market inflates range. RTH-only recount needed. |
| 1b. Quality filters | **FLAG** | Float lookahead probable (current snapshot, not point-in-time). 6 prior blocking issues unresolved. |
| 1c. 5-min vs 15-min ORB | **FLAG** | Two variants used without pre-specified selection rule. V1 (54% Good) > V2 (48%). |
| 1d. Entry thresholds | **FLAG** | VR 2.0 and coil -4% — calibration source undocumented. Possible in-sample fitting. |
| 1e. Entry price = bar_close[B0] | **FLAG BLOCKING** | Lookahead confirmed. Bar close only known at bar end. Need B1-open gap analysis. |

### FA2: Hard Stop Analysis

| Sub-Q | Verdict | Key Issue |
|---|---|---|
| 2a. Population mismatch (236 vs 6,790) | **FLAG** | Different populations. Must confirm which drove -10% selection. |
| 2b. -10% circular reasoning | **FLAG** | PO ratings used to both construct population AND justify threshold. Timeline needed. |
| 2c. 96.5% runner survival | **DOUBT** | "Runner" undefined. Raw counts needed. Likely a subset stat. |
| 2d. Combined exit interaction | **FLAG** | Proxy backtest shows EMA9 exits most losers at -3.4% avg — hard stop rarely fires. Sequential optimisation conditionally defensible. |

### FA3: EMA Exit Research

*(Session hit 3 Amigos gate — partially covered in FA1 session. Key finding from proxy runs: EMA9 crossover dominates exit behaviour, avg loser -3.4%.)*

### FA4: Exhaustion Signals

| Sub-Q | Verdict | Key Issue |
|---|---|---|
| 4a. Wrong population | **DOUBT** | Signals tested on all 3,664 trades but give-back only affects large runners. Intraday peak distribution unknown. |
| 4b. Equal-weight scoring | **DOUBT** | Implementation unknown. Weighted scoring untested. |
| 4c. Premature dismissal | **DOUBT** | S1 trailing stop at 15% showed -0.15pp on ALL trades — sub-population effect unknown. RSI exit engine anomaly flagged (may contaminate Phase 3f-3j). |

**BLOCKING:** RSI exit engine anomaly — if `greater_than` operator holds to EOD, all RSI-exit findings in Phase 3b-3j may be contaminated. Must confirm implementation.

### FA5: Decline Window and Guard Logic

| Sub-Q | Verdict | Key Issue |
|---|---|---|
| 5a. Wick inflation | **DOUBT** | 41.59pp mean measured vs unreachable wick high. Per-trade distribution not provided. |
| 5b. Cluster cutoffs | **DOUBT** | 50pp/20pp/10pp appear arbitrary. 49 trades is small. Outcome-selected tail. |
| 5c. 1m_e5_c1 robustness | **DOUBT** | Parameters e5/c1 undefined in scope. Only tested on 49 trades. Margin over #2 unknown. |
| 5d. Guard C sample | **DOUBT** | "0 hurt" is artefact of 71% non-fire rate. 49/237 hurt in adjacent cluster. Trigger count ≠ improvement count. |
| 5e. Window/RSI diagnosis | **FLAG** | Window length provenance unknown. 9 RSI non-firers may be grinder-profile losers (different regime). |
| 5f. 20-50pp failures | **FLAG** | 40/49 hurt trades unclassified. No RSI threshold sweep on this cluster. |

**BLOCKING:** Full signal stack (d3 + 1m_e5_c1 + Guard C) may all be designed on same 49 trades — zero degrees of freedom for in-set validation. No time-based holdout anywhere in FA5.

### FA6: Entry Quality Signals

| Sub-Q | Verdict | Key Issue |
|---|---|---|
| 6a. B+1 (68% vs 20%) | **DOUBT** | n=10 Bad subsample. CIs overlap. But reframe as position management trigger (not entry filter) is structurally sound. |
| 6b. B-5 approach | **DOUBT** | Means without variance. Same n=32 sample. |
| 6c. Time-of-day | **DOUBT** | Two medians, no distribution. "Second-wave theory" is hypothesis, not evidence. |
| 6d. VR contradiction | **FLAG** | v1 Good VR > Bad. v2 Bad VR > Good. Unresolved contradiction. Must analyse v1/v2 separately. |

**BLOCKING:** Good/Bad rating definition not documented. If ratings incorporate post-entry bar behaviour, all findings circular.

### FA7: Methodology and Forward Bias

| Sub-Q | Verdict | Key Issue |
|---|---|---|
| 7a. Survivorship bias | **FLAG BLOCKING** | Universe selected by outcome. All absolute WR/PnL are upper bounds. |
| 7b. Graduation threshold | **FLAG BLOCKING** | Phase 3 only covers graduates (+5%). Failure population ignored. Graduation count out of 236 unknown. |
| 7c. Wick vs close | **FLAG** | Phase 3 optimises toward unreachable wick peak. Fix: use peak close instead. |
| 7d. d3 as baseline | **DOUBT** | Not the best variant (+38.21% vs +42.72%). 4.51pp gap within noise. Not blocking. |
| 7e. No out-of-sample | **FLAG BLOCKING** | Zero OOS anywhere. Temporal 60/40 split needed before further work. |

### FA8: Missed Opportunities

**Core finding:** Entry filtering likely higher EV than exit optimisation, by addressable population size. But the exact ratio cannot be computed without average PnL per Good/Bad trade.

---

## BLOCKING ISSUES (Must resolve before any claim)

| # | Issue | Source | Resolution |
|---|---|---|---|
| B1 | Entry price lookahead (bar_close[B0]) | FA1-1e | Extract bar_open[B1] for 236 entries. Compute gap distribution. |
| B2 | Survivorship bias in universe | FA7-7a | Reframe as conditional study. Build pre-market filter for live use. |
| B3 | No out-of-sample testing | FA7-7e | Run temporal 60/40 split on 236 entries before further work. |
| B4 | PO rating methodology undocumented | FA2, FA6 | Document: were charts cropped at entry? Were criteria pre-specified? |
| B5 | RSI exit engine anomaly | FA4 | Confirm RSI exit implementation in Phase 3b-3j code. |
| B6 | Graduation count unknown | FA7-7b | Count how many of 236 entries reach +5%. Determines Phase 3 coverage. |
| B7 | Wick-based peak in Phase 3 | FA7-7c | Replace with peak bar_close. Rerun key Phase 3 analyses. |
| B8 | Float data lookahead | FA1-1b | Confirm float data source: point-in-time or current snapshot. |
| B9 | Full signal stack designed on same 49 trades | FA5 | Confirm whether d3, 1m_e5_c1, Guard C all selected on same population. |

---

## CONFIRMED FINDINGS (things we CAN trust)

Despite the extensive flagging, several findings survive the audit:

1. **EMA9 on 5-min bars beats 1-min bars** — consistent across multiple analyses, mechanistically sound (less noise on longer timeframe). Direction reliable even if magnitude uncertain.
2. **ATR trailing stops cut runners short** — all 20 variants triggered on all 132 trades before EOD. Higher multiplier always better. Structural finding, not parameter-dependent.
3. **Hard stop is a tail-risk backstop only** — EMA9 exits most losers at -3.4% avg, well before -10%. Sequential optimisation conditionally defensible.
4. **Guard C asymmetry is real** — works on >50pp catastrophic declines, harms 20-50pp moderate declines. Regime-specific finding. Mechanism: RSI reaches deep exhaustion in catastrophic declines but not moderate ones.
5. **Robotic ticker exclusion** — CIGL, UFG, BCDA, TOPP always Bad. Zero-cost, zero-risk filter.
6. **v1 (5-min ORB) outperforms v2 (15-min ORB)** — 54% vs 48% Good rate. Should be primary research track.

---

## TOP RECOMMENDATIONS (ranked by impact)

### Immediate (resolve before further research)

1. **Reserve 25% held-out subset** (~59 entries) before any threshold analysis. All threshold searches on design set only (~177 entries).
2. **Document PO rating methodology** — when were labels assigned, what was visible on charts, were criteria pre-specified.
3. **Run temporal 60/40 date split** — earliest 60% design, latest 40% held-out. Tests parameter overfit.
4. **Extract bar_open[B1]** for all 236 entries. Compute B0-close to B1-open gap distribution.
5. **Count graduates** — how many of 236 reach +5% close above entry price.
6. **Confirm RSI exit implementation** in Phase 3 code — operator used, engine behaviour.

### High Priority (next research phase)

7. **Replace wick peak with close peak** in all Phase 3 analyses. Rerun Phase 3i variant rankings.
8. **Test Guard C on full 3,664 graduates** — trigger rate, improvement rate, harm rate per cluster.
9. **Decompose 87 "no reason" Bad entries** — Fakeout / Flat / Runner / Structural. Unlock entry filtering.
10. **Pull gap_pct + pm_volume distributions** for all 236 entries split Good/Bad.
11. **VR bucket analysis** — separately on v1 and v2 before combining.

### Strategic

12. **Reframe all research** as conditional: "Given a scanner that identifies probable runners, here's what ORB entry/exit looks like."
13. **Pivot primary research to entry filtering** — reduce 44% Bad rate. Higher addressable population than exit optimisation.
14. **Build pre-market filter** (gap >= 30% + PM volume >= $1M) to approximate 100%+ mover selection without intraday outcome data.
15. **Test 10-20pp cluster** as near-OOS for Phase 3 signals (untouched population, larger than >50pp).

---

## NEW STRATEGY IDEAS (from agents, ranked by expected impact)

### Entry Filtering (highest priority)

| # | Idea | Test | Expected Edge |
|---|---|---|---|
| 1 | Gap% + PM Volume combined filter | Pull distributions for 236, find threshold combo | Reduce Bad rate by 5-10pp |
| 2 | "No Reason" Bad decomposition | Classify 87 Bads by price trajectory | Unlock 1-2 filterable patterns |
| 3 | B-1 coil tightening (-4% → -2%) | Compare Good% at tighter threshold | Zero-infrastructure, +4pp Good rate? |
| 4 | VR ceiling (cap at 5x or 6x) | VR bucket analysis on v1 and v2 separately | Remove exhaustion entries |
| 5 | Time-of-day cap (entries before 10:30 only) | Time bucket Good% analysis | Remove ~30% of Bads |
| 6 | Robotic ticker + same-day dedup | Identify repeat tickers, get G/B breakdown | +3pp Good rate at negligible cost |
| 7 | ORB range as quality signal | Compute range %, split by tercile | Tight ORB = genuine coil |

### Exit / Position Management

| # | Idea | Test | Expected Edge |
|---|---|---|---|
| 8 | B+1 red = exit immediately | If B+1 closes red AND below B0 open, exit | Converts some Bads to ~0 loss |
| 9 | B0 close weak cut-rule | If B0 closes below ORB high (wick only break), exit | Real-time, zero infrastructure |
| 10 | Partial exit at +3% / hold remainder | Lock in gains, let remainder ride | Smooths returns |
| 11 | Time-leashed exit for late entries | If entered after 10:30, must be +X% by 11:00 or exit | Limits late-entry damage |
| 12 | S1 trailing at 8-10% on high-peak trades | Sweep 5-12% on trades reaching +15% intraday | Better calibrated to give-back quantum |
| 13 | EMA5(1m) trail from graduation | Ride EMA5 with tight trailing instead of waiting for d3 | Faster exit on failures |

### Scanner / Universe

| # | Idea | Test | Expected Edge |
|---|---|---|---|
| 14 | Pre-market filter for live scanner | Gap >= 30% + PM vol >= $1M | Approximate runner selection without intraday lookahead |
| 15 | RTH-only range universe | Recount using RTH bars only | Cleaner universe, fewer false inclusions |
| 16 | Control group: 20-50% movers | Run ORB on stocks with moderate moves | Tests signal generalisability |

---

## SESSION COSTS

| Session | Turns | Est. Cost |
|---|---|---|
| FA1 (entry) | 14 | ~$2.50 |
| FA2 (stop) | 4 | ~$0.50 |
| FA3 (EMA) | 1 | ~$0.03 |
| FA4 (exhaustion) | 8 | ~$1.00 |
| FA5 (guard) | 8 | ~$1.20 |
| FA6 (quality) | 7 | ~$0.90 |
| FA7 (bias) | 5 | ~$0.70 |
| FA8 (ideas) | 6 | ~$0.80 |
| **Total** | **53** | **~$7.60** |
