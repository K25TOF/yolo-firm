# Session: orb-threshold
_Date: 2026-03-24 18:06 UTC | Agent: manager | Model: claude-sonnet-4-6_

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

Question: LC-2025-014 — ORB Breakout Detection: Threshold Review

RESEARCH QUESTION: Which volume_ratio threshold should we use for the ORB breakout entry signal?

DATA CONTEXT:

DETECTION RESULTS (on 450 multibagger universe, ORB = 15-min window):
Threshold  Matches  %     Good-rated matched  Good %
VR >= 1.5x   368    81.8%     22/22           100%
VR >= 2.0x   365    81.1%     22/22           100%
VR >= 2.5x   356    79.1%     22/22           100%

All three thresholds capture 100% of PO Good-rated stocks. Difference is only 12 stocks between 1.5x and 2.5x.

ENTRY TIMING (VR >= 2.0x):
09:30-10:00: 47 (12.9%)
10:00-10:30: 40 (11.0%)
10:30-11:30: 66 (18.1%)
11:30-13:00: 71 (19.5%)
13:00-16:00: 105 (28.8%)
Remaining 34 (9.4%): within ORB window (no breakout detected)

GOOD vs NON-GOOD (VR >= 2.0x):
Good-rated (22): entry median 11:08 ET, VR median 4.8x
Non-good (343): entry median 12:02 ET, VR median 3.6x
Good-rated stocks break out 54 minutes earlier and with 33% higher volume.

KEY OBSERVATION: The threshold barely discriminates — going from 1.5x to 2.5x only removes 12 stocks (3.3%). The 85 stocks that DON'T produce any ORB breakout at 1.5x are the interesting population — they moved 100%+ without ever breaking above ORB on volume. These are likely halt-driven or gap-and-fade events.

Optimist — which threshold and why? Is there a case for going lower (1.0x) or is 2.0x the right default?
Challenger — is there lookahead bias in how the ORB breakout is detected? Check: (1) ORB high is computed from the first 15 min — clean? (2) The scan looks at ALL subsequent bars — is this forward-looking in a live context?

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** # LC-2025-014 — Session Open

**Session ID:** LC-2025-014
**Question:** Which volume_ratio threshold should we use for the ORB breakout entry signal?
**Time-box:** Single cycle — threshold selection + bias audit
**Expected outcome:** Threshold recommendation with bias clearance (or blocker), ready for PO decision

## Scope

- **In scope:** Threshold selection (1.0x / 1.5x / 2.0x / 2.5x) rationale; lookahead bias audit of ORB detection methodology; backtest design for threshold validation
- **Out of scope:** ORB window length (15-min fixed for this session); non-ORB breakout population analysis (85 halt-driven stocks — parking per agenda)
- **Agents needed:** Both — Optimist on threshold strategy, Challenger on bias audit

## Data Context Package

```
Detection results (450-stock multibagger universe, ORB = first 15 min):

Threshold  Matches  %      Good-rated  Good%
VR >= 1.5x   368    81.8%   22/22      100%
VR >= 2.0x   365    81.1%   22/22      100%
VR >= 2.5x   356    79.1%   22/22      100%

Delta 1.5x→2.5x: only 12 stocks removed

Entry timing (VR >= 2.0x):
09:30–10:00  47  (12.9%)
10:00–10:30  40  (11.0%)
10:30–11:30  66  (18.1%)
11:30–13:00  71  (19.5%)
13:00–16:00 105  (28.8%)
No breakout  34   (9.4%)

Good vs Non-good (VR >= 2.0x):
Good (22):    median entry 11:08 ET, median VR 4.8x
Non-good(343):median entry 12:02 ET, median VR 3.6x
Good stocks: 54 min earlier, 33% higher VR at entry
```

**Question to Optimist:** Which threshold and why? Is there a case for 1.0x or is 2.0x the right default?

[NEXT: optimist]

---

**Manager:** Session transcript so far.

Optimist, your turn. Respond per protocol.

**Optimist:** ## Optimist Analysis — LC-2025-014 Threshold Selection

