# Incident Management

_Owner: Boardroom | Approved by: PO | Version: 1.0_

---

## Principles

- Safety first — when in doubt, stop trading and investigate
- No heroics — don't attempt fixes during market hours with open positions
- Log everything — every incident gets a status-log.md entry
- Post-incident review within 24 hours for P1/P2

---

## Severity Levels

| Level | Description | Response time |
|---|---|---|
| P1 | Open position at risk, capital loss possible | Immediate |
| P2 | Pipeline down during market hours, no open positions | < 15 min |
| P3 | Degraded service (one component failing, pipeline running) | < 1 hour |
| P4 | Non-urgent issue, detected outside market hours | Next session |

---

## Incident Playbooks

---

### Pipeline Crash During Market Hours

**Detection:** Pushover alert, container exits, `docker ps` shows container stopped.

**P1 — Open position exists:**
1. Log into T212 app immediately
2. Manually close open position(s)
3. Record exit price and reason in status-log.md
4. Do NOT restart pipeline until position is flat
5. Investigate cause, fix, test before next session

**P2 — No open position:**
1. Check `docker logs yolo-dev --tail 50` for error
2. If recoverable (config issue, transient error): fix and restart
3. If unclear: leave stopped, investigate post-market
4. Log incident in status-log.md

---

### Unexpected / Bad Trade

**Detection:** T212 app notification, JournalService entry, or manual check.

**Immediate:**
1. Open T212 app — assess position
2. If position violates any rule (wrong ticker, wrong size, duplicate): close manually
3. Do not wait for TradingEngine — act immediately if risk is unacceptable

**Investigation:**
1. Pull trade from JournalService: `yolo journal show <id>`
2. Check AnalystService decision log
3. Identify which safety rail failed or was bypassed
4. Do not resume trading until root cause identified

---

### API Outage

**Polygon.io down:**
- Pipeline degrades gracefully — scanner continues with cached data
- EntryMonitor has no auto-reconnect — monitor manually and restart container if needed
- If outage > 30 min during market hours: stop pipeline manually
- Check status.polygon.io for estimated recovery

**Trading 212 down:**
- No orders can be placed or cancelled
- TradingEngine continues to evaluate exits but cannot act
- If open position + T212 down: monitor manually, act when API recovers
- Do not accumulate additional exposure during T212 outage

**Anthropic (Claude API) down:**
- AnalystService and StrategyBrain degrade gracefully (optional components)
- Pipeline continues in mechanical mode — no LLM advisory
- Log degraded mode in status-log.md

---

### VPS Outage

**Detection:** SSH connection fails, containers unreachable.

1. Check Hostinger control panel for VPS status
2. If VPS is stopped: start from Hostinger panel
3. If VPS is running but SSH fails: check firewall rules via Hostinger console
4. On recovery: `docker ps` — check which containers restarted automatically
5. Verify no open positions were left from last session
6. If `restart: unless-stopped` containers did not restart: `docker compose up -d`

**If VPS is unrecoverable:**
1. Open T212 manually — close any open positions
2. Provision new VPS if needed
3. Restore from GitHub (code) + PO-held secrets backup

---

### Suspected Security Incident

**Triggers:** Unusual API activity, unexpected orders, suspected key exposure.

**Immediate (P1):**
1. Stop all trading immediately: `docker stop yolo-dev`
2. Revoke and rotate ALL API keys (T212, Polygon, Anthropic) from their respective dashboards
3. Check T212 account for unauthorised orders — cancel/close as needed
4. Check VPS auth logs: `journalctl -u ssh --since "1 hour ago"`

**Investigation:**
1. Identify exposure vector (key in logs, git history, compromised device)
2. Generate new keys, update `.env.prd` and `.env.dev` via root
3. Re-encrypt secrets with age
4. Do not resume trading until all keys rotated and exposure vector addressed

**Post-incident:**
- Full security review before resuming
- Consider additional security hardening (see `risk-policy.md`)

---

## Post-Incident Review

For P1 and P2 incidents, within 24 hours:

1. **What happened** — timeline of events
2. **Impact** — financial, operational
3. **Root cause** — what failed and why
4. **Resolution** — what was done to fix it
5. **Prevention** — what story or change prevents recurrence
6. **Logged in** — `status-log.md` with tag `[INCIDENT]`

---

## Rollback Procedure

If a PRD release causes issues:

```bash
# Identify last known good tag
git log --oneline main | head -10

# Roll back to specific version
git checkout vX.Y.Z
docker compose up -d --build

# Log in status-log.md
echo "## $(date) — ROLLBACK to vX.Y.Z" >> ~/status-log.md
```

See `~/CLAUDE.md` Section 7.4 for full rollback detail.
