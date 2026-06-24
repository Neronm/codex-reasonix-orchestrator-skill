param(
    [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$validator = Join-Path $scriptDir "validate_skill.py"

python $validator --repo-root $RepoRoot --allow-missing-bash
exit $LASTEXITCODE
