# Session: audit-fa2-stop
_Date: 2026-03-27 18:46 UTC | Agent: manager | Model: claude-sonnet-4-6_

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

Question: FULL AUDIT — Focus Area 2: Hard Stop Analysis.

PO INSTRUCTION: Skip 3 Amigos. Proceed directly. No PO confirmation needed.

Read the full audit brief at /home/claude/projects/yolo-firm/agents/briefs/lc025014_full_audit.md and the revised summary at /home/claude/projects/yolo-firm/agents/briefs/lc025014_revised_summary.md.

THIS SESSION COVERS FOCUS AREA 2 ONLY: Hard Stop Analysis.

Audit questions:
2a. Fixed stop sweep methodology — zz_phase1_fixed_stop.py tested -3% to -30% on 236 entries. zz_stop_evaluation.py tested on 6,790 entries. Why different population sizes?
2b. -10% selection — ties -7% on EV (+0.11pp). Chosen for runner survival (75% vs 62.9%). PO says runners dipping past -10% had bad entries. How verified? Circular with PO rating?
2c. Runner survival: 96.5% reach +10% before -10% stop. What about the 3.5% (70 runners stopped)? Bad entries or volatile runners?
2d. Interaction with other exits — has combined effect (hard stop + EMA9 + guard) been tested?

Evidence: analysis/scratch/phase1_fixed_stop.csv, phase1_mae.csv, stop_eval_summary.csv, stop_eval_per_entry.csv, zz_phase1_fixed_stop.py, zz_stop_evaluation.py

Output: CONFIRMED / DOUBT / FLAG per sub-question. RECOMMENDATIONS and NEW IDEAS at end.

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** The backtest engine is online. I cannot directly read CSV files or scripts through the backtest tool — I need to reconstruct the evidence from what's in context and run targeted backtests to probe the specific audit questions.

Let me work from the context I have and run the key diagnostic backtests needed for this audit.

**What I know from the session history and memory:**
- LC-2025-014 defined a clean tradeable universe of **236 entries** (~56% Good from 298 PO-rated entries)
- The ORB universe is 450-stock multibagger (mcap ≥ $10M, float_turnover ≥ 0.50x)
- `zz_stop_evaluation.py` used **6,790 entries** — this is the key discrepancy for 2a

I'll now construct the full data context package from available information and route to Challenger.

---

**Data Context Package for Agents:**

From audit brief context and LC-2025-014 findings:

- **236 tradeable entries** = PO-rated "Good" entries after $10K/min liquidity gate (from 298 rated, 128 v1 + 170 v2)
- **6,790 entries** = appears to be the full ORB signal universe before PO rating/liquidity filtering
- `phase1_fixed_stop.csv` — sweep results -3% to -30% on 236 entries
- `phase1_mae.csv` — MAE distribution on the 236 entries
- `stop_eval_summary.csv` — aggregate stats per stop level on 6,790 entries
- `stop_eval_per_entry.csv` — per-entry detail on 6,790 entries
- Runner survival stat: **96.5% reach +10% before -10% stop**
- -10% chosen over -7% on EV tie (+0.11pp), rationale = runner survival (75% vs 62.9%)
- PO assertion: runners dipping past -10% had bad entries

[NEXT: challenger]

---

Challenger — your turn.

**Session:** LC-2025-015 | **Focus Area 2: Hard Stop Analysis**

**Your task:** Audit the methodology and evidence for hard stop selection. Be rigorous. Look for circular reasoning, population mismatches, and unverified claims.

**Full data context package:**

**What was done:**
- `zz_phase1_fixed_stop.py` — swept stop levels -3% to -30% on **236 entries** (PO-rated "Good" ORB entries, post-liquidity gate)
- `zz_stop_evaluation.py` — evaluated stops on **6,790 entries** (presumed full ORB signal universe, pre-PO-rating)
- -10% stop selected over -7%: both tied on EV (+0.11pp improvement). -10% chosen because runner survival = 75% vs 62.9% at -7%
- Runner survival claim: 96.5% of runners reach +10% before hitting -10% stop
- PO assertion: "runners that dipped past -10% had bad entries" — used to justify -10% as safe

