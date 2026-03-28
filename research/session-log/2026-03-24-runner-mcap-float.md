# Session: runner-mcap-float
_Date: 2026-03-24 09:49 UTC | Agent: manager | Model: claude-sonnet-4-6_

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

Question: LC-2025-014 — Runner Universe: Market Cap & Float Analysis

RESEARCH QUESTION: What is the optimal quality filter for the 1,922 runner universe?

DATA CONTEXT:

METADATA COVERAGE: 786/1,056 unique tickers matched (74.4%). 270 tickers have no metadata — likely OTC, delisted, or very new.

MARKET CAP DISTRIBUTION (786 tickers with data):
P5: $1.8M | P10: $2.7M | P25: $5.7M | P50: $17.3M | P75: $67.2M | P90: $306.6M | P95: $675.8M
- <$1M: 15 (1.9%)
- $1-5M: 160 (20.4%)
- $5-10M: 131 (16.7%)
- $10-25M: 131 (16.7%)
- $25-50M: 117 (14.9%)
- $50-100M: 71 (9.0%)
- $100M+: 161 (20.5%)

FLOAT DISTRIBUTION (731 tickers with data):
P50: 7.4M shares | P25: 2.6M | P75: 21.1M
- <1M: 55 (7.5%)
- 1-5M: 249 (34.1%)
- 5-10M: 120 (16.4%)
- 10M+: 307 (42.0%)

TICKER TYPE: CS (common stock) = 759 (71.9%). Warrants = 71 (6.7%). ADRs = 61 (5.8%). ETFs = 16 (1.5%).

EXCHANGE: XNAS (Nasdaq) = 777 (73.6%). XASE (Amex) = 74 (7.0%). XNYS (NYSE) = 36 (3.4%). OTC = 22 (2.1%).

COMBINED QUALITY FILTER TESTED (mcap >= $10M + CS only + major exchange):
- Surviving: 669 ticker-days (34.8%), 388 tickers
- All 6 clusters retained
- Per cluster retention: EARLY_SPIKE 27%, MORNING_FRONT 29%, others 32-40%
- Median dollar volume of filtered set: $39.5M

ALTERNATIVE THRESHOLDS:
- $25M mcap: 474 days, 288 tickers
- $50M mcap: 309 days, 194 tickers

KEY OBSERVATION FROM PO CHART REVIEW (MORNING_FRONT feedback):
- 9 out of 13 rated events were 'bad' — warrants with zero volume, AH runners misclassified as morning, halt-driven micro-caps
- 2 rated 'good' — RBNE ($124M $vol) and RELI ($26M $vol) — both high market cap, high volume
- PO feedback aligns with the quality filter — bad examples would be removed by mcap >= $10M + CS + major exchange

Optimist — what threshold maximises signal quality while retaining enough sample?
Challenger — is the 74.4% metadata match rate a problem? Are we losing signal in the 25.6% unmatched?

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** ## LC-2025-014 — Runner Universe: Market Cap & Float Analysis

**Session ID:** LC-2025-014
**Time-box:** 30 turns
**Question:** What is the optimal quality filter for the 1,922-event runner universe, balancing signal quality against sample retention?

**Scope:**
- Evaluate the combined quality filter (mcap ≥ $10M + CS only + major exchange) against alternatives
- Assess the 25.6% unmatched metadata risk
- Recommend a threshold for the next phase of runner research
- **In scope:** Threshold selection, metadata gap assessment, sample size adequacy
- **Out of scope:** New indicator testing, vol_filter variants, grinder strategy

**Expected outcome:** A recommended quality filter threshold with supporting rationale, ready for PO approval.

**Agents needed:** Both Optimist and Challenger — non-negotiable.

---

Optimist — your turn.

**Data context package:**

- Runner universe: 1,922 events across 1,056 unique tickers
- Metadata matched: 786/1,056 (74.4%). 270 unmatched — likely OTC, delisted, or very new
- Market cap distribution (786 tickers): median $17.3M. 20.4% in $1–5M range. 20.5% above $100M
- Float distribution (731 tickers): median 7.4M shares. 34.1% in 1–5M range
- Ticker types: 71.9% common stock (CS). Also warrants (6.7%), ADRs (5.8%), ETFs (1.5%)
- Exchange: 73.6% Nasdaq, 7.0% Amex, 3.4% NYSE, 2.1% OTC
- Combined filter tested (mcap ≥ $10M + CS only + major exchange): retains 669 events (34.8%), 388 tickers, all 6 clusters retained
- Alternative thresholds: $25M → 474 events / 288 tickers; $50M → 309 events / 194 tickers
- PO chart review: 9/13 MORNING_FRONT events rated 'bad' (warrants, zero-vol, AH misclassified, halt-driven micro-caps). Both 'good' examples had high mcap + high $vol — consistent with the proposed filter

