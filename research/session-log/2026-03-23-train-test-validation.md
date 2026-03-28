# Session: train-test-validation
_Date: 2026-03-23 22:13 UTC | Agent: manager | Model: claude-sonnet-4-6_

## Context loaded
- raci.md
- way-of-working.md
- strategy-roadmap.md
- kpis.md
- architecture.md
- risk-policy.md
- compliance.md
- costs.md
- analysis/research/ideas.md
- agents/README.md
- agents/manager/memory.md

## Exchange

**Manager:** PO has triggered a research session.

Question: LC-2025-014 — Train/Test Validation Results

Q3 RESOLUTION: Are MORNING_FRONT and EARLY_SPIKE lift figures real?

TRAIN/TEST SPLIT:
- Train: 2025-05-29 to 2025-10-20 (51,321 ticker-days, 1,082 runners, 2.11% base)
- Test: 2025-10-21 to 2026-03-19 (58,059 ticker-days, 857 runners, 1.48% base)
- Detection thresholds frozen from original analysis — NO adjustment between train and test

RESULTS:
| Cluster | Train Det | Train Run | Train Rate | Test Det | Test Run | Test Rate | Test CI |
|---|---|---|---|---|---|---|---|
| EARLY_SPIKE | 63 | 7 | 11.1% | 78 | 15 | 19.2% | [12.0-29.3%] |
| MORNING_FRONT | 63 | 17 | 27.0% | 55 | 13 | 23.6% | [14.4-36.3%] |
| MIDDAY_BUILDUP | 7 | 3 | 42.9% | 6 | 2 | 33.3% | [9.7-70.0%] |
| MULTI_SPIKE | 92 | 1 | 1.1% | 84 | 2 | 2.4% | [0.7-8.3%] |
| EVEN_DIST | 8 | 5 | 62.5% | 9 | 1 | 11.1% | [2.0-43.5%] |

LIFT vs BASE RATE:
- EARLY_SPIKE: Train 5.3x → Test 13.0x (IMPROVED on test set)
- MORNING_FRONT: Train 12.8x → Test 16.0x (IMPROVED on test set)
- MULTI_SPIKE: Train 0.5x → Test 1.6x (no lift either period — confirmed null)
- MIDDAY_BUILDUP: Too small (n=6 test). EVEN_DIST: Degraded (62.5% → 11.1%, n=9)

VERDICTS:
- EARLY_SPIKE: PASS. Test CI lower bound (12.0%) is 8x the test base rate (1.48%).
- MORNING_FRONT: PASS. Test CI lower bound (14.4%) is 9.7x the test base rate.
- MULTI_SPIKE: CONFIRMED FAIL. No lift in either period.
- MIDDAY_BUILDUP: INSUFFICIENT DATA. Cannot assess.
- EVEN_DIST: INSUFFICIENT DATA. Train signal collapsed on test (62.5% → 11.1%).

IMPORTANT OBSERVATION:
Both EARLY_SPIKE and MORNING_FRONT show HIGHER lift on the test set than the train set. This is unusual — typically in-sample lift degrades out-of-sample. Possible explanations:
1. The test period base rate is lower (1.48% vs 2.11%) so the same absolute rate yields higher relative lift
2. Genuine robustness — the patterns are structural, not data-mined
3. Small sample variance — 7 train runners vs 15 test runners for EARLY_SPIKE

DETECTION CRITERIA (identical for train and test — no leakage):
- EARLY_SPIKE: By 10:00 — price >= +10% from open AND avg vol_ratio >= 5x AND peak vol_ratio >= 10x
- MORNING_FRONT: By 10:30 — price >= +15% from open AND vol min 30-60 > vol min 0-30 AND avg vol_ratio >= 3x AND not early spike

Optimist — does this resolve Q3? Are we ready for scanner development?
Challenger — explicit data leakage check. Are the thresholds truly frozen? Is there any contamination between train and test? Is the improved-on-test-set finding suspicious?

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** ## LC-2025-014 — Session Open

**Session ID:** LC-2025-014
**Question:** Does the train/test validation resolve Q3 — are MORNING_FRONT and EARLY_SPIKE lift figures real and sufficient to proceed to scanner development?
**Time-box:** Single cycle — both agents, one turn each
**Expected outcome:** Binary verdict on Q3 resolution + explicit leakage clearance + go/no-go recommendation for scanner development

