# Pre-Registration: Entry Pattern Signal — LC-2025-041

_Status: **LOCKED** — Challenger and Statistician signed off (session: preregistration, 2026-03-31)_
_Two amendments incorporated per agent requirements._

---

## 1. Entry Signal Concept (LOCKED — cannot change after data is examined)

**"First new high after pullback":**
- Wait for a pullback from the opening print (bar_open[570])
- Enter when `bar_high[B] > max(bar_high[570:574])` (ORB high) for the first time AFTER the pullback
- Entry price: `bar_open[B+1]` (bar immediately following the signal bar)
- If no pullback occurs before a new high: signal does NOT fire (straight runners excluded)
- If signal does not fire before timeout: skip trade

---

## 2. Parameter Sweep (pre-specified ranges)

| Parameter | Values to test |
|---|---|
| Pullback depth threshold | 1%, 2%, 3%, 5% below bar_open[570] |
| Timeout | 10:00 ET (ts=600), 10:30 ET (ts=630), 11:00 ET (ts=660) |

**12 combinations total.** Tested on design set ONLY.

### BH Correction Procedure (Amendment 1 — Statistician requirement)

**Null hypothesis per combination:** H₀: Mean paired MAE difference (signal_MAE − baseline_MAE) = 0 for combination k. H₁: Mean paired MAE difference < 0 (signal entry has less adverse excursion).

**Test statistic:** Paired one-sample t-test on (signal_MAE[i] − baseline_MAE[i]) for each trade i where signal fires. One-sided (signal better).

**BH procedure:**
1. Compute p-value for each of the 12 combinations
2. Rank p-values ascending: p₍₁₎ ≤ p₍₂₎ ≤ ... ≤ p₍₁₂₎
3. Find largest k such that p₍ₖ₎ ≤ (k/12) × 0.05
4. All combinations with rank ≤ k are significant after BH correction
5. **Selection rule:** Among significant combinations, select the one with the largest S1 (mean MAE improvement) point estimate
6. **If no combination survives BH:** Report all as non-significant. Do not select a "best" combination. Entry signal FAILS.

**BH gates selection:** A combination can only be selected as "best" if its BH-corrected p-value is significant. BH is not decorative — it is the gate.

---

## 3. Comparison Baseline

Signal entry compared against static 09:35 entry (`bar_open[575]`) on the SAME trades. For each trade:
- Baseline entry: bar_open[575]
- Signal entry: bar_open[B+1] where B is the signal bar
- Same exit rules (ema9_5m_d3 + hard stop -10% + EOD), same 2% cost

Only trades where the signal fires are included in the comparison. Trades where the signal times out are excluded from the paired comparison but counted in the signal fire rate.

---

## 4. Success Criteria (entry quality, exit-independent)

| Criterion | Metric | Threshold | Applies to |
|---|---|---|---|
| **S1** | Mean MAE from signal entry | At least 3pp less negative than from 09:35 | Design set |
| **S2** | Hard stop (-10%) trigger rate from signal entry | At least 15pp lower than from 09:35 | Design set |
| **S3** | Mean MFE from signal entry | No more than 5pp lower than from 09:35 | Design set |

All three required on design set. OOS: same direction on all three (magnitude may differ due to smaller n).

---

## 5. Secondary Metrics (informational only — not pass/fail)

- Mean PnL net from signal entry vs 09:35 entry
- Good rate (MFE_30bar >= 10%) from signal entry vs 09:35 entry
- Signal fire rate (% of qualifying trades where signal fires before timeout)

---

## 6. Population

- **Design set:** May–Dec 2025 trades passing scanner (gap >= 15% + PM $vol >= $5M + pre-9:30 news) + VWAP filter (> +2% at ts=574). Fixed.
- **OOS set:** Jan–Mar 2026 same filter. Examined ONLY after design set analysis is complete.

---

## 7. OOS Execution Gate (Amendment 2 — Challenger requirement)

**OOS execution is CONDITIONAL on post-design-set power confirmation.** Before opening the OOS set:

1. Compute the empirical standard deviation of paired MAE differences (signal − baseline) from the design set
2. Confirm that at the observed design-set N and this std, the test has >= 80% power to detect a 3pp MAE improvement
3. If underpowered (std too large or N too small): OOS results are reported as DIRECTIONAL ONLY, not as a formal validation. The pre-registration explicitly permits this outcome.

The team is NOT locked into an OOS run if design-set results are statistically underpowered. Power confirmation is a gate between design-set completion and OOS execution.

---

## 8. What Can and Cannot Change

| Can change | Cannot change |
|---|---|
| Which parameter combination is selected (data-driven) | The signal concept (pullback then new high) |
| Interpretation of secondary metrics | The three success criteria and their thresholds |
| Research direction after results | The OOS population |
| | Adding new parameters not in the pre-specified sweep |

---

## Sign-Off

**Challenger:** Signed off with two amendments (BH procedure, OOS conditionality). Signal is non-lookahead. Parameter ranges pre-specified. Success criteria exit-independent. Design/OOS split clean.

**Statistician:** Signed off with BH procedure amendment. Power confirmation required before OOS. Sample size adequacy depends on empirical MAE std (unknown until Step 1).

**This document is LOCKED.** Steps 1-2 (feature extraction + descriptive analysis) may now proceed.
