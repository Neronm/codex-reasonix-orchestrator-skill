# Reasonix Hand Contract

Use this reference when updating the prompt or system contract for Reasonix Hand.

## Required Behavior

Reasonix Hand must be told:

* execute only
* do not redesign requirements
* do not expand scope
* do not change unrelated files
* do not ask the user for a second confirmation
* do not ask the user to manually copy `REASONIX_HANDOFF.md`
* read `SPEC.md`
* read `ACCEPTANCE.md`
* read `REASONIX_HANDOFF.md`
* write `EXECUTION_REPORT.md`

## Required Safety Rules

Reasonix Hand must not automatically:

* run `git push`
* run `git commit`
* run `git reset --hard`
* run `git clean`
* delete files
* modify `.env`
* modify secrets
* modify certificates
* modify SSH files
* modify credential files
* install dependencies without explicit approval

## Required Report Content

`EXECUTION_REPORT.md` should include at least:

* files changed
* validation commands and results
* incomplete items or blockers
* notes for Codex Desktop Judge
