# Validation Checklist

Use this to verify the skill/package repository itself before release.

## Automated Package Validation

Run the repository validation entrypoints:

```powershell
.\scripts\validate-skill.ps1
```

```bash
./scripts/validate-skill.sh
```

The raw Python entrypoint is:

```powershell
python scripts/validate_skill.py --repo-root .
```

On Windows without a working Bash environment, use `.\scripts\validate-skill.ps1` locally and let Ubuntu CI cover the Bash syntax gate.

Expect:

* every check prints `PASS: <check-name>`
* exit code `0`
* no placeholder validator path like `<path-to-skill-creator>`
* exact entrypoints remain:
  * `.\scripts\ai-hand.ps1 "<task-slug>"`
  * `./scripts/ai-hand.sh "<task-slug>"`

## Required Repository Files

Confirm these exist:

* `scripts/skill_validator.py`
* `scripts/validate_skill.py`
* `scripts/validate-skill.ps1`
* `scripts/validate-skill.sh`
* `.github/workflows/validate-skill.yml`
* `AGENTS.md`
* `.ai/tasks/README.md`
* `.ai/prompts/reasonix-hand.md`
* `.reasonix/system-hand.md`
* `scripts/ai-hand.ps1`
* `scripts/ai-hand.sh`
* `skills/reasonix-orchestrator/SKILL.md`
* `.codex-plugin/plugin.json`

## Manual Smoke Test For Target Repos

Run this only when you are validating a real target repository that installed the skill.

1. Ask Codex Desktop to process a fake task in Desktop Orchestrator mode.
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
* docs missing any of: `git push`, `git commit`, `git reset --hard`, `git clean`, or "install dependencies without explicit approval"
