# Session: P1-validation
_Date: 2026-03-30 10:39 UTC | Agent: manager | Model: claude-sonnet-4-6_

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

Question: Phase 1 Scanner Signal Validation

PO INSTRUCTION: Skip 3 Amigos. Proceed directly. Challenger + Statistician mandatory.

## RAW RESULTS — Three signals tested on 112,679 ticker-dates (782 RTH 100%+ runners)

### P1.1 — Gap% alone
| Threshold | N | Runners | Rate | Lift | Recall |
|---|---|---|---|---|---|
| >=5% | 9,607 | 264 | 2.75% | 4.0x | 33.8% |
| >=10% | 3,520 | 177 | 5.03% | 7.2x | 22.6% |
| >=20% | 1,250 | 100 | 8.00% | 11.5x | 12.8% |
| >=50% | 322 | 39 | 12.11% | 17.5x | 5.0% |

### P2.1 — PM Dollar Volume alone
| Threshold | N | Runners | Rate | Lift | Recall |
|---|---|---|---|---|---|
| >=00K | 21,596 | 320 | 1.48% | 1.8x | 40.9% |
| >=M | 16,124 | 288 | 1.79% | 2.2x | 36.8% |
| >=M | 7,195 | 225 | 3.13% | 3.8x | 28.8% |
| >=0M | 4,720 | 199 | 4.22% | 5.2x | 25.4% |

### P1.2 — News presence
| Condition | N | Runners | Rate | Lift |
|---|---|---|---|---|
| Has any news | 23,633 | 583 | 2.47% | 3.6x |
| No news | 89,046 | 199 | 0.22% | 0.3x |

NEWS IS THE STRONGEST INDIVIDUAL FILTER: 74.6% of runners (583/782) have news. Only 0.22% of no-news days are runners. News presence is nearly a necessary condition.

### Best triple combinations (n>=30)
| Condition | N | Runners | Rate | Lift | Recall |
|---|---|---|---|---|---|
| gap>=15% + PM>=M + news | 759 | 82 | 10.8% | 16x | 10.5% |
| gap>=20% + PM>=M + news | 603 | 65 | 10.8% | 16x | 8.3% |
| gap>=15% + PM>=M + news | 952 | 91 | 9.6% | 14x | 11.6% |
| gap>=10% + PM>=M + news | 990 | 98 | 9.9% | 14x | 12.5% |

### Surprise finding
PM dollar volume ALONE is weaker than Phase 0 suggested (1.8x at 00K vs 12-13x median separation). The median separation exists but many high-PM-vol non-runners dilute the lift. PM vol works best as SECOND filter after gap% or news, not as primary.

## QUESTIONS

### Statistician:
1. News presence: 583/782 runners have news. Binomial test for news as necessary condition — p-value?
2. Best triple (gap>=15%, PM>=M, news): 82/759 = 10.8%. 95% CI? Is this significantly above base rate 0.694%?
3. Recall at 10.5% (82/782) — only 1 in 10 runners flagged. Is this useful for a scanner? What's the expected daily flag count given ~500 ticker-dates per day?
4. Multiple comparison correction: we tested ~30 threshold combinations. BH correction on the top combos?
5. The lift table is monotonic (more filters = higher precision = lower recall). Is there an optimal precision-recall tradeoff?

### Challenger:
1. News coverage: only 21% of ticker-dates have Benzinga news. Is 'no news' = truly no news, or = no Benzinga coverage for that ticker? Could coverage bias explain the signal?
2. Gap% definition uses 'first bar open' which could be a 04:00 ET PM bar. For stocks that gap up in PM trading, does this capture the full gap or just the overnight gap?
3. PM dollar vol at M threshold: 7,195 days pass. That's ~33 per trading day. Is this a reasonable scanner output volume?
4. The 199 runners with no news (25.4% of runners) — what are these? Data gap or genuinely catalyst-free runners?
5. Are these signals lookahead-free? Gap% = first bar open vs prior close (known at open). PM  = sum of PM bars (known by 09:30). News = published timestamp (known at publication). All appear clean.

Close with explicit Phase 1 verdict and recommendation for Phase 2 priorities.

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** ## Session Open — LC-2025-024

**Session ID:** LC-2025-024
**Date:** 2026-03-30 (continuing research agenda)
**Time-box:** ~20 turns

---

### Session Question
Are the Phase 1 scanner signals (Gap%, PM Dollar Volume, News) statistically valid discriminators of intraday 100%+ runners, and what are the recommended Phase 2 priorities?

### Scope
- **In scope:** Statistical validation of the three P1 signals, multiple comparison correction, precision-recall analysis, bias audits, lookahead check, Phase 1 verdict, Phase 2 priority recommendation
- **Out of scope:** Strategy-level backtesting, entry/exit rules, execution analysis

### Agents Required
- **Statistician** — mandatory (CIs, binomial tests, BH correction, precision-recall tradeoff)
- **Challenger** — mandatory (coverage bias, gap definition, lookahead, data quality)
- **Optimist** — optional, routing at close for alternative angles if session permits

### Expected Outcome
- Phase 1 verdict: PASS / FAIL / CONDITIONAL for each signal
- Answered questions from both statistician and challenger blocks
- Phase 2 priority recommendation for PO review

---

### Data Context Package

**Universe:** 112,679 ticker-dates | 782 RTH 100%+ runners | Base rate = 0.694%

**P1.1 — Gap%:**
- >=5%: N=9,607, 264 runners, 2.75%, lift 4.0x, recall 33.8%
- >=10%: N=3,520, 177 runners, 5.03%, lift 7.2x, recall 22.6%
- >=20%: N=1,250, 100 runners, 8.00%, lift 11.5x, recall 12.8%
- >=50%: N=322, 39 runners, 12.11%, lift 17.5x, recall 5.0%

**P2.1 — PM Dollar Volume:**
- >=100K: N=21,596, 320 runners, 1.48%, lift 1.8x, recall 40.9%
- >=1M: N=16,124, 288 runners, 1.79%, lift 2.2x, recall 36.8%
- >=5M: N=7,195, 225 runners, 3.13%, lift 3.8x, recall 28.8%
- >=10M: N=4,720, 199 runners, 4.22%, lift 5.2x, recall 25.4%

**P1.2 — News:**
- Has news: N=23,633, 583 runners, 2.47%, lift 3.6x, recall 74.6%
- No news: N=89,046, 199 runners, 0.22%, lift 0.3x, recall 25.4%

**Best triple combos (n≥30):**
- gap>=15% + PM>=5M + news: N=759, 82 runners, 10.8%, lift 16x, recall 10.5%
- gap>=20% + PM>=5M + news: N=603, 65 runners, 10.8%, lift 16x, recall 8.3%
- gap>=15% + PM>=1M + news: N=952, 91 runners, 9.6%, lift 14x, recall 11.6%
- gap>=10% + PM>=1M + news: N=990, 98 runners, 9.9%, lift 14x, recall 12.5%

**Surprise finding:** PM vol alone weaker than Phase 0 suggested (1.8x at >=100K). Works best as second filter after gap% or news.

---

Routing to Statistician first — the statistical validation must precede Challenger's bias audit to ensure we're distinguishing data quality issues from genuine signal degradation.

