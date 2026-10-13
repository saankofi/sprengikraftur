# Run 2: a second feature on the receipt scanner (2026-10-12)

The first test of the bundle on an existing project. It used the skills as changed after [run 1](2026-10-11-receipt-scanner.md).

**Brief, given as a plain message with no skill named:** "Staff need to fix misread receipts: edit any field and line item, and delete a receipt. Also make sure other websites can't trigger paid scans."

## Result

- **`plan-feature` loaded by itself.** It then chained into `drive-feature` in the same session.
- **One batch of questions.**
  - It asked two: permanent vs recoverable delete, and overwrite vs full edit history. Both had a recommended default.
  - The owner picked full edit history, against the recommendation.
- **Slices built one after another,** with the reason stated: all three change the same API router and detail view.
- **Shipped:** 3 slices, 4 PRs (the last one updates the docs), CI green.
- **Checks:** 151 Rust tests and 72 frontend tests, all checks clean.
- **Migrations treated with care:** they were tested against a database holding real MVP rows. Now that real data exists, that's the right call.
- **Cost:** $32 for 602 calls. It took 99 minutes for about 5.7k changed lines.

## What went wrong

- **The report was wrong about the reviewer again.**
  - The reviews ran on GPT and the builders on Opus, yet the report said the reviewer "didn't run on @slow".
  - omp's `task` has had a per-call `model` selector since 18.5, so the skill can ask for the model directly.
  - In this setup, the two models differed only because the session model wasn't the default role.
- **Drift from before the feature survived.** PRODUCT.md still had two conflicting bare-`$` rules, and an ADR still described the old fake parser. The finish check only compared *new* ADRs with older ones.
- **It edited the body of an accepted ADR.** On two other ADRs it added an "amended by" note to the status line, which was reasonable.
- **It worked around commit signing.** When signing failed, it pushed unsigned commits over HTTPS. It said so, but it should have stopped.

## Changes made afterwards

- **Config:**
  - removed `pinned_high`: `plan-feature` triage names money, auth and deleting data, and `build-slice` relies on "the cost of being wrong";
  - removed `reviewer_model`: omp's `slow` role is the setting now;
  - renamed `gates` to `approve`, with `approve: [pr]` as the default.
- **`drive-feature`:**
  - slices merge into a `feature/NNNN` branch, and one PR into `main` waits for the human;
  - the finish check also fixes drift that predates the feature.
- **`build-slice`:**
  - starts the reviewer with `model: "@slow"`;
  - doesn't work around security controls.
- **`adr`:** an accepted ADR's status line may change, its body may not.
- **README:** how to set up omp's model roles.
