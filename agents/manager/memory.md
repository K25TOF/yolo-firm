# Manager Memory

## YOLO firm state

- Current phase: Phase 8 released (yolo PRD v0.19.0). Agent framework upgrade in progress.
- Active strategy: vol_filter v2.1.0 (paper, not production ready — EXP-023 verdict)
- Last experiment: LC-2025-015 — Full Audit of ORB Breakout Research (FA1–FA8, 2026-03-27)
- PRD version: v0.19.0 (yolo app); v0.4.1 (yolo-firm)

## Open items for PO review

Items below LC-2025-007 were bulk-approved by PO (2026-03-07 audit handoff). Agent memories already updated.

- LC-2025-005: Engine win_rate display bug — engine returning values like 3200.2% instead of 32.0%. Workshop fix still needed.
- LC-2025-005: Scope request — add RVOL threshold as universe filter parameter to backtester (alongside momentum_universe). Required to re-validate EXP-023 on correct universe.
- LC-2025-006: Add IDEA-019 to ideas.md — ATR isolation test on broad momentum universe
- LC-2025-006: Update strategy-roadmap.md Research State section — ranked leads for next phase
- ~~Engine story: Expose trade distribution metrics~~ — DONE (Story 5.12).
- ~~Engine story: Fix dates="all" resolution~~ — DONE (Story 5.13).
- **LC-2025-012 (pending PO approval):** Update session history in memory. Record ignition event definition. Note engine capability gaps (rolling-window-of-indicator, bar-body geometry, prior-N-bar-high breakout — four of five ignition conditions unimplementable via BacktestEngine).

## Session history (last 5 research + FA audit)

- LC-2025-014 (ORB breakout research): 450-stock multibagger universe (mcap ≥ $10M, float_turnover ≥ 0.50x). ORB entry: first bar after 09:45 with bar_high ≥ ORB high + vol_ratio ≥ 2.0x + B-1 coil within -4%. 298 PO-rated entries (128 v1 + 170 v2). After $10K/min liquidity gate: 236 tradeable entries (~56% Good). Clean tradeable universe defined. **Phase 3 exit research complete** — see findings below.
- LC-2025-012 (ignition event research): Script complete, pending VPS execution. Five ignition conditions defined and Analyst-approved. BacktestEngine approximation ruled out (too lossy). PO to run `python analysis/scratch/zz_ignition_phase1_2.py` from project root and return output for Analyst audit.
- LC-2025-011 (RVOL threshold): volume_ratio_ema threshold 2.0→5.0 on broad universe. +3.51pp WR at 5.0x but all thresholds net negative. Stable +0.035pp WR per 1% trade reduction. RVOL is a working knob but cannot fix core edge. First attempt blocked by dates="all" issue (now fixed in Story 5.13).
- LC-2025-010 (IDEA-018 test): AND-subset (gap >4% AND vol >5x) = 316 trades, 29.10% WR, +1.12pp above baseline — not a loser archetype. IDEA-018 FAIL — retired. Source findings (EXP-012, EXP-021) confirmed as hand-picked artefacts.
- LC-2025-009 (ATR isolation): ATR exit on broad universe — +1.63pp WR, +1,186.9pp PnL vs EMA-only. PASS (marginal). Directionally consistent with EXP-016 but smaller magnitude. Does not fix core edge problem.
- LC-2025-008 (gap accel filter): ema_gap_acceleration < 1.0 on vol_filter — 98.6% trade reduction (6,347→88), WR -4.0pp. Filter structurally incompatible with 3.0% entry. FAIL. Belongs in grinder context only (IDEA-021).

### LC-2025-015 — Full Audit (FA1–FA8, 2026-03-27)

8-session audit of LC-2025-014 ORB breakout research. All sessions used Optimist + Challenger.

| FA | Focus | Verdict | Key Finding | Log |
|---|---|---|---|---|
| FA1 | Universe & Entry Signal | ACTIVE | ORB signal discriminates capture quality; borderline statistical significance; OOS validation required | `2026-03-27-audit-fa1-entry-v2.md` |
| FA2 | Hard Stop | FLAG | Hard stop fires on tail-only subset (avg loser -3.4% vs -10% threshold); sequential optimisation defensible if exit breakdown confirms <10% losses via stop; PO rating lookahead unresolved | `2026-03-27-audit-fa2-stop.md` |
| FA3 | EMA Exit | INCOMPLETE | Session initiated but not completed — stub file only | `2026-03-27-audit-fa3-ema.md` |
| FA4 | Exhaustion Signals | FLAG | RSI exit engine anomaly (greater_than holds to EOD); trade count collapse 82→33 unexplained; S1 threshold likely above natural give-back range | `2026-03-27-audit-fa4-exhaustion.md` |
| FA5 | Guard Logic | DOUBT | Guard C works only in >50pp catastrophic regime, harms 20–50pp; signal stack potentially designed on same 49-trade set (contamination) | `2026-03-27-audit-fa5-guard.md` |
| FA6 | Entry Quality | FLAG | VR shows opposing signals in V1 vs V2; all four signals require v1/v2 stratification; none production-ready | `2026-03-27-audit-fa6-quality.md` |
| FA7 | Methodology & Bias | FLAG BLOCKING | All absolute WR/PnL are upper-bound estimates; graduation count pivotal; temporal OOS split required before further work | `2026-03-27-audit-fa7-bias.md` |
| FA8 | Ideas & Opportunities | ACTIVE | Entry filtering (Gap%+PM Volume) is primary EV lever; Bad label definition is foundational blocker; 56% Good baseline ±3.2pp CI | `2026-03-27-audit-fa8-ideas.md` |

