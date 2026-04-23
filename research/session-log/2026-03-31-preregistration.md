# Session: preregistration
_Date: 2026-03-31 16:24 UTC | Agent: manager | Model: claude-sonnet-4-6_

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

Question: Step 3: Pre-Registration Document — Challenger + Statistician Sign-Off

PO INSTRUCTION: Skip 3 Amigos. Challenger + Statistician ONLY. Short session — sign off or flag issues.

## PRE-REGISTRATION DOCUMENT (PO-specified, review for sign-off)

### 1. Entry Signal Concept (LOCKED)
'First new high after pullback':
- Wait for pullback from opening print
- Enter when bar_high > max(bar_high[570:574]) (ORB high) AFTER pullback
- Entry price: bar_open of bar immediately following signal bar
- If no pullback before new high: signal does not fire (straight runners excluded)

### 2. Parameter Sweep (pre-specified)
| Parameter | Values |
|---|---|
| Pullback depth | 1%, 2%, 3%, 5% below opening print |
| Timeout | 10:00, 10:30, 11:00 ET |
12 combinations. Design set only. BH correction. Best selected by S1. Applied to OOS — one shot.

### 3. Comparison Baseline
Signal entry vs static 09:35 entry (bar_open[575]) on SAME trades. Same exits, same costs.

### 4. Success Criteria (entry quality, exit-independent)
S1: Mean MAE from signal entry at least 3pp less negative than 09:35
S2: Hard stop (-10%) rate at least 15pp lower than from 09:35
S3: Mean MFE from signal entry no more than 5pp lower than from 09:35
All three on design set. OOS: same direction, magnitude may differ.

### 5. Secondary (informational only)
Mean PnL net, Good rate, signal fire rate.

### 6. Population
Design: May-Dec 2025 L2-qualifying trades. OOS: Jan-Mar 2026. Fixed.

### 7. What can/cannot change
Can change: which combo is selected, secondary interpretation
Cannot change: signal concept, criteria, thresholds, OOS population

## FOR CHALLENGER:
1. Is signal concept non-lookahead? Observable bar-by-bar?
2. Were parameter ranges specified before data was examined?
3. Do success criteria measure entry quality independently of exit?
4. Is design/OOS split clean?

## FOR STATISTICIAN:
1. Sample size per combination — adequate to detect 3pp MAE improvement?
2. BH correction for 12 combinations — appropriate?
3. If underpowered: state explicitly
4. CI width on each criterion at expected n per combination

[NEXT: challenger]

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** ## Session Open — LC-2025-041

**Session ID:** LC-2025-041
**Question:** Pre-Registration Document Sign-Off — Challenger + Statistician review
**Time-box:** Short session — sign-off or flag issues only
**Agents needed:** Challenger + Statistician (Optimist/Execution Realist/Scout not required)
**Expected outcome:** Signed-off pre-registration document, or explicit list of blocking issues requiring PO resolution before execution

**Scope:**
- Review the 7-element pre-registration document for methodological soundness
- Challenger: 4 specific questions (lookahead, pre-specification, criteria independence, split cleanliness)
- Statistician: 4 specific questions (sample size, BH correction, power, CI width)
- Both agents must explicitly state PASS or FLAG on each question
- No strategy recommendations, no new hypotheses — sign-off only

**Scope boundaries:**
- NOT in scope: changing the signal concept, criteria, thresholds, or OOS population (locked by PO)
- NOT in scope: discussing alternative signals or exit strategies

---

Routing to Challenger first with full data context package.

[NEXT: challenger]

---

**Challenger — your turn. Session LC-2025-041.**

**Task:** Review the Pre-Registration Document below. Answer the 4 specific questions with explicit PASS or FLAG verdict on each. State any blocking issues clearly.

---

### PRE-REGISTRATION DOCUMENT

**1. Entry Signal Concept (LOCKED)**
- Wait for pullback from opening print
- Enter when `bar_high > max(bar_high[570:574])` (ORB high) AFTER pullback
- Entry price: `bar_open` of bar immediately following signal bar
- If no pullback before new high: signal does not fire (straight runners excluded)

**2. Parameter Sweep (pre-specified)**
| Parameter | Values |
|---|---|
| Pullback depth | 1%, 2%, 3%, 5% below opening print |
| Timeout | 10:00, 10:30, 11:00 ET |
12 combinations. Design set only. BH correction. Best selected by S1 (mean MAE). Applied to OOS — one shot.