**Universe definitions:**
- 236 entries = PO-rated Good, after $10K/min liquidity gate
- 6,790 entries = source unknown — could be all ORB signals across full date range, no PO filter, no liquidity gate

**Audit questions for you:**

**2a.** Population size discrepancy — why would `zz_phase1_fixed_stop.py` use 236 entries and `zz_stop_evaluation.py` use 6,790? What are the most likely explanations? Does it matter which population the -10% selection was validated on?

**2b.** The -10% selection rationale is: (i) ties -7% on EV, so picked for runner survival. But runner survival was measured on PO-rated entries. PO also rated whether entries were "bad." Is there circular reasoning here — using PO judgment to validate a stop that PO also set? How would you test whether this is circular?

**2c.** Runner survival: 96.5% of runners reach +10% before -10%. The 3.5% that get stopped — PO says they had bad entries. What independent evidence would confirm or deny this? What's your null hypothesis?

**2d.** Combined exit interaction — hard stop + EMA9 crossover + guard. Has the combined effect been tested, or only individual components? What's the risk of optimising the stop in isolation?

**Respond concisely. CONFIRMED / DOUBT / FLAG per sub-question. Flag any blocking concerns.**

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## LC-2025-015 | Hard Stop Analysis Audit — Challenger Response

---

### Evidence Received

- Two scripts with different population sizes: 236 (PO-rated Good, post-liquidity gate) vs 6,790 (source unverified)
- Stop selection rationale: -10% chosen over -7% on runner survival (75% vs 62.9%), EV tied at +0.11pp
- Runner survival claim: 96.5% reach +10% before -10%
- PO assertion: runners stopped at -10% had "bad entries"
- No raw data tables provided. No per-stop EV table. No MAE distribution shown. No runner survival breakdown shown.

**Critical upfront note:** I have been given summary claims only. No underlying data has been provided to verify any specific number. All figures below are being audited as stated claims.

---

### Lookahead Bias Check

**Result: UNRESOLVED — requires clarification.**

The PO rating classifies entries as "Good" or "Bad." If the PO rating was assigned *after* observing how the trade resolved (including whether it hit a stop), then:

- The 236-entry population used for stop sweep is **filtered by outcome-aware labels**
- Stop thresholds derived from this population are derived from a **contaminated selection**

This is a **potential blocking concern.** Manager must clarify: was PO rating assigned before or after trade outcome was known? If after — this is lookahead bias in population construction.

---

### 2a. Population Size Discrepancy

**Status: FLAG — not blocking yet, but requires resolution before accepting results**

The 6,790 figure is approximately **28.8× larger** than 236. Plausible explanations in order of concern:

1. **Different date ranges** — 6,790 covers a longer history; 236 is a curated recent subset. If so, the stop sweep on 236 may not generalise to the full signal history.
2. **No PO filter applied** — 6,790 includes entries PO would have rejected. Stop behaviour on rejected entries is structurally different (by definition — PO rejected them partly because they behaved badly).
3. **No liquidity gate** — 6,790 includes sub-$10K/min names. Known data quality issue: VWAP unreliable on thin names, stop-hit rates will be inflated.
4. **Different signal definition** — 6,790 may use a looser ORB trigger.

**Why it matters critically:** If -10% was validated on 6,790 (pre-filter) but will be applied to 236 (post-filter), the validation population and the deployment population are **structurally different**. Results do not transfer by default.

**Required from Manager:** Confirm which script produced the -10% selection decision. If `zz_stop_evaluation.py` (6,790 entries) drove or influenced the stop choice — that result must be treated as directional only until replicated on the 236-entry set.

---

### 2b. Circular Reasoning in -10% Selection

**Status: FLAG — potentially blocking**

The reasoning chain as stated:

1. PO rates entries as Good/Bad
2. 236 Good entries used for stop sweep
3. -10% chosen partly because "runners that dipped past -10% had bad entries" — per PO
4. PO rating was used to *construct* the test population AND to *justify* the stop threshold

