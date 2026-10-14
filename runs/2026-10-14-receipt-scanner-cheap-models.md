# Run 4: cheap models, TypeScript, medium risk (2026-10-14)

A stress test of "assumes a strong model".

**Setup:**
- **Brief:** the same as run 1, but with TypeScript, Node, React and SQLite as the stack.
- **Config:** `risk: medium`.
- **Models:** Kimi K2.7 Code as the builder (`default`) and GLM 5.3 as the reviewer (`slow`), both through OpenRouter.
- **No GitHub remote.**

## Attempt 1

`/living-docs` with the brief was the only prompt. Kimi:

- **Never left `living-docs`.** It went on to write a feature plan, scaffold the project and start building, all inside that skill.
- **Loaded no other skill and started no subagents.** It used its own habits, not the bundle's process.
- **Asked nothing.** It decided the fields itself (only date, merchant and amount), treated everything as HKD with no flag for other currencies, and invented "staff can review and correct later".
- **Read money through a float.** It asked the model for `"amount": 123.45` and computed `Math.round(parseFloat(...) * 100)`. Storage is integer cents. At medium risk, "the cost of being wrong" alone didn't make it careful.
- **Planned the build horizontally:** schema, backend, frontend, then "wire it up". It wrote no acceptance tests first and made no feature branch.

It was stopped mid-build. The work is kept on the `attempt-1-kimi` branch of the local repo.

## Changes made afterwards

- **Each skill now opens with one line saying what it does and doesn't do:**
  - `living-docs` only writes docs, then says what comes next;
  - `plan-feature` writes no code;
  - `build-slice` builds only its slice;
  - `drive-feature` never builds slices itself;
  - `adr` only records the decision.

## Attempt 2

Same setup, with the boundary lines.

- **The boundary held.** It stopped after the docs.
- **It still asked nothing.** It invented a review-before-save step, an admin role, a retry flow and "currency fixed to HKD", all decisions that change what gets built.
- **It broke rules that are already written:**
  - It replaced the brief's "qwen flash" with `qwen/qwen-vl-plus`.
  - Its docs were about what's missing ("scaffold not yet in place", "to add later").
- **"What comes next" was a horizontal build list,** not `plan-feature`.

Stopped there.

## Conclusion

Kimi K2.7 Code can't drive this bundle. It ignores rules that are already written down, so more lines wouldn't help; making it work would take step-by-step instructions, which goes against the bundle's philosophy.

**Kept:**
- the boundary lines;
- a pointer to the next skill: `living-docs` says what comes next is usually `plan-feature`.

**Next:** try a newer cheap model before reaching for a mixed setup.

## Attempt 3: GLM 5.3 builds, Kimi K3 reviews

Same brief and skills. The human added `plan` to `approve` after `living-docs`.

**Result:** shipped. Three vertical slices (an offline walking skeleton, real extraction, then the detail view, phones and a single-process build), 13 signed commits on `feature/0001-receipt-scanner-mvp`, and 42 tests passing. The stop said to merge locally and what's left to check by hand.

**Cost:** about $5.60 in total, by the session logs: $0.31 for `living-docs`, $3.35 for GLM planning, driving and building, and $1.98 for Kimi reviewing. Run 1's Opus build cost $38.

**Good:**
- **Each skill stayed in its lane.** `living-docs` stopped after the docs, `plan-feature` wrote no code, `drive-feature` ran each slice as a `build-slice` subagent, and Kimi K3 reviewed each one.
- **Acceptance tests first.** Each slice opened with failing tests; slice 1's acceptance tests were deleted once green, and two core-flow tests (scan a receipt, see the transactions) were kept.
- **Money done right:** integer minor units per currency, parsed once at the edge, with ambiguous European formats rejected instead of misread.
- **It respected commit signing.** Signing goes through 1Password and timed out once; it stopped and said so instead of working around it. Builders then staged their work and the driver made the commits.
- **An honest report:** the real cost per scan ($0.027, against a planned ≲$0.001), the error paths only tested with fixtures, and the checks left for a human (real receipts, a real phone camera, images going to OpenRouter).

