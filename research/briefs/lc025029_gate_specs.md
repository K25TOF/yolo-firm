# Gate Specifications — Path to Live Trading

_Session: gate-specs (LC-2025-033) | Date: 2026-03-31 | Statistician + Challenger_
_Status: **LOCKED** — PO approved 2026-03-31. All pre-conditions (PC1-PC6) computed and frozen. This document cannot be changed mid-Stage-2 or mid-paper-trading._

---

## Gate 1 — L2 OOS Discrimination Test

**Purpose:** Does ORB entry discriminate Good from Bad on scanner-filtered candidates?

**Population:** All 183 OOS scanner fires (Jan-Mar 2026).

**Method:**
1. For each fire, check if ORB entry condition is met: `bar_close >= orb_high AND vol_ratio >= 2.0x`
2. Split into L2-positive (ORB fires) and L2-negative (no ORB)
3. Compute MFE_30bar for both groups

**Test statistic:** Mann-Whitney U (one-tailed, L2+ MFE > L2- MFE)
- Supplemented by: Good rate lift (L2+ minus L2-) with Wilson 95% CI on each group
- Mann-Whitney U and Good rate test measure different properties (continuous rank ordering vs categorical separation). Both failing is a different diagnostic than one failing.

**Pre-specified thresholds:**
- Discrimination: >= 10pp Good rate lift (L2+ vs L2-)
- Hard floor: Good rate in L2+ group >= 40% (Wilson CI lower bound)
- Mann-Whitney U: p < 0.05 (one-tailed)

**Success criterion — ALL THREE required:**
1. Mann-Whitney U p < 0.05 (one-tailed)
2. Wilson 95% CI lower bound on L2+ Good rate >= 40%
3. Good rate lift >= 10pp

Gate 1 fails if ANY ONE is not satisfied. No "directional positive" language if the formal gate is not cleared.

**Minimum n:** L2+ >= 30, L2- >= 20, total classified >= 50.

**Contingency (L2+ n < 30):** Expand OOS window by 60 calendar days. If still < 30, retire L2.

**Challenger findings incorporated:**
- L2 threshold derivation must be confirmed as NOT derived from the 183 OOS entries (Finding 1 — blocking). Manager confirms: L2 entry conditions (bar_close >= orb_high, VR >= 2.0x) were defined in LC-2025-014, months before OOS data existed. No contamination.
- The 40% floor is derived from IS Good rate (56.6%) minus a buffer. Independent justification: 40% is the minimum at which the strategy expectancy is positive given median win size ~+25% and median loss ~-10% (2.5:1 win/loss ratio at 40% WR = +0% breakeven, accounting for ~0.5% execution cost per trade). This is an approximate economic argument, not derived from the IS distribution.

---

## Gate 2 — Paper Trading Validation

**Purpose:** Does the full stack produce profitable trades in live conditions?

### Good Rate Computation
- **Mechanical label:** MFE_30bar >= T → Good, MFE_30bar < T → Bad
- **T = 40th percentile of IS Good group MFE_30bar.** Manager computes T from the 150 IS Good entries and freezes it before paper trading opens.
- **Pre-condition:** Before freezing T, Manager provides MFE distribution overlap between IS Good and Bad groups + mechanical False Good/False Bad rates. If agreement with PO label < 70%, T is not a valid proxy (Challenger Finding 4).

### Autocorrelation Test
- **Default for n < 75: block bootstrap applied regardless** (Challenger Finding 5)
- **For n >= 75:** Ljung-Box Q on first 10 lags of binary Good/Bad sequence. If p < 0.05 at any lag → block bootstrap. Otherwise Wilson CI.
- **Supplementary: Wald-Wolfowitz runs test** on binary sequence (specifically designed for binary randomness)
- **Block bootstrap spec:** Stationary bootstrap (Politis & Romano), block length = ceil(n^(1/3)), 2,000 resamples, 95% CI from [2.5th, 97.5th percentile]

### Participation Rate
- **Denominator:** All scanner fires where L2 entry conditions are met (L2 is a filter — only L2-positive signals count in the denominator, per Challenger Finding 7a)
- **Numerator:** Trades where paper position was opened
- **Backtest baseline:** Manager confirms OOS execution rate explicitly before locking
- **Gate:** >= 80% of backtest baseline throughout. Flag if below 80% for >= 5 consecutive days.

### Sample Sizes
- **Minimum:** 50 trades (Gate 2 cannot produce a formal verdict below n=50)
- **Target:** 100 trades
- **Interim check at n=50:**
  - Wilson CI lower bound >= 45% → continue to n=100
  - Wilson CI lower bound < 35% → trigger failure protocol early
  - Between 35-45% → continue to n=100 (interim check does not protect against moderate underperformance — acknowledged per Challenger Finding 9)

### Success Criterion at Final n
- Wilson 95% CI lower bound on Good rate >= 40%
- Participation rate >= 80% of backtest baseline throughout
- Both must hold

