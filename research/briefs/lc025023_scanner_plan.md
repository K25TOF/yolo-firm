# LC-2025-023: Pre-Market Scanner Research Plan

_Session: LC-2025-023 | Date: 2026-03-30 | All 6 agents contributed | Cost: $1.48_

---

## Strategic Context

The ORB strategy research (LC-2025-014) established that we can time entries well on stocks we already know are runners (56% Good rate on PO-curated subset). But the raw ORB signal on all stocks produces only ~10-13% Good entries. The missing piece: **identifying runner candidates before market open, without hindsight.**

This plan addresses that gap. Scanner → ORB entry → Exit rules form the complete production strategy.

---

## Literature Findings (Scout)

| Topic | Key Finding | Source Type | Confidence |
|---|---|---|---|
| Gap threshold | Gap >= 10-20% from prior close as baseline filter | Practitioner (Warrior Trading, SMB Capital) | High |
| PM volume | >= 100K shares pre-market; $500K dollar volume = "institutional interest" | Practitioner + Academic (Gao et al. 2018) | High |
| Time window | Signal concentrates 8:00-9:30 ET | Practitioner consensus | Moderate |
| Float | < 10M shares amplifies gap moves | Academic (Bhattacharya et al. 2020) + Practitioner | High |
| Short interest | > 20% of float + gap = squeeze potential | Academic (Lamont & Thaler 2003) + Practitioner | Moderate |
| Catalyst hierarchy | Tier 1 (FDA/M&A/earnings beat) sustains; Tier 3 (offerings/upgrades) fades | Academic (Brusa et al. 2020) + Practitioner | High |
| Pre-market returns | Predict same-day returns for small caps | Academic (Bhattacharya et al. 2020, JFM) | High |

**Internal contradiction flag:** EXP-024 found offerings channel at 50% WR on vol_filter trades. Scout says offerings "almost always fade gaps." Different metrics (re-entry momentum vs gap sustainability). Not a true contradiction.

---

## Proposed Hypotheses (Optimist, audited by Challenger)

### HYP-PM-1: Catalyst-Typed Gap Quality Filter
- **Signal:** Gap >= 10% + Benzinga news within 12h + Tier 1/2 catalyst + PM volume >= 50K shares
- **Grounding:** Strongest combined academic + practitioner evidence
- **Blocker E:** Benzinga channel immutability unconfirmed — channels may change retroactively
- **Blocker F:** EPS consensus data absent — "earnings beat" not classifiable from Benzinga alone
- **Data needed:** Benzinga channel-to-tier mapping (design work, no new data)

### HYP-PM-2: Float x Gap Interaction (Squeeze Potential)
- **Signal:** Float < 10M + gap >= 15% + short interest > 15% + PM volume > 5% of float
- **Grounding:** Strong academic + practitioner evidence. Explains our best tickers (MOBX, DXST)
- **Blocker G:** Float data is current-snapshot, not point-in-time (conservative bias — documented)
- **Data needed:** Float from Benzinga endpoint; short interest has 14-day reporting lag (FINRA)

### HYP-PM-3: Pre-Market Dollar Volume Profile
- **Signal:** PM dollar volume >= $500K by 9:15 ET + acceleration (last 30 min > first 60 min) + gap >= 5%
- **Grounding:** Gao et al. 2018 + practitioner consensus. Dollar volume normalises for price.
- **CRITICAL BLOCKER H:** Requires pre-market bar data pipeline. 3-5 day engineering story.
- **Blocker I:** $500K threshold uncalibrated for our sub-$5 universe
- **Highest information value per Optimist** — but gated on data pipeline

### HYP-PM-4: ORB x Pre-Market Gap Alignment
- **Signal:** Pre-market high + first 15-min RTH candle respects PM high as support + ORB breakout
- **Grounding:** Direct extension of our most validated signal (LC-2025-014 ORB)
- **Scope note:** Extends ORB rules — flagged for future session, not this plan
- **Data needed:** Pre-market high (lighter requirement than full PM bars)

### HYP-PM-5: Multi-Factor Composite Score
- **Signal:** Weighted composite of gap%, PM RVOL, float (inverted), catalyst tier, short interest
- **Priority:** LAST — only after simpler models tested. Overfitting risk on small samples.

---

## Data Availability Matrix

