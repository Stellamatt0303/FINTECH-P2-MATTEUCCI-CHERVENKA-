# strategy_rules.md — 36-Month Low Volatility

Pre-registration for Project 2, The Strategy Lab (FINA 4075/5075, Fall 2026).
Draft for partner review until the pre-registration commit. Locked at that
commit; this file governs if the code and the file ever disagree.

STRATEGY: Low volatility, 36-month (Strategy Menu, Section 2, item (c)).
  One signal only. Test whether relatively stable stocks improve risk-adjusted
  performance with relatively low turnover; outperformance is not assumed.

UNIVERSE: The 200 stocks in P2_ticker_list_2026-08-31.csv, all of them, every
  month. No additions and no liquidity, price, or sector screens. If the
  instructor's extension file marks a stock as delisted, it leaves the universe
  from the following month (Data Dictionary, Section 4).

DATA: panel_returns_2026-08-31.csv, simple monthly total returns, row 0 =
  January 2019, row 91 = August 2026. SHA-256:
  c9d3340eba3a3301a63bb788c87f1d6e9e55de58a3fec16b12a34b313cac076b
  Plus the instructor's dated extension files for September, October, and
  November 2026, each committed with its checkpoint entry. Posted files are
  authoritative; no rebuilt panel is used for graded numbers. Do not edit or
  re-save the source return files. Validate the released panel's hash, 92
  monthly rows, and 200 unique ticker columns.

SIGNAL: For portfolio month t, sample standard deviation of exactly the 36
  monthly total returns from t-36 through t-1 inclusive, using ddof=1.
  Total volatility, not beta or residual volatility. No skip-month: include
  t-1 and exclude t. In code:
      vol = rets[t-36:t, :].std(axis=0, ddof=1)
  Rank unrounded monthly volatility; annualization is for display only.
  MISSING DATA: If any required window return is missing, the stock is
  ineligible that month and is not ranked. Do not fill with zero or shorten
  the window. The released panel has no missing values; this governs the
  live window. If fewer than 20 stocks are eligible, stop and seek instructor
  guidance rather than inventing a portfolio rule.

RANKING: Ascending by volatility (lowest first).

TIE-BREAK: Alphabetical ticker order, using Python string order, for exact
  signal ties. At the 20th/21st boundary, fill remaining slots with the
  alphabetically earliest tied tickers, up to exactly 20 holdings.

PORTFOLIO: The 20 lowest-volatility eligible stocks, equal weights of 1/20
  (5%) each, fully invested, long only. Reset weights at every month-end
  rebalance. No sector constraints or second signal.

REBALANCE: Monthly. Select the portfolio held during month t at the end of
  t-1 using only information through that completed month-end. Signal
  computation and the rebalance trade are assumed to occur at the month-end
  close; state this simplification in the report. No within-month rebalance
  or discretionary substitutions. First portfolio: January 2022 (row 36),
  using January 2019 through December 2021 returns. In-sample backtest:
  January 2022 through August 2026, inclusive, 56 months. Earlier observations
  are warm-up data only.

COSTS: 10 basis points per side (0.0010). One-way turnover = number of names
  in month t's portfolio not held in t-1, divided by 20.
      monthly cost = 2 x 0.0010 x turnover
      gross return = mean of the 20 holdings' returns for month t
      net return = gross return - monthly cost
  The first month of any run counts as a full purchase (turnover = 1), giving
  cost drag of 0.0020, or 0.20%, under the prescribed formula.
  Turnover counts name replacement only. Resetting continuing holdings'
  weights after drift is assumed costless, fixed for both tracks and the
  placebo. Report both gross and net performance.

BENCHMARK: Equal-weighted average of stocks active that month (all 200 until
  a name delists, remaining active names thereafter), rebalanced monthly,
  no costs. Compare over identical dates: January 2022–August 2026 for the
  backtest and September–November 2026 for the live evaluation. Start each
  growth path at $10,000 before its first performance month and compound
  monthly returns. Net returns govern the primary strategy growth path.

LIVE WINDOW: September, October, and November 2026, scored at the three
  checkpoints. September's portfolio uses September 2023–August 2026 returns
  (36 months) from the released panel and is recorded in monitoring_log.md
  entry 0 within the pre-registration commit. Select each later portfolio
  when the instructor's extension file posts and record it in that
  checkpoint's entry before the month it is scored on.
  October uses October 2023–September 2026; November uses November
  2023–October 2026. Never use a scored month's return to choose its holdings.

PLACEBO PLAN (pre-registered): 1,000 random portfolios. Use numpy default_rng,
  seed 4075. Each draws 20 distinct tickers without replacement from stocks
  active at the start of the live window, assigns equal weights, then buys
  and holds those names across the live months. Do not redraw monthly.
  Apply the same cost formula; first month = full purchase. A delisted holding
  is dropped and its weight redistributed equally, matching the example's
  active-universe rule. For each track, report the gap versus the benchmark
  and its percentile in the placebo distribution of gaps. This is the
  buy-and-hold live placebo specified in the instructor's example.

REPORTING: Follow Section 3 of the Detailed Student Instructions: CAGR,
  annualized volatility (sample monthly standard deviation x sqrt(12)),
  Sharpe defined as CAGR / annualized volatility with rf = 0, maximum
  drawdown of the growth path as a negative percentage, and annual one-way
  turnover (mean monthly turnover x 12). State the 56-month backtest length.

NO: Leverage, shorting, cash or T-bill positions, discretionary overrides,
  sector filters, parameter changes (window, holding count, weights, cost
  rate), or edits after the pre-registration commit. Such changes carry
  deduction code P0 under the instructor's example.