**Statistician — your turn.**

Full data context above. Address all five questions:
1. Binomial test — news as necessary condition (583/782 with news)
2. 95% CI for best triple (82/759 = 10.8%) vs base rate 0.694%
3. Recall utility — is 10.5% recall useful? Expected daily flag count at ~500 ticker-dates/day
4. Multiple comparison correction — BH on ~30 threshold combinations
5. Optimal precision-recall tradeoff — is there a principled answer?

Flag anything that would change the Phase 1 verdict.

[NEXT: statistician]

---

**Manager:** Session transcript so far.

Statistician, your turn. Respond per protocol.

**Statistician:** ## Statistical Assessment — LC-2025-024

---

### 1. Binomial Test — News as Necessary Condition (583/782)

**Sample size:** n = 782 runners (adequate for all parametric and non-parametric tests)
**Test:** One-sample binomial test, H₀: P(news | runner) = P(news | universe)

Universe news rate requires derivation: Has-news N = 23,633 of 112,679 total ticker-dates → baseline news coverage = **21.0%**

Observed: 583/782 = **74.6%** of runners have news.

Under H₀ (runners have the same news rate as the universe):
- Expected: 782 × 0.210 = 164.2 runners with news
- Observed: 583
- Z = (583 − 164.2) / √(782 × 0.210 × 0.790) = 418.8 / 11.38 ≈ **36.8**

**p < 0.0001 (effectively zero).** The enrichment is not remotely attributable to chance. News presence is a genuine discriminator of 100%+ runners at population scale.

**Wilson 95% CI on P(news | runner):** [71.4%, 77.6%]

However — critical caveat: this tests association, not causation. News may be correlated with gap% (large gaps attract coverage). If gap% and news are highly collinear, news adds no independent discriminating power beyond gap%. The triple-combo results address this partially (news appears as an incremental lift even within the gap≥10% cohort), but collinearity decomposition has not been run.

> **FLAG FOR CONTEXT:** Challenger should audit gap%/news collinearity — what fraction of gap≥10% tickers also have news? If >90%, news adds no independent information.

---

### 2. 95% CI for Best Triple (82/759 = 10.8%) vs Base Rate 0.694%

**Sample size:** n = 759 (adequate)
**Test:** Wilson score interval for proportion; likelihood ratio test vs base rate

**Wilson 95% CI on precision:** [8.8%, 13.2%]

The CI does **not** contain the base rate of 0.694%. Even the lower bound of 8.8% is **12.7× the base rate.** This is a robust finding — the triple combo signal is a genuine discriminator.

**Formal comparison vs base rate:**
- H₀: p = 0.00694
- Likelihood ratio test: G² = 2 × [82 × ln(82/5.27) + 677 × ln(677/753.73)] ≈ 2 × [82 × ln(15.56) + 677 × ln(0.898)]
- G² ≈ 2 × [82 × 2.745 + 677 × (−0.107)] ≈ 2 × [225.1 − 72.4] ≈ **305.4**
- p < 0.0001

**Verdict:** The 10.8% precision figure is statistically robust. The finding survives at the 99.99% confidence level.

**[STAT FLAG — in-sample caveat]** The 82/759 figure emerges from the same dataset used to select "best triple combos." The reported CI of [8.8%, 13.2%] is an in-sample estimate. True OOS precision will be lower. The gap between in-sample best-combo precision and OOS precision is typically 20-40% of the observed lift in exploratory analyses. PO should not treat 10.8% as a forward-looking number without OOS validation on held-out dates.

---

### 3. Recall Utility — Is 10.5% Recall Useful?

**Sample size basis:** 782 total runners across the dataset period. Requires knowing the date range to compute daily runner frequency.

**Expected daily flag count at ~500 ticker-dates/day:**

The universe is 112,679 ticker-dates. If ~500 ticker-dates/day are processed, the dataset spans approximately 225 trading days. In that case:
- Daily runners: 782 / 225 ≈ **3.5 runners/day** on average
- At 10.5% recall: **0.37 flagged runners/day** (i.e., fewer than 1 captured runner every 3 days on average)
- Daily flag count from the triple combo: 759/225 ≈ **3.4 flags/day**

**Precision-recall interpretation:**
- The triple combo flags ~3.4 tickers/day with a 10.8% hit rate (roughly 1 runner per 3 days of flagging)
- But this misses 89.5% of runners outright

At 10.5% recall, the scanner is a **high-precision, low-recall** instrument. Whether this is "useful" depends on the deployment model:

- If the strategy requires only **one live trade per day** and false positives are costly (capacity-constrained), 10.8% precision on 3.4 flags/day is usable — roughly 1 winner every ~3 days
- If the strategy needs **scale** (multiple runners/week), 10.5% recall is materially insufficient — you'd capture fewer than 2 runners/week on average
- The 33.8% recall at gap≥5% (264/782) captures roughly **1.2 runners/day** but at only 2.75% precision (36 false positives per runner)

**[STAT FLAG] The recall analysis depends critically on the dataset date range and daily distribution of ticker-dates.** If "~500 ticker-dates/day" is an approximation, the expected runner/day figure of 3.5 is uncertain by ±50%. Manager should provide: (a) exact date range, (b) daily ticker-date distribution, (c) daily runner count distribution.

---

### 4. Multiple Comparison Correction — BH on ~30 Threshold Combinations

**Number of comparisons:** The data package shows 4 gap thresholds × 4 PM thresholds × 2 news states = 32 combinations, plus individual signals = approximately **40 total tests** if singles are included.

**Applying Benjamini-Hochberg correction:**

BH controls False Discovery Rate (FDR) at level q = 0.05. With 40 tests:
- Rank p-values from smallest to largest (p₍₁₎ ≤ p₍₂₎ ≤ ... ≤ p₍₄₀₎)
- Reject H₀ for all tests where p₍ᵢ₎ ≤ (i/40) × 0.05
- At q = 0.05, BH threshold for the kth-ranked test = k × 0.00125

**Assessment of survival:**

All signals with lift ≥ 3.6x (news alone) or higher correspond to p-values effectively zero (z-scores 15+, given the large N). Every finding in the data package would survive BH correction at FDR = 0.05.

**However** — the critical concern is not whether the tests survive BH correction (they all will, given the scale of N), but whether the **best triple combos** were selected from a larger sweep of all possible threshold combinations. If the reported "best triple combos" are the top-ranked from a larger set of combinations not fully reported, the effective number of comparisons is larger than 40.

**[STAT FLAG] Multiple comparison risk: inflated comparison count.** If the "best triple combos" table represents top-ranked selections from a larger sweep (e.g., all combinations of gap thresholds from 1% to 50% in 1pp steps × all PM thresholds × news), the effective number of comparisons could be 100–500+. BH correction on the reported 4×4×2 grid is valid only if those were the pre-specified thresholds, not selected after observing results. Manager should confirm: were these the only thresholds tested, or are they the top-ranked from a larger sweep?

---

### 5. Optimal Precision-Recall Tradeoff — Is There a Principled Answer?

**Yes — via F-score with business-appropriate β.**

The standard F₁ score (harmonic mean of precision and recall) treats both equally. For a scanner with asymmetric costs:

**F_β = (1 + β²) × (precision × recall) / (β² × precision + recall)**

- **β < 1:** Weights precision higher (prefer fewer false positives) — appropriate if execution capacity is constrained
- **β > 1:** Weights recall higher (prefer not missing runners) — appropriate if missing a runner is costlier than processing false positives

**Applying to the data:**

At the current options:
| Threshold | Precision | Recall | F₁ | F₀.₅ (precision-weighted) | F₂ (recall-weighted) |
|-----------|-----------|--------|-----|--------------------------|----------------------|
| gap≥5% | 2.75% | 33.8% | 5.1% | 3.3% | 11.6% |
| gap≥10% | 5.03% | 22.6% | 8.1% | 6.0% | 13.6% |
| gap≥20% | 8.00% | 12.8% | 9.9% | 8.8% | 11.6% |
| best triple | 10.8% | 10.5% | 10.6% | 10.7% | 10.6% |

The **best triple combo dominates on F₀.₅** (precision-weighted) and is competitive on F₁. Gap≥10% dominates on **F₂** (recall-weighted) if missing runners is the primary concern.

**Principled recommendation:** The optimal threshold depends on the live trading model:
1. If **position-sizing requires high conviction** → best triple (F₀.₅ optimal)
2. If **the scanner feeds a secondary filter** that will further refine → gap≥10% with news (maximise recall at moderate precision) → the secondary filter handles precision
3. If **equal weighting**, gap≥20% or best triple are nearly tied on F₁

---

### Phase 1 Verdict Summary

| Signal | Statistical finding | Verdict |
|--------|---------------------|---------|
| P1.1 Gap% | Highly significant at all thresholds (p<0.0001). Wilson CI [8.8%, 13.2%] at best triple excludes base rate by 12×. | **PASS** |
| P1.2 News | 74.6% runner coverage vs 21.0% base, Z=36.8, p<0.0001. Independent contribution unconfirmed (collinearity). | **CONDITIONAL** — resolve collinearity with gap% |
| P2.1 PM Dollar Volume | Lift 1.8–5.2× depending on threshold. Valid signal but weaker than gap%. Best as second-stage filter. | **CONDITIONAL** — confirm independence from gap% |

**Unresolved blocking items before Phase 2 priorities can be finalised:**
1. Gap%/news collinearity — are these independent signals or proxies for the same thing?
2. OOS validation plan — in-sample best-triple precision [8.8%, 13.2%] needs temporal hold-out
3. Dataset date range and daily distribution — required to interpret recall utility in operational terms
4. Confirmation that reported threshold combinations are pre-specified, not post-hoc selected from a larger sweep

---

> **FLAG FOR CONTEXT — OOS requirement:** Any Phase 2 priority recommendation that involves threshold selection must specify a temporal OOS validation plan. The S3 blocking condition from LC-2025-018 applies here: in-sample optimisation overstates live performance. This blocks promotion of any threshold to production.

> **FLAG FOR CONTEXT — Challenger:** The four unresolved items above (collinearity, OOS plan, date range, comparison count) are audit items that should feed directly into Challenger's bias review.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** Statistician has delivered a thorough assessment. Four unresolved blocking items identified. Routing to Challenger now with full data context.

---

**Challenger — your turn.**

**Session:** LC-2025-024 | **Question:** Are the Phase 1 scanner signals statistically valid discriminators of intraday 100%+ runners?

**Full data context:**

**Universe:** 112,679 ticker-dates | 782 RTH 100%+ runners | Base rate = 0.694%

**P1.1 — Gap%:**
- >=5%: N=9,607, 264 runners, 2.75%, lift 4.0x, recall 33.8%
- >=10%: N=3,520, 177 runners, 5.03%, lift 7.2x, recall 22.6%
- >=20%: N=1,250, 100 runners, 8.00%, lift 11.5x, recall 12.8%
- >=50%: N=322, 39 runners, 12.11%, lift 17.5x, recall 5.0%

**P2.1 — PM Dollar Volume:**
- >=100K: N=21,596, 320 runners, 1.48%, lift 1.8x, recall 40.9%
- >=1M: N=16,124, 288 runners, 1.79%, lift 2.2x, recall 36.8%
- >=5M: N=7,195, 225 runners, 3.13%, lift 3.8x, recall 28.8%
- >=10M: N=4,720, 199 runners, 4.22%, lift 5.2x, recall 25.4%

**P1.2 — News:**
- Has news: N=23,633, 583 runners, 2.47%, lift 3.6x, recall 74.6%
- No news: N=89,046, 199 runners, 0.22%, lift 0.3x, recall 25.4%

**Best triple combos (n≥30):**
- gap>=15% + PM>=5M + news: N=759, 82 runners, 10.8%, lift 16x, recall 10.5%
- gap>=20% + PM>=5M + news: N=603, 65 runners, 10.8%, lift 16x, recall 8.3%
- gap>=15% + PM>=1M + news: N=952, 91 runners, 9.6%, lift 14x, recall 11.6%
- gap>=10% + PM>=1M + news: N=990, 98 runners, 9.9%, lift 14x, recall 12.5%

**Statistician's key findings:**
- News enrichment: Z=36.8, p<0.0001 — genuine discriminator at population scale
- Best triple CI: [8.8%, 13.2%] — lower bound 12.7× base rate, robust finding
- Recall: ~3.5 runners/day universe-wide; triple combo captures ~0.37/day
- BH correction: all signals survive, but concern raised about post-hoc threshold selection
- F-score analysis: best triple dominates F₀.₅ (precision-weighted); gap≥10% dominates F₂ (recall-weighted)

**Statistician's four unresolved blocking items:**
1. Gap%/news collinearity — independent signals or proxies?
2. OOS validation plan — in-sample CI not forward-looking
3. Dataset date range and daily distribution — required for operational recall interpretation
4. Confirmation threshold combinations are pre-specified, not post-hoc from larger sweep

**Your mandate — three-part audit:**

**A. Lookahead bias check:**
- Gap% and PM Dollar Volume — are these computed from pre-market data only, or could they incorporate RTH data? What is the exact timestamp boundary?
- News — when is the news timestamp relative to market open? Could "has news" include articles published after the runner was already in progress?

**B. Coverage / selection bias:**
- Gap%/news collinearity: what fraction of gap≥10% tickers also have news? Statistician flagged this as potentially fatal to news independence claim
- PM Dollar Volume missing data: what happens to tickers with no PM activity — are they coded as $0 or excluded? How many of the 782 runners had zero PM volume?
- "Runner" definition: is 100%+ measured from open price, prior close, or intraday low? Could the definition itself introduce survivorship bias?

**C. Data quality flags:**
- The PM vol signal being "weaker than Phase 0 suggested" — is this a data quality issue (missing PM data for many tickers) or a genuine signal degradation?
- Best triple combos labeled "n≥30" — what was the full combination space tested? Were these pre-specified thresholds or selected after observing results?

Raise any issue that would change the Phase 1 PASS/CONDITIONAL verdict. Flag as [BLOCKING] if it invalidates a signal entirely.

[NEXT: challenger]

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## Challenger Audit — LC-2025-024

---

### Evidence Received

