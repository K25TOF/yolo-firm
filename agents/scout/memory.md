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

### Session LC-2025-028 — Backtest-to-Paper Trading Transition Framework
**Date:** 2026-03-31
**Research question:** What validation steps are minimum for transitioning a multi-layer intraday momentum strategy (scanner → entry → exit) to paper trading? How should a pipeline with mixed validation states be handled? What does "minimum viable paper trading" look like? Is kappa=0.661 strong agreement for a trading label?

**Searches conducted:**
1. "backtest to paper trading validation framework intraday momentum small cap"
2. "multi-layer signal pipeline validation scanner entry exit trading research methodology"
3. "minimum paper trading period intraday strategy validation statistical significance trades required"
4. "Cohen kappa 0.66 interpretation trading label classification agreement threshold"
5. "walk-forward validation minimum viable trading strategy component testing sequential pipeline Peterson"
6. "paper trading minimum sample size forward test intraday strategy 30 100 trades validation bar"
7. "trading strategy component validation individually before integration filter entry exit signal pipeline testing best practice"
8. "bar close execution bias intraday backtest lookahead bias academic research small cap momentum"

---

## Known Sources

### ORB Strategy

- **Zarattini, Barbon & Aziz (SSRN:4729284, Feb 2024)** — "A Profitable Day Trading Strategy For The U.S. Equity Market." Swiss Finance Institute working paper. 5-min ORB on 7,000+ US stocks 2016–2023 (survivorship-bias-free CRSP data). Key finding: top-20 "Stocks in Play" portfolio: 1,600%+ total return, Sharpe 2.81, annualized alpha 36%. Stocks in Play = stocks with above-normal activity due to fundamental news. 5-min window best performer across 5/15/30/60-min tested. *Highest quality ORB source; SSRN working paper, not peer-reviewed journal.*

- **Zarattini & Aziz (SSRN:4416622, Apr 2023)** — ORB on QQQ/TQQQ 2016–2023. Annualized alpha 33% net of commissions. *SSRN; not peer-reviewed.*

- **Holmberg, Lönnbark & Lundström (Finance Research Letters, 2013)** — "Assessing the profitability of intraday opening range breakout strategies." Peer-reviewed Elsevier journal. Finds ORB strategies yield "significantly higher returns than zero," challenging EMH. *Peer-reviewed academic; highest quality.*

- **Wang et al. (IEEE Access, 2019)** — "Assessing the Profitability of Timely Opening Range Breakout on Index Futures Markets." Over 8% annual returns with p<3% in all five markets. *Peer-reviewed IEEE; medium-high quality.*

- **Wang & Gangwar (SSRN:5198458, Mar 2025)** — ORB on NSE single security. Variants show positive returns vs B&H but p-values 0.45-0.50; "statistically indecisive in a one-year sample for one security." Concludes ORB "operationally appealing but would need stricter data coverage, transactions cost modeling, and advanced significance testing." *New source; relevant caution for low-sample validation.*

- **QuantConnect (practitioner replication)** — 17% win rate on ORB without Stocks in Play filter. 2.396 Sharpe WITH filter. *Informal.*

### RSI Exit Signals

- **Hill, Arthur (SSRN:3412429, Feb 2019)** — RSI bull range (40–100); break below 40 = exit from bull range. *Practitioner-academic; SSRN.*

- **Panigrahi (SSRN:3986000, Feb 2022)** — RSI 60/40 outperforms 50-50 on NIFTY 50. *SSRN.*

- **Tyagi (SSRN:5386654, 2025)** — RSI 60/40 + Dow Theory. *SSRN.*

- **CFA Institute Digest (2013)** — Bajgrowicz & Scaillet: technical trading rules no economic value after costs since 1962. *[SCOUT CONFLICT]; high quality.*

- **TradingView/EdgeTools** — No statistically significant predictive power for RSI extreme readings after multiple-testing correction. *[SCOUT CONFLICT]; practitioner.*

### Momentum Exhaustion Patterns

- **J.P. Morgan QDS (practitioner, 2015)** — Momentum underperforms at turning points; tail risk and negative skewness more likely. *Institutional practitioner.*

- **Chabot, Ghysels & Jagannathan (NBER WP 20660, 2014)** — Momentum crashes predictable. *High quality; NBER.*