### Interpreting the Evidence

The data presents a remarkably clean picture, and I want to be precise about what it does and doesn't tell us.

**What the threshold sensitivity data shows:**

The 1.5x → 2.5x range removes only 12 stocks from a 450-stock universe while preserving 100% Good-rated capture across all thresholds. This is a strong signal that the Good stocks are not marginal cases — they're robust, high-VR events that clear any reasonable threshold comfortably. The median Good VR is 4.8x, meaning the typical Good trade sits well above even the 2.5x cutoff.

**What the entry timing data shows:**

This is the more interesting finding. At VR >= 2.0x:
- Only 23.9% of breakouts occur in the first hour (09:30–10:30)
- 48.3% occur after 11:30
- 28.8% occur in the 13:00–16:00 window

This is not a morning-momentum strategy in execution — it's a full-day scanner. That's not necessarily bad, but it must be acknowledged explicitly.

**The Good vs Non-good divergence is the key signal:**

Good stocks enter 54 minutes earlier and carry 33% higher VR. This is the most actionable finding in the package. It suggests two things simultaneously:
1. Early entry timing is a positive predictor of outcome
2. VR magnitude at entry — not merely threshold clearance — is predictive

The current threshold logic is binary: clears threshold or doesn't. But the data hints that VR-as-continuous-variable carries predictive power *within* the cleared population.

---

### Threshold Recommendation

**2.0x is the right default threshold.** Here is the reasoning:

- 1.5x adds only 3 stocks (368 vs 365) over 2.0x — the marginal universe is negligible and those 3 stocks are by definition the weakest VR events in the set. No Good stock is recovered by dropping to 1.5x.
- 2.5x removes 9 additional stocks from 2.0x with zero Good-stock benefit. This is premature tightening — it reduces future-state coverage without demonstrated selectivity benefit.
- 2.0x sits at the natural inflection: the Good-stock median (4.8x) is more than double the threshold, giving comfortable clearance. The threshold is not artificially tight.
- **The case for 1.0x is weak on current data.** A 1.0x threshold means volume is merely at-pace with the ORB average — there is no breakout signal, only baseline activity. Without a forward performance comparison showing 1.0x captures meaningful Good trades that 2.0x misses, lowering to 1.0x adds noise, not signal.

---

### What This Data Cannot Tell Us (and Must Be Resolved)

Before treating this as a validated threshold, two questions must be answered:

**1. Is VR measured in a lookahead-clean way?**

The data package shows detection results but not the VR calculation methodology. Specifically: is the ORB high/low calculated using *only* the first 15 minutes of data as it would be known at 09:45, or does the ORB reference any forward price data? This is Challenger's territory, but I flag it here because a contaminated VR calculation would invalidate all threshold comparisons.

**2. The 34 no-breakout stocks (9.4%) — what are they?**

At VR >= 2.0x, 34 stocks never produce a ORB breakout signal. Are any of these Good-rated? If a Good stock sits in the no-breakout bucket, the threshold framework has a structural miss — the stock moved without triggering the entry rule. This is not a threshold question, it's a breakout-definition question, but it must be checked.

---

### Alternative Angle — VR Magnitude as a Secondary Filter

The Good-stock median VR of 4.8x vs Non-good median of 3.6x is a 1.2x separation. This is meaningful. My proposal:

**Manager should run:** Within the VR >= 2.0x cleared population (365 stocks), bin trades by VR magnitude at entry: [2.0–3.0x], [3.0–4.0x], [4.0–5.0x], [5.0x+]. Cross-tab each bin against Good/Non-good rating.

If Good concentration increases monotonically with VR bin, then VR magnitude is a second-order filter that improves precision *without* requiring a fixed threshold increase. This preserves universe coverage while improving signal quality — the best of both approaches.

---

### Hypothesis for Entry Timing

The 54-minute earlier entry for Good stocks is consistent with a "fast-mover" profile — the stock that is going to make a large sustained move tends to announce itself early. This is directionally consistent with the skip-first finding from EXP-022 (stocks that establish momentum structure early are better candidates).

