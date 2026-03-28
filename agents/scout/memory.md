# Scout Memory

## Search History

### Session LC-2025-016 — Guard C Review
**Date:** 2026-03-28
**Research question:** Does external literature support Guard C (RSI<40 + price<EMA5 + 5-bar confirmation) as an exit guard on momentum trades in catastrophic decline clusters?

**Searches conducted:**
1. "RSI exit signal momentum strategy academic research"
2. "EMA short-term trend break exit signal RSI combined strategy research"
3. "multi-bar confirmation window false positive reduction technical trading academic"
4. "catastrophic drawdown guard circuit breaker systematic trend following exit"
5. "RSI threshold 40 momentum exit signal academic paper SSRN"
6. "persistence confirmation technical indicator signal filter academic research"

---

### Session LC-2025-017 — Baseline + Research Plan
**Date:** 2026-03-28
**Research question:** External literature sweep on four topics: (1) ORB strategies, (2) RSI exit signals, (3) Momentum exhaustion, (4) Small-cap scanner / RVOL methodology

**Searches conducted:**
1. "opening range breakout strategy academic research win rate evidence"
2. "RSI exit signal momentum trading exhaustion academic paper SSRN"
3. "momentum exhaustion volume decay price divergence exit signal academic study"
4. "small cap momentum scanner RVOL threshold filter methodology academic practitioner"
5. "Zarattini Barbon Aziz ORB opening range breakout stocks in play 2024 SSRN"
6. "relative volume RVOL intraday momentum small cap academic study evidence threshold"

---

## Known Sources

### ORB Strategy

- **Zarattini, Barbon & Aziz (SSRN:4729284, Feb 2024)** — "A Profitable Day Trading Strategy For The U.S. Equity Market." Swiss Finance Institute working paper. 5-min ORB on 7,000+ US stocks 2016–2023 (survivorship-bias-free CRSP data). Key finding: top-20 "Stocks in Play" portfolio: 1,600%+ total return, Sharpe 2.81, annualized alpha 36%. Stocks in Play = stocks with above-normal activity due to fundamental news. 5-min window best performer across 5/15/30/60-min tested. *Highest quality ORB source; SSRN working paper, not peer-reviewed journal.*

- **Zarattini & Aziz (SSRN:4416622, Apr 2023)** — ORB on QQQ/TQQQ 2016–2023. Annualized alpha 33% net of commissions. *SSRN; not peer-reviewed.*

- **Holmberg, Lönnbark & Lundström (Finance Research Letters, 2013)** — "Assessing the profitability of intraday opening range breakout strategies." Peer-reviewed Elsevier journal. Finds ORB strategies yield "significantly higher returns than zero," challenging EMH. Used normally-distributed returns to identify breakout days. *Peer-reviewed academic; highest quality.*

- **Wang et al. (IEEE Access, 2019)** — "Assessing the Profitability of Timely Opening Range Breakout on Index Futures Markets." 1-min intraday data on DJIA, S&P, TAIEX, and others. Over 8% annual returns with p<3% in all five markets; best performance in TAIEX. TORB signals aligned with institutional trader direction. Short probing window best for US markets. *Peer-reviewed IEEE; medium-high quality.*

- **QuantifiedStrategies (practitioner backtest, undated)** — ORB on S&P 500 futures: "opening range breakout strategies are much less relevant now than they used to be, at least for the most traded futures contracts or ETFs." Recommends daily filters to improve. Important caveat for index/ETF application. *Practitioner; informal.*

- **QuantConnect (practitioner replication, undated)** — Recreation of Zarattini et al. 2024 methodology. Achieved 2.396 Sharpe vs 0.836 buy-and-hold (SPY) in 2016. 5-min ORB best-performing duration. 68% of parameter combinations outperformed benchmark. *Practitioner replication; informal.*

- **OptionAlpha (practitioner backtest, 2025)** — 60-min ORB for 0DTE options: 89.4% win rate. But this is options strategy on index, very different from stock ORB. *Practitioner; informal.*

- **ChartSwatcher (practitioner, May 2025)** — 5-min ORB on S&P 500 futures: ~55-60% win rate; average gain >0.5% per trade. Earnings-gap days showed 20-30% higher breakout probability. *Practitioner/informal; not peer-reviewed.*

### RSI Exit Signals

