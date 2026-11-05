# Contributing

Discuss proposed changes in an issue before introducing new data dependencies or research claims. Use synthetic fixtures for tests. Do not submit private data, credentials or employer source files.

Run `python -m pytest -q` and `factorlab demo --output /tmp/factorlab-check` before opening a pull request. Explain the hypothesis, availability timing, validation protocol and effect on output artifacts. Changes to signals or model selection should be evaluated on a new untouched holdout in any real empirical study.

Keep user-facing text in English and update methodology when assumptions change. Check the usage notice before redistributing this repository.
