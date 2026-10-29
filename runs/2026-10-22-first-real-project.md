# First real project: a static bilingual recipe site (2026-10-22)

The first use outside the test runs: a static site in Python, built from about 150 structured recipes, deployed with GitHub Actions to Cloudflare Pages. Opus built, GPT-6.1 Sol reviewed. Config: `risk: medium`, `approve: [merge]`.

## Result

- **Live after 5 days:** two features and 21 PRs, all merged by the agent after the owner's `go`. CI was green throughout, and tests and checks pass.
- **The process held up on real work:**
  - each slice opened with acceptance tests, deleted once green;
  - ADRs for the decisions that are hard to reverse;
  - a log of the owner's decisions that overrides every pipeline rule;
  - the agent stopped instead of working around commit signing when 1Password wasn't running;
  - the last PR came with an audit of the docs against the code;
  - the final stop said what's live, what's left on the owner's side, and that nothing else was open.
- **Cost: $212** in total: $149 for Opus builders, $57 for the main session, $6.60 for GPT reviews.

## What went wrong

- **One session for 5 days.** The driver's context grew from 50k to about 600k tokens, which made every call it made expensive. The docs already carried the state, so a new session per request would have lost nothing.
- **All builders ran on Opus.** A cheaper builder after the plan stop (run 6) would probably have cut the $149 sharply.
- **Work after the feature had shipped** (design passes, images, search engine work, a cooking mode) was done as issues under the shipped feature, without `plan-feature` triaging it as new work. This happened once; not changed yet.

## Changes made afterwards

- **README Usage** is split into Setup (once per project) and Daily use, starting with "start a new session for each request".
- **Builders get their own model role.** omp's `task` agent runs on `modelRoles.task`, checked with a one-subagent run: the session stayed on Opus and the subagent ran on Sonnet. That replaces switching with `/model` at the plan stop.
- **`drive-feature`:** once nothing is left, the final stop says to start a new session for the next request.
- **`plan-feature`** (2026-10-29): a request about a feature that has shipped is triaged as new work, and the feature isn't reopened.