**If** this pattern holds, a time-of-entry filter (e.g., discount any ORB signal first appearing after 12:00) could eliminate a large chunk of the Non-good population (the 28.8% afternoon bucket) with limited Good-stock cost — but this requires confirming how many Good stocks, if any, trigger in the 13:00–16:00 window.

**Manager should also run:** Entry time distribution for the 22 Good stocks only — what % trigger before 11:30 vs after?

---

> **FLAG FOR CONTEXT:** VR magnitude as continuous predictor within cleared population — Good median 4.8x vs Non-good 3.6x — is a second-order filter hypothesis not yet tested. Bin analysis [2.0–3.0x / 3.0–4.0x / 4.0–5.0x / 5.0x+] vs Good/Non-good cross-tab is the next required test before threshold is finalised.

> **FLAG FOR CONTEXT:** Entry timing split — Good stocks enter 54 min earlier than Non-good. Time-of-entry filter (discard signals after 12:00) is an untested precision improvement. Requires Good-stock entry time distribution to assess Good-stock cost.

> **FLAG FOR CONTEXT:** 34 no-breakout stocks at VR >= 2.0x — Good/Non-good composition unknown. If any Good stocks are in this bucket, breakout definition has a structural miss independent of threshold choice.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** # LC-2025-014 — Handing to Challenger

Good analysis from Optimist. Now I need Challenger's bias audit before we can proceed to backtest design.

**Data context for Challenger:**

```
Detection results (450-stock multibagger universe, ORB = first 15 min):

Threshold  Matches  %      Good-rated  Good%
VR >= 1.5x   368    81.8%   22/22      100%
VR >= 2.0x   365    81.1%   22/22      100%
VR >= 2.5x   356    79.1%   22/22      100%

Delta 1.5x→2.5x: only 12 stocks removed

Entry timing (VR >= 2.0x):
09:30–10:00  47  (12.9%)
10:00–10:30  40  (11.0%)
10:30–11:30  66  (18.1%)
11:30–13:00  71  (19.5%)
13:00–16:00 105  (28.8%)
No breakout   34  (9.4%)

Good vs Non-good (VR >= 2.0x):
Good (22):    median entry 11:08 ET, median VR 4.8x
Non-good(343):median entry 12:02 ET, median VR 3.6x
Good stocks: 54 min earlier, 33% higher VR at entry
```

**Optimist's recommendation:** 2.0x threshold. Rationale: 1.5x adds only 3 marginal stocks, 2.5x removes 9 with zero Good-stock benefit. 2.0x is the natural inflection point.

**Optimist's open questions (flagged for Challenger's attention):**
1. VR calculation methodology — is it lookahead-clean? ORB high/low must be computed from first 15-min bars only
2. 34 no-breakout stocks — Good/Non-good composition unknown
3. VR magnitude as continuous predictor — Good median 4.8x vs Non-good 3.6x (bin analysis proposed)
4. Entry timing filter — 28.8% of entries in 13:00–16:00 afternoon window

**Question to Challenger:** Conduct a full bias audit of the ORB detection methodology. What are the lookahead risks? What would invalidate the threshold comparison? Is the 22/22 Good capture rate trustworthy, or is it an artefact of how the universe was constructed?

[NEXT: challenger]

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## Challenger Bias Audit — LC-2025-014

### Evidence Provided

I have been given:
- Threshold sensitivity table (1.5x / 2.0x / 2.5x) across 450-stock universe
- Entry timing distribution at VR >= 2.0x
- Good vs Non-good summary statistics (median entry time, median VR)
- Optimist's threshold recommendation (2.0x) and open questions

I have **not** been given:
- VR calculation methodology or code
- Definition of "Good-rated" and how those 22 stocks were selected
- The composition of the 34 no-breakout stocks
- Any forward performance data (WR, PnL) by threshold
- The date range or stock population construction method
- Any out-of-sample results

---

### Lookahead Bias Check

**RESULT: CANNOT CLEAR. Multiple unresolved lookahead risks identified. This is a blocking finding.**

I will work through each risk explicitly.

---

