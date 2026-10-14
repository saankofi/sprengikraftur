---
name: living-docs
description: Create or refresh a project's living docs — AGENTS.md plus docs/BUSINESS, PRODUCT, ARCHITECTURE and DESIGN. Use at the start of a project, when docs have drifted from the code, or when a fresh agent would lack the context to work well.
---

# living-docs

Give any agent arriving cold what it needs to work well, in as few words as possible.

Only write docs: don't plan or build. When you're done, say what comes next.

## The docs

- `AGENTS.md`: the entry point. How to run, test, lint and format; conventions that aren't obvious from the code; the `## Sprengikraftur` config block; links to the docs below. Keep it short.
- `docs/BUSINESS.md`, optional: the business this lives in, who uses it and why, the domain rules that matter. Leave it out if there's no business context; its absence is information too.
- `docs/PRODUCT.md`: what the product does **today**, its users, core flows, domain rules. What users see, not the numbers and mechanics behind it.
- `docs/ARCHITECTURE.md`: how it's built **today**: components, data, external services, key constraints. Every external service sits behind an interface with a fake, and there's an offline dev mode. If that isn't true yet, say so.
- `docs/DESIGN.md`, optional: visual design (tokens, components, tone) when the product has a UI worth keeping consistent.

## How to work

- Docs describe current truth. Plans and history belong elsewhere (features, ADRs, git).
- Derive from the code and existing docs first. Where they disagree, believe the code and flag the gap.
- Ask the human only what you can't find out or reasonably default: business context, intent, architecture direction, third parties. Ask in one batch, each question with a suggested default.
- Anything the human wrote or approved is binding. Refine the wording; don't change the meaning.
- Check accepted ADRs against the code too. If one no longer holds, supersede it with a new ADR, or flag it.
- Prefer short and accurate over complete. A doc nobody keeps up to date is worse than no doc.
- On a new project, keep the docs minimal: say what exists and what was asked for, not what's missing.

## Config block (in AGENTS.md)

Add it if it's missing, with defaults that suit the project:

```yaml
risk: medium                 # low | medium | high
approve: [merge]             # spec | plan | merge: wait for human approval at these points
mode: feature                # feature | ticket
ci_budget: { unit: 30s, full: 5m }
```
