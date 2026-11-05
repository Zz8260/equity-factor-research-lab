# Research Protocol

## Scope and evidence

The supplied archive contains 77 research scripts: 65 factor scripts returning 110 source-qualified outputs and 12 assembly/modeling utilities. The public catalog also preserves 26 named commented alternatives and an undefined external panel dependency. The eight executable factors are newly written synthetic reconstructions; source-qualified archive entries are metadata, not executable private-platform ports. Counts include repeated names, parameter variants and auxiliary regression outputs.

Original source, credentials, internal adapters, vendor data and bundled environment files are excluded. Original source hashes/byte sizes remain in `source_inventory.csv`; the Chinese filename correspondence stays outside this English repository. The archive alone establishes neither authorship nor investment performance. Use verified personal contributions when presenting the project. Packaging, documentation and reconstructed code were prepared with AI assistance.

## Data contract

The CLI generates data in memory. An authorized real-data adapter must provide pandas DataFrames with these fields:

| Panel | Unique key | Required fields |
| --- | --- | --- |
| Daily | date, symbol | open, close, turnover, market_cap, earnings, book_equity, roe, industry |
| Sampled intraday | date, symbol, time | close, buy_volume, sell_volume, bid_depth, ask_depth |

Dates must share exchange-session and timezone conventions. Prices are positive and consistently adjusted; capitalization and accounting values use matching currencies; turnover and ROE are fractions. Activity/depth is nonnegative. Every daily observation key must have intraday observations and vice versa; at least two correctly ordered intraday samples are needed for volatility. The built-in validator checks columns, duplicate/null keys, finite numbers, positive prices/capitalization, nonnegative activity and non-null industry.

Real inputs additionally need publication-timestamped fundamentals, historical industry/security masters, delisted instruments, corporate actions, complete exchange calendars, session continuity and feed-quality checks. These checks are not supplied by the basic validator. Original archive families need richer schemas, listed in the factor registry. A CSV ingestion CLI and private-platform compatibility layer are not implemented.

## Feature and target timing

1. Sort observations by symbol/date/time. Construct the eight factors from data available by close t; the reversal requires 20 valid historical returns.
2. Within each date, remove incomplete observations and require at least ten securities. Clip each feature to the 1st/99th cross-sectional percentiles.
3. Regress on an intercept, log market capitalization and industry dummies. Rank the residuals within the date and subtract 0.5.
4. Attach next-session return `close[t+1]/open[t+1]-1`. A security missing from the next observed market date is excluded instead of silently jumping to a later date.

This avoids crediting an overnight return to a next-open entry. If an entire market session is absent from the dataset, the observed calendar cannot detect it: a real adapter must enforce calendar completeness. Final rank transformation can reintroduce size/industry exposure; final portfolios are not guaranteed neutral.

## Model validation

Split unique signal dates chronologically, approximately 60% training / 20% validation / 20% testing. Purge training/validation observations whose label realization reaches the next partition. No random row split is used.

The training target is the within-date percentile rank of next-session returns minus 0.5. StandardScaler and Ridge fit training observations only. Choose alpha from 0.1, 1, 10 and 100 by validation mean daily rank IC (Spearman correlation). Keep the selected training-only fit fixed when scoring test observations. Test labels are used only for evaluation. A model score is a ranking signal, not a forecast return percentage.

There is one holdout, not a walk-forward experiment. Repeated strategy changes after inspecting test outcomes need a fresh holdout and an experiment ledger. No confidence interval, multiple-testing correction or real-market significance claim is supplied.

## Portfolio abstraction and costs

Each session, equal-weight the top 20% to +0.5 and the bottom 20% to -0.5; break score ties by symbol. Enter at the next open, close to cash at that session's close. Gross exposure is 1.0, net exposure zero and round-trip turnover 2.0. Cost equals turnover * one_way_bps / 10000. At 10 bps one-way, daily portfolio cost is 20 bps; this is an illustrative assumption rather than a calibrated estimate.

