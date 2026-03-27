# Session: movers-volume-profile
_Date: 2026-03-23 20:11 UTC | Agent: manager | Model: claude-sonnet-4-6_

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

Question: LC-2025-014 — 100%+ Intraday Movers: Volume Profile Clustering

RESEARCH QUESTION: What are the consistent volume profile patterns among 100%+ intraday movers, and which are most actionable for scanner design?

FULL DATA CONTEXT:

POPULATION: 1,922 ticker-days where (HOD-LOD)/LOD >= 100% across ALL bars (incl pre/post market). 1,056 unique tickers. May 2025 - March 2026. 110,240 total ticker-days scanned = 1.7% qualify.

RANGE DISTRIBUTION:
- 100-200%: 1,366 (71%)
- 200-500%: 458 (24%)
- 500-1000%: 82 (4%)
- 1000%+: 33 (2%)

SIX CLUSTERS IDENTIFIED (rule-based, by RTH volume profile shape):

1. EARLY_SPIKE (114, 5.9%): >50% volume in first 30 min. Med range 140%, med dollar vol $344K, med price $1.85. Peak price at 09:40. Volume fades rapidly after 10:00. Thin liquidity stocks.

2. MORNING_FRONT (107, 5.6%): First hour >60% of volume but not concentrated in first 30 min. Med range 145%, med dollar vol $524K, med price $2.08. Peak price at 10:00. Gradual morning build.

3. MIDDAY_BUILDUP (319, 16.6%): Peak volume bucket between 11:00-13:00. Med range 140%, med dollar vol $20.7M, med price $3.01. Peak price at 12:00. Volume spreads across midday session. Better liquidity.

4. AFTERNOON_SURGE (463, 24.1%): >40% of volume in last hour. Med range 154%, med dollar vol $66.6M(!), med price $3.50. Peak price at 15:50. DOMINANT cluster — 58% of volume in the final 10-min bucket. Most liquid cluster by far.

5. MULTI_SPIKE (512, 26.6%): 2+ significant volume spikes separated by >10 buckets. Med range 150%, med dollar vol $22.8M, med price $3.01. Peak price at 13:10. Volume distributed with a large end-of-day spike (16% in final bucket). Largest cluster.

6. EVEN_DIST (407, 21.2%): No single period dominates. Med range 151%, med dollar vol $20.7M, med price $3.25. Peak price at 11:00. Volume front-loaded (81% first half) but without a sharp spike. Classic steady runner.

CROSS-TAB FINDINGS:
- Price: Early spike and morning front are dominated by sub-$1 and $1-3 stocks (thin names). Midday/afternoon/multi/even have more $3+ stocks.
- Range: Afternoon surge and multi-spike have the most extreme movers (500%+).
- Dollar volume: Afternoon surge has 3x the dollar volume of any other cluster ($66.6M median).

KEY OBSERVATION: The AFTERNOON_SURGE cluster has 58% of its volume in the final 10-minute bucket (15:50-16:00). This looks like closing auction / market-on-close activity, not organic momentum. This cluster needs scrutiny — it may be an artefact of forced buying/selling at close.

Optimist — assess which clusters represent genuine tradeable momentum vs artefacts. What is most actionable? What should we investigate next?

Challenger — audit the clustering methodology. Are these real patterns or artefacts of the bucketing? Is the AFTERNOON_SURGE cluster suspicious? Any look-ahead in the methodology? What data gaps exist?

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** ## LC-2025-014 — Session Open

**Session ID:** LC-2025-014
**Question:** What are the consistent volume profile patterns among 100%+ intraday movers, and which are most actionable for scanner design?
**Time-box:** Single session, max 50 turns
**Expected outcome:** Actionable cluster assessment — which clusters warrant further investigation, which are artefacts, and what are the next research steps

**Scope boundaries:**
- In scope: Cluster interpretation, methodology audit, actionability for scanner design, next-step recommendations
- Out of scope: Implementing scanner changes, running backtests this session (data package is descriptive statistics only — no raw trade data to backtest against), capital decisions

**Agents needed:** Both Optimist and Challenger — non-negotiable per protocol

**Data context package** (injected into every routing message):

> Population: 1,922 ticker-days, 110,240 total scanned (1.7% qualify, HOD/LOD ≥ 100%). May 2025–Mar 2026.
> Six clusters: EARLY_SPIKE (114, 5.9%), MORNING_FRONT (107, 5.6%), MIDDAY_BUILDUP (319, 16.6%), AFTERNOON_SURGE (463, 24.1%), MULTI_SPIKE (512, 26.6%), EVEN_DIST (407, 21.2%).
> Key flags: AFTERNOON_SURGE has 58% volume in final 10-min bucket — possible MOC artefact. EARLY_SPIKE/MORNING_FRONT are thin sub-$1 names. AFTERNOON_SURGE has 3x dollar volume of any other cluster ($66.6M median).

---

Optimist — your turn. Full data context below.

**Population:** 1,922 ticker-days where (HOD-LOD)/LOD ≥ 100% across ALL bars (incl. pre/post market). 1,056 unique tickers. May 2025–Mar 2026. 110,240 total ticker-days scanned = 1.7% qualify.

**Range distribution:** 100-200%: 1,366 (71%) · 200-500%: 458 (24%) · 500-1000%: 82 (4%) · 1000%+: 33 (2%)

**Six clusters:**
1. EARLY_SPIKE (114, 5.9%): >50% vol in first 30 min. Med range 140%, med $vol $344K, med price $1.85. Peak price 09:40.
2. MORNING_FRONT (107, 5.6%): First hour >60% vol, not concentrated in first 30 min. Med range 145%, med $vol $524K, med price $2.08. Peak price 10:00.
3. MIDDAY_BUILDUP (319, 16.6%): Peak vol bucket 11:00-13:00. Med range 140%, med $vol $20.7M, med price $3.01. Peak price 12:00.
4. AFTERNOON_SURGE (463, 24.1%): >40% vol in last hour, 58% in final 10-min bucket. Med range 154%, med $vol $66.6M, med price $3.50. Peak price 15:50.
5. MULTI_SPIKE (512, 26.6%): 2+ spikes separated by >10 buckets. Med range 150%, med $vol $22.8M, med price $3.01. Peak price 13:10.
6. EVEN_DIST (407, 21.2%): No single period dominates, 81% first-half vol. Med range 151%, med $vol $20.7M, med price $3.25. Peak price 11:00.

