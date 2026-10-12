---
name: adr
description: Record an architecture or technical decision as a numbered ADR in docs/adr/. Use whenever a decision is made that a future agent would otherwise question, undo or have to rediscover.
---

# adr

Record why something is the way it is, so nobody relitigates it.

- One decision per file: `docs/adr/NNNN-short-slug.md`, numbered after the highest existing number.
- Cover: context, the decision, alternatives considered, consequences, status (`proposed`, `accepted`, or `superseded by NNNN`).
- Keep it short. A few paragraphs at most.
- Accepted ADRs are never edited. To change a decision, write a new ADR and mark the old one superseded.
- Decisions that cross the codebase boundary (architecture direction, third parties, cost, data leaving the system, licenses) stay `proposed` until the human accepts them.
- If the decision changes how things are built, update `docs/ARCHITECTURE.md` to match.
