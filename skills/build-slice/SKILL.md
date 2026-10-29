---
name: build-slice
description: Build one vertical slice to done — tests first, a real end-to-end check, an independent review by a different model, a PR with green CI, and updated docs. Use for a ready-for-agent issue, a slice from a feature doc, or a small well-defined request.
---

# build-slice

Ship one slice so it's verifiably done and the docs still tell the truth.

Build only this slice. Anything else you notice goes in the report.

`docs/` here means the folder set by `docs` in `AGENTS.md` (default `docs`).

## Done means

- Acceptance tests came first: one per acceptance criterion, at the outermost level that shows it (the browser for a UI flow, the API for a backend rule), seen failing. The inside was then test-driven until they passed.
- The real thing works end to end: run it, and use the browser for UI.
- Unit tests written while test-driving stay; only the slice's acceptance tests are deleted once they pass (git keeps them).
- The permanent end-to-end suite has one happy-path test per core flow in `docs/PRODUCT.md`, through the surface users use: the browser for a UI (an HTTP-only test doesn't count), the API or CLI otherwise. If this slice adds or changes a core flow, update that flow and its test, and flag it. With no end-to-end harness yet, the first slice that touches a core flow sets one up and records how to run it in `AGENTS.md`.
- An independent review passed: omp's `reviewer` agent (it runs on omp's `slow` role, a different model from the builder), given the acceptance criteria and the diff. Fix the findings, or record why not.
- A PR is open (omp's `github` tool), with CI green. Fix failures and push until it passes. It targets the feature branch when there is one, otherwise `main`. Given an issue, the PR description says `Closes #N` for it. With no GitHub remote, use local branches and run the checks in `AGENTS.md` in place of CI.
- The docs match reality, and stay short: `docs/PRODUCT.md` (what users see, not the numbers behind it) and `docs/ARCHITECTURE.md` updated, ADRs written for decisions that are hard to reverse, superseding any they contradict, and the slice ticked off in the feature doc.

## How to work

- Read `AGENTS.md` and the relevant docs first; given a slice issue, also the feature doc its feature issue links to. What's written is binding; if something looks wrong, flag it rather than working around it.
- Make technical decisions yourself and keep a decision ledger: what you decided, and what it costs if wrong. It goes in the PR description.
- Stop and ask only about a business rule the docs and acceptance criteria don't settle, or something that commits outside the codebase (a new service or vendor, cost, data leaving the system). Technical questions are yours.
- Let risk set the rigour: higher risk gets more edge-case tests and a stricter review. Rigour scales with the cost of being wrong, not with what's possible.
- Build for what exists. Don't build compatibility for data, users or releases that don't exist yet.
- If CI exceeds `ci_budget`, open an issue to speed it up.
- Merge into a feature branch yourself. A PR into `main` waits for the human's approval if `approve` includes `merge`; once they approve, check CI is green, merge it yourself, and clean up the branch. At the stop, say exactly what to do, what to check, and what happens after ("reply `go` and I'll …").
- If the PR goes into `main` and closes a feature's last open slice (its feature issue has no other open sub-issues), the stop, and the report after merging, end with: start feature issue #N in Orca to finish. `drive-feature` skips the done slices and only does the finish.
- Don't work around security controls (commit signing, auth, hooks). Stop and say so.
- If an omp feature named here isn't available, use an equivalent. If there isn't one, stop and say so.

## Report

What shipped, the PR link, the decision ledger, anything flagged, and what the human should look at. Report what you checked, not what you suspect; if you couldn't check something, say so.
