"""Audit the promised archive coverage and fail explicitly for unavailable factors."""

import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

from factorlab.catalog import FactorUnavailableError, compute_factor, get_factor, load_catalog
from factorlab.data import generate_synthetic
from factorlab.factors import FEATURES, build_factors


def test_all_declared_source_outputs_are_covered_once():
    rows = load_catalog()
    assert len({r["factor_id"] for r in rows}) == len(rows)
    assert Counter(r["status"] for r in rows) == {"demo": 8, "archive": 110, "commented": 26, "reference": 1}
    sources_path = Path(__file__).parents[1] / "docs" / "source_inventory.csv"
    with sources_path.open(newline="") as stream:
        sources = list(csv.DictReader(stream))
    assert len(sources) == 77
    assert Counter(s["role"] for s in sources) == {"factor": 65, "pipeline": 12}
    for status, column in [("archive", "returned_outputs"), ("commented", "commented_outputs")]:
        expected = {(s["source_id"], name) for s in sources for name in s[column].split(";") if name}
        actual = [(r["source_id"], r["source_output"]) for r in rows if r["status"] == status]
        assert len(actual) == len(set(actual))
        assert set(actual) == expected
    assert {r["factor_id"] for r in rows if r["status"] == "demo"} == set(FEATURES)
    source_ids = {s["source_id"] for s in sources}
    for row in rows:
        assert set(row["source_id"].split(";")) <= source_ids
        assert all(row[key] for key in ["definition", "required_data", "available_after", "review_note"])


def test_unavailable_factors_never_silently_return_proxies():
    for row in load_catalog():
        if row["status"] != "demo":
            with pytest.raises(FactorUnavailableError, match="not executable"):
                compute_factor(row["factor_id"], None, None)
    with pytest.raises(KeyError, match="Unknown factor"):
        get_factor("nonexistent")
    assert "one minute" in get_factor("S076.hifeq_1s")["review_note"]
    assert "r>0" in get_factor("S040.std_ngt")["review_note"]


def test_executable_catalog_preserves_original_factor_values():
    import pandas as pd
    daily, intraday = generate_synthetic(seed=11, days=100, symbols=20)
    expected = build_factors(daily, intraday)
    for feature in FEATURES:
        pd.testing.assert_frame_equal(compute_factor(feature, daily, intraday), expected[["date", "symbol", feature]])


def test_catalog_cli_filters_and_unknown_id():
    result = subprocess.run([sys.executable, "-m", "factorlab.cli", "catalog", "--status", "archive", "--family", "order_lifetime", "--json"], capture_output=True, text=True, check=True)
    rows = json.loads(result.stdout)
    assert len(rows) == 10
    assert all(r["family"] == "order_lifetime" and r["status"] == "archive" for r in rows)
    bad = subprocess.run([sys.executable, "-m", "factorlab.cli", "catalog", "--factor", "missing"], capture_output=True, text=True)
    assert bad.returncode != 0
    assert "No factor matches" in bad.stderr
