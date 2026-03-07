# Manager Memory

## YOLO firm state

- Current phase: Phase 5 — Triple Loop (Learning)
- Active strategy: vol_filter v2.1.0 (paper, not production ready — EXP-023 verdict)
- Last experiment: LC-2025-007 — IDEA-018 Combined Overextended Entry Filter (FAIL)
- PRD version: v0.13.0

## Open items for PO review

Items below LC-2025-007 were bulk-approved by PO (2026-03-07 audit handoff). Agent memories already updated.

- LC-2025-005: Engine win_rate display bug — engine returning values like 3200.2% instead of 32.0%. Workshop fix still needed.
- LC-2025-005: Scope request — add RVOL threshold as universe filter parameter to backtester (alongside momentum_universe). Required to re-validate EXP-023 on correct universe.
- LC-2025-006: Add IDEA-019 to ideas.md — ATR isolation test on broad momentum universe
- LC-2025-006: Update strategy-roadmap.md Research State section — ranked leads for next phase
- ~~Engine story: Expose trade distribution metrics~~ — DONE (Story 5.12). run_backtest now returns avg_winner_pct, avg_loser_pct, median_pnl_pct, max_single_trade_pnl_pct, top10_pnl_contribution_pct.
- ~~Engine story: Fix dates="all" resolution~~ — DONE (Story 5.13). dates="all", ["all"], [], or omit all work.

## Session history (last 5)

- LC-2025-011 (RVOL threshold): volume_ratio_ema threshold 2.0→5.0 on broad universe. +3.51pp WR at 5.0x but all thresholds net negative. Stable +0.035pp WR per 1% trade reduction. RVOL is a working knob but cannot fix core edge. First attempt blocked by dates="all" issue (now fixed in Story 5.13).
- LC-2025-010 (IDEA-018 test): AND-subset (gap >4% AND vol >5x) = 316 trades, 29.10% WR, +1.12pp above baseline — not a loser archetype. IDEA-018 FAIL — retired. Source findings (EXP-012, EXP-021) confirmed as hand-picked artefacts.
- LC-2025-009 (ATR isolation): ATR exit on broad universe — +1.63pp WR, +1,186.9pp PnL vs EMA-only. PASS (marginal). Directionally consistent with EXP-016 but smaller magnitude. Does not fix core edge problem.
- LC-2025-008 (gap accel filter): ema_gap_acceleration < 1.0 on vol_filter — 98.6% trade reduction (6,347→88), WR -4.0pp. Filter structurally incompatible with 3.0% entry. FAIL. Belongs in grinder context only (IDEA-021).
- LC-2025-007 (HYP-025 re-test): Grinder strategy corrected exit (0.5%) on broad universe — 12,024 trades, 32.5% WR, 4.9 bar hold. Exit too tight (0.5pp decay room). FAIL on WR and hold profile targets.

## Agent observations

- Analyst strengths/patterns: Strong on logical chain. EXP-023 universe mismatch identification (RVOL-gated vs 50% range) was sharp and materially changed the session conclusion. Correctly separates WR stability from PnL collapse as different signals. Will partially own design weaknesses. Flags protocol items clearly. LC-2025-006: Excellent synthesis depth — surfaced time-of-day contradiction (EXP-012 vs EXP-021 measure different things), ATR subset dependency (moderate movers only), and first-entry/re-entry effect magnitude difference between hand-picked and scanner datasets. LC-2025-007: Immediately caught Config B formulation error (OR vs AND), directed pivot to AND-subset analysis efficiently.
- Engineer strengths/patterns: Strong pre-run diagnostics. Surfaced universe mismatch in EXP-014 diagnostic run before reporting. Delivered clean ATR isolation comparison in batch 2 (same universe, both configs). Correctly assessed RVOL-gating as out of scope rather than attempting a workaround. Flags engine anomalies (win_rate display bug) without being asked. LC-2025-007: Proactively flagged CSV-read limitation before attempting, proposed AND-subset backtest as clean workaround, raised hand for approval before running.

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

**Strategic assessment:** Vol_filter has no edge on the broad momentum universe. All marginal improvements (ATR, RVOL) reduce losses but cannot flip the strategy to profitable. Next research direction requires PO guidance — either (a) pursue grinder strategy with redesigned exit, (b) explore entirely new signal types, or (c) focus on scanner/universe improvements.