- **Springer Financial Innovation (Jan 2025)** — Momentum shows "abnormal profitability" but "concerns persist regarding reliability due to significant volatility." *Peer-reviewed; high quality.*

### Small-Cap Scanner / RVOL Methodology

- **Zarattini et al. (SSRN:4729284, 2024)** — RVOL ≥ 2.0 as Stocks in Play filter. *Best available academic-adjacent source.*

- **StockCharts ChartSchool** — RVOL >2.0 common "in play" threshold. *Practitioner reference.*

### Backtest-to-Paper-Trading Transition Framework (New — LC-2025-028)

- **Peterson, Brian G. (BraveRock, "Developing & Backtesting Systematic Trading Strategies")** — Canonical practitioner-academic reference. Key principles: (1) test components individually before integration; (2) "too many rules will make a backtest look excellent in-sample, and may even work in walk forward analysis, but are very dangerous in production"; (3) post-trade reconciliation between backtest and production requires identical information set. *High-quality practitioner-academic; widely cited in quant community.*

- **Pardo, Robert E. (1992, "Design, Testing and Optimization of Trading Systems")** — Originator of walk-forward analysis framework. WFA = optimization on training set, test on subsequent period, roll forward. First principle: "we don't really care about in-sample results; what matters is out-of-sample system performance." *Foundational practitioner text.*

- **AlgoStrategyAnalyzer / practitioner guide (Jan 2026)** — Multi-phase validation: (1) base setup, (2) initial testing with each entry rule isolated, (3) optimization, (4) robustness (WFA + Monte Carlo), (5) portfolio/risk management. Rule: "If an entry rule doesn't show edge on its own, discard it — filters improve, they don't create edge." Each condition should generate at least 200 trades independently before integration. *Practitioner; medium quality but highly concrete.*

- **FTMO Academy (Feb 2025)** — Forward testing (paper trading) guidance: "A good threshold is to experience between 20 to 100 situations (trades) before making the move to live trading." Also recommends 30-day "shadow phase" to measure strategy participation rate. *Practitioner educational.*

- **Collin Seow / practitioner (Mar 2026)** — Forward testing: "Analyse your forward-testing results with a meaningful sample size – typically 50–100 trades." Metrics: expectancy, profit factor, maximum drawdown. Slippage stress test: "if your strategy can't handle slippage 50-100% higher than current averages, it's likely too fragile." *Practitioner/informal.*

- **BacktestBase (Jan 2026)** — Sample size benchmarks citing López de Prado: ~30 trades = CLT floor; ~100 trades = basic reliability; ~200-500 trades = institutional-grade confidence. Key distinction: "500 trades in 6 months (one regime) is less reliable than 100 trades over 5 years (multiple regimes)." *Practitioner reference.*

- **Medium / Trading Dude (Jul 2025)** — "Minimum of 30 trades to begin statistical inference. Aim for 100+ trades for reliable performance metrics." Paper trading = "final out-of-sample test." *Practitioner/informal.*

- **Quantopian / Portfolio123 cohort study (practitioner-academic)** — 888 Quantopian algorithms analyzed IS vs OOS. Filtered out strategies backtested less than 500 days, Sharpe < -1.0. Each algorithm had minimum 6 months of frozen OOS data. Confirmed IS Sharpe overfitting. *Practitioner-academic hybrid; medium-high quality.*

- **GoatFundedTrader / Backtesting Best Practices (Feb 2026)** — Recommends "30 to 60-day paper-trading mirror" to calibrate slippage, commission, and latency, using empirical numbers back in the simulator. *Practitioner; informal.*

- **InteractiveBrokers Campus (Jun 2025)** — Vector-based backtesting: "risk constraints enforced only at bar close; intraday breaches missed until next bar." Explicitly flags that assuming fills at next bar's close ignores intra-bar price moves and bid-ask spreads. Recommends event-based backtesting for intraday strategies requiring precise execution. *High-quality practitioner from institutional source.*

- **arXiv 2512.12924 (Dec 2025)** — "Interpretable Hypothesis-Driven Trading: A Rigorous Walk-Forward Validation Framework." Combines walk-forward testing with interpretable hypothesis-driven signals. Notes RL approaches "fail profitability tests once realistic transaction costs are included." *arXiv preprint; academic-adjacent.*