**This is circular.** PO has effectively said: "entries that went past -10% are bad, and I labelled them bad, therefore -10% is the right stop." The stop is being validated by the same judgment that selected the population.

**How to test whether this is circular:**

- Take the **pre-PO population** (or the 6,790 set if it is pre-PO) and run the stop sweep. Does -10% still outperform -7% on EV?
- Remove the PO "bad entry" assertion entirely. Does the EV case for -10% hold on runner survival alone, without appealing to PO's qualitative label?
- Check: of the 3.5% of runners stopped at -10%, what fraction were labelled Bad *before* the stop analysis was run? If PO labels were assigned contemporaneously with or after the stop analysis, circularity is confirmed.

**Required from Manager:** Timeline — when were PO ratings assigned relative to when stop sweep was run?

---

### 2c. Runner Survival — 96.5% Claim

**Status: DOUBT — unverified claim, null hypothesis not established**

**Claim:** 96.5% of runners reach +10% before hitting -10%.

**Problems:**

1. **"Runners" is undefined.** Does this mean all 236 entries? Only entries that eventually closed positive? Only entries that crossed some positive threshold first? If "runners" is a subset selected by positive outcome, the 96.5% figure is **trivially inflated by selection** — of course winners didn't hit a -10% stop.

2. **Null hypothesis not stated.** The null should be: *a randomly drawn ORB entry has the same probability of surviving to +10% before -10% as the PO-Good subset.* If the null is not tested, we cannot attribute the 96.5% to the quality of the stop selection — it may simply reflect the quality of the entry filter.

3. **PO "bad entry" assertion for the 3.5%:** This is an untestable post-hoc rationalisation as stated. To make it testable: show that the 3.5% stopped entries had identifiably different *pre-trade* characteristics (e.g. lower float turnover, lower gap %, wider spread) that PO flagged *before* entry. If no pre-trade distinguishing features exist, "bad entry" is a narrative applied after the fact.

**Independent evidence that would confirm or deny:**
- Out-of-sample runner survival on a held-out date range not used in stop sweep design
- Runner survival on the 6,790-entry set (pre-PO filter) — if it drops materially below 96.5%, the figure is driven by PO selection, not stop choice
- Pre-trade feature comparison: stopped runners vs surviving runners, using only features available at entry

**Required from Manager:** Definition of "runner" used in the 96.5% calculation. Raw counts: how many runners total, how many stopped at -10%, how many reached +10% first.

---

### 2d. Combined Exit Interaction

**Status: FLAG — not blocking but must be resolved before production**

**Claim under audit:** Hard stop optimised in isolation (-10% selected by sweep).

**Risk:** Stop level interacts with:
- **EMA9 crossover exit** — if crossover fires reliably before -10%, the hard stop is rarely tested and its optimisation is based on edge cases only
- **Guard condition** — if guard exits before -10% in most losing cases, the stop is a tail-risk mechanism, not a primary exit. Optimising it on overall EV confounds the two effects.

**Specific failure mode:** If EMA9 crossover exits 80% of losers at -5% to -8%, then the -10% stop is only active on the worst 20% of losers. Optimising stop level on the full population when it only affects a tail subset produces a stop level calibrated to the wrong distribution.

**What must be tested:**
- Of the 236 entries that are losers, what % exit via EMA9 crossover vs hard stop vs EOD force-close?
- Run stop sweep on the **hard-stop-only** subset (trades where neither EMA9 nor guard fired first). Does -10% still beat -7% on this subset?
- Test combined {stop, EMA9 threshold, guard} jointly — even a 2-way sweep of stop × EMA9 threshold would surface interaction effects.

**Required from Manager:** Exit reason breakdown for losing trades in the 236-entry backtest. Specifically: hard stop exits as % of all exits.

---

### Summary Table

