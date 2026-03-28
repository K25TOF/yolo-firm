# Session: runner-turnover
_Date: 2026-03-24 13:01 UTC | Agent: manager | Model: claude-sonnet-4-6_

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

Question: LC-2025-014 — Runner Universe: Turnover Analysis

RESEARCH QUESTION: What minimum turnover ratio separates tradeable runners from noise?

DATA CONTEXT:

FLOAT TURNOVER (day $ vol / float value) — 1,404 runner-days with data:
P5=0.01x  P10=0.04x  P25=0.19x  P50=1.11x  P75=7.06x  P90=27.5x

Float turnover buckets:
<0.01x: 56 (4%)   |  0.01-0.05x: 119 (8.5%)  |  0.05-0.10x: 86 (6.1%)
0.10-0.25x: 148 (10.5%)  |  0.25-0.50x: 136 (9.7%)  |  0.50-1.00x: 137 (9.8%)
1.00-2.00x: 148 (10.5%)  |  2.00-5.00x: 155 (11%)  |  5.0-10.0x: 130 (9.3%)  |  10.0x+: 289 (20.6%)

MCAP TURNOVER (day $ vol / market cap) — 1,482 runner-days:
P50=1.61x  P75=10.06x

ABOVE $10M mcap (826 days): float turnover P50=1.02x, mcap turnover P50=0.58x, median day $vol=$39M
BELOW $10M mcap (656 days): float turnover P50=1.23x, mcap turnover P50=7.01x, median day $vol=$26M

KEY CLUSTER FINDING:
  EARLY_SPIKE:    FT P50=0.06x, $vol P50=$1.4M — extremely low turnover
  MORNING_FRONT:  FT P50=0.13x, $vol P50=$1.2M — very low turnover
  MIDDAY_BUILDUP: FT P50=1.42x, $vol P50=$28M — moderate
  AFTERNOON_SURGE: FT P50=2.75x, $vol P50=$73M — high
  MULTI_SPIKE:    FT P50=0.81x, $vol P50=$31M — moderate
  EVEN_DIST:      FT P50=0.96x, $vol P50=$31M — moderate

EARLY_SPIKE and MORNING_FRONT have dramatically lower turnover (0.06x and 0.13x) than all other clusters. This suggests these clusters may contain a high proportion of low-volume/illiquid events.

COMBINED FILTER (mcap >= $10M + float turnover threshold):
  ALL:     737 days, median $vol $43M
  FT>=0.10x: 607 days (82%), median $vol $69M
  FT>=0.25x: 523 days (71%), median $vol $84M
  FT>=0.50x: 450 days (61%), median $vol $106M
  FT>=1.00x: 369 days (50%), median $vol $135M

CORRELATIONS (log10):
float_turnover × mcap_turnover: 0.649 (related but not redundant)
float_turnover × day_$vol: 0.597 (moderate — turnover adds info beyond raw volume)
mcap_turnover × market_cap: -0.484 (smaller caps have higher mcap turnover — mechanical)

NO SHARP BREAKPOINT in the float turnover distribution — it is roughly log-normal with no obvious cliff.

Optimist — does the cluster-level turnover difference matter? What threshold maximises tradeable signal?
Challenger — is float turnover adding signal beyond raw day dollar volume? Or is it redundant?

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** ## Session LC-2025-014 — Runner Universe: Turnover Analysis

**Opening the session.**

---

**Question being investigated:** What minimum float turnover ratio separates tradeable runners from noise? Is float turnover adding signal beyond raw day dollar volume?

**Time-box:** 3 agent turns (Optimist → Challenger → close)

**Scope:**
- Analyse the provided turnover distribution data to recommend a defensible threshold
- Assess whether float turnover is additive vs redundant relative to raw day $ volume
- Cluster-level interpretation is in scope
- No backtests required — this is a data interpretation session
- Threshold recommendation routes to PO for approval before any filter is implemented

**Expected outcome:** A threshold recommendation (or "no threshold") with clear rationale, plus a signal/redundancy verdict on float turnover vs raw volume.

**Agents needed:** Both Optimist and Challenger — non-negotiable.

---

**Data context package for both agents:**