Gross return is sum(weight * open-to-close return); net return subtracts costs. Compound equity from initial capital 1. Maximum drawdown includes that initial observation. Sample-standard-deviation volatility and zero-risk-free-rate Sharpe use 252 sessions; undefined Sharpe is null. The exported equal-weight universe return is contextual, not a matched-risk benchmark.

A-share T+1, short-sale eligibility, borrow/financing, suspensions, price limits, queueing, slippage and capacity are not modeled; the daily long/short round trip can be infeasible. Real-data point-in-time accuracy and execution realism remain necessary before any deployability claim.

## Reproduction and outputs

Default synthetic settings: seed 42, 260 weekday dates, 60 fictional securities and 12 sampled prices per security/day. Weekdays do not model exchange holidays. Static synthetic accounting attributes and lagged latent flow deliberately introduce return structure; it is not market evidence.

The saved run has 48 test sessions: gross return +3.31%, net return -6.15%, maximum net drawdown -7.09%, and model mean rank IC 0.01945. Ridge alpha is 100. The negative net result is retained.

`reports/summary.json` records exact split boundaries, settings and package versions; `requirements-lock.txt` records the local numerical environment. Floating-point near ties can vary by backend. Each demo regenerates these local details:

| Generated CSV | Purpose |
| --- | --- |
| raw_factors | Eight raw factor exposures, including warmup missing values |
| processed_panel | Ranked/residualized features and aligned return labels |
| validation_scores | Validation rank IC for each alpha |
| model_coefficients | Coefficients on training-scaled features; not a complete serialized model |
| test_predictions | Test-period scores and realized labels |
| positions | Security-level weights, including zero positions |
| daily_returns | Gross/net returns, costs, turnover and equity |
| factor_diagnostics | Test-period mean daily rank IC for each individual feature |

Only HTML, overview PNG and JSON summary are tracked; CSV details remain local and can be regenerated. The report embeds its image and can be opened as a standalone file. Modifying experiments overwrites the selected output directory; use `--output` for separate runs.

## Verification and review

The numerical research tests cover deterministic data, input validity, residual orthogonality, invariance of historical features to future observations, target alignment, missing-security sessions, boundary purging, train-only scaling, test-label isolation, two-sided costs, initial-capital drawdown and report generation.

Catalog checks verify all 110 declared source outputs and 26 commented alternatives exactly once, resolve source IDs, retain the eight numerical implementations, and reject unavailable computations rather than filling values or substituting proxies. CLI filters and unknown IDs are checked. The package includes its registry for installed use.

GitHub Actions runs tests and a smaller demo on Python 3.10 and 3.12. [The original implementation checks passed](https://github.com/Zz8260/equity-factor-research-lab/actions/runs/42000066303); see [Actions](https://github.com/Zz8260/equity-factor-research-lab/actions) for current revision status. Passing tests validates these checks, not the existence of real-market alpha.

For a five-minute review, spend one minute on the research map, one on two factor definitions and their data blockers, one on temporal validation, one on gross versus net results, and one on the limitations and verified personal contribution. Be ready to explain why IC can be positive while returns after costs are negative, and why residualized features do not guarantee a neutral portfolio.

## Next experiments

- Build an authorized point-in-time adapter with publication timestamps, delisting-aware universes, corporate actions and exchange calendars.
- Port selected archive definitions only after resolving their formula, threshold and event-timing questions. Extend order survival, cancellation and nonlinear path families without inventing absent external-panel definitions.
- Add purged walk-forward folds, uncertainty estimates and a trial ledger; compare logistic, Lasso and tree baselines under the same protocol.
- Replace the portfolio abstraction with T+1-aware holdings, short eligibility, calibrated financing/execution costs and capacity constraints.

Use synthetic fixtures for changes, run tests and a demo, and document availability timing and acceptance criteria. Keep user-facing text in English and private data outside the repository.
