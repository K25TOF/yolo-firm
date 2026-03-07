# Manager Memory

## YOLO firm state

- Current phase: Phase 5 — Triple Loop (Learning)
- Active strategy: vol_filter v2.1.0 (paper, not production ready — EXP-023 verdict)
- Last experiment: HYP-025 Phase 1 — INCONCLUSIVE (config error, LC-2025-002 audit)
- PRD version: v0.13.0

## Open items for PO review

- LC-2025-002: Revise HYP-025 status from "failure" to "inconclusive — config error" in `research-log.md`
- LC-2025-002: Approve HYP-025 Phase 2 corrected re-test (exit: `ema_gap crosses_below 0.5`)
- LC-2025-002: Log improvement idea — future batch experiments should capture cache-miss vs bar-count skip breakdown separately
- LC-2025-002: Analyst memory update — pending PO approval
- LC-2025-002: Engineer memory update — pending PO approval

## Session history (last 5)

- LC-2025-002 (audit): HYP-025 Phase 1 failure verdict overturned — exit rule inversion (`crosses_below 2.0` with `crosses_above 1.0` entry) disqualifies PnL/WR results. Skip rate structural (universe issue). Acceleration filter directionally promising (+5.8pp WR). Corrected re-test warranted.

## Agent observations

- Analyst strengths/patterns: Strong on logical chain — correctly identified exit flaw as disqualifying (not merely compounding). Will partially own design weaknesses. Flags protocol items clearly (memory update for PO approval, doc separation).
- Engineer strengths/patterns: Strong pre-run diagnostics before executing. Runs targeted confirmatory tests rather than full backtests. Surfaces anomalies clearly (avg hold 52–70 bars vs 7.5 — identified as structural signal). Preserves re-test configs in memory proactively.

## Key lessons

- Exit threshold must be BELOW entry threshold to mirror fade logic (vol_filter: entry 3.0%, exit 1.5%). HYP-025 had it inverted (entry 1.0%, exit 2.0%).
- Lower entry thresholds compound dramatically across large universes — stress-test entry frequency before finalising hypothesis.
- Identical skip rates across configs = structural/universe issue, not strategy artifact. Always run multi-config skip comparison before diagnosing.
