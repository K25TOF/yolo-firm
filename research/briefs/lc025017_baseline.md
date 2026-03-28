# YOLO Research Baseline — LC-2025-017

_Written: LC-2025-017 Part B | Status: DRAFT — PO approval required_
_Source: Part A experiment sweep (EXP-001–024, FA1–FA8 audit, LC-2025-014 Phase 3 exit research)_

---

## Purpose

This document is the single authoritative statement of what has been proven, what is
conditional, what has failed, and what remains unknown. All future research starts here.

---

## Category 1 — PROVEN (use in production design)

### 1.1 Skip-First Entry Filter
- **Finding:** Skipping the first entry signal per ticker per day improves WR by +33pp
  on the scanner universe (scanner-flagged, RVOL-gated tickers)
- **Evidence:** EXP-022 (fresh backtest, 28T, 35%→50% WR), EXP-021 (60T retroactive,
  21%→54%), Class A re-run on 5,755-pair momentum universe (33pp gap confirmed)
- **Scope:** Scanner universe (RVOL-gated). Effect is +5pp only on hand-picked known runners
  (effect is dramatically underestimated by hand-picked studies)
- **Mechanism:** First entry catches the initial volume spike which often immediately reverses;
  second signal confirms the ticker is a real runner
- **Production status:** Validated. Should be included in any live strategy.

### 1.2 News Presence as Mild Positive Signal
- **Finding:** Trades with Benzinga news coverage show 33.3% WR vs 24.3% WR without news
  (+9pp). No-news trades are 85.8% losers (75.7% loss rate vs 66.7% baseline).
- **Evidence:** EXP-024 — 522 trades, 252 tickers, news joined on ticker+date
- **Scope:** vol_filter strategy universe. May generalise; not validated on ORB universe.
- **Production status:** Mild supporting signal. Not sufficient as standalone filter.

### 1.3 Vol_Filter Has No Edge on Broad Momentum Universe
- **Finding:** vol_filter v2.1.0 (EMA gap >3.0%, volume_ratio_ema ≥ 2.0) has no
  statistically significant edge on the broad momentum universe (50% intraday range filter)
- **Evidence:** Six Class A re-runs (LC-2025-005/006) — all produced negative PnL on the
  5,755-pair momentum universe. Original positive results (EXP-010/011, EXP-014,
  EXP-016/023, EXP-022) confirmed as selection-bias artefacts.
- **Exception:** EXP-023 WR stability (32–34%) holds within its intended RVOL-gated scanner
  universe — the PnL collapse is a universe mismatch problem, not a signal quality problem.
- **Production status:** NOT PRODUCTION READY on broad universe.

---

## Category 2 — CONDITIONAL (promising but requires further validation)

### 2.1 ORB Entry Signal — 56% Good Rate (In-Sample)
- **Finding:** ORB breakout entry (first bar after ORB window with bar_close ≥ orb_high + vol_ratio
  ≥ 2.0x + B-1 coil ≤ -4%) produces ~56% Good entries on the multibagger universe
- **Evidence:** LC-2025-014 — 298 PO-rated entries (128 v1 + 170 v2); 236 tradeable after
  $10K/min liquidity gate; ~56% Good (PO visual rating)
- **Scope:** 450-stock multibagger universe (mcap ≥ $10M, float_turnover ≥ 0.50x,
  intraday range ≥ 100%). RTH only.
- **Caveats:** IN-SAMPLE ONLY. OOS validation required before production. Borderline
  statistical significance. 95% CI on 56% ≈ [49%, 63%]. PO rating introduces
  lookahead — true Good rate may be lower.
- **Production status:** CONDITIONAL. Cannot deploy without OOS validation (D3).

### 2.2 ATR Exit (2.0× ATR(14) Trailing Stop)
- **Finding:** ATR trailing stop combined with EMA exit marginally improves results
- **Evidence:** EXP-016 (+9.9pp PnL, +3pp WR on 82 hand-picked trades); LC-2025-009
  (+1.63pp WR on broad universe)
- **Scope:** Effect concentrated on moderate movers; no impact on big runners (ATR never
  fires on sustained moves). Effect is real but does not fix core edge problem.
- **Production status:** Include as supplementary exit rule. Do not rely on as primary edge.

### 2.3 Hard Stop (−10% from Entry)
- **Finding:** Hard stop fires rarely (avg loser is −3.4%, well below −10% threshold);
  threshold is defensible as tail protection
- **Evidence:** FA2 — fires only on catastrophic tail subset; does not distort typical exits
- **Caveats:** Threshold untested across alternatives (−5%, −7.5%); effective sample for
  sensitivity testing is ~25–35 trades (underpowered)
