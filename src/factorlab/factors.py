"""Cross-sectional signals using observations available by each day's close."""

import numpy as np
import pandas as pd

from .data import validate_panel

FEATURES = ["earnings_yield", "book_to_price", "profitability_residual", "reversal_20d", "sampled_volatility", "trade_imbalance", "book_imbalance", "opening_gap"]


def neutralize(values, log_size, industry):
    """OLS residual against an intercept, log market cap and industry dummies."""
    y = np.asarray(values, dtype=float)
    x = np.column_stack([np.ones(len(y)), np.asarray(log_size, dtype=float), pd.get_dummies(industry, drop_first=True, dtype=float).to_numpy()])
    return y - x @ np.linalg.lstsq(x, y, rcond=None)[0]


def build_factors(daily, intraday):
    validate_panel(daily)
    validate_panel(intraday, intraday=True)
    daily_keys = pd.MultiIndex.from_frame(daily[["date", "symbol"]])
    tick_keys = pd.MultiIndex.from_frame(intraday[["date", "symbol"]]).unique()
    if len(daily_keys.difference(tick_keys)) or len(tick_keys.difference(daily_keys)):
        raise ValueError("Daily and intraday observation keys must match.")
    d = daily.sort_values(["symbol", "date"]).copy()
    d["earnings_yield"] = d.earnings / d.market_cap
    d["book_to_price"] = d.book_equity / d.market_cap
    previous_close = d.groupby("symbol").close.shift(1)
    d["opening_gap"] = d.open / previous_close - 1
    d["close_return"] = d.close / previous_close - 1
    weighted = d.close_return * d.turnover
    rolling_sum = weighted.groupby(d.symbol).transform(lambda x: x.rolling(20, min_periods=20).sum())
    rolling_weight = d.groupby("symbol").turnover.transform(lambda x: x.rolling(20, min_periods=20).sum())
    d["reversal_20d"] = -rolling_sum / rolling_weight.replace(0, np.nan)
    d["profitability_residual"] = np.nan
    for _, group in d.groupby("date"):
        x = np.column_stack([np.ones(len(group)), group.earnings_yield.to_numpy()])
        d.loc[group.index, "profitability_residual"] = group.roe - x @ np.linalg.lstsq(x, group.roe, rcond=None)[0]
    t = intraday.sort_values(["symbol", "date", "time"]).copy()
    t["sample_return"] = t.groupby(["symbol", "date"]).close.pct_change(fill_method=None)
    t["squared_return"] = t.sample_return ** 2
    t["depth_imbalance"] = (t.bid_depth - t.ask_depth) / (t.bid_depth + t.ask_depth).replace(0, np.nan)
    stats = t.groupby(["date", "symbol"]).agg(
        squared_return=("squared_return", "sum"), buy_volume=("buy_volume", "sum"), sell_volume=("sell_volume", "sum"), book_imbalance=("depth_imbalance", "mean"))
    stats["sampled_volatility"] = np.sqrt(stats.squared_return)
    stats["trade_imbalance"] = (stats.buy_volume - stats.sell_volume) / (stats.buy_volume + stats.sell_volume).replace(0, np.nan)
    d = d.merge(stats[FEATURES[4:7]], on=["date", "symbol"], how="left", validate="one_to_one")
    return d[["date", "symbol", "market_cap", "industry", *FEATURES]].sort_values(["date", "symbol"]).reset_index(drop=True)


def prepare_features(raw):
    """Date-local winsorization, neutralization and rank transformation."""
    parts = []
    for _, group in raw.groupby("date", sort=True):
        g = group.dropna(subset=FEATURES).copy()
        if len(g) < 10:
            continue
        for feature in FEATURES:
            v = g[feature].clip(g[feature].quantile(0.01), g[feature].quantile(0.99))
            residual = neutralize(v, np.log(g.market_cap), g.industry)
            g[feature] = pd.Series(residual, index=g.index).rank(pct=True) - 0.5
        parts.append(g)
    if not parts:
        raise ValueError("No usable cross-sections after the 20-day warmup.")
    return pd.concat(parts, ignore_index=True)


def attach_targets(features, daily):
    """Signal after close t; enter at open t+1, exit at close t+1."""
    d = daily.sort_values(["symbol", "date"]).copy()
    grouped = d.groupby("symbol")
    d["execution_date"] = grouped.date.shift(-1)
    d["target_return"] = (d.close / d.open - 1).groupby(d.symbol).shift(-1)
    # Missing symbols must not silently jump across a market session.
    calendar = sorted(daily.date.unique())
    next_date = dict(zip(calendar[:-1], calendar[1:]))
    expected = d.date.map(next_date)
    valid = d.execution_date.eq(expected) & d.execution_date.notna()
    labels = d.loc[valid, ["date", "symbol", "execution_date", "target_return"]]
    return features.merge(labels, on=["date", "symbol"], how="inner", validate="one_to_one")