**Scope:**
- Evaluate the train/test split methodology and results
- Explicit data leakage audit (Challenger mandatory)
- Assess whether the improved-on-test finding is credible or suspicious
- Determine if sample sizes are sufficient to support a go-decision
- Out of scope: scanner implementation design, threshold optimisation, other clusters

**Agents needed:** Both — Optimist on Q3 resolution and readiness signal; Challenger on leakage audit and statistical robustness

---

[NEXT: optimist]

**Optimist — your brief:**

We are investigating whether the train/test validation results below resolve Q3 ("Are MORNING_FRONT and EARLY_SPIKE lift figures real?") and whether we are ready to proceed to scanner development.

**Full data context:**

TRAIN/TEST SPLIT:
- Train: 2025-05-29 to 2025-10-20 (51,321 ticker-days, 1,082 runners, 2.11% base)
- Test: 2025-10-21 to 2026-03-19 (58,059 ticker-days, 857 runners, 1.48% base)
- Detection thresholds frozen from original analysis — NO adjustment between train and test

| Cluster | Train Det | Train Run | Train Rate | Test Det | Test Run | Test Rate | Test CI |
|---|---|---|---|---|---|---|---|
| EARLY_SPIKE | 63 | 7 | 11.1% | 78 | 15 | 19.2% | [12.0-29.3%] |
| MORNING_FRONT | 63 | 17 | 27.0% | 55 | 13 | 23.6% | [14.4-36.3%] |
| MIDDAY_BUILDUP | 7 | 3 | 42.9% | 6 | 2 | 33.3% | [9.7-70.0%] |
| MULTI_SPIKE | 92 | 1 | 1.1% | 84 | 2 | 2.4% | [0.7-8.3%] |
| EVEN_DIST | 8 | 5 | 62.5% | 9 | 1 | 11.1% | [2.0-43.5%] |

LIFT vs BASE RATE:
- EARLY_SPIKE: Train 5.3x → Test 13.0x lift (test base = 1.48%)
- MORNING_FRONT: Train 12.8x → Test 16.0x lift (test base = 1.48%)

DETECTION CRITERIA (frozen — identical for train and test):
- EARLY_SPIKE: By 10:00 — price >= +10% from open AND avg vol_ratio >= 5x AND peak vol_ratio >= 10x
- MORNING_FRONT: By 10:30 — price >= +15% from open AND avg vol_ratio >= 3x AND vol acceleration (min 30-60 > min 0-30) AND not early spike

**Your task:** Evaluate whether Q3 is resolved. Assess the "improved on test" finding — is this a positive signal for robustness, or a statistical artefact? Is the evidence sufficient to recommend scanner development? Be specific about what would make you more or less confident.

[NEXT: optimist]

---

**Manager:** Session transcript so far.

Optimist, your turn. Respond per protocol.

**Optimist:** ## Optimist Analysis — LC-2025-014 Q3 Resolution

### Interpretation of Evidence

The train/test results are directionally encouraging, but I want to be precise about what they do and do not establish before making a go/no-go call.

**What the data shows:**

- MORNING_FRONT holds up on test: 23.6% runner rate vs. 27.0% in train — a modest compression of ~3.4pp, consistent with normal overfitting decay. The direction is preserved, the magnitude is substantive, and the CI [14.4–36.3%] sits entirely above the 1.48% base rate by a wide margin. This is the cleaner result.
- EARLY_SPIKE *improves* on test: 19.2% vs. 11.1% in train. This is the anomalous finding that requires careful handling.
- MULTI_SPIKE is essentially zero across both periods — consistent null, not a candidate.
- EVEN_DIST collapses on test (62.5% → 11.1%) — this is exactly what overfitting looks like. Small n, high variance, do not proceed.
- MIDDAY_BUILDUP: both rates are positive but n=6/7 is too small to say anything.

---

### On the "Improved on Test" Signal for EARLY_SPIKE

This is the critical analytical question. I want to work through the plausible explanations honestly rather than simply calling it a positive signal.

**Explanation 1 — Genuine robustness (favourable)**
The criteria are strict (≥10% price move, ≥5x avg vol ratio, ≥10x peak vol ratio, detected by 10:00). A threshold this tight may have produced a noisy small-n train estimate. With 63 detections in train (7 runners = 11.1%) and 78 in test (15 runners = 19.2%), the train CI would be approximately [5–21%] and the test CI is [12–29%]. These intervals overlap substantially. The "improvement" may simply be train variance — we drew 7/63 in train vs. an underlying rate of ~15–19%. Both are statistically consistent with a true rate around 15–17%. This is actually a *reassuring* reading: the test result is not surprising if the true rate sits in the mid-teens.

