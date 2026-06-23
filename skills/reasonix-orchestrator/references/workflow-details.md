# Workflow Details

## Normal Flow

```text
User
  ->
Codex Desktop Brain
  ->
SPEC.md / ACCEPTANCE.md / REASONIX_HANDOFF.md
  ->
User confirmation inside Codex Desktop
  ->
.\scripts\ai-hand.ps1 "<task-slug>"
  ->
Reasonix CLI Hand
  ->
EXECUTION_REPORT.md
  ->
Codex Desktop Judge
  ->
PASS / REVISE / REJECT
```

## Role Meanings

### Brain

Brain means:

* understand request
* constrain scope
* write `SPEC.md`
* write `ACCEPTANCE.md`
* write `REASONIX_HANDOFF.md`
* ask user whether to proceed

### Hand

Hand means:

* read the task artifacts
* make the allowed code changes
* run validation commands when possible
* write `EXECUTION_REPORT.md`

### Judge

Judge means:

* read `EXECUTION_REPORT.md`
* read `git status`
* read `git diff`
* compare result against `SPEC.md` and `ACCEPTANCE.md`
* return `PASS`, `REVISE`, or `REJECT`

## Why This Skill Keeps Markdown Artifacts

Markdown artifacts stay useful because they are:

* reviewable in Codex Desktop
* diffable in Git
* portable across repos
* readable without extra tooling

## Legacy Components

These may exist in older repos, but are not normal control-plane components:

* `.ai/prompts/codex-brain.md`
* `.ai/prompts/codex-judge.md`
* `scripts/ai-brain.ps1`
* `scripts/ai-judge.ps1`
* `scripts/ai-chain.ps1`

Keep them marked as legacy or fallback when they remain in the repo.