- **Hill, Arthur (SSRN:3412429, Feb 2019)** — "Finding Consistent Trends with Strong Momentum: RSI for Trend-Following and Momentum Strategies." Tests RSI range signals on S&P 500 stocks. Key finding: RSI bull range (RSI between 40–100) captures trend consistency; a break below 40 signals exit from bull range. Describes 40 as the lower bound of a "bull range" — directly relevant as Guard C uses RSI<40 as its exit trigger. *Practitioner-academic hybrid; SSRN, not peer-reviewed journal.*

- **Panigrahi, Ashok (SSRN:3986000, Feb 2022)** — RSI 60/40 thresholds on NIFTY 50. Finds 60-40 strategy outperforms 50-50 for short-term returns. RSI<40 as exit threshold has documented practitioner-academic support. *SSRN working paper.*

- **Tyagi, Vipul (SSRN:5386654, 2025)** — RSI 60/40 integrated with Dow Theory trend confirmation. Relevant to "RSI below 40 = exit" logic combined with trend indicator (conceptually similar to Guard C's EMA5 component). *SSRN working paper.*

- **irjmets.com study (June 2024)** — RSI 40/60 thresholds tested on Indian equities. Selling when RSI falls below 40 described as mechanism to "exit as a stock is falling and prevents getting caught in prolonged downtrends." *Low-tier journal; treat as practitioner-level only.*

- **QuantifiedStrategies RSI Range-Momentum (practitioner, 2025)** — RSI bull range (40–100) + RSI momentum >70 = buy signal; exit when both fail. Backtested on SPY since 1993. 12 signals, 10 winners, modest max drawdown. *Practitioner backtest blog.*

- **Maróy, Ákos (SSRN:5095349, Jan 2025)** — Intraday momentum exit strategies: VWAP and ladder-based exits outperform simple indicator exits (Sharpe >3.0, annualized >50%). Exit strategy choice matters significantly. *SSRN.*

- **CFA Institute Digest (2013)** — Summary of Bajgrowicz & Scaillet: technical trading rules have no economic value after transaction costs since 1962. IMPORTANT CONFLICT. *High quality; peer-reviewed digest.*

- **TradingView/EdgeTools study (undated)** — Large-scale RSI study: "RSI extreme readings provide no statistically significant predictive power after accounting for multiple testing." *Practitioner/informal; large-scale but not peer-reviewed.*

- **Collin Seow / practitioner (2026)** — RSI as early warning system for momentum exhaustion; RSI bearish divergence + MACD crossover + ADX weakening = exit signal. *Practitioner/informal.*

### Momentum Exhaustion Patterns

- **J.P. Morgan QDS (practitioner paper, 2015)** — "Momentum Strategies Across Asset Classes." Momentum strategies underperform during turning points and mean-reverting periods. Trend exhaustion phase: "asset price starts moving sideways and downtrend." Tail risk and negative skewness more likely at turning points. *Institutional practitioner paper; high credibility but not peer-reviewed.*

- **Chabot, Ghysels & Jagannathan (NBER WP 20660, 2014)** — Momentum crashes predictable: more likely when momentum recently performed well, interest rates low, or momentum recently outperformed the market. Three-factor alpha 1%/month 1927–2012. *High quality; NBER working paper.*

- **Wikipedia / Volume Analysis (standard reference)** — Extreme volume (5-10x normal) signals exhaustion: all buyers or sellers used up; price stops moving in prior trajectory. Sharp rise + extreme volume = potential reversal. *Reference; not academic.*

- **EC Markets (practitioner, Mar 2026)** — Market exhaustion: "slowing momentum, RSI divergence, and subsequent structure breaks that trigger reversals." When price makes new extreme but RSI fails to confirm = weakening momentum. Stop-loss clusters accelerate reversals. BIS research cited on liquidity deterioration. *Practitioner; cites academic sources.*

- **TradingBrokers (practitioner, Aug 2025)** — Exhaustion indicators: RSI divergence (classic sign), volume anomalies (shrinking volume in trend direction = diminishing participation), momentum decay, overbought/oversold conditions. "There is no single best trend exhaustion indicator; traders often use a blend." *Practitioner/informal.*

- **Springer Financial Innovation (Jan 2025)** — Momentum strategies show "abnormal profitability" but "concerns persist regarding reliability due to significant volatility and susceptibility to substantial losses." Statistical analyses assuming persistence of past patterns produce unreliable out-of-sample results. *Peer-reviewed journal; high quality.*

### Small-Cap Scanner / RVOL Methodology

- **Zarattini, Barbon & Aziz (SSRN:4729284, 2024)** — Explicitly uses "Relative Volume of at least 100%" (RVOL ≥ 2.0) as a filter for "Stocks in Play." Best-performing stocks table filtered by RVOL ≥ 2.0. 5-min ORB with RVOL filter produced Sharpe 2.81 vs unfiltered universe. *Most directly relevant academic-adjacent source for RVOL threshold.*

- **StockCharts ChartSchool (reference, 2025)** — RVOL >2.0: many day traders use as minimum threshold for "stock in play." RVOL >4.0 may signal reversal rather than continuation (exhaustion). RVOL-TOD (time-of-day adjusted) preferred for intraday use. *Practitioner reference; widely cited.*

- **Plus500 / IG Group (practitioner references, 2024-26)** — RVOL >2.0 commonly cited as "in play" threshold. RVOL 1.3–1.8 = growing institutional participation. RVOL >5.0 = climactic/exhaustion. 20-day lookback most common baseline. NYSE data cited: "breakouts with RVOL >2.0 demonstrate 40% greater follow-through" (source quality uncertain). *Practitioner; informal.*

- **TradingSim (practitioner, 2024)** — "Some traders believe a stock needs at least 2.0 RVOL to be considered in play." For penny/momentum stocks, small cap stocks with news can easily hit 10+ RVOL. RVOL of 2 "would be nothing" for small cap news stocks. *Practitioner/informal.*

- **Quora (practitioner community, undated)** — For small caps: "An RVOL of 2 would be nothing [for small cap news stocks]... those kinds of stocks can easily hit 10+ RVOL." Practical guidance: flag RVOL ≥ 2 for closer look; prioritize RVOL ≥ 5 for high-confidence setups. *Informal/community; low quality but directionally consistent.*

- **UseThinkScript Warrior Trading scanner (practitioner, 2022)** — Example scan: minRelVol = 1.5, minMovePct = 5%, price $1-$30, 20-day lookback. Works best before 11:30 AM. *Practitioner implementation; informal.*

---

## Dead-End Paths

- "multi-bar confirmation window false positive reduction technical trading academic" — no academic papers on N-bar persistence specifically.
- "catastrophic drawdown guard circuit breaker systematic trend following exit" — returned drawdown management blogs and trend-following general literature; no papers on RSI/EMA guard for individual stock catastrophic declines.
- "persistence confirmation technical indicator signal filter academic research" — practitioner and TradingView content only.
- "relative volume RVOL intraday momentum small cap academic study evidence threshold" — no dedicated academic paper on RVOL thresholds; best source remains Zarattini et al. (2024) which uses RVOL ≥ 2.0 as Stocks in Play filter.

---

## Key Conflicts Noted

- **[SCOUT CONFLICT]:** Holmberg et al. (2013, peer-reviewed) and Zarattini et al. (2024, SSRN) find ORB profitable. QuantifiedStrategies practitioner backtest finds ORB "much less relevant now" for indices/ETFs. Resolution: Zarattini's edge depends heavily on Stocks in Play filter (RVOL + news catalyst) — plain ORB on indices appears weaker.

- **[SCOUT CONFLICT]:** CFA Institute digest (Bajgrowicz & Scaillet, 2013) finds technical trading rules have no economic value after transaction costs. This broadly challenges all RSI/EMA-based guard designs. However, Guard C is not a standalone alpha-generating strategy — it is a conditional exit guard applied only to confirmed catastrophic declines.

- **[SCOUT CONFLICT]:** EdgeTools/TradingView large-scale RSI study finds "no statistically significant predictive power" for RSI extreme readings after multiple-testing correction. Directly challenges RSI<40 as exit trigger in isolation.

- **[SCOUT CONFLICT]:** QuantConnect win rate note: "The algorithm as written has a 17% win rate (83% loss rate)" for ORB on liquid US equities without Stocks in Play filter. Starkly different from Zarattini's Stocks in Play results. Confirms that the RVOL/news filter is load-bearing for ORB profitability.
