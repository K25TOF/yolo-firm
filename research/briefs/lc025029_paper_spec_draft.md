# Paper Trading Specification — Scanner Strategy

_Source: LC-2025-034 + LC-2025-037 + LC-2025-039 (Signal 3 revision) | Status: DRAFT v2 for PO final lock_
_Signal 3 VWAP filter integrated. All parameters recalibrated by Statistician. Challenger: 4 blocking items._
_CRITICAL: 80% IS Good rate cannot anchor live parameters. Paper trading IS the OOS test. Conservative calibration._

---

## Strategy Summary

**Scanner (L1):** gap >= 15% + PM dollar volume >= $5M + pre-9:30 ET Benzinga news (~3 fires/day)
**[REVISED] L2 Filter:** VWAP position > +2% at ORB close (ts_minute=574) — reduces to ~0.8 trades/day
**Entry:** First RTH bar open on L2-qualifying fires
**Exit:** ema9_5m_d3 (4 consecutive 5-min closes below EMA9) OR hard stop -10% OR EOD force-close
**[REVISED] Position sizing:** 1 unit per trade (fixed), max 3 concurrent — conservative until OOS confirms precision
**[REVISED] Duration:** Target 50 trades minimum, 100 target (~63-125 trading days at 0.8/day)

---

## Entry Rule

**Trigger:** Scanner fire confirmed pre-market (all three L1 conditions met before 09:30 ET)

**[REVISED] L2 Filter — VWAP position at ORB close:**
- At ts_minute = 574 (09:34 ET, last bar of 5-min ORB window), compute:
  `vwap_position = (bar_close[574] - vwap[574]) / vwap[574] × 100`
- Entry ONLY if `vwap_position > +2%`
- VWAP must be the fixed RTH-reset HLC3 version (Workshop story delivered, PO confirmed)
- IS evidence: 80.8% Good rate in above-VWAP group (42/52), +50.3pp lift, p < 0.000001
- **CAUTION: 80% is IS. Paper trading is the OOS test. Do not assume this rate holds.**

**Entry price:** `bar_open` of first RTH bar (ts_minute = 570, 09:30 ET)
- This is the earliest executable price. bar_close[B0] is not transactable.
- If RTH open is not available (halt, missing data): skip this fire, log as missed.
- Note: entry is at 09:30 but L2 filter evaluates at 09:34. Entry is BEFORE the filter.
  Implementation: enter at 09:30 on all scanner fires, exit immediately if VWAP filter fails at 09:34.
  OR: wait until 09:34, confirm VWAP, then enter at bar_open[575]. PO to decide.

**Maximum 3 concurrent positions.** If 3 positions are open when a new L2-qualifying fire occurs:
- Log the fire as "missed — position limit"
- Track missed fire count separately
- If miss rate exceeds 30% of total fires in any 30-trade window, review position limit

**Logging on EVERY scanner fire (regardless of L2 filter):**
- vwap_position (Signal 3 value)
- orb_vol_decel (Signal 2 value, for future L2 validation)
- Whether L2 filter passed or failed
- If failed: reason (VWAP below threshold / missing data / other)

---

## Position Sizing

**[REVISED] Per-trade size:** 1 unit (fixed dollar amount, e.g. $500 or $1,000 — PO specifies)
- Conservative: 80% IS Good rate is unconfirmed OOS. Paper trading IS the OOS test.
- At 3 concurrent max: maximum 3 units exposed simultaneously
- Hard stop at -10% = maximum 0.1 units loss per trade at theoretical stop level
- **Position sizing increase checkpoint:** After n >= 50 fires with OOS precision confirmed >= 25%
  (Wilson CI lower >= 15%), position sizing review is triggered. Not automatic — PO decides.

**Cost assumption:** Apply 2% per-trade round-trip cost to all paper P&L calculations from day one.
- Rationale: sub-$5 small-cap spread (0.5-3%) + entry slippage (0.5-1%) + exit slippage (0.5-1%)
- This is a fixed haircut applied to the final P&L of every trade, not an entry price adjustment

