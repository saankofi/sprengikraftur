# Sprengikraftur

A small skill bundle for building software with strong LLM agents on [oh-my-pi (omp)](https://github.com/can1357/oh-my-pi).

## Philosophy

**Guide how the agent works, not how it does the work.** The skills set direction, boundaries and a definition of done, and leave the technique to the model. Less is more: every line in a skill should change behaviour. The bundle therefore assumes a strong model; weaker models need a more prescriptive process than this one.

Principles that run through every skill:

1. **Docs are the current truth.** A few short docs say why and what; code and tests show how. Updating the docs is part of done.
2. **Decide, don't ask.** Ask the human only about what changes deliverables or acceptance criteria, or what commits to things outside the codebase (architecture direction, third parties, cost, data leaving the system, licenses). Ask in one batch, with suggested defaults. Decide everything else, and record it.
3. **What's written is binding.** Anything the human wrote or approved is a requirement. Fill the gaps; flag conflicts rather than silently "improving" things.
4. **Vertical slices, sized by what they deliver.** Each slice works end to end and has acceptance criteria.
5. **One builder, one independent reviewer.** Tests first, a real end-to-end check, and a review by a different model before the PR.

## Skills

| Skill | Does |
|---|---|
| `living-docs` | Creates or refreshes `AGENTS.md` and `docs/{BUSINESS,PRODUCT,ARCHITECTURE,DESIGN}.md` (BUSINESS and DESIGN are optional) |
| `adr` | Records a decision in `docs/adr/NNNN-*.md` |
| `plan-feature` | Triage, then `docs/features/NNNN-*.md` plus slices as GitHub issues |
| `build-slice` | Builds one slice to done: tests, end-to-end check, review, PR, green CI, docs updated |
| `drive-feature` | Runs `build-slice` across a feature's slices, then reports once |

Each skill works on its own; they coordinate only through the files above.
Execution uses omp's built-in features (`task`, the `reviewer` agent, `browser`, the `github` tool, `omp commit`). If one is missing, the skill uses an equivalent, or stops and says so.

## Config

A YAML block in a `## Sprengikraftur` section of the project's `AGENTS.md` (the `living-docs` skill adds it):

```yaml
risk: medium                 # low | medium | high; a feature doc may override this, with a reason
approve: [pr]                # spec | plan | pr: wait for human approval at these points
mode: feature                # feature = build all slices | ticket = one slice at a time
ci_budget: { unit: 30s, full: 5m }
```

With `approve: [pr]`, slices merge into a feature branch on their own, and you merge the feature into `main`. `approve: []` lets the agent merge to `main` itself.

## Models

The builder and the reviewer must be different models. Builders run on the session's model; omp's `reviewer` agent runs on the `slow` role. Set both roles in `~/.omp/agent/config.yml`:

```yaml
modelRoles:
  default: anthropic/claude-opus-5-5     # builds
  slow: openai-codex/gpt-6.1-sol         # reviews
```

Check with `omp config get modelRoles`. If you switch models in a session (`/model`), keep it different from `slow`. Use strong models for both.

## Install

Symlink the skills where omp discovers them:

```sh
mkdir -p ~/.agents/skills
for s in skills/*/; do ln -s "$PWD/$s" ~/.agents/skills/; done
```

To use them in one project only, link into the project's `.agents/skills/` instead (and gitignore `.agents`).

## Usage

In omp, in the project's directory:

1. **Set up the docs.** Run `/living-docs`, adding what you know: what it's for, who uses it, the stack. It reads any existing code and asks one batch of questions. Read the docs it writes and fix anything wrong; what you write there is binding.
2. **Plan a feature.** Describe what you want, from one line to a full spec. `plan-feature` usually loads by itself; if not, run `/plan-feature <request>`. Small things are done directly. Bigger ones get a feature doc and slices as GitHub issues.
3. **Build it.** Run `/drive-feature docs/features/NNNN-*.md` to build every slice and get one report back. To build one slice yourself, run `/build-slice <issue>`.
4. **Read the report.** Look at the decision ledger, anything flagged, and the checks left for you.

Run `/living-docs` again whenever the docs seem to have drifted. Add `spec` or `plan` to `approve` if you also want to approve those before work continues.

## Status

Tested on two runs: a new project (a receipt-scanner MVP) and a second feature on top of it. Not yet checked:
1. Using the `github` tool's Actions watch for the CI fix loop.
2. Whether goal or loop mode helps `drive-feature`.
3. A builder other than Opus.

Write-ups of test runs are in [`runs/`](runs/).

Ideas borrowed from OpenSpec, BMAD, Matt Pocock's skills, Compound Engineering, Spec Kit, Superpowers and cc-sdd.
