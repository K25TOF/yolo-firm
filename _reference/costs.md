# Costs & Expenses

_Owner: Boardroom | Approved by: PO | Version: 1.0_

---

## Fixed Costs

| Service | Purpose | Cost | Billing |
|---|---|---|---|
| Claude Max 20x | Boardroom (claude.ai) + Claude Code (Workshop) | €274.99 | Monthly |
| Hostinger VPS KVM 2 | Infrastructure — srv1161923.hstgr.cloud | £263.76 | Annually (~£22/month) |
| Massive.com (Polygon.io) | Market data API — bars, snapshots, WebSocket | $199.00 | Monthly |

**Approximate monthly fixed cost:** ~£490/month (converted to GBP at current rates — subject to FX fluctuation)

---

## Variable Costs

| Service | Purpose | Model | Rate |
|---|---|---|---|
| Anthropic API | DDBot, AnalystService, StrategyBrain, Org Learning agents | Haiku 4.5 | $1.00 / $5.00 per 1M tokens (in/out) |
| Anthropic API | StrategyBrain (advisory) | Sonnet 4.6 | $3.00 / $15.00 per 1M tokens (in/out) |

**Optimisations available:**
- Prompt caching: up to 90% savings on repeated context (system prompts, firm docs)
- Batch API: 50% discount for non-time-sensitive workloads (research cycles)
- Use Haiku by default — escalate to Sonnet only when reasoning depth is needed

**Estimated API spend:** Low at current usage. Research cycle cadence adds ~$2–5/month. Monitor via Anthropic Console.

### Cost Logging Policy

All Claude API calls must log usage automatically. Logging is implemented in the shared `AnthropicClient` wrapper — one place, covers all callers (DDBot, AnalystService, StrategyBrain, and all future Org Learning agents).

Each API call logs: timestamp, caller, model, input_tokens, output_tokens, estimated_cost_usd.

Logs written to `analysis/kpis/api-costs.json` (append per call).
After each session, pipeline writes a human-readable summary to `analysis/kpis/costs-live.md`.
The viewer serves `costs-live.md` as a live costs section — page refresh shows latest data.

---

## Cost Governance

- All fixed costs approved by PO before commitment
- Variable API costs reviewed monthly
- Manager agent enforces token budget per learning cycle
- Any new recurring cost requires PO approval before onboarding
- Currency note: costs spread across EUR, GBP, USD — track in native currency per line item

---

## Break-Even Reference

Once live trading begins, monthly fixed costs set the minimum profit target:

| Item | Monthly equivalent |
|---|---|
| Claude Max | ~€275 |
| VPS | ~£22 |
| Polygon | ~$199 |
| Claude API | TBD (variable) |

_YOLO must generate sufficient profit to cover operating costs before any return is realised._