**Your question:** What threshold maximises signal quality while retaining enough sample? Should we raise the bar above $10M, and what is the risk of losing real signal at stricter thresholds?

[NEXT: optimist]

---

**Manager:** Session transcript so far.

Optimist, your turn. Respond per protocol.

**Optimist:** ## Optimist Analysis — LC-2025-014 Quality Filter Threshold

### Interpreting the Evidence

The data package tells a coherent story, and it is a constructive one. The PO chart review is the most actionable signal here: 9/13 MORNING_FRONT events rated 'bad' were attributable to identifiable structural defects — warrants, zero-volume days, AH misclassification, halt-driven micro-caps. Critically, **both 'good' examples shared high mcap + high $vol**. That is not noise. That is the filter telling us what it wants to be.

The combined filter (mcap ≥ $10M + CS only + major exchange) retaining 669 events at 34.8% is not a loss of signal — it is a concentration of it. The 65.2% excluded are disproportionately the structural junk the PO review already flagged. Retention of all 6 clusters confirms we are not selecting away any genuine phenotype of runner behaviour.

### The Threshold Question

The argument for stopping at $10M rather than pushing to $25M or $50M rests on three observations:

1. **The median mcap is $17.3M.** A $25M threshold cuts below the median — you are discarding the modal runner, not an outlier tail. That is a meaningful loss of representativeness.

2. **The $1–5M bucket (20.4%) is legitimately junk** — warrants, shells, zero-vol events. The $10M threshold clips this bucket cleanly without amputating the $10–25M range, which is likely populated by real small-cap runners with genuine intraday momentum.

3. **The float data supports $10M as the right cut.** Median float is 7.4M shares with 34.1% in the 1–5M range. Low float is a known amplifier of intraday range — it is not disqualifying noise, it is mechanistically relevant to the 100%+ move universe. Pushing mcap to $50M would over-index on mid-cap names where 100%+ intraday moves have different structural causes (news, M&A, short squeeze on larger floats) and may not generalise to the tradeable small-cap momentum setup.

### Where the Risk Actually Lives

The real risk is not the threshold — it is the **25.6% unmatched metadata**. At 270 unmatched tickers, we do not know whether those events are concentrated in specific clusters or distributed evenly. If MORNING_FRONT or MULTI_SPIKE are disproportionately populated by unmatched tickers, any cluster-level analysis on the filtered set is systematically biased without us knowing it.

This is the blocking issue, not the mcap cutoff.

### Proposed Position

**Recommend $10M as the working threshold**, with one condition: before any cluster-level analysis proceeds on the filtered set, Manager should run a **cluster × matched/unmatched cross-tab**. If unmatched events are evenly distributed across clusters (within ±5pp of the 25.6% base rate), the $10M filter stands clean. If any cluster is >40% unmatched, that cluster's results must be flagged as unreliable until metadata is recovered or the events are excluded separately.

### Specific Tests to Request

1. **Cluster × metadata match status cross-tab** — count of matched vs. unmatched events per cluster, expressed as % unmatched per cluster. This is the single highest-priority data item.

2. **$10M–$25M band characterisation** — what do the 195 events dropped between $10M and $25M look like? If they skew toward specific clusters or ticker types, we learn something. If they are evenly distributed, $10M is confirmed as the right cut.

3. **$vol distribution within the filtered 669** — the PO 'good' examples were high mcap AND high $vol. A $vol floor (e.g., ≥ $500K daily) applied inside the $10M filter may do more work than raising the mcap threshold, with less sample cost.

---

> **FLAG FOR CONTEXT:** Unmatched metadata (270 tickers, 25.6%) is a blocking risk for cluster-level analysis. Cluster × match-status cross-tab must precede any cluster inference. If any cluster is >40% unmatched, its results are unreliable. This principle should be retained as a standing methodological gate.

> **FLAG FOR CONTEXT:** Float is mechanistically relevant to 100%+ intraday move universe — low float amplifies range. A $50M mcap threshold would over-index on mid-cap names with structurally different move causes. $10M preserves the small-cap momentum phenotype. Retain as rationale for threshold recommendation.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** Optimist has given a well-structured case for $10M with a conditional gate on the metadata cross-tab. Now I need Challenger to audit that reasoning before I synthesise.