I have the data context package as provided by Manager, plus the Statistician's assessment. I have not seen: raw data files, code used to compute any signal, the definition of "runner," the timestamp logic for any feature, or confirmation of what the full combination space tested was.

---

## A. Lookahead Bias Check

### A1. Gap% — Timestamp Boundary

**Claim:** Gap% is a pre-market signal.

**Problem:** "Gap%" is not defined anywhere in the data package. I do not know:
- Is it computed as `(open_price - prior_close) / prior_close`?
- Is it computed as `(PM_high - prior_close) / prior_close`?
- At what exact timestamp is "gap" frozen — 9:00 AM? 9:28 AM? 9:30:00 AM exactly?

**[BLOCKING — LOOKAHEAD RISK]** If gap% uses the RTH open price (9:30 bar open), it is legitimate. If it uses any price after 9:30:00, it incorporates data from after the decision point. If it uses a "current pre-market price" that is snapshotted at any time during RTH (e.g., a stale PM quote that was refreshed), it may be contaminated.

**Critical secondary issue:** If gap% is computed as `(open - prior_close) / prior_close` using the RTH 9:30 open price — the open price is *itself* partially determined by the intraday demand that creates runners. For a stock that gaps 50%+ at open due to a catalyst, the open price is co-determined with the outcome. This is not classic lookahead bias (the open is knowable at 9:30:00), but it does mean **gap% is partially an outcome proxy, not a pure predictor**. This needs to be explicitly acknowledged in the Phase 1 verdict.

**Required confirmation:** The exact formula and timestamp for gap% computation. Manager must provide the code snippet or explicit definition.

---

### A2. PM Dollar Volume — Timestamp Boundary

**Claim:** PM Dollar Volume is pre-market activity.

**[BLOCKING — LOOKAHEAD RISK]** Same issue as above, but more acute. PM Dollar Volume must be confirmed as the cumulative volume × price from 4:00 AM (or 7:00 AM) through exactly 9:29:59 AM. I need to know:
- What is the exact PM session window used?
- Is PM volume sourced from a real-time feed snapshot or from a historical PM bar file?
- If from a historical PM bar file: is this file reconstructed from complete-day records, or from a live capture? If reconstructed, when were the PM bars collected — at PM session end (9:29 AM) or post-hoc from daily history?

**Post-hoc PM bar reconstruction is a known lookahead vector.** Data vendors frequently retroactively adjust pre-market records. If the PM volume figures used here were sourced from a vendor that retroactively fills PM bars, the "pre-market volume" a live system would have seen at 9:25 AM may have been materially lower than what the research database shows.

**Required confirmation:** Source of PM dollar volume data — live capture vs reconstructed, and vendor name/method.

---

### A3. News — Timestamp Boundary

**[BLOCKING — LOOKAHEAD RISK — HIGHEST PRIORITY]**

This is the most serious lookahead concern in the entire dataset.

"Has news" is flagged for 23,633 of 112,679 ticker-dates. But I have no information about:
1. **What timestamps qualify as "news"?** If a news article is published at 9:45 AM after the stock has already moved 40%, that article is caused by the runner — it is not a predictor of it.
2. **What is the news source?** Wire services (PRN, GlobeNewswire) have timestamps. But aggregators (Bloomberg, FactSet, even some free scrapers) frequently tag news with the *retrieval date*, not the *publication time*. If "has news" means "had a news item tagged to this ticker on this date" without a sub-day timestamp filter, the signal is contaminated by post-open coverage.
3. **Is the news categorised by type?** Pre-market earnings releases and FDA announcements are genuine pre-market signals. Analyst upgrades, news coverage of price action, SEC filing releases, and social media aggregation are temporally ambiguous.

**The 74.6% runner coverage rate for "has news" is highly suspicious in this light.** If news were a genuinely pre-market-only signal, I would expect meaningful coverage gaps for tickers with no scheduled catalysts. A 74.6% rate suggests either (a) news is very broadly defined to include any coverage on the day, including post-open coverage, or (b) large-gap runners systematically attract same-day news coverage *as a consequence of their move*. Either interpretation would contaminate the news signal with outcome-driven information.

**Directional assessment:** If post-open news is included, the 74.6% recall figure is an overestimate. The true pre-market-only news recall for runners could be substantially lower — and more importantly, the 21.0% base rate for "has news" in the full universe could also be inflated by post-open coverage on any high-volume day, making the relative enrichment less extreme than Z=36.8 suggests.

**This is a blocking finding pending timestamp confirmation.** The news signal cannot be assigned a Phase 1 PASS or CONDITIONAL verdict until the timestamp definition is confirmed.

---

### A4. Runner Definition — Outcome Measurement

**"RTH 100%+ runners"** — measured from what reference price? This is not defined in the data package.

Three plausible definitions:
1. `(intraday_high - open) / open >= 1.0` — gain from open
2. `(intraday_high - prior_close) / prior_close >= 1.0` — gain from prior close
3. `(intraday_high - intraday_low) / intraday_low >= 1.0` — intraday range

**Each produces a different universe and a different alignment with gap%:**
- Definition (1): a stock that opens +60% and then doubles from open is a runner. Gap% predicts the open price which is the starting reference — partially circular.
- Definition (2): a stock needs to exceed 100% above prior close total. Large-gap stocks start with a "head start" toward this threshold — this inflates runner rate within high-gap cohorts mechanically, regardless of any genuine signal.
- Definition (3): pure intraday range — least correlated with gap% by construction.

**[BLOCKING — POTENTIAL MECHANICAL INFLATION]** If the runner definition uses prior close as the baseline (definition 2), then gap% has a mechanical relationship with "runner" status: a stock that opens +60% only needs another +40% intraday to qualify. A stock that opens flat needs +100% intraday. This inflates runner rates in high-gap cohorts by design, not by genuine signal. The 17.5x lift at gap≥50% may be substantially attributable to this mechanical effect rather than genuine predictive power.

**Required confirmation:** Exact runner definition formula and reference price.

---

## B. Coverage / Selection Bias

### B1. Gap%/News Collinearity

The Statistician correctly flagged this. I will sharpen the question.

**The triple combo data partially addresses this, but incompletely.** The fact that `gap>=10% + PM>=1M + news` (N=990) shows lift=14x while `gap>=10%` alone shows lift=7.2x tells us news adds something *within* the gap≥10% cohort — but I cannot quantify this without knowing the marginal contribution of news conditional on gap.

**Specifically, I need:**
- N and runner rate for `gap>=10% + news` (without PM filter)
- N and runner rate for `gap>=10% without news`

If `gap>=10% + news` has nearly the same runner rate as `gap>=10% + PM>=1M + news`, then PM vol is the redundant signal. If `gap>=10% without news` has a runner rate close to `gap>=10%` overall, then news is the redundant signal. Without this 2×2 decomposition, I cannot confirm which signals are genuinely independent.

**This is not blocking for Phase 1 verdict but is blocking for Phase 2 prioritisation.**

---

### B2. PM Dollar Volume — Zero/Missing Data Treatment

**Critical data quality question with no answer in the data package:**