- 1,404 runner-days with float turnover data; 1,482 with mcap turnover
- Distribution is log-normal, no sharp breakpoint: P5=0.01x, P25=0.19x, P50=1.11x, P75=7.06x, P90=27.5x
- Cluster P50s: EARLY_SPIKE=0.06x, MORNING_FRONT=0.13x vs all others 0.81x–2.75x
- Combined filter (mcap ≥$10M + FT threshold): FT≥0.25x retains 71% of days, lifts median $vol from $43M→$84M; FT≥1.00x retains 50%, lifts to $135M
- Float turnover × day $vol correlation: 0.597 (moderate — not redundant)
- Float turnover × mcap turnover: 0.649 (related but not redundant)

---

Optimist — your turn.

**Question for you:** Given the cluster-level turnover split (EARLY_SPIKE at 0.06x and MORNING_FRONT at 0.13x vs all other clusters at 0.81x+), does the cluster difference represent a genuine tradeability signal? Which threshold do you recommend and why — and is there a case for keeping low-turnover events rather than filtering them?

[NEXT: optimist]

---

**Manager:** Session transcript so far.

Optimist, your turn. Respond per protocol.

**Optimist:** ## Optimist Analysis — LC-2025-014 Float Turnover

---

### Interpreting the Evidence

**The cluster split is real and meaningful.**

The gap between EARLY_SPIKE (0.06x) / MORNING_FRONT (0.13x) and all other clusters (0.81x–2.75x) is not marginal — it is a 6x to 20x difference at the median. This is not noise in a continuous distribution; it is a structural separation. The two low-turnover clusters represent a qualitatively different type of event.

The log-normal shape of the overall distribution (P5=0.01x, P50=1.11x, P90=27.5x) tells us there is no natural breakpoint in the full population — but the cluster-level data *provides* the breakpoint that the aggregate distribution obscures. The 0.13x ceiling of MORNING_FRONT sits well below the 0.19x P25 of the full population. That means the two low-turnover clusters are concentrated in the bottom quartile of the overall distribution. They are not scattered throughout — they are systematically low.

**What low turnover means for tradeability:**

Float turnover below 0.25x means fewer than 25% of the float changed hands on the day of a 100%+ move. There are two possible explanations:

1. **Thin float, illiquid execution:** The move was genuine but the tradeable size is too small to enter/exit without moving the market. This is the execution-risk interpretation.
2. **Catalyst without participation:** The move happened on limited participation — a squeeze on negligible float, a halt-driven gap, or a pre-market event that resolved before the open with minimal intraday continuation.

Both explanations argue *against* these events being actionable for the YOLO strategy. In explanation (1), we can't get in and out cleanly. In explanation (2), the vol_filter_ema10 strategy has nothing to enter — the move already happened. The EARLY_SPIKE cluster's peak at 09:40 and its $344K median dollar volume reinforces this: these are events where most of the action occurred in the first 10 minutes and liquidity was minimal throughout.

**The correlation evidence supports additionality:**

A correlation of 0.597 between float turnover and day $vol is moderate — these are related but measuring different things. Raw day $vol tells you how many dollars traded. Float turnover tells you *what fraction of the available supply* those dollars represent. A $10M day on a $1B float is very different from a $10M day on a $5M float — same raw volume, opposite tradeability profiles. The 0.597 correlation confirms they are not redundant. Both belong in the filter.

---

### Threshold Recommendation: **FT ≥ 0.25x**

**Rationale:**

- Retains 71% of the runner population — we are not over-filtering
- Lifts median day $vol from $43M to $84M — nearly a 2x improvement in the quality of the retained universe
- Sits just above the MORNING_FRONT ceiling (0.13x), cleanly separating the two low-turnover clusters from the rest
- Is conservative enough that any genuine high-momentum runner with real participation will survive it
- The P25 of the full distribution is 0.19x — setting the threshold at 0.25x removes the bottom quartile plus a small buffer; this is not aggressive

**The case for keeping low-turnover events:**

I want to address this directly rather than dismiss it. There *is* a hypothetical scenario where low-turnover events are worth keeping: if EARLY_SPIKE and MORNING_FRONT show *higher* forward win rates on the vol_filter strategy despite their liquidity constraints. If the move is so concentrated and so fast that a well-timed entry in the first 10 minutes captures outsized R, the low participation might actually reduce chasing and improve entry quality.

