import numpy as np
import pandas as pd
import pytest

from factorlab.cli import run_demo
from factorlab.data import generate_synthetic, validate_panel
from factorlab.evaluation import chronological_split, fit_model, portfolio_metrics, simulate_portfolio
from factorlab.factors import FEATURES, attach_targets, build_factors, neutralize, prepare_features


@pytest.fixture(scope="module")
def panels():
    return generate_synthetic(seed=7, days=100, symbols=20)


def test_deterministic_and_valid(panels):
    daily, intraday = panels
    a, b = generate_synthetic(seed=7, days=100, symbols=20)
    pd.testing.assert_frame_equal(daily, a)
    pd.testing.assert_frame_equal(intraday, b)
    with pytest.raises(ValueError):
        validate_panel(pd.concat([daily, daily.iloc[:1]]))
    with pytest.raises(ValueError):
        validate_panel(daily.assign(close=-1))


def test_neutralization_is_orthogonal():
    rng = np.random.default_rng(1)
    size = rng.normal(size=60)
    industry = pd.Series(["A", "B", "C"] * 20)
    y = 3 + size * 2 + (industry == "B") * 4 + rng.normal(size=60)
    residual = neutralize(y, size, industry)
    design = np.column_stack([np.ones(60), size, pd.get_dummies(industry, drop_first=True)])
    np.testing.assert_allclose(design.T @ residual, 0, atol=1e-10)


def test_future_observations_do_not_change_past_features(panels):
    daily, intraday = panels
    cutoff = daily.date.unique()[65]
    full = prepare_features(build_factors(daily, intraday))
    prefix = prepare_features(build_factors(daily[daily.date <= cutoff], intraday[intraday.date <= cutoff]))
    pd.testing.assert_frame_equal(full[full.date <= cutoff].reset_index(drop=True), prefix)


def test_target_alignment_and_missing_session(panels):
    daily, intraday = panels
    features = prepare_features(build_factors(daily, intraday))
    panel = attach_targets(features, daily)
    sample = panel.iloc[0]
    next_bar = daily[(daily.date == sample.execution_date) & (daily.symbol == sample.symbol)].iloc[0]
    assert sample.target_return == pytest.approx(next_bar.close / next_bar.open - 1)
    assert sample.execution_date > sample.date
    missing = daily[~((daily.date == sample.execution_date) & (daily.symbol == sample.symbol))]
    updated = attach_targets(features, missing)
    assert updated[(updated.date == sample.date) & (updated.symbol == sample.symbol)].empty


def test_chronology_and_training_only_scaler(panels):
    daily, intraday = panels
    panel = attach_targets(prepare_features(build_factors(daily, intraday)), daily)
    train, validation, test = chronological_split(panel)
    assert train.execution_date.max() < validation.date.min()
    assert validation.execution_date.max() < test.date.min()
    predictions, tuning, _, model = fit_model(train, validation, test)
    np.testing.assert_allclose(model.named_steps["standardscaler"].mean_, train[FEATURES].mean())
    changed_test = test.copy()
    changed_test["target_return"] *= -100
    other, other_tuning, _, _ = fit_model(train, validation, changed_test)
    np.testing.assert_allclose(predictions.score, other.score)
    pd.testing.assert_frame_equal(tuning, other_tuning)


def test_portfolio_round_trip_costs_and_initial_drawdown():
    p = pd.DataFrame({"date": [pd.Timestamp("2024-01-01")] * 10, "execution_date": [pd.Timestamp("2024-01-02")] * 10, "symbol": list("abcdefghij"), "score": range(10), "target_return": [0.0] * 10})
    daily, holdings = simulate_portfolio(p, cost_bps=10)
    assert holdings.weight.sum() == pytest.approx(0)
    assert holdings.weight.abs().sum() == pytest.approx(1)
    assert daily.turnover.iloc[0] == pytest.approx(2)
    assert daily.net_return.iloc[0] == pytest.approx(-0.002)
    assert portfolio_metrics(daily)["max_net_drawdown"] == pytest.approx(-0.002)
    with pytest.raises(ValueError):
        simulate_portfolio(p, cost_bps=-1)


def test_end_to_end_outputs(tmp_path):
    result = run_demo(tmp_path, seed=3, days=100, symbols=20)
    assert result["test_sessions"] > 0
    assert (tmp_path / "overview.png").stat().st_size > 1000
    assert "Synthetic demonstration only" in (tmp_path / "demo_report.html").read_text()
    assert (tmp_path / "summary.json").exists()
    assert set(FEATURES) <= set(pd.read_csv(tmp_path / "raw_factors.csv").columns)
