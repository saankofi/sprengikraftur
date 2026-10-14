---
name: plan-feature
description: Turn a request, idea or spec into a planned feature — triage it, write docs/features/NNNN-*.md with deliverables and acceptance criteria, and split it into vertical slices as GitHub issues. Use when someone wants something built that is bigger than a quick fix.
---

# plan-feature

Turn a request into something an agent can build and a human can check.

Only plan: don't write code. Building happens in `build-slice` or `drive-feature`.

## Triage first

A request may hold several unrelated changes; triage and plan each on its own. Choose the lightest route that's safe, and say which you chose:
- **direct:** small, low-risk and obvious. Just do it; no plan.
- **ticket:** one slice. A single issue with acceptance criteria.
- **feature:** anything bigger, or touching money, auth, deleting data, the data model, or a new external service.

Then ask: **does this change the architecture?** A new component, storage, service or deployment shape, or a change across the codebase (auth, background jobs). If so, decide it before slicing: ADRs (use the `adr` skill) and `docs/ARCHITECTURE.md`, then make the first slice a thin path through the new structure, end to end. Usually the answer is no, in one line.

## The feature doc

`docs/features/NNNN-short-slug.md`. Cover:
- **why:** the problem and who has it
- **deliverables:** what will exist when it's done
- **acceptance criteria:** observable and testable
- **out of scope**
- **risk:** inherits the project default; any override needs a reason
- **slices:** with links to their issues
- **assumptions and decisions** made along the way. Owner decisions go in PRODUCT.md or an ADR; link to them rather than repeating them.
- **status:** `planned`, `building` or `shipped`

Describe what and why. Leave the how to the builder, except where architecture or third-party choices need deciding (use the `adr` skill).

## Slices

- Each slice is vertical: it works end to end and delivers something observable.
- Size slices by what they deliver, not by count. One slice is fine; so is ten.
- Each slice has its own acceptance criteria and notes any known risks.
- Create them as GitHub issues (omp's `github` tool) labelled `feature:NNNN` and `ready-for-agent`, with dependencies noted. With no issue tracker, list them in the feature doc.

## Working with the human

- Start from whatever exists, from a one-line idea to a full spec. What they wrote is binding; fill only the gaps.
- Ask only what changes deliverables or acceptance criteria, or what commits to things outside the codebase. Ask in one batch, with suggested defaults. Record every other assumption in the doc.
- If `approve` includes `spec`, stop once the deliverables and acceptance criteria are written, before slicing. If it includes `plan`, stop once the slices are planned, before building. At a stop, say exactly what to do, what to check, and what happens after ("reply `go` and I'll …", or "nothing: merging finishes it").
- Otherwise go straight on: `build-slice` for a ticket, `drive-feature` for a feature.