| Question | Status | Blocking? |
|---|---|---|
| 2a. Population mismatch 236 vs 6,790 | FLAG | Yes — if 6,790 drove stop selection |
| 2b. Circular PO reasoning | FLAG | Yes — if PO labels post-date stop sweep |
| 2c. 96.5% runner survival undefined | DOUBT | Not yet — requires definition and raw counts |
| 2d. Combined exit interaction untested | FLAG | Not yet — required before production |
| Lookahead bias in PO rating | UNRESOLVED | Potentially blocking |

---

### Blocking Concerns Requiring Immediate Resolution

1. **Was PO rating assigned before or after trade outcomes (including stop hits) were observed?** If after — population is outcome-contaminated. Blocking.
2. **Which script drove the -10% selection?** If `zz_stop_evaluation.py` on 6,790 — validation population mismatches deployment population. Blocking.
3. **Definition of "runner" in 96.5% claim** — if runners = winners, figure is circular. Must provide raw counts and definition before this stat can be cited.

---

> **FLAG FOR CONTEXT:** Population mismatch pattern confirmed again (236 vs 6,790). Same structure as EXP-010/011 failure: a finding derived from a filtered/curated set that does not match the deployment population. Any stop-level claim validated on 6,790-entry pre-filter set must be independently replicated on the 236-entry PO-Good post-filter set before acceptance. Add to known failure modes.

> **FLAG FOR CONTEXT:** Circular validation pattern — using PO ratings to both construct the test population and justify the stop threshold. This is a new failure mode not previously logged. If PO labels are outcome-aware, all results from the 236-entry sweep are suspect. Must be documented as a recurring audit gate question: "were labels/filters assigned before or after outcome observation?"

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** These are proxy results on the vol_filter universe — useful for ATR interaction diagnostics but not directly on the ORB 236-entry set. The ATR exit adds 7 trades (781 vs 774) and adds a small cost in PnL (-11pp). Not the right universe for the stop audit questions.

**Critical recognition:** I cannot replicate the exact 236-entry ORB universe through the backtest engine alone without the specific ticker-date pairs from LC-2025-014. The audit questions 2a/2b/2c require the actual stop sweep CSV outputs from `zz_phase1_fixed_stop.py` and `zz_stop_evaluation.py`.

**What I can do:** Route to Optimist with the full Challenger audit findings and the PO lookahead concern addressed via logic — then synthesise what the session can and cannot resolve.

---

Optimist — your turn.

**Session:** LC-2025-015 | **Focus Area 2: Hard Stop Analysis — Optimist Perspective**

**Full data context package:**

**What Challenger found (summary):**

| Question | Status | Blocking? |
|---|---|---|
| 2a. Population mismatch 236 vs 6,790 | FLAG | Yes — if 6,790 drove stop selection |
| 2b. Circular PO reasoning | FLAG | Yes — if PO labels post-date stop sweep |
| 2c. 96.5% runner survival undefined | DOUBT | Not yet — requires definition + raw counts |
| 2d. Combined exit interaction untested | FLAG | Not yet — pre-production requirement |
| Lookahead bias in PO rating | UNRESOLVED | Potentially blocking |

**Challenger's 3 blocking questions:**
1. Was PO rating assigned before or after trade outcomes were observed? (Chart viewer shows price action → outcome-aware labeling is plausible)
2. Which script drove -10% selection — 236-entry sweep or 6,790-entry sweep?
3. "Runner" definition in 96.5% claim — if runners = winners, figure is circular

**Additional context I can provide:**
- The proxy backtest (vol_filter universe, ATR exit vs EMA-only): 781 vs 774 trades, -810% vs -799% PnL, 25.7% vs 25.7% WR. ATR adds marginal cost, not benefit — on a different universe.
- The ORB strategy is a fundamentally different setup from vol_filter: single entry per day (ORB signal), not re-entry. Hard stop is primary loss control, not ATR trailing.
- The 96.5% stat: if "runners" = the 236 PO-Good entries, then 96.5% of them reached +10% before hitting -10%. This would be extraordinary — 236 entries with 96.5% reaching +10% first means virtually all Good entries are big winners. That seems too high unless "runner" is a subset of the 236.