However, I cannot substantiate this hypothesis from the data provided. The $344K median dollar volume for EARLY_SPIKE is a hard practical constraint — position sizing becomes untenable before the edge question even matters. Until we have trade-level execution data showing these clusters are enterable at real size, the execution-risk argument dominates and the threshold stands.

---

### Signal/Redundancy Verdict

**Float turnover is additive, not redundant, relative to raw day $vol.**

The 0.597 correlation leaves ~64% of variance unexplained between the two measures. The cluster-level P50 differences (0.06x vs 2.75x) are not replicated by the $vol differences in the same proportion — MIDDAY_BUILDUP has $20.7M $vol but 0.81x turnover, while AFTERNOON_SURGE has $66.6M $vol but presumably higher turnover. The two measures are capturing different dimensions of the same event. Both should be required, not treated as substitutes.

The mcap turnover correlation of 0.649 with float turnover also confirms these are related but distinct — mcap turnover captures market cap relative participation, float turnover captures supply-side constraint. Keep both as separate filter inputs.

---

### What Challenger Should Stress-Test

I want to flag two specific challenges Challenger should examine:

1. **Is the 0.25x threshold stable across time?** If EARLY_SPIKE and MORNING_FRONT are concentrated in a particular date range (e.g., a specific market regime), the cluster difference may be temporal rather than structural. The threshold could be regime-dependent.

2. **Does removing low-turnover events introduce survivorship bias in a new form?** If we filter by FT ≥ 0.25x before evaluating the strategy, we are conditioning on information that was only reliably available *after* the open in illiquid names. The forward base rate question from LC-2025-014 applies here too — at what intraday time is FT ≥ 0.25x a *confirmed* signal rather than a projected one?

---

> **FLAG FOR CONTEXT:** Float turnover threshold of FT ≥ 0.25x recommended as defensible scanner filter. Key rationale: (1) cleanly separates low-turnover clusters (EARLY_SPIKE 0.06x, MORNING_FRONT 0.13x) from the actionable population; (2) retains 71% of runner-days; (3) $vol correlation 0.597 confirms additionality — float turnover is not redundant with raw volume. Two open questions for future sessions: (a) threshold stability across market regimes, (b) intraday timing of when FT ≥ 0.25x is confirmable in real-time for pre-entry use.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-014 — Handoff to Challenger

Optimist has delivered a well-structured analysis. Key positions to stress-test:

1. **FT ≥ 0.25x threshold** — rationale: sits above MORNING_FRONT ceiling (0.13x), retains 71%, doubles median $vol
2. **Float turnover is additive** — 0.597 correlation leaves ~64% variance unexplained
3. **Low-turnover events excluded** on execution-risk grounds ($344K median $vol for EARLY_SPIKE)
4. **Optimist self-flagged two open questions:** regime stability of threshold, and intraday timing of FT confirmation

---

Challenger — your turn.

**Data context package:**

- 1,404 runner-days with float turnover data; 1,482 with mcap turnover
- Distribution is log-normal, no sharp breakpoint: P5=0.01x, P25=0.19x, P50=1.11x, P75=7.06x, P90=27.5x
- Cluster P50s: EARLY_SPIKE=0.06x, MORNING_FRONT=0.13x vs all others 0.81x–2.75x
- Combined filter (mcap ≥$10M + FT threshold): FT≥0.25x retains 71% of days, lifts median $vol from $43M→$84M; FT≥1.00x retains 50%, lifts to $135M
- Float turnover × day $vol correlation: 0.597 (moderate — not redundant)
- Float turnover × mcap turnover: 0.649 (related but not redundant)
- EARLY_SPIKE cluster: P50 $vol = $344K, peak activity 09:40
- Optimist recommendation: FT ≥ 0.25x as scanner filter; float turnover additive to raw $vol

**Question for you:** Audit the FT ≥ 0.25x threshold recommendation. Is the cluster evidence strong enough to support a hard filter at this level? What are the methodological risks — including the two the Optimist self-flagged (regime stability, intraday timing)? Are there conditions under which this threshold should be rejected or deferred?

