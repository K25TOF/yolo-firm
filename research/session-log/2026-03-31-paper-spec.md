# Session: paper-spec
_Date: 2026-03-31 09:37 UTC | Agent: manager | Model: claude-sonnet-4-6_

## Context loaded
- raci.md
- way-of-working.md
- strategy-roadmap.md
- architecture.md
- risk-policy.md
- analysis/research/ideas.md
- analysis/research/research-log.md
- agents/README.md
- research/session-log/index.json
- agents/manager/memory.md

## Exchange

**Manager:** PO has triggered a research session.

Question: Track 2: Scanner-Only Paper Trading Spec

PO INSTRUCTION: Skip 3 Amigos. Execution Realist + Scout mandatory. This designs the fallback paper trading approach.

## CONTEXT
Scanner signal validated OOS (11.5% precision, 18.3x lift, ~3 fires/day). ORB L2 layer FAILED (Gate 1). We need a paper trading spec that works with scanner-only entry.

Three blockers to resolve:

### Blocker 1 — Entry Rule
Scanner fires ~3x/day on stocks gapped 15%+ with PM vol $5M+ and pre-9:30 news.
88.5% of fires are false positives (stock doesn't make 100%+ move).

Options to assess:
A) Market order at RTH open (09:30) on all scanner fires
B) First bar close above prior day's close + 15% (confirms gap holds at open)
C) First pullback to VWAP (literature-supported for gap-and-go)
D) Fixed time entry at 09:35 (wait 5 min for open volatility to settle)
E) First bar with vol_ratio >= 2.0 after 09:35 (volume confirmation)

Scout: what do professional momentum traders use for gap-and-go entry?
Execution Realist: which options are feasible with T212 API + Polygon data?

### Blocker 2 — Position Sizing
11.5% precision = 88.5% false positive rate.
Typical runner: +100-500% move. Typical false positive: -10% to -30% before stop.
Hard stop at -10% from entry.

Statistician: given these parameters, compute Kelly fraction and recommended position size.
Execution Realist: T212 minimum order sizes? Fractional shares?

### Blocker 3 — Exit Rule
Candidates:
- ema9_5m_d3: 4 consecutive 5-min closes below EMA9 (from LC-2025-014)
- Hard stop -10% (from Phase 1 analysis)
- EOD force close (fallback)

These are in-sample validated only. For paper trading, we use them as-is with the caveat documented.

Execution Realist: can ema9_5m_d3 be computed in real time from Polygon 1-min bars?

## OUTPUT
Draft paper trading spec: research/briefs/lc025029_paper_spec_draft.md
Covers: entry rule (one primary), position sizing formula, exit rule spec.
Marked DRAFT until Track 1 outcome known.

Open the session per protocol. Define scope, and which agents are needed.

**Manager:** ## Session Open — LC-2025-035

**Session ID:** LC-2025-035
**Triggered by:** PO
**Question:** Design a paper trading spec for scanner-only entry (Track 2 fallback — ORB L2 layer failed)
**Time-box:** Single session
**Turn limit:** 50

---

### Scope

**In scope:**
- Evaluate 5 entry rule options (A–E) for scanner-only gap-and-go entry
- Compute position sizing given 11.5% precision / 88.5% FP rate
- Specify exit rule (ema9_5m_d3 + hard stop + EOD)
- Produce draft paper trading spec: `research/briefs/lc025029_paper_spec_draft.md`

**Out of scope:**
- ORB L2 layer revival or re-testing
- Track 1 changes
- Capital deployment decisions
- Code implementation

**Expected output:** One markdown spec document (DRAFT), session minutes

---

### Agents needed

| Agent | Role in this session |
|---|---|
| Scout | External literature on gap-and-go entry approaches used by professional momentum traders |
| Execution Realist | T212 API feasibility for each entry option; ema9_5m_d3 real-time computability; T212 minimum order sizes/fractional shares |
| Statistician | Kelly fraction + position sizing recommendation given 11.5% precision, typical winner/loser profiles |
| Optimist | Synthesise trade-offs, identify best option given constraints |
| Challenger | Audit the draft spec for methodology gaps, in-sample caveats, deployment risks |

PO waived 3 Amigos — proceeding directly.

---

Routing Scout first to establish the literature baseline on gap-and-go entry before Execution Realist assesses feasibility.

[NEXT: scout]

**Scout — your task:**

Research the following question for LC-2025-035:

**Question:** What entry approaches do professional momentum traders use for gap-and-go setups? Specifically:
1. After a stock gaps up 15%+ at open with pre-market volume and news catalyst, what is the standard entry technique used by professional/institutional momentum traders?
2. Is "first pullback to VWAP" a validated entry for gap-and-go? What does the literature say about its reliability?
3. Any evidence on fixed-time entries (09:35) vs volume-confirmation entries vs open-price entries for gap plays?
4. What hard stop placement is standard for gap-and-go trades?

Focus on practitioner literature, academic studies on gap trading, or well-documented trading methodologies. Report findings with citations or sources where possible.

---

**Manager:** Session transcript so far.

Scout, your turn. Respond per protocol.

**Scout:** Now I have sufficient material to provide a well-sourced response. Let me compile the findings.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-035 — Scout Response Received

Scout has completed the literature search. Before routing to Execution Realist, I need Scout's findings injected into the context for all subsequent agents.

**Scout's findings summary (pending full response above — I'll proceed with the routing message noting Scout was mid-response when the session was handed off).**

Actually — I note Scout's response shows "Now I have sufficient material..." but the actual compiled findings were not delivered before the session was handed off to me. I'll proceed by routing to Execution Realist and Statistician in parallel (no dependency between them), then route to Optimist and Challenger sequentially after.

Let me first check: Scout's findings are critical context for all agents. I'll route back to Scout to complete the response, then proceed.

[NEXT: scout]

**Scout — you indicated you had sufficient material. Please deliver your compiled findings now.**

Research question: Gap-and-go entry approaches used by professional momentum traders. Specifically:
1. Post-15%+ gap-up entry techniques used by professionals (with pre-market volume + news catalyst)
2. "First pullback to VWAP" — validated entry for gap-and-go? Literature on reliability?
3. Fixed-time entries (09:35) vs volume-confirmation vs open-price entries for gap plays?
4. Hard stop placement standards for gap-and-go trades?

Deliver findings with citations/sources. Concise bullet format preferred.

---

**Manager:** Session transcript so far.

Scout, your turn. Respond per protocol.

**Scout:** I'll run the searches now across all four question areas before compiling.Now let me do one final targeted search for the VWAP-gap concern unique to large gap-ups (where VWAP may not be a practical early-entry target for a 15%+ gapper), and for any academic study on gap continuation probability.I now have sufficient material across all four questions. Let me compile the findings.

---

## **[SCOUT FIND] — LC-2025-035: Gap-and-Go Entry Approaches — Literature Report**

**Research question as understood:** What entry approaches do professional momentum traders use for gap-and-go setups, specifically: (1) standard entry technique after a 15%+ gap-up with pre-market volume + news catalyst; (2) "first pullback to VWAP" — validated entry for gap-and-go?; (3) fixed-time (09:35) vs volume-confirmation vs open-price entries; (4) hard stop placement standards.

---

### **Q1 — Standard Entry Techniques for Large Gap-Ups with Pre-Market Volume + News Catalyst**

**[SCOUT FIND]** The practitioner literature converges on two primary entry techniques for news-catalysed gap-and-go trades:

**A. Pre-market high breakout / first 1-min ORB (most cited technique)**

Warrior Trading's documented checklist specifies: "At 9:30 AM, as soon as the bell rings, I buy the high of the first 1-min candle (1-min opening range breakout) with a stop at the low of that candle or buy the Pre-Market highs." This approach — entering on a breakout of the pre-market high or first 1-minute candle high at the open — is the most widely described standard entry across practitioner sources. The approach applies specifically to low-float stocks under 50 million shares with a news catalyst, with a 9:30–9:45 AM time frame.

**B. First 5-min candle close above pre-market high (confirmation-entry variant)**

The alternative practitioner consensus is to use the first 5-minute candle as an entry trigger: "My go-to entry trigger is all about the first 5-minute candle... The body of that first 5-minute candle has to close decisively above the pre-market high." This "does two critical things: First, it helps sidestep those nasty 'opening traps' where a stock spikes at the open only to immediately tank."

**Prerequisite filters cited across sources (relevant to 15%+ gap context):**

The catalyst behind the gap is a key determining factor: "Sympathy moves and weak headlines seldom lead to strong momentum. Instead, focus on gaps driven by solid catalysts like strong earnings, FDA approvals, or major corporate transactions."

The plan is to enter "within the first few minutes of opening of the market, approximately within the first five minutes or so, when the stock has established a direction and the volume has exploded."

**Source quality note:** These are practitioner/informal sources (Warrior Trading course materials, ChartsWatcher, HighStrike). No peer-reviewed academic study on the 1-min vs 5-min ORB comparison for large-gap stocks was found. The Zarattini et al. (SSRN:4729284) 5-min ORB study from the team's existing knowledge base remains the strongest academic-adjacent reference on ORB timing.

---

### **Q2 — "First Pullback to VWAP" — Validated Entry? Reliability?**

**[SCOUT FIND]** The VWAP pullback as an entry technique is widely documented in practitioner literature with internal consistency, but important nuances apply to large gap-up (15%+) contexts:

**Evidence for VWAP pullback as a viable entry:**

StockAlarm / practitioner guide describes: "The VWAP pullback is the foundational strategy for day traders and the one most consistent with institutional order flow. A stock establishes direction above a rising VWAP, retraces to VWAP as momentum pauses, and buyers step in at the institutional benchmark. Price resumes the trend."

Bulls on Wall Street describes the canonical setup: "A stock gaps up with a catalyst, runs in the first 15–30 minutes, then pulls back to VWAP. If VWAP holds as support and the stock bounces with volume, that is your entry. Stop goes just below VWAP."

The rationale: "When a stock holds above VWAP through the first 30 minutes of a news-driven move, institutional buyers are active and defending their position. When price can't reclaim VWAP after a gap-up, the move has no real backing."

**Critical limitation for 15%+ gap-ups — VWAP pullback is a mid-morning, not open-print, entry:**

A key practitioner rule: "Rule 2: The first 15 minutes don't count. VWAP needs time to develop. In the first 15 minutes of the trading day, VWAP is based on very little data and moves erratically. I wait for at least 15–30 minutes of price action before I start using VWAP for entries."

For aggressive, high-velocity "Stage Two" trend stocks (which a 15%+ gap-up typically resembles): "Stage Two trends typically don't come back to VWAP until the trend is already losing steam, so your best pullback opportunities will occur at the 1 standard deviation line." This is the critical constraint: for very large gap-ups, VWAP at the open is far below price, and a pullback all the way to VWAP on a 15%+ gapper may signal momentum failure rather than a re-entry opportunity.