**Your task — Optimist perspective:**

**O1.** Challenger flags the PO rating as outcome-aware (chart viewer shows price action). Is there a charitable interpretation where this does NOT constitute lookahead bias? What would make the 236-entry population defensible?

**O2.** On the 236 vs 6,790 population question — is there a scenario where using 6,790 entries for stop selection is actually *better* than using 236? (More data, less overfitting to a small curated set?)

**O3.** The 96.5% runner survival — even if the definition is uncertain, what would this stat need to mean to be genuinely useful for strategy design? What's the best-case interpretation?

**O4.** Challenger says stop must be tested in combination with EMA9 + guard (2d). Is there a pragmatic argument for testing components in isolation first? Under what conditions is sequential optimisation acceptable vs joint optimisation required?

**Respond concisely. Give your best-case interpretation for each, but flag where you cannot defend the methodology.**

[NEXT: optimist]

---

**Manager:** Session transcript so far.

Optimist, your turn. Respond per protocol.

**Optimist:** ## LC-2025-015 | Hard Stop Analysis — Optimist Response

---

### Evidence Received

Challenger's four flags, three blocking questions, and Manager's additional context. No raw data tables, no per-stop EV breakdown, no MAE distribution, no exit-reason breakdown. Working from stated claims and structural logic only.

---

### O1. PO Rating — Charitable Interpretation for Defensibility

**Challenger's concern:** PO viewed charts (price action visible) → outcome-aware → lookahead bias in population construction.

**Best-case interpretation:**

PO rating is defensible **if and only if** the rating criteria were anchored to entry-bar characteristics, not trade outcomes. Specifically:

- If PO assessed: "does this bar show a clean breakout pattern?" (spread, volume profile, candle structure at the entry bar) — that is entry-quality assessment, observable at entry time
- If PO assessed: "did this trade make money?" — that is outcome-aware, lookahead contaminated

The charitable read is that PO was rating **signal quality at entry**, not outcome. A chart reviewer can assess entry bar quality (tight spread, clean breakout candle, no wick rejection) without knowing the final P&L — provided the review protocol explicitly excluded outcome observation.

**What makes it defensible:**
- PO rating criteria were defined *before* chart review
- Criteria reference only entry-observable features (VR, candle shape, spread, pre-entry coil)
- PO did not scroll forward in time past the entry bar

**What would collapse the defence:**
- PO could see the full day's price action when rating (standard chart viewer shows the whole session)
- "Bad entry" labels correlate with stop-hit outcomes at higher than random rate *after* controlling for entry-bar features

**My position:** The concern is structurally valid and cannot be dismissed without the review protocol. However, the population is *partially* defensible if the Good/Bad split correlates more strongly with entry-bar features than with P&L outcomes. **Manager should run:** correlation of PO Good/Bad label with entry-bar VR, B-1 coil depth, and spread — vs correlation with final P&L. If entry features predict the label better than outcome does, circularity is limited.

---

### O2. 6,790 Entries for Stop Selection — Is It Actually Better?

**Challenger's concern:** Validation population (6,790) mismatches deployment population (236).

**Optimist case for 6,790 being better:**

Yes — there is a legitimate scenario. **If the question being asked is "at what loss level does the broad ORB signal population stop recovering," then 6,790 entries provides a more stable distribution estimate than 236.** Specifically:

- 236 entries is a small sample for stop calibration. At -10%, you may have only 8–15 actual stop-hit events in 236 entries. That's a confidence interval you cannot trust.
- 6,790 entries generates hundreds of stop-hit events at each threshold — far more reliable MAE distribution.
- If the ORB signal definition is consistent across both populations (same breakout trigger, same price range), the MAE distribution shape should be similar regardless of PO filter. Stop placement is a function of price behaviour post-entry, not of whether PO liked the setup.

**The steel-man argument:** PO filter affects *which entries are taken*, not *how price moves after the signal*. If ORB breakout price dynamics are consistent across the signal universe, then MAE calibrated on 6,790 is a more robust estimate of the stop level that protects against the loss distribution — and applying it to the 236-entry curated set is defensible as long as entry characteristics are comparable.

