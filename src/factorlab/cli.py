"""Run the complete offline synthetic demonstration."""

import argparse
import importlib.metadata
from pathlib import Path

import pandas as pd

from .data import generate_synthetic
from .evaluation import chronological_split, fit_model, portfolio_metrics, rank_ic, simulate_portfolio
from .factors import FEATURES, attach_targets, build_factors, prepare_features
from .report import write_report


def run_demo(output="reports", seed=42, days=260, symbols=60, cost_bps=10.0):
    import numpy as np
    if not np.isfinite(cost_bps) or cost_bps < 0:
        raise ValueError("Cost in basis points must be finite and nonnegative.")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    daily, intraday = generate_synthetic(seed, days, symbols)
    raw = build_factors(daily, intraday)
    panel = attach_targets(prepare_features(raw), daily)
    train, validation, test = chronological_split(panel)
    predictions, tuning, coefficients, _ = fit_model(train, validation, test)
    returns, positions = simulate_portfolio(predictions, cost_bps)
    diagnostics = pd.DataFrame([{"feature": f, "mean_rank_ic": float(rank_ic(test, f).mean())} for f in FEATURES])
    metrics = portfolio_metrics(returns)
    metrics["model_mean_rank_ic"] = float(rank_ic(predictions, "score").mean())
    partitions = {name: {"signal_start": str(part.date.min().date()), "signal_end": str(part.date.max().date()), "last_label_date": str(part.execution_date.max().date()), "rows": len(part)} for name, part in [("train", train), ("validation", validation), ("test", test)]}
    best_alpha = float(tuning.loc[tuning.validation_mean_rank_ic.idxmax(), "alpha"])
    metadata = {"seed": seed, "days": days, "symbols": symbols, "cost_bps": cost_bps, "selected_ridge_alpha": best_alpha, "partitions": partitions, "versions": {p: importlib.metadata.version(p) for p in ["numpy", "pandas", "matplotlib", "scikit-learn"]}}
    for name, frame in {"raw_factors": raw, "processed_panel": panel, "test_predictions": predictions, "validation_scores": tuning, "model_coefficients": coefficients, "factor_diagnostics": diagnostics, "daily_returns": returns, "positions": positions}.items():
        frame.to_csv(output / f"{name}.csv", index=False)
    write_report(output, returns, diagnostics, metrics, metadata)
    print(f"Synthetic demonstration completed: {output / 'demo_report.html'}")
    print(f"Test sessions: {metrics['test_sessions']}; model mean rank IC: {metrics['model_mean_rank_ic']:.4f}")
    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["demo"])
    parser.add_argument("--output", default="reports")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--days", type=int, default=260)
    parser.add_argument("--symbols", type=int, default=60)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    args = parser.parse_args()
    run_demo(args.output, args.seed, args.days, args.symbols, args.cost_bps)


if __name__ == "__main__":
    main()