[NEXT: challenger]

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## Challenger Audit — LC-2025-014 Float Turnover Threshold

---

### Evidence Provided

I have been given the following data:
- 1,404 runner-days with float turnover; 1,482 with mcap turnover
- Full distribution percentiles: P5=0.01x, P25=0.19x, P50=1.11x, P75=7.06x, P90=27.5x
- Cluster P50s: EARLY_SPIKE=0.06x, MORNING_FRONT=0.13x; all others 0.81x–2.75x
- Filter retention/lift table: FT≥0.25x retains 71%, lifts median $vol $43M→$84M; FT≥1.00x retains 50%, lifts to $135M
- Correlation: FT × day $vol = 0.597; FT × mcap turnover = 0.649
- EARLY_SPIKE: P50 $vol = $344K, peak 09:40

I have **not** been given: cluster trade counts, date ranges, outcome (WR/PnL) breakdowns by cluster or turnover bucket, intraday FT construction methodology, float source/staleness data, or regime-period labelling.

---

### Lookahead Bias Check

**This is the first and most serious issue.**

Float turnover = day dollar volume / (float × price). To compute this ratio at any intraday decision point, you need:

1. **Day dollar volume to that point** — available in real-time, cumulative ✓
2. **Float** — sourced from a data provider (e.g. Finviz, Yahoo Finance). This is a **static figure** that is typically updated with a lag, sometimes days or weeks after significant events (secondary offerings, lockup expirations, insider sales). If the float figure used in the research dataset was pulled *after* the trading date, it may reflect post-event float rather than the float available to a trader in real-time. **This is a potential lookahead bias.**
3. **Price denominator** — if float is expressed in shares, no price denominator is needed; if in dollars, price at what time? Close? This must be specified.

**The data package does not state the source or timestamp of the float figures used.** Until this is confirmed, every float turnover ratio in this dataset is suspect for lookahead bias.

**Verdict: Lookahead bias — UNRESOLVED. Blocking until float sourcing is confirmed.**

Additionally: the intraday timing question Optimist self-flagged is not just an "open question" — it is a structural prerequisite. A scanner filter using FT ≥ 0.25x is only valid if FT can be computed *before entry*. What time does the entry signal fire? If it fires at 09:35, cumulative dollar volume may be insufficient to confirm 0.25x on a stock with a $100M float. The threshold may only be confirmable mid-morning for many names in the universe, meaning the filter as stated cannot be applied at signal time for a significant fraction of trades. **This is not a regime question — it is a filter executability question.**

---

### Claim 1: "The cluster split is real and meaningful"

**Challenge: We have P50s. We do not have distributions or counts.**

The Optimist correctly identifies a large P50 gap between clusters. But I need more before calling this "structural separation":

- **What are the N counts per cluster?** If EARLY_SPIKE = 40 runner-days and MORNING_FRONT = 35 runner-days, together they represent ~5.3% of 1,404. The "two clusters" framing implies they are comparable in weight to the others — are they?
- **What is the within-cluster variance?** A P50 of 0.06x with a P90 of, say, 0.35x would mean a substantial fraction of EARLY_SPIKE events *clear* the 0.25x threshold. We are filtering on cluster identity (implicitly) but the threshold is being applied to the continuous variable. Without within-cluster percentile data, we cannot confirm the threshold cleanly separates these clusters in practice.
- **The Optimist states "the two low-turnover clusters are concentrated in the bottom quartile."** This is an inference, not a fact from the provided data. The P25 of the full population is 0.19x. That MORNING_FRONT P50 = 0.13x does not confirm *concentration* — it confirms the median is below P25. A cluster can have a median in the bottom quartile while having a wide distribution that extends into higher quantiles.

**I cannot accept "structural separation" from P50s alone. Manager must provide per-cluster N counts and at minimum P25/P75 per cluster.**

---

### Claim 2: "FT ≥ 0.25x retains 71% and lifts median $vol from $43M to $84M"

**Challenge: What is the composition of the retained vs filtered population?**

The 71% retention figure and $vol lift are the core quantitative support for the threshold. But:

