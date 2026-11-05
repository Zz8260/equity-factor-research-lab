"""Source-qualified factor definitions with explicit execution availability."""

import csv
from importlib.resources import files

STATUSES = ("demo", "archive", "commented", "reference")


class FactorUnavailableError(ValueError):
    """An inspected research definition has no executable public adapter."""


def load_catalog():
    with files("factorlab").joinpath("factor_catalog.csv").open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def get_factor(factor_id):
    for row in load_catalog():
        if row["factor_id"] == factor_id:
            return row
    raise KeyError(f"Unknown factor: {factor_id}")


def compute_factor(factor_id, daily, intraday):
    """Calculate a demo factor; never substitute a proxy for an archive output."""
    row = get_factor(factor_id)
    if row["status"] != "demo":
        raise FactorUnavailableError(
            f"{factor_id} is {row['status']}, not executable in this public package. "
            f"Requires: {row['required_data']} "
            "An authorized dataset and a reviewed implementation/adapter are required."
        )
    from .factors import FEATURES, build_factors
    if factor_id not in FEATURES:
        raise ValueError(f"Executable catalog entry has no implementation: {factor_id}")
    return build_factors(daily, intraday)[["date", "symbol", factor_id]]
