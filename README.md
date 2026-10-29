# Sprengikraftur

A small skill bundle for building software with strong LLM agents on [oh-my-pi (omp)](https://github.com/can1357/oh-my-pi).

## Philosophy

**Guide how the agent works, not how it does the work.** The skills set direction, boundaries and a definition of done, and leave the technique to the model. Less is more: every line in a skill should change behaviour. The bundle therefore assumes a strong model; weaker models need a more prescriptive process than this one.

Principles that run through every skill:

1. **Docs are the current truth.** A few short docs say why and what; code and tests show how. Updating the docs is part of done.
2. **Ask about the business, decide the technical.** Business rules (what gets recorded, money, who can do what, what users see) are never guessed silently. Technical choices are the agent's, recorded as it goes. Architecture and commitments outside the codebase (third parties, cost, data leaving the system, licenses) are proposed as ADRs for the human to accept. Questions come in one batch, each with a default, so `go` answers them all.
3. **What's written is binding.** Anything the human wrote or approved is a requirement. Fill the gaps; flag conflicts rather than silently "improving" things.
4. **Vertical slices, sized by what they deliver.** Each slice works end to end and has acceptance criteria. The plan marks which slices can be built together, and those are built in parallel; rules they share are settled in the feature doc first, so each slice doesn't invent its own.
5. **One builder, one independent reviewer.** Acceptance tests first, a real end-to-end check, and a review by a different model before the PR. Unit tests stay, and each core flow keeps a happy-path end-to-end test through what users use.
6. **Stop only where a human is needed.** Run every other step. At a stop, say exactly what to do and what happens after, so nothing has to be remembered.

## Skills

| Skill | Does |
|---|---|
| `living-docs` | Creates or refreshes `AGENTS.md` and `docs/{BUSINESS,PRODUCT,ARCHITECTURE,DESIGN}.md` (BUSINESS and DESIGN are optional) |
| `adr` | Records a decision in `docs/adr/NNNN-*.md` |
| `plan-feature` | Triage, then `docs/features/NNNN-*.md` plus a feature issue with its slices as sub-issues |
| `build-slice` | Builds one slice to done: tests, end-to-end check, review, PR, green CI, docs updated |
| `drive-feature` | Runs `build-slice` across a feature's slices, then reports once |

Each skill works on its own; they coordinate only through the files above and their GitHub issues.
Execution uses omp's built-in features (`task`, the `reviewer` agent, `browser`, the `github` tool, `omp commit`), plus `gh` for issues, which the `github` tool can't create. If one is missing, the skill uses an equivalent, or stops and says so.

## Config

A YAML block in a `## Sprengikraftur` section of the project's `AGENTS.md` (the `living-docs` skill adds it):

```yaml
risk: medium                 # low | medium | high; a feature doc may override this, with a reason
approve: [merge]             # spec | plan | slice | merge: wait for the human at these points
ci_budget: { unit: 30s, full: 5m }
docs: docs                   # folder for the docs, ADRs and feature docs
```

### `risk`

How costly a mistake would be. It sets the rigour (edge-case tests, how strict the review is) and how readily the agent asks about business rules:

- **`low`:** asks only when it can't go on without an answer.
- **`medium`:** asks where a wrong guess would record wrong data or be hard to undo, for example how currencies are handled.
- **`high`:** asks about any business rule that isn't written down.

Technical choices are never asked; architecture and outside commitments always come to you as proposed ADRs. A feature doc can raise or lower risk for that feature, with a reason.

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

### `docs`

Where the docs, ADRs and feature docs live; every `docs/` path in the skills and in this README means this folder. Leave it as `docs` unless `docs/` already has another job, such as a published docs site; then use something like `docs/sprengikraftur`. `living-docs` checks for this when it first adds the config block, and asks. `AGENTS.md` always stays at the repo root. To move the docs later, change `docs` and run `/living-docs`; it moves them and fixes the links.

## Models

There are three jobs, and they need different things:

- **Planning** (`living-docs`, `plan-feature`): judgement about the business, such as which questions to ask, safe defaults, and checking facts. It uses few tokens, so use the strongest model you have.
- **Building** (`build-slice`): good technical judgement. It uses most of the tokens, so this is where a cheaper model pays off.
- **Reviewing** (omp's `reviewer` agent): an independent check. Always a different model from the builder, ideally from a different company. It's cheap.

Each job runs on an omp model role: the session (planning and driving) on `default`, builders (omp's `task` agent) on `task`, and the reviewer on `slow`. Set them in `~/.omp/agent/config.yml` (check with `omp config get modelRoles`):

```yaml
modelRoles:
  default: anthropic/claude-opus-5.5     # plans and drives
  task: anthropic/claude-sonnet-5.5      # builds
  slow: openai-codex/gpt-6.1-sol         # reviews
```

Without `task`, builders run on `default`. Keep `task` and `slow` different. On a subscription, choose by quota rather than price: a cheaper builder still saves most of it, because building uses most of the tokens.

Tested in [`runs/`](runs/) (✓ good, ✗ not good enough, ? untested; prices per million tokens in/out on OpenRouter, October 2026):

| Model | In / out | Plan | Build | Review |
|---|---|---|---|---|
| `anthropic/claude-fable-5.1` | $10 / $50 | ? | – | – |
| `anthropic/claude-opus-5.5` | $4 / $20 | ✓ | ✓ | ? |
| `anthropic/claude-sonnet-5.5` | $2 / $10 | ? | ? | ? |
| `openai/gpt-6-astra` | $10 / $50 | ? | – | – |
| `openai/gpt-6.1-sol` | $2 / $10 | ? | ? | ✓ |
| `z-ai/glm-5.3` | $0.08 / $4.80 | ✗ | ✓ | ? |
| `moonshotai/kimi-k3` | $0.50 / $15 | ✗ | ? | ✓ |
| `deepseek/deepseek-v4-pro` | $0.66 / $1.98 | ? | ? | ? |
| `qwen/qwen3.8-max` | $2 / $6 | ? | ? | ? |
| `moonshotai/kimi-k2.7-code` | $0.67 / $3.35 | ✗ | ✗ | – |

Proven so far: **Opus plans, GLM 5.3 builds, GPT-6.1 Sol or Kimi K3 reviews**, for about $6 for a small MVP. On a real 5-day project with Opus building, building was 70% of the cost. Cheap models plan badly: they fill business gaps with silent defaults and state unchecked facts. The smallest tiers (Haiku, GPT Luna, the Flash models) are untested and probably too small to build.

## Install

```sh
npx skills add saankofi/sprengikraftur -g -a universal
```

This installs into `~/.agents/skills`, which omp reads. Leave out `-g` to install into one project's `.agents/skills` instead. Check with `omp read skill://plan-feature`; update with `npx skills update -g`.

## Usage

### Setup (once per project)

1. **Install** the skills and **set the model roles** (above).
2. In omp, in the project's directory, run `/living-docs`, adding what you know: what it's for, who uses it, the stack. It reads any existing code and asks one batch of questions.
3. **Read the docs it writes** and fix anything wrong; what you write there is binding. Set `risk` and `approve` in `AGENTS.md` if the defaults don't fit.

### Daily use

1. **Start a new session for each request.** The docs carry the context, so a fresh session loses nothing, and it's cheaper and sharper than one that has run for days.
2. **Ask for what you want**, from one line to a full spec. `plan-feature` usually loads by itself; if not, run `/plan-feature <request>`. Small things are done directly; bigger ones get a feature doc, plus a GitHub feature issue with the slices as its sub-issues.
3. **Do what each stop says.** Answer its questions (`go` accepts the defaults), check the plan if `plan` is in `approve`, and approve the PR into `main` with `go`. The agent merges it, and the docs are already current. When a request is finished, start a new session for the next one.

Every issue the bundle creates starts with the command that builds it, so you can start work from Orca's issue list. Filter it with `is:open label:feature` for the features, or `is:open label:ready-for-agent -label:slice` for everything you can start at the top level (features and tickets).

To build an existing plan:
- **In one session:** start the feature issue from Orca, or run `/drive-feature <feature issue URL or docs/features/NNNN-*.md>`. It builds the slices the plan marks as buildable together in parallel, and the rest in dependency order, closes each slice's issue as it merges, and the final PR closes the feature issue. To check as you go, or to build fewer at once, add a limit in plain words. It stops after each batch on the feature branch, and `go` starts the next. For example:
  ```
  /drive-feature docs/features/0003-csv-export.md build 3 slices, then stop
  /drive-feature docs/features/0003-csv-export.md at most 2 at once
  /drive-feature docs/features/0003-csv-export.md one slice at a time, I'll test each on my phone
  /drive-feature docs/features/0003-csv-export.md build only slice 2
  ```
- **One slice or ticket per session** (for example, several sessions side by side): start its issue from Orca, or run `/build-slice <issue URL>`. With no feature branch, each gets its own PR into `main` that closes its issue, merged on your `go`. Pick slices the feature doc marks as buildable together. When the last slice of a feature merges, its stop tells you to start the feature issue from Orca: it skips the finished slices, does only the finish (docs, `living-docs`, status), and its PR closes the feature issue. After a big change made outside the bundle, run `/living-docs` to bring the docs back in line.

## Status

Tested on six runs: a receipt-scanner MVP and two features on top of it with Opus and GPT, then the MVP again with cheap models and finally with Opus planning and GLM building. Not yet checked:
1. Using the `github` tool's Actions watch for the CI fix loop.
2. Whether goal or loop mode helps `drive-feature`.
3. `approve: [slice]`.
4. Starting issues from Orca's issue list.

Write-ups of test runs are in [`runs/`](runs/).

Ideas borrowed from OpenSpec, BMAD, Matt Pocock's skills, Compound Engineering, Spec Kit, Superpowers and cc-sdd.

## License

MIT. See [LICENSE](LICENSE).
