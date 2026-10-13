# Run 3: CSV export and a currency rule (2026-10-13)

The first run with the simplified config (`approve: [pr]`, omp's `slow` role set to GPT, Opus building).

**Brief:** "The accountant needs a CSV export of transactions for a date range. Also, owner decision: a bare $ on a Hong Kong receipt counts as HKD."

## Result

- **Two questions, both good.**
  - What one CSV row should be.
  - How far the `$` decision goes: scans only, which was already true, or the stored rule everywhere.
- **The feature-branch flow worked.**
  - Two slices were built one after another and merged into `feature/0003-csv-export`.
  - One PR into `main` (#20) waits for the human, with CI green.
- **Drift inside the feature's scope was fixed.**
  - The two conflicting bare-`$` rules in PRODUCT.md now agree.
  - ADR 0013 supersedes part of ADR 0007, and 0007's change was to its status line only.
  - Stale status lines in ARCHITECTURE.md and BUSINESS.md were updated.
- **No leftover todo reminder at the end.**
- **Cost:** $7.22 for 232 calls, in about 30 minutes, for about 1.3k changed lines.

## What went wrong

- **The report was wrong about the reviewer a third time.** omp started the reviewer on the `slow` role (GPT) by default, yet the report said both reviews ran on the default model. Telling the builder to pass `model: "@slow"` made it look for a setting it couldn't find, and then report that the setting was missing.
- **Two unrelated changes became one feature.** Triage was written as if every request is a single change.
- **Drift outside the feature survived.** ADR 0006 still says the offline fake uses the real parser, and it doesn't. Nothing in this feature touched that area, so finding it is `living-docs`' job, not `drive-feature`'s.

## Changes made afterwards

- **`build-slice`:** names omp's `reviewer` agent and notes that it runs on the `slow` role. There's no setting left for the builder to look for.
- **`plan-feature`:** a request may hold several unrelated changes, and each gets triaged and planned on its own.

## Afterwards: `living-docs` with no input ($4.09)

- **A small, accurate PR (+28/−25 lines).** It corrected real errors, removed history from the status lines, and added a few trivia lines.
- **It missed the ADR 0006 drift, because the skill never mentioned ADRs.** Fix: `living-docs` now checks accepted ADRs against the code.
- **This led to the pipeline change.**
  - `drive-feature` runs `living-docs` on the feature branch before the PR into `main`, so merging is the last step.
  - Every stop says what to do and what happens after.
  - `approve: [pr]` was renamed to `approve: [merge]`.
