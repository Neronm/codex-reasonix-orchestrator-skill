# Minimal Test Checklist

Use this after someone installs the skill into another repo.

## Repository Layout

Confirm these exist:

* `AGENTS.md`
* `.ai/tasks/README.md`
* `.ai/prompts/reasonix-hand.md`
* `.reasonix/system-hand.md`
* `scripts/ai-hand.ps1`
* `scripts/ai-hand.sh`
* `skills/reasonix-orchestrator/SKILL.md`
* `.codex-plugin/plugin.json`

## Skill Validation

Run:

```powershell
python -X utf8 <path-to-skill-creator>/quick_validate.py skills/reasonix-orchestrator
```

Expect:

* validator exits successfully

## Bundled Script Validation

Run:

```powershell
$tokens = $null; $errors = $null; [void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path "skills/reasonix-orchestrator/scripts/ai-hand.ps1"), [ref]$tokens, [ref]$errors); if ($errors.Count -gt 0) { $errors | ForEach-Object { $_.ToString() }; exit 1 } else { Write-Host "PowerShell syntax OK" }
```

Expect:

* `PowerShell syntax OK`

Run:

```bash
bash -n skills/reasonix-orchestrator/scripts/ai-hand.sh
```

Expect:

* command exits successfully

## Workflow Smoke Test

1. Ask Codex Desktop to process a fake task in Orchestrator mode.
2. Confirm Codex Desktop creates:
   * `.ai/tasks/<task-slug>/SPEC.md`
   * `.ai/tasks/<task-slug>/ACCEPTANCE.md`
   * `.ai/tasks/<task-slug>/REASONIX_HANDOFF.md`
3. Confirm Codex Desktop asks for confirmation before calling Reasonix.
4. Confirm the normal command matches the target OS:

```powershell
.\scripts\ai-hand.ps1 "<task-slug>"
```

```bash
./scripts/ai-hand.sh "<task-slug>"
```

5. Confirm Reasonix writes:

```text
.ai/tasks/<task-slug>/EXECUTION_REPORT.md
```

6. Confirm Codex Desktop reviews `EXECUTION_REPORT.md`, `git status`, and `git diff`.

## Failure Signals

Treat these as failures:

* `ai-chain.ps1` presented as normal path
* `codex` CLI used for Brain or Judge
* user asked to confirm inside Reasonix
* user asked to manually copy `REASONIX_HANDOFF.md`
* `EXECUTION_REPORT.md` missing after a claimed successful hand run
* macOS / Linux flow documented without `chmod +x scripts/ai-hand.sh` on first use
