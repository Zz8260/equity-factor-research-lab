# Portfolio Case Study

## Problem

An exploratory equity-factor archive is difficult for an external reviewer to assess when it relies on private data interfaces, repeated scripts and absent datasets. A credible portfolio needs a coherent, runnable example with explicit timing and a clear boundary around what can be verified.

## Research coverage in the archive

The inspected material covers factor construction across daily fundamentals, prices, intraday returns, trades and order books. It also explores industry/size processing, correlation, label preparation and linear or tree-based models. This establishes the thematic basis for the portfolio reconstruction; individual authorship and empirical outcomes are not inferred.

## Deliverables of this reconstruction

- An English project narrative and source-theme inventory.
- Eight standalone representative factor implementations.
- Deterministic synthetic daily and sampled intraday data.
- Date-local preprocessing and forward return alignment.
- Chronological partitions with boundary-label purging and train-only scaling.
- Validation-selected Ridge scoring, with a fixed test-period evaluation.
- Gross/net intraday portfolio diagnostics with two-sided transaction costs.
- A portable report, numerical outputs, tests and CI configuration.

## Engineering decisions worth discussing

**Availability before prediction.** Signals are computed at the close and executed the following session. The realized overnight gap is never counted as return earned by a next-open entry.

**A reproducible subset.** Eight signals were reconstructed instead of claiming every exploratory variant was portable. Private adapters and the original source archive are excluded.

**Inspectable modeling.** Ridge provides a compact coefficient-based example; alpha selection and coefficient exports expose what the model learned. Logistic, Lasso and tree experiments remain archive themes rather than unsupported runnable features.

**Costs as part of the result.** The daily round trip incurs both entry and exit costs. A negative net curve remains in the report.

## Presentation language

Suggested factual description of this repository:

> Equity Factor Research Lab is a reproducible Python demonstration of equity signal engineering, chronological model validation and transaction-cost-aware diagnostics. It reconstructs eight representative signals from the themes of a 77-script research archive and evaluates the workflow on deterministic synthetic data.

Suggested explanation of the evidence boundary:

> The included numbers are synthetic workflow outputs. Original market-data backtests were not provided, so I do not use this repository to claim a historical alpha or employer investment result.

The owner should add verified role, dates, individual responsibilities and approved real-world outcomes separately if available. Those details are deliberately not fabricated here.