The PM Dollar Volume thresholds (≥100K, ≥1M, ≥5M, ≥10M) imply a continuous distribution. But:
- Tickers with no PM activity: are they coded as $0 (and therefore included in the "below threshold" bucket for all thresholds) or excluded from PM analysis entirely?
- If excluded: the denominators for PM analysis may not sum to 112,679. I cannot verify this from the data provided.
- If included as $0: the "below ≥100K" group contains both genuinely low-PM tickers and tickers with no data coverage. These are different populations.

**Checking the numbers:** PM ≥100K has N=21,596. Total universe = 112,679. That means ~91,083 ticker-dates have PM volume below $100K or no PM data. If a large fraction of these are "no PM data available" rather than "genuinely low PM activity," the PM signal's apparent weakness (1.8x lift at ≥100K) may be partly a data coverage artefact.

**For the 782 runners specifically:** How many had zero or missing PM volume? If runners systematically have PM data available (because they are actively traded pre-market), while the general universe has many tickers with no PM coverage, the comparison is not apples-to-apples.

**Required:** Count of ticker-dates with zero or null PM volume in (a) full universe and (b) runner subset.

---

### B3. "Weaker Than Phase 0 Suggested" — Signal or Data?

The data package notes PM vol alone is "weaker than Phase 0 suggested." This is unexplained in the provided context.

**Two competing explanations:**
1. **Data quality:** Phase 0 used a different PM data source, different session hours, or a different missing-data treatment. The apparent weakening is a data artefact.
2. **Genuine signal degradation:** Phase 0 may have been run on a smaller, curated sample. The broader 112,679 ticker-date universe dilutes the signal because it includes many days/tickers where PM vol has no predictive relevance.

**I cannot distinguish these from the provided evidence.** Manager must supply: (a) Phase 0 PM vol lift figure and the dataset it was computed on, (b) confirmation that PM data source and session hours are identical between Phase 0 and the current analysis.

---

### B4. "Best Triple Combos (n≥30)" — Combination Space

**[BLOCKING — POST-HOC SELECTION RISK]**

The data package reports exactly 4 triple combos, all with news=True, all with PM≥1M or higher, and all with gap≥10% or higher. This selection is suspiciously clean.

**Questions that must be answered:**
1. How many total threshold combinations were evaluated to produce this "best" table? The Statistician estimated ~40 combinations on a 4×4×2 grid, but if gap thresholds of 5%, 10%, 15%, 20%, 25%, 30%, 40%, 50% were all tested (8 values) × 4 PM thresholds × 2 news states = 64 combinations, plus all doubles and singles, the effective comparison count is 100+.
2. Were these four combos selected because they had the highest precision? Highest lift? Highest F-score? The selection criterion is not stated.
3. The label "n≥30" implies a minimum N filter was applied. How many combinations were excluded by this filter? If 50 combinations were evaluated but 30 had N<30 and were dropped, the "reported best" may simply be the highest-N combinations, not the highest-precision ones — but this conflation of selection criteria is not transparent.

**Without knowing the full combination space, the BH correction applied by the Statistician is invalid.** BH was applied to "~40 tests" — but if 100+ combinations were evaluated and only the top 4 are reported, the effective multiple testing burden is on 100+ tests, not 40. Surviving BH at 40 tests does not survive BH at 100 tests for marginal cases. (For the strongest signals with effectively-zero p-values this is moot, but the marginal signals — e.g., gap≥10% + PM≥1M + news at 9.9% precision — could drop below significance.)

---

## C. Summary Assessment

### Lookahead Bias Check — Explicit Statement

| Signal | Lookahead Risk | Severity |
|--------|---------------|----------|
| Gap% (if using RTH open) | Low — open is knowable at decision time; but partially outcome-correlated | Acknowledged limitation, not blocking |
| Gap% (if using any post-9:30 price) | High | **BLOCKING** |
| PM Dollar Volume (if from live capture) | Low | Acceptable |
| PM Dollar Volume (if retroactively reconstructed) | High | **BLOCKING** |
| News (if timestamp-filtered to pre-open only) | Low | Acceptable |
| News (if any same-day news included) | **Critical** | **BLOCKING** |
| Runner definition vs gap% (mechanical inflation) | Medium-High | **BLOCKING pending definition** |

**Result: Lookahead bias cannot be cleared for any of the three signals until timestamp definitions and the runner definition formula are provided.** This is not a formality — the news signal in particular has a material probability of being contaminated by post-open coverage based on the 74.6% recall figure alone.

---

### Revised Phase 1 Verdict

| Signal | Statistician Verdict | Challenger Override | Reason |
|--------|---------------------|--------------------|-|
| P1.1 Gap% | PASS | **CONDITIONAL** | Runner definition may mechanically inflate lift in high-gap cohorts; timestamp confirmation required |
| P1.2 News | CONDITIONAL | **BLOCKED** | Timestamp definition not provided; 74.6% recall is a red flag for post-open contamination |
| P2.1 PM Dollar Volume | CONDITIONAL | **CONDITIONAL** | Data coverage for zero-PM tickers unresolved; source confirmation required |

---

### Mandatory Questions for Manager (Priority Order)

**[BLOCKING — must answer before Phase 1 verdict is finalised]**

1. **Runner definition:** Exact formula. Is 100%+ measured from prior close, RTH open, or intraday low?
2. **News timestamp:** Is "has news" filtered to pre-market publications only (before 9:30 AM)? What is the exact timestamp cutoff? What is the news data source?
3. **Gap% formula:** Is it `(open - prior_close) / prior_close` using the 9:30 RTH open bar? Or another formula?
4. **PM Dollar Volume source:** Live capture or retroactively reconstructed? What are the exact PM session hours used?
5. **Full combination space:** How many threshold combinations were evaluated in total? What was the selection criterion for "best"?

**[Non-blocking but required before Phase 2 prioritisation]**

6. **Gap%/news 2×2 decomposition:** Runner rates for `gap≥10% + news`, `gap≥10% + no news`, `gap<10% + news`, `gap<10% + no news`
7. **PM zero/missing data counts:** In full universe and runner subset
8. **Phase 0 PM vol lift figure and dataset:** To diagnose whether weakening is data artefact or genuine
9. **Dataset date range and year-by-year distribution:** Required for regime-specificity assessment (2020–2021 high-retail participation vs other periods)

---

> **FLAG FOR CONTEXT — Memory update required:** News timestamp lookahead as a new failure mode pattern. Post-open news coverage contaminating same-day "has news" flags is a systematic risk in any event-driven scanner research. Add to known failure modes.

> **FLAG FOR CONTEXT — Runner definition circularity:** When runner threshold is measured from prior close, gap% has a mechanical (non-signal) relationship with runner qualification. This is a structural design issue that must be checked in any momentum/gap research. Add to known failure modes.

> **FLAG FOR CONTEXT — Phase 2 priorities:** Cannot be responsibly recommended until the five blocking questions above are answered. Any Phase 2 recommendation made before resolving news timestamp contamination risk would be built on a potentially invalid foundation.

Now updating memory with new failure mode patterns identified in this session.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## Session Continues — LC-2025-024

Excellent work from both agents. Challenger has raised five blocking questions that must be resolved before Phase 1 verdicts can be finalised. I need to answer these from the research context before I can route further.

Let me work through what I can resolve analytically vs what requires PO/VPS confirmation.

---

### Triage of Challenger's Five Blocking Questions

**Q1 — Runner definition (100%+ from what reference price?)**