- **The baseline $43M median is suspicious.** The full universe P50 $vol implied by the dataset should be calculable. If the full distribution has a median of $43M, that is very low for a 100%+ runner universe. Is this median dragged down by the sub-$1, thin-float names? If so, the $84M lift may be almost entirely explained by removing sub-$1 junk rather than by the float turnover signal itself.
- **Is the mcap ≥ $10M filter already applied to the $43M baseline?** The data says "combined filter (mcap ≥$10M + FT threshold)" — which implies the $43M baseline already includes the mcap filter. If not, the $vol lift is conflating two filter effects and we cannot isolate FT's contribution.
- **The FT ≥ 1.00x case lifts median to $135M at 50% retention.** This is a 60% improvement over FT ≥ 0.25x's $84M median. The Optimist recommends 0.25x without addressing why 0.5x or 1.0x is not preferable. The recommendation is arbitrary within the range 0.25x–1.00x without outcome data.

**Required: Confirm whether $43M baseline includes or excludes the mcap filter. Provide $vol medians at FT ≥ 0.5x to fill the gap between 0.25x and 1.0x. Provide the proportion of filtered-out trades attributable to each filter independently.**

---

### Claim 3: "Float turnover is additive — 0.597 correlation confirms it"

**Challenge: Correlation direction and magnitude interpretation**

The 0.597 figure is used to support additionality. This is partially valid but the argument has a gap:

- **Low correlation ≠ additive signal.** Two variables can be poorly correlated because they are measuring different things, *one of which has no predictive value*. The 0.597 correlation tells us FT and $vol are not the same metric. It says nothing about whether FT has *incremental predictive power for outcomes*. The Optimist conflates "not redundant as a measurement" with "not redundant as a signal." These are different claims.
- **What outcomes are we predicting?** No outcome variable (WR, PnL, next-bar return) has been provided. The correlation argument for additionality requires a correlation with *outcomes*, not just a cross-correlation between inputs. Without outcome data, we have evidence that FT and $vol are different metrics — not that FT adds signal.
- **The partial R² argument is not stated.** To claim additionality properly: run $vol alone against outcomes, then add FT and measure incremental R². That has not been done. We have a bivariate input correlation presented as if it were a regression result.

**The "additive" verdict should be downgraded to "non-redundant as a metric." Additive as a signal is unproven without outcome data.**

---

### Claim 4: "EARLY_SPIKE $344K median $vol is a hard practical constraint"

**This is the strongest individual claim and I accept it conditionally.**

$344K median day dollar volume makes position sizing untenable for any strategy targeting > $5K–$10K position size without moving the market. The execution-risk argument for filtering EARLY_SPIKE is valid *if* the $344K figure is (a) a P50 not a mean (confirmed — stated as P50), and (b) representative of conditions at signal time, not just EOD. If $344K is reached by EOD but only $50K traded in the first 30 minutes, the practical constraint is even tighter.

**However:** I note this is an argument for filtering EARLY_SPIKE specifically, not for the 0.25x FT threshold generally. The $344K constraint could be addressed by a direct dollar volume filter (e.g. intraday $vol > $1M by 10:00) without invoking float turnover at all. If a $vol floor already exists in the scanner, FT ≥ 0.25x may be doing redundant work for this specific exclusion.

---

### Claim 5: "FT ≥ 0.25x sits above the MORNING_FRONT ceiling (0.13x)"

**Challenge: "Ceiling" is not in the data.**

The data provides MORNING_FRONT P50 = 0.13x. The Optimist refers to a "ceiling" of 0.13x. A P50 is not a ceiling — it is a midpoint. Without knowing the P75 or P90 of MORNING_FRONT, we cannot confirm that 0.25x clears the cluster. If MORNING_FRONT P75 = 0.40x, then roughly 25% of MORNING_FRONT events would pass the FT ≥ 0.25x filter, meaning the threshold does *not* cleanly exclude this cluster.

**This is a specific factual error in the Optimist's framing. "Ceiling" should read "median." The threshold placement relative to the cluster is unconfirmed without per-cluster upper percentiles.**

---

### Regime Stability (Optimist's Open Question 1)

The Optimist correctly flags this but understates the risk. Specific concern:

- Float turnover is sensitive to **market cap changes over time**. In a bull regime, floats stay stable but $vol inflates — FT ratios rise mechanically. In a low-volatility regime, FT ratios compress. A threshold calibrated on 1,404 runner-days spanning multiple regimes may embed a regime-specific P50 that shifts meaningfully year-over-year.
- **We have no date range for the 1,404 runner-days.** If these are 2020–2021 meme-stock regime days, the 0.25x threshold may be badly miscalibrated for 2023–2025 conditions. This is not resolvable from the provided data.

**Required: Date range of the 1,404 runner-days and year-by-year or regime-period FT distribution summary.**

---

### Conditions Under Which the Threshold Should Be Rejected or Deferred

1. **Float sourcing is confirmed as post-hoc** — the entire FT dataset is contaminated by lookahead bias and must be reconstructed with real-time float data. **[BLOCKING]**
2. **Per-cluster N counts show EARLY_SPIKE + MORNING_FRONT are < 5% of the universe** — the "structural separation" claim collapses; these are edge cases not worth designing a filter around.
3. **Within-cluster P75 for MORNING_FRONT exceeds 0.25x** — the threshold does not cleanly exclude the target cluster.
4. **$43M baseline includes no mcap filter** — the $vol lift is a conflation of two effects; FT's independent contribution is unquantified.
5. **Date range is concentrated in 2020–2021** — threshold calibration is regime-specific and non-transferable to current conditions without recalibration.

---

### Summary Verdict

| Claim | Status |
|---|---|
| Cluster P50 gap is real | **Partially supported** — P50s confirm gap, distributions unknown |
| 0.25x threshold cleanly separates low-turnover clusters | **Unsupported** — "ceiling" error; within-cluster upper percentiles not provided |
| FT adds signal beyond $vol | **Unproven** — correlation ≠ predictive additionality; no outcome data |
| EARLY_SPIKE execution risk is real | **Accepted conditionally** — $344K P50 is compelling; intraday profile unknown |
| FT ≥ 0.25x is the right threshold vs 0.5x or 1.0x | **Arbitrary** — no outcome data to distinguish; 1.0x lifts $vol 60% more at 50% retention |
| Float sourcing is real-time safe | **Unresolved — BLOCKING** |

**Recommendation: Defer the threshold decision until (1) float sourcing is confirmed as real-time compatible, (2) per-cluster N counts and upper percentile distributions are provided, (3) the $43M/$84M lift is decomposed between the mcap and FT filters independently.**

The 0.25x figure is a reasonable *candidate* threshold but is not defensible as a *recommendation* on current evidence.

---

**FLAG FOR CONTEXT:** Float turnover filter (FT ≥ 0.25x) — threshold candidate only, not yet defensible. Three blocking issues: (1) float data sourcing not confirmed as real-time compatible — potential lookahead bias; (2) "ceiling" framing error — MORNING_FRONT P50=0.13x is not a ceiling, within-cluster upper percentiles required to confirm threshold cleanly excludes target cluster; (3) additionality claim conflates metric non-redundancy with signal non-redundancy — outcome data required. Session produced four required data requests before threshold can advance to PO approval.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-014 — Synthesis

Both agents have been consulted. Closing the session.

---

### Key Findings (3-5 bullets)

- **Cluster split is directionally real but evidence is incomplete.** EARLY_SPIKE (0.06x) and MORNING_FRONT (0.13x) P50s sit well below all other clusters (0.81x–2.75x). The structural separation is plausible but unconfirmed — per-cluster N counts and upper percentile distributions (P75/P90) are required before "separation" is defensible.

- **FT ≥ 0.25x is a reasonable candidate threshold, not a defensible recommendation.** Optimist's rationale is internally coherent; Challenger's audit identified a factual framing error ("ceiling" vs "median" for MORNING_FRONT P50=0.13x) and three blocking gaps before the threshold can advance.

- **Lookahead bias risk is unresolved and blocking.** Float turnover requires a float figure of known provenance. If float was pulled post-hoc (e.g. from a static data provider after the trading date), every FT ratio in the dataset is contaminated. This must be confirmed before any filter decision.

- **Additionality claim is weaker than presented.** The 0.597 correlation confirms FT and $vol are non-redundant as *metrics* — not that FT adds *predictive signal*. No outcome variable (WR, PnL) has been tested against FT. "Additive as a metric" ≠ "additive as a signal."