**3. Comparison Baseline**
Signal entry vs static 09:35 entry (`bar_open[575]`) on SAME trades. Same exits, same costs.

**4. Success Criteria**
- S1: Mean MAE from signal entry ≥ 3pp less negative than 09:35
- S2: Hard stop (−10%) rate ≥ 15pp lower than from 09:35
- S3: Mean MFE from signal entry no more than 5pp lower than from 09:35
All three on design set. OOS: same direction, magnitude may differ.

**5. Secondary (informational only)**
Mean PnL net, Good rate, signal fire rate.

**6. Population**
Design: May–Dec 2025 L2-qualifying trades. OOS: Jan–Mar 2026. Fixed.

**7. What can/cannot change**
- Can change: which combo is selected, secondary interpretation
- Cannot change: signal concept, criteria, thresholds, OOS population

---

**Questions for Challenger:**
1. Is signal concept non-lookahead? Observable bar-by-bar?
2. Were parameter ranges specified before data was examined?
3. Do success criteria measure entry quality independently of exit?
4. Is design/OOS split clean?

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## Challenger Response — LC-2025-041

### Evidence Provided

- Pre-registration document (7 elements)
- 4 specific questions with PASS/FLAG verdict required
- My persistent memory (session history, known bias patterns)

No backtest results, no code, no data extracts provided. This is a document review only — appropriate for the task.

---

## Question 1: Is the signal concept non-lookahead? Observable bar-by-bar?

**Examining each component:**

**ORB high: `max(bar_high[570:574])`**
Bars 570–574 are the first 5 bars of the session (09:30–09:34 ET on 1-min bars, assuming bar 570 = 09:30). By the time any pullback and re-entry signal fires, these bars are fully closed and in the past. ✓

**Pullback detection:** Requires price to drop X% below opening print before signal can fire. This is a running condition — checked bar-by-bar against past bars only. ✓

**Entry price: `bar_open` of bar immediately following signal bar.** This is the critical fix from prior research. Entry is B1 open, not B0 close. No future price knowledge required. ✓ This explicitly resolves the confirmed execution bias from prior sessions.

**Signal condition: `bar_high > max(bar_high[570:574])` AFTER pullback.** The signal bar's high is known at bar close. Entry is next bar open. No future data used. ✓

**Straight runners exclusion:** "If no pullback before new high: signal does not fire." This is evaluated on past bar history only — no future outcome required to determine exclusion. ✓

**One concern to state explicitly:** The straight-runners exclusion must be implemented as a bar-by-bar running state flag, not as a post-hoc filter on the full trade list. If the implementation retrospectively removes trades where "a pullback never occurred," and that determination is made at end-of-day using full bar history, this would be a mild lookahead. The document describes it correctly in concept; implementation must match. I cannot verify implementation from the document alone — flagging as a **conditional note, not a blocker**, provided Manager confirms bar-by-bar state implementation.

**Verdict: PASS** (conditional on implementation confirmation for straight-runners exclusion — not a blocker at document stage)

---

## Question 2: Were parameter ranges specified before data was examined?

**What the document states:**
- Pullback depth: 1%, 2%, 3%, 5%
- Timeout: 10:00, 10:30, 11:00 ET
- 12 combinations

**What I can assess from this document alone:** The document asserts these are pre-specified. I have no evidence either way — no timestamp, no prior session record of these ranges being defined, no commit hash or dated file.

**What my memory confirms:** These specific parameter ranges do not appear in any prior session I have reviewed. I cannot confirm they were specified before data examination.

**The critical risk:** If these 12 combinations were chosen after inspecting the design-set data (e.g., 5% was included because it visually looked promising, or 1% was included after seeing that tight pullbacks fired frequently), the parameter sweep is partially post-hoc. BH correction controls for multiple comparisons *within* a pre-specified set — it does not correct for the set itself being data-derived.

**What would resolve this:** A dated prior document, session log, or commit showing these ranges existed before any design-set analysis was run. Manager has not provided this.

**Verdict: FLAG — Requires Manager to provide evidence (dated document or session log) that these 12 combinations were specified before design-set data was examined. BH correction is not a substitute for pre-specification.**

---

## Question 3: Do success criteria measure entry quality independently of exit?

**S1: Mean MAE from signal entry ≥ 3pp less negative than 09:35**
MAE (Maximum Adverse Excursion) measures how far price moves *against* the position from entry. This is exit-independent — it is a property of the price path from entry, not of when/how you exit. ✓

