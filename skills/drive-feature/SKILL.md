---
name: drive-feature
description: Build a planned feature end to end by running build-slice for each of its slices, then report back once. Use when a feature doc with slices exists and the human wants it built, either whole or one slice at a time.
---

# drive-feature

Get a whole feature built while the human is away, then hand back one clear report.

## How to work

- Read the feature doc and `AGENTS.md`. Set the feature's status to `building`.
- Build each slice with `build-slice`, in dependency order, each in its own `task` subagent. Keep your own context small: take back only each slice's report, never its diffs.
- Build slices one after another by default. Run them in parallel (isolated worktrees) only when they change different parts of the code; if two slices touch the same screen, table, module or rule, build them in sequence.
- If `mode: ticket`, build one slice and stop.
- Stop for the human only at a configured gate, or when a question blocks the work. Otherwise keep going: park the blocked slice and carry on with the others.

## Finish

- Check that the docs describe what actually shipped: PRODUCT, ARCHITECTURE, ADRs, the feature doc. Check new ADRs against older ones; supersede any they contradict. Where docs conflict on a product rule, say which rule the code follows today, and flag it. Set the status to `shipped`.
- Hand back one report:
  - what shipped, with links
  - the combined decision ledger
  - anything flagged or parked
  - what needs human review, most important first
