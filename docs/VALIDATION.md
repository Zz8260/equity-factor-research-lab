# Validation Record

Local validation completed on 2026-11-05 using Python 3.12.

- Editable installation from `pyproject.toml` completed successfully.
- `python -m pytest -q`: **7 tests passed**.
- The default `factorlab demo` completed with seed 42, 260 business dates and 60 fictional securities.
- The generated chart was visually inspected for complete labels and readable curves.
- Exported text was checked for embedded credentials found in the local archive, internal data paths and Chinese text; none were present in the reviewed export.

The tests cover deterministic data, basic input checks, residual orthogonality, invariance of past features to future observations, next-session target alignment, missing-security sessions, chronological partition boundaries, training-only scaler statistics, test-label isolation, round-trip costs, initial-capital drawdown and report generation.

## Default synthetic result

| Measure | Value |
| --- | --- |
| Test sessions | 48 |
| Selected Ridge alpha | 100 |
| Mean model daily rank IC | 0.01945 |
| Gross cumulative return | 3.31% |
| Net cumulative return | -6.15% |
| Maximum net drawdown | -7.09% |
| One-way cost assumption | 10 basis points |
| Average entry-plus-exit turnover | 2.0 |

These are synthetic demonstration results. The negative net result illustrates how costs can dominate a weak scoring signal. It is not a result from the original archive or an employer portfolio.

The [hosted research checks](https://github.com/Zz8260/equity-factor-research-lab/actions/runs/42000066303) passed on Python 3.10 and 3.12 for implementation commit `ab2cfc3`. Both jobs installed the package, ran all tests and completed a smaller synthetic demo. Consult the Actions page for the status of later commits. The exact local package versions are recorded in `requirements-lock.txt` and `reports/summary.json`.
