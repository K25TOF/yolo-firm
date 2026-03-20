# YOLO-FIRM — Current State

Branch: develop
Last approved stories: Story 5.13 (dates="all" support)
Pending PO review: none
Pipeline: paused (LLM API costs — sessions not running autonomously)
Agent model: Haiku (text), Sonnet (tool-use)
Sessions: LC-2025-001 through LC-2025-012

## Active Research

**LC-2025-012: Ignition Event Research** — completed 2026-03-17
- ZigZag swing detection, staircase pattern clustering, ATR-based exit optimisation
- Full report in status-log.md (2026-03-17 entry)
- Scripts in `analysis/scratch/` are active research artefacts — do not delete

## Tools

- Chart viewer: http://72.61.203.132:8050 (signal_bars visualisation, trade review)
- Daily refresh cron: running in yolo repo (02:30 ET Tue–Sat)

## Next Steps

- Signal accumulation framework research (pending PO direction)
- trades.json regeneration after EDT/EST timezone fix (deferred)