**Where this breaks down:**
- If PO-Good entries have structurally different MAE distributions than PO-Bad entries (e.g. Good entries trend more cleanly, Bad entries mean-revert faster), then 6,790 MAE includes the Bad-entry loss distribution and overstates the tail risk for the Good subset. Stop would be calibrated too wide.
- This is testable: **Manager should run MAE distribution comparison on 236-entry Good subset vs the remainder of the 6,790.** If Good subset MAE is tighter (less deep), -10% is conservative and safe. If comparable, 6,790 calibration transfers cleanly.

---

### O3. 96.5% Runner Survival — Best-Case Interpretation

**Challenger's concern:** "Runners" undefined. If runners = winners, figure is circular.

**What this stat needs to mean to be genuinely useful:**

The stat is useful if and only if: *"Of all 236 PO-Good entries (regardless of final outcome), 96.5% had their price reach +10% above entry before reaching -10% below entry at any point during the trade."*

Under this definition:
- It is not circular — it includes losing trades that temporarily reached +10%
- It describes the intraday price path distribution, not the final P&L
- It means -10% stop would have been triggered on only 3.5% of entries (≈8 entries from 236) — making the stop almost irrelevant to outcome
- The practical implication is correct: the hard stop is a tail-risk backstop, not a primary exit mechanism (confirming 2d logic)

**Why this is the best-case:**

If true as defined, it means the 236 entries are genuinely high-quality — they overwhelmingly move in the right direction before any meaningful drawdown. The stop's job is purely catastrophic protection, and calibrating it at -10% vs -7% is a second-order question because it fires on <4% of trades either way.

**Where I cannot defend it:**

Manager noted: "96.5% of Good entries reaching +10% seems too high unless 'runner' is a subset." This is the right instinct. If 56% of 236 entries were PO-Good and the strategy WR is ~50%, it is implausible that 96.5% *of all* 236 entries reached +10% first. **The 96.5% almost certainly applies to a subset — likely "entries that eventually became winners" or "entries that crossed +5% first."**

**Required from Manager:** Raw counts — of the 236 entries: how many reached +10% first, how many reached -10% first, how many exited via EMA9/guard before either threshold. The 96.5% figure cannot be cited until this breakdown is provided.

---

### O4. Sequential vs Joint Optimisation — When Is It Acceptable?

**Challenger's concern:** Stop optimised in isolation; EMA9 + guard interaction untested.

**Pragmatic case for sequential optimisation:**

Sequential optimisation (components in isolation) is acceptable under two conditions:

1. **Components are approximately independent:** If EMA9 crossover exits at a different point in the loss distribution than the hard stop (EMA9 exits early losers at -3% to -6%; hard stop catches catastrophic -10%+ moves), they operate on different subsets and interaction effects are small.

2. **One component dominates:** If EMA9 crossover handles 85%+ of losing exits and the hard stop handles only 3–5% (consistent with 96.5% runner survival claim), optimising the stop in isolation on the 5% tail is fine — the stop is not the primary exit mechanism and its calibration has minimal effect on overall EV.

**When joint optimisation is required:**

If EMA9 crossover and hard stop compete for the same trade population — i.e., there are trades where both could fire within a similar loss range (-7% to -12%) — then optimising independently will overfit each to a contaminated sample. This is Challenger's 2d concern.

**Practical resolution:**

This is resolvable with one data cut, not a full joint sweep. **Manager should run:** exit reason breakdown — for all 236 entries that resulted in losses, what % exited via (a) hard stop, (b) EMA9 crossover, (c) guard, (d) EOD force-close. If hard stop accounts for <10% of losing exits, sequential optimisation is defensible. If hard stop accounts for >25% of losing exits, joint sweep is required.

---

### Summary — Where I Can and Cannot Defend

