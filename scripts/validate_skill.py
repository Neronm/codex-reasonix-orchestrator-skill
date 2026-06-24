#!/usr/bin/env python3
"""
Unified repository validator for the Reasonix Orchestrator skill package.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from skill_validator import validate_skill as validate_skill_frontmatter


@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str


@dataclass
class ValidationReport:
    results: list[CheckResult]

    def render(self) -> str:
        return "\n".join(
            f"{'PASS' if result.passed else 'FAIL'}: {result.name} - {result.message}" for result in self.results
        )

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)


REQUIRED_FILES = [
    Path("README.md"),
    Path(".codex-plugin/plugin.json"),
    Path("scripts/skill_validator.py"),
    Path("scripts/validate_skill.py"),
    Path("scripts/validate-skill.ps1"),
    Path("scripts/validate-skill.sh"),
    Path(".github/workflows/validate-skill.yml"),
    Path("skills/reasonix-orchestrator/SKILL.md"),
    Path("skills/reasonix-orchestrator/scripts/ai-hand.ps1"),
    Path("skills/reasonix-orchestrator/scripts/ai-hand.sh"),
    Path("skills/reasonix-orchestrator/references/file-contracts.md"),
    Path("skills/reasonix-orchestrator/references/reasonix-hand-contract.md"),
    Path("skills/reasonix-orchestrator/references/test-checklist.md"),
    Path("skills/reasonix-orchestrator/references/workflow-details.md"),
    Path("skills/reasonix-orchestrator/agents/openai.yaml"),
]

DOC_FILES = [
    Path("README.md"),
    Path("skills/reasonix-orchestrator/SKILL.md"),
    Path("skills/reasonix-orchestrator/references/file-contracts.md"),
    Path("skills/reasonix-orchestrator/references/reasonix-hand-contract.md"),
    Path("skills/reasonix-orchestrator/references/test-checklist.md"),
    Path("skills/reasonix-orchestrator/references/workflow-details.md"),
]

ENTRYPOINT_DOC_FILES = [
    Path("README.md"),
    Path("skills/reasonix-orchestrator/SKILL.md"),
    Path("skills/reasonix-orchestrator/references/file-contracts.md"),
    Path("skills/reasonix-orchestrator/references/test-checklist.md"),
    Path("skills/reasonix-orchestrator/references/workflow-details.md"),
]

WINDOWS_ENTRYPOINT = r'.\scripts\ai-hand.ps1 "<task-slug>"'
UNIX_ENTRYPOINT = './scripts/ai-hand.sh "<task-slug>"'
PROHIBITED_PLACEHOLDER = "<path-to-skill-creator>"
FORBIDDEN_OPERATIONS = [
    "git push",
    "git commit",
    "git reset --hard",
    "git clean",
]


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_python() -> str:
    for candidate in ("python", "python3"):
        try:
            subprocess.run([candidate, "--version"], check=True, capture_output=True)
            return candidate
        except (OSError, subprocess.CalledProcessError):
            continue
    raise RuntimeError("Python executable not found in PATH.")


def run_command(args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, capture_output=True)


def decode_output(proc: subprocess.CompletedProcess[bytes]) -> str:
    chunks = [proc.stdout or b"", proc.stderr or b""]
    decoded: list[str] = []
    for chunk in chunks:
        if not chunk:
            continue
        for encoding in ("utf-8", sys.getfilesystemencoding(), "gbk", "cp936", "latin-1"):
            try:
                decoded.append(chunk.decode(encoding))
                break
            except UnicodeDecodeError:
                continue
        else:
            decoded.append(chunk.decode("utf-8", errors="replace"))
    return "\n".join(part.strip() for part in decoded if part.strip()).strip()


def find_powershell() -> str | None:
    for candidate in ("pwsh", "powershell"):
        try:
            subprocess.run([candidate, "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"], check=True, capture_output=True)
            return candidate
        except (OSError, subprocess.CalledProcessError):
            continue
    return None


def bash_available() -> bool:
    try:
        proc = run_command(["bash", "--version"])
    except OSError:
        return False
    if proc.returncode != 0:
        return False
    version_text = decode_output(proc)
    return "GNU bash" in version_text or "bash" in version_text.lower()


def run_check(name: str, predicate: bool, success: str, failure: str) -> CheckResult:
    return CheckResult(name=name, passed=predicate, message=success if predicate else failure)


def check_required_files(repo_root: Path) -> CheckResult:
    missing = [str(path) for path in REQUIRED_FILES if not (repo_root / path).exists()]
    return run_check(
        "required-files",
        not missing,
        "All required package files exist.",
        f"Missing required files: {', '.join(missing)}",
    )


def check_skill_frontmatter(repo_root: Path) -> CheckResult:
    valid, message = validate_skill_frontmatter(repo_root / "skills/reasonix-orchestrator")
    return CheckResult("skill-validator", valid, message)


def check_manifest_required_fields(repo_root: Path) -> CheckResult:
    manifest = json.loads((repo_root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    required_paths = [
        ("name",),
        ("version",),
        ("description",),
        ("author", "name"),
        ("license",),
        ("skills",),
        ("interface", "displayName"),
        ("interface", "shortDescription"),
        ("interface", "longDescription"),
        ("interface", "developerName"),
        ("interface", "category"),
        ("interface", "capabilities"),
        ("interface", "defaultPrompt"),
    ]
    missing: list[str] = []
    for path in required_paths:
        cursor = manifest
        for key in path:
            if not isinstance(cursor, dict) or key not in cursor:
                missing.append(".".join(path))
                break
            cursor = cursor[key]
    return run_check(
        "manifest-required-fields",
        not missing,
        "plugin.json contains all required fields.",
        f"plugin.json is missing: {', '.join(missing)}",
    )


def check_manifest_role_boundary(repo_root: Path) -> CheckResult:
    manifest = json.loads((repo_root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    long_description = manifest["interface"]["longDescription"]
    passed = "Codex Desktop" in long_description and "Brain" in long_description and "Judge" in long_description and "Reasonix CLI" in long_description and "Hand" in long_description
    return run_check(
        "manifest-role-boundary",
        passed,
        "plugin.json longDescription preserves Codex Desktop and Reasonix CLI boundaries.",
        "plugin.json longDescription must mention Codex Desktop as Brain/Judge and Reasonix CLI as Hand.",
    )


def check_powershell_syntax(repo_root: Path) -> CheckResult:
    shell = find_powershell()
    if shell is None:
        return CheckResult("powershell-syntax", False, "PowerShell executable not found.")
    script_path = repo_root / "skills/reasonix-orchestrator/scripts/ai-hand.ps1"
    command = (
        "$tokens = $null; "
        "$errors = $null; "
        f"[void][System.Management.Automation.Language.Parser]::ParseFile('{script_path.as_posix()}', [ref]$tokens, [ref]$errors); "
        "if ($errors.Count -gt 0) { $errors | ForEach-Object { $_.ToString() }; exit 1 } else { Write-Host 'PowerShell syntax OK' }"
    )
    proc = run_command([shell, "-NoProfile", "-Command", command])
    if proc.returncode == 0:
        output = decode_output(proc)
        return CheckResult("powershell-syntax", True, output or "PowerShell syntax OK")
    output = decode_output(proc)
    return CheckResult("powershell-syntax", False, output or "PowerShell syntax check failed.")


def check_bash_syntax(repo_root: Path, require_bash: bool) -> CheckResult:
    script_path = repo_root / "skills/reasonix-orchestrator/scripts/ai-hand.sh"
    if not require_bash and not bash_available():
        return CheckResult("bash-syntax", True, "Bash syntax check skipped: bash is not required on this platform.")
    if not bash_available():
        return CheckResult("bash-syntax", False, "bash is required but not available in PATH.")
    proc = run_command(["bash", "-n", str(script_path)])
    if proc.returncode == 0:
        return CheckResult("bash-syntax", True, "bash -n passed for skills/reasonix-orchestrator/scripts/ai-hand.sh")
    output = decode_output(proc)
    return CheckResult("bash-syntax", False, output or "bash -n failed.")


def check_placeholder_paths(repo_root: Path) -> CheckResult:
    offenders: list[str] = []
    for path in DOC_FILES:
        text = load_text(repo_root / path)
        if f"{PROHIBITED_PLACEHOLDER}/quick_validate.py" in text or f"{PROHIBITED_PLACEHOLDER}>/quick_validate.py" in text:
            offenders.append(str(path))
    return run_check(
        "docs-no-placeholder-validator-path",
        not offenders,
        "Documentation contains no placeholder validator paths.",
        f"Placeholder validator path found in: {', '.join(offenders)}",
    )


def check_entrypoints(repo_root: Path) -> CheckResult:
    missing: list[str] = []
    for path in ENTRYPOINT_DOC_FILES:
        text = load_text(repo_root / path)
        if WINDOWS_ENTRYPOINT not in text or UNIX_ENTRYPOINT not in text:
            missing.append(str(path))
    return run_check(
        "docs-entrypoints",
        not missing,
        "All key docs reference the exact Windows and macOS/Linux entrypoints.",
        f"Entrypoint strings missing or drifted in: {', '.join(missing)}",
    )


def check_role_boundaries(repo_root: Path) -> CheckResult:
    files = [
        Path("README.md"),
        Path("skills/reasonix-orchestrator/SKILL.md"),
        Path("skills/reasonix-orchestrator/references/workflow-details.md"),
    ]
    failures: list[str] = []
    for path in files:
        text = load_text(repo_root / path)
        if "Codex Desktop" not in text or ("Brain" not in text and "Judge" not in text):
            failures.append(str(path))
            continue
        if "Reasonix CLI" not in text or "Hand" not in text:
            failures.append(str(path))
    return run_check(
        "docs-role-boundaries",
        not failures,
        "Core docs preserve Codex Desktop Brain/Judge and Reasonix CLI Hand boundaries.",
        f"Role boundary text missing in: {', '.join(failures)}",
    )


def check_ai_chain_legacy(repo_root: Path) -> CheckResult:
    offenders: list[str] = []
    for path in DOC_FILES:
        text = load_text(repo_root / path)
        lowered = text.lower()
        if "ai-chain.ps1" in text and "presented as normal path" not in lowered and "legacy" not in lowered and "fallback" not in lowered:
            offenders.append(str(path))
    return run_check(
        "docs-ai-chain-legacy",
        not offenders,
        "Every ai-chain.ps1 mention is marked legacy/fallback.",
        f"ai-chain.ps1 appears without legacy/fallback wording in: {', '.join(offenders)}",
    )


def check_codex_cli_boundary(repo_root: Path) -> CheckResult:
    files = [
        Path("README.md"),
        Path("skills/reasonix-orchestrator/SKILL.md"),
        Path("skills/reasonix-orchestrator/references/workflow-details.md"),
    ]
    offenders: list[str] = []
    for path in files:
        text = load_text(repo_root / path)
        if "codex" not in text.lower():
            offenders.append(str(path))
            continue
        lowered = text.lower()
        if "not used for brain/judge" not in lowered and "stays out of brain / judge" not in lowered and "does not use `codex` cli as `brain / judge`" not in lowered:
            offenders.append(str(path))
    return run_check(
        "docs-codex-cli-boundary",
        not offenders,
        "Core docs explicitly keep codex CLI out of Brain/Judge duties.",
        f"codex CLI boundary wording missing in: {', '.join(offenders)}",
    )


def check_no_manual_handoff_copy(repo_root: Path) -> CheckResult:
    text = load_text(repo_root / Path("skills/reasonix-orchestrator/references/reasonix-hand-contract.md"))
    passed = "do not ask the user to manually copy `REASONIX_HANDOFF.md`" in text
    return run_check(
        "docs-no-manual-handoff-copy",
        passed,
        "Reasonix hand contract forbids manual REASONIX_HANDOFF.md copy requests.",
        "Reasonix hand contract must explicitly forbid manual REASONIX_HANDOFF.md copy requests.",
    )


def check_safety_boundaries(repo_root: Path) -> CheckResult:
    files = [
        Path("README.md"),
        Path("skills/reasonix-orchestrator/SKILL.md"),
        Path("skills/reasonix-orchestrator/references/reasonix-hand-contract.md"),
    ]
    missing: list[str] = []
    for path in files:
        text = load_text(repo_root / path)
        for operation in FORBIDDEN_OPERATIONS:
            if operation not in text:
                missing.append(f"{path}:{operation}")
        if "install dependencies without explicit approval" not in text and "dependency install without approval" not in text:
            missing.append(f"{path}:dependency-install-approval")
    return run_check(
        "docs-safety-boundaries",
        not missing,
        "Safety boundaries are documented consistently across core docs.",
        f"Missing safety boundary text: {', '.join(missing)}",
    )


def check_validation_commands(repo_root: Path) -> CheckResult:
    files = [
        Path("README.md"),
        Path("skills/reasonix-orchestrator/SKILL.md"),
        Path("skills/reasonix-orchestrator/references/test-checklist.md"),
    ]
    missing: list[str] = []
    for path in files:
        text = load_text(repo_root / path)
        if "validate-skill.ps1" not in text or "validate-skill.sh" not in text:
            missing.append(str(path))
    return run_check(
        "docs-validation-commands",
        not missing,
        "User-facing docs reference the repository validation entrypoints.",
        f"Validation entrypoints missing in: {', '.join(missing)}",
    )


def check_openai_agent_metadata(repo_root: Path) -> CheckResult:
    readme = load_text(repo_root / Path("README.md"))
    yaml_text = load_text(repo_root / Path("skills/reasonix-orchestrator/agents/openai.yaml"))
    passed = "agents/openai.yaml" in readme and "default prompt" in readme.lower() and "default_prompt" in yaml_text
    return run_check(
        "agent-metadata-documented",
        passed,
        "README documents the purpose of skills/reasonix-orchestrator/agents/openai.yaml.",
        "README must explain why skills/reasonix-orchestrator/agents/openai.yaml exists.",
    )


def check_ci_workflow(repo_root: Path) -> CheckResult:
    text = load_text(repo_root / Path(".github/workflows/validate-skill.yml"))
    required_strings = [
        "windows-latest",
        "ubuntu-latest",
        "scripts/validate-skill.ps1",
        "scripts/validate-skill.sh",
        "chmod +x scripts/validate-skill.sh",
        "chmod +x skills/reasonix-orchestrator/scripts/ai-hand.sh",
    ]
    missing = [needle for needle in required_strings if needle not in text]
    return run_check(
        "ci-cross-platform",
        not missing,
        "CI workflow validates the package on Windows and Ubuntu.",
        f"CI workflow is missing: {', '.join(missing)}",
    )


def validate_repository(repo_root: str | Path, require_bash: bool = False) -> ValidationReport:
    root = Path(repo_root).resolve()
    results = [
        check_required_files(root),
        check_skill_frontmatter(root),
        check_manifest_required_fields(root),
        check_manifest_role_boundary(root),
        check_powershell_syntax(root),
        check_bash_syntax(root, require_bash=require_bash),
        check_placeholder_paths(root),
        check_entrypoints(root),
        check_role_boundaries(root),
        check_ai_chain_legacy(root),
        check_codex_cli_boundary(root),
        check_no_manual_handoff_copy(root),
        check_safety_boundaries(root),
        check_validation_commands(root),
        check_openai_agent_metadata(root),
        check_ci_workflow(root),
    ]
    return ValidationReport(results)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--require-bash", action="store_true")
    parser.add_argument("--allow-missing-bash", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    require_bash = args.require_bash
    if args.allow_missing_bash:
        require_bash = False
    report = validate_repository(args.repo_root, require_bash=require_bash)
    print(report.render())
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
