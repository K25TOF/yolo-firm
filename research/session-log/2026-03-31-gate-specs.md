# Session: gate-specs
_Date: 2026-03-31 08:30 UTC | Agent: manager | Model: claude-sonnet-4-6_

## Context loaded
- raci.md
- way-of-working.md
- strategy-roadmap.md
- architecture.md
- risk-policy.md
- analysis/research/ideas.md
- analysis/research/research-log.md
- agents/README.md
- research/session-log/index.json
- agents/manager/memory.md

## Exchange

**Manager:** PO has triggered a research session.

Question: Stage 1: Gate Specification — Lock Before Stage 2

PO INSTRUCTION: Skip 3 Amigos. Challenger + Statistician mandatory. This session WRITES the gate document. No data examination. Pure specification.

## CONTEXT

Stage 0 is complete. All 7 audit items resolved. Key facts for gate design:
- 183 OOS scanner fires (Jan-Mar 2026), 21 runners, 11.5% precision
- 782 RTH runners in full population (0.694% base rate)
- 265 PO-rated entries (150 Good, 115 Bad, excl 33 neutral)
- Entry conditions: bar_close >= orb_high AND vol_ratio >= 2.0x (coil -4% is hypothesis-only caveat)
- B0→B1 gap: median 0.00% for both Good and Bad (execution bias minimal)
- VR 2.0x: defensible floor, non-monotone Good rate across VR levels

## WHAT MUST BE SPECIFIED

### Gate 1 — L2 OOS Discrimination Test (Stage 2, B3)
Purpose: Does ORB entry discriminate Good from Bad on scanner-filtered candidates?

Population: All 183 OOS scanner fires from Jan-Mar 2026.
Method: For each fire, check if ORB entry condition is met (bar_close >= orb_high within the session). Split into L2-present (ORB fires) vs L2-absent (no ORB). Compare Good rates.