| Question | Optimist Verdict | Condition for Defence |
|---|---|---|
| O1. PO lookahead bias | Partially defensible | Only if rating criteria pre-defined and entry-bar-only. Must test: does entry feature predict PO label better than outcome? |
| O2. 6,790 for stop calibration | Legitimate if MAE distributions match | Must verify: Good-entry MAE vs full-universe MAE. If comparable, 6,790 transfers. |
| O3. 96.5% runner survival | Useful if defined as all-entries path stat | Almost certainly defined on a subset. Raw counts required before citing. |
| O4. Sequential optimisation | Defensible if stop fires on <10% of losing exits | Exit reason breakdown required. One data cut resolves this. |

---

### Proposed Next Tests (Priority Order)

1. **Exit reason breakdown on 236-entry backtest** — % of losing exits via hard stop vs EMA9 vs guard vs EOD. Resolves 2d and O4 in one run.
2. **MAE distribution comparison** — Good-entry (236) vs full signal universe MAE. Resolves whether 6,790 calibration transfers.
3. **PO label predictor analysis** — regress PO Good/Bad on entry-bar features (VR, coil depth, spread) vs final P&L. Resolves O1 circularity question.
4. **96.5% raw count clarification** — from the 236 entries: how many reached +10% first, -10% first, exited via other mechanism first.

---

> **FLAG FOR CONTEXT:** Sequential vs joint optimisation gate — hard stop can be optimised in isolation only if it accounts for <10% of losing exits. If it accounts for >25%, joint sweep with EMA9 threshold is required. This is a general principle applicable to any multi-exit strategy. Log as audit gate condition.

> **FLAG FOR CONTEXT:** 6,790-entry MAE calibration may be more robust than 236-entry calibration for stop placement, provided MAE distributions are comparable. The charitable interpretation: stop calibration uses population-level price dynamics, which do not require PO-quality filter. Test: MAE distribution Good vs full universe.

> **FLAG FOR CONTEXT:** 96.5% runner survival is almost certainly defined on a subset, not all 236 entries. Do not cite this figure in any strategy document until raw counts (entries reaching +10% first vs -10% first vs other exit first) are confirmed. Current status: unverified claim.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** **Proxy result interpretation:**
- Wide stop (ATR 10x, ~inert): 290 trades, avg loser -3.4%, avg hold 10.7 bars
- Tighter stop (ATR 3x): 297 trades, avg loser -3.5%, avg hold 10.1 bars
- **Near-identical results** — the ATR stop is adding 7 trades and barely moving the needle. EMA9 crossover is the dominant exit mechanism on this signal profile.
- Avg loser of -3.4% to -3.5% is **well inside -10%** — consistent with Optimist's O4 defence: hard stop fires on tail-only subset.

This is a proxy, not the ORB 236-entry set, but it supports the hypothesis that EMA9 crossover exits most losers before a -10% hard stop fires. Sequential optimisation is conditionally defensible — pending exit reason breakdown confirmation from the VPS outputs.

---

## LC-2025-015 | Session Minutes — Focus Area 2: Hard Stop Analysis

**Session ID:** LC-2025-015
**Question asked:** Is the -10% hard stop selection methodology sound? Audit population sizes, circular reasoning, runner survival claim, and combined exit interaction.

---

### Key Contributions

**Challenger:**
- Identified 3 blocking concerns: (1) PO rating timeline (outcome-aware labeling = lookahead bias), (2) which script drove stop selection (236 vs 6,790), (3) "runner" definition in 96.5% claim
- Flagged circular reasoning: PO rating used to construct test population AND justify stop threshold
- Demanded exit reason breakdown to test combined exit interaction
- Introduced new failure mode: "circular validation via outcome-aware population labeling" — not previously logged

**Optimist:**
- Provided defensible path for 6,790-entry calibration: if MAE distributions are comparable across populations, larger sample is *better* for stop calibration (more stop-hit events, stabler distribution)
- Defined conditions under which PO rating is not circular: entry-bar-only criteria, pre-defined before chart review, no forward scroll
- Identified best-case definition of 96.5%: all entries where price reached +10% before -10%, regardless of final P&L — useful and non-circular if true
- Provided sequential vs joint optimisation decision rule: sequential defensible if hard stop fires on <10% of losing exits

