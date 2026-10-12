# Run 1: receipt-scanner MVP (2026-10-11)

The first end-to-end test of the bundle on a new project.

**Setup:**
- **Brief:** an internal tool for a small Hong Kong business. Staff upload a receipt photo, a vision model extracts the transaction, and it's saved.
- **Stack (given):** Rust, SolidJS, SQLite, OpenRouter.
- **Answers:** reused from an earlier one-shot build of the same brief.
- **Models:** Opus built it; omp's `reviewer` agent reviewed it on GPT.
- **Config:** `risk: high`, no gates, `mode: feature`.

**Flow:** `living-docs`, then `plan-feature` (4 slices as GitHub issues), then `drive-feature`.

## Result

- **Shipped:** all 4 slices in 78 minutes, as 4 PRs with CI green. No questions mid-run.
- **Checks:** 106 Rust tests, 49 frontend tests and 2 Playwright end-to-end tests. Clippy, eslint, tsc and the formatters are all clean.
- **Blind review:** about 8/10 as a foundation for agents. The same rubric gave a Superpowers build about 7 and a one-shot build about 6.5.
- **Cost:** $38 in total, 95.7M cache-read tokens. The main session stayed small (2.6M); the four builders used the rest.
- **Honesty:** the report flagged the acceptance criteria that were only tested with stand-ins: a real photographed receipt, and real phones.

## What went wrong

- **Building slices in parallel produced conflicting rules.** One slice flagged a bare `$`; another told the model to read it as HKD. An older ADR was also left stale after a later slice changed the behaviour it described.
- **It over-built.** It added a backfill migration for data that didn't exist yet, and heavy paranoia code. "Risk sets the rigour" had no upper bound.
- **The docs were too long.** About 6.7k words and 9 ADRs. Implementation numbers leaked into PRODUCT.md.
- **The report guessed instead of checking.** It said the reviewer might be the same model as the builder. The session logs showed it was GPT, a different model.

## Changes made afterwards

- **`drive-feature`:**
  - Build slices one after another by default; run them in parallel only when they change different code.
  - The final check compares new ADRs with older ones.
- **`build-slice`:**
  - Rigour scales with the cost of being wrong.
  - Don't build compatibility for data or users that don't exist yet.
  - Docs stay short.
  - Report what was checked, not what's suspected.
- **`adr`:** only for decisions that are hard to reverse, and it checks for ADRs it contradicts.
- **`plan-feature`:** links to owner decisions instead of repeating them.
- **`living-docs`:** PRODUCT.md describes what users see.
