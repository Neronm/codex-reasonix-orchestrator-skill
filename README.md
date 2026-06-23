# Reasonix Orchestrator

让 `Codex Desktop` 负责规划与验收，让 `Reasonix CLI` 负责真实代码执行的可复用 Codex Skill / Plugin。  
A reusable Codex Skill / Plugin that lets `Codex Desktop` handle planning and review while `Reasonix CLI` performs real code execution.

这个仓库适合想把 AI 协作链路固定成下面模式的开发者。  
This repository is for developers who want a stable AI collaboration workflow with clear role boundaries.

* `Codex Desktop` 负责正常的 `Brain / Judge / Orchestrator`
* `Codex Desktop` is the normal `Brain / Judge / Orchestrator`
* `Reasonix CLI` 负责正常的 `Hand / Executor`
* `Reasonix CLI` is the normal `Hand / Executor`
* 正常执行入口只有：
* The only normal execution entrypoint is:

```powershell
.\scripts\ai-hand.ps1 "<task-slug>"
```

* 不使用 `ai-chain.ps1` 作为正常入口
* `ai-chain.ps1` is not used as the normal entrypoint
* 不使用 `codex` CLI 做正常的 `Brain / Judge`
* `codex` CLI is not used for the normal `Brain / Judge`

## 这是什么 / What This Is

这是一个可复用工作流仓库，核心目的是把 `Codex Desktop + Reasonix CLI` 的协作方式产品化、文档化、可安装化。  
This is a reusable workflow repository that packages the `Codex Desktop + Reasonix CLI` collaboration model into something installable, inspectable, and reusable.

安装后，你可以在自己的项目里使用同样的协作链路：  
After installation, you can use the same workflow in your own project:

* 在 `Codex Desktop` 中提出需求
* Ask for changes in `Codex Desktop`
* 由 `Codex Desktop` 生成 `SPEC.md / ACCEPTANCE.md / REASONIX_HANDOFF.md`
* Let `Codex Desktop` generate `SPEC.md / ACCEPTANCE.md / REASONIX_HANDOFF.md`
* 由 `Codex Desktop` 在对话里向你确认是否执行
* Let `Codex Desktop` ask for confirmation in the conversation
* 确认后，调用 `Reasonix CLI` 执行真实代码修改
* After confirmation, call `Reasonix CLI` for real code changes
* 最后仍由 `Codex Desktop` 读取结果并给出 `PASS / REVISE / REJECT`
* Finally, let `Codex Desktop` read the results and return `PASS / REVISE / REJECT`

## 适合什么场景 / Best Fit

适合：  
Best fit:

* 希望规划、范围控制、验收判断都在 `Codex Desktop` 里完成
* You want planning, scoping, and acceptance decisions to stay in `Codex Desktop`
* 希望真正改代码的是 `Reasonix CLI`
* You want `Reasonix CLI` to perform the real code edits
* 希望任务交接通过 Markdown 文件显式落盘
* You want explicit Markdown handoff artifacts
* 希望执行入口固定、可审计、可 smoke-test
* You want a fixed, auditable, smoke-testable execution path
* 希望把同一套工作流复用到多个项目
* You want to reuse the same workflow across multiple repositories

不适合：  
Not a good fit:

* 直接把 AI 当成无约束自动改代码工具
* You want unconstrained autonomous code editing
* 需要 `codex` CLI 直接承担 Brain / Judge 的流程
* You need `codex` CLI to act as Brain / Judge
* 不希望引入显式任务工件
* You do not want explicit task artifacts

## 分工模型 / Role Split

### Codex Desktop

`Codex Desktop` 是唯一正常的：  
`Codex Desktop` is the only normal:

* `Brain`
* `Judge`
* `Orchestrator`

它负责：  
It is responsible for:

* 理解需求
* understanding the request
* 约束范围
* constraining scope
* 生成任务工件
* generating task artifacts
* 在桌面对话中向用户确认
* asking for confirmation in the desktop conversation
* 读取执行结果
* reading execution results
* 输出最终判断
* returning the final judgment

### Reasonix CLI

`Reasonix CLI` 是唯一正常的：  
`Reasonix CLI` is the only normal:

* `Hand`
* `Executor`

它负责：  
It is responsible for:

* 读取 `SPEC.md`
* reading `SPEC.md`
* 读取 `ACCEPTANCE.md`
* reading `ACCEPTANCE.md`
* 读取 `REASONIX_HANDOFF.md`
* reading `REASONIX_HANDOFF.md`
* 进行允许范围内的真实代码修改
* making real code changes within the allowed scope
* 运行验证命令
* running validation commands
* 写出 `EXECUTION_REPORT.md`
* writing `EXECUTION_REPORT.md`

## 工作流图 / Workflow Diagram

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

## 安装前提 / Prerequisites

使用前建议具备：  
Recommended prerequisites:

* `Codex Desktop`
* `Reasonix CLI`
* `Git`
* `PowerShell`

可选：  
Optional:

* `Codex CLI`

说明：这个仓库支持作为 skill 被发现和引用，但正常工作流里不使用 `codex` CLI 充当 Brain / Judge。  
Note: this repository can be discovered and invoked as a skill, but the normal workflow does not use `codex` CLI as Brain / Judge.

## 仓库内容 / Repository Layout

```text
skills/
  reasonix-orchestrator/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
.codex-plugin/
  plugin.json
LICENSE
README.md
```

## 如何安装到目标项目 / Install Into a Target Project

### 作为 Skill 安装 / Install as a Skill

把 `skills/reasonix-orchestrator/` 放进你的 Codex skills 目录。  
Place `skills/reasonix-orchestrator/` into your Codex skills directory.

常见目标位置：  
Common target location:

```text
$CODEX_HOME/skills/reasonix-orchestrator/
```

如果没有自定义 `CODEX_HOME`，也常见放到：  
If you do not use a custom `CODEX_HOME`, a common location is:

```text
~/.codex/skills/reasonix-orchestrator/
```

### 作为 Plugin 使用 / Use as a Plugin

仓库已提供：  
This repository already includes:

```text
.codex-plugin/plugin.json
```

这让仓库可以进一步作为 Codex Plugin 分发基础来使用。  
This makes the repository suitable for later Codex Plugin distribution and packaging.

`TODO`：如果你打算通过 GitHub 或其他分发方式发布插件，需要按目标环境补充实际安装命令和发布地址。  
`TODO`: if you plan to distribute this through GitHub or another channel, add the real install command and published repository URL for your target environment.

## 如何使用 / How To Use

### 在 Codex Desktop 中使用 / Use in Codex Desktop

```text
请使用 $reasonix-orchestrator，检查当前仓库的 Orchestrator 工作流是否仍然满足：
- Codex Desktop = Brain / Judge
- Reasonix CLI = Hand
- 唯一正常执行入口 = .\scripts\ai-hand.ps1 "<task-slug>"
```

```text
Use $reasonix-orchestrator to verify that the repository still follows this workflow:
- Codex Desktop = Brain / Judge
- Reasonix CLI = Hand
- The only normal execution entrypoint = .\scripts\ai-hand.ps1 "<task-slug>"
```

### 在 Codex CLI 中使用 / Use in Codex CLI

```text
Use $reasonix-orchestrator to audit the workflow files in this repository.
```

## 请求模板 / Request Template

在 `Codex Desktop` 中，建议用户这样提需求：  
In `Codex Desktop`, a good request template is:

```text
按 Codex Desktop Orchestrator 模式处理。

任务名：example-task

需求：
实现一个小范围、可验证的改动。

范围：
只改完成任务所必需的文件。

不要改：
不要改无关模块，不要改 .env，不要改密钥文件。

验收：
相关验证通过，且没有无关文件变更。

请先作为 Brain 生成 SPEC / ACCEPTANCE / REASONIX_HANDOFF，展示摘要后问我是否确认交给 Reasonix 执行。
```

```text
Handle this in Codex Desktop Orchestrator mode.

Task name: example-task

Request:
Implement one small, verifiable change.

Scope:
Only edit the files required to complete the task.

Do not modify:
Do not modify unrelated modules, .env files, or secret files.

Acceptance:
Relevant validation passes and no unrelated files change.

First act as Brain and generate SPEC / ACCEPTANCE / REASONIX_HANDOFF, then show a summary and ask whether to hand it off to Reasonix.
```

## 安全边界 / Safety Boundary

这个工作流明确禁止自动进行以下操作：  
This workflow explicitly forbids automatically doing any of the following:

* `git push`
* `git commit`
* `git reset --hard`
* `git clean`
* 删除文件
* deleting files
* 修改 `.env`
* modifying `.env`
* 修改密钥、证书、SSH、凭据文件
* modifying secret, certificate, SSH, or credential files
* 未经明确批准自动安装依赖
* installing dependencies without explicit approval

同时还要确保：  
It must also ensure:

* 所有用户确认都在 `Codex Desktop` 内完成
* all user confirmations happen inside `Codex Desktop`
* 不要求用户去 `Reasonix` 里二次确认
* the user is not asked to confirm again inside `Reasonix`
* 不要求用户手动复制 `REASONIX_HANDOFF.md`
* the user is not asked to manually copy `REASONIX_HANDOFF.md`

## Smoke Test

建议安装后做一轮最小 smoke-test：  
Recommended minimum smoke test after installation:

1. 运行 skill 校验 / Run skill validation:

```powershell
python -X utf8 <path-to-skill-creator>/quick_validate.py skills/reasonix-orchestrator
```

2. 校验 bundled PowerShell 脚本语法 / Validate bundled PowerShell script syntax:

```powershell
$tokens = $null; $errors = $null; [void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path "skills/reasonix-orchestrator/scripts/ai-hand.ps1"), [ref]$tokens, [ref]$errors); if ($errors.Count -gt 0) { $errors | ForEach-Object { $_.ToString() }; exit 1 } else { Write-Host "PowerShell syntax OK" }
```

3. 在 `Codex Desktop` 发起一个假任务 / Start a fake task in `Codex Desktop`
4. 确认 `Codex Desktop` 先生成工件 / Confirm `Codex Desktop` generates artifacts first:
   * `SPEC.md`
   * `ACCEPTANCE.md`
   * `REASONIX_HANDOFF.md`
5. 确认 `Codex Desktop` 先问你是否执行 / Confirm `Codex Desktop` asks for confirmation first
6. 确认正常入口仍然是 / Confirm the normal entrypoint is still:

```powershell
.\scripts\ai-hand.ps1 "<task-slug>"
```

7. 确认 `Reasonix CLI` 写出 / Confirm `Reasonix CLI` writes:

```text
.ai/tasks/<task-slug>/EXECUTION_REPORT.md
```

8. 确认 `Codex Desktop` 最终读取 / Confirm `Codex Desktop` finally reads:
   * `EXECUTION_REPORT.md`
   * `git status`
   * `git diff`

更完整清单见：  
For the fuller checklist, see:

* [skills/reasonix-orchestrator/references/test-checklist.md](skills/reasonix-orchestrator/references/test-checklist.md)

## 常见问题入口 / FAQ

### 1. 这个 skill 会不会改业务代码？ / Will this skill modify business code?

不会。这个 skill 的目标是安装、更新、审计、打包工作流本身，不是替你实现业务需求。  
No. This skill is for installing, updating, auditing, and packaging the workflow itself, not for implementing business features.

### 2. `ai-chain.ps1` 还能不能用？ / Can `ai-chain.ps1` still be used?

可以保留，但它不是正常入口，只是 `legacy / fallback`。  
It can remain in the repo, but it is not the normal entrypoint. It is only `legacy / fallback`.

### 3. 为什么不用 `codex` CLI 做 Brain / Judge？ / Why not use `codex` CLI for Brain / Judge?

因为这个模式明确要求正常 Brain / Judge 都由 `Codex Desktop` 承担，避免控制面分裂。  
Because this workflow explicitly requires normal Brain / Judge responsibilities to stay in `Codex Desktop`, avoiding a split control plane.

### 4. 如果目标项目缺文件怎么办？ / What if the target project is missing files?

在文档里写 `TODO`，不要猜。  
Write `TODO` in the docs instead of guessing.

### 5. 更多说明在哪里？ / Where can I find more detail?

* [工作流说明 / Workflow details](skills/reasonix-orchestrator/references/workflow-details.md)
* [文件契约 / File contracts](skills/reasonix-orchestrator/references/file-contracts.md)
* [Reasonix Hand 契约 / Reasonix Hand contract](skills/reasonix-orchestrator/references/reasonix-hand-contract.md)
* [插件打包说明 / Plugin packaging notes](skills/reasonix-orchestrator/references/plugin-packaging.md)
* [测试清单 / Test checklist](skills/reasonix-orchestrator/references/test-checklist.md)