**Your task:** Assess which clusters represent genuine tradeable momentum vs artefacts. What is most actionable for scanner design? What should we investigate next? Be specific — bullet points, prioritised recommendations.

[NEXT: optimist]

---

**Manager:** Session transcript so far.

Optimist, your turn. Respond per protocol.

**Optimist:** ## Optimist Assessment — LC-2025-014

### Interpretation of Evidence

This is a rich descriptive dataset. Six clusters, 1,922 qualifying ticker-days over ~10 months. Before declaring any cluster an artefact, I want to be precise about what "artefact" means here — it means the volume profile reflects a mechanical or structural force (index rebalancing, ETF flows, MOC orders) rather than organic momentum. That's a testable claim, not a given.

Let me work through each cluster:

---

**EARLY_SPIKE (114, 5.9%) — High signal potential, thin universe**

- Median price $1.85, median $vol $344K. This is sub-penny-stock territory for liquidity.
- But: peak price at 09:40 means the move completes *fast*. This is the profile of a gap-and-go or pre-market catalyst that gets confirmed in the open.
- Actionability concern: $344K median $vol means position sizing is severely constrained. But it's not zero — for small-size entries, this is the cleanest directional signal in the set.
- **Not an artefact.** Thin, yes. Untradeable at scale, yes. Tradeable with size constraints — open question.

---

**MORNING_FRONT (107, 5.6%) — Most structurally clean cluster**

- Volume concentration in first hour (60%+) but spread across the hour, not just the open. Peak price 10:00.
- Median $vol $524K — still thin but the best of the early clusters.
- This profile matches the classic "opening range extension" pattern: volume confirms the move after the first 30 minutes, not during the spike. That's *more* actionable for scanner design because the scanner has time to fire before the peak.
- **Highest priority for early-entry scanner design.** The volume signal is early and the move hasn't fully resolved.

---

**MIDDAY_BUILDUP (319, 16.6%) — Legitimate momentum cluster, underappreciated**

- Peak volume 11:00-13:00, peak price 12:00. Median $vol $20.7M — this is real liquidity.
- This profile matches accumulation into lunch — either a continuation after a morning base or a catalyst that hits mid-session.
- At $3.01 median price, this is the bottom of the tradeable-with-meaningful-size zone.
- **Second priority.** The build pattern means a scanner can catch the early volume anomaly before the price peak. Most scanners are tuned for open — this cluster is systematically under-served.

---

**AFTERNOON_SURGE (463, 24.1%) — Treat as suspected artefact, but do not discard**

- 58% of volume in the final 10-min bucket. Median $vol $66.6M — 3x any other cluster. Median price $3.50.
- The 58% in the final bucket is the key flag. This pattern is consistent with MOC (market-on-close) order imbalances, ETF rebalancing, or index reconstitution events. These are structural, not organic momentum.
- **However:** 463 ticker-days is the second-largest cluster. If even 30% of these are genuine momentum moves that happen to also attract MOC flow (because the stock ran hard all day), the signal is real — the MOC volume is *additive*, not *causal*.
- **Action required before dismissing:** Segment by whether these names appear in any major ETF or index. If the high-$vol names (>$10M $vol) are concentrated in index components or heavily-ETF-tracked names, that confirms artefact. If they're small-caps with no index presence, the MOC flag is overstated.
- **Do not discard. Audit required.**

---

**MULTI_SPIKE (512, 26.6%) — Most complex, potentially most valuable**

- Largest cluster. Two or more spikes separated by >10 buckets. Peak price 13:10. Median $vol $22.8M.
- This is the profile of a stock that gets *multiple* catalysts or waves of buying in a single day. That's not noise — it's a specific market microstructure: initial spike, profit-taking, secondary confirmation.
- For scanner design: the *second* spike is the actionable entry. After the first spike, the stock is on the scanner's radar. The second spike is the confirmation that the move is continuing, not exhausting.
- This connects directly to our existing skip-first filter (+75.2pp improvement, EXP-022). MULTI_SPIKE may be the *universe* for which skip-first was always the correct design.
- **High priority — strong connection to confirmed edge.**

---

**EVEN_DIST (407, 21.2%) — Underrated, potentially the cleanest for systematic entry**

- No single period dominates. 81% first-half volume. Peak price 11:00. Median $vol $20.7M.
- This is the profile of a stock that trends steadily, without a single spike. 81% first-half volume means buying pressure is front-loaded but distributed — not a violent open, not a late surge.
- For scanner design: this is the grinder profile. Consistent volume + consistent price appreciation. Entry anywhere in the first half captures meaningful upside.
- **Direct connection to IDEA-016/HYP-025 grinder concept.** This cluster may be the empirical description of what the grinder entry was designed to catch.
- **Third priority — but critical for validating the grinder hypothesis.**

---

### Prioritised Recommendations

**Priority 1 — MULTI_SPIKE × skip-first validation**
Run a frequency analysis: what fraction of MULTI_SPIKE ticker-days would have been caught by the skip-first filter as currently designed? If the answer is >60%, MULTI_SPIKE is the empirical validation of EXP-022's mechanism. This is the highest-value data cut available right now.

**Priority 2 — AFTERNOON_SURGE artefact audit**
Cross-reference AFTERNOON_SURGE tickers against ETF/index membership. Split the 463 into "index-tracked" vs "not index-tracked." If the $66.6M median $vol is driven entirely by index names, the cluster is mechanical. If it holds in non-index names, there's a real signal here worth pursuing.

**Priority 3 — EVEN_DIST × grinder entry alignment**
Check whether EVEN_DIST ticker-days disproportionately match the grinder entry criteria (EMA gap 1.0%+ above VWAP at the time of scanner fire). This would confirm or deny whether EVEN_DIST is the empirical cluster the grinder strategy was targeting.

**Priority 4 — MORNING_FRONT scanner timing window**
For MORNING_FRONT: what is the distribution of the volume concentration *within* the first hour? Is it front-half (09:30-09:45) or back-half (09:45-10:00)? If back-half, a scanner firing at 09:45 could systematically catch this cluster before peak price at 10:00. That's a concrete scanner design parameter.

