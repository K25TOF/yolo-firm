# Entry Pattern Research Proposal — LC-2025-041

_Session: LC-2025-041 v2/v3 | Date: 2026-03-31 | Optimist contributed. Challenger/Statistician/ExecRealist sessions crashed (API overload — their concerns addressed by Manager below)._

---

## The Problem

The scanner + VWAP filter correctly identifies runner days (80.8% Good rate from 09:30, validated OOS). But entry at 09:35 or 09:40 is too late — 67% of trades hit the -10% hard stop. The move happens from the 09:30 open but the entry catches the wrong part of the intraday pattern.

**Signal quality is high. Entry timing destroys the edge.**

---

## PO Hypothesis: Four Intraday Scenarios

| Scenario | Pattern | Entry approach |
|---|---|---|
| 1. Straight runner | Gap up, keeps running, no pullback | Enter immediately — rare |
| 2. Spike-pullback-breakout | Spikes, pulls back below open, finds support, reverses, breaks out | Wait for pullback completion |
| 3. Tank-reversal-breakout | Tanks from open (profit-taking), finds floor, reverses, breaks through | Wait for floor confirmation |
| 4. Failed runner | Starts like 2/3 but never recovers | Do not enter |

**Key insight:** Scenarios 2 and 3 require waiting for a completed pullback before entry. Static timing (09:35) enters during or before the pullback — which is why 67% of trades immediately dip to the stop.

---

## Proposed Research: Feature Extraction + Pattern Classification

### Phase 1: Extract features from existing 192 trades (no new backtests)

**Pre-entry features (observable at or before entry time):**

| Feature | Formula | What it measures |
|---|---|---|
| F1.1 ORB gap at open | `(open_price - orb_high) / orb_high` | How far above/below breakout level stock opens |
| F1.2 ORB retest depth | `(min(bar_low[570:574]) - orb_high) / orb_high` | Deepest dip during ORB window |
| F2.1 Path slope | Linear regression slope on `bar_close[570:574]` / orb_high | Direction of price in first 5 min |
| F2.2 High-to-close ratio | `(max_high - close[574]) / (max_high - min_low)` in ORB window | Where price closed relative to ORB range |
| F2.3 Recovery ratio | `(close[574] - min_low) / (max_high - min_low)` in ORB window | **Core signal:** pullback-then-recovery pattern |

**Post-entry features (for retrospective labelling only — NOT available at entry time):**

| Feature | Formula | What it measures |
|---|---|---|
| F3.1 MFE/MAE ordering | Which comes first: +5% MFE or -5% MAE? | Distinguishes runner path from failure |
| F3.2 Early drawdown | `min(bar_low[575:580] - entry_price) / entry_price` | Immediate post-entry behaviour |
| F3.3 MFE_30bar | Already computed | Ultimate move quality |

### Phase 2: Assign pattern labels

| Pattern | Label rule |
|---|---|
| 1 — Straight runner | slope > 0 AND hc_ratio < 0.3 AND early_dd > -2% |
| 2 — Spike-pullback-recover | hc_ratio >= 0.5 AND recovery >= 0.6 AND orb_gap > 0 |
| 3 — Tank-floor-reversal | orb_gap < 2% AND slope < 0 AND recovery >= 0.6 |
| 4 — Failed runner | early_dd <= -5% AND MFE_30bar < 5% |

### Phase 3: Cross-tabulate patterns vs outcomes

For each pattern: count trades, Good rate (MFE >= 10%), mean PnL, stop-out rate. If labelling is working: patterns 1/2/3 should have materially higher Good rates than the 35% baseline.

### Phase 4: Test entry signal

**Primary hypothesis: "First new high after pullback"**

Enter when `bar_high > max(bar_high[570:574])` (ORB high) for the first time AFTER the trade has experienced a pullback of >= 2% from the opening print.

- **Non-lookahead:** Observable bar-by-bar in real time
- **Pattern-aware:** Waits for pullback completion (required for scenarios 2/3)
- **Entry price:** `bar_open` of the bar AFTER the confirmation bar
- **Timeout:** If no new high after pullback by 10:00 ET, skip (scenario 4 or stall)

---

## Known Risks (Manager's assessment, incorporating Challenger/Statistician concerns)

### Overfitting risk: HIGH
- 192 trades split 4 ways = ~48 per scenario. Below Statistician's n=50 minimum for reliable inference per group.
- 5+ features × 4 labels × threshold selections = massive free parameter space on a small sample.
- **Mitigation:** Pre-register ONE entry signal (the "first new high after pullback" rule) before running ANY data analysis. Test ONLY this signal. Do not sweep thresholds.

### Feature circularity risk: MEDIUM
- F3 features (post-entry) are used to create labels, then labels are used to evaluate the entry signal.
- **Mitigation:** The entry signal (Phase 4) uses ONLY pre-entry features (F1, F2). Post-entry features define the OUTCOME label, not the entry rule. This is standard — like using PnL to evaluate a signal that doesn't use PnL.

### Implementation feasibility: CONFIRMED
- All features are computable from 1-min OHLCV bars available in real time via Polygon
- "First new high after pullback" requires bar-by-bar scanning — achievable within a 1-second evaluation cycle
- Entry at bar_open after confirmation: requires detecting the confirmation bar's high and placing a market/limit order before the next bar opens

### Temporal validation: REQUIRED
- Phase 1-3 use all 192 trades (May 2025 - Mar 2026)
- Phase 4 MUST split: design on May-Dec 2025 (146 trades), validate on Jan-Mar 2026 (46 trades)
- 46 OOS trades is small but is what we have. Results must carry explicit wide CI.

---

## Recommended Execution Sequence

| Step | Task | Data | Effort | Dependency |
|---|---|---|---|---|
| **1** | Extract F1-F2 features from 192 trades | Existing bar data | Low (1-2h) | None |
| **2** | Descriptive analysis: feature distributions for Good vs Bad trades | Step 1 output | Low | Step 1 |
| **3** | Pre-register entry signal: "first new high after pullback" with 2% pullback threshold, 10:00 timeout | Written document | Zero | Before Step 4 |
| **4** | Compute entry signal on design set (May-Dec 2025): when does it fire, at what price, on how many trades? | Existing bar data | Medium | Steps 1, 3 |
| **5** | Walk trades from signal entry: PnL, exit type, Good rate | Step 4 output | Medium | Step 4 |
| **6** | Validate on OOS (Jan-Mar 2026) | Same code, different dates | Low | Step 5 |
| **7** | Multi-agent validation session (Challenger + Statistician) | Steps 5-6 results | Medium | Step 6 |

**Estimated total effort:** 1-2 days of data analysis + 1 validation session.

---

## Success Criterion

Pre-specified before any data analysis:

1. **Entry signal fires** on >= 40% of L2-qualifying trades (not too selective)
2. **Mean PnL net >= 0%** on signal-entry trades (breakeven or better after 2% cost)
3. **Good rate >= 50%** on signal-entry trades (above the 35% full-stack baseline)
4. Results hold on OOS (Jan-Mar 2026) within CI of design set

If all four hold: the pattern-aware entry is validated and replaces the static 09:35 entry in the paper spec.

If any fail: document which and why. The signal research finding (scanner + VWAP identifies runner days) remains valid — the entry timing problem requires a different approach.

---

_Note: Challenger and Statistician sessions crashed due to API overload. Their concerns (overfitting, free parameters, pre-registration, temporal validation) are addressed in the "Known Risks" section. A formal validation session with both agents is Step 7 in the execution sequence — no conclusion is accepted without their sign-off._
