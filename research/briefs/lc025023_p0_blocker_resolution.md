# LC-2025-023 Phase 0 — Blocker Resolution Document

_Date: 2026-03-30 | Sessions: P0-validation (LC-2025-024) | Agents: Challenger + Statistician_
_Status: APPROVED (pending PO confirmation)_

This document resolves the four blockers identified in the scanner research plan before Phase 1 begins. It becomes part of the permanent baseline.

---

## Blocker A — Control Group: RESOLVED

### Definition
- **Target group (runners):** Ticker-dates where RTH range >= 100% AND gap >= 10% from prior close
- **Control group (non-runners):** Ticker-dates where gap >= 10% from prior close BUT RTH range < 100%

### Population
| Group | N | % of gap>=10% |
|---|---|---|
| Runners | 177 | 5.0% |
| Non-runners (control) | 3,342 | 95.0% |
| **Total gap >= 10%** | **3,519** | 100% |

### Key separating variables (runners vs control)

| Variable | Runners (N=177) | Control (N=3,342) | Separation |
|---|---|---|---|
| Gap% median | +22.2% | +15.7% | Moderate |
| Gap% mean | +45.4% | +43.3% | Weak (means similar) |
| PM volume median | 2,224,790 | 183,828 | **12x** |
| PM dollar vol median | $9,694,722 | $743,300 | **13x** |
| PM bar count median | 218 | 98 | 2.2x |

**Strongest signal: Pre-market volume (12-13x median separation).** Gap% alone is a weak discriminator (means nearly identical, medians differ by only 6.5pp).

### Challenger flags on control group
- Mean/median inversion in PM dollar vol (control mean > runner mean, but control median << runner median). Large-cap non-runners inflate control mean. Simple threshold will mis-include this group.
- Ticker repeats exist (max 109 days per ticker) — independence assumption may be violated for clustering-sensitive tests.
- Some control entries may be "near-runners" (80-99% range). Consider defining control as <50% range for cleaner separation.

---

## Blocker B — 100%+ Move Definition: RESOLVED

### Locked Definition
**A "100%+ move" is defined as:**
```
(max(bar_high) - min(bar_low)) / min(bar_low) >= 1.0
```
**Using RTH bars only (ts_minute 570-959, 09:30-15:59 ET).**

### Why RTH only
- Pre/post market inclusion inflated the original universe. 234 of the original 450 runner-days (52%) do NOT qualify under RTH-only because their 100%+ range depended on pre/post market bars.
- For scanner research, RTH-only is the correct definition because: (a) we trade during RTH, (b) the exit rules operate on RTH bars, (c) pre-market range is not observable at entry time for the portion that occurs after the open.

### Impact on original universe
| | Count |
|---|---|
| Original 450 (all bars, quality filtered) | 450 |
| RTH-only 100%+ (no quality filter) | 782 |
| In both (original AND RTH 100%+) | 216 |
| Original only (PM-inflated) | 234 |
| RTH-only new (no quality filter match) | 566 |

**The 566 "new" RTH-only runners are NOT a logical contradiction.** They are stocks that moved 100%+ during RTH but failed the original quality filters (mcap >= $10M, type=CS, major exchange, float_turnover >= 0.50). These are micro-caps, OTC stocks, warrants, etc.

**For Phase 1 scanner research:** Use the 782 RTH-only runners as the target population (no quality filters — the scanner should find candidates regardless of market cap). Quality filters can be applied as a second-stage refinement after the scanner signal is validated.

---

## Blocker J — True Base Rate: RESOLVED

### Base Rate
**0.694% of all ticker-dates are 100%+ RTH movers.**

| Metric | Value |
|---|---|
| Total ticker-dates | 112,679 |
| 100%+ RTH runners | 782 |
| Base rate | **0.694%** |
| 95% Wilson CI | [0.646%, 0.744%] |

This confirms the Statistician's earlier estimate of 0.3-0.8% (the rate falls within this range).

### Lift by gap threshold

| Gap threshold | Total days | Runners | Rate | Lift |
|---|---|---|---|---|
| All (>=0%) | 112,011 | 731 | 0.65% | 1.0x |
| >= 5% | 9,607 | 264 | 2.75% | **4.0x** |
| >= 10% | 3,519 | 177 | 5.03% | **7.2x** |
| >= 15% | 1,934 | 133 | 6.88% | **9.9x** |
| >= 20% | 1,250 | 100 | 8.00% | **11.5x** |
| >= 30% | 688 | 71 | 10.32% | **14.9x** |
| >= 50% | 322 | 39 | 12.11% | **17.5x** |

