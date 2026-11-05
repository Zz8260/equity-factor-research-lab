"""Chronological learning, factor diagnostics and an explicit toy portfolio."""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .factors import FEATURES


def chronological_split(panel):
    dates = sorted(panel.date.unique())
    if len(dates) < 30:
        raise ValueError("At least 30 usable dates are required.")
    train_end, validation_end = dates[int(len(dates) * 0.6)], dates[int(len(dates) * 0.8)]
    train = panel[(panel.date < train_end) & (panel.execution_date < train_end)].copy()
    validation = panel[(panel.date >= train_end) & (panel.date < validation_end) & (panel.execution_date < validation_end)].copy()
    test = panel[panel.date >= validation_end].copy()
    if any(part.empty for part in [train, validation, test]):
        raise ValueError("Empty chronological partition.")
    return train, validation, test


def rank_ic(panel, score):
    result = {}
    for date, group in panel.groupby("date"):
        # Pearson correlation of average ranks is Spearman correlation.
        a, b = group[score].rank(), group.target_return.rank()
        result[date] = a.corr(b) if a.nunique() > 1 and b.nunique() > 1 else np.nan
    return pd.Series(result, name="rank_ic", dtype=float)


def fit_model(train, validation, test):
    y = train.groupby("date").target_return.rank(pct=True) - 0.5
    candidates, fitted = [], {}
    for alpha in [0.1, 1.0, 10.0, 100.0]:
        model = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
        model.fit(train[FEATURES], y)
        scored = validation.assign(score=model.predict(validation[FEATURES]))
        ic = float(rank_ic(scored, "score").mean())
        candidates.append({"alpha": alpha, "validation_mean_rank_ic": ic})
        fitted[alpha] = model
    best = max(candidates, key=lambda c: c["validation_mean_rank_ic"])
    model = fitted[best["alpha"]]
    # Keep the train-only fit fixed. The validation set selects alpha only.
    predictions = test.assign(score=model.predict(test[FEATURES]))
    coefficients = pd.DataFrame({"feature": FEATURES, "coefficient_on_training_scaled_features": model.named_steps["ridge"].coef_})
    return predictions, pd.DataFrame(candidates), coefficients, model


def simulate_portfolio(predictions, cost_bps=10.0, quantile=0.2):
    """Intraday long/short: close to cash daily; charge both entry and exit."""
    if not np.isfinite(cost_bps) or cost_bps < 0 or not 0 < quantile <= 0.5:
        raise ValueError("Costs must be finite and nonnegative; quantile must be in (0, 0.5].")
    rows, holdings = [], []
    for date, group in predictions.groupby("date", sort=True):
        g = group.sort_values(["score", "symbol"]).copy()
        n = max(1, int(len(g) * quantile))
        weights = pd.Series(0.0, index=g.index)
        weights.loc[g.index[:n]] = -0.5 / n
        weights.loc[g.index[-n:]] = 0.5 / n
        gross = float((weights * g.target_return).sum())
        # Gross exposure is 1.0, entry+exit turnover is 2.0 per session.
        turnover = float(2 * weights.abs().sum())
        cost = turnover * cost_bps / 10000
        rows.append({"signal_date": date, "date": g.execution_date.iloc[0], "gross_return": gross, "turnover": turnover, "cost": cost, "net_return": gross - cost, "equal_weight_universe_return": float(g.target_return.mean())})
        g["weight"] = weights
        holdings.append(g[["date", "execution_date", "symbol", "score", "weight", "target_return"]])
    daily = pd.DataFrame(rows)
    if daily.empty:
        raise ValueError("No predictions to evaluate.")
    daily["gross_equity"] = (1 + daily.gross_return).cumprod()
    daily["net_equity"] = (1 + daily.net_return).cumprod()
    return daily, pd.concat(holdings, ignore_index=True)


def portfolio_metrics(daily):
    net = daily.net_return
    volatility = float(net.std(ddof=1))
    equity_with_initial = pd.concat([pd.Series([1.0]), daily.net_equity], ignore_index=True)
    drawdown = equity_with_initial / equity_with_initial.cummax() - 1
    return {"test_sessions": len(daily), "gross_total_return": float(daily.gross_equity.iloc[-1] - 1), "net_total_return": float(daily.net_equity.iloc[-1] - 1), "annualized_net_volatility": volatility * np.sqrt(252), "annualized_net_sharpe_zero_rf": float(net.mean() / volatility * np.sqrt(252)) if volatility > 0 else None, "max_net_drawdown": float(drawdown.min()), "average_round_trip_turnover": float(daily.turnover.mean())}
