---
name: drive-feature
description: Build a planned feature end to end by running build-slice for each of its slices, then report back once. Use when a feature doc with slices exists and the human wants it built, either whole or one slice at a time.
---

# drive-feature

Get a whole feature built while the human is away, then hand back one clear report.

Don't build slices yourself: each one runs as `build-slice` in its own subagent.

## How to work

- Read the feature doc and `AGENTS.md`. Set the feature's status to `building`.
- Work on a branch `feature/NNNN-short-slug` from `main`. Each slice's PR targets it and is merged once review and CI pass.
- Build each slice with `build-slice`, in dependency order, each in its own `task` subagent. Keep your own context small: take back only each slice's report, never its diffs.
- Build slices one after another by default. Run them in parallel (isolated worktrees) only when they change different parts of the code; if two slices touch the same screen, table, module or rule, build them in sequence.
- If `mode: ticket`, build one slice (its PR targets `main`) and stop.
- Stop for the human only at a step listed in `approve`, or when a question blocks the work. When you stop, say exactly what to do, what to check, and what happens after ("reply `go` and I'll …", or "nothing: merging finishes it"). Otherwise keep going: park the blocked slice and carry on with the others.

## Finish

- Check that the docs describe what actually shipped: PRODUCT, ARCHITECTURE, ADRs, the feature doc. Fix any drift you find in them, including drift from before this feature. Check new ADRs against older ones; supersede any they contradict. Where docs conflict on a product rule, say which rule the code follows today, and flag it. Then run `living-docs` on the feature branch. Set the status to `shipped`.
- Open one PR from the feature branch into `main`, with the report as its description and the checks only a human can do (real devices, real files) as a checklist. If `approve` includes `merge`, leave the merge to the human; otherwise merge it once CI passes.
- Hand back one report:
  - what shipped, with links
  - the combined decision ledger
  - anything flagged or parked
  - what needs human review, most important first
  - last, the stop: what the human does now, and what happens after
