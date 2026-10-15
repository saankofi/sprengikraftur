# Run 6: Opus plans, GLM 5.3 builds (2026-10-15)

The receipt-scanner MVP again (receipt-scanner-5), with the jobs split by model:
- **Opus 5.5** ran `living-docs` and `plan-feature`. The human accepted every default and didn't raise currency.
- At the plan stop, the human switched the session to **GLM 5.3** with `/model` and replied `go` with no changes.
- **GPT-6.1 Sol** reviewed.

Config: `risk: medium`, `approve: [plan, merge]`.

## Result

- **Shipped:** two vertical slices on `feature/0001-receipt-scan-poc`, all commits signed. Slice 1 was a walking skeleton with the fake scanner, slice 2 the real scanner.
- **Checks:** 43 server tests, 2 frontend tests and 3 Playwright end-to-end tests, all offline; re-run independently.
- **The stop** asked for `go` to merge and delete the branch.
- **Cost:** about $5.90 in total:
  - Opus, docs and plan: $0.79;
  - Opus, a builder stopped by mistake: $0.17;
  - GLM, driving and building: $4.54;
  - GPT, reviews: $0.39.

## Opus's planning (compared with GLM and Kimi on the same brief, run 5)

- **It asked about currency without being prompted,** with a safe default. It also asked about final amount versus subtotal (the 10% service charge) and about duplicates. It asked nothing technical.
- **It checked the API key and the model ID against OpenRouter.**
- **The plan named the risks in this business:** DD/MM dates, `¥` meaning RMB or JPY, the model reading the subtotal. Library choices were left to the builder.
- **It decided one business rule itself and flagged it:** blank fields are saved. It should have been a question at `medium`.

## GLM's building

- **Acceptance tests first,** deleted once green. Three end-to-end tests for the core flows were kept (upload, list, rejected file). This is the first run that kept browser tests.
- **The plan's risks drove the checks.** A live scan of a receipt with a 10% service charge took the final total; a CNY receipt kept its currency; 14/10 was read day first.
- **It kept the binding rule.** It didn't change "blank fields are saved", which the human approved with `go`.
- **An honest report:** flaky model output on half the attempts until a retry was added, the credit left on the key, and phones can't reach the server as configured. Each was flagged as the owner's call.

## What went wrong

- **The driver built code itself.** OpenRouter credit ran out mid-slice 2 and the builder died. The next day, the GLM driver wrote the retry, the token cap and the fixes itself instead of resuming the builder; it did send the result for review.
- **`living-docs` was skipped at the finish again** (the second GLM run in a row). The builders had kept the docs current.
- **The plan stop was missed once.** Opus read `approve` before the human added `plan` and started building; it stopped cleanly when told.
- **Provider stalls** cost about 2.5 hours of wall-clock time.

## Changes made afterwards

- **`drive-feature`:**
  - resume or restart a dead slice, don't finish it yourself;
  - `living-docs` is its own step at the finish, "even if the docs look current".
- **`plan-feature` and `drive-feature`:** read `approve` from AGENTS.md at the stop.
- **README:** a Models section covering the three jobs, how to switch models at the plan stop, and the table of tested models.
