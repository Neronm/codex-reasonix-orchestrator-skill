---
name: reasonix-orchestrator
description: Use when installing, updating, auditing, or packaging a repository workflow where Codex Desktop must stay the normal Brain and Judge, Reasonix CLI must stay the Hand, and the only normal execution entrypoint must be scripts/ai-hand.ps1. Trigger on requests about AGENTS.md, .ai/tasks, .ai/prompts, scripts/ai-hand.ps1, workflow extraction, or Codex plugin packaging for this orchestration pattern.
---

# Reasonix Orchestrator

## Overview

Use this skill to turn a repo's Codex Desktop plus Reasonix Hand workflow into a reusable, inspectable collaboration contract.

Keep the normal control plane fixed:

* Codex Desktop = normal Brain / Judge / Orchestrator
* Reasonix CLI = Hand / executor
* `.\scripts\ai-hand.ps1 "<task-slug>"` = only normal execution entrypoint
* `ai-chain.ps1` = legacy/fallback only
* `codex` CLI = not used for Brain/Judge in Codex Desktop Orchestrator mode

## Trigger Checklist

Use this skill when the repo needs any of these:

* install or refresh Codex Desktop Orchestrator workflow files
* extract current workflow into a reusable Codex skill
* package the repo as a Codex plugin with `.codex-plugin/plugin.json`
* audit whether Brain/Judge/Hand boundaries are still correct
* document how `AGENTS.md`, `.ai/tasks`, `.ai/prompts`, and `scripts/ai-hand.ps1` fit together

Do not use this skill for normal business-feature implementation.

## Workflow

1. Inspect workflow source files first.
2. Identify the current contract:
   * who acts as Brain
   * who acts as Judge
   * who acts as Hand
   * which command is the only normal execution entrypoint
3. Update collaboration files only:
   * skill files
   * docs
   * plugin packaging files
   * reusable scripts
4. Preserve safety boundaries:
   * no business-code edits unless the user explicitly asks for them outside this skill
   * no auto-commit
   * no auto-push
   * no destructive git cleanup
5. Validate the extracted skill and any bundled scripts.

## Required Files

Read these files when they exist:

* `AGENTS.md`
* `.ai/tasks/README.md`
* `.ai/prompts/reasonix-hand.md`
* `.reasonix/system-hand.md`
* `scripts/ai-hand.ps1`

Read these only as legacy/background if the repo still keeps them:

* `.ai/prompts/codex-brain.md`
* `.ai/prompts/codex-judge.md`
* `scripts/ai-brain.ps1`
* `scripts/ai-judge.ps1`
* `scripts/ai-chain.ps1`

For longer guidance, load:

* [references/workflow-details.md](references/workflow-details.md)
* [references/file-contracts.md](references/file-contracts.md)
* [references/reasonix-hand-contract.md](references/reasonix-hand-contract.md)
* [references/plugin-packaging.md](references/plugin-packaging.md)
* [references/test-checklist.md](references/test-checklist.md)

Use bundled script:

* [scripts/ai-hand.ps1](scripts/ai-hand.ps1)

## Safety Checks

Before claiming success, confirm all of these:

* Codex Desktop is still documented as the only normal Brain and Judge.
* Reasonix CLI is still documented as the Hand only.
* `.\scripts\ai-hand.ps1 "<task-slug>"` is still the only normal execution entrypoint.
* `ai-chain.ps1` is documented as legacy/fallback only.
* `codex` CLI is documented as not used for Brain/Judge in Desktop Orchestrator mode.
* user confirmations are documented as happening inside Codex Desktop
* no workflow doc tells the user to manually copy `REASONIX_HANDOFF.md`
* no generated doc tells the agent to auto-run `git push`, `git commit`, `git reset --hard`, `git clean`, file deletion, secret changes, or dependency install without approval

## Validation Commands

Run the skill validator:

```powershell
python -X utf8 <path-to-skill-creator>/quick_validate.py skills/reasonix-orchestrator
```

Run a PowerShell syntax check for the bundled hand script:

```powershell
$tokens = $null; $errors = $null; [void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path "skills/reasonix-orchestrator/scripts/ai-hand.ps1"), [ref]$tokens, [ref]$errors); if ($errors.Count -gt 0) { $errors | ForEach-Object { $_.ToString() }; exit 1 } else { Write-Host "PowerShell syntax OK" }
```

Optionally inspect workflow-only diff:

```powershell
git diff -- AGENTS.md .ai/tasks/README.md .ai/prompts/reasonix-hand.md .reasonix/system-hand.md scripts/ai-hand.ps1 skills/reasonix-orchestrator .codex-plugin/plugin.json README.md
```

## Common Mistakes

* Documenting `ai-chain.ps1` as normal path. Wrong.
* Letting `codex` CLI creep back into Brain/Judge. Wrong.
* Forgetting `.reasonix/system-hand.md` in the dependency chain.
* Mixing business-code changes into workflow extraction.
* Writing plugin docs that assume an exact Codex install command when the repo does not yet know the target distribution path. Mark `TODO` instead of guessing.
