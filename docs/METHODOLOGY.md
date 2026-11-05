# Research Methodology

## 1. Establish the evidence boundary

The locally supplied archive contains 77 research scripts and two bundled third-party environment files. It contains no underlying price panel, verified backtest report, realized portfolio record or reproducible internal platform environment. The published implementation and all generated outputs are new demonstration artifacts.

## 2. Generate a controlled dataset

The simulator creates 60 fictional securities over 260 weekday dates by default, with 12 sampled intraday prices and volume/depth observations per security per day. Prices remain positive, identifiers start with `SYN`, and an explicit random seed controls every draw. Valuation, quality and lagged flow have deliberately embedded weak return structure. This makes the dataset useful for exercising the workflow, with no inference about market efficiency.

The weekday calendar does not model exchange holidays. Earnings, book equity and ROE are static synthetic attributes. With real fundamentals, a point-in-time join based on publication timestamps is mandatory; a financial period end is not its availability date.

## 3. Form signals at the close

Daily and intraday input keys must match. Data is sorted by symbol, date and, where applicable, time. The 20-day reversal requires 20 valid returns and therefore includes a warmup. Opening gaps use the preceding observed close. An adapter for real data must validate session continuity, corporate actions and timestamps before calling these functions.

Feature construction uses no forward observations. A test compares all past features with features recomputed on a truncated dataset. This verifies the included implementation under its stated input contract; it does not prove a future vendor adapter is free of leakage.

## 4. Process the cross-section

For each date and feature:

1. Remove incomplete observations; require at least 10 securities.
2. Clip values at the cross-sectional 1st and 99th percentiles.
3. Regress on an intercept, log market capitalization and industry dummy variables using least squares.
4. Retain residuals, then rank them within the date and subtract 0.5.

These steps use only the current date's observable universe. A real universe must also be point-in-time, including delisted securities. Final rank transformation can reintroduce industry or size exposure; exact residual orthogonality applies before ranking. Portfolio-level neutrality is not enforced.

## 5. Align the target with execution

For a signal dated t, the target is `close[t+1] / open[t+1] - 1`. Entries occur at the following session's open; exits occur at that session's close. This avoids attributing overnight returns to an investor who only entered at the next open. Rows with no next session are dropped. If a security is missing from the next date in the observed market calendar, its label is excluded rather than shifted to a later session.

An actual execution system must add signal publication delays, tradability checks and realistic fills. The demo assumes every selected instrument can be traded at both reference prices.

## 6. Separate learning and evaluation

Unique signal dates are split approximately 60% training, 20% validation and 20% testing. Training and validation observations are purged when their target realization date reaches the next partition. No random row split is used.

The training target is the cross-sectional percentile rank of next-session returns, centered at zero. For each Ridge alpha in `0.1, 1, 10, 100`, the scaler and model fit only training observations. Validation selects the highest mean daily rank IC. The selected training-only fit then scores test features; there is no fit on the combined training and validation sets. Test labels affect diagnostics only.

The demonstration uses one holdout split. Purged walk-forward evaluation, stability intervals and a policy for repeated research trials remain future work. Selecting further changes after seeing this test report would require a new untouched holdout for a valid empirical study.

## 7. Evaluate an explicit portfolio abstraction

Each test day, the lowest-scoring 20% receive equal weights totaling -0.5 and the highest-scoring 20% receive weights totaling +0.5. Ties are broken by symbol for determinism. Gross exposure is 1.0; net exposure is zero. Positions start and end in cash every day.

Gross return is the sum of weight times next-session open-to-close return. Entry plus exit turnover is 2.0 per day. Cost is `turnover * one_way_cost_bps / 10000`, so 10 bps one-way means a 20 bps daily portfolio cost. There is no assertion that 10 bps is empirically calibrated.

Equity compounds daily gross or net returns from initial capital 1. Maximum drawdown includes the initial capital observation. Annualized volatility and Sharpe use 252 sessions and sample standard deviation; Sharpe assumes a zero risk-free rate. Undefined Sharpe is recorded as null. The equal-weight universe return is an informational CSV series, not a matched-risk benchmark.

## 8. Preserve reproducibility and limitations

The report stores the seed, universe size, date count, selected alpha, partition boundaries and numerical package versions. The exact local environment is recorded in `requirements-lock.txt`; platform-specific wheels are resolved by pip. Small floating-point differences across numerical backends can affect near ties.

Real A-share portfolios require T+1 settlement-aware holdings, security-level short eligibility, price-limit and suspension filters, corporate-action adjustments, borrow/financing costs and capacity modeling. The included same-day round trip is an analytical illustration and can be infeasible in that market. No real-market performance or deployability claim follows from this demo.