**Gap-through-stop risk acknowledged:**
- Hard stop fires as a signal at -10%, but actual fill on small caps can be -20% to -40% (halt gaps, thin books)
- Paper trading logs BOTH the signal trigger price (-10%) and simulated actual fill price
- The gap between them becomes an input to the live position sizing model
- If median gap-through exceeds 5pp in paper trading, position sizing must be reduced before live

---

## Exit Rules

### Primary: ema9_5m_d3
- **EMA9 computation:** `ema[i] = close[i] × 0.2 + ema[i-1] × 0.8`, seeded at first 5-min bar of RTH session
- **5-min bars:** Aggregate 1-min bars into 5-min buckets. Close = last 1-min close in bucket.
- **Exit trigger:** 4 consecutive 5-min bar closes below EMA9
- **Exit price:** Close of the 4th consecutive bar below EMA9
- **Evaluation starts:** First 5-min bucket AFTER the bucket containing entry bar
- **In-sample validated only.** Paper trading is the first forward test.

### Safety: Hard stop -10%
- Exit if `(current_price - entry_price) / entry_price <= -0.10`
- Checked on every 1-min bar close during the trade
- Log both trigger price and simulated fill price (see gap-through-stop above)

### Fallback: EOD force-close
- Close all open positions at 15:55 ET (5 minutes before RTH close)
- Exit price: bar_close at ts_minute = 955

### Early-exit fallback (first 5-min bar)
- **Definition:** If the first COMPLETE 5-min bar after entry (ts_minute 575-579 bucket) closes below entry price, exit immediately at that bar's close.
- **"First complete 5-min bar"** = the 5-min bucket starting at ts_minute 575 (09:35 ET). Entry is at 09:30; this bar is 09:35-09:39.
- **Interaction with EMA seeding:** During the first 45 minutes (9 five-min bars), EMA9 is seeding and unreliable. This fallback protects during the seeding window.
- **Does NOT interact with hard stop:** Both can be active simultaneously. Whichever fires first wins.

---

## Monitoring: Kill Criterion

### [REVISED] Primary kill test
**Exact binomial test, one-sided. H₀: true Good rate >= 11.5%. H₁: true Good rate < 11.5%.**

11.5% = OOS validated scanner-only precision. This is the CATASTROPHIC FAILURE gate — kills the strategy only if it performs worse than the unfiltered scanner. It is NOT a Signal 3 quality gate.

**Rationale (Statistician + Challenger):** The 80% IS Good rate cannot anchor the kill criterion because paper trading IS the OOS test. If we set H₀ = 80% and Signal 3 OOS precision is 40% (still excellent), the kill criterion would fire incorrectly. The correct null is the minimum acceptable performance — scanner-only baseline.

### [REVISED] Checkpoints

| n (L2-qualifying fires) | Type | Kill threshold | Action |
|---|---|---|---|
| **5 days** | **Fire rate check** | < 0.3 fires/day average | Investigate scanner/VWAP implementation. Not a kill. |
| **30** | **Early warning** | 0 Good trades observed | Flag to PO. NOT a formal kill. |
| **60** | Formal kill | <= 1 Good trade | Kill paper trading. Route to diagnosis. |
| **100** | Formal kill | <= 4 Good trades | Kill paper trading. Route to diagnosis. |

- Per-checkpoint alpha: 0.0125 (Bonferroni, 4-checkpoint denominator)
- Family-wise alpha: <= 5%
- At 0.8 trades/day: n=30 at ~38 days, n=60 at ~75 days, n=100 at ~125 days
- **Day 5 fire rate check added:** If VWAP filter fires on < 15% of scanner entries (vs IS 28%),
  investigate before continuing — possible implementation issue or regime change.
- If killed: enter Gate 2 failure protocol (per gate specs document)

