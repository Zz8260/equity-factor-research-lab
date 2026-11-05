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

The GitHub Actions workflow is configured for Python 3.10 and 3.12. A local pass does not imply that both hosted jobs have run; consult the Actions page for actual hosted status. The exact local package versions are recorded in `requirements-lock.txt` and `reports/summary.json`.
