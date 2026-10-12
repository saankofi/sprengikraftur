---
name: drive-feature
description: Build a planned feature end to end by running build-slice for each of its slices, then report back once. Use when a feature doc with slices exists and the human wants it built, either whole or one slice at a time.
---

# drive-feature

Get a whole feature built while the human is away, then hand back one clear report.

## How to work

- Read the feature doc and `AGENTS.md`. Set the feature's status to `building`.
- Build each slice with `build-slice`, in dependency order, each in its own `task` subagent. Keep your own context small: take back only each slice's report, never its diffs.
- Run slices in parallel (isolated worktrees) only when they're truly independent.
- If `mode: ticket`, build one slice and stop.
- Stop for the human only at a configured gate, or when a question blocks the work. Otherwise keep going: park the blocked slice and carry on with the others.

## Finish

- Check that the docs describe what actually shipped: PRODUCT, ARCHITECTURE, ADRs, the feature doc. Set the status to `shipped`.
- Hand back one report:
  - what shipped, with links
  - the combined decision ledger
  - anything flagged or parked
  - what needs human review, most important first
