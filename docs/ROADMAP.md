# Project Roadmap

## Completed in version 1.0

- [x] Inspect and catalog the 77-script source archive locally.
- [x] Define disclosure boundaries and exclude original credentials/adapters.
- [x] Reconstruct eight representative factors with standard Python libraries.
- [x] Add deterministic synthetic data and input validation.
- [x] Implement chronological partitions, boundary-label purging and train-only scaling.
- [x] Select Ridge alpha on validation rank IC and evaluate a fixed test partition.
- [x] Export costs, returns, positions, diagnostics and a portable English report.
- [x] Test timing, transformations, costs and the end-to-end workflow.
- [x] Provide CI configuration and reviewer documentation.

## Next research milestones

- [ ] Build an authorized point-in-time data adapter with publication timestamps, corporate actions and complete exchange calendars.
- [ ] Add purged walk-forward evaluation, confidence intervals and a ledger for repeated experiments.
- [ ] Replace the intraday portfolio abstraction with holdings that respect T+1, short eligibility, price limits and suspensions.
- [ ] Model borrow, financing, slippage, liquidity and capacity from measured inputs.
- [ ] Extend selected order-survival, cancellation and nonlinear price-adjustment themes where data rights permit.
- [ ] Compare Lasso, logistic and tree baselines under exactly the same temporal protocol.

Each open milestone needs an inspectable acceptance criterion before implementation. Completion refers to the standalone demonstration; it does not imply completion of the original private research program.