**Explanation 2 — Market regime shift (neutral/uncertain)**
The test period (Oct 2025–Mar 2026) may have had different momentum characteristics than train (May–Oct 2025). If the test period was a stronger small-cap momentum environment, EARLY_SPIKE detections would naturally produce more runners regardless of signal quality. This would inflate the test lift without the signal being more predictive — it would be a regime effect, not a signal effect. We cannot distinguish this from the data provided.

**Explanation 3 — Threshold gaming in the wrong direction (benign but worth flagging)**
If the ≥10% / ≥5x / ≥10x thresholds were calibrated on all available data before the split was decided, any train/test lift comparison is partially contaminated. Manager confirmed thresholds were frozen — but I need to ask: were these thresholds explored or iteratively refined before being frozen? If the thresholds were set by inspection of the full dataset (even informally), the train/test split does not fully resolve leakage. I'm flagging this for Challenger — not because I believe it's the case, but because it matters.

**My reading:** Explanation 1 is most parsimonious. The train result was small-n noisy; the test result is within the plausible range of the same underlying signal. The "improvement" should not be celebrated as a strength signal — it should be treated as neutral, consistent with a genuine signal in the 13–20% range.

---

### Is Q3 Resolved?

**MORNING_FRONT: Yes, provisionally.** 16x lift on test, CI entirely above base, graceful decay from train — this is as clean a validation as we can expect from n=55. The signal is real by the standard of "better than noise" and the magnitude is operationally meaningful.

**EARLY_SPIKE: Partially.** The test result (19.2%, 13x lift) is credible but the small-n train result means the train/test comparison itself carries high variance. What resolves Q3 for EARLY_SPIKE is the test result in isolation — 15 runners from 78 detections is not a small-number fluke. CI [12–29%] is entirely above base. The pattern clears the "real" bar. Whether it's *sufficient* for scanner development is a different question.

