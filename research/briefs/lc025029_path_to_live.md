# Path to Live Trading — Research Agenda

_Session: LC-2025-029 | Date: 2026-03-30 | All 6 agents contributed | Cost: ~$1.50_
_Status: DRAFT — PO approval required_

---

## Current State

| Layer | Status | Key Number |
|---|---|---|
| **L1 Scanner** | OOS VALIDATED (conditional) | 11.5% precision, 18.3x lift, ~3 fires/day |
| **L2 ORB Entry** | IN-SAMPLE ONLY | 56% Good on curated (in-sample), not tested on scanner fires |
| **L3 Exit** | IN-SAMPLE ONLY | ema9_5m_d3 baseline + hard stop -10% |

---

## Two Parallel Tracks

**Track 1 — Research validation** (the real work): Test L2 entry on the 183 OOS scanner fires. This is the only genuine new research needed. If L2 discriminates on scanner-filtered candidates, the full stack works.

**Track 2 — Audit/infrastructure** (verification + engineering): Code audits, pipeline builds, Workshop stories. Largely parallel with Track 1. Does not block research but blocks deployment.

---

## Stage 0: Audit & Verification (Parallel, immediate)

| Task | Type | Owner | Blocks | Priority |
|---|---|---|---|---|
| **A1: RVOL baseline audit** | Code audit | Workshop | L2 validation pipeline | **FIRST** |
| A2: signal_bars schema audit | Code audit | Workshop/Manager | L2 signal replication | High |
| **A3: Coil/VR threshold derivation** | Doc review | Manager | **Prerequisite for B3** | High |
| A4: Raw Good/Bad counts reconciliation | Data query | Manager | Gate 2 design | High |
| A5: B0→B1 gap distribution | Data query | Manager | Gate 2 backtest baseline | High |
| A6: L1 news pre-specification | Doc review | Manager/PO | Lifts L1 CONDITIONAL | High |
| A7: 183 OOS fire date distribution | Data query | Manager | Gate 1 design | Medium |

**A1 is highest risk:** If RVOL baseline is static (not rolling), the 56% Good rate baseline may be invalidated. Challenger flagged this as potentially requiring L2 validation restart.

**A3 is critical path:** B3 cannot run until coil/VR derivation sequence is confirmed as pre-outcome.

---

## Stage 1: Gate Specification (Sequential, after Stage 0)

Must be locked in writing before any data is examined:

**Gate 1 — L2 OOS discrimination test:**
- Population: all 183 OOS scanner fires
- Test: Fisher's exact test, L2-present Good rate vs L2-absent Good rate
- Threshold: >=15pp discrimination, Wilson 95% CI lower bound >= 35%
- Minimum n: >=30 L2-qualifying fires from the 183

**Gate 2 — Paper trading validation:**
- Wilson 95% CI lower bound on Good rate >= 40%
- Participation rate vs backtest baseline
- Block bootstrap CI if temporal autocorrelation detected
- **Failure protocol** (pre-specified): if CI lower bound < 40% at 50 trades, halt and diagnose. Max extension: 30 additional days. Decision authority: PO.

---

## Stage 2: Research (Critical Path)

| Task | Type | Dependency | Effort |
|---|---|---|---|
| **B3: L2 OOS on 183 scanner fires** | Backtest | A3 complete | Medium |
| B5-backtest: Re-score 236 entries at B1 open | Data query | Parallel to B3 | Low |

**B3 is the make-or-break test.** If ORB entry discriminates on scanner-filtered candidates (Good rate significantly above 35%), the strategy pipeline works. If not, L2 needs redesign.

---

## Stage 3: Workshop Pipeline Build (Parallel with Stage 2)

| Story | Dependency | Effort |
|---|---|---|
| L1 scanner encoding in MarketScanner | A6 resolved | Medium |
| L2 ORB entry framework (thresholds as config) | A3 complete | Medium |
| RVOL rolling fix (if A1 finds static) | A1 result | Medium |
| ema9_5m_d3 exit rule spec + TradingEngine impl | Rule spec by Manager/PO | Medium-High |
| Data feed staleness detection | Independent | Low |
| Polygon-T212 timestamp offset resolution | Independent | Low |

---

## Stage 4: Paper Trading

**Entry condition:** All of Stage 0 resolved + Stage 1 gates locked + Stage 2 B3 passed Gate 1 + Stage 3 stories complete.

**Design:**
- 30-day shadow minimum; 90-day target
- Target: 100 trades (contingency: if <50 at day 60, reassess)
- Three-point fill tracking: signal-fire price, B1-open price, actual fill price
- Evaluate at Gate 2

**L1-only staged paper trading** (Optimist proposal): run scanner only (no entry/exit) to validate fire rate and infrastructure. Deferred to PO decision — requires explicit quarantine commitment ("results are infrastructure data, not strategy data") before approval.

---

## Timeline Estimate

| Stage | Duration | Notes |
|---|---|---|
| Stage 0 (audit) | 1-2 weeks | Parallel tasks, A1 is gating |
| Stage 1 (gate specs) | 2-3 days | Sequential, after Stage 0 |
| Stage 2 (research) | 1 week | B3 is the critical test |
| Stage 3 (Workshop) | 2-3 weeks | Parallel with Stage 2 |
| Stage 4 (paper) | 30-90 days | Per literature + Statistician |
| **Total to paper start** | **~4-6 weeks** | **Gated on A1 result** |
| **Total to live readiness** | **~4-7 months** | **Gated on Gate 2 pass** |

---

## Top 5 Risks (Challenger)

1. **A1 (RVOL static baseline):** If static, may invalidate 56% Good rate. Unknown remediation timeline. Could restart L2 validation.
2. **B3 failure:** If L2 doesn't discriminate on scanner fires, the strategy pipeline doesn't work. Root cause investigation needed.
3. **Execution bias (B0→B1 gap):** All PnL figures are upper-bound. B5-backtest measures the real gap. If >3%, strategy economics degrade materially.
4. **Paper trading sample:** At 3 fires/day and ~50% L2 pass rate, need ~60-90 days for 100 trades. If fire rate or pass rate degrades, timeline extends.
5. **Gate 2 failure protocol undefined:** Must pre-specify stop/continue criteria before paper starts.

---

## What "Validated and Ready for Paper Trading" Means

The team agrees on this minimum bar:

1. All Stage 0 audit items resolved (no unverified assumptions in the pipeline)
2. Gate specs locked in writing before any Stage 2 data is examined
3. B3 passes Gate 1 (L2 entry discriminates on scanner-filtered candidates)
4. Workshop pipeline complete (scanner + entry + exit implemented with thresholds as config)
5. Three-point fill tracking operational
6. Gate 2 failure protocol pre-specified

If all six conditions are met, paper trading can begin.

---

## Agent Consensus Summary

| Agent | Key contribution | Stance |
|---|---|---|
| **Optimist** | Three parallel streams (research / audit / Workshop). L1-only staged paper as infrastructure test. | Push for speed via parallelism |
| **Challenger** | A1 is highest risk. B4 is prerequisite for B3. Gate 2 failure protocol must be pre-specified. | Sequence discipline over speed |
| **Statistician** | 50-100 trades minimum for paper. Wilson CI for all gates. BH correction for any sweep. | Statistical rigour throughout |
| **Exec Realist** | 3 deployment blockers (PM vol threshold, Benzinga latency, position sizing). VPS adequate. | Build feasible, timeline realistic |
| **Scout** | Literature anchors: 50-100 trades minimum. Staged validation (backtest → paper → small live → full) is standard. | External validation of approach |

---

_This is the team's proposal. We own it. PO approval required before execution begins._