#### Risk 1 — ORB High/Low Calculation (HIGH SEVERITY)

The core of this methodology is detecting when price breaks above/below the Opening Range. The Opening Range high and low must be computed from **only the first 15-minute bars of that trading day**, as they would be known at exactly 09:45 ET.

**The risk:** If the ORB is computed using any intraday bar data beyond 09:45 — for example, if the implementation looks back across the full day's bars to identify the range retrospectively — then every single breakout signal is contaminated. The system would "know" that price stayed below a level before calling a breakout above it.

**What I need to clear this:** The exact VR and ORB calculation code, or an explicit description of the data slice used. Specifically:
- At what timestamp is the ORB high/low frozen?
- Is the 15-minute window defined as bar-open 09:30 through bar-close 09:44:59, or something else?
- Is VR calculated as volume-to-that-point divided by a reference volume that is itself computed from future bars?

**I cannot clear this without seeing the calculation methodology.**

---

#### Risk 2 — Volume Ratio Reference Period (HIGH SEVERITY)

VR = current volume / reference volume. The reference volume definition is critical.

**The risk:** If reference volume is defined as average daily volume (ADV) computed over a lookback window that includes the trading day being tested, then VR is contaminated. ADV calculations on the test date must use only data prior to that date.

**A second version of this risk:** If the reference volume is the ORB-period average volume computed across all days in the dataset (including future days relative to each observation), the threshold comparisons are entirely circular — you are measuring today's volume against a benchmark that partially includes today and future days.

**What I need to clear this:** Explicit definition of the reference volume denominator for VR, including the lookback window and whether it excludes same-day or future-day data.

---

#### Risk 3 — "Good-rated" Universe Construction (HIGH SEVERITY — Potential Survivorship Bias)

The 100% Good-rated capture rate (22/22 across all thresholds) is presented as strong evidence. But this figure is only meaningful if the "Good" label was assigned **without using any information derived from the breakout signal itself**.

**The risk I am identifying:** The 450-stock multibagger universe is described as such — a multibagger universe. These stocks are selected because they made large moves. If:

1. The "Good" label is assigned based on the stock making a large subsequent price move, AND
2. The ORB detection methodology was designed or tuned on this same universe

— then 22/22 capture is a tautology. Of course the methodology detects breakouts on stocks we already know broke out. The universe was selected precisely because these stocks had large moves, which are almost always accompanied by high volume and range expansion.

**This is survivorship bias in the population construction, not lookahead bias in the calculation — but it is equally disqualifying.**

The correct test is: what is the false positive rate on stocks that did **not** become multibaggers? What fraction of the 343 Non-good stocks triggered VR >= 2.0x on a day when they subsequently gave back the move? The 100% Good capture rate tells us nothing about precision — only recall.

**What I need to clarify this:**
- How were the 22 "Good" stocks labelled? What criterion?
- Were any of the 22 Good stocks excluded from the universe before analysis began?
- What is the false positive rate — i.e., of 343 Non-good VR >= 2.0x triggers, what % resulted in no meaningful follow-through?

---

#### Risk 4 — Threshold Selection from Observed Outcomes (MEDIUM SEVERITY — In-Sample Overfitting Risk)

The recommendation of 2.0x as the "natural inflection point" is based on the observation that 2.0x → 2.5x removes 9 stocks with zero Good-stock cost. But this threshold evaluation was performed on the **full dataset including the Good/Non-good labels**.

**The risk:** The threshold was effectively chosen by observing which threshold preserved Good stocks. This is reverse-engineering from outcomes. On a held-out population, the threshold that best preserves Good-stock capture may differ.

This is the same pattern I flagged in EXP-021 (threshold selection from outcome buckets). It fits in-sample perfectly but may be meaningless on new data.

**What is needed:** The threshold comparison must be validated on a held-out subset not used to observe the Good/Non-good distribution. If the full 450-stock universe was used to both define "Good" and to select the threshold, the 100% capture rate is in-sample and not generalisable.

---

#### Risk 5 — Entry Timing Contamination (MEDIUM SEVERITY)