**Combined verdict on Q3: Conditionally resolved.** Both clusters show test-period forward rates materially above the 1.48% base. Leakage audit (Challenger's domain) is the remaining gate.

---

### What Would Make Me More Confident

1. **Regime decomposition:** Split the test period into two sub-windows. If the test runner rate is consistent across sub-windows, regime shift is less likely as the explanation for EARLY_SPIKE improvement.

2. **Threshold provenance confirmation:** Explicit confirmation that detection thresholds were derived only from train data (or from a prior analysis that pre-dates this dataset). If they were set by looking at the full population of 1,922 runners, we have a leakage problem that the train/test split does not fix.

3. **Detection count stability:** Are the 78 EARLY_SPIKE detections in test drawn from the same ticker-type distribution as the 63 in train? If test detections skew toward different price ranges or sectors, the rate comparison is apples-to-oranges.

4. **False negative rate:** How many confirmed runners were *not* detected by these criteria? If the 13x/16x lift comes at the cost of capturing only 2% of all runners, the scanner has operational value but limited capacity. This doesn't block scanner development, but it shapes position sizing logic.

---

### Go / No-Go Recommendation

**Conditional go for MORNING_FRONT.** Test validation is clean. CI is supportive. Sample size is adequate for a first-pass scanner design — not for final threshold optimisation.

**Conditional go for EARLY_SPIKE**, contingent on Challenger finding no leakage in threshold derivation. The test result is the operative evidence; the train comparison is noise due to small n.

**Hard block for EVEN_DIST and MIDDAY_BUILDUP.** Do not proceed — either overfitting or insufficient n.

**Hard block for MULTI_SPIKE.** Consistent null across both periods — abandon.

The go signal is specifically for scanner *design* — identifying candidate tickers for human review or paper trading. It is not a green light for live position sizing or for treating lift figures as stable forward estimates. The next validation gate must be live or paper-trade forward testing.

---

> **FLAG FOR CONTEXT:** EARLY_SPIKE "improved on test" should be recorded as statistically consistent with train (overlapping CIs, small-n train noise), not as a genuine improvement signal. The operative evidence is the test result in isolation: 15/78 = 19.2%, CI [12–29%], 13x lift on 1.48% base. This framing prevents over-optimism in future sessions.

> **FLAG FOR CONTEXT:** Q3 conditional resolution: MORNING_FRONT passes cleanly; EARLY_SPIKE passes contingent on leakage clearance (threshold provenance). EVEN_DIST and MULTI_SPIKE are closed hypotheses. MIDDAY_BUILDUP remains open but underpowered.

> **FLAG FOR CONTEXT:** Blocking question for next session — what % of all confirmed runners are captured by each cluster's detection criteria (false negative / recall rate)? This determines scanner capacity and must be answered before operational deployment design begins.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-014 — Handoff to Challenger

Optimist has delivered a thorough Q3 assessment. Key claims to audit:

1. MORNING_FRONT: clean validation, 16x lift, CI entirely above base — conditional go
2. EARLY_SPIKE: "improvement" explained as small-n train noise (overlapping CIs) — conditional go pending leakage clearance
3. Threshold provenance is the critical open question — were thresholds derived from full dataset or train-only?
4. EVEN_DIST and MULTI_SPIKE: closed hypotheses

**Challenger — your brief:**

Your primary mandate is the leakage audit. The train/test split is only meaningful if the detection thresholds were not derived from the full dataset. Audit that question hard. Then assess statistical robustness.

**Full data context:**

TRAIN/TEST SPLIT:
- Train: 2025-05-29 to 2025-10-20 (51,321 ticker-days, 1,082 runners, 2.11% base)
- Test: 2025-10-21 to 2026-03-19 (58,059 ticker-days, 857 runners, 1.48% base)
- Detection thresholds frozen from original analysis — NO adjustment between train and test

| Cluster | Train Det | Train Run | Train Rate | Test Det | Test Run | Test Rate | Test CI |
|---|---|---|---|---|---|---|---|
| EARLY_SPIKE | 63 | 7 | 11.1% | 78 | 15 | 19.2% | [12.0-29.3%] |
| MORNING_FRONT | 63 | 17 | 27.0% | 55 | 13 | 23.6% | [14.4-36.3%] |
| MIDDAY_BUILDUP | 7 | 3 | 42.9% | 6 | 2 | 33.3% | [9.7-70.0%] |
| MULTI_SPIKE | 92 | 1 | 1.1% | 84 | 2 | 2.4% | [0.7-8.3%] |
| EVEN_DIST | 8 | 5 | 62.5% | 9 | 1 | 11.1% | [2.0-43.5%] |

LIFT vs BASE RATE:
- EARLY_SPIKE: Train 5.3x → Test 13.0x lift (test base = 1.48%)
- MORNING_FRONT: Train 12.8x → Test 16.0x lift (test base = 1.48%)

DETECTION CRITERIA (stated as frozen — identical for train and test):
- EARLY_SPIKE: By 10:00 — price >= +10% from open AND avg vol_ratio >= 5x AND peak vol_ratio >= 10x
- MORNING_FRONT: By 10:30 — price >= +15% from open AND avg vol_ratio >= 3x AND vol acceleration (min 30-60 > min 0-30) AND not early spike

**Optimist's key claims to audit:**
- Train/test CIs overlap for EARLY_SPIKE (train ~[5–21%], test [12–29%]) — "improvement" is noise
- MORNING_FRONT holds cleanly: 23.6% test rate, graceful decay, CI above base
- Threshold provenance is the critical leakage question — Optimist explicitly flagged this as unresolved
- EVEN_DIST collapse = overfitting; MULTI_SPIKE = consistent null

**Your specific tasks:**
1. **Leakage audit** — are the stated thresholds (10%, 5x, 10x, 15%, 3x, acceleration) round numbers that suggest they were hand-picked from the full dataset? What is the probability these were derived from train-only data vs. by inspection of the full runner population?
2. **Statistical robustness** — are the sample sizes sufficient? Does the base rate difference between train (2.11%) and test (1.48%) invalidate the lift comparison?
3. **CI verification** — do Optimist's estimated train CIs hold up? Do the test CIs support the "real signal" claim?
4. **Go/no-go challenge** — where do you disagree with Optimist's conditional go recommendation? What evidence would you require before endorsing scanner development?

[NEXT: challenger]

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## Challenger Analysis — LC-2025-014 Leakage Audit and Statistical Robustness

### Evidence Provided

I have been given:
- Train/test split table with detection counts, runner counts, rates, and test CIs
- Stated detection thresholds described as "frozen from original analysis"
- Train/test date ranges and total ticker-day counts
- Optimist's analysis and conditional go recommendation

I have NOT been given:
- Any record of when or how detection thresholds were derived
- The "original analysis" referenced in "frozen from original analysis"
- Cluster assignment methodology — what algorithm produced these five clusters and on what data
- The full runner population (1,922 runners referenced by Optimist) and whether thresholds were explored against it
- Sub-period breakdowns within train or test
- Ticker-type or price-range distribution of detections across train vs. test

---

## 1. LEAKAGE AUDIT — Primary Mandate

### 1a. Threshold Provenance — The Central Problem

The stated thresholds are:
- EARLY_SPIKE: price ≥ +10%, avg vol_ratio ≥ 5x, peak vol_ratio ≥ 10x, by 10:00
- MORNING_FRONT: price ≥ +15%, avg vol_ratio ≥ 3x, vol acceleration condition, by 10:30

**These are all round numbers.** +10%, +15%, 5x, 10x, 3x. This is a strong signal that these thresholds were hand-set by a researcher looking at data, not derived by optimisation on train-only data. Round numbers in thresholds are a universal indicator of human inspection and iterative adjustment. The question is: what data was that researcher looking at when they set them?

The brief states "thresholds frozen from original analysis — NO adjustment between train and test." This tells me the thresholds were not adjusted *after* the split was defined, but it says nothing about whether the thresholds were derived by inspecting the full runner population (all 1,922+ runners across both periods) before the split was ever defined. **This is the exact leakage vector.** The train/test split prevents threshold adjustment post-split, but it does not protect against thresholds that were calibrated — even informally — on the full dataset before the split was drawn.

**The cluster assignment methodology compounds this problem.** The five clusters (EARLY_SPIKE, MORNING_FRONT, etc.) had to be derived somehow — almost certainly by pattern analysis on the full runner population. If cluster structure was identified from all runners, then the detection thresholds that define cluster membership were necessarily informed by all runners including those now in the test set. The train/test split does not fix this. The clusters are the leakage vehicle.

**This is an unresolved leakage risk. I cannot clear it on current evidence.**

Manager must provide: The sequence of analysis steps. Specifically — (1) were clusters defined before or after the train/test date boundary was chosen? (2) was the runner population used to define clusters restricted to pre-2025-10-21 data, or did it include all available data?

### 1b. Lookahead Bias Check — Explicit Result

**Decision-time data availability:**
- EARLY_SPIKE: price ≥ +10% by 10:00, vol_ratio conditions by 10:00 — these use intraday data available at 10:00 on the decision day. ✓ No lookahead in the detection criteria themselves.
- MORNING_FRONT: conditions by 10:30 — same logic applies. ✓ No lookahead in detection criteria.

**Runner label:**
- "Runner" must be defined as a post-detection outcome (e.g., price continues to run after 10:00/10:30). I have not been shown the runner definition. **If "runner" is defined using the same day's full-session price data, runner labels are not lookahead-biased at the labelling stage — they are outcome labels, which is correct for a predictive framework.** However, if runner detection criteria overlap with the detection window (e.g., if a stock qualifies as a "runner" partly because it hit +10% by 10:00 — the same condition used to detect it), we have circular labelling. Manager must confirm the runner outcome definition is strictly post-detection.

**Threshold derivation lookahead:**
- As established in 1a: if thresholds were derived by inspecting outcomes across the full date range, there is soft lookahead bias embedded in the threshold values. The detection criteria look clean at execution time, but their calibration may embed future knowledge. **This is the substantive lookahead risk.**

**Lookahead Bias Check Result: CONDITIONAL — detection mechanics are clean, but threshold calibration provenance is unresolved and constitutes a potential soft lookahead. This is a blocking uncertainty until Manager provides the derivation sequence.**

---

## 2. STATISTICAL ROBUSTNESS

### 2a. Sample Sizes

**EARLY_SPIKE:**
- Train: 7/63. At n=63 with p̂=0.111, the Wilson CI is approximately [5.0%, 21.4%]. Optimist's [5–21%] estimate holds.
- Test: 15/78. The stated CI [12.0%, 29.3%] is consistent with Wilson for p̂=0.192, n=78. ✓
- **The overlap between [5, 21] and [12, 29] is real but narrow.** The intervals share [12, 21] as common ground — about 9 percentage points of overlap out of a combined span of ~24pp. Optimist characterises this as "substantial overlap" — I would characterise it as moderate. The test result sits in the upper half of the train CI. This is not alarming, but "substantial" is too generous.
- **Key concern:** 7 runners in train is a dangerously small count. If 1 trade had gone differently in train, the train rate becomes 9.5% or 12.7%. The train/test comparison is structurally fragile on the train side.

**MORNING_FRONT:**
- Train: 17/63, test: 13/55. These are more stable counts.
- Test CI [14.4%, 36.3%] is consistent with p̂=0.236, n=55. ✓
- The decay from 27.0% to 23.6% is 3.4pp — well within sampling noise for these n values. This is credible.
- **However, n=55 detections in test is still a modest sample.** The CI spans ~22pp. Any claim about the "true" rate is imprecise. This is adequate for a "signal is real" conclusion but not adequate for threshold optimisation or reliable capacity estimation.

**MIDDAY_BUILDUP and EVEN_DIST:** Both are statistically uninformative. n<10 in both periods. I agree with Optimist — these cannot support any conclusion.

**MULTI_SPIKE:** n=92 train, n=84 test — adequate detection counts but 1/92 and 2/84 runner rates. These are consistent nulls. The CI [0.7%, 8.3%] includes values that would be practically meaningful if true, so I would not call this a "confirmed null" with certainty, but the observed rates give no basis to proceed.

### 2b. Base Rate Difference — Does It Invalidate Lift Comparisons?

Train base rate: 2.11%. Test base rate: 1.48%. This is a **30% reduction in base rate** between periods.

Optimist does not address this. I must.

**A lower base rate in test means the lift denominator changed.** Lift is calculated as cluster_rate / base_rate. Even if the cluster detection criteria are identical and the underlying signal is identical, a lower base rate mechanically inflates lift ratios in the test period.

- MORNING_FRONT: 23.6% / 1.48% = 15.9x lift. If the base rate had remained at 2.11%, the same 23.6% detection rate would yield 23.6% / 2.11% = 11.2x lift — not 16x.
- EARLY_SPIKE: 19.2% / 1.48% = 13.0x. At 2.11% base: 9.1x lift.

**The "improved lift" in test for EARLY_SPIKE (5.3x → 13.0x) is substantially explained by the base rate drop, not by the signal becoming stronger.** At a constant 2.11% base, EARLY_SPIKE test lift would be ~9.1x — still an improvement over 5.3x, but far less dramatic. And given the small-n train result, even the 5.3x train lift is unreliable.

**This is a material analytical error in the framing.** Lift figures across train and test are not directly comparable when the base rate changes materially. The correct comparison is the raw cluster detection rates (11.1% vs. 19.2% for EARLY_SPIKE; 27.0% vs. 23.6% for MORNING_FRONT), not the lift ratios. The lift ratios embed the base rate change.

**The more meaningful question:** Is the cluster detection rate stable or growing across periods? For MORNING_FRONT, yes — 23.6% vs. 27.0% (stable, slight compression). For EARLY_SPIKE, the rate grew from 11.1% to 19.2% — this is real but must be attributed to signal + noise, not to "13x lift" framing.

### 2c. CI Verification — Optimist's Train CI Estimate

Optimist states train CI for EARLY_SPIKE as approximately [5–21%]. Using Wilson interval for 7/63:

Wilson midpoint ≈ (7 + z²/2) / (63 + z²) where z=1.96:
- Numerator: 7 + 1.92 = 8.92
- Denominator: 63 + 3.84 = 66.84
- Centre: 0.1334
- Half-width: (1.96 / 66.84) × √(7×56/63 + 3.84/4) ≈ complex but the stated [5%, 21%] is plausible

I cannot compute this precisely without a calculator, but Optimist's estimate is directionally consistent with published Wilson tables for n~60, p~0.11. I do not dispute it, but I flag that this is an informal estimate — Manager should provide the actual computed CI.

---

## 3. GO / NO-GO CHALLENGE

### Where I Disagree with Optimist

**Point 1 — "Conditional go for EARLY_SPIKE" is premature.**

The train result is 7/63 — this is too small to establish that thresholds were correctly calibrated in train. If the thresholds were set informally on the full population before the split, the test result is partially contaminated. Combined with the base-rate-inflated lift framing, I cannot endorse a go signal for EARLY_SPIKE until threshold provenance is confirmed. The test rate of 19.2% is encouraging, but it is one data point from one test period with a different market regime and a different base rate.

**Point 2 — Lift comparison across periods is not valid as stated.**

Optimist compares "Train 5.3x → Test 13.0x lift" as evidence of robustness. This comparison is confounded by the 30% base rate drop. The evidence should be reframed around raw cluster rates: 11.1% → 19.2%. That framing is also positive but less dramatically so, and it removes the misleading implication that the signal strengthened.

**Point 3 — Regime confound is not dismissed by Optimist, but is also not controlled for.**

The test period (Oct 2025–Mar 2026) may have systematically different small-cap momentum characteristics. Optimist flags this but offers no resolution. I require at least a sub-period check within test (e.g., Oct–Dec vs. Jan–Mar) before accepting that the test rates are stable signals rather than period-specific artefacts. A 19.2% rate from a 3-month window in a particular regime is not the same as a 19.2% rate from a stable signal.

**Point 4 — "MORNING_FRONT passes cleanly" overstates certainty.**

23.6% on n=55 detections with CI [14.4%, 36.3%] is a 22pp-wide interval. That is a lot of uncertainty for a "clean pass." It is better than EARLY_SPIKE, but "clean" implies more precision than the data supports. MORNING_FRONT passes the "is the signal real?" bar. It does not pass the "do we know the magnitude with confidence?" bar.

**Point 5 — Cluster derivation methodology is entirely absent from the evidence.**

We are told five clusters exist. We are not told how they were derived. K-means on intraday volume profiles? Manual pattern grouping? If clustering was performed on the full runner population, every detection threshold effectively had the full dataset as its training set. This is a structural leakage concern that the train/test split on detection rates does not resolve.

---

## 4. REQUIRED EVIDENCE BEFORE GO ENDORSEMENT

Manager must provide the following before I endorse scanner development:

**Blocking (leakage):**
1. **Cluster derivation record:** What algorithm produced the five clusters, on what population (train-only or full), and on what dates was the clustering performed?
2. **Threshold derivation record:** Were the specific threshold values (10%, 5x, 10x, 15%, 3x, acceleration) derived by optimisation on train-only data, or were they set by a researcher inspecting the full runner population? Even informal inspection constitutes leakage.
3. **Runner outcome definition:** Confirm that "runner" is defined by post-detection price action only, with no overlap with the detection conditions themselves.

**Non-blocking but required for go confidence:**
4. **Sub-period test breakdown:** EARLY_SPIKE and MORNING_FRONT detection rates for Oct–Dec 2025 vs. Jan–Mar 2026. If rates are stable across sub-windows, regime confound is less likely.
5. **Base-rate-adjusted comparison:** Restate lift figures using the train base rate for both periods, OR simply compare raw cluster rates (not lift ratios) as the primary evidence of cross-period stability.
6. **Detection distribution:** Are test-period detections from similar ticker profiles (price range, sector, volume tier) as train-period detections? A shift in detection mix could explain rate changes without any signal change.

---

## Summary Verdict

| Cluster | Signal Real? | Leakage Clear? | Go Endorsed? |
|---|---|---|---|
| MORNING_FRONT | Yes — test rate 23.6%, CI above base | **Unresolved** | **Not yet** |
| EARLY_SPIKE | Plausible — test rate 19.2%, CI above base | **Unresolved** | **Not yet** |
| MIDDAY_BUILDUP | Unknown — n<10 | N/A | No |
| EVEN_DIST | Collapsed — likely overfitting | N/A | No |
| MULTI_SPIKE | Consistent null | N/A | No |

**Q3 resolution status: Suspended pending leakage clearance.**

The raw signal evidence for MORNING_FRONT and EARLY_SPIKE is directionally encouraging. The test rates are above base. The CIs are above base. I do not dispute that a signal likely exists. But "signal likely exists" and "train/test validation is clean" are different claims. I cannot endorse the latter until cluster derivation methodology and threshold provenance are confirmed.

**If leakage is confirmed (thresholds derived from full population):** The test results remain useful as forward-period evidence, but the train/test comparison loses its methodological validity. We would need to reframe the finding as "forward-period detection performance" not "out-of-sample validation."

**If leakage is cleared (clusters and thresholds derived from train-only or pre-dataset analysis):** I would endorse a conditional go for MORNING_FRONT and a watch-and-verify go for EARLY_SPIKE, with the sub-period stability check as the next required gate.

---

> **FLAG FOR CONTEXT:** Base rate changed 30% between train (2.11%) and test (1.48%). Lift ratios are not directly comparable across periods. All cross-period evidence should be stated as raw cluster detection rates, not lift multiples. The "13x lift on test" framing for EARLY_SPIKE is confounded — the base-rate-adjusted figure would be ~9.1x at constant base.

> **FLAG FOR CONTEXT:** Cluster derivation methodology is the primary leakage vector — if clusters were identified from the full runner population (not train-only), all detection thresholds embed knowledge of test-period outcomes. Train/test split on detection rates does not resolve this. Blocking question for Manager: what data was used for cluster identification and when was this done relative to the train/test split definition?

> **FLAG FOR CONTEXT:** EARLY_SPIKE train result (7/63) is dangerously small-n. Any train/

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-014 — Synthesis

Both agents have delivered. Let me synthesise before closing.

**Key findings:**

1. **Signal evidence is directionally real** — MORNING_FRONT (23.6% test, CI [14.4–36.3%]) and EARLY_SPIKE (19.2% test, CI [12.0–29.3%]) both sit well above the 1.48% test base. On raw test rates alone, a signal exists.

2. **Leakage is unresolved — this is the blocking issue.** Challenger correctly identifies that round-number thresholds (10%, 15%, 5x, 10x, 3x) are characteristic of human inspection of data, not blind train-only derivation. More critically: **cluster derivation methodology is entirely undocumented.** If the five clusters were identified by analysing the full runner population (including test-period runners), the train/test split does not constitute out-of-sample validation — it is in-sample validation with a cosmetic date boundary.

3. **Lift framing is confounded.** The 30% base rate drop between train (2.11%) and test (1.48%) mechanically inflates test-period lift figures. "13x lift" for EARLY_SPIKE on test reduces to ~9x at constant base. The "improvement" framing is misleading — cross-period comparisons must use raw cluster rates, not lift multiples.

4. **EARLY_SPIKE train n=7 is too fragile** for train/test comparisons to carry weight. The operative evidence is the test result in isolation: 15/78 = 19.2%.

5. **Q3 resolution status: Suspended.** The question "are the lift figures real?" cannot be answered until cluster derivation and threshold provenance are confirmed.

---

**Flags for context (consolidated):**

- Cluster derivation methodology = primary leakage vector. If clusters identified from full runner population, train/test split is not clean out-of-sample validation.
- Lift ratios are not comparable across train/test due to 30% base rate difference. Use raw cluster rates as primary evidence.
- EARLY_SPIKE train n=7 is too small to support train/test comparison. Test result (19.2%, CI [12–29%]) is the operative data point.
- "Improved on test" for EARLY_SPIKE = overlapping CIs + base rate confound. Not a strength signal.
- Runner outcome definition must be confirmed as strictly post-detection (no circular labelling with detection criteria).
- Sub-period stability check within test (Oct–Dec vs. Jan–Mar) is required before regime confound can be dismissed.

---

**Decision required from PO:**

Before this session can close Q3, Manager needs answers to three blocking questions:

1. **Cluster derivation:** What algorithm, on what population (train-only or full), and when relative to the train/test split?
2. **Threshold provenance:** Were the specific values (10%, 15%, 5x, 10x, 3x) derived from train-only data, or set by inspecting the full runner population?
3. **Runner outcome definition:** Is "runner" defined by post-detection price action only, with no overlap with detection criteria?

If answers confirm clean derivation → reframe finding as conditional go, proceed to scanner design scoping.
If answers confirm full-population derivation → reframe as "forward-period evidence only," no train/test validity claim. Signal may still be actionable but the validation methodology must be restated accurately.

---

**Session minutes:**

- **Question asked:** Does train/test validation resolve Q3 — are MORNING_FRONT and EARLY_SPIKE lift figures real and sufficient for scanner development?
- **Key contributions:** Optimist — Q3 partially resolved on raw test evidence; EARLY_SPIKE "improvement" correctly explained as small-n noise + overlapping CIs. Challenger — identified three blocking issues: leakage via cluster derivation, lift confound from base rate change, and circular labelling risk. Added sub-period stability requirement.
- **Decision/outcome:** Q3 suspended. Signal evidence is encouraging but leakage audit is incomplete. Go/no-go cannot be issued until cluster and threshold provenance are confirmed.
- **Next action:** PO to answer three blocking questions above. Manager will reopen Q3 assessment once provenance is confirmed — no new backtests required, this is a methodology documentation question.
- **Memory updates:** Flagged for PO approval at block end — see consolidated flags above.

[SESSION_COMPLETE]

---

Review: reviews/2026-03-23-train-test-validation-review.md