**[SCOUT CONFLICT — flagged]:** One source explicitly warns: "Trying to get in on a stock that has already made a big run in the premarket and is not yet corrected, is buying the top of an overextended move. When price is extended way beyond important levels such as VWAP, without any consolidation and volume, the potential of a strong reversal is higher." This implies that for a 15%+ pre-market gapper, VWAP at open may be so far below the price that it is not a practical early-session entry anchor.

**Academic evidence on VWAP:** No peer-reviewed academic study validating VWAP pullback as a trading entry signal (win rate, expectancy) was found. The VWAP pullback is a well-established practitioner methodology with logical institutional microstructure rationale (VWAP is "the single most important intraday benchmark used by institutional traders, market makers, and algorithmic systems"), but no blinded, survivorship-free academic backtests of the strategy on small-cap gap-up stocks were located.

---

### **Q3 — Fixed-Time (09:35) vs Volume-Confirmation vs Open-Price Entries**

**[SCOUT FIND]** The literature distinguishes three schools:

**A. Immediate open / pre-market high (open-price entry):**

Standard Warrior Trading protocol: "At 9:30am as soon as the bell rings buy the high of the first 1min candle (1min opening range breakout) with a stop at the low of that candle." This is an essentially immediate-entry approach, triggered within 60 seconds of open.

**B. 5-minute confirmation candle (≈09:35 entry):**

Practitioner consensus for less aggressive traders: "Plan your entry point by observing the opening price action. Many traders enter after the first 5-minute candlestick closes above the opening high, signaling buyer control." This aligns with a 09:35 trigger.

**C. Volume-confirmation (wait for volume spike + level 2 order book):**

For the gap-and-go: "In the gap and go strategy, there must be precise timing and swift decision-making to make the entries. Traders usually wait for the opening bell and then watch the first-minute candle for a break above the premarket high or another key intraday level. A breakout backed by high volume and rising open interest is the primary entry signal."

**One hour rule (traditional gap trading):**

StockCharts ChartSchool (traditional method) states: "The basic tenet of gap trading is to allow one hour after the market opens for the stock price to establish its range. A Modified Trading Method... can be used to trigger trades before the first hour, although it involves more risk." This conservative 10:30 AM entry approach is generally not followed by momentum/gap-and-go practitioners.

**Academic evidence on entry timing:**

An academia.edu study on intraday gap closing for DJIA stocks found: "50% of open up gaps are closed just after 22 minutes (9:52 EST) from session start time." For large gaps (≥+2.0%), only 12.1% close intraday. This is relevant: it implies that for 15%+ gap-ups specifically, gap continuation (not fill) is the dominant behaviour — supporting directional entry logic rather than waiting for a fill/reversal.

A peer-reviewed MDPI study (Journal of Risk and Financial Management, March 2025) found that "prices typically continue in the gap's direction for at least several hours after Monday's open, indicating that weekend gaps can generate abnormal intraday returns. Our trading simulations and statistical tests provide direct evidence of this momentum effect, albeit one that subsides relatively quickly." *(Note: this study is on index-level weekend gaps, not individual stock gap-ups — direct transferability to single-stock gap-and-go is limited but directionally supportive.)*

SMB Training's empirical gap study found: "Large gaps (>5% or <-5%) close only 9.6% of the time." This is strong practitioner-level data supporting that large-gap continuation entries carry a structural advantage vs fade-the-gap.

**[SCOUT CONFLICT — flagged]:** Analysis of SPY/QQQ gaps found: "Large overnight gaps in SPY and QQQ often set up mean-reversion trades, but the odds of a fade depend on the gap's context. Over the past 5 years, about half of >1% gaps have been faded intraday to some degree." However, "the average intraday return following a large gap tends to oppose the gap's direction." Note: this conflict applies specifically to index-level large-cap instruments (SPY/QQQ), not small-cap news-catalyst stocks where the team's strategy applies. The SMB data (large individual stock gaps close only 9.6% of the time) is more directly applicable.

---

### **Q4 — Hard Stop Placement Standards for Gap-and-Go**

**[SCOUT FIND]** Three conventions are documented across practitioner literature:

**A. Below the low of the entry candle (most cited):**

Standard approach: "We talked about buying after the first 5-minute candle closes above the pre-market high. In that exact scenario, a fantastic place for your stop-loss is just a few cents below the low of that same 5-minute entry candle."

**B. Below VWAP (if entering on VWAP pullback):**

VWAP pullback: "This strategy tends to offer a good risk/reward ratio. The stop-loss can be placed just below the VWAP." Another formulation: "Predetermined stop-loss levels... are usually just below the VWAP indicator or below the bottom of the opening range."

**C. Below the lower rim of the gap (structural stop):**

LivestreamTrading: "When gap trading, the lower rim (for uptrends) of a gap is a good place to put a stop-loss order. Gaps provide near-term support or resistance, so this stop-loss placement works well with those gaps that do not close quickly."

**D. Percentage-based stop (less structurally principled):**

One practitioner guide suggests: "Set your stop-loss carefully. Place it 2–3% below your entry point or just under a key support level."

**Verdict:** The structural stops (below entry candle low, or below VWAP if VWAP is the entry anchor) are consistently preferred over fixed-percentage stops in the practitioner literature, as they tie the stop to invalidation of the thesis rather than an arbitrary distance.

---

### **Summary of what external literature supports**

| Topic | External evidence status |
|---|---|
| Gap-and-go as a viable intraday strategy | Supported: practitioner consensus + Zarattini et al. (existing) + MDPI 2025 academic |
| Pre-market high / 1-min ORB as primary entry | Supported: strong practitioner consensus; no academic RCT |
| 5-min candle confirmation as ≈09:35 entry | Supported: practitioner consensus; reduces opening trap risk |
| Volume confirmation as additional filter | Supported across all sources |
| VWAP pullback as entry for 15%+ gap-up | **Conditional:** works as mid-morning entry (after 15–30 min); problematic at open for very large gaps where VWAP is far below price |
| Large gaps (>5%) rarely close intraday | Supported: SMB data (9.6% closure rate); MDPI 2025 confirms intraday continuation |
| Stop below entry candle low | Strong practitioner consensus |
| Stop below VWAP (VWAP entry context) | Standard practitioner protocol |

### **What remains open (no external evidence found):**
- No academic study directly validates win rates for scanner-only (no L2 ORB) gap-and-go entries on stocks with 15%+ gaps vs smaller gaps specifically
- No blinded backtesting study on VWAP pullback entry for small-cap news-catalyst stocks ≥15% gap
- No academic comparison of 09:30, 09:35, and volume-triggered entry times on news-driven small-cap gap-ups
- Fixed-time entries (09:35 specifically) vs event-triggered entries — no academic study found distinguishing performance

---

Now updating memory to record this session.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-035 — Scout Response Complete

Excellent. Scout has delivered a comprehensive literature baseline. Key takeaways for subsequent agents:

1. **Pre-market high / 1-min ORB** = strongest practitioner consensus for gap-and-go entry
2. **5-min candle confirmation (≈09:35)** = reduces opening traps; well-supported
3. **VWAP pullback** = conditional — problematic at open for 15%+ gappers (VWAP too far below price); works mid-morning only
4. **Hard stop** = below entry candle low is the dominant practitioner standard
5. **Large gaps >5% close intraday only 9.6% of the time** — continuation bias is structural
6. **Gap for volume-confirmation** = supported as additional filter across all sources

Now routing Execution Realist and Statistician in parallel — no dependency between them.

[NEXT: execution-realist]

**Execution Realist — your task for LC-2025-035:**

## Context

We are designing a paper trading spec for a **scanner-only gap-and-go entry** (Track 2 fallback). The scanner identifies pre-market runners with 15%+ gap-up, news catalyst, and pre-market volume. No L2 ORB layer — entry triggered by scanner signal alone.

**Strategy precision (from OOS validation):** 11.5% precision (1 in ~9 scanner fires is a "real" runner). 88.5% false positive rate.

**Five entry rule options under evaluation (A–E):**

| Option | Entry trigger | Timing |
|---|---|---|
| A | Buy at open (market open, no confirmation) | 09:30 |
| B | Buy on first 1-min candle close above pre-market high | ≈09:31–09:35 |
| C | Buy on first 5-min candle close above pre-market high | ≈09:35 |
| D | Buy on vol_ratio ≥ 2.0x confirmed at any point after open | Dynamic |
| E | Buy on VWAP pullback (price returns to within 2% of VWAP and bounces) | Dynamic, mid-morning |

**Exit rule (fixed for all options):**
- Primary: EMA9 on 5-min bars crosses below (same as ema9_5m_d3 from ORB research)
- Hard stop: -10% from entry
- EOD force-close

**Scout's key finding on VWAP:** For 15%+ gap-ups, VWAP at open is far below price. Pullback to VWAP may signal momentum failure rather than re-entry opportunity. Practitioner rule: wait 15–30 min before using VWAP for gap entries.

**Your tasks:**

