---
name: adr
description: Record an architecture or technical decision as a numbered ADR in docs/adr/. Use for decisions that are hard to reverse, or that a future agent would likely undo. Not for choices the code already makes obvious.
---

# adr

Record why something is the way it is, so nobody relitigates it.

- One decision per file: `docs/adr/NNNN-short-slug.md`, numbered after the highest existing number.
- Cover: context, the decision, alternatives considered, consequences, status (`proposed`, `accepted`, or `superseded by NNNN`).
- Keep it short. A few paragraphs at most.
- An accepted ADR's body is never edited; only its status line may change (e.g. "amended by 0012"). To change a decision, write a new ADR and mark the old one superseded. Check existing ADRs for one your decision contradicts.
- Decisions that cross the codebase boundary (architecture direction, third parties, cost, data leaving the system, licenses) stay `proposed` until the human accepts them.
- If the decision changes how things are built, update `docs/ARCHITECTURE.md` to match.
