# Reasonix Orchestrator

Reusable skill/package for a fixed `Codex Desktop + Reasonix CLI` workflow.

- `Codex Desktop` = normal `Brain / Judge / Orchestrator`
- `Reasonix CLI` = normal `Hand / Executor`
- Windows entrypoint = `.\scripts\ai-hand.ps1 "<task-slug>"`
- macOS / Linux entrypoint = `./scripts/ai-hand.sh "<task-slug>"`
- `ai-chain.ps1` = legacy/fallback only
- `codex` CLI = not used for Brain/Judge in Desktop Orchestrator mode

---

## 中文

### 概览

这个仓库把一套固定职责边界的协作方式打包成可复用 skill/package：

- `Codex Desktop` 负责规划、确认、验收
- `Reasonix CLI` 负责按交接合同执行
- Windows 正常入口：`.\scripts\ai-hand.ps1 "<task-slug>"`
- macOS / Linux 正常入口：`./scripts/ai-hand.sh "<task-slug>"`

这不是业务仓库安装器。它整改和分发的是 **skill/package 本身**，让仓库具备本地验证、CI 验证、文档一致性检查。

### 仓库结构

```text
.
├── .codex-plugin/plugin.json
├── .github/workflows/validate-skill.yml
├── scripts/
│   ├── skill_validator.py
│   ├── validate_skill.py
│   ├── validate-skill.ps1
│   └── validate-skill.sh
├── skills/reasonix-orchestrator/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
└── README.md
```

### 安装

把 `skills/reasonix-orchestrator/` 复制到 Codex 的 `skills/` 目录。