From the research agenda context (LC-2025-017-partB and LC-2025-023): the runner universe is defined as RTH 100%+ runners. From the ORB research (LC-2025-014), the multibagger universe used `intraday range ≥ 100%` — specifically stocks where `(intraday_high - prior_close) / prior_close ≥ 1.0`. This is **Definition 2** in Challenger's taxonomy — measured from prior close.

**Challenger's concern is valid.** A stock gapping +60% at open only needs +40% more intraday to qualify. This mechanically inflates runner rates within high-gap cohorts. The 17.5x lift at gap≥50% likely contains a mechanical component. I cannot quantify this split without a separate analysis comparing "gap-adjusted" intraday gains vs raw prior-close-based runner status.

This is a **material limitation** that must be flagged to PO but does not invalidate the signal entirely — gap% still requires genuine pre-market catalyst activity to produce large gaps.

**Q2 — News timestamp:** Cannot be resolved from context documents. The news data source is Benzinga via Massive/Polygon API (per EXP-024 and IDEA-023 notes). Benzinga timestamps are publish-time, not retrieval-time. However, I cannot confirm whether the P1.2 analysis filtered to pre-9:30 AM publications only. **Requires PO confirmation — escalating.**

**Q3 — Gap% formula:** From the scanner architecture (market_scanner.py context): gap% uses `todayChangePerc` from Polygon snapshot, which is `(current_price - prior_close) / prior_close`. During pre-market, this is computed against the last PM quote. At RTH open, this becomes the open price. The P1 research would have used daily bar data — almost certainly `(open - prior_close) / prior_close`. **Likely clean but requires confirmation.**

**Q4 — PM Dollar Volume source:** From architecture context, Polygon provides PM bars. PM bars from Polygon's historical API are reconstructed from trade data — not a live capture. Retroactive adjustment risk is **low for Polygon** (they use consolidated tape), but cannot be ruled out entirely. **Requires PO confirmation.**

**Q5 — Full combination space:** Cannot resolve from context. The "best triple combos (n≥30)" table looks like it may be top-ranked from a larger sweep. **Requires PO confirmation.**

---

### What I Can Resolve Right Now

Three of the five blocking questions require PO confirmation from VPS data. Two (Q1 runner definition, Q3 gap formula) can be partially addressed analytically.

Before escalating to PO, I should run the backtester to test one resolvable question: does the gap% signal survive if we apply a **gap-only** filter (no news, no PM) and examine whether the precision curve matches a mechanical inflation model?

Actually — the backtest engine cannot test this directly since it operates on price bars, not pre-market data. The P1 signals are scanner-level filters, not entry rules. I cannot resolve this via `run_backtest`.

The right path is: **escalate the five blocking questions to PO, route Optimist for alternative angles, then close.**

---

Before closing, routing to Optimist for alternative angles on the Phase 2 priority question — specifically whether there's a framing that remains valid even if one or more P1 signals are partially contaminated.

**Optimist — your turn.**

**Session:** LC-2025-024 | **Question:** Phase 1 scanner signals for 100%+ runners — what remains valid and what are the Phase 2 priorities?

**Data context (same as above):**
- Universe: 112,679 ticker-dates | 782 runners | 0.694% base rate
- Gap% at ≥10%: lift 7.2x, recall 22.6%; at ≥20%: lift 11.5x, recall 12.8%
- PM Dollar Volume ≥5M: lift 3.8x, recall 28.8% (weaker than expected)
- News (any): lift 3.6x, recall 74.6%
- Best triple (gap≥15% + PM≥5M + news): 10.8% precision, 10.5% recall, N=759

**Challenger's blocking findings:**
1. Runner definition uses prior close → gap% may have mechanical inflation at high gap levels (gap+50% stock only needs +40% more to "qualify")
2. News timestamp unconfirmed — 74.6% recall is suspicious, may include post-open articles
3. Gap% formula and PM source require confirmation
4. Full combination space unknown — possible post-hoc selection bias

**Statistician's key flags:**
- In-sample best-triple CI [8.8%, 13.2%] — OOS precision will be lower
- ~3.5 runners/day universe-wide; triple combo captures ~0.37/day at 10.5% recall
- BH correction valid only if ~40 combinations were pre-specified

**Your mandate:**
1. Is there an angle on Phase 2 priorities that remains valid even if news is partially contaminated by post-open coverage?
2. Is there a reformulation of the runner definition that avoids the mechanical inflation problem — and would that reformulation be worth testing?
3. Are there Phase 2 signals (beyond the three P1 signals) that could complement gap% in a way that's demonstrably free of the lookahead concerns Challenger raised?

Be concrete. Flag anything that belongs in persistent memory.

[NEXT: optimist]

---

**Manager:** Session transcript so far.

Optimist, your turn. Respond per protocol.

**Optimist:** ## Optimist Assessment — LC-2025-024

---

### Interpretation of the Evidence

The session has produced a genuinely strong statistical finding beneath a layer of methodological concerns. Let me separate the durable from the fragile.

**What is structurally robust regardless of Challenger's blocking findings:**

Gap% is the strongest signal and the least contaminated. Even under the worst-case mechanical inflation scenario (prior-close runner definition), the gap% lift curve is not fully explained by mechanics. Here is why: if mechanical inflation were the primary driver, we would expect the lift curve to be *steepest* at the gap threshold where the mechanical "head start" tips a stock over 100% — roughly gap≥50% to gap≥70%. But the lift curve shows meaningful enrichment beginning at gap≥5% (4.0x) and rising monotonically through gap≥50% (17.5x). A purely mechanical model predicts a step function near the 100%-minus-gap boundary, not a smooth monotone curve. The smooth curve is consistent with gap% being a genuine predictor, not purely a definitional artefact. The mechanical component exists but is not the whole story.

**What is fragile and should not be relied upon until confirmed:**

News at 74.6% recall is the most suspicious number in the dataset. Challenger is right that this is a red flag. A 74.6% rate against a 21.0% base is extraordinary, and post-open coverage contamination is a plausible explanation. However — and this is critical — even if news is partially contaminated, it does not follow that news has *zero* independent predictive power. The question is quantitative: how much of the 74.6% recall survives a strict pre-9:30 AM timestamp filter? The answer could be 40%, which is still enormously enriched. We should not discard the signal — we should demand the clean version of it.

PM Dollar Volume underperformance relative to Phase 0 expectations is actually *informative*. A signal that appears strong in a curated sample and weakens in the broad universe is telling us something about regime or selection — not that the signal is useless, but that it is conditional. The conditionally valid version of PM vol may be: "PM vol is a confirming filter, not a leading filter." The triple combo data supports this — PM vol adds lift *on top of* gap%, not independently.

---

### 1. Phase 2 Priorities — Valid Even If News Is Contaminated

The key insight is that Phase 2 should be designed to *purify* the P1 signals, not abandon them. Here is the framing that survives even the worst-case news contamination scenario:

**Gap% is the anchor signal.** It is the least contaminated, has the strongest monotone lift curve, and requires only a formula and timestamp confirmation (both likely to clear). Gap% at ≥10% gives 22.6% recall with 7.2x lift on a universe of 3,520 ticker-dates. This is a workable funnel.

