# Factor Catalog

## Executable demonstration

| Feature | Formula / convention | Timing | Difference from the archive |
| --- | --- | --- | --- |
| `earnings_yield` | earnings / market_cap | Close t | Synthetic earnings; no vendor financial table |
| `book_to_price` | book_equity / market_cap | Close t | Synthetic book equity |
| `profitability_residual` | ROE - fitted ROE from intercept + earnings yield | Close t | Daily cross-sectional fit; archive also explores 300-day per-security regressions |
| `reversal_20d` | -sum(turnover * close_return) / sum(turnover), trailing 20 returns | Close t | Normalized return convention instead of the archive's unnormalized gross-price-ratio sum |
| `sampled_volatility` | sqrt(sum(sample_return squared)), within-day sampled close changes | Close t | Twelve intraday samples; first sample has no prior intraday return and is excluded |
| `trade_imbalance` | (sum buy_volume - sum sell_volume) / total volume | Close t | Classified synthetic flow, no exchange trade flags |
| `book_imbalance` | mean((bid_depth - ask_depth) / (bid_depth + ask_depth)) | Close t | Aggregated depth, no full ten-level reconstruction |
| `opening_gap` | open[t] / close[t-1] - 1 | Open t; used after close t | Plain signed gap, without nonlinear early-session combinations |

Zero denominators become missing values and are excluded by the processing step. Signals have fixed definitions; no sign is chosen using the test set. Ridge learns coefficient signs from training data.

## Additional archive themes

The English [source inventory](source_inventory.csv) indexes all 77 scripts, including parameter and transformation variants. It records script-level evidence rather than a claim of 77 distinct factors. It includes:

- Positive/negative intraday volatility, skewness and cumulative-return variants.
- Early-session windows from 5 to 29 minutes.
- Small-order volume/amount imbalance and ranking variants.
- Order-book skewness, depth distribution and pressure.
- Cancellation and order-survival behavior at several durations.
- Nonlinear price adjustment with quantile, cubic and arctangent variants.
- Industry variants and turnover-related orthogonalization.
- Correlation diagnostics, feature assembly, label assembly, OLS, logistic regression, Lasso, Ridge and decision trees.

These themes are documented as inspected research coverage. Their exact private-platform implementations are excluded; they are not claimed as executable or empirically validated here.
