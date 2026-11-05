# Equity Factor Research Lab

**Equity signals from valuation to order-book behavior, with an auditable research inventory and an eight-factor runnable demo.**

[Factor library](docs/FACTORS.md) · [Research method](docs/RESEARCH.md) · [Project board](https://github.com/users/Zz8260/projects/2)

| Research scope | What is available |
| --- | --- |
| Runnable demonstration | **8 factors**, deterministic synthetic data, chronological Ridge validation and transaction-cost diagnostics |
| Original research coverage | **77 scripts: 65 factor scripts and 12 research utilities** |
| Factor inventory | **110 source-qualified returned outputs**, **26 commented alternatives**, and one externally referenced feature panel |
| Evidence | Inspectable definitions, source fingerprints, data requirements, availability timing and implementation review notes |

The archive count includes variants, repeated names and auxiliary outputs; it is not a count of independent validated alphas. The public implementation is a reconstruction. **All performance figures use synthetic data.** Original credentials, private source files and vendor data are excluded.

## Research map

| Family | Research question | Archive outputs | Public demo |
| --- | --- | ---: | --- |
| Valuation & profitability | Does price differ from accounting value or profitability? | 8 | Earnings yield, book to price, profitability residual |
| Return distribution | Does intraday dispersion or asymmetry contain information? | 6 | Sampled volatility |
| Price, volume & jumps | How do reversal, turnover and jump behavior interact? | 5 | 20-day reversal |
| Opening session | Does the opening gap or early price path contain information? | 6 | Opening gap |
| Trades & small orders | Does the direction or size of flow matter? | 26 | Trade imbalance |
| Order book | Does depth shape or pressure contain information? | 6 | Aggregate book imbalance |
| Order lifetime | Does order survival or cancellation speed matter? | 10 | Documented; event-level adapter needed |
| Nonlinear price adjustment | Do path shape, industry comparison or turnover residuals help? | 43 | Documented; source-specific recipes need porting |

The [factor library](docs/FACTORS.md) maps every returned output and named commented alternative to its source, definition and data needs. Related demo factors are explicitly labeled as simplified proxies. Missing inputs or implementation questions produce an availability error, never fabricated values.

## Eight executable factors

| Factor | Definition |
| --- | --- |
| `earnings_yield` | Earnings / market capitalization |
| `book_to_price` | Book equity / market capitalization |
| `profitability_residual` | Cross-sectional ROE residual versus earnings yield and an intercept |
| `reversal_20d` | Negative trailing 20-return turnover-weighted average simple return |
| `sampled_volatility` | Square root of within-day squared sampled returns |
| `trade_imbalance` | (Buy volume - sell volume) / total classified volume |
| `book_imbalance` | Mean normalized aggregate bid/ask depth imbalance |
| `opening_gap` | Current open / preceding session close - 1 |

## Run or inspect

Python 3.10 or later:

```bash
git clone https://github.com/Zz8260/equity-factor-research-lab.git
cd equity-factor-research-lab
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
factorlab demo
python -m pytest -q
```

Open `reports/demo_report.html`. Installation needs a package registry; the demo itself needs no network, API key or private dataset. Generated CSV details are written locally and ignored by Git.

```bash
factorlab catalog --status archive --family order_lifetime
factorlab catalog --factor S076.hifeq_1s
factorlab catalog --json
```

## What the demo tests

**Close-t features → next-session open-to-close labels → chronological 60/20/20 split → validation-selected Ridge → untouched test diagnostics.** Boundary-crossing labels are purged; scaling and model coefficients fit only training data. The portfolio allocates +0.5 to the highest-scoring 20% and -0.5 to the lowest-scoring 20%, returning to cash daily.

![Synthetic demonstration: gross/net equity and factor rank IC](reports/overview.png)

The saved synthetic run has 48 test sessions, mean model rank IC **0.01945**, gross return **+3.31%** and net return **-6.15%** at a 10 bps one-way cost assumption. Daily entry-plus-exit turnover is 2.0. Costs overwhelm the weak toy signal; the negative result is retained. See [experiment settings and metrics](reports/summary.json).

This demonstrates research mechanics, not real-market alpha. The intraday long/short abstraction does not implement A-share T+1 holdings, short eligibility, borrow, price limits or capacity. Full assumptions, source discrepancies and next steps are in the two documents below.

## Review in three steps

1. Read [FACTORS.md](docs/FACTORS.md): coverage, formulas, variants and data blockers.
2. Read [RESEARCH.md](docs/RESEARCH.md): timing, validation, costs, tests and limitations.
3. Inspect [factors.py](src/factorlab/factors.py), [evaluation.py](src/factorlab/evaluation.py) and [tests](tests), then run the demo.

The CLI, numerical modules and catalog live in `src/factorlab`; `reports` keeps only the portable report, chart and summary. The complete source audit is in [source_inventory.csv](docs/source_inventory.csv); the installable definition registry is [factor_catalog.csv](src/factorlab/factor_catalog.csv).

Prepared with AI assistance for Zz8260's technical portfolio. Describe personal contributions using verified facts. See [usage notice](USAGE_NOTICE.md).
