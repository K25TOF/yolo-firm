# Session Review: audit-fa2-stop
_Date: 2026-03-27 18:52 UTC | Model: claude-sonnet-4-6_

## Manager Synthesis

**Proxy result interpretation:**
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
_Session log: session-log/2026-03-27-audit-fa2-stop.md_
