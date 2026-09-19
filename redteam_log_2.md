# redteam_log.md — FINTECH-P2-Example (Round 2)

Red-team of strategy_rules.md before the pre-registration commit (Project 2, Step 6).
Third reviewer: Claude (Sonnet 5), claude.ai, 9/18/2026. Route: pasted the full rules file
(post Round-1 fixes) with the instruction "find every ambiguity that would let a dishonest
researcher flex this backtest later; quote the phrase, explain the exploit, propose exact
replacement wording." Ten findings.

FINDING 1 — Delisted-stock return is unspecified at the point of exit.
  Quote: "If the instructor's extension file marks a stock as delisted, it leaves the universe
  from the following month."
  Exploit: the rule fixes when a stock exits but not what return it contributes in its final
  active month — last traded price, 0%, or -100% are all consistent with the text, and each
  moves gross return, benchmark, and placebo differently. A researcher could pick whichever
  flatters the result after seeing it.
  FIX: added to UNIVERSE/DATA — "A stock's return for the month in which it delists is taken
  exactly as given in the instructor's extension file, with no invented, floored, or capped
  value; this return feeds that month's gross return, benchmark, and placebo calculations as
  applicable. The stock is excluded from all universes starting the following month."

FINDING 2 — "Exact" ties are not defined in floating point.
  Quote: "TIE-BREAK: Alphabetical ticker order ... for exact signal ties."
  Exploit: volatility is a float computed from real data; "exact" equality between two
  independently-coded computations can fail on the last bit even when economically identical.
  A researcher could claim a boundary case is "not exactly tied" (or is) depending on which
  answer helps.
  FIX: rewrote TIE-BREAK — "Two stocks are tied if their computed volatilities are equal when
  rounded to 10 decimal places under the single reference implementation in [file/function].
  Disputes are resolved by re-running that one implementation, not by independent re-derivation."

FINDING 3 — The live-window recording deadline permits a lookahead window.
  Quote: "Select each later portfolio when the instructor's extension file posts and record it
  in that checkpoint's entry before the month it is scored on."
  Exploit: as worded, an entry committed any time before the scored month *ends* arguably
  satisfies "before the month it is scored on," letting a researcher watch weeks of the scored
  month's price action before finalizing the pick — defeating the point of a live test.
  FIX: rewrote LIVE WINDOW — "...and record it in that checkpoint's entry no later than
  11:59pm on the last calendar day before the first day of the month it is scored on. The
  commit timestamp is binding; an entry committed on or after the first day of the scored month
  is invalid and that checkpoint is scored using the benchmark only."

FINDING 4 — The placebo's random-draw sequence is not reproducibly pinned down.
  Quote: "Use numpy default_rng, seed 4075. Each draws 20 distinct tickers without
  replacement..."
  Exploit: a fixed seed alone doesn't fix the output — ticker ordering (alphabetical vs. CSV
  column order vs. shuffled) and whether one Generator is reused across all 1,000 draws vs.
  reseeded each time both change every resulting portfolio. "Seed 4075" could be cited
  truthfully while the placebo distribution is quietly rerolled until it looks favorable.
  FIX: added to PLACEBO PLAN — "Construct rng = np.random.default_rng(4075) once. Sort the
  eligible tickers alphabetically. For i in 0..999, draw rng.choice(tickers, size=20,
  replace=False) in a single loop using this one Generator instance, in this order, with no
  intervening random calls. This exact procedure, run once, is the pre-registered placebo set
  and is not regenerated."

FINDING 5 — "Track" and "gap" are used but never defined.
  Quote: "For each track, report the gap versus the benchmark and its percentile in the placebo
  distribution of gaps."
  Exploit: "gap" could mean a CAGR difference, a total-return difference, or a Sharpe
  difference — these rank differently — and "track" is never tied to specific date ranges.
  Leaving both open lets a researcher select whichever metric produces the best percentile
  after the fact.
  FIX: added definitions — "'Track' means the in-sample backtest (Jan 2022–Aug 2026) and the
  live window (Sep–Nov 2026), scored separately. 'Gap' means (strategy net CAGR − benchmark
  CAGR) for that track. Compute this gap for the actual strategy and for each of the 1,000
  placebo portfolios, then report the strategy's percentile rank within the placebo gaps."