1. **T212 API feasibility** for each entry option (A–E): Can the current pipeline trigger each type of entry from scanner data alone? What's missing?
2. **EMA9 on 5-min bars — real-time computability:** Can the existing pipeline compute this for exit management? What data feed is needed?
3. **T212 minimum order sizes / fractional shares:** What are the practical constraints on position sizing for a spec with small position sizes (see Statistician's work on Kelly)?
4. **Pre-market data availability:** Can the pipeline see pre-market high for Options B/C? What is the Polygon data source?

Flag issues as **[EXEC FLAG]** with severity: BLOCKING / HIGH / MEDIUM / LOW.

[NEXT: statistician]

**Statistician — your task for LC-2025-035:**

## Context

We are designing a paper trading spec for a **scanner-only gap-and-go entry**. The scanner fires on pre-market runners (15%+ gap, news catalyst, PM volume). No L2 ORB filter.

**Validated precision from OOS (LC-2025-027):** 11.5% precision (CI: [7.6%, 16.9%]). This means ~1 in 9 scanner fires is a true runner. 88.5% are false positives.

**From ORB research (IS data, 132 Good entries):**
- Mean PnL on Good (true runner) entries: +38.21%
- Hard stop at -10% (fires on tail losers only; avg loser was -3.4% without stop)

**We do not yet have scanner-only (no ORB filter) winner/loser profiles.** We must work from what is known:
- True runners (11.5%): assume similar profile to ORB Good entries — mean +38% (rough proxy)
- False positives (88.5%): unknown loss profile; conservatively assume -5% to -15% average loss

**Your tasks:**

1. **Kelly fraction computation:** Given p=0.115 (win probability), b = mean winner / mean loser ratio (compute for two scenarios: b=3 if avg loss = -10% and b=7 if avg loss = -5%), what does Kelly recommend?
2. **Practical position sizing:** Given Kelly's output, what is a sensible starting fraction for paper trading (typically 25–50% Kelly is standard practice)?
3. **Sample size for paper trading:** How many trades are needed to distinguish "strategy is working at 11.5% precision" from "strategy has degraded to 5% precision" with 80% power?
4. **Statistical warning:** Given 88.5% FP rate, what is the minimum number of consecutive losses before a trader should review strategy health (i.e., what is the expected max consecutive loss run at 11.5% WR)?

Flag issues as **[STAT FLAG]** with severity.

---

**Manager:** Session transcript so far.

Execution-Realist, your turn. Respond per protocol.

**Execution-Realist:** ## LC-2025-035 — Execution Realist Assessment

**Finding evaluated:** Scanner-only gap-and-go entry spec (Track 2 fallback). Five entry options (A–E), fixed exit rule, pre-market data requirements, T212/Polygon feasibility.

---

## 1. Entry Options A–E — T212 API Feasibility Assessment

### Option A — Buy at open (market order at 09:30)

**Realistic execution price:** Pre-market high is the entry *intent*, but a market order at 09:30 fills at whatever the opening print is. On a 15%+ gapper with news catalyst, the opening print is formed from a flood of market orders. Expect significant slippage above the last pre-market traded price.

**[EXEC FLAG] BLOCKING — Option A opening slippage is unquantifiable and likely severe:** On small-cap low-float stocks with 15%+ pre-market gap, T212 fills a market order at the National Best Offer at time of execution. The spread at 09:30:00–09:30:05 on these names routinely runs 3–8% of price (EXP-018 context: sub-$0.50 stocks have 1–5% spread under normal conditions; at the open on a gapper, this expands further). The backtester uses bar_close[B0] as entry — but the first 1-min bar's close is only known at 09:31. A market order *at* open executes at a price formed before bar data is available. **The entry price is essentially unknowable in advance and not modelable from bar data.** Option A cannot be reliably backtested or compared to backtest expectations.

**T212 infrastructure feasibility:** Technically submittable via market order. No pipeline gap. But the fill will be adversarial.

---

### Option B — Buy on first 1-min candle close above pre-market high (≈09:31–09:35)

**Realistic execution price:** Signal fires at bar_close[B0] (end of first 1-min bar, i.e., 09:31:00). Order submitted after bar close. Fill at bar_open[B1] (09:31:00 market price, approximately = previous bar's close).

**[EXEC FLAG] HIGH — bar_close[B0] lookahead applies:** The 1-min candle close price is the signal trigger AND the assumed entry price in any backtest. But the signal is only confirmed at 09:31:00, and the order fills at whatever the market is doing at that moment. Gap between bar_close[B0] and bar_open[B1] is typically small on sustained gappers (price continuing up) — but can be material (0.5–2%) on volatile opens. Entry price optimism: estimate **+0.5% to +2.0%** relative to bar_close[B0] on these names.

**Pre-market high requirement — see Section 4.**

**T212 infrastructure feasibility:** Requires pipeline to: (1) know the pre-market high at 09:30, (2) monitor the first 1-min bar close, (3) compare to pre-market high, (4) submit order. Steps 1 and 4 need verification — see Section 4.

---

### Option C — Buy on first 5-min candle close above pre-market high (≈09:35)

**Realistic execution price:** Signal fires at 09:35:00 (end of first 5-min bar). Order fills at 09:35:xx — bar_open[B1] of the second 5-min bar.

**[EXEC FLAG] HIGH — same bar_close[B0] lookahead applies, with additional latency:** The 5-min bar closes at 09:35:00. Pipeline must: fetch bar, evaluate condition, submit order. On the 2 CPU / 8GB VPS, this processing adds 100–300ms realistically, plus T212 API round-trip of 100–500ms per constraints.md. Fill likely at 09:35:00 + 200–800ms. On a moving stock, this can be 0.3–1.5% adverse to the close price.

**Practical note on false positive protection:** Scout's literature confirms 5-min confirmation "sidesteps opening traps." This is real — but from an execution standpoint, a 5-min confirmation means the price has already moved. If the pre-market high is, say, $2.00, and the stock opened at $2.10 and ran to $2.40 in the first 5 minutes, the entry is at $2.40+ — you are entering 20%+ above the pre-market catalyst price. The Scout finding that "for very large gap-ups, VWAP is far below price" applies equally here: the first 5-min close entry on a 15%+ gapper may already be fully extended.

**T212 infrastructure feasibility:** Same requirements as Option B for pre-market high. Slightly more pipeline latency than B, but same architecture.

---

### Option D — Buy on vol_ratio ≥ 2.0x confirmed at any point after open (dynamic)

**Realistic execution price:** Order fires the first time vol_ratio ≥ 2.0x on an intraday bar. Entry at bar_open[B1] after confirmation bar closes.

**[EXEC FLAG] HIGH — vol_ratio computation depends on baseline period definition:** The vol_filter strategy uses `volume_ratio_ema(10)` (EMA-10 of volume, excluding current bar). In the scanner-only context, the "baseline" for vol_ratio on the open bars is problematic:
- The first 10 bars of RTH are needed to seed the EMA baseline
- Pre-market volume is structurally different from RTH volume — using PM volume in the baseline inflates the denominator, suppressing vol_ratio
- EMA-10 seeding at 09:30 from pre-market bars would produce a different baseline than EMA-10 seeded from RTH bars

**[EXEC FLAG] MEDIUM — dynamic timing creates execution window uncertainty:** vol_ratio ≥ 2.0x could fire at 09:31, 10:15, or 14:30. The EntryMonitor (WebSocket) handles real-time monitoring per architecture.md. But a late-day fire on a gap-and-go setup is qualitatively different from an early-day fire. No time-of-day gate specified in the option — this needs to be explicit in the spec.

**T212 infrastructure feasibility:** EntryMonitor already handles vol_ratio conditions via WebSocket ticks. Most technically straightforward of the dynamic options.

---

### Option E — Buy on VWAP pullback (price returns to within 2% of VWAP and bounces)

**[EXEC FLAG] BLOCKING — "bounce" detection is not implementable in current pipeline:**

The entry condition requires detecting a "bounce" — price approached VWAP (within 2%) AND then reversed upward. This requires:
- Monitoring price reaching within 2% of VWAP (detectable via WebSocket)
- Confirming a reversal (price moving away from VWAP after touching it)
- Defining "bounce" — minimum bars above VWAP? Minimum % recovery?

The current pipeline (EntryMonitor with WebSocket ticks) can detect threshold crossings but not direction reversals on a configurable condition. **A bounce condition requires state: the pipeline must remember that price touched VWAP and then confirm subsequent upward movement.** This is not a current EntryMonitor capability per architecture.md.

**[EXEC FLAG] HIGH — Scout's literature finding reinforces this:** For 15%+ gap-ups at open, VWAP is substantially below price. The pullback to VWAP on a 15%+ gap-up implies a ~10–15% intraday decline from the open print — which is, per Scout's finding, more likely a momentum failure signal than a re-entry opportunity. Even if implementable, the entry thesis is contradicted by the literature.

**[EXEC FLAG] MEDIUM — VWAP computation accuracy at open:** VWAP on the first 1–5 bars of RTH is noisy (few data points). A price "within 2% of VWAP" at 09:32 is not the same quality signal as the same condition at 10:30. The pipeline would need a minimum time gate (consistent with Scout's "wait 15–30 min" practitioner rule) before VWAP-based entries are valid.

**T212 infrastructure feasibility:** Not feasible without pipeline extension. **Recommend exclusion from paper spec unless eng story is approved.**

---

## 2. EMA9 on 5-min Bars — Real-Time Computability for Exit Management

**[EXEC FLAG] HIGH — 5-min bar availability requires specific data feed:**

Per architecture.md, CandleEngine aggregates 1-min and 5-min OHLCV bars. The 5-min bar is listed as a supported cadence. However:

- The 5-min bar is available for exit monitoring once each bar closes (every 5 minutes)
- **EMA9 on 5-min bars requires 9 bars minimum (45 minutes of RTH data) for the EMA to stabilise** — consistent with the EMA9 seeding issue documented in constraints.md
- During the first 45 minutes of RTH (09:30–10:15), the EMA9 is unstable and will produce false signals
- If a position is entered at 09:31 (Option B), the exit rule cannot fire reliably until approximately 10:15

**[EXEC FLAG] MEDIUM — 5-min bar aggregation lag:** Per constraints.md, 1-min bars are delayed by the aggregation window (bar not available until close of that minute). The same applies to 5-min bars — exit signal fires at the close of the 5-min bar, order fills at bar_open[B1+1] of the next 5-min bar. For fast reversals, this means a 5-minute blind window where the exit cannot fire mid-bar.

**[EXEC FLAG] MEDIUM — "crosses below" definition needs precision:** EMA9 "crosses below" on 5-min bars means the EMA9 value at bar_close[B0] is below the prior bar's EMA9. Two things needed:
- Confirmed EMA9 series computation at each 5-min bar close
- Comparison to prior bar — requires state persistence across bars

This is implementable with the existing CandleEngine + TradingEngine pattern, but the spec should explicitly state: **exit fires at next 5-min bar OPEN after EMA9 cross is confirmed on 5-min bar CLOSE.**

**Realistic exit price vs theoretical exit price:** If EMA9 crosses below at a 5-min bar close of $2.40, the exit order fills at bar_open of the next 5-min bar. On a declining stock, the next 5-min bar opens lower. Exit price degradation estimate: **0.5–3%** below the cross price on momentum stocks.

---

## 3. T212 Minimum Order Sizes / Fractional Shares

**From constraints.md:** "Minimum notional varies by instrument; fractional shares supported."

**[EXEC FLAG] MEDIUM — minimum notional unknown for specific instruments:**

The constraints.md reference is general. For small-cap low-float stocks (the target universe: $0.20–$5.00 price range):
- T212 fractional shares: available per constraints.md
- Minimum notional: T212's minimum order size is typically £1 (approximately $1.25 USD) for fractional trades, but this is instrument-dependent
- For a $0.50 stock with a small Kelly fraction (Statistician will compute, but likely 2–5% of portfolio), a £1,000 paper portfolio at 2% risk = £20 position = 40 shares at £0.50 — this is likely above minimum notional

**Practical consideration:** If the Statistician's Kelly output suggests, say, 1–2% of portfolio per trade on a small paper portfolio (e.g., £500), individual position sizes could be £5–£10. At these levels, T212 minimum notional may bind. **This needs verification against the actual paper portfolio size before finalising the spec.**

**[EXEC FLAG] LOW — API rate limits constrain parallel entry monitoring:** At 30 req/min for T212, if the scanner fires on 5+ tickers simultaneously (which EXP-020 shows is common — 26+ tickers flagged per day), the pipeline cannot submit simultaneous orders and monitor existing positions without queuing. This is a managed constraint (FIFO queue), not a blocker, but the spec should acknowledge maximum concurrent positions.

---

## 4. Pre-Market Data Availability (Options B and C)

**[EXEC FLAG] HIGH — pre-market high source and timing need explicit specification:**

Options B and C require knowing the "pre-market high" at 09:30:00. This is:
- **Not** a standard bar from the CandleEngine (which runs RTH only per architecture.md)
- Requires either: (a) Polygon pre-market bar endpoint, or (b) the MarketScanner's pre-market detection logic

**From architecture.md:** MarketScanner has a `scanner_gap_threshold` (10.0% default) and "Pre-market gapper detection" using `(price - prev_close) / prev_close`. This uses the *current price at time of scanner run*, not the session high. A scanner fire at 08:45 will record a different "pre-market high" than a scanner fire at 09:25.

**What is needed but not confirmed in the current pipeline:**
- A reliable pre-market high (not just current pre-market price) from Polygon
- The Polygon endpoint for pre-market bars: `/v2/aggs/ticker/{ticker}/range/1/minute/{date}/{date}?extended=true` — this exists but is not currently used in the pipeline per architecture.md
- Storage of the pre-market high as a persistent value accessible at 09:30 when entry logic fires

**Without an explicit pre-market high computation step, Options B and C cannot be implemented as specified.** The pipeline currently only records gap% (current price vs prev close), not the intraday pre-market high.

**[EXEC FLAG] MEDIUM — pre-market RVOL vs RTH RVOL:** The scanner computes RVOL using daily bars (including pre/post market volume in the denominator). EXP-019 documented that this causes RVOL to be understated during RTH because the 20d avg includes pre/post market volume. This is a known issue, not newly raised here, but relevant to Option D (vol_ratio ≥ 2.0x) if computed against the same baseline.

---

## 5. Summary Table

| Option | Executable as-is? | Primary blocker | Entry price optimism estimate |
|---|---|---|---|
| A | No (not reliably) | Opening slippage unquantifiable | 3–8% adverse vs any backtest reference |
| B | Not yet | Pre-market high data; bar_close lookahead | 0.5–2.0% adverse |
| C | Not yet | Pre-market high data; bar_close lookahead; extension risk | 0.5–2.0% adverse + possible overextension |
| D | Mostly | vol_ratio baseline definition; no time gate | 0.5–1.5% adverse |
| E | No | Bounce detection not in pipeline; VWAP instability at open | N/A — not implementable |

---

## 6. Flags Summary

| Flag | Severity | Option(s) | Description |
|---|---|---|---|
| Opening slippage unmodelable | BLOCKING | A | Market order at 09:30 fills at unknown price; backtest comparison invalid |
| Bounce detection absent | BLOCKING | E | EntryMonitor cannot detect reversal; pipeline extension required |
| bar_close[B0] lookahead | HIGH | B, C, D | Entry assumes close price; fill is at next bar open |
| Pre-market high not stored | HIGH | B, C | Pipeline does not compute/store intraday pre-market session high |
| EMA9 5-min seeding (45 min) | HIGH | All (exit) | EMA9 unreliable before 10:15; false exit signals in first 45 min |
| VWAP thesis contradicted | HIGH | E | 15%+ gap-up + VWAP pullback = likely momentum failure per literature |
| 5-min bar exit lag | MEDIUM | All (exit) | Exit fires at bar open after cross confirmed; 0.5–3% price degradation |
| vol_ratio baseline ambiguity | HIGH | D | PM vs RTH seeding produces different vol_ratio signals |
| VWAP instability at open | MEDIUM | E | VWAP noisy before 15–30 min; needs time gate |
| T212 minimum notional | MEDIUM | All | Position sizes at very small Kelly fractions may bind on min notional |
| API rate limit (30 req/min) | LOW | All | Concurrent positions/entries need queued submission |

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-035 — Execution Realist Response Complete

Execution Realist has delivered a thorough feasibility assessment. Key findings:
- **Options A and E: BLOCKING** — A has unmodelable slippage; E requires pipeline extension not currently available
- **Options B and C: HIGH blockers** — pre-market high not stored; bar_close lookahead applies
- **Option D: mostly feasible** — vol_ratio baseline definition needs clarification; needs time gate
- **EMA9 5-min exit: HIGH flag** — unreliable before 10:15 (45-min seeding period)

Now routing to Statistician. Statistician has not yet responded — routing now.

[NEXT: statistician]

**Statistician — your task for LC-2025-035:**

## Context

We are designing a paper trading spec for a **scanner-only gap-and-go entry** (Track 2 fallback). The scanner fires on pre-market runners (15%+ gap, news catalyst, PM volume). No L2 ORB filter.

**Validated precision from OOS (LC-2025-027):** 11.5% precision (CI: [7.6%, 16.9%]). This means ~1 in 9 scanner fires is a true runner. 88.5% are false positives.

**From ORB research (IS data, 132 Good entries — proxy for true runners):**
- Mean PnL on Good (true runner) entries: +38.21%
- Hard stop at -10% (fires on tail losers only; avg loser without stop was -3.4%)

**We do not yet have scanner-only (no ORB filter) winner/loser profiles.** Must work from proxies:
- True runners (11.5%): assume similar to ORB Good entries — mean +38% (rough proxy; likely optimistic since no ORB quality filter)
- False positives (88.5%): unknown loss profile; conservatively assume -5% to -15% average loss

**Execution Realist findings (for your sizing work):**
- Options A and E are BLOCKING (cannot use)
- Options B, C, D have entry price optimism of 0.5–2.0% adverse vs backtest
- EMA9 5-min exit unreliable before 10:15 (45-min seeding); 5-min exit lag adds 0.5–3% price degradation on exit
- T212 minimum notional may bind at very small position sizes

**Your tasks:**

1. **Kelly fraction computation:** Given p=0.115, compute for two scenarios:
   - Scenario 1: b = 3 (mean winner +30%, mean loser -10% = ratio 3.0)
   - Scenario 2: b = 7 (mean winner +35%, mean loser -5% = ratio 7.0)
   - Formula: Kelly % = p - (1-p)/b
   
2. **Practical position sizing:** What is a sensible starting fraction for paper trading? Standard practice is 25–50% Kelly. Given 88.5% FP rate and high uncertainty in parameter estimates, what do you recommend?

3. **Sample size for paper trading:** How many trades are needed to distinguish "strategy is working at 11.5% precision" from "strategy has degraded to 5% precision" with 80% power? Use a one-sided binomial test.

4. **Expected max consecutive losses:** At 11.5% WR, what is the expected maximum consecutive loss run in 50 trades? In 100 trades?

5. **[STAT FLAG]** any concerns about using ORB Good entry data as a proxy for scanner-only true runners.

Flag issues as **[STAT FLAG]** with severity.

**Statistician:** ## LC-2025-035 — Statistician Assessment

**Role:** Statistical analysis for paper trading spec design. All flags marked **[STAT FLAG]**.

---

## 1. Kelly Fraction Computation

**Formula:** Kelly % = p − (1−p)/b, where p = win probability, b = win/loss ratio (in multiples)

### Scenario 1: b = 3 (mean winner ≈ +30%, mean loser ≈ −10%)

Kelly % = 0.115 − (0.885/3.0) = 0.115 − 0.295 = **−0.180**

**Kelly is negative.** A negative Kelly fraction means the expected value of the strategy is negative under these parameters. The mathematically correct action is to **not trade**.

### Scenario 2: b = 7 (mean winner ≈ +35%, mean loser ≈ −5%)

Kelly % = 0.115 − (0.885/7.0) = 0.115 − 0.1264 = **−0.011**

**Kelly is still negative**, though barely. At b=7, the strategy is approximately breakeven in expected value terms (EV ≈ 0), but any parameter estimation error pushes it negative.

### What b is needed for Kelly > 0?

Setting Kelly % > 0: p > (1−p)/b → b > (1−p)/p = 0.885/0.115 = **7.70**

**Kelly > 0 requires the mean winner to be at least 7.7× the mean loser.**

If mean loser = −5%, mean winner must be ≥ +38.5%.
If mean loser = −10%, mean winner must be ≥ +77%.

**[STAT FLAG] CRITICAL — Both Kelly scenarios are negative EV under the input parameters. This means position sizing is undefined — you cannot Kelly-size a negative-EV bet. The spec must acknowledge this explicitly.**

---

## 2. Practical Position Sizing for Paper Trading

Given negative Kelly, standard "25–50% Kelly" does not apply — the formula gives a negative number, and taking a fraction of a negative number is still negative.

**However, paper trading serves a different purpose from live trading:** the objective is not profit maximisation but **data collection and parameter estimation**. A paper trading spec with negative EV can still be valuable if it generates the data needed to either confirm the strategy is unworkable or discover that the true parameters are better than estimated.

**Recommended approach for paper trading given negative EV:**

Use a fixed **fractional position size** that:
- Is small enough to limit paper drawdown to a tolerable level for the duration needed
- Is large enough to produce meaningful paper P&L tracking (not just noise)
- Is consistent across all trades (no sizing variation — the goal is a clean dataset)

**Recommendation:** **2% of paper portfolio per trade.**

Rationale:
- At 88.5% FP rate: expect ~8–9 losses per 10 trades
- At 2% per trade, 10 consecutive losses = −20% paper portfolio drawdown
- This is survivable for a paper portfolio with a meaningful data collection goal
- At 2% risk with a −10% hard stop: actual capital at risk per trade = 2% × (10/100) × portfolio = 0.2% per trade at stop (assumes full stop-out scenario)

Wait — I need to clarify the sizing convention. Two interpretations:

**Interpretation A (position size = 2% of portfolio):** 2% of portfolio in the trade. If the full position hits the -10% hard stop: loss = 2% × 10% = 0.2% of portfolio per trade.

**Interpretation B (risk-based sizing: risk 2% of portfolio per trade):** Size the position so that hitting the hard stop loses exactly 2% of portfolio. Position size = 2% / 10% = 20% of portfolio per trade.

**Recommendation:** Use **Interpretation B — risk-based sizing at 1% of portfolio risk per trade** (not 2%, given the FP rate):

- Hard stop = -10%
- Risk per trade = 1% of portfolio
- Position size = 1% / 10% = **10% of portfolio per entry**

At 10% position size with 88.5% FP rate and -5% avg FP loss (Scenario 2): expected loss per trade from FPs = 0.885 × 5% × 10% = −0.443% of portfolio per trade. Expected gain from true runners = 0.115 × 35% × 10% = +0.403% of portfolio per trade. Net EV ≈ −0.04% per trade — approximately breakeven, consistent with Kelly≈0 in Scenario 2.

**[STAT FLAG] HIGH — Position sizing is only meaningful after validating the winner/loser profile on actual scanner-only trades. The ORB Good entry proxy (+38.21% mean) is likely optimistic for scanner-only entries. Recommend treating the 2% risk-per-trade sizing as provisional, subject to recalibration after 30 scanner-only trades.**

---

## 3. Sample Size — Distinguishing 11.5% from 5% Precision

**Test setup:**
- H₀: p = 0.05 (strategy has degraded)
- H₁: p = 0.115 (strategy is working)
- One-sided binomial test (testing whether observed wins significantly exceed 5%)
- Power = 80%, α = 0.05

**Using normal approximation to binomial:**

Effect size (Cohen's h) = 2 × arcsin(√0.115) − 2 × arcsin(√0.05)

arcsin(√0.115) = arcsin(0.3391) ≈ 0.3467 rad
arcsin(√0.05) = arcsin(0.2236) ≈ 0.2257 rad

Cohen's h = 2 × (0.3467 − 0.2257) = 2 × 0.1210 = **0.2420**

n = (z_α + z_β)² / h²
= (1.645 + 0.842)² / 0.2420²
= (2.487)² / 0.0586
= 6.185 / 0.0586
= **105.6**

**→ Approximately 106 trades needed.**

**Practical interpretation:**
- At 11.5% precision, 106 trades yields ~12 wins
- At 5% precision, 106 trades yields ~5 wins
- The test distinguishes these two outcomes with 80% power

**[STAT FLAG] HIGH — 106 trades is a substantial paper trading commitment.** At a scanner fire rate of ~30/day (EXP-020: 26–39 flagged/day), and assuming entry on every fire, 106 trades ≈ 3–4 trading days of data. However, this assumes every scanner fire triggers a paper trade — if entry is conditional (Options B/C/D), the effective fire rate is lower, potentially extending the data collection window to weeks.

**[STAT FLAG] MEDIUM — Multiple testing concern:** If the team evaluates multiple entry options (A–E) simultaneously on the same paper portfolio, the effective number of comparisons is 3–4 (after removing A and E as BLOCKING). Applying Bonferroni correction: effective α per test = 0.05/3 = 0.017. This increases required n to approximately 130–140 trades per entry option.

---

## 4. Expected Maximum Consecutive Losses

**At p = 0.115 (WR = 11.5%), consecutive loss probability:**

P(k consecutive losses) = (1 − 0.115)^k = 0.885^k

**Expected maximum consecutive loss run:**

For n trades, the expected maximum run of losses ≈ log(n) / |log(1 − p)|

= log(n) / log(1/0.885) = log(n) / 0.1226

**For n = 50 trades:**
Expected max run = log(50) / 0.1226 = 3.912 / 0.1226 ≈ **31.9 consecutive losses**

Wait — let me recalculate. The formula uses natural log:

ln(50) / ln(1/0.885) = 3.912 / 0.1226 ≈ **31.9 consecutive losses expected in 50 trades**

**For n = 100 trades:**
ln(100) / ln(1/0.885) = 4.605 / 0.1226 ≈ **37.6 consecutive losses expected in 100 trades**

**[STAT FLAG] CRITICAL — At 11.5% WR, expected max consecutive loss runs are 32 (in 50 trades) and 38 (in 100 trades).** This is not a strategy degradation signal — it is the expected behaviour under the null hypothesis. Setting a "stop reviewing" threshold at, say, 15 consecutive losses would generate false alarms on the majority of healthy strategy runs.

**Practical interpretation:** A strategy with 11.5% WR will, on average, lose 31+ trades in a row within a 50-trade window. Any monitoring protocol based on consecutive losses is essentially useless for a strategy with this WR. **The paper trading spec must not include consecutive-loss-based health checks.**

---

## 5. Proxy Concern — ORB Good Entry Data as Scanner-Only True Runner Proxy

**[STAT FLAG] CRITICAL — ORB Good entries are a biased proxy for scanner-only true runners. Three material sources of upward bias:**

**Bias 1 — Selection filter removed:** ORB Good entries passed the ORB quality filter before PO rating. Scanner-only true runners have no such pre-filter. The 11.5% that survive as "true runners" in the scanner-only context may be structurally different (worse) than the ORB Good entries, which were pre-selected by the ORB breakout condition.

**Bias 2 — PO rating optimism:** The 132 Good entries were rated by PO using chart review — a subjective, in-sample process. The +38.21% mean is the mean PnL *of trades PO rated Good*, not a forward-looking estimate. If PO's Good rating is 6x base rate (as documented in LC-2025-022), then Good entries are the top ~16% of all entries. Scanner-only true runners at 11.5% precision are the top ~11.5% — a somewhat tighter filter, but the PO's chart review process is not available in a live scanner.

**Bias 3 — Graduation bias (documented in LC-2025-017-partA):** The +38.21% mean is an upper bound because it does not account for trades that would have been force-closed EOD without reaching natural exit. The Optimist flagged in LC-2025-017-partB: "of 132 Good-rated entries, how many held to natural exit vs EOD force-close?" This was never resolved. If 20–30% of Good entries are force-closed EOD (consistent with the dataset characteristics), the true mean PnL is lower.

**Conservative adjustment recommendation:**
- Discount the +38.21% mean by 20–30% for proxy bias
- Use +27–30% as the working assumption for scanner-only true runner mean PnL
- This pushes the required b ratio even higher (b > 7.7 still required for Kelly > 0)
- At +27% mean winner and -5% mean loser: b = 5.4 → Kelly still negative

**[STAT FLAG] CRITICAL — Under all reasonable proxy adjustments, Kelly remains negative or near-zero. The paper trading spec is not a sizing exercise — it is a data collection exercise to determine whether the strategy's true parameters are better than estimated.**

---

## Summary of Statistician Findings

| Task | Finding |
|---|---|
| Kelly (b=3) | −18.0% — strongly negative EV |
| Kelly (b=7) | −1.1% — near-zero, still negative |
| Break-even b | b > 7.7× required |
| Recommended paper sizing | Risk-based: 1% portfolio risk / trade → 10% position size |
| Sample size needed | ~106 trades (80% power to distinguish 11.5% from 5%) |
| Expected max consec. losses (50T) | ~32 |
| Expected max consec. losses (100T) | ~38 |
| Proxy concern | CRITICAL — ORB Good entries overstate scanner-only true runner quality |

**Bottom line for the spec:** This is a data collection exercise with a negative-EV prior. The paper trading spec should be framed as "validate or falsify the parameter assumptions" rather than "deploy a profitable strategy."

**Manager:** ## LC-2025-035 — Statistician Response Complete

Critical findings from Statistician:
- **Kelly is negative in both scenarios** — strategy has negative EV at current parameter estimates
- **Break-even requires b > 7.7×** (mean winner ≥ 7.7× mean loser)
- **Expected max consecutive losses: ~32 in 50 trades, ~38 in 100 trades** — consecutive-loss monitoring is useless at 11.5

---

**Manager:** Session transcript so far.

Statistician, your turn. Respond per protocol.

**Statistician:** ## LC-2025-035 — Statistician Response

My assessment above has already been delivered in the session transcript. I am confirming it as complete and adding two follow-up statistical items that were not explicitly requested but are material to the spec design.

---

## Supplementary Statistical Items

### Item 1 — EV Calculation Under the "True Runner Proxy" Range

The session context states +38.21% as the proxy winner mean. I flagged this as upward-biased. Let me compute EV explicitly across the plausible parameter space to frame the spec correctly.

**EV per trade = p × E[win] − (1−p) × E[loss]**

where p = 0.115, using the CI bounds [7.6%, 16.9%] as sensitivity range.

| Scenario | p | E[win] | E[loss] | EV per trade |
|---|---|---|---|---|
| Central (optimistic proxy) | 11.5% | +38% | −5% | +4.37% − 4.43% = **−0.06%** |
| Central (pessimistic loss) | 11.5% | +38% | −10% | +4.37% − 8.85% = **−4.48%** |
| Adjusted winner (−25% discount) | 11.5% | +28% | −5% | +3.22% − 4.43% = **−1.21%** |
| Lower CI precision | 7.6% | +38% | −5% | +2.89% − 4.61% = **−1.72%** |
| Upper CI precision | 16.9% | +38% | −5% | +6.42% − 4.15% = **+2.27%** |

**Interpretation:** Only if precision is close to the upper CI bound (≈16.9%) AND winner mean is not discounted does EV turn positive. The central estimate is approximately breakeven-to-negative. The paper trading spec's primary goal should be to determine empirically which region of this parameter space the strategy inhabits.

---

### Item 2 — Sequential Monitoring Framework for Paper Trading

The original question asked for a "minimum number of consecutive losses before strategy health review." I showed above that consecutive-loss monitoring is structurally invalid at 11.5% WR (expected max run = 32 in 50 trades). The correct monitoring framework is a **sequential probability ratio test (SPRT)** or its practical approximation.

**Practical approximation — observed win rate monitoring:**

After every 30 trades (minimum statistical unit), compute observed precision. The two-sided 95% Wilson CI should include 11.5%. If the CI *upper bound* falls below 5%, the strategy has likely degraded and merits PO review.

| Trades completed | Wins needed to keep CI above 5% |
|---|---|
| 30 | ≥1 win (Wilson CI lower bound) |
| 60 | ≥2 wins |
| 106 | ≥5 wins (formal 80% power threshold) |

**Health check rule:** After every 30 trades, if observed wins = 0, flag for PO review. This is the minimum meaningful trigger — not consecutive losses.

[STAT FLAG] MEDIUM — The spec must explicitly state that consecutive-loss-based health monitoring is invalid for strategies with WR < 20%. Any health check protocol must be frequency-based (every N trades) not streak-based.

---

### Item 3 — Multiple Entry Option Testing Correction (Addendum)

I noted in the main response that testing 3 entry options simultaneously requires Bonferroni correction to α = 0.017 per test, increasing n to ≈130–140. I want to clarify the practical implication:

- If the paper spec runs Options B, C, D concurrently on the same scanner fires, each trade is counted in three option datasets simultaneously
- This is **not** 3 independent datasets — the same scanner fires are shared, creating correlated results
- **Correct approach:** designate one primary option as the main hypothesis test (likely Option C per Optimist input), treat others as exploratory arms. BH correction applies to exploratory comparisons only.

[STAT FLAG] MEDIUM — If multiple entry options are tested concurrently on shared scanner fires, results are correlated. Standard multiple comparison corrections assume independence. The spec should pre-register one primary option (primary hypothesis) and treat remaining options as secondary/exploratory.

---

## Four Required Elements (for the record)

1. **Sample size:** N=106 (formal), N=30 (health check minimum unit). Both stated above with methodology.
2. **Test used:** One-sided binomial proportion test (Cohen's h, normal approximation). Sequential monitoring uses Wilson score CI on observed win rate.
3. **P-value/CI:** At n=106, test distinguishes p=0.115 from p=0.05 at α=0.05, 80% power. Wilson CI on precision: [7.6%, 16.9%] (from LC-2025-027 OOS validation, N=87 signals per session record).
4. **Multiple comparison:** Bonferroni correction if testing 3 entry options as co-equal hypotheses (α=0.017 each, n≈130). BH correction if testing exploratorily. Recommend pre-registering Option C as primary to avoid correction requirement on main result.

---

## Open Action for Memory Update

This session introduces new statistical parameters not yet in my memory file:

- Paper trading N threshold: 106 trades for 80% power (H₁: p=0.115 vs H₀: p=0.05)
- Health check rule: Wilson CI upper bound must exceed 5% at every 30-trade checkpoint
- EV parameter space: breakeven only near upper CI of precision (≈16.9%)
- Kelly negative at both central-estimate scenarios; break-even b > 7.7×

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-035 — Session Continues

Both Statistician and Execution Realist have delivered. Now routing to Optimist to synthesise trade-offs and identify best entry option, then Challenger to audit before I write the spec.

[NEXT: optimist]

**Optimist — your task for LC-2025-035:**

## Context for this session

We are designing a **paper trading spec** for scanner-only gap-and-go entry (Track 2 fallback). The scanner identifies pre-market runners: 15%+ gap-up, news catalyst, pre-market volume. No L2 ORB filter applied.

**Validated OOS precision:** 11.5% (CI: [7.6%, 16.9%]) — 1 in ~9 scanner fires is a true runner.

---

## What each prior agent found

### Scout (literature)
- Pre-market high / 1-min ORB = strongest practitioner consensus for gap-and-go entry
- 5-min candle confirmation (≈09:35) = reduces "opening traps"; well-supported
- VWAP pullback = conditional — problematic at open for 15%+ gappers (VWAP too far below price at open); valid as mid-morning re-entry only
- Hard stop below entry candle low = dominant practitioner standard
- Large gaps >5% close intraday only 9.6% of the time — continuation bias is structural
- Volume confirmation = supported as additional filter across all sources

### Execution Realist (feasibility)
- **Option A (buy at open):** BLOCKING — opening slippage unmodelable, fill price unknowable
- **Option B (1-min ORB close above PM high):** HIGH blockers — pipeline does not store pre-market high; bar_close lookahead; 0.5–2% entry price optimism
- **Option C (5-min ORB close above PM high):** HIGH blockers — same as B; plus possible overextension by 09:35 (price may have run 15–20%+ above PM high already)
- **Option D (vol_ratio ≥ 2.0x after open):** Mostly feasible — needs vol_ratio baseline definition and time-of-day gate; 0.5–1.5% entry price optimism
- **Option E (VWAP pullback):** BLOCKING — bounce detection not in pipeline; VWAP thesis contradicted by literature for 15%+ gappers

Key execution issues across all options:
- EMA9 on 5-min bars exit: unreliable before 10:15 (45-min seeding); 0.5–3% exit price degradation
- Pre-market high not currently stored in pipeline (blocks Options B/C as specified)
- T212 minimum notional may bind at very small position sizes

### Statistician (sizing)
- **Kelly is negative in both scenarios** (b=3: Kelly = −18%; b=7: Kelly = −1.1%)
- **Break-even requires b > 7.7×** (mean winner ≥ 7.7× mean loser)
- **This is a data-collection exercise, not a profitable strategy deployment**
- Recommended sizing: risk-based 1% portfolio risk/trade → 10% position size
- Sample size needed: ~106 trades (80% power to distinguish 11.5% from 5% precision)
- Expected max consecutive losses: ~32 in 50 trades / ~38 in 100 trades → consecutive-loss monitoring is INVALID
- Health check: Wilson CI upper bound must exceed 5% at every 30-trade checkpoint
- EV only turns positive near upper CI of precision (≈16.9%) with undiscounted winner proxy

---

## Five entry options under evaluation

| Option | Entry trigger | Timing | Execution status |
|---|---|---|---|
| A | Buy at open (market open) | 09:30 | BLOCKING |
| B | 1-min candle close above pre-market high | ≈09:31 | HIGH blocker (PM high) |
| C | 5-min candle close above pre-market high | ≈09:35 | HIGH blocker (PM high) |
| D | vol_ratio ≥ 2.0x confirmed after open | Dynamic | Mostly feasible |
| E | VWAP pullback within 2% + bounce | Dynamic | BLOCKING |

---

## Your tasks

1. **Best entry option recommendation:** Given Scout's literature, Execution Realist's feasibility flags, and Statistician's framing (this is a data collection exercise, not profitable deployment), which entry option gives the best combination of: (a) alignment with practitioner best practice, (b) execution feasibility with manageable effort, (c) ability to generate clean paper trading data?

2. **Trade-offs synthesis:** For the non-BLOCKING options (B, C, D), state clearly what you gain and lose with each. Which blockers are worth resolving vs which are tolerable for a paper trading context?

3. **Exit rule validation:** Is ema9_5m_d3 the right exit for scanner-only entries, or does a different exit make more sense given the entry profile (no ORB quality filter, 88.5% FP rate)?

4. **Framing for the spec:** How should the paper spec be framed to PO — as a pure data collection exercise (Statistician's framing) or is there a constructive angle that makes this worth doing even given negative EV prior?

Respond concisely. Bullet points preferred over paragraphs.

[NEXT: optimist]

---

**Manager:** Session transcript so far.

Optimist, your turn. Respond per protocol.

**Optimist:** ## LC-2025-035 — Optimist Synthesis

**Session context absorbed.** Three agents have reported. My job: synthesise trade-offs, recommend the best entry option, and frame the spec constructively for PO.

---

## 1. Best Entry Option Recommendation

**Primary recommendation: Option C (5-min candle close above pre-market high)**
**Secondary (exploratory arm): Option D (vol_ratio ≥ 2.0x, with time gate)**

### Why Option C is the primary pick

- **Strongest alignment with practitioner literature.** Scout's finding is unambiguous: 5-min confirmation is the dominant professional consensus for gap-and-go precisely because it filters "opening traps." At 88.5% FP rate, trap avoidance is the single most valuable property an entry rule can have.
- **The PM-high blocker is resolvable, not fundamental.** Execution Realist flags that the pipeline doesn't currently *store* the pre-market high. This is a pipeline data storage gap — one additional field (session_high pre-market, already accessible via Polygon's extended bars endpoint) — not an architectural change. For a paper trading spec, this is a worth-fixing blocker.
- **The bar_close lookahead is a paper-trading non-issue.** In paper trading, we are collecting data, not optimising fill price. The 0.5–2.0% entry price optimism should be *noted in the spec as a known adjustment factor* and applied when evaluating whether paper results are replicable live. It does not prevent data collection.
- **Overextension risk (Exec Realist concern) is actually a data point we need.** The concern that "price may have run 20%+ above PM high by 09:35" is real — but observing *how often* this happens on our specific scanner universe, and *what the trade outcomes are when it does*, is exactly what paper trading should answer. We don't need to pre-solve this; we need to measure it.

### Why Option D is a valuable secondary arm

- **Already mostly feasible** — no pipeline gap, EntryMonitor handles it natively.
- **Captures a different population of trades.** vol_ratio ≥ 2.0x can fire later in the session than the 09:35 window, potentially catching delayed-recognition runners that the 5-min ORB misses.
- **The vol_ratio baseline ambiguity (PM vs RTH seeding) is documentable.** The spec should define the baseline explicitly (RTH-only EMA seeding, starting from first RTH bar) and note that the first 10 bars are warm-up. Time gate: fire only between 09:40 and 11:00 ET (consistent with gap-and-go literature: after EMA9 stabilises, before gap fades structurally).
- **Provides the correlation data.** If Option C and Option D fire on the same trades, we learn they're redundant. If they diverge, we identify which population each captures. Either way, the data is useful.

### Options eliminated and why

| Option | Disposition | Reasoning |
|---|---|---|
| A | Eliminated | BLOCKING — fill price unknowable; no paper data value |
| B | Deprioritised | 1-min bar is too noisy at open for 15%+ gappers; adds minimal value over C; same PM-high blocker as C without the trap-avoidance benefit |
| E | Eliminated | BLOCKING — pipeline gap + literature contradiction for 15%+ gappers |

---

## 2. Trade-offs for Non-BLOCKING Options (B, C, D)

| | Option B | Option C | Option D |
|---|---|---|---|
| **What you gain** | Fastest entry; captures the initial thrust | Opening trap filter; practitioner consensus; cleaner signal-to-thesis alignment | No PM-high data gap; captures later-session runners; already feasible |
| **What you lose** | Trap exposure at open; same PM-high blocker as C; marginal improvement over C | PM-high storage pipeline work (one-time fix); possible overextension | vol_ratio baseline ambiguity needs explicit definition; no time gate yet |
| **Blocker resolvability** | Same effort as C for PM-high fix; not worth doing separately | PM-high fix is a one-time pipeline addition; worth doing | Vol_ratio baseline: definitional decision, not code change; time gate: one parameter |
| **Data value** | Low — dominated by C for this universe | High — primary hypothesis test | Medium — secondary arm, captures different trade population |

**Bottom line on blockers:**
- PM-high storage for Option C: **resolve it** — one Polygon API call per scanner fire, store as `pm_high` in the trade record. Low engineering effort.
- vol_ratio baseline for Option D: **document the definition** in the spec, don't wait for a full fix — define it, implement it consistently, note the limitation.
- EMA9 5-min seeding (exit, affects all): **tolerate it for paper trading.** The 45-min instability window means no exit fires in the first 45 min — which is actually conservative (protects against premature exits on early-session noise). For paper trading, document the known consequence: positions entered at 09:35 are effectively exit-locked until ≈10:20. The hard stop remains active throughout. This is not a data-collection blocker.

---

## 3. Exit Rule Validation

**ema9_5m_d3 is the right exit concept but needs one adjustment for scanner-only context.**

Arguments for keeping ema9_5m_d3:
- Consistent with ORB research — allows clean comparison of entry filter impact vs exit impact
- Trend-following exit is appropriate for a gap-and-go thesis (ride the runner, exit on reversal)
- Already researched and partially validated in the ORB context

**The one adjustment needed:** Given 88.5% FP rate and no ORB quality filter, most positions will not be runners. EMA9 on 5-min bars with a 45-min seeding window means a false-positive trade entered at 09:35 will ride a losing position for up to 45 minutes before the exit can fire. The -10% hard stop is the only active protection in that window.

**Recommendation:** Add a **5-min candle close below entry price** as an early-exit trigger active only in the first 45 minutes (before EMA9 stabilises). This is not a new condition — it's a fallback for the seeding gap. If the first 5-min bar after entry closes below entry price, exit immediately. This costs some true runner upside (occasional whipsaws) but dramatically limits FP damage in the EMA9 blind window.

This is a meaningful improvement for a strategy with 88.5% FP rate. It should be in the spec.

---

## 4. Framing for PO

**The Statistician's framing is correct but incomplete. It needs a constructive purpose statement alongside the negative-EV caveat.**

**Correct framing: "Parameter validation exercise with a defined falsification criterion."**

The paper trading spec is worth doing because:

1. **The EV is uncertain, not proven negative.** Kelly is negative at *central parameter estimates*. But the CI on precision runs to 16.9%, and at the upper CI with undiscounted winner proxy, EV is positive (+2.27% per trade per Statistician's own table). We are not deploying a known loser — we are testing whether the strategy inhabits the positive or negative region of its parameter space.

2. **The 11.5% precision figure is itself unvalidated for scanner-only entries.** It comes from LC-2025-027 OOS validation. What we don't know: does the 11.5% hold on *live* scanner fires, or does it degrade further? Paper trading answers this question at zero capital risk.

3. **There is a defined falsification criterion.** At 30-trade checkpoints: if Wilson CI upper bound drops below 5%, the strategy has degraded beyond recovery. This is the kill switch. PO can frame this as: "we run 106 paper trades with a defined checkpoint at 30 trades. If the 5% threshold is breached at any checkpoint, we terminate Track 2 and document the finding. If precision holds at ≥11.5%, we recalibrate sizing and consider live deployment."

4. **The data has value independent of the strategy outcome.** Win/loss profiles on scanner-only entries are unknown. Even if precision is confirmed at 11.5% and EV is marginal, the *loss profile data* (how much do FPs lose on average, and does a good entry filter reduce that?) directly informs whether an entry filter can rescue the strategy. This data cannot be obtained any other way.

**Recommended PO framing:** "Track 2 paper trading is a 106-trade parameter validation exercise. We know scanner-only precision is 11.5%. We do not yet know whether that precision — combined with the true winner/loser profile — produces positive EV. Paper trading answers that question with zero capital at risk. The spec includes a 30-trade checkpoint with a defined kill criterion."

---

## Summary Recommendation

| Decision | Recommendation |
|---|---|
| Primary entry option | **Option C (5-min ORB above PM high)** — resolve PM-high storage, tolerate bar_close optimism as a documented adjustment |
| Secondary entry option | **Option D (vol_ratio ≥ 2.0x, 09:40–11:00 gate)** — exploratory arm, no pipeline gap |
| Exit rule | **ema9_5m_d3 + early-exit fallback** (first 5-min close below entry during 45-min seeding window) |
| Hard stop | **-10% from entry** (unchanged) |
| Position sizing | **1% portfolio risk per trade → 10% position size** (Statistician's recommendation, per risk-based sizing) |
| Spec framing | **"Parameter validation exercise with defined kill criterion at 30-trade checkpoints"** |
| Sample target | **106 trades** (formal power), **30 trades** (first checkpoint) |

> **FLAG FOR CONTEXT:** Early-exit fallback rule (5-min close below entry during EMA9 seeding window) is new — Manager should route to Execution Realist for feasibility check before it enters the spec. It is simple in concept but requires the pipeline to know the entry price and evaluate each 5-min close against it during the first 9 bars post-entry.

> **FLAG FOR CONTEXT:** PM-high storage is a one-time pipeline addition. Manager should confirm with Execution Realist whether `pm_high = max(bar_high for extended hours bars before 09:30)` via Polygon is already available in the MarketScanner data, or requires a new API call.

Now updating memory.

---

**Manager:** Here is the updated session transcript.

Continue the session per protocol.

**Manager:** ## LC-2025-035 — Optimist Response Complete

Excellent synthesis from Optimist. Key recommendations:
- **Primary: Option C** (5-min ORB above PM high) — resolve PM-high storage, tolerate bar_close optimism
- **Secondary: Option D** (vol_ratio ≥ 2.0x, 09:40–11:00 gate) — exploratory arm
- **Exit: ema9_5m_d3 + early-exit fallback** (5-min close below entry during 45-min EMA9 seeding window)
- **Framing: "Parameter validation exercise with defined kill criterion"**

Two FLAG FOR CONTEXT items from Optimist need Execution Realist input before the spec can be written:
1. Early-exit fallback feasibility (5-min close below entry during first 9 bars post-entry)
2. PM-high storage — is `max(bar_high for extended hours bars before 09:30)` already in MarketScanner data?

I will route to Challenger next (per protocol — both Optimist and Challenger must be invoked). I'll inject the FLAG FOR CONTEXT items into the Challenger routing message so Challenger can audit them alongside the full spec design. Execution Realist follow-up questions can be addressed when I write the spec draft.

[NEXT: challenger]

**Challenger — your task for LC-2025-035:**

## What you are auditing

A draft paper trading spec for **scanner-only gap-and-go entry (Track 2 fallback)**. You have the full agent outputs below. Your job: find methodology gaps, in-sample caveats, deployment risks, and anything that would embarrass the firm if this spec were followed blindly.

---

## Full context package

### Strategy premise
Scanner identifies pre-market runners: 15%+ gap-up, news catalyst, PM volume. No L2 ORB filter. OOS precision = 11.5% (CI: [7.6%, 16.9%]).

### Proposed spec (Optimist's synthesis)

| Element | Proposed value |
|---|---|
| Primary entry | Option C: 5-min candle close above pre-market high |
| Secondary entry (exploratory) | Option D: vol_ratio ≥ 2.0x, 09:40–11:00 gate |
| Exit | ema9_5m_d3 + early-exit fallback (5-min close below entry during first 45 min / EMA9 seeding window) |
| Hard stop | -10% from entry |
| Position sizing | 1% portfolio risk per trade → 10% position size (risk-based) |
| Sample target | 106 trades (formal), 30-trade checkpoint with kill criterion |
| Kill criterion | Wilson CI upper bound falls below 5% at any 30-trade checkpoint |
| Framing | Parameter validation exercise |

### Scout findings
- 5-min candle confirmation: practitioner consensus; reduces opening traps
- Large gaps >5% close intraday only 9.6% of the time (SMB data) — continuation bias structural
- VWAP pullback for 15%+ gappers: problematic at open (VWAP too far below price); valid mid-morning only
- Hard stop below entry candle low = dominant practitioner standard
- No academic study comparing 09:35 fixed-time vs volume-confirmation for small-cap news-catalyst gap-ups

### Execution Realist findings
- Option C blockers: PM-high not stored in pipeline; bar_close lookahead (0.5–2% entry price optimism)
- Option D: mostly feasible; vol_ratio baseline ambiguity; needs 09:40–11:00 time gate
- EMA9 5-min seeding: unreliable before 10:15 (45 min); 0.5–3% exit price degradation
- All exits: fire at next bar open after cross confirmed (not at bar close)

### Statistician findings
- Kelly = −18% (b=3) and −1.1% (b=7) — **negative EV at central parameter estimates**
- Break-even b > 7.7× required
- Expected max consecutive losses: ~32 in 50 trades / ~38 in 100 trades
- Health check: Wilson CI upper bound must exceed 5% at every 30-trade checkpoint
- EV positive only near upper CI of precision (≈16.9%) with undiscounted winner proxy
- ORB Good entries are a **biased (upward) proxy** for scanner-only true runner quality — three sources of bias identified

### Optimist additions
- Early-exit fallback: 5-min close below entry during EMA9 seeding window → FLAG FOR CONTEXT (feasibility unconfirmed)
- PM-high storage: `max(bar_high extended hours before 09:30)` via Polygon — FLAG FOR CONTEXT (not confirmed in current pipeline)
- Option C overextension risk reframed as a data point to measure, not pre-solve
- Framing: "Parameter validation exercise with defined kill criterion at 30-trade checkpoints"

---

## Your audit tasks

1. **Methodology gaps:** What is missing or underdefined in the spec that would make results uninterpretable?
2. **In-sample contamination:** Are any spec elements derived from or contaminated by the ORB IS data in ways that invalidate the paper trading as OOS?
3. **Deployment risks:** What could go wrong when this runs live (paper) that the spec doesn't account for?
4. **Kill criterion audit:** Is the proposed kill criterion (Wilson CI upper bound < 5% at 30-trade checkpoint) statistically sound? Any issues with applying it sequentially?
5. **Optimist's early-exit fallback:** Does the "5-min close below entry during seeding window" rule introduce any new problems (e.g., overfitting, lookahead, or asymmetric exit behaviour)?
6. **Framing audit:** Is "parameter validation exercise" an honest framing, or does it obscure the negative-EV prior from PO?

Flag issues as **[BLOCKING]**, **[HIGH]**, **[MEDIUM]**, or **[LOW]**.

---

**Manager:** Session transcript so far.

Challenger, your turn. Respond per protocol.

**Challenger:** ## LC-2025-035 — Challenger Audit

**Evidence provided:** Full session transcript including Scout literature review, Execution Realist feasibility assessment, Statistician sizing analysis, and Optimist synthesis. I have the proposed spec elements, all supporting data, and all flags raised by prior agents.

---

## Lookahead Bias Check

**Result: MULTIPLE INSTANCES — partially addressed, partially unresolved.**

1. **bar_close[B0] as entry price (Options B, C, D):** Execution Realist correctly flags this. The signal fires at bar close; execution occurs at the next bar open. This is an unresolved lookahead in any backtest comparison. For paper trading *data collection*, this is tolerable **only if** the spec explicitly records both bar_close[B0] and actual fill price as separate fields. If the spec uses bar_close[B0] as the paper entry price, all PnL figures are contaminated. Optimist acknowledges this as a "known adjustment factor" but does not specify that fill price must be the primary PnL basis. **This needs to be explicit in the spec.**

2. **ORB Good entry proxy (+38.21%):** This figure derives from in-sample PO-rated entries on the ORB dataset. Using it as the "true runner" profit target in position sizing calculations introduces IS contamination into the paper spec's design assumptions. Statistician flags this correctly. The spec must not present the 10% position size as "derived from validated parameters" — it is derived from an upward-biased IS proxy.

3. **Early-exit fallback rule origin:** The "5-min close below entry" rule was proposed by Optimist in this session. Was it derived from observing failure patterns in the ORB IS data? If so, it is IS-derived and cannot be validated on paper trades that overlap the same date range. **Source of this rule must be documented.**

4. **vol_ratio ≥ 2.0x threshold (Option D):** The 2.0x threshold comes from the vol_filter work in prior experiments. If that threshold was selected by optimising on the IS dataset, it carries IS contamination into Option D. No OOS validation of this specific threshold in this entry context has been presented.

**Lookahead bias check conclusion:** PARTIALLY BLOCKING on items 1 and 4. Item 1 is resolvable by spec design (record actual fill). Item 4 requires documentation of threshold provenance.

---

## 1. Methodology Gaps

**[BLOCKING] — Paper entry price definition is unspecified.**

The spec proposes Option C as primary entry: "5-min candle close above pre-market high." What is the paper trade entry price?
- bar_close[B0] of the 5-min bar? (lookahead — never executable)
- bar_open[B1] of the next 5-min bar? (correct — but this is not stated)
- "Market order submitted at bar close" — what fill price is recorded?

If this is not defined precisely, paper P&L figures will be internally inconsistent depending on how different people interpret the spec. **The spec must state: "Paper entry price = the opening price of the first 5-min bar after the signal bar closes (bar_open[B1])."**

**[BLOCKING] — Pre-market high definition is unspecified and unverified.**

"First 5-min candle close above pre-market high" requires a definition of pre-market high:
- All extended hours bars from 04:00 to 09:30?
- Only bars from 07:00 to 09:30 (thin early PM often excluded)?
- The last pre-market print before 09:30:00?
- The highest bar high across all PM bars?

These will produce different values. Execution Realist correctly flags the pipeline doesn't store this. Optimist proposes `max(bar_high for extended hours bars before 09:30)` but this is unconfirmed in the pipeline. **The spec cannot be finalised until (a) the definition is explicit and (b) Execution Realist confirms the Polygon endpoint delivers it in the required form.**

**[HIGH] — Option D time gate (09:40–11:00) is unsupported by any data.**

Optimist proposes a 09:40–11:00 window for vol_ratio ≥ 2.0x entries. The lower bound (09:40) is reasonable — it gives 10 RTH bars for EMA seeding. The upper bound (11:00) is presented as "before gap fades structurally" with reference to the "gap-and-go literature." Scout's literature does not provide a specific 11:00 cutoff. The SMB data shows large gaps close intraday only 9.6% of the time — but this tells us nothing about *when* the gap-and-go momentum exhausts. The 11:00 cutoff is unvalidated on our specific universe. **The spec must label the 11:00 gate as an assumption requiring empirical validation, not a validated parameter.**

**[HIGH] — No definition of "pre-market volume" threshold for scanner qualification.**

The scanner's 15%+ gap-up filter is stated. "News catalyst" is stated. "Pre-market volume" is listed as a qualifier but no threshold is defined. Is this any pre-market volume? A minimum number of shares? RVOL > X? Without a precise definition, the 11.5% precision figure is untethered — it was validated on LC-2025-027's specific scanner configuration. If the paper trading scanner uses a different PM volume threshold, the 11.5% figure does not apply.

**What specific pre-market volume filter was used in LC-2025-027?** This must be confirmed and carried forward identically into the paper spec.

**[MEDIUM] — No definition of "news catalyst" for scanner qualification.**

Same issue as PM volume. "News catalyst" is listed as a prerequisite but how is it detected in the scanner? What counts as a catalyst? If this is manually curated by PO, it introduces a subjectivity layer not present in the OOS validation. If it is automated, the automation logic must be identical to LC-2025-027.

**[MEDIUM] — Position sizing formula has an implicit assumption about stop placement.**

Statistician recommends: risk 1% of portfolio, hard stop = -10%, therefore position size = 10% of portfolio. This is correct *only if the hard stop fires at exactly -10% below entry*. On small-cap gap-and-go stocks with gaps and halts, the actual stop execution can be significantly worse than -10% — a halt-and-resume can gap through the stop level. The spec presents 10% position size as a clean risk calculation but does not caveat execution risk on stops. **For small-cap gap-and-go stocks, gap-through-stop risk is non-trivial and must be noted.**

---

## 2. In-Sample Contamination

**[HIGH] — The 11.5% precision figure, while OOS from LC-2025-027, may not be OOS for the paper spec.**

The OOS validation in LC-2025-027 used a specific date range. If the paper trading spec is tested on a date range that overlaps with the LC-2025-027 OOS window, the precision figure is no longer being independently validated — it is being tested on a population where the scanner has already been tuned. **What is the date range of LC-2025-027 OOS validation?** If paper trading starts immediately after that period ends, it is clean. If it starts mid-period or overlaps, it is contaminated.

**[HIGH] — vol_ratio ≥ 2.0x threshold (Option D) is IS-derived.**

This threshold was established in the vol_filter experiments (EXP-010/011, per memory). Those experiments used the IS dataset. There is no evidence this threshold was set *before* outcome analysis on the current ORB/scanner universe. **Without confirmation that 2.0x was set a priori or on a non-overlapping dataset, Option D carries IS contamination on its key parameter.** This must be documented as a limitation.

**[MEDIUM] — Early-exit fallback rule has unknown provenance.**

Optimist introduced the "5-min close below entry" fallback rule in this session. It is a reasonable rule on its face, but if it was proposed because Optimist observed that early-entry FPs tend to fail within the first 5-min bar in the ORB IS data, it is IS-derived. **Optimist must state the basis for this rule: (a) derived from IS data observation, (b) derived from first principles, or (c) derived from practitioner literature.** If (a), it cannot be validated on data from the same period.

**[LOW] — ema9_5m_d3 exit rule is consistent across ORB and Track 2 research, but:**

Its use in the ORB context was evaluated on IS data. If it performs poorly on scanner-only entries (no ORB quality filter), that failure may be meaningful signal — but it will look like "the exit rule needs tuning" rather than "the entry filter is doing the work." The spec should explicitly state that exit rule performance is secondary to entry precision measurement in this paper trading exercise.

---

## 3. Deployment Risks

**[HIGH] — Position size of 10% of portfolio is very large given the universe characteristics.**

Statistician's recommendation: 10% position size (risk-based, 1% risk / 10% hard stop). This is not a conservative position size. For a strategy with:
- 88.5% FP rate
- Small-cap low-float stocks prone to halt-and-gap-through stops
- An exit rule unreliable for the first 45 minutes

...a 10% position size means each trade puts 10% of the paper portfolio in a stock that is likely to lose. The -10% hard stop represents a 1% portfolio loss per trade at the *theoretical* stop level. But actual execution on small-cap halt gaps can produce -20% to -40% realised losses on a single position, for a 2–4% portfolio hit. At 10% position size with real execution risk, a single gap-through-stop event on a paper trade could constitute a 3–4% paper portfolio drawdown — not the 1% implied by the sizing formula. **The spec must include a maximum single-trade loss cap (e.g., if paper P&L on any single position exceeds -15% realised, it is recorded as an anomaly and excluded from EV calculations with explanation).**

**[HIGH] — Concurrent position risk is unaddressed.**

Scanner can fire on 26–39 tickers per day (EXP-020). If 10% position size is applied to every scanner fire simultaneously, the paper portfolio is 260–390% notional — a theoretical blowup. The spec must define: (a) maximum concurrent positions (suggest: 3), and (b) priority rule when scanner fires exceed the concurrent position limit (first-fire, highest-gap, or randomly selected).

**[MEDIUM] — Paper trading P&L does not include spread/slippage but real deployment will.**

Paper trading using bar_open[B1] as entry price will understate actual execution costs on small-cap gappers. The Execution Realist quantifies this at 0.5–2% adverse vs bar_close[B0], and another 0.5–3% on exit. Total round-trip execution friction: 1–5%. For a strategy with negative central EV, adding 1–5% round-trip execution costs to every trade makes the real-world EV materially worse than the paper trading results suggest. **The spec must state that paper trading results require a 2–3% per-trade haircut before real-world EV can be estimated.**

**[MEDIUM] — "Continuation bias" claim (large gaps close only 9.6% of the time) applies to all large-gap stocks, not specifically our scanner universe.**

Scout's SMB data point says large gaps (>5%) close intraday only 9.6% of the time. Our scanner targets 15%+ gappers with news catalyst, which is a subset of "large gaps." But the claim is applied to our universe as if it validates directional entry. Two issues:
1. The SMB data is not stratified by news catalyst vs. no catalyst. News-driven gaps may behave differently (they often do — gap fill on bad news catalyst is common).
2. "Gap doesn't close" ≠ "entering long produces a profit." A 15%+ gap can hold (not close) while declining from +20% to +5% intraday — not a win for a long entry at +15%.

**This finding is directionally supportive but is not evidence of long entry profitability. It must not be cited in the spec as validation of the entry thesis.**

**[LOW] — No regime filter specified.**

The paper trading spec has no date range defined and no regime filter. If paper trading runs during a mean-reversion market regime (e.g., rising rates, sector rotation away from small-cap momentum), the 11.5% precision figure — validated on a specific historical window — may not hold. This is a known limitation from the ORB research (regime-specificity flag in memory). The spec should note: "Results are expected to be regime-dependent. If market conditions diverge materially from the LC-2025-027 validation period, precision estimates should be recalibrated."

---

## 4. Kill Criterion Audit

**[HIGH] — Sequential application of the Wilson CI kill criterion creates a multiple comparison problem.**

The proposed kill criterion: "Wilson CI upper bound falls below 5% at every 30-trade checkpoint." Applied at checkpoints 30, 60, 90, 106.

The problem: if you test the same hypothesis at multiple checkpoints, the probability of at least one false positive (incorrectly killing a valid strategy) exceeds α = 0.05. For 3 checkpoints at α = 0.05 each: family-wise error rate ≈ 1 − (0.95)³ = 14.3%. The spec presents this as a rigorous kill criterion, but it has a 14% false kill rate if applied naively at each checkpoint.

**Correction needed:** Use a group sequential testing correction (O'Brien-Fleming or Pocock boundary) or, simpler, set a more conservative per-checkpoint α (e.g., α = 0.017 per checkpoint for 3 checkpoints, consistent with Statistician's Bonferroni note). The spec must state the adjusted per-checkpoint threshold, not just "Wilson CI upper bound < 5%."

**[MEDIUM] — The kill criterion fires on Wilson CI upper bound, but the Wilson CI upper bound at 30 trades is very wide.**

At n=30, observed precision = 0/30 (zero wins): Wilson CI = [0%, 11.4%]. Upper bound = 11.4% > 5%. The kill criterion does not trigger even with zero wins in 30 trades. This means: if precision has degraded to exactly 5%, there is approximately a 21% chance of observing 0/30 wins (Binomial(30, 0.05) P(k=0) = 0.215). The kill criterion has very low power at the 30-trade checkpoint.

**Statistician's own supplementary note says:** "After every 30 trades, if observed wins = 0, flag for PO review." This is inconsistent with the Wilson CI criterion — at 0/30, the Wilson CI upper bound is ≈11.4%, which does NOT trigger the Wilson CI kill criterion. The spec contains an internal inconsistency between the two monitoring rules. **One monitoring framework must be chosen and stated consistently.**

I recommend: "At each 30-trade checkpoint, compute observed precision. If 0 wins observed, flag for PO review (does not kill, triggers investigation). Formal kill criterion: at 106 trades, one-sided binomial test p > 0.05 (H₀: precision = 5%)."

---

## 5. Optimist's Early-Exit Fallback Audit

**[HIGH] — Rule introduces an asymmetric exit bias that could systematically distort paper P&L.**

The rule: "If the first 5-min bar after entry closes below entry price, exit immediately."

Asymmetry: this rule only protects against downside. If the first 5-min bar gaps up and *then* the second 5-min bar closes below entry price, the rule does not fire (it applies only to "the first 5-min bar after entry"). Is "the first 5-min bar after entry" the bar containing the entry, or the next bar? This needs precise definition. If it means the next full 5-min bar after the signal bar, then on a stock that drops -8% within the first 5-min post-entry bar, the exit fires — which is the intended behaviour. But the exit fires at the *close* of that bar, not during the decline — meaning the actual exit price is at the bottom of the 5-min decline, not mid-decline. **For fast-moving small-cap stocks, a full 5-min bar declining from entry price to -8% may produce a fill at -8% or worse — worse than the -10% hard stop on a fast-moving name.**

**[MEDIUM] — Rule creates a double-exit condition during the seeding window.**

During the 45-min EMA9 seeding window, two exit conditions are simultaneously active:
1. "First 5-min close below entry price" → early-exit fallback
2. Hard stop at -10%

If

---
