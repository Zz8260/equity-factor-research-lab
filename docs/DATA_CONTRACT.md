# Data Contract

The CLI generates synthetic inputs. To work with authorized external data, import `build_factors`, `prepare_features` and `attach_targets` from `factorlab.factors`, then pass pandas DataFrames matching this contract. A real-data CSV ingestion CLI is not included in version 1.0.

## Daily panel

Unique key: `(date, symbol)`. Use pandas datetime values normalized to the same exchange session date.

| Column | Meaning |
| --- | --- |
| `date` | Exchange session date |
| `symbol` | Stable security identifier |
| `open`, `close` | Positive, consistently adjusted prices in the same currency |
| `turnover` | Nonnegative daily turnover ratio, expressed as a fraction |
| `market_cap` | Positive capitalization in currency units |
| `earnings` | Point-in-time earnings in the same currency units |
| `book_equity` | Point-in-time book equity in the same currency units |
| `roe` | Point-in-time return on equity as a fraction |
| `industry` | Non-null industry category available on that date |

## Sampled intraday panel

Unique key: `(date, symbol, time)`. Every daily key must have intraday observations and vice versa. Sortable `HH:MM` time strings are used in the simulator. External adapters must enforce exchange timezone, session bounds, strict ordering and at least two samples for volatility.

| Column | Meaning |
| --- | --- |
| `date`, `symbol` | Join keys with the daily panel |
| `time` | Observation time within the exchange session |
| `close` | Positive sampled price |
| `buy_volume`, `sell_volume` | Nonnegative classified trade volumes in matching units |
| `bid_depth`, `ask_depth` | Nonnegative aggregate depth in matching units |

## Adapter responsibilities

The included validator rejects missing fields, duplicate or null keys, non-finite numeric fields, nonpositive prices/capitalization and negative activity. It does not validate financial publication dates, security master history, adjusted-price methodology, corporate actions, exchange calendars or feed completeness. Those checks belong in a documented adapter before real-data use.

Targets use the next observed market session, and are excluded if a symbol is absent on that date. Inputs should use a complete market-session calendar; if an entire market day is absent from the supplied panel, that gap cannot be detected from the observations alone.

## Generated output files

| Output | Contents |
| --- | --- |
| `raw_factors.csv` | Unprocessed daily factor exposures, including warmup missing values |
| `processed_panel.csv` | Ranked/residualized features and aligned labels |
| `validation_scores.csv` | Validation mean rank IC for every Ridge alpha |
| `model_coefficients.csv` | Selected model coefficients on training-scaled features |
| `test_predictions.csv` | Untouched test features, scores and realized labels |
| `positions.csv` | Symbol-level weights and returns for every test session |
| `daily_returns.csv` | Gross/net returns, round-trip turnover, costs and equity |
| `factor_diagnostics.csv` | Per-feature mean daily rank IC on test dates |
| `summary.json` | Metrics, settings, split dates and package versions |
| `overview.png`, `demo_report.html` | Portable visual review artifacts |
