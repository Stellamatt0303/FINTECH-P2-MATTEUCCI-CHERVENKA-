"""
strategy.py — LOCKED STRATEGY CODE (Track 1)
FINA 4075/5075 Project 2 — Fall 2026

Rule (strategy_rules.md governs if the two ever disagree):
  For portfolio month t, calculate each eligible stock's sample standard
  deviation over the 36 monthly total returns t-36 through t-1, with ddof=1
  and no skip-month. Rank ascending, breaking exact ties alphabetically by
  ticker. Hold the 20 lowest-volatility stocks at equal weights, rebalance
  monthly, and charge 10 basis points per side.

CODE RULE: after the pre-registration commit, rerun this file unchanged at
each checkpoint. Do not edit it in response to backtest or live results.
"""

import numpy as np
import pandas as pd


PER_SIDE = 0.0010
N_HOLD = 20
WINDOW = 36
FIRST_TRADEABLE = WINDOW       # row 36 = January 2022


def load_panel(panel_path, ticker_path):
    """Read the course files and return (rets, dates, tickers, info).

    rets: T x N NumPy array of simple monthly total returns.
    dates: month-end dates from the panel.
    tickers: ticker symbols in panel-column order.
    info: instructor ticker-list data indexed by Ticker.
    """
    panel = pd.read_csv(panel_path, index_col=0, parse_dates=True)
    info = pd.read_csv(ticker_path).set_index("Ticker")

    panel.columns = panel.columns.astype(str).str.strip()
    info.index = info.index.astype(str).str.strip()
    panel = panel.apply(pd.to_numeric, errors="raise")

    tickers = list(panel.columns)
    assert list(info.index) == tickers, "ticker list and panel columns differ"
    assert panel.index.is_monotonic_increasing, "panel dates are not chronological"
    assert panel.index.is_unique, "panel contains duplicate dates"
    assert len(tickers) == len(set(tickers)), "panel contains duplicate tickers"
    assert not np.isinf(panel.to_numpy()).any(), "panel contains infinite returns"

    return panel.to_numpy(dtype=float), panel.index, tickers, info


def signal(t, rets):
    """Sample volatility over rows t-36 through t-1 inclusive."""
    window = rets[t - WINDOW:t]
    assert window.shape[0] == WINDOW
    return np.std(window, axis=0, ddof=1)


def select_holdings(t, rets, tickers):
    """Return indices of the 20 eligible stocks with lowest volatility.

    A stock is ineligible if any return in its 36-month signal window is
    missing. Exact volatility ties are broken alphabetically by ticker.
    """
    if t < FIRST_TRADEABLE:
        raise ValueError("36 months of history are required before selection")

    window = rets[t - WINDOW:t]
    eligible = np.isfinite(window).all(axis=0)
    vol = signal(t, rets)

    candidates = [i for i in range(len(tickers)) if eligible[i]]
    if len(candidates) < N_HOLD:
        raise ValueError("fewer than 20 stocks have complete 36-month histories")

    order = sorted(candidates, key=lambda i: (vol[i], tickers[i]))
    return set(order[:N_HOLD])


def run_track(select_fn, rets, t0, t1, per_side=PER_SIDE):
    """Run a strategy from row t0 through row t1, inclusive.

    Equal weights; first month turnover = 1; later one-way turnover equals
    names entering divided by 20; monthly cost = 2 * per_side * turnover.
    Returns (values, turnovers, holdings), where values starts at 1.0.
    """
    if not (0 <= t0 <= t1 < len(rets)):
        raise ValueError("invalid backtest row range")

    previous = set()
    values = [1.0]
    turnovers = []
    holdings = []

    for t in range(t0, t1 + 1):
        current = select_fn(t, rets)
        if len(current) != N_HOLD:
            raise ValueError("selection rule must return exactly 20 holdings")

        turnover = 1.0 if not previous else len(current - previous) / N_HOLD
        gross_return = rets[t, sorted(current)].mean()
        cost = 2 * per_side * turnover
        net_return = gross_return - cost

        values.append(values[-1] * (1 + net_return))
        turnovers.append(turnover)
        holdings.append(current)
        previous = current

    return np.array(values), np.array(turnovers), holdings


def bench(rets, t0, t1):
    """Equal-weighted full-panel benchmark, monthly rebalanced, no costs."""
    if not (0 <= t0 <= t1 < len(rets)):
        raise ValueError("invalid benchmark row range")

    values = [1.0]
    for t in range(t0, t1 + 1):
        active = np.isfinite(rets[t])
        if not active.any():
            raise ValueError(f"no active benchmark stocks in row {t}")
        monthly_return = rets[t, active].mean()
        values.append(values[-1] * (1 + monthly_return))
    return np.array(values)


def stats(values, turns=None):
    """Calculate the performance measures required by the assignment."""
    values = np.asarray(values, dtype=float)
    months = len(values) - 1
    if months < 2:
        raise ValueError("at least two return months are required for statistics")

    monthly = values[1:] / values[:-1] - 1
    cagr = (values[-1] / values[0]) ** (12 / months) - 1
    vol = monthly.std(ddof=1) * np.sqrt(12)
    sharpe = cagr / vol if vol != 0 else np.nan
    maxdd = (values / np.maximum.accumulate(values) - 1).min()

    output = {
        "CAGR": cagr,
        "Annualized volatility": vol,
        "Sharpe (rf = 0)": sharpe,
        "Maximum drawdown": maxdd,
        "Growth of $10,000": 10000 * values[-1],
    }

    if turns is not None:
        turns = np.asarray(turns, dtype=float)
        if len(turns) != months:
            raise ValueError("turnover count must equal return-month count")
        output["Annual one-way turnover"] = turns.mean() * 12
        output["Cost drag per year"] = 2 * PER_SIDE * turns.mean() * 12

    return output


def run_low_volatility_backtest(rets, tickers):
    """Convenience wrapper for January 2022 through the panel's final month."""
    if len(rets) <= FIRST_TRADEABLE:
        raise ValueError("panel does not contain a tradeable month")

    select_fn = lambda t, data: select_holdings(t, data, tickers)
    t0 = FIRST_TRADEABLE
    t1 = len(rets) - 1

    strategy_values, turnovers, holdings = run_track(
        select_fn, rets, t0, t1
    )
    benchmark_values = bench(rets, t0, t1)

    return strategy_values, benchmark_values, turnovers, holdings, t0, t1