---

**Challenger — your turn.**

**Question:** Audit the Optimist's recommendation of $10M as the working threshold. Challenge the logic, identify any methodological weaknesses, and assess whether the unmatched metadata risk is adequately characterised.

**Data context package:**

- Runner universe: 1,922 events across 1,056 unique tickers
- Metadata matched: 786/1,056 tickers (74.4%). 270 unmatched — likely OTC, delisted, or very new
- Market cap distribution (786 tickers): median $17.3M. 20.4% in $1–5M range. 20.5% above $100M
- Float distribution (731 tickers): median 7.4M shares. 34.1% in 1–5M range
- Ticker types: 71.9% CS. Also warrants (6.7%), ADRs (5.8%), ETFs (1.5%)
- Exchange: 73.6% Nasdaq, 7.0% Amex, 3.4% NYSE, 2.1% OTC
- Combined filter tested (mcap ≥ $10M + CS only + major exchange): retains 669 events (34.8%), 388 tickers, all 6 clusters retained
- Alternative thresholds: $25M → 474 events / 288 tickers; $50M → 309 events / 194 tickers
- PO chart review: 9/13 MORNING_FRONT events rated 'bad' (warrants, zero-vol, AH misclassified, halt-driven micro-caps). Both 'good' examples had high mcap + high $vol

**Optimist's position summary:**
- $10M is the right threshold because it clips the $1–5M junk bucket without cutting into the median ($17.3M)
- Float is mechanistically relevant — $50M would over-index on mid-cap names
- Primary risk is unmatched metadata, not the threshold itself
- Conditional gate: cluster × matched/unmatched cross-tab before any cluster-level analysis
- Additional tests: $10–$25M band characterisation, $vol distribution within filtered 669

**Your question:** Is the $10M recommendation adequately evidenced? Are there methodological weaknesses in the Optimist's logic? Is the metadata risk correctly characterised, or is it more/less severe than presented?

[NEXT: challenger]

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## Challenger Audit — LC-2025-014 Quality Filter Threshold

### Evidence I Have Been Given

- Aggregate distribution statistics for 786 matched tickers (mcap, float, ticker type, exchange)
- Filter retention counts at three thresholds ($10M: 669 events; $25M: 474; $50M: 309)
- PO chart review: 9/13 bad, 2 good, 2 unaccounted (13 total reviewed from an unspecified sampling method)
- Cluster retention statement: "all 6 clusters retained" under $10M filter
- Unmatched count: 270 tickers, 25.6% of 1,056

---

### Lookahead Bias Check

**Result: Not applicable to this analysis phase — no entry signals, price features, or outcome-based thresholds are being tested here.** This is a universe construction / metadata quality decision. The mcap and float data are static attributes, not derived from forward price outcomes.

**However, one forward-contamination risk exists:** The $10M threshold was selected *after* the PO chart review identified structural defects in the MORNING_FRONT cluster. If the threshold was tuned specifically to exclude the 9 bad PO examples, then the 669-event retention figure is partially fitted to those 13 reviewed cases. This is a mild form of design-subset contamination — not blocking at this stage, but it must be acknowledged. The threshold should be validated against the full unreviewed universe, not just the 13 PO-reviewed events.

---

### Unsupported Claims and Logical Weaknesses

#### 1. "The $10M threshold clips the $1–5M junk bucket cleanly"

**Challenged.** The data shows 20.4% of tickers are in $1–5M. But the filter is mcap ≥ $10M, which excludes the $5–10M range as well. We have no breakdown of what is in the $5–10M band. If legitimate small-cap runners concentrate there, the filter is not "clipping junk cleanly" — it is discarding a material segment with zero characterisation. **Manager must provide: event count and ticker type breakdown for the $5–10M mcap band.**

#### 2. "Both 'good' examples had high mcap + high $vol — the filter telling us what it wants to be"

**Challenged on sample size.** Two data points cannot establish a filter principle. The PO review covered 13 events from an unspecified sample of MORNING_FRONT. We do not know:
- How those 13 were selected (random? manual pick? worst-first?)
- Whether the 2 'good' examples are representative of the broader 'good' population or cherry-picked
- What the base rate of 'good' events is across the full 669

**A 2/13 'good' rate from a non-random sample is not evidence of filter effectiveness.** It may reflect sampling bias in the PO review itself. **Manager must provide: the sampling methodology for the 13 PO-reviewed events.**