FINDING 6 — Annual turnover doesn't say whether the first-month spike is included.
  Quote: "annual one-way turnover (mean monthly turnover x 12)."
  Exploit: the first month of any run is a mandated 100% turnover. Whether that month is
  included in the mean barely matters over 56 backtest months but is a huge lever over the
  3-month live window — an easy way to claim the strategy is "low turnover" by excluding it.
  FIX: rewrote REPORTING — "Annual one-way turnover = mean of all monthly turnover values in
  the reporting window, including the initial full-purchase month, x 12. Report backtest and
  live-window turnover separately; do not blend them."

FINDING 7 — Drawdown, volatility, and Sharpe don't say gross or net.
  Quote: "maximum drawdown of the growth path ..." / "Sharpe defined as CAGR / annualized
  volatility."
  Exploit: the file separately says net returns govern the benchmark comparison, but never
  states whether drawdown/vol/Sharpe are computed on the gross or net path — leaving room to
  headline whichever looks better and call it "the" number.
  FIX: added to REPORTING — "CAGR, annualized volatility, Sharpe, and maximum drawdown are
  computed on the net growth path as the primary figures, and also computed and labeled on the
  gross growth path for comparison."

FINDING 8 — "Both tracks" in the costs section references an undefined term.
  Quote: "Resetting continuing holdings' weights after drift is assumed costless, fixed for
  both tracks and the placebo."
  Exploit: same gap as Finding 5 — an undefined "track" is a seam a researcher can later argue
  a given calculation (e.g. "the live track") wasn't actually covered by this clause.
  FIX: resolved by cross-reference once "track" is defined in Finding 5's fix; no separate
  rewrite needed.

FINDING 9 — CAGR's compounding formula is left implicit.
  Quote: "CAGR, annualized volatility ..., Sharpe ..., maximum drawdown ..., and annual one-way
  turnover ... State the 56-month backtest length."
  Exploit: with a non-integer number of years (56 months = 4.667 years), more than one
  defensible annualization formula exists, and the choice can move CAGR by tens of basis
  points — enough to flip a strategy-vs-benchmark comparison.
  FIX: added to REPORTING — "CAGR = (V_end / V_start)^(12/n) − 1, where n is the number of
  monthly returns compounded (56 for the backtest, 3 for the live window) and V_start/V_end are
  the growth-path values before the first and after the last performance month."

FINDING 10 — The "NO" list doesn't cover the conventions fixed elsewhere.
  Quote: "NO: Leverage, shorting, cash or T-bill positions, discretionary overrides, sector
  filters, parameter changes (window, holding count, weights, cost rate), or edits after the
  pre-registration commit."
  Exploit: this list locks down five named parameters but not the tie-break tolerance,
  delisting-return treatment, gap definition, turnover-averaging convention, or gross/net basis
  for risk stats — exactly the items Findings 1–7 pin down. A researcher could argue changing
  one of those "isn't a parameter change" and so escapes the anti-flexing rule entirely.
  FIX: extended the list — "...or edits after the pre-registration commit. This prohibition
  covers not only the five parameters above but also every computational convention fixed
  elsewhere in this document (tie-break tolerance, delisting-return treatment, gap definition,
  turnover-averaging window, gross/net basis for risk statistics, and the placebo RNG
  procedure). Any such change after the pre-registration commit carries deduction code P0."

Effect on the numbers: none of the ten fixes change the chosen strategy — universe, signal,
ranking, weights, rebalance cadence, and cost rate are untouched. All ten sit in the downstream
bookkeeping layer (delisting treatment, tie tolerance, RNG procedure, metric definitions,
annualization convention) — exactly where a backtest can be flexed after seeing results while
still technically matching the pre-registered rules. The value of this round is that those
conventions are now pinned down before the live window begins.
