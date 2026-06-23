param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$TaskSlug
)

$ErrorActionPreference = "Stop"

Write-Host "Codex Desktop Orchestrator mode: invoking Reasonix Hand only."
Write-Host "Expected caller: Codex Desktop after user confirmation."

function Get-ProjectRoot {
    return (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}

function Assert-SafeTaskSlug {
    param([string]$Slug)

    if ($Slug -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$') {
        throw "Invalid task slug. Use 1-80 chars: letters, numbers, dot, underscore, hyphen."
    }
}

function Test-CommandAvailable {
    param([string]$Name)

    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Get-CommandText {
    param([scriptblock]$Command)

    try {
        $output = & $Command 2>&1
        return [string]::Join([Environment]::NewLine, @($output))
    }
    catch {
        return $_.Exception.Message
    }
}

function Resolve-ReasonixInvocation {
    if (-not (Test-CommandAvailable "reasonix")) {
        throw "reasonix CLI not found in PATH."
    }

    $version = Get-CommandText { reasonix --version }
    if ($LASTEXITCODE -ne 0 -or -not $version.Trim()) {
        $version = Get-CommandText { reasonix --help }
    }

    $help = Get-CommandText { reasonix --help }
    if ($help -match '(?m)^\s*reasonix\s+run\s+') {
        return @{ Command = "run"; Version = $version.Trim(); Help = $help }
    }
    if ($help -match '(?m)^\s*reasonix\s+code\s+') {
        return @{ Command = "code"; Version = $version.Trim(); Help = $help }
    }
    if ($help -match '(?m)^\s*reasonix\s+exec\s+') {
        return @{ Command = "exec"; Version = $version.Trim(); Help = $help }
    }

    throw "reasonix CLI found, but no supported execution command detected. Expected run, code, or exec."
}

function Invoke-ReasonixTask {
    param(
        [string]$Prompt,
        [string]$ProjectRoot
    )

    $reasonixInfo = Resolve-ReasonixInvocation

    switch ($reasonixInfo.Command) {
        "run" { $args = @("run", "--dir", $ProjectRoot, $Prompt) }
        "code" { $args = @("code", "--dir", $ProjectRoot, $Prompt) }
        "exec" { $args = @("exec", "--dir", $ProjectRoot, $Prompt) }
        default { throw "Unsupported reasonix command: $($reasonixInfo.Command)" }
    }

    & reasonix @args
    if ($LASTEXITCODE -ne 0) {
        throw "reasonix $($reasonixInfo.Command) failed with exit code $LASTEXITCODE."
    }
}

$projectRoot = Get-ProjectRoot
Assert-SafeTaskSlug $TaskSlug

$taskDir = Join-Path $projectRoot ".ai/tasks/$TaskSlug"
if (-not (Test-Path $taskDir)) {
    throw "Task directory not found: $taskDir"
}

$specPath = Join-Path $taskDir "SPEC.md"
$acceptancePath = Join-Path $taskDir "ACCEPTANCE.md"
$handoffPath = Join-Path $taskDir "REASONIX_HANDOFF.md"
$reportPath = Join-Path $taskDir "EXECUTION_REPORT.md"
$promptPath = Join-Path $projectRoot ".ai/prompts/reasonix-hand.md"
$systemPath = Join-Path $projectRoot ".reasonix/system-hand.md"

foreach ($path in @($specPath, $acceptancePath, $handoffPath, $promptPath, $systemPath)) {
    if (-not (Test-Path $path)) {
        throw "Required file missing: $path"
    }
}

$promptTemplate = Get-Content -Raw $promptPath
$systemHand = Get-Content -Raw $systemPath
$spec = Get-Content -Raw $specPath
$acceptance = Get-Content -Raw $acceptancePath
$handoff = Get-Content -Raw $handoffPath

$prompt = @(
    $systemHand
    ""
    $promptTemplate
    ""
    "Project root:"
    $projectRoot
    ""
    "Task directory:"
    $taskDir
    ""
    "Required execution report path:"
    $reportPath
    ""
    "SPEC.md:"
    $spec
    ""
    "ACCEPTANCE.md:"
    $acceptance
    ""
    "REASONIX_HANDOFF.md:"
    $handoff
    ""
    "Execute now. Act only as Reasonix Hand. Do not redesign requirements. Do not ask the user for more confirmation. Write EXECUTION_REPORT.md when finished."
) -join [Environment]::NewLine

Invoke-ReasonixTask -Prompt $prompt -ProjectRoot $projectRoot

if (-not (Test-Path $reportPath)) {
    throw "Reasonix Hand did not create required file: $reportPath"
}

Write-Host "Reasonix Hand report written to $reportPath"
