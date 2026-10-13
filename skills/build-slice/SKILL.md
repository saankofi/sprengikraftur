---
name: build-slice
description: Build one vertical slice to done — tests first, a real end-to-end check, an independent review by a different model, a PR with green CI, and updated docs. Use for a ready-for-agent issue, a slice from a feature doc, or a small well-defined request.
---

# build-slice

Ship one slice so it's verifiably done and the docs still tell the truth.

## Done means

- The acceptance criteria are covered by tests, written first.
- The real thing works end to end: run it, and use the browser for UI. Keep only core happy-path end-to-end tests permanently.
- An independent review passed: omp's `reviewer` agent (it runs on omp's `slow` role, a different model from the builder), given the acceptance criteria and the diff. Fix the findings, or record why not.
- A PR is open (omp's `github` tool), with CI green. Fix failures and push until it passes. It targets the feature branch when there is one, otherwise `main`.
- The docs match reality, and stay short: `docs/PRODUCT.md` (what users see, not the numbers behind it) and `docs/ARCHITECTURE.md` updated, ADRs written for decisions that are hard to reverse, superseding any they contradict, and the slice ticked off in the feature doc.

## How to work

- Read `AGENTS.md` and the relevant docs first. What's written is binding; if something looks wrong, flag it rather than working around it.
- Make technical decisions yourself and keep a decision ledger: what you decided, and what it costs if wrong. It goes in the PR description.
- Stop and ask only for things that change acceptance criteria, or that commit to things outside the codebase (a new service or vendor, cost, data leaving the system).
- Let risk set the rigour: higher risk gets more edge-case tests and a stricter review. Rigour scales with the cost of being wrong, not with what's possible.
- Build for what exists. Don't build compatibility for data, users or releases that don't exist yet.
- If CI exceeds `ci_budget`, open an issue to speed it up.
- Merge into a feature branch yourself. A PR into `main` waits for the human if `approve` includes `pr`.
- Don't work around security controls (commit signing, auth, hooks). Stop and say so.
- If an omp feature named here isn't available, use an equivalent. If there isn't one, stop and say so.

## Report

What shipped, the PR link, the decision ledger, anything flagged, and what the human should look at. Report what you checked, not what you suspect; if you couldn't check something, say so.