macOS / Linux：

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/reasonix-orchestrator ~/.codex/skills/reasonix-orchestrator
chmod +x ~/.codex/skills/reasonix-orchestrator/scripts/ai-hand.sh
```

Windows：

```text
%USERPROFILE%\.codex\skills\reasonix-orchestrator\
```

如果你使用自定义 `CODEX_HOME`，改为对应的 `skills/` 目录即可。

### 验证

本仓库唯一事实来源是统一验证脚本。

Windows：

```powershell
.\scripts\validate-skill.ps1
```

macOS / Linux：

```bash
./scripts/validate-skill.sh
```

原始 Python 入口：

```powershell
python scripts/validate_skill.py --repo-root .
```

验证目标：

- skill frontmatter 合法
- `ai-hand.ps1` PowerShell 语法合法
- `ai-hand.sh` Bash 语法合法
- `.codex-plugin/plugin.json` 必填字段完整
- `README.md`、`SKILL.md`、`references/*`、`plugin.json` 关键契约无漂移
- 文档无占位符路径、无过时入口

Windows 说明：

- 本地以 `.\scripts\validate-skill.ps1` 为准
- 如果本机没有可用 Bash，本地验证可以跳过 Bash 语法检查
- Ubuntu CI 仍必须运行 `./scripts/validate-skill.sh`

### 使用

典型流程：

```text
User
  -> Codex Desktop Brain
  -> SPEC.md / ACCEPTANCE.md / REASONIX_HANDOFF.md
  -> User confirmation inside Codex Desktop
  -> Windows: .\scripts\ai-hand.ps1 "<task-slug>"
  -> macOS / Linux: ./scripts/ai-hand.sh "<task-slug>"
  -> Reasonix CLI Hand
  -> EXECUTION_REPORT.md
  -> Codex Desktop Judge
  -> PASS / REVISE / REJECT
```

关键边界：

- `Codex Desktop` 保持正常 `Brain / Judge`
- `Reasonix CLI` 保持正常 `Hand`
- `ai-chain.ps1` 仅 legacy/fallback
- Desktop Orchestrator 模式不用 `codex` CLI 承担 Brain/Judge

### 安全边界

默认不自动执行以下操作：

- `git push`
- `git commit`
- `git reset --hard`
- `git clean`
- 删除文件
- 修改 `.env`
- 修改 secrets、证书、SSH 文件、凭据文件
- install dependencies without explicit approval

也不要求用户手动复制 `REASONIX_HANDOFF.md`。

### agents/openai.yaml

`skills/reasonix-orchestrator/agents/openai.yaml` 是可选 agent metadata。它给支持该约定的工具提供显示名、简短描述、默认 prompt 文案；它不改变 `SKILL.md` 的主契约，也不替代统一验证脚本。

### FAQ

**Q: 为什么不直接让 Codex 改代码？**  
A: 这个模式刻意把规划/验收和执行拆开。`Codex Desktop` 保留 Brain/Judge，`Reasonix CLI` 只做 Hand。

**Q: 为什么保留 `SPEC.md` / `ACCEPTANCE.md` / `REASONIX_HANDOFF.md`？**  
A: 它们是显式交接合同，定义范围、完成标准、可改区域、受保护区域。

**Q: 这个仓库会自动接入目标业务仓库吗？**  
A: 不会。本仓库只验证和分发 skill/package 自身。

---

## English

### Overview

This repository packages a fixed-responsibility workflow:

- `Codex Desktop` handles planning, confirmation, and acceptance review
- `Reasonix CLI` handles execution against explicit handoff artifacts
- Windows entrypoint: `.\scripts\ai-hand.ps1 "<task-slug>"`
- macOS / Linux entrypoint: `./scripts/ai-hand.sh "<task-slug>"`

This repository does not act as a target-repo installer. It hardens the **skill/package itself** with local validation, CI validation, and contract-drift checks.

### Install

Copy `skills/reasonix-orchestrator/` into Codex's `skills/` directory.

macOS / Linux:

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/reasonix-orchestrator ~/.codex/skills/reasonix-orchestrator
chmod +x ~/.codex/skills/reasonix-orchestrator/scripts/ai-hand.sh
```

Windows:

```text
%USERPROFILE%\.codex\skills\reasonix-orchestrator\
```

If you use a custom `CODEX_HOME`, place it under that `skills/` directory instead.

### Validate

Use the repository validation entrypoints as the single source of truth.

Windows:

```powershell
.\scripts\validate-skill.ps1
```

macOS / Linux:

```bash
./scripts/validate-skill.sh
```

Raw Python entrypoint:

```powershell
python scripts/validate_skill.py --repo-root .
```

Validation covers:

- valid skill frontmatter
- valid PowerShell syntax for `ai-hand.ps1`
- valid Bash syntax for `ai-hand.sh`
- required `.codex-plugin/plugin.json` fields
- zero contract drift across `README.md`, `SKILL.md`, `references/*`, and `plugin.json`
- no placeholder validator paths or stale entrypoints

### Workflow

```text
User
  -> Codex Desktop Brain
  -> SPEC.md / ACCEPTANCE.md / REASONIX_HANDOFF.md
  -> User confirmation inside Codex Desktop
  -> Windows: .\scripts\ai-hand.ps1 "<task-slug>"
  -> macOS / Linux: ./scripts/ai-hand.sh "<task-slug>"
  -> Reasonix CLI Hand
  -> EXECUTION_REPORT.md
  -> Codex Desktop Judge
  -> PASS / REVISE / REJECT
```

Key boundaries:

- `Codex Desktop` remains the normal `Brain / Judge`
- `Reasonix CLI` remains the normal `Hand`
- `ai-chain.ps1` remains legacy/fallback only
- Desktop Orchestrator mode does not use `codex` CLI for Brain/Judge

### Safety Boundaries

The workflow does not automatically:

- `git push`
- `git commit`
- `git reset --hard`
- `git clean`
- delete files
- modify `.env`
- modify secrets, certificates, SSH files, or credential files
- install dependencies without explicit approval

It also does not ask the user to manually copy `REASONIX_HANDOFF.md`.

### agents/openai.yaml

`skills/reasonix-orchestrator/agents/openai.yaml` is optional agent metadata. It provides a display name, short description, and default prompt text for tooling that surfaces those values. It does not replace the `SKILL.md` contract or the repository validator.
