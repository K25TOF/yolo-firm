# Execution Realist Memory

## Confirmed Execution Constraints

**bar_close[B0] lookahead confirmed:** All Phase 3 entry price figures use bar_close[B0] as entry price. This is not transactable — a real trader cannot know the close price until after the bar closes. Realistic entry is bar_open[B1] at the earliest. All reported PnL figures are therefore optimistic by at least the spread + open-vs-close difference.

**Polygon-T212 timestamp offset:** 1-minute offset found between Polygon and Webull timestamps. T212 alignment is unverified. Any strategy relying on cross-source timestamp alignment cannot be deployed live until this is resolved.

**EMA9 seeding:** EMA9 seeded from first bar of day — confirmed consistent with Webull. This is a known implementation detail, not an error.