The median entry time for Good stocks is 11:08 ET. For Non-good it is 12:02 ET.

**The risk:** If "entry time" is defined as the time of first ORB breakout signal, this is clean. But if "entry time" was identified by looking at when the stock reached its maximum intraday move and working backward to the nearest signal — this is a forward-looking construction.

**What I need:** Confirmation that entry time is defined purely as the first bar at which price exceeds the ORB high with VR >= 2.0x — calculated forward in time, not backward from outcome.

---

### What the Data Cannot Establish (Without Further Evidence)

**Claim: "2.0x is the natural inflection point"**
- NOT SUPPORTED. The data shows 2.0x preserves 22/22 Good stocks, but so does 1.5x and 2.5x. The "natural inflection" framing implies a performance cliff at other thresholds. No forward performance data (WR, PnL, follow-through rate) has been provided. Without this, 2.0x is indistinguishable from 1.5x or 2.5x on any outcome-relevant metric.

**Claim: "Good-stock median VR 4.8x vs Non-good 3.6x is the key signal"**
- DIRECTIONAL ONLY. This is a summary statistic comparison with no significance test and no out-of-sample check. With n=22 Good stocks, the median is influenced by individual outliers. I want the full distribution, not just medians.

**Claim: "Only 12 stocks removed across 1.5x → 2.5x range"**
- This is arithmetic from the table and I accept it as stated. However, "only 12" is a framing choice — 12 stocks is 2.7% of the universe. Whether that matters depends entirely on whether those 12 stocks are disproportionately Non-good (in which case 2.5x is better) or random (in which case 2.0x is arbitrary). The data does not break down those 12 stocks.

---

### Summary: Blocking Questions Before Threshold Can Be Accepted

**Manager must provide before this finding can proceed:**

1. **VR calculation code or explicit methodology** — how is reference volume defined, what is the lookback window, is same-day data excluded?

2. **ORB freeze timestamp** — at what exact time is the ORB high/low locked for signal generation?

3. **"Good" label definition** — what criterion assigns a stock as Good vs Non-good, and was this criterion applied before or after observing the breakout signal?

4. **False positive rate** — of 343 Non-good triggers at VR >= 2.0x, what % resulted in meaningful follow-through vs reversal? Without this, 100% Good capture is a recall metric without a precision counterpart.

5. **Composition of the 34 no-breakout stocks** — Good/Non-good split required. If any Good stock is in this bucket, the recall claim of 22/22 is incorrect.

6. **Out-of-sample threshold validation** — results from a held-out subset not used to observe Good/Non-good labels.

7. **Entry time construction method** — confirm entry time is computed forward from signal, not backward from outcome.

---

### On the Optimist's 2.0x Recommendation

The recommendation is **not accepted at this stage**. The reasoning is internally consistent but it rests entirely on in-sample Good-stock capture rates, which are potentially tautological given survivorship bias in the universe construction. The 2.0x threshold may be correct, but the current evidence cannot distinguish it from 1.5x or 2.5x on any forward-performance basis.

The threshold decision must wait for: (a) lookahead bias clearance on VR calculation, and (b) at minimum a false positive rate to give the 22/22 recall figure meaningful context.

---

> **FLAG FOR CONTEXT:** ORB methodology has 5 unresolved bias risks. The most critical are: (1) ORB high/low freeze timestamp — must be confirmed as 09:45 ET with no forward bar data; (2) VR reference volume construction — must exclude same-day and future-day data; (3) "Good" label survivorship bias — multibagger universe selected on outcome, 22/22 capture may be tautological. All three are blocking. Threshold recommendation cannot proceed until these are cleared.

> **FLAG FOR CONTEXT:** 100% Good-stock capture rate across all tested thresholds (1.5x–2.5x) is a recall metric only. No precision metric (false positive rate on Non-good population) has been provided. Without precision, threshold comparison has no discriminating power on forward performance.

> **FLAG FOR CONTEXT:** Threshold selection from outcome-labelled full dataset is an in-sample overfitting risk consistent with EXP-021 pattern. Held-out validation required before threshold is finalised.

---