**Priority 5 — EARLY_SPIKE + MORNING_FRONT liquidity floor**
These clusters are thin. Before any scanner work, establish the minimum $vol threshold that keeps a tradeable subset. Filter to $vol ≥ $1M and recount. If MORNING_FRONT holds even 30-40 names above that threshold, it's worth a dedicated scanner.

---

### What I Am Not Prepared to Concede

- **AFTERNOON_SURGE is not automatically discarded.** The artefact hypothesis is a hypothesis, not a finding. It requires a test.
- **EARLY_SPIKE and MORNING_FRONT are not dead ends.** They are size-constrained, not untradeble. The right response is a liquidity floor, not elimination.
- **EVEN_DIST is not "no pattern."** Even distribution with first-half front-loading is a *specific* and *rare* profile. It deserves the same analytical rigour as the spike clusters.

---

> **FLAG FOR CONTEXT:** MULTI_SPIKE cluster (512 ticker-days, 26.6%) shows strong structural alignment with skip-first filter logic (EXP-022, +75.2pp). Hypothesis: MULTI_SPIKE is the empirical universe for which skip-first was the correct design. Requires frequency analysis to confirm. If confirmed, this becomes the primary cluster for scanner optimisation.

> **FLAG FOR CONTEXT:** EVEN_DIST cluster (407 ticker-days, 21.2%) shows profile consistent with grinder trade concept (IDEA-016/HYP-025) — distributed volume, first-half front-loaded, no single spike. Hypothesis: EVEN_DIST is the empirical description of the grinder universe. Requires cross-check against grinder entry criteria (EMA gap 1.0%+ above VWAP).

> **FLAG FOR CONTEXT:** AFTERNOON_SURGE artefact claim is unconfirmed. 58% final-bucket volume is consistent with MOC flows but not proven to be caused by them. Required test: split by ETF/index membership. Do not discard cluster until test is run.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-014 — Handoff to Challenger

Good structured assessment from Optimist. Now routing to Challenger for methodology audit and evidence demands.

Challenger — your turn. Full data context and Optimist's assessment below.

**Your task:** Audit the methodology and Optimist's claims. Demand evidence where claims outrun the data. Check for lookahead bias and structural flaws. Be specific — what holds up, what doesn't, what needs to be tested before any of this is actionable?

---

**DATA CONTEXT PACKAGE:**

**Population:** 1,922 ticker-days where (HOD-LOD)/LOD ≥ 100% across ALL bars (incl. pre/post market). 1,056 unique tickers. May 2025–Mar 2026. 110,240 total ticker-days scanned = 1.7% qualify.

**Range distribution:** 100-200%: 1,366 (71%) · 200-500%: 458 (24%) · 500-1000%: 82 (4%) · 1000%+: 33 (2%)

**Six clusters:**
1. EARLY_SPIKE (114, 5.9%): >50% vol in first 30 min. Med range 140%, med $vol $344K, med price $1.85. Peak price 09:40.
2. MORNING_FRONT (107, 5.6%): First hour >60% vol, not concentrated in first 30 min. Med range 145%, med $vol $524K, med price $2.08. Peak price 10:00.
3. MIDDAY_BUILDUP (319, 16.6%): Peak vol bucket 11:00-13:00. Med range 140%, med $vol $20.7M, med price $3.01. Peak price 12:00.
4. AFTERNOON_SURGE (463, 24.1%): >40% vol in last hour, 58% in final 10-min bucket. Med range 154%, med $vol $66.6M, med price $3.50. Peak price 15:50.
5. MULTI_SPIKE (512, 26.6%): 2+ spikes separated by >10 buckets. Med range 150%, med $vol $22.8M, med price $3.01. Peak price 13:10.
6. EVEN_DIST (407, 21.2%): No single period dominates, 81% first-half vol. Med range 151%, med $vol $20.7M, med price $3.25. Peak price 11:00.

**Key flags:** AFTERNOON_SURGE has 58% volume in final 10-min bucket — possible MOC artefact. EARLY_SPIKE/MORNING_FRONT are thin sub-$1 names (med $vol $344K / $524K). AFTERNOON_SURGE has 3x dollar volume of any other cluster ($66.6M median).

---

**Optimist's key claims (audit these):**

1. MORNING_FRONT is "most structurally clean" and "highest priority for early-entry scanner design" — scanner has time to fire before peak price at 10:00
2. MULTI_SPIKE connects to skip-first filter (EXP-022) — "MULTI_SPIKE may be the universe for which skip-first was always the correct design"
3. AFTERNOON_SURGE artefact claim "is a hypothesis, not a finding" — requires ETF/index membership test before dismissal
4. EVEN_DIST = grinder profile — "empirical description of what the grinder entry was designed to catch"
5. MIDDAY_BUILDUP is "second priority" — liquidity and timing make it actionable
6. EARLY_SPIKE and MORNING_FRONT are "size-constrained, not untradeable" — a liquidity floor (≥$1M $vol) would keep a tradeable subset

[NEXT: challenger]

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## Challenger Audit — LC-2025-014

### Evidence Received

- Descriptive statistics for 1,922 ticker-days across 6 clusters
- Cluster definitions (volume concentration rules)
- Median price, median $vol, median range, peak price time per cluster
- Population qualification rule: (HOD-LOD)/LOD ≥ 100% across ALL bars including pre/post market
- Optimist's interpretive claims connecting clusters to prior experiments (EXP-022, IDEA-016/HYP-025)

### Lookahead Bias Check

**This is a descriptive clustering exercise, not a backtest. However, several structural lookahead questions must be answered:**

**FINDING 1 — Population selection uses full-day outcome (HOD-LOD ≥ 100%)**
The qualification rule requires the full day's HOD and LOD to be known. This means **every ticker-day in this dataset was selected because it achieved a 100%+ intraday range on that day**. The volume profile clustering is performed entirely on a population that was pre-filtered by a full-day outcome.

This is not a lookahead bias in the backtest sense — but it is a **survivorship-selection bias** that is critical to every actionability claim made by Optimist. A scanner fires *during* the day. At scanner fire time, the full-day HOD/LOD is not known. Therefore:

> **The base rate question is unanswered:** Of all days a stock showed the MORNING_FRONT volume profile through, say, 09:45, what fraction went on to achieve 100%+ range? That denominator is missing entirely from this dataset.