| Signal | Available Now? | Source | Gap/Action |
|---|---|---|---|
| gap_pct (from prior close) | YES | signal_bars.parquet column | None |
| Pre-market 1-min bars | YES (84% coverage) | signal_bars.parquet, ts_minute 240-569 | Verify coverage on 100%+ move days |
| Pre-market volume/dollar vol | DERIVABLE | Sum from PM bars | Pipeline script needed |
| Pre-market high | DERIVABLE | max(bar_high) from PM bars | Pipeline script needed |
| Benzinga news + channels | YES | 95,115 cached files | Channel-to-tier mapping needed |
| Benzinga timestamp type | UNCONFIRMED | Cache audit needed (30 min) | [EXEC FLAG X4] |
| Float (shares outstanding) | FETCHABLE | Benzinga float endpoint (~15 min) | Coverage unknown for OTC/micro |
| Short interest | NOT CACHED | Benzinga endpoint; 14-day lag | Secondary screen only [EXEC FLAG X6] |
| Market cap | YES | ticker_metadata.parquet | Current-snapshot, not point-in-time |
| Exchange/type | YES | ticker_metadata.parquet | Current-snapshot bias (OTC uplisting risk) |
| EPS consensus | NOT AVAILABLE | Would need new data source | Tier 2 catalyst uses announcement type only |

**Key finding: Pre-market bars EXIST in signal_bars.parquet.** ts_minute starts at 240 (04:00 ET). 84% of ticker-dates have PM bars (~50 bars average). This is the critical enabler — no new Polygon fetches needed for historical research.

---

## Blocking Issues (Challenger)

| ID | Issue | Blocks | Severity |
|---|---|---|---|
| **A** | No control group (gap-up non-runners) — precision uncalculable | All hypotheses | **CRITICAL** |
| **B** | "100%+" definition ambiguous (range vs open-to-high) | Training data design | High |
| **C** | Scanner != trading signal — must separate universe from entry | Success metric | High |
| **D** | Date distribution of 450 universe unknown — regime risk | Threshold calibration | High |
| **J** | Base rate denominator survivorship-biased (1.7% is wrong) | Power calculations | High |
| E | Benzinga channel immutability unconfirmed | HYP-PM-1 | Medium |
| G | Float is current-snapshot | HYP-PM-2 | Medium (conservative) |
| H | PM bar pipeline = 3-5 day engineering | HYP-PM-3 | Medium (data exists) |
| I | $500K threshold uncalibrated | HYP-PM-3 | Low |

**Blocker A is critical.** To test any scanner hypothesis, we need a control group: stocks that gapped up but did NOT make a 100%+ move. The 450-stock universe only contains successes. The full signal_bars.parquet (~5,000 tickers) is the control population — but we need to identify which non-runner days had gap >= X% to compute false positive rate.

---

## Statistical Requirements (Statistician)

| Requirement | Value | Rationale |
|---|---|---|
| True base rate | 0.3-0.8% (not 1.7%) | Survivorship bias in denominator corrected |
| Sample for 2x lift detection | ~5,200 ticker-days (at p0=0.5%) | 80% power, alpha=0.05 |
| Sample for 3x lift (primary bar) | ~1,700 ticker-days | More realistic target |
| BH correction | Mandatory across all variants | Pre-register N before examining |
| Temporal split | Mandatory; lock cutoff before threshold examination | Prevents in-sample fitting |
| Clustering correction | Required if any ticker >= 5% of flagged population | Known small-cap repeat pattern |
| Minimum reporting | n, test, p-value/CI, BH status, lift + NNS | Standard for all directions |

**HYP-PM-3 untestable without pipeline.** HYP-PM-5 premature (needs 10K+ ticker-days).

---

## Execution Feasibility (Execution Realist)

**Executable now (no new infrastructure):**
- Float data fetch for universe (~15 min)
- Benzinga timestamp audit (~30 min)
- Gap% analysis on existing signal_bars.parquet
- Channel-to-tier mapping schema (design only)

**Executable with engineering story (3-5 days each):**
- Pre-market bar data pipeline extension [Blocker H]
- MarketScanner pre-market operating mode (future live deployment)

**Not currently executable:**
- EPS consensus estimates (new data source onboarding)
- Point-in-time float data
- Real-time short interest

**Live deployment notes:**
- MarketScanner currently runs from 09:30 ET — would need 04:00 start for PM scanning
- VPS (2 CPU / 8GB) adequate for 60-second polling pre-market
- Polygon 1-minute timestamp offset affects "last 30 min" window by 1 bar [EXEC FLAG X10]

---

## Connection Diagram: Complete Strategy Pipeline

