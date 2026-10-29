# AGENTS.md

Sprengikraftur is a skill bundle for omp. The skills are `skills/*/SKILL.md`; `README.md` says what the bundle does and how to use it; `runs/` holds write-ups of test runs.

## Checks

`python3 scripts/check.py` checks each skill's frontmatter and the relative links in the Markdown. CI runs the same.

## Conventions

- No `docs/` (owner's decision): the README is the product doc, and a feature's issue is its feature doc.
- Every line in a skill should change behaviour. Keep additions short and in the skills' existing voice: guide how the agent works, not how it does the work.
- No smoke run for skill changes (owner's decision, 2026-10-29): skill text has no runtime. Verification is the independent review of the diff against the acceptance criteria; the next real run in `runs/` confirms the behaviour.

## Sprengikraftur

```yaml
risk: medium                 # low | medium | high
approve: [merge]             # spec | plan | slice | merge: wait for the human at these points
ci_budget: { unit: 30s, full: 5m }
docs: docs                   # folder for the docs, ADRs and feature docs
```