**Not good:**
- **It asked nothing, again.** The plan decided HKD only with no currency column, and no line items, tax, payment method or raw output. It listed these openly as assumptions, so the plan stop caught them and one reply fixed them. Without `plan` in `approve`, a US-dollar receipt would have been saved as Hong Kong dollars.
- **`living-docs` wasn't run at the finish.** The driver checked the docs against the code itself instead.
- **The kept "end-to-end" tests are at the HTTP level.** There are no frontend tests; the browser was only checked by hand during each slice.
- **Interruptions:** provider stalls, and the OpenRouter credit ran out mid-slice once. Each time it resumed cleanly when told to carry on.

**Conclusion:** GLM 5.3 can drive the bundle, but not alone: it doesn't ask product questions. With cheap models, use `approve: [plan, merge]` so a human checks the plan's assumptions.

## Changes made afterwards

- **`approve: [slice]` replaces `mode`.** It stops after each slice on the feature branch so the human can try it; `mode: ticket` (a PR into `main` per slice) is gone.
- **The README** documents each `approve` value and recommends `[plan, merge]` with models that don't ask.
- **Install** is `npx skills add saankofi/sprengikraftur -g -a universal`.
- **Merging:** the human approves with `go`; the agent checks CI and merges.

# Run 5: GLM 5.3 again, with business questions (2026-10-14)

The same brief and models as run 4, attempt 3, after the question changes: ask about business rules (as far as `risk` says), decide technical ones, and put the questions inside the plan stop. Stopped at the plan stop. Cost: $0.12.

**Better:**
- **`living-docs` asked three questions in one batch, each with a default, all about business rules:** which fields to record, which accounting system, and whether to record who submitted. Run 4 asked none. Removing "or reasonably default", the phrase it had quoted to itself, made the difference.
- **`plan-feature` asked two, both about money:** confirm before saving, and delete. They came inside the plan stop, so there was no second stop.
- **No technical questions.** Technical choices were listed separately as the planner's decisions, and the builder was told the endpoint shapes "are defaults, not straitjackets".

**Still wrong:**
- **Currency only came up because the human asked.** The recommended field set left it out, at `medium` risk where it is the clearest case of wrong data.
- **An invented model ID.** It wrote `qwen/qwen3-vl-flash` into the docs, with a made-up retirement date for an older snapshot. OpenRouter has no such model; it searched the web and never checked OpenRouter.
- **A contradiction between docs went unnoticed.** BUSINESS.md says currency is "never assumed to be HKD", PRODUCT.md says "default HKD when unreadable", and the plan inherited the second.
- **A wasted question:** it asked whether to reopen "no delete", which PRODUCT.md had already settled.

**Conclusion:** the question changes work, even on a cheap model. What GLM lacks is judgement: checking facts, seeing contradictions, picking safe defaults. It plans and builds well enough once the docs and plan are right. Next: screen Kimi K3 on `living-docs` and `plan-feature` alone; if it fails too, use a frontier model for docs and planning and a cheap one to build.

## Changes made afterwards

- **`living-docs`:** facts about outside services (model IDs, API versions, prices) are checked against the service itself, not memory or search results.

## Attempt 2: Kimi K3, `living-docs` only

The same brief, with the fact-check line. Stopped after `living-docs`.

**Good:**
- **It checked the model ID against OpenRouter's live model list** and wrote the right one (`qwen/qwen3.8-flash`) as a setting. The new line worked.
- **It handled the key carefully:** it read only the key names from `.env` and used the key without printing it.
- **Two questions, both about business:** which accounting system, and whether staff log in. Nothing technical. The docs were minimal (484 words).

**Not good:**
- **"Amounts are HKD only; no multi-currency in the MVP"** was written as a business rule without asking, the same as GLM.
- **It set `risk: low` itself.** Since risk now decides how readily it asks, that lowered the bar for its own questions.
- **It recommended Xero** for a question whose honest answer was "undecided".

## Changes made afterwards

- **`living-docs`:** writes the default config; changing `risk` or `approve` is the human's call.

**Next:** run Opus on the same brief, as a baseline. No model has raised currency unprompted on this brief yet, and run 1 never tested it: Opus was given the answers.
