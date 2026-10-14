# Run 4: cheap models, TypeScript, medium risk (2026-10-14)

A stress test of "assumes a strong model".

**Setup:**
- **Brief:** the same as run 1, but with TypeScript, Node, React and SQLite as the stack.
- **Config:** `risk: medium`.
- **Models:** Kimi K2.7 Code as the builder (`default`) and GLM 5.3 as the reviewer (`slow`), both through OpenRouter.
- **No GitHub remote.**

## Attempt 1

`/living-docs` with the brief was the only prompt. Kimi:

- **Never left `living-docs`.** It went on to write a feature plan, scaffold the project and start building, all inside that skill.
- **Loaded no other skill and started no subagents.** It used its own habits, not the bundle's process.
- **Asked nothing.** It decided the fields itself (only date, merchant and amount), treated everything as HKD with no flag for other currencies, and invented "staff can review and correct later".
- **Read money through a float.** It asked the model for `"amount": 123.45` and computed `Math.round(parseFloat(...) * 100)`. Storage is integer cents. At medium risk, "the cost of being wrong" alone didn't make it careful.
- **Planned the build horizontally:** schema, backend, frontend, then "wire it up". It wrote no acceptance tests first and made no feature branch.

It was stopped mid-build. The work is kept on the `attempt-1-kimi` branch of the local repo.

## Changes made afterwards

- **Each skill now opens with one line saying what it does and doesn't do:**
  - `living-docs` only writes docs, then says what comes next;
  - `plan-feature` writes no code;
  - `build-slice` builds only its slice;
  - `drive-feature` never builds slices itself;
  - `adr` only records the decision.

## Attempt 2

Same setup, with the boundary lines.