Every "actionability" claim rests on this missing denominator. Without it, we are describing what 100%+ movers looked like in hindsight, not what signals predict them going forward.

**FINDING 2 — Peak price time is a full-day metric**
"Peak price 09:40" for EARLY_SPIKE, "Peak price 10:00" for MORNING_FRONT — these are determined using the full trading day's price series. At 09:35, you do not know whether 09:40 will be the peak. Optimist's claim that "the scanner has time to fire before the peak at 10:00" implicitly treats the peak time as knowable. It is not. It is a backward-looking summary statistic.

**Lookahead Bias Status: Not a backtest flaw (no backtest is being proposed), but the descriptive statistics are entirely backward-looking. All actionability claims derived from them carry an unquantified forward-prediction gap. This is not blocking for cluster description — it IS blocking for any claim about scanner timing or entry opportunity without the missing base rate data.**

---

### Claim-by-Claim Audit

---

**Claim 1: MORNING_FRONT is "most structurally clean" and "highest priority for early-entry scanner design" — scanner has time to fire before peak price at 10:00**

**Not supported by the evidence provided.**

- "Structurally clean" is undefined. What makes it cleaner than EVEN_DIST? No metric is offered.
- The peak-price-at-10:00 argument is backward-looking (see Finding 2 above). We know these 107 days peaked at 10:00 *on average*. We do not know:
  - What fraction peaked before 09:45 (rendering the scanner too slow)?
  - What fraction peaked before the volume concentration was detectable?
  - What fraction of days showing MORNING_FRONT-style volume through 09:45 went on to peak at 10:00 vs. reversed?
- The "60%+ first-hour volume" criterion: at what intraday timestamp does this criterion become detectable? If 60% of the first-hour volume arrives in the *last* 15 minutes of that hour, the scanner cannot fire before the peak.
- 107 ticker-days. This is the second-smallest cluster. Any scanner recommendation based on 107 examples without a forward base rate is speculative.

**Required evidence before accepting:** Distribution of peak price times within MORNING_FRONT (not just median). Volume arrival curve within the first hour — when does the 60% threshold become detectable intraday? Base rate: how many days show early-morning volume concentration but do NOT achieve 100%+ range?

---

**Claim 2: MULTI_SPIKE connects to EXP-022 skip-first — "may be the universe for which skip-first was always the correct design"**

**Speculative. The connection is asserted, not demonstrated.**

- EXP-022 skip-first filter result (+75.2pp) came from a specific tested universe. That universe is not defined in the data provided here. Is it the same population as this clustering exercise? We don't know.
- MULTI_SPIKE is defined as "2+ spikes separated by >10 buckets." What is a "bucket"? If buckets are 10-minute bars, ">10 buckets" = >100 minutes. That means spikes must be separated by at least 1h40m. Does EXP-022's skip-first logic operate on this timescale? We don't know.
- "Skip-first" means skipping the *first* entry signal and waiting for confirmation. MULTI_SPIKE means there *were* multiple spikes. These are not the same thing. A stock with 3 volume spikes may have had its price peak on the first spike — in which case skip-first would have *missed* the move, not caught it.
- The 512 count is the largest cluster. Large cluster + intuitive-sounding connection to a prior finding is exactly the kind of pattern that produces false confirmations.

**Required evidence before accepting:** (1) Define "bucket" precisely. (2) Show the price trajectory within MULTI_SPIKE days — does price continue rising into the second spike, or does it peak on the first? (3) Show the EXP-022 tested universe and confirm it overlaps meaningfully with this population.

---

**Claim 3: AFTERNOON_SURGE artefact claim "is a hypothesis, not a finding"**

**Partially correct framing, but Optimist's alternative hypothesis is also unsubstantiated.**

- Optimist argues that 30% of AFTERNOON_SURGE could be genuine momentum with MOC flow being *additive*. This is possible but equally undemonstrated.
- The 58% final-10-minute concentration is extreme. For context: a uniform distribution across 78 ten-minute bars would allocate ~1.3% per bucket. 58% in one bucket is 44x the uniform rate. That is not "some MOC flow on top of momentum" — that is a dominant structural force.
- Median $vol of $66.6M is 3x the next cluster. This concentration of dollar volume in one cluster should be explained, not assumed away.
- Optimist's proposed test (ETF/index membership) is reasonable but incomplete. Many non-index small-caps also attract MOC flows on high-volume days via index-tracking ETFs that rebalance based on market cap thresholds.
- **Additional disqualifying concern:** Peak price at 15:50 is 10 minutes before close. A scanner firing at 15:50 based on volume surge is entering at or near the close. The entry price, exit price, and hold time for this cluster are entirely undefined. At $66.6M median $vol, this might be a large-cap anomaly — but the median price is only $3.50, which means the share volume is enormous. What is driving this?

**Required evidence before accepting the "not artefact" position:** Show the price trajectory within AFTERNOON_SURGE days. Does price peak at 15:50 or earlier? If price peaks at 15:50, this is entirely driven by the final-bucket volume — which is almost certainly MOC/structural. Show the distribution of market caps and ETF membership in this cluster.

---

**Claim 4: EVEN_DIST = grinder profile**

**Asserted without cross-referencing the actual grinder criteria.**

- IDEA-016/HYP-025 grinder concept has specific entry criteria — EMA gap 1.0%+ above VWAP is cited by Optimist. None of the cluster statistics (median range, $vol, price, peak time) map directly to that criterion.
- "81% first-half volume" and "no single period dominates" are *necessary* conditions for a grinder but not *sufficient*. A stock that gaps up 5% at open and then trades sideways with distributed volume would satisfy these criteria — that is not a grinder momentum trade.
- "Even distribution with first-half front-loading is a specific and rare profile" — 407 ticker-days = 21.2% of the sample. That is the third-largest cluster. It is not rare within this population.
- The EMA gap condition requires VWAP data at the time of scanner fire. None of the cluster statistics include VWAP relationship data.

**Required evidence before accepting:** (1) Apply the actual grinder entry criteria to EVEN_DIST days and show what fraction pass. (2) Show the intraday price trajectory for EVEN_DIST — is it a sustained uptrend (grinder) or a flat/whipsaw day with distributed volume?

---

