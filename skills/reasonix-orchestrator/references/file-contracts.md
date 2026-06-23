# File Contracts

## Primary Workflow Files

### `AGENTS.md`

Must define:

* Codex Desktop as the only normal Brain and Judge
* Reasonix CLI as Hand only
* `.\scripts\ai-hand.ps1 "<task-slug>"` as the Windows execution entrypoint
* `./scripts/ai-hand.sh "<task-slug>"` as the macOS / Linux execution entrypoint
* Codex Desktop selecting the matching script for the user's system
* `ai-chain.ps1` as legacy/fallback only
* no `codex` CLI for Brain/Judge
* safety rules against destructive or secret-touching actions

### `.ai/tasks/README.md`

Must explain:

* how a task starts in Codex Desktop
* which files get created under `.ai/tasks/<task-slug>/`
* when the user confirms
* how revise loops run

### `.ai/prompts/reasonix-hand.md`

Must tell Reasonix Hand:

* execute only
* no redesign
* no scope expansion
* no unrelated file changes
* no second user confirmation
* must write `EXECUTION_REPORT.md`

### `.reasonix/system-hand.md`

Acts as the stable system-level contract for Reasonix Hand.

Keep it aligned with `.ai/prompts/reasonix-hand.md`.

### `scripts/ai-hand.ps1`

Must:

* validate the task slug
* load `SPEC.md`
* load `ACCEPTANCE.md`
* load `REASONIX_HANDOFF.md`
* load `.ai/prompts/reasonix-hand.md`
* load `.reasonix/system-hand.md`
* call `reasonix`
* require `EXECUTION_REPORT.md` to exist before success

### `scripts/ai-hand.sh`

Must:

* validate the task slug
* load `SPEC.md`
* load `ACCEPTANCE.md`
* load `REASONIX_HANDOFF.md`
* load `.ai/prompts/reasonix-hand.md`
* load `.reasonix/system-hand.md`
* call `reasonix`
* require `EXECUTION_REPORT.md` to exist before success

## Optional / Legacy Files

Treat these as legacy unless the repo has a specific compatibility need:

* `.ai/prompts/codex-brain.md`
* `.ai/prompts/codex-judge.md`
* `scripts/ai-brain.ps1`
* `scripts/ai-judge.ps1`
* `scripts/ai-chain.ps1`

## TODO Cases

If a repo does not yet contain one of the required workflow files, document `TODO` instead of inventing hidden behavior.
