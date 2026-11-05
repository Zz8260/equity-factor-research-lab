"""Deterministic synthetic panels and explicit input validation."""

import numpy as np
import pandas as pd

DAILY_COLUMNS = ["date", "symbol", "open", "close", "turnover", "market_cap", "earnings", "book_equity", "roe", "industry"]
INTRADAY_COLUMNS = ["date", "symbol", "time", "close", "buy_volume", "sell_volume", "bid_depth", "ask_depth"]


def validate_panel(frame, intraday=False):
    required = INTRADAY_COLUMNS if intraday else DAILY_COLUMNS
    missing = set(required) - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    keys = ["date", "symbol", "time"] if intraday else ["date", "symbol"]
    if frame.empty or frame[keys].isna().any().any() or frame.duplicated(keys).any():
        raise ValueError("Input must be nonempty with unique, non-null observation keys.")
    numeric = [c for c in required if c not in {"date", "symbol", "time", "industry"}]
    if not np.isfinite(frame[numeric].to_numpy(dtype=float)).all():
        raise ValueError("Numeric observations must be finite.")
    positive = ["close"] if intraday else ["open", "close", "market_cap"]
    nonnegative = ["buy_volume", "sell_volume", "bid_depth", "ask_depth"] if intraday else ["turnover"]
    if (frame[positive] <= 0).any().any() or (frame[nonnegative] < 0).any().any():
        raise ValueError("Prices/capitalization must be positive; activity cannot be negative.")
    if not intraday and frame["industry"].isna().any():
        raise ValueError("Industry must be available for neutralization.")


def generate_synthetic(seed=42, days=260, symbols=60):
    """Create toy data. Latent structure is intentional and is not market evidence."""
    if days < 100 or symbols < 20:
        raise ValueError("Use at least 100 days and 20 symbols.")
    rng = np.random.default_rng(seed)
    names = [f"SYN{i:04d}" for i in range(symbols)]
    dates = pd.bdate_range("2023-01-02", periods=days)
    shares = rng.uniform(5e7, 5e8, symbols)
    quality = rng.normal(0, 1, symbols)
    earnings = shares * np.exp(quality * 0.3) * rng.uniform(0.5, 2, symbols)
    book = shares * rng.uniform(5, 15, symbols)
    price = rng.uniform(15, 70, symbols)
    records, ticks = [], []
    times = ["09:35", "10:00", "10:25", "10:50", "11:15", "11:30", "13:05", "13:30", "13:55", "14:20", "14:45", "15:00"]
    flow = rng.normal(0, 1, symbols)
    for date in dates:
        market = rng.normal(0, 0.006)
        open_price = price * np.exp(rng.normal(0, 0.004, symbols))
        # Yesterday's flow weakly influences today's toy return.
        intraday_return = np.clip(market + 0.0006 * quality + 0.001 * flow + rng.normal(0, 0.018, symbols), -0.12, 0.12)
        price = open_price * (1 + intraday_return)
        flow = 0.5 * flow + rng.normal(0, 0.8, symbols)
        turnover = rng.uniform(0.005, 0.06, symbols)
        for i, name in enumerate(names):
            records.append((date, name, open_price[i], price[i], turnover[i], shares[i] * price[i], earnings[i], book[i], 0.08 + quality[i] * 0.025, f"Industry{i % 5}"))
            steps = rng.normal(0, 0.001, len(times))
            path = open_price[i] * np.exp(np.cumsum(steps))
            path *= np.exp(np.linspace(0, np.log(price[i] / path[-1]), len(times)))
            for time, close in zip(times, path):
                volume = rng.uniform(500, 5000)
                imbalance = np.tanh(flow[i] * 0.4 + rng.normal(0, 0.3))
                depth = rng.uniform(2000, 10000)
                book_imbalance = np.tanh(flow[i] * 0.3 + rng.normal(0, 0.4))
                ticks.append((date, name, time, close, volume * (1 + imbalance) / 2, volume * (1 - imbalance) / 2, depth * (1 + book_imbalance), depth * (1 - book_imbalance)))
    daily = pd.DataFrame(records, columns=DAILY_COLUMNS)
    intraday = pd.DataFrame(ticks, columns=INTRADAY_COLUMNS)
    validate_panel(daily)
    validate_panel(intraday, intraday=True)
    return daily, intraday