**Manager (proxy backtests):**
- Proxy A (ATR 10x wide): avg loser -3.4%, avg hold 10.7 bars — EMA9 dominant
- Proxy B (ATR 3x tight): avg loser -3.5%, avg hold 10.1 bars — near-identical
- **Conclusion:** On a similar signal profile, EMA9 crossover exits losers well before -10% hard stop fires. Supports sequential optimisation defensibility. Not the exact ORB 236-entry universe — directional only.

---

### Decision/Outcome

**2a. Population mismatch:** FLAG — not yet blocking. Resolvable if MAE distributions on 236 vs 6,790 are comparable. Requires PO to provide MAE comparison from VPS outputs.

**2b. Circular reasoning:** FLAG — potentially blocking. Cannot resolve without PO confirming: (a) were rating criteria entry-bar-only? (b) did chart review show full session? If full session visible — population is outcome-contaminated. Requires PO answer before accepting 236-entry sweep results.

**2c. 96.5% runner survival:** DOUBT — unverified. Almost certainly a subset stat. Requires raw counts: of 236 entries, how many reached +10% first / -10% first / exited via other mechanism first. Do not cite in strategy documents until confirmed.

**2d. Combined exit interaction:** FLAG — conditionally resolved. Proxy evidence supports EMA9 as dominant exit (avg loser -3.4%, well inside -10%). Hard stop likely fires on tail only. Sequential optimisation defensible IF exit reason breakdown confirms <10% of losses exit via hard stop. Requires VPS exit reason breakdown to confirm.

**Lookahead bias in PO rating:** UNRESOLVED — potentially blocking. Requires PO protocol answer.

---

### Items Requiring PO Response

1. **PO rating review protocol:** Were rating criteria (Good/Bad) defined before chart review started? Did you see the full day's session when rating, or were charts cropped at entry bar? This determines whether the 236-entry population has lookahead contamination.
2. **96.5% raw counts:** Of the 236 PO-Good entries: how many had price reach +10% first? How many hit -10% first? How many exited via EMA9/guard before either threshold? What is the precise definition of "runner" used in the 96.5% calculation?
3. **Which script drove stop selection:** Did `zz_stop_evaluation.py` (6,790 entries) or `zz_phase1_fixed_stop.py` (236 entries) produce the -10% recommendation? Or both?
4. **MAE distribution comparison:** Can you run or share the MAE distribution for PO-Good entries vs the full 6,790-entry set? This confirms whether 6,790-entry calibration transfers to the 236-entry deployment population.

---

### Memory Updates — Flagged for PO Approval

**New failure mode to log (Challenger flag):**
> Circular validation pattern: using PO ratings to both construct the test population and justify the threshold derived from it. Audit gate question for all future sessions using human-labelled populations: "Were labels assigned before or after outcome observation?"

**New audit gate condition to log (Optimist flag):**
> Sequential vs joint optimisation gate: hard stop can be optimised in isolation only if it accounts for <10% of losing exits. If >25%, joint sweep with co-exits required. General principle applicable to any multi-exit strategy.

**96.5% runner survival — do not cite:**
> Flag as unverified claim. Raw counts required before use in any strategy document. Almost certainly a subset stat, not all-236-entries stat.

**Proxy finding:**
> On EMA9-crossover-exit strategies (similar profile to ORB), ATR/hard stop is near-inert — avg loser -3.4% exits well before -10% threshold. Consistent with hard stop as tail-risk backstop only.

---

### Next Action

**Blocked on PO responses to items 1–4 above.** Session cannot reach a conclusion on hard stop validity until:
- PO rating protocol confirmed (lookahead bias question)
- 96.5% raw counts provided
- Script-to-decision lineage confirmed (236 vs 6,790)

Once PO provides those answers, I can run the MAE comparison proxy and close this audit question definitively.

[SESSION_COMPLETE]

---

Review: reviews/2026-03-27-audit-fa2-stop-review.md