#### 3. "Retention of all 6 clusters confirms we are not selecting away any genuine phenotype"

**Challenged.** "All 6 clusters retained" is a presence/absence claim, not a proportionality claim. A cluster could retain 3 events out of 400 and technically be "retained." We have no per-cluster event count before and after filtering. The $10M filter could be decimating one or two clusters numerically while preserving token representation.

**Manager must provide: per-cluster event counts before and after the $10M filter.**

#### 4. "The $1–5M bucket is legitimately junk"

**This conflates two separate mechanisms.** The PO review identified: warrants, zero-vol events, AH misclassifications, halt-driven micro-caps. Some of these (warrants, ETFs) are already excluded by the CS-only component of the combined filter. The mcap component is doing separate work. We do not know what fraction of the $1–5M mcap bucket is junk due to *mcap* specifically vs. junk already caught by the *ticker type* filter. The filters are not independent, and their individual contributions have not been isolated.

**Manager must provide: how many events are excluded by each filter component independently (mcap, CS-only, major exchange), and how many by their intersection.**

#### 5. Float as mechanistic amplifier justifying $10M over $50M

**This is an opinion, not a data-supported argument.** The Optimist asserts that low float amplifies intraday range and that $50M mcap would "over-index on mid-cap names with structurally different move causes." No data is provided to support this. We have float distributions but no outcome data (WR, return magnitude) segmented by float or mcap range. The mechanistic claim may be correct, but it is not evidenced in the data package.

---

### Metadata Risk: More Severe Than Presented

The Optimist characterises the 25.6% unmatched metadata as a "blocking risk for cluster-level analysis" pending a cross-tab. I agree it is blocking, but the severity is understated in two ways:

**A. The 25.6% figure is tickers, not events.** We have 1,922 events across 1,056 tickers. If unmatched tickers have a different event frequency than matched tickers (e.g., OTC names that appeared multiple times during a volatile period), the event-level unmatched rate could be materially higher or lower than 25.6%. **Manager must provide: unmatched count expressed as events, not just tickers.**

**B. The "likely OTC, delisted, or very new" characterisation is an assumption, not a finding.** If unmatched tickers skew toward delisted names, they are survivorship-bias-relevant — excluding them could systematically remove events that ended badly (halt, halt-and-delist, forced exit). This would artificially improve the quality profile of the matched set. **Manager must confirm: what is the actual breakdown of unmatched tickers by probable cause (OTC vs. delisted vs. new)?**

---

### Specific Demands Before Accepting the $10M Recommendation

| # | Required Data | Why It Is Blocking |
|---|---|---|
| 1 | Per-cluster event counts before and after $10M filter | "All 6 retained" is not sufficient — need proportional impact |
| 2 | $5–10M mcap band: event count and ticker type breakdown | Filter may be cutting legitimate runners, not just junk |
| 3 | PO review sampling methodology (how were 13 events selected?) | 2/13 good-rate finding is unreliable without this |
| 4 | Filter component contribution breakdown (mcap vs. CS vs. exchange, independently) | Cannot evaluate if $10M mcap is doing real work vs. redundant with CS filter |
| 5 | Unmatched count expressed as events (not tickers) | 25.6% unmatched-ticker rate ≠ 25.6% unmatched-event rate |
| 6 | Unmatched ticker breakdown by probable cause | "Likely OTC/delisted" is an assumption; delisted = survivorship bias risk |

---

### What I Do Not Dispute

- The principle of applying a combined quality filter is sound
- $10M is a reasonable starting point for discussion
- The unmatched metadata cross-tab is correctly identified as high priority
- The $vol floor suggestion is a valid additional lever

---

### Summary Verdict

**The $10M recommendation is plausible but not yet adequately evidenced.** The core logical gap is that we are evaluating filter quality based on: (a) 2 positive examples from an uncharacterised 13-event PO review, and (b) aggregate distributions that do not isolate filter component contributions. The metadata risk is also more severe at the event level than the ticker level suggests. The recommendation cannot be accepted as-is — it requires the six data items above before it clears methodological review.

---

> **FLAG FOR CONTEXT:** Unmatched metadata severity: the 25.6% figure is ticker-based. Event-level unmatched rate may differ materially if OTC/delisted tickers have higher or lower event frequency. Always require event-level unmatched counts, not just ticker-level. Also: delisted unmatched tickers = potential survivorship bias — their exclusion may inflate quality metrics of the matched set.