**Claim 5: MIDDAY_BUILDUP is "second priority" — liquidity and timing make it actionable**

**Weakly supported. The timing argument has a gap.**

- $20.7M median $vol is genuine liquidity — this is the strongest part of the claim and I accept it.
- "A scanner can catch the early volume anomaly before the price peak at 12:00" — this requires that the volume anomaly is detectable before 12:00. If the peak volume bucket is 11:00-13:00, the volume anomaly may not become statistically distinguishable from normal trading until 11:30 or later. Peak price at 12:00 means the entry window is narrow.
- "Most scanners are tuned for the open — this cluster is systematically under-served" — this is an opinion, not a finding. It may be correct, but it's presented as a competitive advantage claim without evidence of what other scanners do.

**Required evidence before accepting second-priority ranking:** Show the volume arrival curve within the 11:00-13:00 window. At what point does MIDDAY_BUILDUP volume become anomalous relative to baseline? How wide is the entry window before the 12:00 price peak?

---

**Claim 6: EARLY_SPIKE and MORNING_FRONT are "size-constrained, not untradeable" — $1M $vol floor keeps a tradeable subset**

**The $1M threshold is invented without justification.**

- Median $vol for EARLY_SPIKE is $344K. Median for MORNING_FRONT is $524K. These are medians — meaning at least 50% of ticker-days in these clusters are below these figures.
- A $1M floor on a distribution where the median is $344K and $524K respectively would eliminate well over 50% of each cluster. The remaining subset could be as small as 20-30 ticker-days.
- No distribution data is provided (e.g., 75th/90th percentile $vol). The claim that a $1M floor "keeps a tradeable subset" is asserted without any data on what survives.
- Additionally: $1M $vol at $1.85 median price = ~540,000 shares traded. Bid-ask spread on sub-$2 stocks is structurally wide (known from prior sessions: 1-5%). Slippage on entry/exit at meaningful size would materially erode any edge.

**Required evidence before accepting:** Show the $vol percentile distribution for EARLY_SPIKE and MORNING_FRONT. How many ticker-days survive a $1M floor? A $2M floor? What is the 75th percentile $vol for each?

---

### Structural Issues Not Raised by Optimist

**Issue A — Cluster boundary stability is unknown**
The six clusters are defined by volume concentration rules (e.g., ">50% vol in first 30 min"). These are threshold-based, not data-derived (no k-means or hierarchical clustering mentioned). What happens to a ticker-day that has 49% vol in the first 30 min? It falls into a different cluster. The sensitivity of cluster membership to threshold choice is unexamined. Cluster counts could shift materially with small rule changes.

**Issue B — 1,056 unique tickers in 1,922 ticker-days means average ~1.8 days per ticker**
This means many tickers appear in multiple clusters on different days. A single ticker could appear in EARLY_SPIKE on one day and MULTI_SPIKE on another. This is not a flaw in itself, but it means the clusters are not describing *types of stocks* — they are describing *types of days*. Scanner design implications are very different: you cannot select a stock based on its cluster membership because the membership is day-specific, not ticker-specific.

**Issue C — Pre/post market volume inclusion**
The HOD/LOD qualification uses "ALL bars (incl. pre/post market)." Are the volume profile clusters built on regular-hours volume only, or do they include pre/post market volume? If pre-market volume is included in the first-bucket calculation, EARLY_SPIKE may be capturing pre-market momentum, not the 09:30 open spike. This materially changes the interpretation and scanner timing.

**Issue D — Cluster sizes and statistical confidence**
EARLY_SPIKE (114) and MORNING_FRONT (107) are thin. Any sub-segmentation (e.g., filtering by $vol ≥ $1M, or splitting by price tier) will produce cells with <30 observations. Statistical conclusions from those subsets would be unreliable.

---

### What Holds Up

- The $vol stratification across clusters is real and meaningful. AFTERNOON_SURGE's $66.6M vs. others' $20M is a genuine structural difference worth understanding.
- The MOC/artefact hypothesis for AFTERNOON_SURGE is well-motivated by the 58% final-bucket concentration. It needs testing, not dismissal — but also not the benefit of the doubt Optimist extends it.
- MIDDAY_BUILDUP and MULTI_SPIKE have adequate sample size (319 and 512) and real liquidity ($20.7M and $22.8M) to support further analysis.
- The request for ETF/index membership audit on AFTERNOON_SURGE is the correct next step.

---

### Summary: What Must Be Answered Before Any Claim Is Actionable

| # | Required Evidence | Blocks Which Claim |
|---|---|---|
| 1 | Forward base rate: what % of days showing each cluster's early-day volume pattern went on to achieve 100%+ range? | ALL actionability claims |
| 2 | MORNING_FRONT intra-hour volume arrival curve — when does the 60% threshold become detectable? | Claim 1 |
| 3 | MULTI_SPIKE price trajectory — does price rise into the 2nd spike or peak at the 1st? | Claim 2 |
| 4 | EXP-022 tested universe — does it overlap with this population? | Claim 2 |
| 5 | AFTERNOON_SURGE price trajectory intraday — does price peak at 15:50 or earlier? | Claim 3 |
| 6 | EVEN_DIST intraday price trajectory — sustained uptrend or flat? | Claim 4 |
| 7 | Fraction of EVEN_DIST days passing actual grinder entry criteria | Claim 4 |
| 8 | $vol percentile distributions for EARLY_SPIKE and MORNING_FRONT | Claim 6 |
| 9 | Clarify: are cluster volume profiles built on regular hours only or including pre/post? | Structural Issue C |
| 10 | Ticker-day overlap across clusters — what % of tickers appear in multiple clusters? | Structural Issue B |

---

**FLAG FOR CONTEXT:** Survivorship-selection bias is the primary methodological issue in LC-2025-014. Every cluster description is derived from a population pre-filtered by full-day outcome (HOD-LOD ≥ 100%). The forward base rate — what fraction of days showing a given intraday volume pattern go on to achieve 100%+ range — is entirely absent from the data package. No actionability claim can be validated without this denominator. This is not a blocking error in the clustering itself, but it is blocking for any scanner design recommendation.

