# Session Review: kill-criterion
_Date: 2026-03-31 10:46 UTC | Model: claude-sonnet-4-6_

## Manager Synthesis

## Session Continue — LC-2025-037

Statistician has delivered. Clean, well-structured output. Before closing, let me assess the substance and check for any issues requiring escalation.

---

### Assessment of Statistician Output

**Accepted without change:**
- Exact binomial test (not Wilson CI upper bound) — correct reframing. Wilson CI < 5% was testing the wrong null.
- Bonferroni correction at 3 formal checkpoints → per-checkpoint α = 0.0125. Conservative but appropriate for kill decisions where Type 1 error (false kill) is costly.
- n=30 structural insufficiency is mathematically correct. P(X=0 | p=0.089, n=30) ≈ 0.071 >> 0.0125. n=30 cannot support a formal kill decision.
- Minimum n=48 for first possible formal kill (0-wins path). Clean derivation.
- 14.3% figure in prior spec confirmed wrong. Correct FWER = 4.9% with Bonferroni.

**One note on checkpoint count:** Statistician correctly identifies that only 3 checkpoints (n=60, 90, 106) are formal kill points. Bonferroni denominator should be 3, not 4 → per-checkpoint α = 0.05/3 = **0.0167**, not 0.0125. The summary table says "Bonferroni, 3 formal checkpoints" but the per-checkpoint α quoted is 0.05/4 = 0.0125. This is a minor inconsistency — the Statistician excluded n=30 from the formal count in prose but retained the 4-checkpoint alpha. This should be flagged for PO resolution: use α=0.0167 (3 checkpoints) or α=0.0125 (conservative, treats n=30 as if it were formal). The kill thresholds may shift slightly under α=0.0167.

**S5 open flag:** Accepted. Kill criterion cannot be locked until S5 baseline precision is confirmed.

---

### Session Close — LC-2025-037

**Question asked:** Design a statistically coherent kill criterion for the paper trading spec — resolve the conflict between primary kill criterion (Wilson CI) and supplementary 0-wins rule.

**Key contributions:**
- **Statistician:** Full kill criterion redesign — switched from Wilson CI to exact binomial test against pre-specified null (H₀: p ≥ 8.9%). Computed Bonferroni-corrected thresholds at each checkpoint. Proved n=30 is structurally insufficient for formal kill. Derived minimum n=48. Resolved the Challenger conflict by placing n=30 in "early warning" regime only.

**Decision/outcome:**
- Primary kill test: **exact binomial, one-sided, H₀: p ≥ 8.9%**
- Formal checkpoints: **n=60 (≤2 wins), n=90 (≤3 wins), n=106 (≤4 wins)**
- n=30: **early warning only — 0 wins → PO flag, not a kill**
- Per-checkpoint α: **0.0125 (conservative, 4-checkpoint denominator)** — OR — **0.0167 (3-checkpoint denominator, excluding n=30)** → PO to resolve
- Family-wise α: ≤ 5% under either choice
- Prior "14.3%" figure: **deleted**
- **Spec cannot be locked until S5 confirmed**

**Next action:**
1. PO to resolve the α denominator question (3 vs 4 checkpoints) — minor but affects exact threshold values
2. PO to confirm S5 baseline precision before locking kill criterion numbers
3. Once S5 confirmed, Manager to recompute win thresholds at each checkpoint if baseline ≠ 8.9%

**Memory updates:** None required this session — kill criterion design is a spec artefact, not a persistent research finding.

**Doc updates:** Kill criterion table is spec-ready pending S5 and α denominator resolution. Paper spec document to be updated by PO.

[SESSION_COMPLETE]

---
_Session log: session-log/2026-03-31-kill-criterion.md_