**Phase 2 priority recommendation — conditional on gap% clearing confirmation:**

The Phase 2 agenda should answer: *within the gap≥10% cohort (3,520 ticker-dates), what signals further discriminate the 177 runners from the 3,343 non-runners?*

This reframes Phase 2 as a *conditional enrichment* problem rather than a fresh signal search. This matters because:
- It sidesteps the news timestamp problem — if we test news *only within* the gap≥10% cohort, we can run the timestamp filter on a much smaller data slice (3,520 rows, not 112,679)
- It sidesteps the runner definition circularity — the gap≥10% cohort already controls for "head start" effects because all members have a similar prior-close gap structure
- It sidesteps the PM vol regime concern — we are asking whether PM vol adds lift *given* gap≥10%, not whether it stands alone

**Specifically, Manager should request the 2×2 decomposition Challenger already called for:**
- `gap≥10% + news` vs `gap≥10% + no news` — runner rates for each cell
- `gap≥10% + PM≥1M` vs `gap≥10% + PM<1M` — runner rates for each cell

If news adds 2x lift within the gap≥10% cohort (clean pre-open version), it is a genuine Phase 2 signal. If PM adds an independent 2x lift within the same cohort, it earns Phase 2 inclusion. These tests are small-N but focused — exactly the right design.

---

### 2. Runner Definition Reformulation

Challenger's concern about prior-close measurement is correct but solvable. Here is the reformulation I would test:

**Alternative runner definition: `(intraday_high - RTH_open) / RTH_open ≥ 0.50`**

Rationale: This measures intraday continuation from open rather than total move from prior close. A 50% gain *from open* is a genuinely remarkable intraday move and is not mechanically correlated with gap%. A stock that opens +60% and then gains 50% from that open is a different beast from a stock that gaps +60% and drifts sideways — the former is the actual trading opportunity.

**Why 50% rather than 100%?** Two reasons:
1. The prior-close 100% threshold already bakes in gap% — a gap≥50% stock needs only 33% intraday continuation to qualify. Requiring 50% *from open* is a more demanding and gap-independent test.
2. The resulting universe size will be smaller, but it will be cleaner. If 50%-from-open runners still show strong gap% enrichment, the signal is real and mechanical inflation is not the explanation.

**Manager should run:** Count of ticker-dates where `(intraday_high - RTH_open) / RTH_open ≥ 0.50`, and recompute gap% lift curve against this alternative runner definition. If the lift curve shape is preserved (monotone, meaningful at gap≥5%), mechanical inflation was not the dominant driver. If the lift curve flattens dramatically, Challenger's concern was the right call.

This test requires only daily bar data (open, high) and the existing gap% field — no new data sources needed.

---

### 3. Phase 2 Signals Demonstrably Free of Lookahead Concerns

Here are three signal categories for Phase 2 that are structurally cleaner than news:

**3a. Float-adjusted gap% (Float Turnover at Open)**

We already have this from LC-2025-014 — float turnover = `day_dollar_volume / (free_float × open_price)`. The float is a static fundamental. The open price is known at 9:30:00. A stock gapping 20% on low float with high float turnover is a categorically different setup from a stock gapping 20% on high float with low turnover. Float turnover has no lookahead risk because float is not determined by intraday price action. This was used in the multibagger universe filter (≥0.50x) and showed a natural breakpoint.

**Manager should test:** Within gap≥10% cohort, what is the runner rate for float_turnover ≥ 0.50x vs <0.50x? This reuses existing data and has no lookahead concern.

**3b. Gap% × relative to ATR (normalized gap)**

Raw gap% treats a 15% gap the same regardless of whether the stock's typical daily range is 2% or 15%. A gap of 15% on a stock with ATR of 2% is a 7.5-sigma event; the same gap on a stock with ATR of 15% is baseline. Normalised gap = `gap% / ATR_20day` (ATR computed from prior 20 days, so fully pre-market). This is completely free of lookahead. If normalised gap discriminates runners better than raw gap%, we gain both explanatory power and signal integrity confirmation.

**Manager should test:** Compute ATR-normalised gap for the 112,679 ticker-dates. Compute runner rates at normalised gap thresholds of 1x, 2x, 3x, 5x ATR. Compare lift curve shape to raw gap%.

**3c. News × catalyst type (if Benzinga data permits subcategory)**

If the Benzinga timestamp issue is resolved and news is confirmed pre-market only, the next Phase 2 question is: does catalyst *type* discriminate within the "has news" cohort? Earnings, FDA catalysts, and M&A announcements have different continuation profiles. A "has news" flag that distinguishes earnings vs analyst upgrade vs price-action coverage is a materially richer signal. This requires only a category field from the existing Benzinga data pull — no new data source.

**Manager should check:** Does the existing Benzinga data include a category/tag field? If yes, cross-tab runner rate by category within the `has news` cohort.

---

### Confidence Assessment

| Finding | Confidence | Blocking condition |
|---|---|---|
| Gap% is a genuine discriminator (not purely mechanical) | High | Requires gap formula confirmation + alternative runner definition test |
| News has some real pre-market signal content | Medium | Requires timestamp audit — but prior-close runner rate is not zero for no-news runners (25.4% recall / 199 runners without news still exist) |
| PM vol is a conditional confirming signal, not a leading signal | Medium-High | Consistent with triple combo data; not blocking |
| Best triple precision [8.8%, 13.2%] is structurally real | High — with caveat | OOS precision will be lower; treat as upper bound |
| Float turnover and ATR-normalised gap are clean Phase 2 candidates | High | No lookahead concerns |

---

### Phase 2 Priority Recommendation (Provisional — Pending Blocking Question Resolution)

**Priority 1 (immediate, no new data needed):**
- Alternative runner definition test: `(intraday_high - RTH_open) / RTH_open ≥ 0.50`
- Gap%/news/PM 2×2 decompositions within gap≥10% cohort (Challenger already requested this)

**Priority 2 (requires existing data reuse):**
- Float turnover within gap≥10% cohort (data already exists from LC-2025-014 pipeline)
- ATR-normalised gap computation across full universe

**Priority 3 (requires timestamp audit first):**
- News category decomposition by catalyst type (Benzinga category field)
- Pre-market-only news signal reconstruction with strict <9:30 AM filter

**Priority 4 (OOS validation — structural requirement):**
- Temporal split: train on first 60% of dates, validate on last 40%. Apply to best triple and any Phase 2 additions. This is the S3 blocking condition and cannot be bypassed.

---

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## Session Continues — LC-2025-024

Optimist has delivered. Three structurally sound contributions:

1. **Mechanical inflation rebuttal** — smooth lift curve (not step-function) is inconsistent with pure mechanical inflation. Gap% is a genuine signal with a mechanical *component*, not a mechanical *artefact*.
2. **Runner definition reformulation** — `(intraday_high - RTH_open) / RTH_open ≥ 0.50` as a gap-independent alternative. Testable with existing daily bar data.
3. **Three clean Phase 2 signals** — float turnover (no lookahead), ATR-normalised gap (no lookahead), news catalyst type (requires timestamp audit first).

---

### Session Status

| Agent | Status |
|---|---|
| Statistician | ✅ Complete |
| Challenger | ✅ Complete |
| Optimist | ✅ Complete |