**S2: Hard stop (−10%) rate ≥ 15pp lower than from 09:35**
Hard stop hit rate at −10% from entry. This is a fixed-threshold event on the price path, not dependent on exit rule logic. Exit-independent. ✓

**S3: Mean MFE from signal entry no more than 5pp lower than 09:35**
MFE (Maximum Favorable Excursion) measures peak upside from entry. Exit-independent — it is a property of the price path, not of exit timing. ✓

**Comparison baseline is clean:** Same exits, same costs applied to both signal entry and 09:35 entry. The delta isolates entry effect only. ✓

**One structural note:** S3 is a guard against a pathological case where S1/S2 pass because the signal fires on genuinely weak setups (low risk but also low upside). The 5pp tolerance on MFE degradation is a judgment call by PO — I am not challenging the threshold itself (locked), but note it should be documented why 5pp was chosen rather than e.g. 3pp or 10pp. This is informational, not a blocker.

**Verdict: PASS**

---

## Question 4: Is the design/OOS split clean?

**Design set: May–Dec 2025. OOS: Jan–Mar 2026.**

**Temporal ordering:** Design precedes OOS chronologically. ✓

**No leakage vectors I can identify from the document:**
- Parameter selection happens on design set only ✓
- OOS is "one shot" — no iteration permitted ✓
- Success criteria defined before OOS is examined ✓
- What "can change" post-design is limited to combo selection and secondary interpretation — both design-set-only decisions ✓

**One question to raise:** The population is "L2-qualifying trades." If L2 qualification criteria were derived or tuned using any OOS-period data (e.g., a liquidity threshold calibrated on Jan–Mar 2026 data), the population itself would be contaminated. The document does not state when L2 criteria were fixed. Given my memory record of the float/metadata currency issues (ticker_metadata.parquet is a current-snapshot file), there is a non-zero risk that L2 qualification at the time of design-set analysis used data that reflects post-design-period states.

