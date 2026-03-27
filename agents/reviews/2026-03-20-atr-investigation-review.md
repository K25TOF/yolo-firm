# Session Review: atr-investigation
_Date: 2026-03-20 10:03 UTC | Model: claude-sonnet-4-6_

## Manager Synthesis

## LC-2025-013 (Continuation) — Synthesis on ATR Precision Investigation

Challenger has done sharp work. Before I can synthesise, I need to resolve three factual gaps Challenger has correctly flagged. Let me run the numbers directly.

**What I need to resolve:**
1. The ATR(T) precision column — Challenger cannot verify the circular dependency ruling without it
2. The inclusive precision story — Challenger's recomputation shows a different (non-monotonic) curve
3. ATR lookback N and method — not stated in the data provided

I don't have direct access to the raw script output beyond what was provided in the session context. Let me work with what can be derived, and flag what requires PO to pull from the VPS.

**What I can resolve from the data already in context:**

**Inclusive precision — Challenger's recomputation is correct and I can verify it:**

| Threshold | Movers | N_without | Inclusive Prec | Exclusive Prec |
|---|---|---|---|---|
| ALL | 926 | 18,769 | 4.93% | 6.1% |
| ≥0.3% | 459 | 8,693 | 5.28% | 7.1% |
| ≥0.5% | 240 | 4,159 | 5.77% | 8.2% |
| ≥0.7% | 109 | 1,941 | 5.61% | 8.4% |
| ≥1.0% | 29 | 534 | 5.43% | 8.7% |

Challenger's arithmetic checks out. The inclusive curve peaks at ≥0.5% (5.77%) and reverses. This is a genuine finding that changes the picture.

**What I cannot resolve without PO pulling VPS data:**
- ATR(T) precision column (verifying the +1.4pp delta claim)
- ATR lookback N and method

---

## Synthesis — LC-2025-013 ATR Precision Finding

**The picture is more complex than either agent's initial read. Here is the integrated assessment:**

### What is settled

- **Precision lift is real but definition-dependent.** Under exclusive precision (Movers/Movers+FalseBK), the lift is 6.1%→8.7%. Under inclusive precision (Movers/N_without), it is 4.93%→5.77%, peaking at ≥0.5% then reversing. Both are arithmetically correct — they answer different questions.
- **≥1.0% threshold is dropped.** Challenger's CI calculation is sound: lower bound 5.7% falls below unfiltered baseline 6.1%. Not statistically credible. Removed from all recommendations.
- **≥0.7% is borderline.** CI lower bound 6.9% clears baseline but marginally. Insufficient to recommend.
- **≥0.3% and ≥0.5% are statistically credible** under both exclusive and inclusive precision metrics.
- **The middle-ground exclusion is the key open question.** Challenger correctly identified that Middle-ground events are excluded from the precision denominator. Whether this exclusion is principled (Middle-ground events are genuinely non-informative for this filter decision) or artefactual (they're excluded because they're inconvenient) determines which precision metric is correct.

### What requires PO to pull from VPS

Two items are blocking full closure:

1. **ATR(T) precision column** — needed to independently verify the circular dependency ruling. The +1.4pp delta claim is asserted as resolved but Challenger has not seen the data. This is a legitimate audit flag.

2. **ATR lookback N and averaging method** — needed for both signal quality assessment and live implementation feasibility.

3. **Business rationale for Middle-ground exclusion** — is there a principled definition of "ignition event precision" that justifies excluding 0.5–3% peak moves? Or were they excluded because they fall in a grey zone?

---

## Updated Recommendation (pending VPS data pull)

**Working recommendation (conditional):**

| Threshold | Exclusive Prec | Inclusive Prec | CI Status | Verdict |
|---|---|---|---|---|
| ≥0.3% | 7.1% | 5.28% | Clean | **Use as minimum gate** |
| ≥0.5% | 8.2% | 5.77% | Clean | **Preferred if sample permits** |
| ≥0.7% | 8.4% | 5.61% | Marginal | Not recommended |
| ≥1.0% | 8.7% | 5.43% | Below baseline | **Dropped** |

The inclusive precision curve tells us something important: above ≥0.5%, we are not improving the true signal rate — we are mostly excluding Middle-ground events from the denominator. The optimal threshold under the inclusive metric is ≥0.5%, which aligns with Optimist's stretch recommendation.

---

## Items Requiring PO Action

**[BLOCKER — soft]:** Three data pulls needed from VPS before ATR filter can be adopted:

1. `python analysis/scratch/zz_ignition_phase1_2.py` ATR(T) precision column — or confirm the +1.4pp delta numbers
2. ATR lookback N and averaging method used in the script
3. Confirm the business rationale for Middle-ground exclusion (is this defined in the script, or a post-hoc choice?)

These are not blockers to closing this session — they are blockers to **adopting the ATR filter in production labelling**. We can close the session now and route these to PO as pre-conditions for the next step.

---

## Session Minutes — LC-2025-013 (ATR Precision Continuation)

**Question asked:** Does the ATR precision lift (6.1%→8.7%) survive (a) circular dependency test and (b) denominator artefact concern?

**Key contributions:**
- **Optimist:** Cleared circular dependency based on ATR(T) vs ATR(T-1) negligible delta. Argued mover:FalseBK ratio improves in absolute terms. Recommended ≥0.3% (working) and ≥0.5% (stretch). Requested middle-ground decomposition as one outstanding test.
- **Challenger:** Confirmed the denominator artefact is material — Middle-ground events are entirely excluded from precision denominator (verified by arithmetic). Computed inclusive precision (Movers/N_without) showing non-monotonic curve peaking at ≥0.5% then reversing. Dropped ≥1.0% on statistical grounds (CI lower bound below baseline). Flagged ATR(T) precision column as absent — circular dependency ruling unverifiable from data provided.

**Decision/outcome:**
- Precision lift is real but definition-dependent. Exclusive metric: 6.1%→8.7%. Inclusive metric: 4.93%→5.77%.
- ≥1.0% dropped from all recommendations (statistically unreliable)
- ≥0.7% not recommended (marginal CI)
- ≥0.3% and ≥0.5% are the only defensible thresholds
- Under inclusive precision, optimal threshold is ≥0.5% — consistent with Optimist's stretch recommendation but for a different reason (curve peaks there, not Optimist's sample-size trade-off argument)
- Three data items remain open before filter can be adopted in production

**Next action:**
- PO to pull from VPS: (a) ATR(T) precision column, (b) ATR lookback N + method, (c) Middle-ground exclusion rationale from script
- Once data provided, single follow-up turn to close remaining open items
- No new backtests required for this specific question — it is a data interpretation question

**Memory updates flagged:** Yes — pending PO approval:
- Record Challenger's denominator artefact finding (inclusive vs exclusive precision distinction)
- Record ≥1.0% threshold as dropped (statistical grounds)
- Record that ≥0.5% is optimal under inclusive precision
- Record three open data items required before ATR filter adoption

**FLAG FOR CONTEXT:** ATR precision lift confirmed but definition-dependent. Exclusive precision (Movers/Movers+FalseBK): 6.1%→8.7%, monotonic. Inclusive precision (Movers/N_without): 4.93%→5.77%, peaks at ≥0.5% then reverses. Three items block production adoption: ATR(T) precision data, ATR lookback/method, Middle-ground exclusion rationale.

=== SESSION CLOSED ===

[SESSION_COMPLETE]

---
_Session log: session-log/2026-03-20-atr-investigation.md_
