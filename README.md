# Sprengikraftur

A small skill bundle for building software with strong LLM agents on [oh-my-pi (omp)](https://github.com/can1357/oh-my-pi).

## Philosophy

**Guide how the agent works, not how it does the work.** The skills set direction, boundaries and a definition of done, and leave the technique to the model. Less is more: every line in a skill should change behaviour. The bundle therefore assumes a strong model; weaker models need a more prescriptive process than this one.

Principles that run through every skill:

1. **Docs are the current truth.** A few short docs say why and what; code and tests show how. Updating the docs is part of done.
2. **Decide, don't ask.** Ask the human only about what changes deliverables or acceptance criteria, or what commits to things outside the codebase (architecture direction, third parties, cost, data leaving the system, licenses). Ask in one batch, with suggested defaults. Decide everything else, and record it.
3. **What's written is binding.** Anything the human wrote or approved is a requirement. Fill the gaps; flag conflicts rather than silently "improving" things.
4. **Vertical slices, sized by what they deliver.** Each slice works end to end and has acceptance criteria.
5. **One builder, one independent reviewer.** Acceptance tests first, a real end-to-end check, and a review by a different model before the PR.
6. **Stop only where a human is needed.** Run every other step. At a stop, say exactly what to do and what happens after, so nothing has to be remembered.

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
approve: [merge]             # spec | plan | slice | merge: wait for the human at these points
ci_budget: { unit: 30s, full: 5m }
```

### `approve`

Everything runs on its own except the steps listed in `approve`. At each one the agent stops and says what to check, what to reply, and what happens next.

| Value | Stops | You | Then |
|---|---|---|---|
| `spec` | After the feature doc's deliverables and acceptance criteria, before slicing | Check *what* gets built. Reply `go` or say what to change | It plans the slices |
| `plan` | After the slices are planned, before building | Check what gets built and how it's cut. Reply `go` or say what to change | It builds every slice |
| `slice` | After each slice is built, reviewed and merged into the feature branch | Try it: the stop says how to run it and what to check. Reply `go` or report a problem | It fixes the problem, or starts the next slice |
| `merge` | After every slice is done and the docs are refreshed on the feature branch | Review the one PR (or branch) into `main` and its checklist of human-only checks. Reply `go` | It checks CI, merges into `main` and cleans up the branches. The feature is done |

- **`[merge]` (default):** you only see the finished feature.
- **`[plan, merge]`:** also catches wrong guesses about the product before any code is written. Use it with models that don't ask questions (see [run 4](runs/2026-10-14-receipt-scanner-cheap-models.md)).
- **`[slice, merge]`:** test as you go; use it when you want to see each step working on a real device or real data.
- **`[]`:** fully hands-off; the agent merges into `main` as soon as CI passes.

You never merge anything yourself: approving is replying `go` in the session.

Small changes skip the feature machinery: a one-line fix is just done, and a single-slice ticket gets its own PR into `main`, which waits for your `go` if `merge` is set.

## Models

The builder and the reviewer must be different models. Builders run on the session's model; omp's `reviewer` agent runs on the `slow` role. Set both roles in `~/.omp/agent/config.yml`:

```yaml
modelRoles:
  default: anthropic/claude-opus-5-5     # builds
  slow: openai-codex/gpt-6.1-sol         # reviews
```

Check with `omp config get modelRoles`. If you switch models in a session (`/model`), keep it different from `slow`. Use strong models for both.

## Install

```sh
npx skills add saankofi/sprengikraftur -g -a universal
```

This installs into `~/.agents/skills`, which omp reads. Leave out `-g` to install into one project's `.agents/skills` instead. Check with `omp read skill://plan-feature`; update with `npx skills update -g`.

## Usage

In omp, in the project's directory:

1. **Set up the docs.** Run `/living-docs`, adding what you know: what it's for, who uses it, the stack. It reads any existing code and asks one batch of questions. Read the docs it writes and fix anything wrong; what you write there is binding.
2. **Ask for what you want**, from one line to a full spec. `plan-feature` usually loads by itself; if not, run `/plan-feature <request>`. Small things are done directly. Bigger ones get a feature doc and slices as GitHub issues, and are then built, reviewed and documented without further input.
3. **Do what the stop message says.** Usually that's reviewing one PR into `main`, with a checklist of checks only you can do, then replying `go`. The agent merges it; the docs are already current, so that finishes the feature.

To build an existing plan, run `/drive-feature docs/features/NNNN-*.md`, or `/build-slice <issue>` for one slice. Change `approve` to choose where it stops for you (see [`approve`](#approve)).

## Status

Tested on four runs: a new project (a receipt-scanner MVP) and two features on top of it with Opus and GPT, then the MVP again with cheap models. GLM 5.3 building with Kimi K3 reviewing shipped it for about $6; Kimi K2.7 couldn't drive it. Not yet checked:
1. Using the `github` tool's Actions watch for the CI fix loop.
2. Whether goal or loop mode helps `drive-feature`.
3. `approve: [slice]`.

Write-ups of test runs are in [`runs/`](runs/).

Ideas borrowed from OpenSpec, BMAD, Matt Pocock's skills, Compound Engineering, Spec Kit, Superpowers and cc-sdd.