**FLAG FOR CONTEXT:** MULTI_SPIKE–EXP-022 connection is unvalidated. The claimed alignment between MULTI_SPIKE cluster and skip-first filter logic requires: (1) bucket size definition, (2) price trajectory confirmation that second spike follows price continuation (not reversal), (3) confirmation that EXP-022 tested universe overlaps with this population. Do not carry this connection forward as established.

**FLAG FOR CONTEXT:** Cluster boundary stability unexamined. Six clusters are defined by hard threshold rules, not data-derived partitioning. Sensitivity to threshold choice (e.g., 49% vs 50% in first 30 min) is unknown. Cluster membership counts may be unstable.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-014 — Manager Synthesis

Both agents have responded. Strong session — let me synthesise before closing.

**Key findings:**

1. **Survivorship bias is the primary methodological constraint.** Challenger is correct: every cluster was selected by full-day outcome. The forward base rate (what % of days showing early volume pattern go on to achieve 100%+ range) is entirely absent. This blocks all actionability claims until that denominator is established.

2. **AFTERNOON_SURGE is likely a structural artefact.** 58% of volume in the final 10-min bucket is 44x the uniform rate. The "MOC additive" hypothesis is possible but unsupported — the default assumption should be structural until tested. Lowest actionability for scanner design.

3. **MULTI_SPIKE (512) and MIDDAY_BUILDUP (319) have the strongest fundamentals** — adequate sample size, real liquidity, no dominant artefact flag. But both require price trajectory data (does price rise into the 2nd spike? how wide is the pre-12:00 entry window?) before any ranking claim holds.

4. **MORNING_FRONT "highest priority" claim is premature.** 107 ticker-days, missing intra-hour volume arrival curve, and the peak-time argument is backward-looking. Cannot be ranked #1 without forward base rate data.

5. **EVEN_DIST ↔ grinder and MULTI_SPIKE ↔ skip-first connections are hypotheses, not findings.** Both are worth pursuing as falsifiable tests — neither should be carried forward as established.

---

**Flags for PO review:**

- FLAG 1 (Challenger): Forward base rate is the blocking missing data point. All scanner recommendations require: "of days showing pattern X through time T, what % achieve 100%+ by EOD?" This is a data task for the next session.
- FLAG 2 (Challenger): Cluster boundary stability unexamined — threshold-based rules, not data-derived. Sensitivity analysis needed before committing to cluster definitions.
- FLAG 3 (Optimist): MULTI_SPIKE × skip-first connection is a high-priority testable hypothesis — requires price trajectory data and EXP-022 universe overlap check.
- FLAG 4 (Optimist): AFTERNOON_SURGE artefact test (ETF/index membership) is the correct next step before dismissing 463 ticker-days.
- FLAG 5 (Optimist): EVEN_DIST × grinder connection — requires applying actual grinder entry criteria to EVEN_DIST days to confirm or deny.

---

**Final turn — asking each agent for additional flags before close.**

Optimist — one final turn. Given Challenger's audit, is there anything you want to add, retract, or flag for context that isn't already captured above? Data context package repeated below for your reference.

**Population:** 1,922 ticker-days, 6 clusters. EARLY_SPIKE (114), MORNING_FRONT (107), MIDDAY_BUILDUP (319), AFTERNOON_SURGE (463, 58% final-bucket volume, $66.6M median $vol), MULTI_SPIKE (512), EVEN_DIST (407, 81% first-half vol). Key flags: survivorship-selection bias (full-day HOD/LOD used for qualification), forward base rate absent, cluster boundaries are threshold-based not data-derived.

**Challenger's key findings:** (1) Forward base rate missing — blocks all actionability claims. (2) Peak price times are backward-looking — scanner timing arguments invalid without volume arrival curves. (3) MULTI_SPIKE ↔ skip-first connection unvalidated (bucket definition unclear, price trajectory unknown, EXP-022 universe overlap unconfirmed). (4) AFTERNOON_SURGE 58% final-bucket = 44x uniform rate — not "additive MOC," this is structurally dominant. (5) Cluster boundary stability unexamined.

[NEXT: optimist]

---

**Manager:** Session transcript so far.

Optimist, your turn. Respond per protocol.

**Optimist:** Memory updated. My final position is logged.

To summarise what I am adding and retracting at session close:

**Retractions:**
- MORNING_FRONT "highest priority" — withdrawn. Argument depended on backward-looking peak time.
- MULTI_SPIKE ↔ skip-first as an established connection — withdrawn. Remains a hypothesis in good standing only.
- EVEN_DIST ↔ grinder as confirmed — withdrawn. Requires grinder criteria cross-check.
- AFTERNOON_SURGE "not artefact" framing — withdrawn. Default posture revised to likely artefact, disproof required.

**Additions:**
- Cluster-predictability-from-pre-market-conditions as the correct long-run direction for resolving survivorship bias. If cluster assignment is predictable from pre-open data, the full-day outcome filter stops being a methodological blocker.
- All priority rankings suspended pending two blocking items: forward base rate and intra-hour volume arrival curves.

**Nothing carried forward as a finding that wasn't already in prior memory**, with the exception of the revised AFTERNOON_SURGE posture (elevated to likely artefact) and the new cluster-predictability hypothesis.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-014 — Routing to Challenger (Final Turn)

Optimist has cleanly retracted the unsupported claims and added one new hypothesis (cluster predictability from pre-market conditions). Now routing to Challenger for final flags.

Challenger — one final turn. Given the full session, is there anything you want to add, retract, or flag for context that isn't already captured? Specific ask: does the cluster-predictability-from-pre-market hypothesis (Optimist's addition) hold up methodologically, or does it carry its own structural problems?

**Data context package (full):**

**Population:** 1,922 ticker-days, 6 clusters. EARLY_SPIKE (114), MORNING_FRONT (107), MIDDAY_BUILDUP (319), AFTERNOON_SURGE (463, 58% final-bucket volume, $66.6M median $vol), MULTI_SPIKE (512), EVEN_DIST (407, 81% first-half vol). Key flags: survivorship-selection bias (full-day HOD/LOD used for qualification), forward base rate absent, cluster boundaries are threshold-based not data-derived.

**Challenger's prior findings (already captured):**
1. Forward base rate missing — blocks all actionability claims
2. Peak price times are backward-looking — scanner timing arguments invalid without volume arrival curves
3. MULTI_SPIKE ↔ skip-first connection unvalidated
4. AFTERNOON_SURGE 58% final-bucket = 44x uniform rate — structurally dominant, not additive MOC
5. Cluster boundary stability unexamined
6. Pre/post market volume inclusion in cluster definitions — unresolved
7. Average 1.8 days per ticker — clusters describe *days*, not *stocks*