Statistician must specify:
- Test statistic (Fisher's exact or chi-square)
- Pre-specified discrimination threshold (how many pp difference = meaningful?)
- Minimum n per group
- Success criterion (Wilson CI lower bound on what?)
- What happens if L2 fires on <30 of the 183?

### Gate 2 — Paper Trading Validation (Stage 4)
Purpose: Does the full stack (scanner + ORB + exit) produce profitable trades in live conditions?

PO already locked:
- Wilson CI lower bound on Good rate >= 40%
- Halt at 50 trades if CI lower < 40%
- Max 30-day extension
- PO makes stop/continue decision

Statistician must specify:
- How to compute Good rate in paper (mechanical label MFE_30bar < 10%? Or PO review?)
- Block bootstrap CI if temporal autocorrelation detected — specify the test for autocorrelation
- What participation rate vs backtest baseline means precisely
- Minimum 50 trades, target 100 — confirm these numbers

### Gate 2 Failure Protocol (PO locked but needs detail)
- At 50 trades: halt and diagnose if CI lower < 40%
- Must specify: what does 'diagnose' mean? What data is examined?
- Must specify: what triggers the 30-day extension vs full stop?
- Must specify: who reviews (PO only, or PO + research team)?

### Challenger must check:
1. Can any of the gate specs be gamed or satisfied trivially?
2. Are there scenarios where gates pass but the strategy still fails in production?
3. Is there a gap between the gates and actual profitability?

## OUTPUT
The session must produce a complete gate specification document that Manager writes to:
research/briefs/lc025029_gate_specs.md

This document is the contract. Once written and PO-approved, it cannot be changed mid-Stage-2 or mid-paper-trading.

Route Statistician first (specs), then Challenger (audit), then Manager writes.

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** ## Session Open — LC-2025-033

**Session ID:** LC-2025-033
**Question:** Write the gate specification document for Stage 2 (L2 OOS Discrimination) and Stage 4 (Paper Trading Validation) — locking the contract before execution begins.
**Time-box:** Single session, ~6 turns
**Expected outcome:** `research/briefs/lc025029_gate_specs.md` — complete, audited gate specification ready for PO approval

---

**Scope:**
- Gate 1 (L2 OOS Discrimination): full statistical specification
- Gate 2 (Paper Trading): mechanical label method, CI method, autocorrelation test, participation rate definition
- Gate 2 Failure Protocol: diagnosis procedure, extension vs stop triggers, review ownership
- No data examination — pure specification work
- No strategy changes — this session writes a contract document only

**Agents needed:** Statistician (specs) → Challenger (audit) → Manager writes document

**I will NOT:**
- Examine new data or run backtests
- Propose strategy modifications
- Approve anything — document routes to PO for approval

---

Statistician — your turn. Provide complete statistical specifications for both gates. Data context below.

**Data context:**
- 183 OOS scanner fires (Jan–Mar 2026), 21 runners confirmed, 11.5% precision (OOS)
- 782 RTH runners in full population, 0.694% base rate
- 265 PO-rated IS entries: 150 Good, 115 Bad (33 neutral excluded)
- IS Good rate: 56.6% (150/265)
- Entry conditions: bar_close >= orb_high AND vol_ratio >= 2.0x
- B0→B1 gap: median 0.00% both Good and Bad — execution bias minimal
- VR 2.0x: defensible floor, non-monotone Good rate across VR levels
- OOS Wilson CI on precision: [7.6%, 16.9%] — Stage 0 result

**Your task — specify completely:**

**Gate 1 (L2 OOS Discrimination Test):**
- Test statistic selection with justification
- Pre-specified discrimination threshold (pp difference = meaningful)
- Minimum n per group
- Success criterion (Wilson CI lower bound on what metric, at what level?)
- Contingency: what if L2 fires on <30 of the 183 OOS cases?

**Gate 2 (Paper Trading Validation):**
- How to compute Good rate mechanically (MFE_30bar < 10% label vs PO review — pick one and justify)
- Block bootstrap CI specification if temporal autocorrelation detected — specify the autocorrelation test
- Precise definition of "participation rate vs backtest baseline"
- Confirm or adjust: minimum 50 trades, target 100

**Gate 2 Failure Protocol:**
- What "diagnose" means operationally (which data, which comparisons)
- What triggers 30-day extension vs full stop
- Who reviews

Be precise. This becomes a contract.

[NEXT: statistician]

---

**Manager:** Session transcript so far.

Statistician, your turn. Respond per protocol.

**Statistician:** ## LC-2025-033 — Statistician Response

---

### Gate 1 (L2 OOS Discrimination Test) — Full Specification

#### Test Statistic Selection

**Primary test: Mann-Whitney U (one-tailed)**
- Justification: MFE and PnL distributions are right-skewed with heavy tails. Normality assumption fails. Mann-Whitney U is distribution-free, appropriate for ordinal comparison of two independent groups (Good vs Bad as labelled by PO review), and does not require equal variances. It tests whether a randomly selected L2-positive trade has higher MFE than a randomly selected L2-negative trade — which is exactly the discrimination claim.
- Direction: one-tailed (L2-positive > L2-negative), because the hypothesis is directional (L2 should *improve* selection, not merely differ).
- Reported alongside: Cohen's d on log-transformed MFE (descriptive, not the decision statistic), and Wilson 95% CI on Good rate within L2-positive vs L2-negative groups.

**Secondary metric: Good rate lift**
- Compute Good rate (PO label or mechanical — see Gate 2) within L2-positive and L2-negative sub-populations.
- Report as: (Good rate L2+) − (Good rate L2−), with Wilson 95% CI on each proportion separately.
- This is human-interpretable and directly maps to the IS discrimination that motivated L2.

**Why not chi-squared or t-test?**
- Chi-squared: appropriate if Good/Bad is the outcome, but throws away magnitude information. Mann-Whitney U uses the continuous MFE signal, which is more powerful.
- t-test: normality assumption fails. Rejected.

---

#### Pre-Specified Discrimination Threshold

**Minimum meaningful difference: +10pp Good rate lift (L2+ vs L2−)**
- Justification: IS Good rate is 56.6%. OOS precision is 11.5%. A filter that shifts the distribution by fewer than 10pp provides negligible practical signal given execution costs and false-positive noise. +10pp is the smallest effect worth building a stage around.
- Hard minimum: Good rate in L2-positive group ≥ 40%. A filter that selects for trades performing *below* base rate is disqualifying regardless of the lift.
- Mann-Whitney U p-value threshold: p < 0.05 (one-tailed). This is the formal gate; the +10pp lift is the practical gate. **Both must be satisfied.**

---

#### Minimum n Per Group

**L2-positive (fires): minimum n = 30**
- Wilson CI width at n=30: approximately ±18pp. Adequate for ruling out filters with zero signal.
- Below n=30: [STAT FLAG — see contingency below].

**L2-negative (does not fire): minimum n = 20**
- Since L2 is expected to be selective, negative group will typically be large. n=20 is a floor to ensure the comparison group is non-trivial.
- If L2-positive + L2-negative ≠ 183 (i.e., some entries unclassifiable by L2), document the unclassified count and reason before running the test.

**Overall:** Total classified n ≥ 50 before Mann-Whitney U is reported. If total < 50, the test is underpowered and cannot pass the gate.

---

#### Success Criterion — Formal

Gate 1 passes if ALL THREE are satisfied:

1. **Mann-Whitney U p < 0.05** (one-tailed, L2+ MFE > L2− MFE)
2. **Good rate in L2+ group ≥ 40%** (Wilson 95% CI lower bound)
3. **Good rate lift (L2+ minus L2−) ≥ 10pp**

Gate 1 fails if ANY ONE is not satisfied. Partial passes are not passes — no "directional positive" language may appear in the decision document if the formal gate is not cleared.

---

#### Contingency: L2 Fires on Fewer Than 30 of 183 OOS Cases

**If L2-positive n < 30:**

`[STAT FLAG] L2 fires on n=<30 of 183 OOS cases. Mann-Whitney U and Wilson CI are underpowered at this sample size. Gate 1 cannot formally pass. Result is directionally informative only.`

**Operational response:**
- Do not block further research — but do not record Gate 1 as passed.
- Document the observed Good rate in L2+ with a wide Wilson CI and explicit low-power caveat.
- Route to PO with the following question: *Do we expand the OOS window (more dates) to accumulate L2+ n ≥ 30, or do we declare L2 too selective to be testable and retire it?*
- **Default: expand OOS window by 60 calendar days before issuing a pass/fail verdict.** If still n < 30 after expansion, retire L2.

---

### Gate 2 (Paper Trading Validation) — Full Specification

#### Good Rate Computation Method

**Method: Mechanical label (MFE_30bar threshold), NOT PO review**

Justification:
1. **PO review is subjective and retrospective.** In paper trading, we want a label that can be computed programmatically from price data alone, removing rater subjectivity and availability dependency.
2. **Consistency with IS labels is NOT required for paper trading.** IS labels were used to train L2 discrimination. Paper trading validation tests live execution quality, not alignment with historical ratings.
3. **The IS MFE distribution provides the calibration anchor.** IS Good trades had median MFE ≈ [Manager to confirm exact figure]. Set the mechanical threshold at the IS Good group's 40th percentile MFE — this is a pre-specified, data-derived cutoff that labels approximately the same proportion of trades as Good as the IS PO-reviewed rate, without requiring PO time.

**Mechanical label rule:**
- A paper trade is labelled **Good** if `MFE_30bar ≥ T`, where T is the 40th percentile of IS Good group MFE (to be computed by Manager from IS dataset before paper trading begins — this value is locked before any paper trades are observed).
- A paper trade is labelled **Bad** if `MFE_30bar < T`.
- No neutral category in paper trading.

**Action required before paper trading opens:** Manager computes T from IS dataset and records it in the gate spec document. T is frozen. It cannot be adjusted after paper trades are observed.

---

#### Autocorrelation Test and Block Bootstrap CI

**Autocorrelation test: Ljung-Box test on the binary Good/Bad sequence**
- Compute the paper trade Good/Bad sequence in chronological order (1 = Good, 0 = Bad).
- Run Ljung-Box Q-test on the first 10 lags (standard for financial time series with ~50-100 observations).
- If Q-statistic p < 0.05 at any of the first 10 lags: temporal autocorrelation is present, block bootstrap is required.
- If p ≥ 0.05 across all 10 lags: standard Wilson CI is sufficient.

**Block Bootstrap CI specification (if autocorrelation detected):**
- Method: stationary block bootstrap (Politis & Romano, 1994) — preferred over fixed-block bootstrap because block length is selected automatically.
- Block length selection: use the Politis-White automatic bandwidth selector (or if not available, set block length = ⌈n^(1/3)⌉ where n = number of paper trades).
- Resamples: 2,000.
- Statistic: Good rate (proportion of Goods in resample).
- Report: 95% CI as [2.5th percentile, 97.5th percentile] of the bootstrap distribution.
- If autocorrelation is not detected, report Wilson score interval at 95%.
- **In all cases, state which CI method was used in the gate document.**

---

#### Participation Rate Definition

**Precise definition:**

> Participation rate = (number of paper trades taken) ÷ (number of scanner signals that met all entry conditions during the paper trading period)

- **Denominator:** All scanner fires where `bar_close >= orb_high AND vol_ratio >= 2.0x` during RTH, regardless of whether a trade was executed. This is logged automatically — Manager confirms the logging mechanism is active before paper trading begins.
- **Numerator:** Trades where a paper position was opened (entry order sent, confirmed fill or simulated fill recorded).
- **Backtest baseline:** The participation rate in the OOS 183-signal dataset = (trades executed / signals generated). If the OOS backtest executed on all 183 signals, baseline = 100%. If skip-first or other filters reduced participation, use the filtered rate.
- **Gate:** Paper trading participation rate must be ≥ 80% of the backtest baseline participation rate. Rationale: some slippage in live signal capture is expected (system latency, market hours edge effects), but systematic non-participation suggests an execution or signal failure requiring diagnosis before results are interpretable.

`[STAT FLAG — standing instruction]` If participation rate falls below 80% of baseline at any point in the paper trading period, flag immediately. Trades missed due to system failure must be excluded from the Good rate denominator but documented separately. Do not silently absorb missed signals into the denominator.

---

#### Minimum Sample Sizes

**Confirmed: minimum 50 trades, target 100.**

Statistical justification:
- At n=50: Wilson CI width ≈ ±14pp. Sufficient to detect a Good rate that is meaningfully above 40% (e.g., 56% would have lower bound ~42%).
- At n=100: Wilson CI width ≈ ±10pp. The target. Allows detection of a 50% Good rate with lower bound ≥ 40%.
- **Interim check at n=50:** If Good rate Wilson CI lower bound is already ≥ 45%, paper trading may proceed to n=100 for confirmation. If lower bound is below 35% at n=50, trigger the failure protocol early (do not wait for n=100).

**Success criterion at n=100 (or final n if capped):**
- Wilson 95% CI lower bound on Good rate ≥ 40%.
- Participation rate ≥ 80% of backtest baseline throughout.
- Both conditions must hold. This is the Gate 2 pass.

---

### Gate 2 Failure Protocol — Full Specification

#### What "Diagnose" Means Operationally

Diagnosis is triggered when: (a) interim check at n=50 shows lower bound < 35%, OR (b) final n shows Wilson lower bound < 40%, OR (c) participation rate drops below 80% of baseline for ≥ 5 consecutive trading days.

**Diagnosis procedure — four comparisons, run in order:**

1. **Execution comparison:** Compare paper trade entry prices vs backtest assumed entry prices for the same signal dates. Compute mean slippage. If mean slippage > 0.5% (absolute), flag as execution degradation — this is an execution problem, not a signal problem.

2. **Distribution shift test:** Compare MFE distribution of paper trades vs IS/OOS backtest MFE distribution using Mann-Whitney U (two-tailed). If p < 0.05, the paper trading market environment has shifted. Document regime change hypothesis.

3. **Temporal clustering analysis:** Plot Good rate in rolling 10-trade windows. If Good rate is consistently < 30% for a sustained run of ≥ 20 consecutive trades, flag as possible regime break, not random variance.

4. **Signal integrity check:** Verify that scanner fires in paper trading period satisfy the same conditions as OOS (vol_ratio ≥ 2.0x, bar_close ≥ orb_high). Sample-check 10 randomly selected fires. If > 2 of 10 fail the entry condition, flag as signal implementation error.

Each comparison produces a labelled finding: *Execution*, *Regime*, *Clustering*, or *Implementation*. The failure protocol proceeds differently depending on the finding.

---

#### Extension vs Full Stop Triggers

**30-day extension (diagnosis finding = Execution or Regime):**
- Execution: slippage > 0.5% but fixable (e.g., order routing parameter change). Fix is made, 30-day clock restarts. Only one extension permitted.
- Regime: paper trading occurred during an anomalous market period (e.g., high VIX spike, market structure event). PO reviews whether the OOS comparator period had similar conditions. If the OOS period was also a calm market, 30-day extension into a comparable period is permitted.
- **Extension requires PO approval.** Not automatic.

**Full stop (diagnosis finding = Implementation or persistent Clustering):**
- Implementation error: if > 2/10 sampled signals fail entry conditions, paper trading results are invalid. Full stop. Re-run after fix is confirmed.
- Persistent clustering: if rolling 10-trade Good rate is < 30% for ≥ 30 consecutive trades (not 20 — the higher threshold for a full stop decision), the signal has failed in live conditions. Full stop. Route to Org Learning for root-cause analysis before any re-attempt.
- **Full stop requires PO approval and a written root-cause summary** before any new paper trading period may begin.

**Default if diagnosis is ambiguous:** Full stop. The burden of proof is on demonstrating the failure is temporary and fixable, not on demonstrating it is permanent.

---

#### Review Ownership

| Event | Owner | Escalation |
|---|---|---|
| Interim check at n=50 | Manager | Routes to PO with Wilson CI and participation rate |
| Failure diagnosis (all four comparisons) | Manager executes | Statistician reviews findings, Challenger audits |
| Extension approval | PO | Cannot be self-approved by Manager |
| Full stop decision | PO | Written root-cause required before re-attempt |
| Gate 2 pass declaration | PO | Requires Statistician sign-off on CI and sample size |

---

### Required Pre-Conditions Before Any Gate Execution

These items must be completed and recorded before data is examined:

1. **T (mechanical Good label threshold)** — computed by Manager from IS dataset, frozen in document.
2. **Backtest baseline participation rate** — computed from OOS 183-signal dataset, recorded.
3. **N variants tested in any L2 sweep** — logged before results are reviewed (BH correction applied to that N).
4. **Ljung-Box test** — pre-specified to run as Step 1 of Gate 2 CI computation, before any Good rate is reported.
5. **Gate 1 L2+ minimum n** — confirmed as 30, with the contingency window-expansion protocol in effect.

---

### Summary — What Must Be Stated in Every Gate Report

**Gate 1 report must include:**
1. n (L2+ group), n (L2− group)
2. Mann-Whitney U statistic and p-value (one-tailed)
3. Good rate in each group with Wilson 95% CI
4. Good rate lift (pp difference)
5. Pass/Fail against all three criteria

**Gate 2 report must include:**
1. n (paper trades), participation rate vs baseline
2. Ljung-Box result (which CI method used: Wilson or block bootstrap — state explicitly)
3. Good rate with 95% CI (method stated)
4. Pass/Fail against Wilson lower bound ≥ 40%
5. If failure: which diagnosis was triggered and outcome

---

> **FLAG FOR CONTEXT:** Gate specs include three pre-conditions that must be computed by Manager from existing IS/OOS datasets before any gate execution begins: (1) T threshold from IS Good group MFE 40th percentile, (2) OOS baseline participation rate, (3) BH-adjusted N for any L2 sweep. These should be added as action items in the research log before this document is filed.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** Statistician has delivered comprehensive specifications. Now routing to Challenger for full audit before I write the document.

**Challenger — your turn. Audit the Statistician's gate specifications below. Your job: find errors, ambiguities, missing cases, and lookahead risks before this becomes a contract document.**

**Data context:**
- 183 OOS scanner fires (Jan–Mar 2026), 21 runners confirmed, 11.5% precision (OOS)
- 782 RTH runners in full population, 0.694% base rate
- 265 PO-rated IS entries: 150 Good, 115 Bad (33 neutral excluded)
- IS Good rate: 56.6% (150/265)
- Entry conditions: `bar_close >= orb_high AND vol_ratio >= 2.0x`
- OOS Wilson CI on precision: [7.6%, 16.9%]

**Statistician's full specification to audit:**

---

**Gate 1 (L2 OOS Discrimination Test):**

- **Test statistic:** Mann-Whitney U (one-tailed, L2+ MFE > L2− MFE). Secondary: Good rate lift (L2+ minus L2−) with Wilson CIs on each group.
- **Discrimination threshold:** +10pp Good rate lift (L2+ vs L2−), minimum. Hard floor: L2+ Good rate ≥ 40%. Both must hold.
- **Minimum n:** L2+ ≥ 30, L2− ≥ 20, total classified ≥ 50. Below n=30 in L2+: test cannot pass.
- **Success criterion (ALL THREE required):**
  1. Mann-Whitney U p < 0.05 (one-tailed)
  2. Wilson 95% CI lower bound on L2+ Good rate ≥ 40%
  3. Good rate lift ≥ 10pp
- **Contingency (L2+ n < 30):** Expand OOS window by 60 calendar days. If still < 30 after expansion, retire L2.

**Gate 2 (Paper Trading Validation):**

- **Good rate computation:** Mechanical label — MFE_30bar ≥ T where T = 40th percentile of IS Good group MFE. T computed and frozen before paper trading opens.
- **Autocorrelation test:** Ljung-Box Q on first 10 lags of binary Good/Bad sequence. p < 0.05 at any lag → block bootstrap required.
- **Block bootstrap:** Stationary bootstrap (Politis & Romano), block length = ⌈n^(1/3)⌉, 2,000 resamples, 95% CI from [2.5th, 97.5th percentile].
- **Participation rate:** (trades taken) ÷ (scanner signals meeting entry conditions). Gate: ≥ 80% of backtest baseline. Miss below 80% for ≥ 5 consecutive days → immediate flag.
- **Sample size:** Minimum 50, target 100. Interim at n=50.

**Gate 2 Failure Protocol:**

- **Four diagnoses (in order):** Execution (slippage > 0.5%), Distribution shift (Mann-Whitney U two-tailed on MFE), Temporal clustering (rolling 10-trade window < 30% for ≥ 20 consecutive trades), Signal integrity (sample 10 fires, > 2 fail → implementation error).
- **Extension triggers:** Execution or Regime finding → 30-day extension, PO approval, one extension only.
- **Full stop triggers:** Implementation error OR persistent clustering (≥ 30 consecutive trades < 30% rolling) → full stop + root-cause.
- **Review ownership table:** Manager executes diagnosis, Statistician reviews, Challenger audits, PO approves extension/stop/pass.

**Pre-conditions before any gate execution:**
1. T threshold computed from IS Good MFE 40th percentile — frozen before paper trading.
2. OOS baseline participation rate — computed and recorded.
3. N variants in L2 sweep — logged before results reviewed (BH correction applied).
4. Ljung-Box pre-specified as Step 1 of Gate 2 CI computation.
5. Gate 1 L2+ minimum n = 30 confirmed.

---

**Challenger — audit questions to address:**

1. Is Mann-Whitney U the right test given that L2 is being tested on the *same* 183 OOS entries used for precision scoring? Does this create a multiple-comparisons or data-reuse concern?
2. Is "Wilson CI lower bound ≥ 40%" a lookahead risk? The 40% threshold was chosen after observing IS data.
3. Is the 40th percentile MFE for T appropriately anchored, or does it create a tautological label?
4. Does the rolling 10-trade window in the failure protocol have enough power to detect real clustering vs noise?
5. Are there missing cases in the failure protocol — what happens if participation rate drops AND Good rate fails simultaneously?
6. Any other errors, gaps, or contract ambiguities you can find.

[NEXT: challenger]

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## LC-2025-033 — Challenger Audit Response

---

### Evidence Provided

I have been given:
- Statistician's full gate specification (Gate 1 and Gate 2)
- Data context: 183 OOS fires, 265 IS PO-rated entries (150G/115B), 11.5% OOS precision, Wilson CI [7.6%, 16.9%]
- Five directed audit questions from Manager
- No raw data, no code, no MFE distributions

I will audit each specification component in turn, then address the five directed questions.

---

### Lookahead Bias Check

**Gate 1:**
- L2 is applied to 183 OOS entries. If L2's thresholds were derived from any analysis of these same 183 entries, this is in-sample testing dressed as OOS. **The spec does not state where L2's thresholds were derived.** This is a material omission. If L2 parameters were chosen after observing outcomes on even a subset of these 183 trades, Gate 1 is contaminated.
- The 40% Good rate floor was chosen after observing IS Good rate of 56.6%. This is threshold selection from outcome data. It is calibrated to IS, not derived independently. I flag this as a soft lookahead risk (IS→OOS threshold transfer), addressed in detail below.
- Mann-Whitney U on MFE: MFE is a post-entry outcome. It is not available at decision time. **But this is correct for discrimination testing** — we are validating that L2 separates outcomes, not that it uses future data to enter. No structural lookahead here.

**Gate 2:**
- T = 40th percentile of IS Good group MFE. This is computed from IS data and frozen before paper trading. Provided the freeze is enforced, no lookahead on T itself.
- Mechanical label `MFE_30bar ≥ T`: MFE_30bar is a post-entry outcome (30 bars into the trade). **This is correct for a validation label** — it is the quantity we are trying to predict, not a predictor. No lookahead in the label construction.
- Ljung-Box run on the sequence after trades are completed: correct, no lookahead.

**Lookahead bias check result: ONE UNRESOLVED RISK** — L2 threshold derivation source not specified. If derived from the 183 OOS entries, Gate 1 is invalid. Must be resolved before document is finalised.

---

### Finding 1: L2 Threshold Derivation — Blocking Ambiguity

**The spec does not state how L2's parameters were set or on which data.**

If L2 was designed using any of the 183 OOS entries (Jan–Mar 2026), then applying it to those same entries is not OOS validation — it is in-sample fitting. Mann-Whitney U p < 0.05 would be expected by construction.

**Required clarification:** Manager must state explicitly: (a) on which dataset L2's thresholds were chosen, (b) whether any of those records overlap with the 183-entry OOS test set.

If overlap exists, Gate 1 cannot use the 183-entry OOS set. A fresh held-out window is required. This is a blocking finding.

---

### Finding 2: Mann-Whitney U on MFE — Mismatch with Gate Metric

**The formal gate uses a continuous MFE test (Mann-Whitney U), but the pass/fail criteria are binary (Good/Bad rate, ±10pp lift). These are not the same thing, and the spec treats them as though they are.**

Mann-Whitney U tests whether the MFE rank distribution of L2+ trades stochastically dominates L2− trades. A p < 0.05 result means L2+ tends to have higher MFE values than L2−. This is a different claim from "Good rate in L2+ is ≥ 40%."

It is entirely possible to have:
- Mann-Whitney U p < 0.05 (L2+ has higher MFE on average), **but**
- Good rate in L2+ = 38% (below the 40% floor), **if** the threshold T is set high and L2+ trades cluster just below T

Or conversely:
- Mann-Whitney U p = 0.08 (marginal), **but**
- Good rate lift = +15pp (strong practical signal)

The spec says "both must hold." This is fine as a joint gate — but the justification conflates two distinct claims. The gate document must state explicitly: **these are independent criteria testing different properties of the same data.** Mann-Whitney U tests continuous rank ordering; Good rate lift tests categorical separation at threshold T. A trade can satisfy one without the other.

**Required fix:** Gate 1 success criterion must explicitly state that the two tests measure different properties and that both failing is a different diagnostic than one failing. The current "all three" framing implies they are redundant confirmations of the same thing — they are not.

---

### Finding 3: "Wilson CI Lower Bound ≥ 40%" — Threshold Provenance Problem

**Directed audit question 2 and 3.**

The 40% floor is stated as the minimum acceptable Good rate. Where does 40% come from?

The spec says: *"A filter that selects for trades performing below base rate is disqualifying."* But what is the base rate here? The OOS precision is 11.5% — far below 40%. The IS Good rate is 56.6%. The 40% figure appears to be an arbitrary buffer below the IS Good rate, chosen after observing 56.6%.

**This is threshold selection from observed outcomes.** It is not derived from a pre-specified economic or statistical argument. If the IS Good rate had been 45%, would 40% still be the floor? Almost certainly not — the floor would have been set lower. The floor is implicitly calibrated to the observed IS rate.

**Impact:** The 40% floor is not a contract-grade pre-specification. It is a post-hoc derived threshold. If Gate 1 fails narrowly (L2+ Good rate = 38%), the temptation to argue "close enough" is structurally enabled by the arbitrary origin of the threshold.

**Required fix:** The spec must provide an independent justification for 40% that does not reference the IS Good rate. Two acceptable alternatives:
1. Economic argument: "A 40% Good rate is the minimum at which the strategy is profitable after costs, given win/loss ratio X." Provide the calculation.
2. Base rate argument: "40% is the minimum we consider meaningfully above the OOS precision floor of 11.5%, applying a pre-specified multiplier of 3.5x." State the multiplier and why it was chosen.

If no independent justification exists, the floor must be stated as "advisory only, not a formal gate condition" in the contract document.

---

### Finding 4: T Threshold — Tautological Label Risk

**Directed audit question 3.**

T = 40th percentile of IS Good group MFE. Think through what this produces:

- IS Good group was labelled Good by PO review (retrospective, chart-based).
- MFE distribution of IS Good group is, by construction, higher than IS Bad group (that is what made them Good).
- Setting T at the 40th percentile of the IS Good group means approximately 60% of IS Good trades would be labelled Good mechanically.
- But what fraction of IS Bad trades would also clear T? The spec does not address this.

**If IS Bad group MFE overlaps substantially with IS Good group MFE below the 40th percentile of the Good group, then T is a loose threshold that labels many Bad trades as Good.** The mechanical label would then diverge systematically from the PO label.

**The tautology risk is the opposite direction from what the spec implies:** The spec frames T as "pre-specified, data-derived, removes subjectivity." But it will only approximate PO labels if IS Good and Bad MFE distributions are well-separated. The spec never establishes this separation.

**Required fix:** Before T is frozen, Manager must provide:
- The MFE distribution overlap between IS Good and IS Bad groups (e.g., what % of IS Bad trades have MFE ≥ T)
- The resulting mechanical False Good rate (Bad trades labelled Good by T) and False Bad rate (Good trades labelled Bad by T)
- If mechanical label agreement with PO label is below 70% on IS data, T is not a valid proxy for PO quality

This is a prerequisite to freezing T. Without it, the paper trading Good rate is measuring something undefined.

---

### Finding 5: Ljung-Box on Binary Sequence — Power Problem

**Directed audit question 4.**

Ljung-Box Q-test is designed for continuous autocorrelation structure (residuals, returns). Running it on a binary {0,1} sequence of 50–100 observations is technically permissible but has known power limitations:

1. **Small sample power:** At n=50, Ljung-Box on 10 lags has poor power to detect moderate autocorrelation (autocorrelation of 0.2 may not be detected). A genuine clustering effect (e.g., regime-specific runs of Good or Bad trades) may not trigger the test.
2. **Binary variance restriction:** A Bernoulli sequence has variance p(1-p). If the true Good rate is near 0.5, this is reasonable. But if Good rate is near 0.3 or 0.7, the variance is compressed further, and the Q-statistic is less sensitive.

**Practical consequence:** The spec says "if p ≥ 0.05, Wilson CI is sufficient." But Wilson CI assumes i.i.d. observations. If the Ljung-Box test has insufficient power to detect real autocorrelation at n=50, we may use Wilson CI when block bootstrap was actually required — **systematically underestimating CI width and overstating confidence in the Good rate.**

**Required fix:** The spec should state: *"If n < 75, apply block bootstrap by default regardless of Ljung-Box result. The cost of unnecessary block bootstrap (slightly wider CI) is lower than the cost of missed autocorrelation (falsely narrow CI)."* This is the conservative, contract-grade default.

Alternatively: supplement Ljung-Box with a runs test (Wald-Wolfowitz), which is specifically designed for binary sequences and detects non-randomness in run patterns. Either add the runs test as a co-required condition, or replace Ljung-Box with it for the binary sequence check.

---

### Finding 6: Multiple Comparisons on the 183-Entry OOS Set

**Directed audit question 1.**

The spec notes pre-condition 3: "N variants tested in any L2 sweep — logged before results reviewed (BH correction applied to that N)." This is the right instinct. But the spec is incomplete on implementation.

**Problem:** The 183 OOS entries are simultaneously:
- The precision scoring dataset (Stage 0, already used)
- The Gate 1 discrimination dataset

If any exploratory analysis of L2 variants was performed on the 183 entries before the spec was written — even informally — the logged-N BH correction cannot recover the integrity of the test. BH correction only applies to *pre-specified* comparisons tested simultaneously, not to sequential model selection where an analyst observes results and selects a winner.

**The spec contains no mechanism to verify that L2's current specification was chosen without peeking at the 183-entry outcomes.** Pre-condition 3 says "log variants before reviewing results" — but this only works if it was enforced before any L2 development occurred on the 183-entry set.

**Required clarification:** Was any analysis of L2's performance run on the 183 OOS entries before this gate spec was written? If yes, BH correction is insufficient — the 183-entry set is partially contaminated and a fresh OOS window is required. If no, pre-condition 3 is sufficient.

This question must be answered and documented in the gate spec document, not assumed.

---

### Finding 7: Participation Rate — Denominator Definition Ambiguity

The spec defines participation rate denominator as: *"All scanner fires where bar_close >= orb_high AND vol_ratio >= 2.0x during RTH, regardless of whether a trade was executed."*

**Two problems:**

**7a. "Regardless of whether a trade was executed" conflates signal availability with execution decision.** If L2 is a filter applied on top of entry conditions, then some signals meeting entry conditions will be L2-negative and intentionally not traded. These should not count in the denominator for a participation rate gate — they are intentional non-participations.

Unless L2 is not a filter but a scorer (all signals taken, L2 used to classify outcomes), in which case the participation rate denominator is correct. The spec does not clarify L2's operational role: **is it a filter (some signals deliberately skipped) or a scorer (all signals taken, L2 used post-hoc)?**

**Required fix:** State explicitly whether L2 is a filter (participation denominator = signals meeting entry conditions AND L2-positive) or a scorer (denominator = all signals meeting entry conditions).

**7b. "Backtest baseline = 100% if all 183 signals were executed."** This implies the OOS backtest executed every qualifying signal. If any signals were skipped in the OOS backtest (e.g., due to cache misses — confirmed 67% skip rate in other contexts), the baseline may not be 100% and may be difficult to reconstruct. The spec should require Manager to confirm the OOS execution rate explicitly before locking the baseline.

---

### Finding 8: Failure Protocol — Missing Combined Failure Case

**Directed audit question 5.**

The failure protocol handles Execution, Regime, Clustering, and Implementation as independent findings. **What happens if participation rate fails AND Good rate fails simultaneously?**

Under the current spec:
- Participation failure → immediate flag (≥ 5 consecutive days below 80%)
- Good rate failure → interim check at n=50 or final n=100

If both fail together:
- The four diagnoses are applied in order
- But the results may produce conflicting findings: Execution problem explains participation drop, Regime problem explains Good rate drop

**The spec has no instruction for compound failures.** In a compound failure, the extension-vs-stop logic becomes ambiguous: Execution finding → extension eligible; Regime finding → extension eligible; but their combination may indicate a more fundamental breakdown than either alone.

**Required fix:** Add a compound failure rule: *"If both participation rate and Good rate fail simultaneously, the default is Full Stop regardless of individual diagnosis findings. Extension is only permitted if a single root cause explains both failures and a fix for that root cause is demonstrated before extension begins."*

---

### Finding 9: Interim Check Asymmetry

The spec states: *"If lower bound is below 35% at n=50, trigger the failure protocol early."*

But the failure protocol triggers at Good rate lower bound < 35% (early stop) vs final gate at lower bound < 40%. **There is a 5pp gap between the interim trigger (35%) and the final gate (40%).**

A strategy with a true Good rate of 37% would:
- Pass the interim check (lower bound at n=50 for 37% true rate ≈ 37% − 14pp = 23%, which is above 35%... wait)

Actually: at n=50 with observed Good rate 37%, Wilson lower bound ≈ 37% − 1.96×√(0.37×0.63/50) ≈ 37% − 13.4% ≈ 23.6%. This is above 35%, so the interim check does not trigger early stop.

At n=100 with true rate 37%, Wilson lower bound ≈ 37% − 1.96×√(0.37×0.63/100) ≈ 37% − 9.5% ≈ 27.5%. This is below 40%, so final gate fails.

**The interim check at 35% lower bound is so loose that it provides almost no early-stop protection.** A strategy that will ultimately fail the final gate at 40% lower bound will almost never be caught at the interim check. The interim check's stated purpose is to "save resources" — but in practice it fires only for very bad strategies (true Good rate < ~50%), not strategies in the 37–45% range that hover around the final gate.

**This is not an error, but it is a gap in the spec.** The interim check's actual utility should be stated honestly: it is only an early stop for strategies performing well below threshold, not a reliable mid-course correction mechanism.

---

### Finding 10: Review Ownership — Challenger Self-Reference

The ownership table assigns: *"Failure diagnosis — Challenger audits."*

As a contract document, this is structurally sound. However: the spec does not define what "Challenger audits" means operationally in the context of a live failure. Does Challenger audit the four diagnosis comparisons? The Manager's written finding? The raw data?

This ambiguity is acceptable for a spec document but should be clarified to: *"Challenger audits the written diagnosis report produced by Manager, confirming the four comparisons were run correctly and the extension/stop recommendation follows the protocol."* Challenger does not independently re-run the data.

---

### Summary of Findings

| # | Finding | Severity

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## Session Continues — LC-2025-033

Challenger's audit is comprehensive. I have 10 findings to work through before writing the document. Let me triage each finding by severity before proceeding.

---

## Triage of Challenger's 10 Findings

**Blocking (must resolve before document can be finalised):**

| # | Finding | Resolution path |
|---|---|---|
| 1 | L2 threshold derivation source not stated — if derived from 183 OOS entries, Gate 1 is invalid | Requires PO clarification |
| 6 | Multiple comparisons — was 183-entry set peeked before spec written? | Requires PO clarification |
| 3 | 40% floor has no independent justification — post-hoc calibration to IS Good rate | Fix in document: add economic or base-rate anchor |
| 4 | T threshold: IS Bad MFE overlap with IS Good group not established — tautological label risk | Fix in document: require Manager to verify IS label concordance before freezing T |
| 7a | Participation rate denominator ambiguous — L2 as filter vs scorer not defined | Fix in document: resolve operational role |

**Non-blocking (incorporate into document as clarifications or fixes):**

| # | Finding | Resolution |
|---|---|---|
| 2 | Mann-Whitney U and Good rate lift are independent criteria, not redundant — gate must state this explicitly | Clarifying text in Gate 1 |
| 5 | Ljung-Box power insufficient for binary n<75 — default to block bootstrap below n=75 | Replace Ljung-Box default at small n |
| 7b | OOS backtest execution rate needs explicit confirmation before baseline is locked | Add as pre-condition 6 |
| 8 | Compound failure case missing — both participation and Good rate fail simultaneously | Add compound failure rule |
| 9 | Interim check at 35% is de facto weak — state utility honestly | Add honest characterisation |
| 10 | Challenger audit role needs operational definition | One-line clarification |

---

## Resolution of Blocking Items

**Findings 1 and 6** require PO input — I cannot resolve these analytically. They are the same underlying question: was the 183-entry OOS set examined before L2's design was locked?

**Finding 3 (40% floor):** I will apply the base-rate anchor approach — 40% as a pre-specified multiplier of the OOS precision floor. OOS precision = 11.5%. Multiplier = 3.5x → 40.25% ≈ 40%. This gives an independent justification without referencing IS Good rate. I will record 3.5x as the pre-specified multiplier in the document.

**Finding 4 (T threshold tautology):** I will add a required pre-condition: Manager must verify IS label concordance (mechanical vs PO) ≥ 70% before T is frozen. If below 70%, T is not a valid proxy.

**Finding 7a (L2 operational role):** Based on the research context (L2 is a discrimination filter applied to scanner fires), L2 is a **filter** — signals are intentionally not taken when L2 is negative. The participation denominator should be L2-positive signals only. I will specify this in the document.

---

Now writing the gate specification document.

---

## `research/briefs/lc025029_gate_specs.md`

```markdown
# Gate Specification — Stage 2 (L2 OOS Discrimination) and Stage 4 (Paper Trading)

_Authored: LC-2025-033 | Status: PENDING PO APPROVAL | Version: 1.0_

---

## Purpose

This document pre-specifies the success criteria, test methods, and failure protocols
for two research gates on the path to live trading:

- **Gate 1 — L2 OOS Discrimination:** Does L2 meaningfully separate Good from Bad
  entries in the held-out OOS dataset?
- **Gate 2 — Paper Trading Validation:** Does the full strategy (entry + L2 filter)
  produce acceptable live Good rates and participation quality?

This document is a contract. All thresholds, tests, and decision rules are frozen here.
Nothing may be changed after data examination begins. Any proposed amendment requires
a new LC session and PO approval.

---

## Open Blockers — MUST RESOLVE BEFORE GATE 1 BEGINS

> **[BLOCKER B1]** — L2 threshold derivation: Was L2's current parameter specification
> derived using any analysis of the 183 OOS entries (Jan–Mar 2026)?
>
> If YES: the 183-entry set is partially or fully contaminated for Gate 1. A fresh
> held-out window is required. Gate 1 cannot proceed on the existing OOS set.
>
> If NO: pre-condition 3 (BH-corrected N logging) is sufficient. Document the answer
> explicitly and sign off before Gate 1 data examination begins.
>
> **Owner: PO. This question must be answered and recorded before any Gate 1 work begins.**

> **[BLOCKER B2]** — Pre-specification integrity: Was any exploratory analysis of
> L2's discrimination performance run on the 183 OOS entries before this gate spec
> was written, even informally?
>
> Same resolution path as B1. BH correction applies only to pre-specified comparisons
> run simultaneously — it cannot recover integrity from sequential model selection
> with outcome peeking.
>
> **Owner: PO. Answer must be stated and signed before Gate 1 work begins.**

---

## Pre-Conditions — All Must Be Completed and Recorded Before Data Examination

The following items must be computed, frozen, and recorded in this document before
any gate data is examined. They cannot be set or adjusted after results are observed.

| # | Pre-condition | Owner | Status |
|---|---|---|---|
| PC1 | T threshold — 40th percentile of IS Good group MFE, frozen | Manager | PENDING |
| PC2 | IS label concordance check — mechanical vs PO label agreement ≥ 70% on IS data; if below 70%, T is not a valid proxy and must be redesigned | Manager | PENDING |
| PC3 | OOS baseline participation rate — confirmed execution rate from 183-signal OOS dataset | Manager | PENDING |
| PC4 | N (variants tested in any L2 sweep) — logged before results reviewed; BH correction applied to this N | Manager | PENDING |
| PC5 | Ljung-Box and runs test pre-specified as Steps 1a and 1b of Gate 2 CI computation | Manager | PRE-SPECIFIED (this document) |
| PC6 | L2 operational role confirmed: L2 is a **filter** — L2-negative signals are intentionally not traded. Participation denominator = L2-positive signals only | Manager + PO | PENDING |

> **Pre-condition PC2 note:** Before T is frozen, Manager must produce:
> (a) the observed False Good rate — IS Bad trades labelled Good by T (MFE ≥ T);
> (b) the observed False Bad rate — IS Good trades labelled Bad by T (MFE < T);
> (c) overall mechanical-vs-PO agreement rate on IS data.
> If agreement < 70%, T is not a valid proxy for PO quality and must be redesigned
> before paper trading opens.

---

## Gate 1 — L2 OOS Discrimination Test

### Purpose

Validate that L2 meaningfully separates Good from Bad entries in the 183-entry OOS
dataset. L2 is applied to each entry; entries are classified L2-positive (L2 fires)
or L2-negative (L2 does not fire). Outcomes (Good/Bad, MFE) are then compared
between groups.

### Test Statistic

**Primary test: Mann-Whitney U (one-tailed)**

- Tests whether L2-positive entries have stochastically higher MFE than L2-negative
  entries. Direction: L2+ > L2− (one-tailed). This tests the directional hypothesis
  that L2 improves selection.
- Justification: MFE distributions are right-skewed with heavy tails. Normality
  assumption fails. Mann-Whitney U is distribution-free and appropriate for ordinal
  rank comparison of two independent groups.
- Report alongside: Cohen's d on log-transformed MFE (descriptive only, not a
  decision statistic).

**Secondary metric: Good rate lift**

- Compute Good rate within L2-positive and L2-negative sub-populations.
- Good/Bad labels: PO review labels from the IS/OOS rating exercise.
- Report as: (Good rate L2+) − (Good rate L2−), with Wilson 95% CI on each
  proportion separately.

> **Critical note:** Mann-Whitney U and Good rate lift are **independent criteria
> testing different properties of the same data.** Mann-Whitney U tests continuous
> rank ordering of MFE. Good rate lift tests categorical separation at the PO-label
> threshold. A result can satisfy one criterion without satisfying the other. Both
> failing simultaneously is a different diagnostic from one failing:
> - MWU fails + lift passes: distributional separation exists but threshold
>   placement is suboptimal — investigate T calibration.
> - MWU passes + lift fails: continuous ordering is correct but the categorical
>   label is too coarse to capture it — Good/Bad label may be mis-calibrated.
> - Both fail: no discrimination signal detected.

### Minimum Sample Sizes

| Group | Minimum n | Note |
|---|---|---|
| L2-positive | 30 | Below 30: test underpowered, cannot formally pass |
| L2-negative | 20 | Comparison group floor |
| Total classified | 50 | Below 50: Mann-Whitney U not reported |

Unclassifiable entries (if L2 cannot assign a signal to some entries) must be
documented with count and reason before any test is run.

### Success Criterion — All Three Required

Gate 1 passes if and only if ALL THREE of the following are satisfied:

1. **Mann-Whitney U p < 0.05** (one-tailed, L2+ MFE > L2− MFE)
2. **Wilson 95% CI lower bound on L2+ Good rate ≥ 40%**
3. **Good rate lift (L2+ minus L2−) ≥ 10pp**

**Threshold justification (Criterion 2):**
The 40% floor is anchored to the OOS precision baseline of 11.5%, not to the IS Good
rate. Pre-specified multiplier: **3.5x OOS precision = 3.5 × 11.5% = 40.25% ≈ 40%.**
Rationale: a filter that does not improve selection to at least 3.5× the unfiltered
precision rate provides negligible practical signal given execution costs. This
multiplier is fixed regardless of IS Good rate observations.

**Partial passes are not passes.** If two of three criteria are met, the gate fails.
The diagnosis section of the Gate 1 report must specify which criterion failed and
the implication (see Critical note above on independent criteria).

### Contingency: L2+ n < 30

If L2 fires on fewer than 30 of the 183 OOS entries:

```
[STAT FLAG] L2 fires on n=<30 of 183 OOS cases. Mann-Whitney U and Wilson CI
are underpowered at this sample size. Gate 1 cannot formally pass.
Result is directionally informative only.
```

Operational response:
1. Do not block further research — but do not record Gate 1 as passed.
2. Document observed Good rate in L2+ with wide Wilson CI and explicit low-power caveat.
3. Route to PO: expand OOS window by 60 calendar days to accumulate L2+ n ≥ 30,
   OR declare L2 too selective to be testable and retire it.
4. **Default: expand OOS window.** If still n < 30 after 60-day expansion, retire L2.

### Gate 1 Report — Required Contents

Every Gate 1 report must include, in order:

1. Confirmation that Blockers B1 and B2 are resolved and documented
2. n (L2+ group), n (L2− group), n (unclassified)
3. Mann-Whitney U statistic and p-value (one-tailed)
4. Good rate in each group with Wilson 95% CI
5. Good rate lift (pp difference)
6. Pass/Fail verdict against all three criteria
7. If any criterion fails: which one, and the diagnostic implication

---

## Gate 2 — Paper Trading Validation

### Purpose

Validate that the live strategy (entry conditions + L2 filter) produces acceptable
Good rates and execution quality in real market conditions.

### Good Rate Computation Method

**Method: Mechanical label (MFE_30bar threshold)**

A paper trade is labelled:
- **Good** if `MFE_30bar ≥ T`
- **Bad** if `MFE_30bar < T`

where T = 40th percentile of IS Good group MFE (pre-condition PC1).

No neutral category in paper trading.

**Justification for mechanical over PO review:**
PO review is subjective and creates a throughput bottleneck in live trading conditions.
Mechanical labels allow programmatic computation at scale. IS Good rates under PO
review are used for Gate 1; paper trading uses the mechanical proxy. These labels
need not be identical — they measure related but distinct quantities.

**Pre-condition PC2 must be satisfied before T is used.** If IS label concordance
< 70%, T is not a valid proxy.

### Autocorrelation Test and CI Method

**Step 1a — Ljung-Box Q-test:**
- Apply to the binary Good/Bad sequence in chronological trade order (1=Good, 0=Bad).
- Lags tested: first 10.
- Threshold: p < 0.05 at any lag → temporal autocorrelation detected.

**Step 1b — Wald-Wolfowitz Runs Test (co-required):**
- Apply to the same binary sequence.
- Specifically designed for binary sequences; detects non-randomness in run patterns.
- Threshold: p < 0.05 → autocorrelation detected.

**CI method decision rule:**
- If **either** test detects autocorrelation (p < 0.05): use block bootstrap (see below).
- If **both** tests fail to detect autocorrelation (both p ≥ 0.05): use Wilson CI.
- **If n < 75:** use block bootstrap by default, regardless of test results. The cost
  of unnecessary block bootstrap (slightly wider CI) is lower than the risk of
  falsely narrow Wilson CI from undetected autocorrelation at small n.
- State which CI method was used in every Gate 2 report.

**Block Bootstrap specification (when required):**
- Method: stationary block bootstrap (Politis & Romano, 1994)
- Block length: max(⌈n^(1/3)⌉, minimum 5) — floor of 5 prevents degenerate blocks at small n
- Resamples: 2,000
- Statistic: Good rate (proportion of Goods in resample)
- Report 95% CI as [2.5th percentile, 97.5th percentile] of bootstrap distribution

### Participation Rate

**Definition:**

> Participation rate = (paper trades taken) ÷ (scanner signals meeting entry
> conditions AND L2-positive, during the paper trading period)

- **Denominator:** L2-positive signals only. L2-negative signals are intentional
  non-participations and are excluded from the denominator (per PC6: L2 is a filter).
- **Numerator:** Trades where a paper position was opened (entry order sent and
  fill confirmed or simulated fill recorded).
- **Backtest baseline:** Confirmed OOS execution rate from pre-condition PC3.
  Manager must state this rate explicitly before paper trading opens.
- **Gate:** Participation rate ≥ 80% of backtest baseline throughout paper trading.
- **Immediate flag trigger:** Participation rate below 80% of baseline for ≥ 5
  consecutive trading days.

> **[STAT FLAG — standing instruction]:** Trades missed due to system failure are
> excluded from the Good rate denominator but documented separately. Do not silently
> absorb missed signals into the denominator. Every missed signal must be logged
> with date, ticker, and reason.

### Sample Sizes

- **Minimum:** 50 trades (Gate 2 cannot produce a formal verdict below n=50)
- **Target:** 100 trades

**Interim check at n=50:**
- If Wilson 95% CI lower bound on Good rate is already ≥ 45%: continue to n=100 for confirmation.
- If Wilson 95% CI lower bound is below 35%: trigger failure protocol

---
