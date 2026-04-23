# Workshop Story: Fix `vwap_session` to RTH-Reset, HLC3-Based VWAP

_Source: LC-2025-036 | Agents: Scout + Exec Realist + Challenger (7 spec flags resolved)_
_Status: Ready for Workshop. PO approved. Blocks Signal 3 (VWAP position at ORB close)._

---

## Context

The current `vwap_session` indicator in `signal_bars.py` accumulates VWAP from pre-market (04:00 ET) using Polygon's pre-aggregated per-bar VWAP field (`b["vw"]`). This diverges materially from what retail momentum traders see on TradingView, Webull, and ThinkorSwim — all of which default to RTH-reset VWAP starting at 09:30 ET using `(H+L+C)/3`. The fix aligns our backtester with the VWAP that retail traders actually react to, making `vwap_distance` and VWAP-based filters meaningful for strategy research.

**What's wrong today:**
- `vwap` column: Polygon per-bar VWAP (`b["vw"]`) — tracks close, not cumulative session VWAP
- `vwap_delta_pct`: cumulative VWAP starting from first bar of day (pre-market 04:00 ET)
- Pre-market volume dilutes the VWAP, making it stickier and less responsive than RTH-only

**What it should be:** Standard RTH VWAP as defined below.

---

## Implementation Specification

### Formula
```
typical_price = (bar_high + bar_low + bar_close) / 3
cum_tp_vol += typical_price * bar_volume
cum_vol += bar_volume
VWAP = cum_tp_vol / cum_vol
```

**Do NOT use Polygon's per-bar VWAP field (`b["vw"]`).** Compute from raw OHLCV only.

### Reset Rule
- **Daily reset.** Cumulative values (`cum_tp_vol` and `cum_vol`) reset to zero independently for each calendar day.
- **Reset point:** Immediately before processing the first bar with `ts_minute >= 570` (09:30 ET). That bar is the first contributor to the VWAP calculation.
- **If no bar exists at exactly 09:30:** Reset at the first bar with `ts_minute >= 570` on that day.
- **Pre-market bars (ts_minute < 570):** Contribute zero to the VWAP calculation. VWAP is undefined (NaN) for all pre-market bars.

### Timezone Handling
All timestamp comparisons must use US/Eastern timezone. If bar timestamps are stored as UTC, convert to US/Eastern using `zoneinfo.ZoneInfo("America/New_York")` before applying the 09:30 boundary. DST transitions must be handled correctly — do NOT use a fixed UTC offset.

### Zero-Volume Bars
- If a bar has `volume == 0` after the session open: skip it (do not update `cum_tp_vol` or `cum_vol`). Carry forward the previous VWAP value.
- If the FIRST RTH bar of the session has `volume == 0`: VWAP remains `NaN` for that bar. Continue NaN until the first bar with `volume > 0`. Do NOT carry forward the prior day's closing VWAP.

### Halt Handling
- Bars during trading halts (if present in cache) are included in the VWAP calculation — they have OHLCV data and should contribute.
- If no bars are present during a halt period (gap in timestamps), VWAP carries forward the last computed value. No special handling needed.

### Early Close Days
- RTH close on early close days (e.g., day before holidays) ends at 13:00 ET (ts_minute=780), not 16:00. The VWAP calculation stops at the last RTH bar.
- The existing `is_rth` flag should be used to determine RTH boundaries.

### Columns Affected
- **`vwap_delta_pct`** — must be recomputed using the new RTH-reset cumulative VWAP
- The stored `vwap` column (Polygon per-bar VWAP) should be **removed** from signal_bars.parquet — it is not used by any current research and its presence invites confusion
- If any other code references the `vwap` column, update to use `vwap_session` or the new cumulative VWAP

---

## Acceptance Criteria

1. **Formula:** `(H+L+C)/3 × V` cumsum / cumvol. Polygon `vw` field not used.
2. **Reset:** Cumulative values reset to zero immediately before the first bar with `ts_minute >= 570` on each calendar day. That bar is the first contributor.
3. **Pre-market exclusion:** All bars with `ts_minute < 570` have VWAP = NaN.
4. **Zero-volume guard:** V=0 bars skipped (carry forward). NaN at session open if first bar has V=0.
5. **Timezone:** US/Eastern via `zoneinfo`, not fixed UTC offset. DST-safe.
6. **All internal VWAP implementations** (series, per-bar, helpers) use the same reset logic and formula. Workshop enumerates them in PR description.
7. **Unit tests:** Normal RTH day, pre-market exclusion, zero-volume at session open (→ NaN), zero-volume mid-session (→ carry forward), HLC3 accumulation correctness, early close day.
8. **Spot check:** For at least one real ticker+date from the dataset, computed `vwap_session` at 3+ intraday timestamps manually verified against TradingView's VWAP. Tolerance: ±0.05%. Documented in PR.
9. **signal_bars.parquet regenerated.** Confirmation: record file modification timestamp and row count before and after. Both must change. Document in PR.
10. **Smoke test passes.** All existing tests green.
11. **`agents/execution-realist/constraints.md` updated** with the VWAP definition.

---

## Out of Scope
- Live pipeline VWAP (MarketScanner / TradingEngine) — separate story
- Extended-hours VWAP variant — not needed for current research
- VWAP bands (standard deviation) — not needed

---

## Blocks
**Signal 3** (VWAP position at ORB close) in the scanner research is blocked until this story is complete and PO has visually confirmed the new VWAP matches Webull on 3-5 charts in the chart viewer.