- **Production status:** Include as tail risk protection. Threshold selection requires
  larger sample before optimising.

### 2.4 Guard C (RSI<40 within 5 bars of entry)
- **Finding:** Guard C improves outcomes on >50pp catastrophic decline cluster only
  (+2.16pp, 0/49 hurt)
- **Evidence:** FA5 — proven on >50pp subset; HARMS 20–50pp subset (40/49 hurt)
- **Caveats:** Signal stack may have been designed on same 49-trade set (contamination risk).
  Does not generalise beyond catastrophic decline regime.
- **Production status:** Do NOT deploy as general exit rule. Consider only for
  catastrophic-decline detection if that regime can be identified at entry time.

### 2.5 ORB B-1 Coil Filter (≤ −4% below ORB high at B-1)
- **Finding:** Requiring B-1 to be near but below ORB high appears to improve entry quality
- **Evidence:** FA1 — ORB signal discriminates capture quality; borderline statistical
  significance
- **Production status:** CONDITIONAL on OOS validation.

---

## Category 3 — FAILED / RETIRED

| Finding | Evidence | Reason Retired |
|---|---|---|
| Vol_filter positive results (EXP-010/011/014/016/022) | LC-2025-005/006 Class A re-runs | Selection bias — hand-picked ticker artefact |
| IDEA-018 (gap >4% AND vol >5x as loser archetype) | LC-2025-010 — +1.12pp above baseline | Not a loser archetype on broad universe; source findings were hand-picked artefacts |
| Gap acceleration filter on vol_filter | LC-2025-008 — 98.6% trade reduction, −4.0pp WR | Structurally incompatible with 3.0% entry threshold |
| HYP-025 Grinder Phase 1 | LC-2025-007 — 32.5% WR, 4.9 bar hold | Exit too tight (exit 2.0% > entry 1.0% — inverted logic); pending corrected re-test |
| RSI exit on momentum trades | FA4 engine anomaly; literature confirms fragility | Engine anomaly + short-timeframe RSI exits documented as unreliable |

---

## Category 4 — OPEN QUESTIONS (not yet tested or blocked)

| Question | Blocker | Priority |
|---|---|---|
| Does Gap% from prior close predict ORB entry quality? | None — zero marginal data effort | High |
| Can we define a mechanical Bad label that reproduces PO ratings? | None | High (enables D3) |
| Does the 56% ORB Good rate hold OOS? | D2 mechanical label + n≥95 OOS entries | Critical (production gate) |
| Do EMA exit thresholds (d1/d2/d3) differ materially on ORB universe? | 5-min bar computation method confirmation | Medium |
| Does sub-$1 spread reality invalidate PnL figures? | No spread model in backtester | Cross-cutting |
| Does retest pattern at ORB high predict entry quality? | Pre-check retest count; n likely <30 | Low (exploratory) |
| VWAP asymmetric threshold for sub-$1 vs >$1 stocks | None | Low |
| HYP-025 corrected grinder re-test | PO approval | Parked |

---

## Category 5 — KNOWN ENGINE LIMITATIONS

| Limitation | Impact |
|---|---|
| No rolling-window-of-indicator comparison | Cannot implement ignition event conditions 3/4/5 |
| No bar-body geometry (close-open / high-low) | Cannot implement green candle body ratio filter |
| No prior-N-bar-high breakout | Cannot implement ORB breakout natively (use ib_high indicator instead) |
| Stop-from-entry is stateful | Percentage stop from entry requires custom walk (not rule-based engine) |
| 5-min bar computation method | EMA9 on 5-min bars may require pre-aggregation step — unconfirmed |
| All entries use bar_close[B0] | All PnL figures are upper-bound estimates; live trading degrades by 0.5–2.0% |
| Spread not modelled | Sub-$1 live PnL materially lower than backtest PnL; 2–5% typical spread |

---

## Summary Statement

The research programme has established one proven entry edge (skip-first on scanner
universe, not yet validated on ORB universe), one conditional entry signal (ORB at 56%
Good in-sample, unvalidated OOS), and confirmed that
vol_filter has no edge on the broad momentum universe. The primary gap is a scalable,
mechanical method for labelling entry quality (Bad label) and an OOS validation of the
ORB signal. Exit research has been extensive but has not produced a validated production-
ready exit rule beyond the marginal ATR contribution.

The highest-leverage next research area is entry quality filtering — specifically Gap%
stratification and mechanical Bad label definition. These are low-effort, high-information
steps that will unblock the OOS validation path.