**Optimist's final-turn addition:** If cluster assignment is predictable from pre-open data (e.g., gap-up size, pre-market volume), the full-day outcome filter stops being a methodological blocker — because the scanner can use pre-open signals without knowing the full-day outcome. Assess this hypothesis.

[NEXT: challenger]

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## Challenger Final Turn — LC-2025-014

### Evidence Received

- Full session transcript including Optimist's initial assessment, Challenger's prior audit, Manager synthesis, Optimist's retractions and additions
- Descriptive statistics for 1,922 ticker-days across 6 clusters (unchanged)
- Optimist's new hypothesis: cluster assignment is predictable from pre-open data → resolves survivorship bias as methodological blocker

---

### Lookahead Bias Check — Final Session Status

**Descriptive clustering exercise only. No backtest proposed this session.**

The survivorship-selection bias remains the dominant structural issue — confirmed and carried forward. No new lookahead bias introduced this session.

**Optimist's new hypothesis requires a separate lookahead check** (see below).

**Status: Not blocking for the clustering description itself. Remains blocking for all actionability claims. No change from prior finding.**

---

### Assessment of the Cluster-Predictability-from-Pre-Market Hypothesis

Optimist's argument: if cluster membership can be predicted from pre-open data (gap-up size, pre-market volume), then the scanner can fire on pre-open signals without requiring full-day outcome knowledge — and the survivorship bias stops being a methodological blocker.

This is a structurally interesting argument. I will assess it precisely.

---

**Step 1: Does predictability of cluster membership resolve the survivorship bias? No — it shifts it.**

The survivorship bias in this dataset is: **every ticker-day in the population achieved 100%+ intraday range.** If pre-open data predicts cluster membership, you still only know which cluster a 100%+ mover will belong to — you do not know whether the stock will be a 100%+ mover at all.

The missing denominator remains: **of all stocks showing pre-open signal X, what fraction go on to achieve 100%+ range?** Predicting cluster membership within the 100%+ population does not answer that question. It only adds a second-level prediction (cluster assignment) on top of the still-unanswered first-level prediction (100%+ qualification).

Formally: the hypothesis resolves within-population cluster assignment uncertainty. It does not resolve population membership uncertainty. The scanner must solve population membership first.

---

**Step 2: Does the hypothesis introduce a new lookahead risk?**

Yes — and this is important.

If the cluster-predictability model is trained on this dataset (1,922 ticker-days, all pre-selected by full-day outcome), the model learns to predict cluster assignment from pre-open features *conditional on the stock having already achieved 100%+ range*. The pre-open features in this dataset are not a random sample of pre-open features in the market — they are the pre-open features of stocks that happened to move 100%+.

This means:
- Pre-market gap size in this dataset is the gap size distribution *among 100%+ movers* — not the full population gap size distribution
- Pre-market volume in this dataset is the volume distribution *among 100%+ movers* — not the full population

A predictability model trained here would overfit to the characteristics of winners. Applied in production, it would generate false signals on stocks showing similar pre-open characteristics that do not go on to achieve 100%+ range.

**This is a selection-conditional feature distribution problem.** The features look predictive in the training set because the training set was selected by outcome. This is a known failure mode — flagged in memory as "design-subset contamination" and "threshold selection from outcome buckets."

---

**Step 3: Is the hypothesis falsifiable in a useful way?**

Yes — but only with the correct experimental design. The test is:

1. Take all ticker-days in the full 110,240-day scanned universe (not just the 1,922 qualifiers)
2. Extract pre-open features for each day (gap size, pre-market volume, etc.)
3. Train a cluster-assignment model on the 1,922 qualifiers
4. Apply to the full 110,240 and measure: (a) what fraction of predicted-MORNING_FRONT days actually achieve 100%+ range? (b) what fraction of predicted-MULTI_SPIKE days achieve 100%+?
5. That gives the forward base rate per cluster — which is the missing denominator

This design is valid **only if** the model is trained on a held-out subset of the 1,922 and tested on a different subset. If the full 1,922 is used for both training and testing cluster assignment, the results are in-sample and meaningless.

**The hypothesis is not methodologically broken — but it requires the correct experimental design to avoid converting a selection bias problem into a model overfitting problem.**

---

**Step 4: Practical feasibility concern**

The hypothesis assumes pre-open features (gap size, pre-market volume) have sufficient discriminating power to separate clusters. There is no evidence for this in the current data package. Consider:

- EARLY_SPIKE vs. MORNING_FRONT: both are early-hours clusters, both thin, both sub-$2. Their distinction is *within* the first hour — can pre-open data distinguish these reliably?
- MIDDAY_BUILDUP vs. MULTI_SPIKE: peak volume occurs 11:00+ and 13:10 respectively. Pre-open signals may have very low predictive power for which pattern emerges 3-5 hours later.
- AFTERNOON_SURGE: if this is a structural/MOC artefact, it may be perfectly unpredictable from pre-open data by design — MOC flows are not a function of the opening gap.

There is no a priori reason to expect that pre-open features are informative about which *intraday* volume pattern emerges. The hypothesis is plausible for early clusters (EARLY_SPIKE, MORNING_FRONT) and implausible for late clusters (AFTERNOON_SURGE, MIDDAY_BUILDUP).

---

### Structured Assessment of Hypothesis Validity

| Dimension | Assessment |
|---|---|
| Does it resolve survivorship bias? | **No.** Resolves within-population cluster assignment only. Population membership question remains open. |
| Does it introduce new lookahead/selection risk? | **Yes.** Features in this dataset are drawn from the 100%+ survivor population. Model trained here will overfit to winner characteristics. |
| Is it falsifiable? | **Yes**, with correct design: train on held-out subset, apply to full 110,240, measure forward base rate per cluster. |
| Is it plausible for early clusters? | **Plausible.** Pre-open gap + volume may correlate with EARLY_SPIKE/MORNING_FRONT assignment. |
| Is it plausible for late clusters? | **Weak.** MIDDAY_BUILDUP, AFTERNOON_SURGE patterns emerge hours after open. Pre-open signal is temporally distant. |
| Ready to carry forward as a hypothesis? | **Conditionally yes**, but must be framed as: "pre-open features may predict cluster assignment *within the 100%+ population*, which is a necessary but not sufficient condition for scanner utility." |

