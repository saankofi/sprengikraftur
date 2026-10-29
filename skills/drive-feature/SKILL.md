---
name: drive-feature
description: Build a planned feature end to end by running build-slice for each of its slices, then report back once. Use when a feature doc with slices exists and the human wants it built.
---

# drive-feature

Get a whole feature built while the human is away, then hand back one clear report.

Don't build slices yourself: each one runs as `build-slice` in its own subagent.

`docs/` here means the folder set by `docs` in `AGENTS.md` (default `docs`).

## How to work

- Read the feature doc and `AGENTS.md`. Set the feature's status to `building`. Slices already ticked off in the feature doc are done; skip them.
- Work on a branch `feature/NNNN-short-slug` from `main`. Each slice's PR targets it and is merged once review and CI pass.
- Build each slice with `build-slice`, in dependency order, each in its own `task` subagent. Keep your own context small: take back only each slice's report, never its diffs. If a slice's subagent dies, resume it or start a new one from where it stopped; don't finish the slice yourself.
- By default, build in parallel the slices the feature doc marks as buildable together, each in an isolated worktree. If the doc doesn't mark them, build slices one after another, and in parallel only when they change different parts of the code; if two touch the same screen, table, module or rule, build them in sequence.
- If the human gives a limit ("build 3 slices", "at most 2 at once", "one at a time"), keep to it. After that many slices, stop as for `slice` below, and on `go` carry on with the next batch.
- If `approve` includes `slice`, stop after each slice is merged into the feature branch so the human can try it: how to run it, what to try (its acceptance criteria), and the checks only a human can do. On `go`, start the next slice; if they report a problem, fix it first.
- Stop for the human only at a step listed in `approve` (read it from `AGENTS.md` when you get there; the human may have changed it), or when a question blocks the work. When you stop, say exactly what to do, what to check, and what happens after ("reply `go` and I'll …"). Otherwise keep going: park the blocked slice and carry on with the others.

## Finish

- Check that the docs describe what actually shipped: PRODUCT, ARCHITECTURE, ADRs, the feature doc. Fix any drift you find in them, including drift from before this feature. Check new ADRs against older ones; supersede any they contradict. Where docs conflict on a product rule, say which rule the code follows today, and flag it.
- Then run the `living-docs` skill on the feature branch, even if the docs look current. (If the slices were merged into `main` one by one, do the finish on a short branch from `main`.) Set the status to `shipped`.
- Open one PR from the feature branch into `main`, with the report as its description and the checks only a human can do (real devices, real files) as a checklist. If `approve` includes `merge`, stop for the human's approval; once they approve, check CI is green, merge it yourself, and clean up the branches. Otherwise merge it once CI passes.
- Hand back one report:
  - what shipped, with links
  - the combined decision ledger
  - anything flagged or parked
  - what needs human review, most important first
  - last, the stop: what the human does now, and what happens after. Once nothing is left, say to start a new session for the next request; the docs carry everything.
