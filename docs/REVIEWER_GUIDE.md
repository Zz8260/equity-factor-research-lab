# Five-Minute Reviewer Walkthrough

## Minute 1: Explain the problem and scope

Open the README. Explain that the project turns a platform-dependent exploratory archive into a portable research demonstration. Identify the eight implemented signals and explain that the 77-script count includes variants and utilities.

## Minute 2: Demonstrate reproducibility

Run `factorlab demo --output /tmp/factorlab-review` and open the generated HTML report. Explain the seed, fictional securities and intentionally embedded synthetic structure. Show `summary.json` to inspect exact split dates, selected alpha and package versions.

## Minute 3: Explain how future information is controlled

Open `src/factorlab/factors.py` and `src/factorlab/evaluation.py`. Walk through the close-t signal, next-session open-to-close target, boundary-label purge and training-only scaler. Show the test that recomputes historical features after truncating future data.

## Minute 4: Interpret the result

Compare gross and net equity curves. Explain why a 1.0 gross intraday exposure generates 2.0 round-trip turnover and 20 bps of daily cost at a 10 bps one-way assumption. State whether the included run loses money after costs. Inspect coefficients and mean daily rank IC without treating synthetic results as market evidence.

## Minute 5: Discuss realistic next steps

Use the roadmap to discuss point-in-time fundamentals, delisting-aware universes, exchange calendars, walk-forward validation, A-share T+1 constraints, borrow eligibility and capacity. Distinguish the archived research themes from newly implemented engineering work.

## Questions to prepare for

- Why use chronological dates rather than random security-date rows?
- What is rank IC, and why can positive IC coexist with a loss after costs?
- Does residualizing features guarantee a neutral final portfolio?
- What assumptions make the intraday long/short example infeasible in A-shares?
- Which parts did you personally contribute to in the original research?
- What data and permissions would be required to verify real historical results?