- **Quantreo Newsletter (Dec 2025)** — Look-ahead bias: "A strategy affected by it may look stable, profitable, and well-behaved in a backtest, yet it has no chance of surviving live trading." Common source: misaligned targets, improper validation, feature computation errors. *Practitioner/informal.*

- **Trading Dude (Medium, 2025)** — "Never use the close of the same candle to decide a trade at that close. Use the next bar's open instead." Direct relevance to our documented bar_close[B0] execution bias. *Practitioner/informal; widely cited rule.*

### Kappa=0.661 Interpretation

- **Landis & Koch (1977, cited via Wikipedia/Cohen's Kappa)** — Standard kappa magnitude guidelines: 0.00–0.20 = slight; 0.21–0.40 = fair; 0.41–0.60 = moderate; **0.61–0.80 = substantial**; 0.81–1.00 = almost perfect. Kappa=0.661 falls in the **substantial agreement** band. *Standard reference; Landis & Koch note these are guidelines, not universal standards.*

- **Bakeman et al. (cited via Wikipedia/Cohen's Kappa)** — "No one value of kappa can be regarded as universally acceptable." Kappa values affected by: number of categories, prevalence of categories, observer bias. With binary classification and imbalanced classes, kappa may understate or overstate agreement.

- **PLOS One (2019)** — Caution: in unbalanced binary classification, kappa can exhibit "undesired behaviour — a worse classifier gets higher kappa score." Recommends using Matthews Correlation Coefficient (MCC) as complement. *Peer-reviewed; relevant for imbalanced trading labels.*

---

## Dead-End Paths

- "multi-bar confirmation window false positive reduction technical trading academic" — no academic papers on N-bar persistence specifically.
- "catastrophic drawdown guard circuit breaker systematic trend following exit" — returned drawdown management blogs; no papers on RSI/EMA guard for individual stock catastrophic declines.
- "persistence confirmation technical indicator signal filter academic research" — practitioner/TradingView content only.
- "relative volume RVOL intraday momentum small cap academic study evidence threshold" — no dedicated academic paper on RVOL thresholds; best source remains Zarattini et al. (2024).
- "multi-layer signal pipeline validation scanner entry exit trading research methodology" — returned pipeline architecture articles (data pipeline design), not signal pipeline validation methodology papers. Peterson (BraveRock) is closest available academic-adjacent reference.

---

## Key Conflicts Noted

- **[SCOUT CONFLICT]:** Holmberg et al. (2013) and Zarattini et al. (2024) find ORB profitable. QuantifiedStrategies finds ORB "much less relevant now" for indices/ETFs. Resolution: RVOL/news filter is load-bearing.

- **[SCOUT CONFLICT]:** CFA Institute digest (Bajgrowicz & Scaillet, 2013) finds technical trading rules no economic value after costs. Broadly challenges RSI/EMA-based guards.

- **[SCOUT CONFLICT]:** EdgeTools/TradingView: "no statistically significant predictive power" for RSI extreme readings after multiple-testing correction.

- **[SCOUT CONFLICT]:** QuantConnect: 17% win rate without Stocks in Play filter vs Zarattini's 56%+ with filter. RVOL filter is load-bearing.

- **[SCOUT CONFLICT]:** Bar_close[B0] execution bias in our backtest. Literature (IB Campus, Trading Dude) explicitly flags this as a look-ahead/execution bias source. "Never use the close of the same candle to decide a trade at that close — use the next bar's open instead." Our documented bias in Layer 2 entry is flagged by external literature as a known source of inflated backtest performance.

- **[SCOUT CONFLICT]:** Wang & Gangwar (SSRN, Mar 2025) show ORB returns positive vs B&H but statistically indecisive (p ~0.45–0.50) on a one-year single-security sample. Implies our scanner OOS validation (21/183 fires, ~11 months) may not achieve statistical decisiveness even if directionally correct.

- **[SCOUT CONFLICT]:** PLOS One (2019) cautions that kappa can give a worse classifier higher scores in imbalanced binary problems. Our mechanical label (MFE_30bar<10%) may be imbalanced; kappa=0.661 should be complemented with MCC or F1 for full picture.