**Gap% is a significant first-pass filter.** At gap >= 10%, the universe shrinks from 112K to 3.5K days (97% reduction) while retaining 177/782 = 22.6% of runners. The runner rate increases from 0.65% to 5.03% — a 7.2x lift.

### Monthly runner rate (regime stability)

| Period | Rate | Comment |
|---|---|---|
| May-Jun 2025 | 1.04-1.05% | Early period, higher |
| Jul-Dec 2025 | 0.53-0.88% | Stabilises |
| Jan-Mar 2026 | 0.48-0.77% | Consistent with Jul-Dec |

Rate is relatively stable after initial period. No major regime break visible. Slight downward trend (May-Jun vs Jan-Mar) but within normal variation.

### Gap% definition
`gap_pct = (first_bar_open - prev_day_close) / prev_day_close × 100`

Uses the **first bar open** of the day (which could be a pre-market bar at 04:00 ET) vs the **prior day RTH close**. This is observable before market open — no lookahead.

668 ticker-dates (0.6%) have null gap_pct (no prior day data or no first bar). 51 runners have null gap. These are excluded from gap-filtered analyses but included in the base rate computation.

### Statistical requirements for Phase 1 (Statistician confirmed)
- N >= 500 ticker-days per arm for detecting 2pp improvements at 80% power
- N = 3,519 (gap >= 10%) detects effects as small as 2pp in runner rate
- BH correction mandatory across all tested thresholds
- Temporal split: lock cutoff before threshold examination

---

## Blocker X4 — Benzinga Timestamps: RESOLVED

### Timestamp type
The `published` field in Benzinga news cache uses **ISO 8601 format** (e.g., `2025-08-11T08:32:28Z`). This is the **publish timestamp**, not an ingest timestamp.

### Availability
- 95,115 news files cached (ticker_date.json format)
- Fields: benzinga_id, title, teaser, published, tickers, channels, tags
- Channels include: 'earnings', 'movers', etc.

### Usability for scanner
- Publish timestamp is usable for pre-market timing (can determine if news was published before 09:30 ET)
- Precision: second-level (adequate for pre-market scanner which operates on minute-level)

### Remaining items (deferred to Phase 1)
- News coverage rate for runner ticker-dates (what % have news?)
- Pre-market vs intraday breakdown of publish times
- Channel distribution for runner vs non-runner days

These are Phase 1 data queries, not blockers.

---

## Ticker Independence Note

Top ticker has 109 days in the dataset (0.10% of total). No ticker exceeds 5% of entries. Clustering correction is NOT required at the aggregate level (Statistician threshold: flag if any ticker >= 5%). However, within the runner population (N=782), repeat tickers should be checked — if the same 50 tickers account for most of the 782 runner-days, the effective sample is smaller than N suggests.

---

## Data Integrity Notes

| Item | Status |
|---|---|
| 112,679 ticker-dates in signal_bars.parquet | Confirmed |
| Pre-market bar coverage | 85.3% of ticker-dates have PM bars |
| Gap% null rate | 0.6% (668 days) — no prior day data |
| signal_bars.parquet universe construction | Unknown — exchange/activity filters may apply. Not yet audited. |

**Open item:** The exact construction rules for the 112,679-entry universe are undocumented. This is flagged but NOT blocking for Phase 1 — the universe is what it is, and all analyses are conducted on this population. The construction question becomes relevant if we need to extrapolate to a different ticker universe in production.

---

## Summary: Blocker Status

| Blocker | Status | Locked Decision |
|---|---|---|
| **A — Control group** | **RESOLVED** | Gap>=10%: 3,519 days (177 runners, 3,342 control) |
| **B — 100%+ definition** | **RESOLVED** | RTH bars only: (max(bar_high) - min(bar_low)) / min(bar_low) >= 1.0 |
| **J — Base rate** | **RESOLVED** | 0.694% [0.646%, 0.744%] on 112,679 ticker-dates |
| **X4 — Benzinga timestamps** | **RESOLVED** | `published` field, ISO 8601, second-level precision |

**Phase 1 may proceed** with these definitions locked. Any change to these definitions requires a new blocker resolution document.