---

## Gate 2 Failure Protocol

### Triggers
- Interim: Wilson CI lower bound < 35% at n=50
- Final: Wilson CI lower bound < 40% at final n
- Participation: below 80% for >= 5 consecutive days

### Diagnosis Procedure (four comparisons, in order)
1. **Execution:** Compare paper entry prices vs backtest entry prices. Mean slippage > 0.5% → execution degradation
2. **Distribution shift:** Mann-Whitney U (two-tailed) on paper MFE vs OOS backtest MFE. p < 0.05 → regime change
3. **Temporal clustering:** Rolling 10-trade Good rate. Consistently < 30% for >= 20 consecutive trades → clustering
4. **Signal integrity:** Sample 10 random fires. > 2 fail entry conditions → implementation error

### Extension vs Stop
- **Extension (30 days, one only, PO approval):** Execution problem (fixable) OR regime problem (anomalous period)
- **Full stop (PO approval + written root cause):** Implementation error OR persistent clustering (>= 30 consecutive trades < 30%)
- **Compound failure (participation AND Good rate fail simultaneously):** Default is FULL STOP regardless of individual diagnoses. Extension only if single root cause explains both AND fix is demonstrated (Challenger Finding 8).
- **Default if ambiguous:** Full stop. Burden of proof is on demonstrating failure is temporary.

### Review Ownership
| Event | Owner | Escalation |
|---|---|---|
| Interim check (n=50) | Manager | Routes to PO |
| Diagnosis (4 comparisons) | Manager executes | Statistician reviews, Challenger audits |
| Extension approval | PO | Cannot be self-approved |
| Full stop | PO | Written root cause required |
| Gate 2 pass | PO | Statistician sign-off on CI |

---

## Pre-Conditions (must be completed before any gate execution)

| # | Pre-condition | Owner | Status | Value |
|---|---|---|---|---|
| PC1 | T threshold from IS Good MFE 40th percentile | Manager | **DONE** | **T = 21.09%** (40th pctl of 112 IS Good entries' MFE_30bar) |
| PC2 | MFE overlap analysis | Manager | **DONE** | Agreement 74.9%, kappa 0.514. False Good rate 6.9% (5/72). False Bad rate 35.4% (45/127). Passes 70% agreement threshold. |
| PC3 | OOS baseline participation rate | Manager | **DONE** | **100%** (all 183 qualifying signals executed in backtest) → paper gate: >= 80% |
| PC4 | N variants in L2 sweep | Manager | **DONE** | **N = 1** (single pre-specified condition from LC-2025-014). BH correction not applicable. |
| PC5 | L2 threshold derivation confirmed as pre-OOS | Manager | DONE | LC-2025-014, months before OOS data existed |
| PC6 | Ljung-Box / runs test pre-specified for Gate 2 | Statistician | DONE | This document |

### PC1 Detail: T = 21.09%
A paper trade is labelled **Good** if MFE_30bar >= 21.09%. This value is FROZEN. It cannot be adjusted after paper trades are observed.

IS Good group MFE_30bar distribution: P10=7.87%, P25=14.67%, **P40=21.09%**, P50=25.05%, P75=52.20%, P90=87.36%.

### PC2 Detail: Mechanical Label Validation at T = 21.09%
On 199 IS entries (112 Good, 87 Bad):

| | Mechanical Good (MFE >= 21.09%) | Mechanical Bad (MFE < 21.09%) |
|---|---|---|
| **PO Good** | 67 (TP) | 45 (FN) |
| **PO Bad** | 5 (FP) | 82 (TN) |

- Agreement: 74.9% (passes Challenger's 70% threshold)
- False Good rate: 6.9% (only 5 Bad trades mislabelled as Good — very conservative)
- False Bad rate: 35.4% (45 Good trades mislabelled as Bad — T is strict, misses moderate Goods)
- Only 5.7% of IS Bad trades have MFE >= T — the threshold cleanly separates Bad trades
- The label is asymmetrically conservative: high confidence that "mechanical Good" entries are genuinely Good, but misses ~40% of genuine Goods. This is the correct direction for a validation label.

---

## Reporting Requirements

**Gate 1 report must include:**
1. n (L2+ group), n (L2- group)
2. Mann-Whitney U statistic and p-value (one-tailed)
3. Good rate in each group with Wilson 95% CI
4. Good rate lift (pp)
5. Pass/Fail against all three criteria

**Gate 2 report must include:**
1. n (paper trades), participation rate vs baseline
2. Autocorrelation test result + which CI method used (state explicitly)
3. Good rate with 95% CI
4. Pass/Fail against Wilson lower bound >= 40%
5. If failure: which diagnosis triggered and outcome

---

_This document is the contract. Once PO-approved, it cannot be changed mid-Stage-2 or mid-paper-trading._