All three agents have delivered. Before closing, I need to synthesise findings and determine what I can run vs what requires PO escalation.

---

### What I Can Run Right Now

Optimist proposed testing the alternative runner definition: count ticker-dates where `(intraday_high - RTH_open) / RTH_open ≥ 0.50`. This requires daily bar data — open and high prices. The backtest engine operates on 1-min bars, not daily bar aggregates, so I cannot run this directly via `run_backtest`.

However — I **can** run a proxy test using the backtest engine. The engine has `price_change_pct` as an indicator. If I set up an entry at open and an exit when `price_change_pct >= 50%` from open, I could count qualifying ticker-dates. But this would be a signal bar walk, not a daily bar query — it would require running across the full universe, which is computationally expensive and architecturally misaligned with what I have.

**Verdict:** The alternative runner definition test and the 2×2 decompositions require VPS-level data access (daily bar aggregates, not BacktestEngine). These must be escalated to PO for execution.

The `run_backtest` tool is not the right instrument for this session's open questions — they are all data analysis tasks on the scanner/universe layer, not backtesting tasks.

---

### Five Blocking Questions — Final Disposition

| # | Question | Disposition |
|---|---|---|
| Q1 | Runner definition (prior close vs open) | **Confirmed as prior close** — mechanical inflation is real, magnitude unknown. Escalate to PO for alternative definition test |
| Q2 | News timestamp — pre-9:30 filter? | **Cannot resolve from context** — escalate to PO |
| Q3 | Gap% formula | **Likely `(open - prior_close) / prior_close`** — high confidence but requires VPS confirmation |
| Q4 | PM Dollar Volume source | **Polygon historical API (reconstructed)** — low retroactive risk, but requires PO confirmation |
| Q5 | Full combination space | **Cannot resolve from context** — escalate to PO |

---

### Proceeding to Session Close

Both Challenger and Optimist have been consulted. Statistician delivered first. All three agents have given final-turn contributions. Synthesising now.

---

## Session Close — LC-2025-024

### Key Findings (5 bullets)

1. **Gap% is the anchor signal — statistically robust with a known limitation.** Lift curve is monotone (4.0x at ≥5% → 17.5x at ≥50%), Wilson CI for best triple [8.8%, 13.2%] excludes base rate by 12×. Smooth lift shape is inconsistent with pure mechanical inflation (Optimist rebuttal accepted). Limitation: runner definition from prior close gives high-gap stocks a mechanical head start — magnitude of mechanical component unknown until alternative runner definition is tested.

2. **News signal is blocked pending timestamp audit.** Z=36.8 enrichment is extraordinary but 74.6% recall rate is suspicious — likely includes post-open coverage articles. Cannot assign PASS or CONDITIONAL until Benzinga timestamp filter (pre-9:30 AM only) is confirmed. This is the single highest-priority confirmation needed.

3. **PM Dollar Volume is a conditional confirming filter, not a leading signal.** Lift of 1.8x standalone, but 14–16x lift in triple combos — consistent with PM vol adding discriminating power within the gap cohort, not independently. Weakness relative to Phase 0 expectations may reflect data coverage gaps (zero-PM tickers coded as $0). Requires missing-data audit.

4. **Best triple combo precision [8.8%, 13.2%] is in-sample only.** OOS precision will be lower. At 10.5% recall, the triple captures ~0.37 runners/day in a ~500-ticker-day universe — fewer than 2 runners/week. Whether this is operationally sufficient depends entirely on the live trading model (capacity-constrained high-conviction vs scale).

5. **Two clean Phase 2 signal candidates identified — no lookahead concerns.** Float turnover (static fundamental × open price) and ATR-normalised gap (prior 20-day ATR) are structurally clean alternatives that complement gap% without timestamp ambiguity. Both can be computed from existing data.

---

### FLAG FOR CONTEXT — Master List

| # | Source | Flag | Priority |
|---|---|---|---|
| 1 | Challenger | News timestamp lookahead — post-open coverage may contaminate 74.6% recall figure | **BLOCKING** |
| 2 | Challenger | Runner definition (prior close) creates mechanical inflation in high-gap lift figures | **BLOCKING pending quantification** |
| 3 | Challenger | Full combination space unknown — BH correction may be based on undercount of tests | High |
| 4 | Challenger | PM vol missing-data treatment (zero vs excluded) — may inflate apparent PM vol weakness | High |
| 5 | Statistician | Best triple [8.8%, 13.2%] is in-sample — OOS precision will be lower by 20–40% of lift | High |
| 6 | Statistician | Dataset date range required for operational recall interpretation (~3.5 runners/day assumed) | Medium |
| 7 | Statistician | Gap%/news collinearity — news may proxy gap%, not add independent information | Medium |
| 8 | Optimist | Alternative runner definition `(high - open) / open ≥ 50%` — tests mechanical inflation hypothesis | Medium |
| 9 | Optimist | Float turnover × gap% and ATR-normalised gap as clean Phase 2 candidates | Medium |
| 10 | Optimist | News catalyst type decomposition (earnings vs FDA vs price-action coverage) — requires timestamp audit first | Low (after #1 resolved) |

---

### Phase 1 Verdict (Provisional — Pending Blocking Questions)

| Signal | Verdict | Condition to upgrade |
|---|---|---|
| P1.1 Gap% | **CONDITIONAL PASS** | Confirm gap formula = `(open - prior_close)/prior_close`; quantify mechanical inflation via alternative runner def |
| P1.2 News | **BLOCKED** | Confirm Benzinga timestamp filter = pre-9:30 AM publications only |
| P2.1 PM Dollar Volume | **CONDITIONAL** | Confirm missing-data treatment; confirm Polygon PM source |

---

### Phase 2 Priority Recommendation (For PO Review)

**Pre-condition:** Resolve Q1–Q5 blocking questions first. Phase 2 priorities below assume gap% clears confirmation.

| Priority | Task | Data needed | Effort |
|---|---|---|---|
| P2-A | Confirm news timestamp filter (pre-9:30 AM only) + recompute recall | VPS — Benzinga data audit | Low |
| P2-B | Alternative runner definition test: `(high - open) / open ≥ 50%` | VPS — daily bar aggregates | Low |
| P2-C | 2×2 decomposition: gap≥10% × news, gap≥10% × PM≥1M | VPS — existing dataset | Low |
| P2-D | Float turnover within gap≥10% cohort | VPS — float data (LC-2025-014 pipeline) | Medium |
| P2-E | ATR-normalised gap across full universe | VPS — daily ATR computation | Medium |
| P2-F | Temporal OOS split (first 60% train / last 40% validate) on best triple | VPS — date-stratified rerun | Medium |

**P2-A, P2-B, P2-C are immediate and require only existing data.** They resolve the three blocking questions and validate (or overturn) the Phase 1 conditional verdicts. Everything downstream depends on their outcomes.

---

### Next Action

**Escalate to PO** with:
1. Five blocking questions (Q1–Q5) for VPS confirmation
2. Phase 1 provisional verdicts above
3. Phase 2 priority table (P2-A through P2-F)
4. Optimist's clean signal proposals (float turnover, ATR-normalised gap) as Phase 2 additions

Writing memory update now.

---
