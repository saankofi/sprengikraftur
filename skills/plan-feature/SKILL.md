---
name: plan-feature
description: Turn a request, idea or spec into a planned feature — triage it, write docs/features/NNNN-*.md with deliverables and acceptance criteria, and split it into vertical slices as GitHub issues. Use when someone wants something built that is bigger than a quick fix.
---

# plan-feature

Turn a request into something an agent can build and a human can check.

## Triage first

Choose the lightest route that's safe, and say which you chose:
- **direct:** small, low-risk and obvious. Just do it; no plan.
- **ticket:** one slice. A single issue with acceptance criteria.
- **feature:** anything bigger, or touching a `pinned_high` area, the data model, or a new external service.

## The feature doc

`docs/features/NNNN-short-slug.md`. Cover:
- **why:** the problem and who has it
- **deliverables:** what will exist when it's done
- **acceptance criteria:** observable and testable
- **out of scope**
- **risk:** inherits the project default; any override needs a reason
- **slices:** with links to their issues
- **assumptions and decisions** made along the way.
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
- If `gates` includes `spec` or `plan`, stop for approval before slices are built.