```
PRE-MARKET (04:00-09:30 ET)
  Scanner identifies candidates:
    Gap% >= threshold (from grouped daily / snapshot API)
    + PM dollar volume >= threshold (from PM bars)
    + Catalyst tier 1/2 (from Benzinga news)
    + Float < threshold (from Benzinga float endpoint)
    → Candidate list (~5-20 tickers per day)
           |
           v
RTH OPEN (09:30+)
  ORB Entry Timing (LC-2025-014):
    Wait for ORB window (5-min)
    B0: bar_close >= orb_high AND vol_ratio >= 2.0
    B-1 coil: within -4% of orb_high
    Liquidity gate: $10K/min
    → Enter trade at bar_close[B0]
           |
           v
IN-TRADE
  Exit Rules (LC-2025-014 Phase 3):
    Layer 1: Hard stop -10% from entry (safety floor)
    Layer 2: ema9_5m_d3 (4 consecutive 5-min closes below EMA9)
    Layer 3: Guard C on catastrophic declines (conditional)
    Fallback: EOD force-close
```

---

## Research Sequencing

### Phase 0 — Resolve Blockers (before any hypothesis testing)

| Step | Task | Effort | Blocks |
|---|---|---|---|
| **P0.1** | Build control group: identify all gap >= 10% days in signal_bars.parquet that did NOT make 100%+ move | Low (data query) | Blocker A |
| **P0.2** | Define "100%+" precisely: (max(bar_high) - min(bar_low)) / min(bar_low) using RTH bars only | Low (decision) | Blocker B |
| **P0.3** | Compute true base rate on full population (all ticker-days, not just runner universe) | Low (data query) | Blocker J, all power calcs |
| **P0.4** | Benzinga timestamp audit — publish vs ingest time | Low (30 min) | EXEC FLAG X4 |

### Phase 1 — Test Simple Signals (no new infrastructure)

| Step | Hypothesis | Data Needed | Population | Effort |
|---|---|---|---|---|
| **P1.1** | Gap% alone as predictor of 100%+ move | gap_pct from signal_bars + control group | All ticker-days with gap >= 5% | Low |
| **P1.2** | Catalyst presence (news vs no-news) as predictor | Benzinga cache join | Same as P1.1 | Low |
| **P1.3** | Float < 10M as predictor (conditional on gap) | Float fetch + join | Same as P1.1 | Low-Medium |

### Phase 2 — Test PM Volume Signals (requires PM bar pipeline)

| Step | Hypothesis | Data Needed | Effort |
|---|---|---|---|
| **P2.1** | PM dollar volume >= $500K as predictor | PM bars from signal_bars.parquet | Medium (pipeline script) |
| **P2.2** | PM volume acceleration (last 30 min vs first 60 min) | Same | Medium |
| **P2.3** | PM high vs prior close alignment with ORB | PM high from PM bars | Medium |

### Phase 3 — Combine and Validate

| Step | Task | Dependency |
|---|---|---|
| **P3.1** | Combine best single-factor signals into 2-3 factor model | P1 + P2 results |
| **P3.2** | Temporal OOS validation (train on May-Dec 2025, test Jan-Mar 2026) | P3.1 |
| **P3.3** | Connect scanner output to ORB entry: does scanner-filtered ORB Good rate exceed unfiltered? | P3.2 |

---

## Success Criteria

| Level | Criterion | Implication |
|---|---|---|
| **Minimum viable** | Any single pre-market signal achieves >= 2x lift over base rate (scanner flags 2-3% of stocks, base rate 0.5%) with n >= 1,700 | Scanner has signal, worth refining |
| **Useful** | 2-factor model achieves >= 3x lift with precision >= 5% (1 in 20 flagged stocks is a runner) | Scanner usable as first-pass filter |
| **Production-ready** | Combined scanner + ORB entry produces >= 40% Good rate on OOS entries with n >= 95 | Full strategy pipeline validated |

---

## Key Risks

1. **Base rate is very low (0.3-0.8%)** — even a 3x lift only reaches 1-2.4% hit rate. The scanner must be VERY selective to be useful.
2. **Small sample of runner days (~450)** — limits the number of signals we can test before running out of degrees of freedom.
3. **PM bar coverage asymmetry** — adequate on catalyst days (runners have active pre-markets), sparse on control days. This biases toward finding PM volume as a signal whether or not it is real.
4. **Float data is current-snapshot** — conservative bias (documented) but unknown magnitude.
5. **Survivorship in runner universe** — the 450 stocks were identified by outcome. Any signal that correlates with the selection criterion will appear to work.

---

_All 6 agents contributed. Scout: literature. Optimist: 5 hypotheses. Challenger: 10 blocking issues.
Statistician: 7 statistical flags. Execution Realist: data availability + live deployment assessment._