### Kill decision authority
- Early warning (n=30): PO reviews, decides continue/investigate
- Formal kill (n=60+): Automatic unless PO explicitly overrides with written justification

---

## Data Logging Requirements

Every scanner fire during paper trading must log:

| Field | Description |
|---|---|
| date | Trading date |
| ticker | Stock symbol |
| scanner_fire_time | Timestamp when all 3 scanner conditions confirmed |
| gap_pct | Gap from prior close |
| pm_dollar_vol | Pre-market dollar volume |
| news_present | Boolean + Benzinga article ID |
| entry_price | bar_open at RTH open (actual paper entry) |
| **orb_vol_decel** | **volume(last 2 ORB bars) / volume(first 2 ORB bars) — logged for future L2 validation** |
| orb_high | ORB high (5-min window) |
| orb_low | ORB low |
| exit_price | Price at exit |
| exit_type | ema9_5m_d3 / hard_stop / eod_close / early_exit_fallback |
| exit_time | Timestamp of exit |
| mfe_30bar | Max bar_high in first 30 bars after entry |
| mae_30bar | Min bar_low in first 30 bars after entry |
| pnl_gross | (exit_price - entry_price) / entry_price |
| pnl_net | pnl_gross - 2% cost assumption |
| mech_good | MFE_30bar >= 10% (D2-validated label, kappa=0.661) |
| stop_trigger_price | If hard stop: price at -10% signal |
| stop_fill_price | If hard stop: simulated actual fill price |
| missed | Boolean: was this fire missed due to position limit? |

---

## Vol_Decel Logging (Future L2 Validation)

**PO direction:** Log `orb_vol_decel` on every scanner fire from day one. Do not use it for entry/exit decisions during this paper phase.

When paper trading accumulates sufficient n in each vol_decel tercile (target: n >= 30 per tercile), retest Gate 1 formally:
- Mann-Whitney U on MFE between top and bottom terciles
- Wilson CI lower on Good rate in top tercile >= 40%
- Good rate lift >= 10pp

If Gate 1 passes on accumulated paper data: vol_decel becomes an active L2 filter for the next phase.

---

## Paper Trading Duration

**[REVISED]**
- **Minimum:** 50 L2-qualifying trades (for Gate 2 Wilson CI to be informative)
- **Target:** 100 trades (for adequate kill criterion power at formal checkpoints)
- **Estimated time:** ~63-125 trading days at 0.8 L2-qualifying fires/day
- **Contingency:** If < 15 L2-qualifying trades at day 60, reassess VWAP filter fire rate
- **L1-only infrastructure phase:** Scanner fires logged for first 5 trading days before paper
  trading begins (quarantined — infrastructure validation only, per PO commitment)
- **Day 5 fire rate checkpoint:** Confirm VWAP filter fires on >= 15% of scanner entries.
  If below, investigate implementation before continuing.

---

## Success Criterion (Gate 2, from locked gate spec)

**[REVISED]** Gate 2 retains the same structure but with Signal 3 context:
- Wilson 95% CI lower bound on Good rate (MFE_30bar >= 10%, D2-validated label) >= 40%
- Participation rate >= 80% of baseline
- Block bootstrap CI if n < 75 or Ljung-Box detects autocorrelation
- Both must hold for Gate 2 to pass
- **Note:** At 80% IS Good rate, the 40% Wilson CI lower bound is conservative. If OOS confirms
  >= 60% Good rate at n=50+, Gate 2 will pass early. The 40% floor is retained as the minimum
  acceptable performance, not the expected outcome.
- **Signal 3-specific MFE tracking:** Track MFE distribution separately for Signal 3 trades
  (above-VWAP entries). If Signal 3 Goods systematically have lower MFE than full population,
  flag for Gate 2 review before final verdict.

---

_This spec is DRAFT. Final lock requires PO approval. Once locked, no changes permitted during paper trading._