---

### Additions to Prior Flags

Everything from my prior audit stands unchanged. Adding:

**FLAG FOR CONTEXT:** Cluster-predictability-from-pre-market hypothesis does NOT resolve survivorship bias — it only addresses within-population cluster assignment. The forward base rate (what % of all scanned days showing pre-open pattern X achieve 100%+ range) remains the blocking missing data point. A predictability model trained on the 1,922-day survivor population will overfit to winner characteristics if applied directly to the full 110,240-day universe. Correct experimental design: train on held-out subset of 1,922, apply to full 110,240, measure 100%+ qualification rate by predicted cluster. This is the only design that yields a valid forward base rate.

**FLAG FOR CONTEXT:** Cluster-predictability plausibility is asymmetric by cluster. Pre-open signals are plausible predictors for EARLY_SPIKE and MORNING_FRONT (early pattern, temporally close to pre-open). They are weak predictors for MIDDAY_BUILDUP, MULTI_SPIKE, and AFTERNOON_SURGE (patterns emerge 2-6 hours after open). AFTERNOON_SURGE in particular may be structurally unpredictable from pre-open data if driven by MOC flows.

---

### Session Close Summary

**What this session established (findings):**
1. Six cluster descriptions are valid as backward-looking summaries of 100%+ mover volume profiles
2. AFTERNOON_SURGE is the default-artefact cluster — 44x uniform concentration in final bucket, requires disproof not proof
3. MULTI_SPIKE and MIDDAY_BUILDUP have adequate sample and liquidity for further analysis
4. All priority rankings and actionability claims are suspended pending forward base rate data

**What this session did not establish (hypotheses only):**
1. MULTI_SPIKE ↔ skip-first connection
2. EVEN_DIST ↔ grinder connection
3. Cluster-predictability-from-pre-market as survivorship bias solution
4. Any scanner timing recommendation

**One blocking data task required before session findings become actionable:**
> Of all 110,240 scanned ticker-days, extract those showing each cluster's defining volume pattern through intraday timestamp T (T < peak price time). Compute 100%+ qualification rate for each cluster. This is the forward base rate. Without it, cluster descriptions are historically interesting and strategically inert.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-014 — Session Close

Both agents have completed their final turns. Challenger's assessment of the cluster-predictability hypothesis is thorough and conclusive. Proceeding to close.

---

### Session Minutes — LC-2025-014

**Question asked:** What are the consistent volume profile patterns among 100%+ intraday movers, and which are most actionable for scanner design?

**Key contributions:**

- **Optimist:** Structured cluster-by-cluster interpretation. Prioritised MORNING_FRONT, MULTI_SPIKE, and MIDDAY_BUILDUP. Proposed testable connections: MULTI_SPIKE ↔ skip-first (EXP-022), EVEN_DIST ↔ grinder (IDEA-016). Identified AFTERNOON_SURGE as suspect. Cleanly retracted all unsupported priority claims when challenged. Added cluster-predictability-from-pre-market hypothesis as a path to resolving survivorship bias.
- **Challenger:** Identified survivorship-selection bias as the primary structural constraint — every cluster description is derived from a population pre-filtered by full-day outcome. Demonstrated that peak-price-time arguments are backward-looking. Audited all six Optimist claims systematically, finding none actionable without forward base rate data. Assessed the cluster-predictability hypothesis: does not resolve survivorship bias (only addresses within-population cluster assignment), introduces selection-conditional feature distribution risk if trained on the survivor population without proper hold-out design.

**Decision/outcome:**

- Six cluster descriptions are valid as backward-looking summaries — no dispute
- AFTERNOON_SURGE elevated to **default artefact** — 44x uniform concentration, disproof required before any scanner use
- MULTI_SPIKE and MIDDAY_BUILDUP are the **strongest candidates** for further analysis (adequate sample, real liquidity, no dominant artefact flag)
- All priority rankings and scanner timing claims are **suspended** — blocked by missing forward base rate
- MULTI_SPIKE ↔ skip-first and EVEN_DIST ↔ grinder remain **hypotheses only** — not findings
- Cluster-predictability hypothesis is **conditionally valid** but requires correct experimental design (hold-out training + full 110,240-day test universe); does not resolve population membership question

**Blocking data task (one):**
> For each cluster, extract all ticker-days in the full 110,240-day universe showing the cluster's defining volume pattern through intraday timestamp T (where T < median peak price time for that cluster). Compute the 100%+ qualification rate. This yields the forward base rate per cluster — the single data point that makes all cluster findings actionable.

**Next action:** PO review. Propose this as the agenda task for LC-2025-015.

---

### Flags for PO Review

| # | Source | Flag |
|---|---|---|
| F1 | Challenger | **Blocking.** Forward base rate is absent. All scanner recommendations require: "of days showing pattern X through time T, what % achieve 100%+ by EOD?" Must be computed before any cluster is acted upon. |
| F2 | Challenger | Cluster boundary stability unexamined — threshold-based rules, not data-derived. Sensitivity analysis needed before committing to cluster definitions. |
| F3 | Challenger | Cluster-predictability hypothesis does not resolve survivorship bias — only addresses within-population cluster assignment. If used for modelling, requires hold-out design + application to full 110,240-day universe to yield valid forward base rate. |
| F4 | Challenger | Pre/post market volume inclusion in cluster definitions is unresolved. If pre-market volume is included in first-bucket calculation, EARLY_SPIKE interpretation changes materially. |
| F5 | Optimist | MULTI_SPIKE × skip-first is a high-priority testable hypothesis — requires (1) bucket definition, (2) price trajectory confirmation that second spike follows continuation not reversal, (3) EXP-022 universe overlap check. |
| F6 | Optimist | AFTERNOON_SURGE artefact test (ETF/index membership + price trajectory) is the correct next step before dismissing 463 ticker-days. |
| F7 | Optimist | EVEN_DIST × grinder — requires applying actual grinder entry criteria to EVEN_DIST days to confirm or deny. |

---

### Memory Update (pending PO approval)

---
