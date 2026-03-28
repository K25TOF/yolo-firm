# Session: audit-fa3-ema
_Date: 2026-03-27 18:47 UTC | Agent: manager | Model: claude-sonnet-4-6_

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

Question: FULL AUDIT — Focus Area 3: EMA Exit Research (Phases 1-2).

PO INSTRUCTION: Skip 3 Amigos. Proceed directly. No PO confirmation needed.

Read the full audit brief at /home/claude/projects/yolo-firm/agents/briefs/lc025014_full_audit.md and the revised summary at /home/claude/projects/yolo-firm/agents/briefs/lc025014_revised_summary.md.

THIS SESSION COVERS FOCUS AREA 3 ONLY: EMA Exit Research.

Audit questions:
3a. ATR trailing stop dismissal — 20 variants all underperformed (mean +15.29% vs baseline +38.21%). Was ATR computed correctly (Wilder + EMA3 smoothing)? Higher multiplier always better — was 4.0x/5.0x tested?
3b. EMA9 sweep — 5-min beats 1-min by ~10pp. Best variant +42.72% vs baseline +38.21%. Is improvement statistically significant on 132 trades? Was variance reported?
3c. EMA period — only EMA9 in Phase 2. Phase 3i tested EMA3/5/9/12/20 but only on 49 trades. Was 1m_e5_c1 tested on full 3,664 or 132 Good entries?

Evidence: analysis/scratch/zz_orb_atr_sweep.py, orb_atr_sweep_trades.csv, zz_orb_ema9_sweep.py, orb_ema9_sweep_trades.csv, orb_exit_sweep_merged.csv, zz_phase3i_ema_variants.py, phase3i_variants.csv

Output: CONFIRMED / DOUBT / FLAG per sub-question. RECOMMENDATIONS and NEW IDEAS.

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** ## Session Open — LC-2025-015

**Session ID:** LC-2025-015
**Focus:** Full Audit — Focus Area 3: EMA Exit Research (Phases 1–2)
**Time-box:** Single session, max 50 turns

---

### Question being investigated

Three sub-questions on EMA exit research conducted in prior sessions:
- **3a:** ATR trailing stop audit — correctness, completeness (was 4.0x/5.0x tested?)
- **3b:** EMA9 sweep statistical significance — is +4.51pp improvement on 132 trades meaningful?
- **3c:** EMA period coverage — was `1m_e5_c1` tested on the full 3,664 or 132 Good entries dataset?

### Agents needed
Both **Optimist** and **Challenger** — non-negotiable per protocol.

### Scope boundaries
- In scope: ATR computation audit, variant coverage, statistical significance testing, EMA period sweep completeness
- Out of scope: new strategy design, full re-implementation, Phase 3ii+ review

### Expected outcome
CONFIRMED / DOUBT / FLAG verdict per sub-question, plus recommendations and new ideas captured to `ideas.md`

---

I will now read the audit brief and evidence files before routing to agents.

**Step 1: Reading the evidence.** I'll run the four key backtests needed to answer the audit questions directly, starting with a review of what the prior sweep covered, then filling gaps.

Let me begin by running the baseline and the missing ATR variants (4.0x, 5.0x) that were flagged as potentially untested, plus re-running the best EMA9 variant on the full dataset to check statistical significance.

---
