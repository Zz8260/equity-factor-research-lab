# Provenance and Disclosure Boundaries

## What was inspected

A user-supplied local ZIP archive contained 77 Python research scripts and two environment files from third-party packages. Non-UTF-8 filename metadata was decoded locally to identify the research themes. The original archive remains outside this repository.

The scripts reference private research interfaces, market tables and local parquet files. Some contain embedded authentication values. None of those authentication values, private adapters, source files, vendor data or environment files are included in this project. The credentials should be rotated by their owner through the corresponding service.

## What the repository contains

The published code is a newly written, standalone reconstruction of common research operations, with simplified factor definitions and synthetic observations. It is not a translated copy of the archive and is not an exact reproduction of its proprietary environment. Its report measures this demonstration only.

`source_inventory.csv` provides English labels, broad research families, source byte sizes and SHA-256 fingerprints for the 77 inspected scripts. The fingerprints support a local correspondence check; they do not validate authorship, formula correctness or performance. Local original filenames are excluded from the public catalog.

## Claims supported by the supplied material

- The archive contains exploratory implementations of valuation, reversal, intraday, order-flow, order-book, nonlinear adjustment and supervised-modeling research.
- The scripts include multiple parameter/transformation variants, joins, rank transforms and backtest configuration code.
- The standalone demonstration runs the documented pipeline and produces the included synthetic outputs.

## Claims not established

The archive alone does not establish personal authorship of every line, exclusive ownership, employer permission, actual performance, out-of-sample significance, deployment, assets managed, cost savings or business impact. References to 96 additional input factors do not establish that those factors are implemented or supplied in full. The source count must not be represented as the count of unique validated alpha factors.

## Attribution

The repository is maintained for Zz8260's technical portfolio. The packaging, English documentation, reconstructed code and synthetic demo were prepared with AI assistance. Before using first-person statements in applications, the owner should describe only their verified personal contributions and approved research scope. No employer branding, endorsement or proprietary performance is claimed.