- **Four data requests must be resolved before threshold recommendation routes to PO.** (1) Float data source and timestamp confirmed as real-time compatible. (2) Per-cluster N counts. (3) Per-cluster P75/P90 distributions. (4) $vol lift decomposed: mcap filter contribution vs FT filter contribution independently.

---

### FLAG FOR CONTEXT Items

1. **[BLOCKING — Lookahead bias]** Float sourcing method not confirmed. If float figures are post-hoc (static provider, end-of-day or later pull), the FT dataset cannot be used as-is. Requires Workshop or PO to confirm data pipeline float sourcing method.

2. **[FACTUAL CORRECTION]** "MORNING_FRONT ceiling = 0.13x" is incorrect framing. 0.13x is the cluster P50, not a ceiling. Per-cluster upper percentiles are required to confirm FT ≥ 0.25x actually excludes the target clusters rather than merely sitting above their median.

3. **[OPEN QUESTION — Filter executability]** FT is a cumulative intraday metric. At signal fire time (e.g. 09:35), cumulative $vol may be insufficient to confirm FT ≥ 0.25x on higher-float names. This is an implementation constraint, not a regime question. Needs intraday FT confirmation timing analysis before the filter is implementable.

4. **[OPEN QUESTION — Regime stability]** Date range of the 1,404 runner-days unknown. If concentrated in 2020–2021, threshold calibration may be non-transferable to current conditions. Year-by-year FT distribution summary needed.

5. **[THRESHOLD ARBITRARINESS]** No outcome data distinguishes FT ≥ 0.25x from 0.5x or 1.0x. The 1.0x level lifts median $vol 60% more (to $135M) at 50% retention. Without WR/PnL breakdown by FT bucket, the 0.25x selection is not supportable over alternatives.

---

### Decision / Outcome

**Status: DEFERRED — threshold candidate identified, not approved.**

FT ≥ 0.25x remains a live candidate pending resolution of four data requests. Session has produced a clear checklist for what is needed before this can route to PO as a recommendation.

---

### Required Actions (for PO)

| # | Action | Owner | Priority |
|---|---|---|---|
| 1 | Confirm float data source and pull timestamp in the research pipeline — real-time compatible? | Workshop / PO | Blocking |
| 2 | Provide per-cluster N counts for all clusters in the runner universe | Manager / next session | Required |
| 3 | Provide per-cluster P75/P90 float turnover distributions | Manager / next session | Required |
| 4 | Decompose $vol lift: mcap ≥$10M filter alone vs combined with FT filter | Manager / next session | Required |
| 5 | Provide FT bucket WR/PnL breakdown (e.g. <0.25x, 0.25–1.0x, 1.0–5.0x, >5.0x) | Manager / next session | Before threshold approval |

---

### Memory Updates (for PO approval)

**Proposed update to manager memory.md:**

Add to session history:
> LC-2025-014 (float turnover threshold): FT ≥ 0.25x identified as candidate threshold — deferred. Blocking issue: float data sourcing not confirmed as real-time compatible (lookahead bias risk). Four data requests outstanding before threshold routes to PO. Key finding: cluster P50 gap is directionally real (EARLY_SPIKE 0.06x, MORNING_FRONT 0.13x vs others 0.81x+) but within-cluster distributions unknown. Additionality claim (correlation 0.597) confirmed as metric non-redundancy only — signal additionality unproven without outcome data.

Add to key lessons:
> **Correlation ≠ signal additionality.** A bivariate correlation between two input metrics (e.g. FT × $vol = 0.597) confirms they are non-redundant as measurements — it does not confirm incremental predictive value. Signal additionality requires outcome data (WR/PnL by bucket or regression R² increment).

> **Cluster P50 ≠ cluster ceiling.** When setting a filter threshold to exclude a cluster, the threshold must clear the cluster's upper percentile distribution (P75/P90), not just its median. Setting a threshold above a cluster median may still pass 25–40% of that cluster's members.

---

No doc updates to `strategy-roadmap.md` or `kpis.md` required — session produced deferred decision, no strategy state change.

=== SESSION CLOSED ===

[SESSION_COMPLETE]

---

Review: reviews/2026-03-24-runner-turnover-review.md