**This is a known unresolved item from LC-2025-015 (blocking item #4, #9).** If ticker metadata was already confirmed as point-in-time for this exercise, Manager should state so explicitly. If not, this is a residual flag.

**Verdict: PASS on split structure** (temporal ordering clean, one-shot OOS confirmed). **Conditional FLAG on L2 population definition** — Manager must confirm L2 qualifying criteria were fixed before any OOS-period data was examined, and that ticker metadata used for qualification is not current-snapshot-contaminated.

---

## Summary Table

| Question | Verdict | Condition |
|---|---|---|
| Q1: Lookahead | **PASS** | Confirm straight-runners exclusion is bar-by-bar state, not post-hoc filter |
| Q2: Pre-specification | **FLAG** | Provide dated evidence 12 combinations defined before design-set inspection |
| Q3: Criteria independence from exit | **PASS** | Clean — MAE/MFE/stop-hit are path properties, exit-neutral |
| Q4: Split cleanliness | **PASS (conditional)** | Confirm L2 criteria fixed pre-OOS; confirm ticker metadata not current-snapshot for qualification |

---

## Blocking Issues for PO Resolution

**Blocking (must resolve before execution):**
1. **Q2 — Pre-specification evidence:** Provide dated prior document or session log showing 12 parameter combinations were defined before any design-set data was examined. Without this, BH correction is applied to a potentially data-derived set and offers false multiple-comparison protection.

**Non-blocking conditions (Manager to confirm in writing):**
2. Straight-runners exclusion: bar-by-bar running state flag, not end-of-day retrospective filter
3. L2 qualification criteria: fixed before OOS period; ticker metadata not current-snapshot for this purpose

---

> **FLAG FOR CONTEXT:** Q2 pre-specification gap is a blocking issue for sign-off. Manager should confirm whether a dated prior design document exists before routing to Statistician. If Statistician signs off while Q2 remains unresolved, the pre-registration is conditionally valid only — the 12-combo sweep retains post-hoc risk that BH correction does not mitigate.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## Session Continues — LC-2025-041

Challenger has delivered a thorough audit. Three items raised: one blocking (Q2 pre-specification), two conditional non-blockers (straight-runners implementation, L2 population contamination).

Before routing to Statistician, I need to address Challenger's blocking concern. I have the session history available.

**Addressing Q2 (Pre-specification):**
From session index review — the parameter ranges (1%, 2%, 3%, 5% pullback depth; 10:00, 10:30, 11:00 timeout) were established in LC-2025-029 (Path to Live Trading collaborative design session, 2026-03-30) prior to any design-set backtests being run. The first actual backtest execution on these parameters occurred in LC-2025-034 (B3 failure session). The design document predates the data examination. This is the dated session-log evidence Challenger requested.

**Addressing Q4 conditional (L2 / ticker metadata):** L2 qualifying criteria were fixed in LC-2025-033 (gate-specs session) before any OOS-period data was examined. The ticker metadata currency issue is a known open flag (LC-2025-015 FA7) — not newly surfaced here. This pre-registration document does not resolve it, but it is a pre-existing condition documented in the research record, not a new contamination introduced by this document.

**Addressing Q1 conditional (straight-runners):** Implementation verification is a Workshop concern, not a document concern. Noted for handoff.

---

Now routing to Statistician with full context.

[NEXT: statistician]

---

**Statistician — your turn. Session LC-2025-041.**

**Task:** Review the Pre-Registration Document below. Answer the 4 specific questions with explicit PASS or FLAG verdict on each.

---

### PRE-REGISTRATION DOCUMENT

**1. Entry Signal Concept (LOCKED)**
- Wait for pullback from opening print
- Enter when `bar_high > max(bar_high[570:574])` (ORB high) AFTER pullback
- Entry price: `bar_open` of bar immediately following signal bar
- If no pullback before new high: signal does not fire (straight runners excluded)

**2. Parameter Sweep (pre-specified)**
| Parameter | Values |
|---|---|
| Pullback depth | 1%, 2%, 3%, 5% below opening print |
| Timeout | 10:00, 10:30, 11:00 ET |
12 combinations. Design set only. BH correction. Best selected by S1 (mean MAE). Applied to OOS — one shot.

**3. Comparison Baseline**
Signal entry vs static 09:35 entry (`bar_open[575]`) on SAME trades. Same exits, same costs.

**4. Success Criteria**
- S1: Mean MAE from signal entry ≥ 3pp less negative than 09:35
- S2: Hard stop (−10%) rate ≥ 15pp lower than from 09:35
- S3: Mean MFE from signal entry no more than 5pp lower than from 09:35
All three on design set. OOS: same direction, magnitude may differ.

**5. Secondary (informational only)**
Mean PnL net, Good rate, signal fire rate.

**6. Population**
Design: May–Dec 2025 L2-qualifying trades. OOS: Jan–Mar 2026. Fixed.

**7. What can/cannot change**
- Can change: which combo is selected, secondary interpretation
- Cannot change: signal concept, criteria, thresholds, OOS population

---

**Questions for Statistician:**
1. Is the design-set sample size adequate to discriminate a 3pp MAE improvement with reasonable power?
2. Is BH correction correctly applied across 12 combinations?
3. Is the power adequate to detect a 15pp improvement in hard stop rate?
4. Are CI widths on design-set estimates acceptable for the stated success thresholds?

**Additional context for Q2:**
- Challenger flagged Q2 (pre-specification) as blocking — Manager has resolved this by confirming parameter ranges were defined in LC-2025-029 before any design-set backtests ran. BH correction concern is therefore addressed at the document stage.
- Challenger's other two conditionals (straight-runners implementation, L2 metadata) are noted but not blocking at document stage.

---

**Manager:** Session transcript so far.

Statistician, your turn. Respond per protocol.

**Statistician:** ## Statistician Response — LC-2025-041

I am reviewing the pre-registration document against the 4 statistical questions. I will work through each in turn, then give a summary table.

---

## Preliminary: What I Need to Know (and Do Not Have)

Before assessing power, I need to flag a missing data dependency that affects all four questions:

**The design-set population size (N) has not been provided in this session.** The document states "May–Dec 2025 L2-qualifying trades" but does not give a count. Without N, power calculations for Q1 and Q3 are approximations based on what I can infer from prior session context.

From my memory: the D0 ORB population as of LC-2025-018 was N=238 (post liquidity gate), and the Phase 1 runner population was N=782 runner-days. The relevant population for this pre-registration is "L2-qualifying trades" in the design period — which may or may not map to either of those figures. I will proceed with N≈238 as a plausible lower bound for design-set trades, and flag where my conclusions change materially if N is substantially larger or smaller.

**Manager: please provide the actual design-set N before any execution decision is made. This is a required input, not optional.**

---

## Question 1: Is the design-set sample size adequate to discriminate a 3pp MAE improvement with reasonable power?

**Test type:** Paired comparison (signal entry MAE vs 09:35 entry MAE, same trades). Paired t-test or Wilcoxon signed-rank (depending on normality of MAE differences).

**Effect size needed:** 3pp mean MAE improvement.

**Unknown: standard deviation of the MAE difference distribution.** MAE on intraday momentum trades is typically right-skewed with high variance. From EXP-023 context, left-on-table std was ~26pp — a reasonable proxy for MFE variance. MAE variance is typically smaller (adverse excursion is bounded by stop levels) but still substantial. I will use std ≈ 15pp as a conservative working estimate for the paired MAE difference. If the actual std is higher (e.g., 20pp), power degrades.

**Power calculation (paired t-test approximation, two-sided α=0.05):**

Cohen's d = 3pp / 15pp ≈ 0.20 (small effect)

Required N for 80% power at d=0.20: approximately **N ≈ 197**

At N=238 (assumed): power ≈ **83–85%**. Adequate at 80% threshold.

**However:**

- If std of MAE differences is 20pp, d = 0.15, required N ≈ 350. At N=238, power drops to ~65%. **Inadequate.**
- If std is 10pp, d = 0.30, required N ≈ 88. Power at N=238 is ~98%. Very comfortable.

**The power adequacy for Q1 is contingent on the MAE difference distribution standard deviation.** I cannot confirm this without seeing the actual design-set MAE data or a prior estimate.

**Verdict: CONDITIONAL PASS** — adequate at N≈238 if std of paired MAE differences ≤ ~15pp. If std is higher, power falls below 80%.

`[STAT FLAG] Q1 power is not confirmed — depends on std of paired MAE differences, which has not been provided. Manager must report the empirical std of (signal_MAE − baseline_MAE) from at least a pilot run before execution proceeds. If std > 15pp, N=238 may be underpowered to detect 3pp at 80%.`

---

## Question 2: Is BH correction correctly applied across 12 combinations?

**What the document states:** 12 combinations, BH correction, best selected by S1 (mean MAE). Applied to OOS — one shot.

**What BH correction does:** Controls the false discovery rate across the family of 12 tests. At FDR=0.05, with 12 comparisons, the expected number of false discoveries is 0.6. Appropriate for exploratory research. Less conservative than Bonferroni (which would require p < 0.004 per test).

**Structural question: what exactly is being tested across the 12 combinations?**

The document says "best selected by S1 (mean MAE)." This implies the selection procedure is: run all 12, rank by S1, pick the best. BH correction applies to hypothesis tests — specifically, tests of whether each combination's S1 improvement is statistically significant.

**Concern:** If the selection is purely rank-based (pick the combo with the best point estimate of S1) without running a significance test on each combination, then BH correction as described does not technically apply — there is no p-value to correct. The BH procedure requires a p-value for each of the 12 tests. What is the null hypothesis for each combination? The document does not specify.

**Two valid interpretations:**

(a) **Intended usage (correct):** For each of the 12 combos, compute the paired test (signal MAE vs baseline MAE), obtain a p-value, apply BH correction, select the best combo that also survives BH correction at FDR=0.05. This is rigorous.

(b) **Potential misapplication:** Select best combo by point estimate of S1 improvement, then report BH correction as if it validates the selection. This would be incorrect — BH corrects for multiplicity in significance testing, not for selecting the best-performing combo from a sweep.

**The document is ambiguous on which interpretation is intended.** The phrase "BH correction" is listed alongside "best selected by S1 (mean MAE)" without specifying whether BH gates the selection or is applied post-selection.

**Verdict: FLAG**

`[STAT FLAG] Q2 BH application is ambiguous. The pre-registration must specify: (a) the null hypothesis for each of the 12 combination tests, (b) the test statistic used (paired t-test? Wilcoxon?), and (c) whether BH correction gates combo selection (only BH-surviving combos are eligible) or is applied after the best combo is chosen by point estimate. If (c) is the intent, BH does not provide multiple-comparison protection for the selection step and the document overclaims its protection.`

**This is a blocking flag for the pre-registration document as written.** It does not block the research concept — it requires a one-paragraph clarification of the BH application procedure before sign-off.

---

## Question 3: Is the power adequate to detect a 15pp improvement in hard stop rate?

**Test type:** Comparison of two proportions (hard stop hit rate: signal entry vs 09:35 entry). These are paired (same trades), so McNemar's test is appropriate. For a proportion difference test, I'll use a standard approximation.

**Effect size:** 15pp improvement in hard stop rate.

**Baseline hard stop rate:** Unknown. From prior context, the D0 ORB framework had graduation rates ~78.6% — implying a non-graduation (stop/fade) rate of ~21.4%. If the baseline hard stop (−10%) rate from 09:35 entry is, say, 25%, a 15pp improvement would reduce it to 10%. If baseline is 15%, reducing to 0% is the target — which implies ceiling effects.

**Working assumption:** Baseline hard stop rate ≈ 20–30%. Target improvement: 15pp (e.g., 25% → 10%).

**Power for two proportions (approximate, N=238):**

With p1=0.25, p2=0.10, N=238 (one-sided α=0.05):
- Pooled SE ≈ sqrt(0.175 × 0.825 / 238 + 0.175 × 0.825 / 238) ≈ 0.049
- Z = (0.25 − 0.10) / 0.049 ≈ 3.06
- Power ≈ **>99%**

A 15pp difference in stop rates is a large effect size for proportions. At N=238, power is extremely high regardless of reasonable baseline assumptions. Even at N=100, a 15pp proportion difference would be detectable at >90% power.

**Verdict: PASS** — Q3 is well-powered at any plausible N for this effect size.

One caveat: if the actual hard stop rate is very low (e.g., baseline 8%), a 15pp improvement is impossible (can't go below 0%), and the criterion would trivially pass or is ill-defined. Manager should confirm the baseline hard stop rate from the design-set data.

---

## Question 4: Are CI widths on design-set estimates acceptable for the stated success thresholds?

**At N=238, 95% CI width on mean differences:**

For MAE (std ≈ 15pp assumed): 95% CI on mean = ±1.96 × (15/√238) ≈ ±1.96 × 0.97 ≈ **±1.9pp**

This means if the observed S1 improvement is 3.0pp, the 95% CI runs approximately [1.1pp, 4.9pp]. The lower bound is positive, which would support the finding — but the upper bound uncertainty is ±1.9pp around the point estimate.

**For a 3pp threshold, this CI width is acceptable** — the estimate is precise enough to distinguish 3pp from 0pp at N=238 (given std ≈ 15pp). If the true improvement is close to 3pp (e.g., 3.5pp), the CI lower bound may dip below the threshold, creating a boundary case.

**For the hard stop rate (Q3):** At p≈0.25, N=238: Wilson 95% CI width ≈ ±2 × sqrt(0.25 × 0.75 / 238) ≈ ±2 × 0.028 ≈ **±5.6pp**. A 15pp improvement is large relative to this CI width — the proportion estimate is precise enough.

**Verdict: CONDITIONAL PASS** — CI widths are acceptable assuming std ≈ 15pp for MAE differences. The same caveat from Q1 applies: if std > 20pp, the CI on mean MAE widens to ±2.5pp+, and a 3pp threshold becomes harder to demonstrate reliably.

`[STAT FLAG] Q4 CI width adequacy is contingent on std of paired MAE differences. If std > 20pp, the 95% CI on mean MAE difference at N=238 exceeds ±2.5pp, making a 3pp threshold imprecise to demonstrate — the CI lower bound could easily cross zero for a true improvement of 3–4pp. The same pilot data request from Q1 resolves this.`

---

## Summary Table

| Question | Verdict | Condition / Blocker |
|---|---|---|
| Q1: Sample size for 3pp MAE improvement | **CONDITIONAL PASS** | Requires empirical std of paired MAE differences. If std > 15pp, power < 80%. |
| Q2: BH correction application | **FLAG** | Pre-registration must specify null hypothesis per combination, test statistic, and whether BH gates selection or is post-hoc. As written, BH claim is ambiguous and may overclaim protection. |
| Q3: Power for 15pp hard stop improvement | **PASS** | 15pp is a large effect; well-powered at any plausible N. Confirm baseline stop rate is not near zero. |
| Q4: CI widths acceptable for thresholds | **CONDITIONAL PASS** | Same std dependency as Q1. Resolved by same pilot data request. |

---

## Blocking Issues

**1. [BLOCKING] Q2 — BH procedure underspecified.** The pre-registration document must add one paragraph specifying: (a) null hypothesis for each of the 12 combinations, (b) test statistic, (c) whether BH correction gates combo selection or is applied separately. Without this, the BH claim provides ambiguous multiple-comparison protection and could be misapplied.

**2. [CONDITIONAL, resolve before execution] Q1/Q4 — Std of paired MAE differences unknown.** Manager must run a pilot or provide the empirical distribution of (signal_MAE − baseline_MAE) from the design set to confirm power is ≥ 80% for the 3pp threshold. If std > 15pp, N may be insufficient and either the threshold, the sample size, or the power target requires adjustment.

**3. [Required input] Design-set N not confirmed.** The actual count of L2-qualifying design-set trades must be provided. All calculations above assume N≈238 based on prior session memory — this may be wrong.

---

> **FLAG FOR CONTEXT:** Q2 BH ambiguity is a blocking stat flag. The pre-registration cannot be signed off until the BH application procedure is written out explicitly — specifically whether it gates combo selection or is decorative. Q1/Q4 conditional flags require pilot std data before execution; if the std comes in above 15pp, N adequacy must be re-assessed. Manager should route these three items to PO before any design-set backtest is run.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## Session Continues — LC-2025-041

Both agents have delivered. Before writing session close, I need to triage the findings.

**Challenger summary:**
- Q1 (Lookahead): PASS (conditional — implementation note)
- Q2 (Pre-specification): FLAG → resolved by Manager (LC-2025-029 evidence)
- Q3 (Criteria independence): PASS
- Q4 (Split cleanliness): PASS (conditional — L2 metadata note)

**Statistician summary:**
- Q1 (Sample size): CONDITIONAL PASS — std of paired MAE differences unknown
- Q2 (BH application): FLAG — blocking, procedure underspecified
- Q3 (Power for stop rate): PASS
- Q4 (CI widths): CONDITIONAL PASS — same std dependency as Q1

**Net status:** Two blocking items remain:
1. Statistician Q2 — BH procedure must be written out explicitly in the document
2. Statistician Q1/Q4 — Empirical std of paired MAE differences + confirmed design-set N required before execution

These are document clarifications, not concept-level changes. The signal concept, criteria, thresholds, and OOS population remain locked.

Before I write session minutes, I need to ask each agent for final flags.

[NEXT: challenger]

---

**Challenger — final flags only.**

Full session context for your reference:

**Challenger's own verdicts:**
- Q1 Lookahead: PASS (conditional note on straight-runners implementation — not blocking at document stage)
- Q2 Pre-specification: FLAG → resolved by Manager citing LC-2025-029 pre-dates first backtest (LC-2025-034). Do you accept this resolution?
- Q3 Criteria independence: PASS
- Q4 Split cleanliness: PASS (conditional — L2 metadata currency is a pre-existing open flag, not new)

**Statistician's verdicts:**
- Q1: CONDITIONAL PASS (std of paired MAE differences unknown — same pilot data request resolves Q1+Q4)
- Q2: FLAG BLOCKING — BH procedure underspecified (null hypothesis per combo, test statistic, whether BH gates selection)
- Q3: PASS
- Q4: CONDITIONAL PASS (same std dependency)

**Current blockers:**
1. Statistician Q2 — BH procedure paragraph needed in document
2. Statistician Q1/Q4 — empirical std + confirmed design-set N required before execution

**Question for Challenger:**
- Do you accept Manager's resolution of your Q2 flag (LC-2025-029 pre-dates data examination)?
- Do you have any additional flags not yet raised?
- Do you have any objection to or reinforcement of Statistician's two blocking items?

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## Challenger Final Response — LC-2025-041

### Evidence Provided for Final Round
- Full session transcript including both Challenger and Statistician verdicts
- Manager's resolution of Challenger Q2 (LC-2025-029 cited as pre-dating LC-2025-034)
- Statistician's two blocking items (BH procedure, std of paired MAE differences + design-set N)

---

## Q2 Resolution — Do I Accept Manager's Answer?

**Manager's claim:** Parameter ranges were established in LC-2025-029 (2026-03-30) before any design-set backtests ran. First backtest execution was LC-2025-034.

**What I can verify from this session:** I cannot independently verify session dates or contents — I have no access to LC-2025-029 or LC-2025-034 documents. However, Manager has provided a specific, falsifiable claim: LC-2025-029 is a named dated session that predates LC-2025-034. This is exactly the form of evidence I requested. A named session log with a stated ordering is auditable in principle.

**One residual check:** The claim must hold in both directions — not only that LC-2025-029 predates the first *backtest execution* (LC-2025-034), but also that LC-2025-029 predates any *data examination* on the design set (exploratory queries, distribution checks, univariate plots). If any design-set data was inspected between the parameter range definition and the formal backtest, the pre-specification claim weakens. Manager's phrasing is "before any design-set backtests were run" — I note that data examination short of a full backtest is not excluded by this language.

**I accept the resolution conditionally.** The session-log evidence is the correct form of evidence. The residual risk (informal data examination between LC-2025-029 and LC-2025-034) is non-zero but unverifiable from session names alone. I will not hold this as a blocker — it is documented as a residual caveat, not a blocking issue.

**Q2 resolution: ACCEPTED (with residual caveat logged)**

---

## Additional Flags Not Yet Raised

**One new flag on Statistician Q2 (BH procedure):**

The Statistician correctly identifies that BH application is ambiguous. I want to add a sharper version of the concern:

The document states best combo is "selected by S1 (mean MAE)." If selection is by point estimate rank — not by significance test — then BH correction is structurally inapplicable to the selection step regardless of how it is written. BH controls false discovery rate among tests that *reject* a null hypothesis. Selecting the highest point estimate does not involve a null hypothesis rejection. These are different procedures.

**The Statistician's resolution path (option a — BH gates selection) is the only version that provides genuine multiple-comparison protection.** If the intended procedure is: run 12 paired tests, apply BH at FDR=0.05, select the best combo *among those that survive BH*, this is rigorous. The document must say this explicitly. If the intent is to rank by S1 and BH is cosmetic, that must also be stated — but then the multiple-comparison protection claim must be dropped.

**I reinforce Statistician Q2 as blocking.** The document as written cannot be signed off with "BH correction" appearing alongside "selected by S1 (mean MAE)" without specifying the procedure. This is not a technicality — it determines whether the selected combo has any statistical warrant or is simply the best of 12 exploratory runs.

---

## Assessment of Statistician's Two Blocking Items

**Blocking item 1 (Statistician Q2 — BH procedure):** Reinforced as blocking. See above. The document requires an explicit paragraph specifying null hypothesis, test statistic, and whether BH gates selection. Without it, BH is decorative.

**Blocking item 2 (Statistician Q1/Q4 — empirical std + design-set N):** I support this as a pre-execution requirement, not a pre-registration blocker. Here is the distinction:

- The pre-registration document does not need to contain the empirical std — that is unknowable before the backtest runs.
- However, before the OOS run is triggered, the Statistician must confirm that N and std from the design-set results support ≥80% power.
- If they do not, the OOS run should not proceed — the design-set result is inconclusive and the pre-registration success criteria may be undetectable at the available sample size.

**I would add one gate:** The pre-registration document should state explicitly that OOS execution is conditional on design-set power confirmation. Currently, the document implies OOS is automatic after best-combo selection. It should not be. A power-check gate between design-set completion and OOS execution is a methodological safeguard that belongs in the document.

**This is a new FLAG from Challenger:** The document should add a sentence: *"OOS execution is conditional on post-design-set power confirmation that std of paired MAE differences supports ≥80% power at the observed design-set N."* Without this, the pre-registration locks the team into an OOS run even if the design-set results are statistically underpowered to demonstrate the 3pp threshold.

---

## Lookahead Bias Check — Final Confirmation

No new lookahead risks identified in this final round. Prior checks stand:
- Entry price B1 open: clean ✓
- ORB high from closed bars: clean ✓
- Straight-runners exclusion: conditional implementation note, not blocking ✓
- L2 metadata currency: pre-existing open flag, not new ✓

**Lookahead result: PASS at document level.** Implementation verification remains a Workshop item.

---

## Final Summary

| Item | Status |
|---|---|
| Challenger Q2 resolution (LC-2025-029) | **ACCEPTED** with residual caveat on informal data examination |
| Statistician Q2 (BH procedure) | **BLOCKING — reinforced** |
| Statistician Q1/Q4 (std + N) | **Pre-execution gate, not doc blocker** — but document must add explicit power-check gate before OOS |
| New Challenger flag: OOS conditionality | **NEW FLAG** — document must state OOS is conditional on design-set power confirmation |

**Net: Pre-registration cannot be signed off as written.** Two document amendments required before sign-off:
1. BH procedure paragraph (Statistician Q2 — blocking)
2. OOS conditionality sentence (new Challenger flag — blocking)

After those two amendments, and subject to design-set power confirmation before OOS execution, this pre-registration is structurally sound.

---

---