## LC-2025-014 Phase 3 Exit Research — Key Findings (COMPLETE)

- **Baseline:** ema9_5m_d3 exit produces +38.21% total PnL on graduating trades
- **Guard C (rsi<40 within M=5 bars):** Proven on >50pp decline cluster — +2.16pp improvement, 0/49 hurt
- **Guard C does NOT generalise:** On 20–50pp cluster, guard harms performance (40/49 hurt trades unclassified)
- **Phase 3 status:** Entry development complete in scope. Exit design not started. All figures in-sample only.

## Ignition event definition (LC-2025-012)

All five conditions must be true on the ignition bar:
1. `volume_ratio_ema >= 5.0`
2. `close > open` (green candle)
3. `(close - open) / (high - low) >= 0.70` (body ratio; zero-range bars excluded)
4. Prior 10 intra-session bars: price range < 3% of close AND `volume_ratio_ema` max < 1.5
5. `close > max(high)` of prior 10 intra-session bars

Phase 2 safe entry: price hits +7% above ignition close (5% target + 2% slippage) before returning to ignition close. Simultaneous hit (same bar: high ≥ target AND low ≤ return) = not safe (conservative).

Script: `analysis/scratch/zz_ignition_phase1_2.py` — assembled and ready. Run from `/home/claude/projects/yolo/`.

## Engine capability gaps (confirmed LC-2025-012)

BacktestEngine cannot implement:
- Rolling-window-of-indicator comparison (e.g., max VR over prior N bars)
- Bar-body geometry indicator (close-open / high-low ratio)
- Prior-N-bar-high breakout condition
- Green candle (close > open within bar; price_change_pct measures close-to-close, not open-to-close)

Only 1 of 5 ignition conditions is directly expressible via engine entry rules. Prototype script is the only valid path for this hypothesis class.

## Agent observations

- Analyst strengths/patterns: Strong on logical chain. EXP-023 universe mismatch identification (RVOL-gated vs 50% range) was sharp and materially changed the session conclusion. Correctly separates WR stability from PnL collapse as different signals. Will partially own design weaknesses. Flags protocol items clearly. LC-2025-006: Excellent synthesis depth — surfaced time-of-day contradiction (EXP-012 vs EXP-021 measure different things), ATR subset dependency (moderate movers only), and first-entry/re-entry effect magnitude difference between hand-picked and scanner datasets. LC-2025-007: Immediately caught Config B formulation error (OR vs AND), directed pivot to AND-subset analysis efficiently. LC-2025-012: Clean methodology audit — identified the intra-bar ordering ambiguity and ruled conservative before execution. Correct call at baseline measurement stage.
- Engineer strengths/patterns: Strong pre-run diagnostics. Surfaced universe mismatch in EXP-014 diagnostic run before reporting. Delivered clean ATR isolation comparison in batch 2 (same universe, both configs). Correctly assessed RVOL-gating as out of scope rather than attempting a workaround. Flags engine anomalies (win_rate display bug) without being asked. LC-2025-007: Proactively flagged CSV-read limitation before attempting, proposed AND-subset backtest as clean workaround, raised hand for approval before running. LC-2025-012: Correctly assessed BacktestEngine approximation as too lossy (only 1/5 conditions implementable) and recommended PO manual execution rather than running a degraded test.

## Key lessons