> **FLAG FOR CONTEXT:** Filter component independence: combined filters (mcap + CS + exchange) must be decomposed into individual contributions before evaluating which component is doing the work. Overlap between CS-only and mcap filters is unquantified here. This is a standing methodological requirement for any multi-component filter evaluation.

> **FLAG FOR CONTEXT:** PO chart review sampling methodology must always be documented. Uncharacterised sampling from a small N (13 events) cannot be used as primary evidence for threshold selection. Require: how events were selected, whether selection was random or manual, and what the base rate of 'good' events looks like across the full filtered set.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** As expected — the BacktestEngine cannot answer metadata distribution questions. These diagnostic queries require direct analysis of the runner universe dataset on the VPS, not the backtesting engine.

[BLOCKER: LC-2025-014 requires metadata cross-tabulation queries that the BacktestEngine cannot execute. Specifically needed: (1) per-cluster event counts before/after $10M filter, (2) $5–10M mcap band characterisation, (3) filter component contribution breakdown (mcap vs CS vs exchange independently), (4) unmatched count as events not tickers, (5) unmatched ticker breakdown by probable cause. These require direct Python/pandas queries against the runner universe dataset — likely `analysis/datastore/` or the ignition event script outputs. Workshop or PO VPS execution required.]

---

## LC-2025-014 — Interim Session Minutes

I can write a partial synthesis now. The recommendation cannot be finalised until the blocked data items are resolved, but I can record what the agents established and what remains open.

---

**Question asked:** What is the optimal quality filter for the 1,922-event runner universe, balancing signal quality against sample retention?

**Key contributions:**

*Optimist:*
- $10M threshold recommended: clips the $1–5M junk bucket without cutting below the $17.3M median
- Float is mechanistically relevant — $50M would over-index on mid-caps with structurally different move causes
- Correctly identified unmatched metadata as the primary risk
- Proposed cluster × match-status cross-tab as the gate before any cluster-level analysis
- Bonus proposal: $vol floor may do more work than raising mcap threshold

*Challenger:*
- Accepted the principle of a combined filter; challenged the evidence base for $10M specifically
- Identified 6 blocking data gaps — all legitimate:
  1. Per-cluster counts before/after filter (presence ≠ proportionality)
  2. $5–10M band uncharacterised
  3. PO review sampling methodology unknown (2 good examples from 13 = unreliable without knowing how 13 were selected)
  4. Filter component contributions not isolated (CS filter vs mcap filter overlap unquantified)
  5. Unmatched count is ticker-based not event-based
  6. Unmatched cause breakdown (OTC vs delisted = survivorship bias risk if delisted)
- Lookahead bias check: **clean** — static metadata attributes, no forward contamination. Minor exception noted: $10M threshold was partly shaped by the PO chart review, creating mild design-subset contamination

**Decision/outcome:** **BLOCKED — cannot finalise threshold recommendation.** $10M is a plausible working hypothesis but is not yet evidenced to Challenger's standard. Six data items required.

---

**Items for PO action:**

| # | Item | Action required |
|---|---|---|
| 1 | Per-cluster event counts before/after $10M filter | VPS query — Workshop or PO to run |
| 2 | $5–10M mcap band: event count + ticker type breakdown | VPS query |
| 3 | PO review sampling methodology (how were 13 MORNING_FRONT events selected?) | PO to document |
| 4 | Filter component contributions independently (mcap / CS / exchange) | VPS query |
| 5 | Unmatched count expressed as events, not tickers | VPS query |
| 6 | Unmatched ticker breakdown by probable cause (OTC / delisted / new) | VPS query |

Items 1, 2, 4, 5, 6 are all VPS pandas queries against the runner metadata dataset. If PO can run them, I can reconvene and complete the synthesis in LC-2025-015.

Item 3 is a PO knowledge item — how were those 13 MORNING_FRONT events selected for chart review?

---

**FLAGS FOR CONTEXT (standing methodological gates):**
- Unmatched metadata must always be expressed as event-level rate, not ticker-level rate
- Filter component contributions must be decomposed before evaluating multi-component filters
- PO chart review sampling methodology must be documented before using review outcomes as threshold evidence
- Delisted unmatched tickers = survivorship bias risk — flag whenever metadata gaps exist

**Next action:** PO to run the six VPS queries and provide results. Manager will reconvene LC-2025-015 to complete synthesis and finalise threshold recommendation.

[SESSION_COMPLETE]

---