- Exit threshold must be BELOW entry threshold to mirror fade logic (vol_filter: entry 3.0%, exit 1.5%). HYP-025 had it inverted (entry 1.0%, exit 2.0%).
- Lower entry thresholds compound dramatically across large universes — stress-test entry frequency before finalising hypothesis.
- Identical skip rates across configs = structural/universe issue, not strategy artifact. Always run multi-config skip comparison before diagnosing.
- Momentum universe filter passes ~5.6% of all ticker-date pairs (5,755 / 103,554). Baseline for future experiment sizing.
- `greater_than` / `less_than` operators confirmed functional (LC-2025-007 — 13,656 trade delta with/without VWAP filter). LC-2025-003 finding was incorrect. Both forms (`greater_than` / `>`, `less_than` / `<`) work.
- **vol_filter has no edge on the broad momentum universe (50% range filter).** All 6 Class A re-runs confirm this. Positive original results were selection-biased.
- **EXP-023 is the partial exception:** WR stable at 32–34% across universe sizes. PnL collapse is a universe definition problem (RVOL-gated scanner vs 50% range filter), not a signal quality problem. Original +67.4% result not invalidated within its intended universe.
- **ATR exit marginally helps** — confirmed on both hand-picked (+9.9pp PnL, EXP-016) and broad universe (+1.63pp WR, +1,186.9pp PnL, LC-2025-009). Effect real but does not fix core edge problem. Both configs remain deeply negative on broad universe.
- **Selection bias pattern:** All pre-LC-2025-005 positive results used hand-picked tickers or favourable date subsets. Universe expansion consistently exposes the strategy's dependence on outlier runners (Principle #6 violation confirmed).
- **Re-entry effect is dataset-dependent:** 33pp WR gap (21%→54%) on scanner universe; only 5pp gap on hand-picked set. Hand-picked tickers pre-selected as real runners — first entries on known runners less likely to be spike fakes. Skip-first effect is dramatically underestimated by hand-picked studies.
- **Time-of-day distinction:** EXP-012 (early absolute time = good) and EXP-021 (early relative-to-flag = bad) measure different things. Early entries by wall clock are modestly positive; entries within 20 bars of scanner flag are bad (22% WR, -31.3%). Scanner flag itself often coincides with the spike it detected.
- **VR >5x is a loser marker, not a quality filter — on hand-picked sets only.** On the broad universe, AND-subset (gap >4% AND vol >5x) shows +1.12pp WR above baseline. Both indicators are ambiguous: they can mark exhaustion OR strong momentum depending on stage-of-move context. The broad universe contains both cases in roughly equal proportion.
- **Combined overextended profile (gap >4% AND vol >5x) is rare** — only 5% of vol_filter entries on the broad universe (316 of ~6,275 trades). Not a dominant signal regime.
- **Engine has no native AND-gate rejection logic.** Workaround: invert the rejection condition as additional entry rules (AND-gate inclusion). To test a blocking hypothesis, run a backtest where the block condition IS the entry requirement — this isolates the subset directly.
- **Hand-picked artefact pattern is now confirmed across 4+ cases:** EXP-010/011, EXP-012/021, EXP-014, IDEA-018. Positive hand-picked findings should be treated as hypotheses only until broad universe validation.
- **Prototype script path is required for hypotheses using rolling-window-of-indicator comparisons, bar-body geometry, or prior-N-bar-high breakouts.** BacktestEngine cannot express these. Do not attempt approximation — it measures the wrong thing. Route to PO for VPS execution.
- Class A re-run priority order (historical reference): EXP-023 (17-day batch), EXP-022 (skip-first), EXP-016 (ATR exit), EXP-014 (EMA-10 volume ratio) — all now completed.
- Missing engine dependencies (not blocking Class A, historical reference): hold-duration exit (cut_bar_5), adaptive bar-5 exit, `max_bar_chg_5b`, `price_chg_10b` indicators.

## Ranked leads for next research phase (updated after Leads #1-5 audit)

All 5 tested leads from LC-2025-006 are now closed:

| Lead | Session | Verdict | Key finding |
|---|---|---|---|
| #1 HYP-025 corrected re-test | LC-2025-007 | FAILED | 32.5% WR, 4.9 bar hold — exit too tight |
| #2 Gap accel on vol_filter | LC-2025-008 | FAILED | 98.6% trade reduction, -4.0pp WR — incompatible with 3.0% entry |
| #3 ATR isolation | LC-2025-009 | PASS (marginal) | +1.63pp WR, does not fix core edge problem |
| #4 IDEA-018 overextended filter | LC-2025-010 | FAILED | AND-subset +1.12pp above baseline — not a loser archetype |
| #5 RVOL threshold | LC-2025-011 | PASS (marginal) | +3.51pp WR at 5.0x but all thresholds net negative |

**Remaining untested:** VWAP asymmetric threshold (IDEA-017) — sub-$1 vs >$1 separate thresholds. Low effect size, low effort.

**New direction (LC-2025-012):** Ignition event research — fundamentally different hypothesis class from vol_filter variants. Tests whether extreme-volume breakouts from calm/flat bases have a structurally different (higher) safe entry rate. Results pending VPS execution.

**Strategic assessment:** Vol_filter has no edge on the broad momentum universe. All marginal improvements (ATR, RVOL) reduce losses but cannot flip the strategy to profitable. Ignition event research is the first test of a genuinely new signal type since the re-validation cycle began.
