<p align="center">
  <img src="assets/reasonix-logo.svg" alt="Reasonix Logo" width="360" />
</p>

<p align="center">
  <img src="assets/reasonix-mascot.jpg" alt="Reasonix Mascot" width="220" />
</p>

<h1 align="center">Reasonix Orchestrator</h1>

<p align="center">
  A reusable orchestration workflow for teams that want Codex Desktop to stay the Brain and Judge, while Reasonix CLI acts as the Hand.
</p>

<p align="center">
  为 <code>Codex Desktop + Reasonix CLI</code> 设计的可复用协作工作流。<br />
  Keep planning, confirmation, and review in Codex. Delegate execution to Reasonix.
</p>

<p align="center">
  <a href="#zh-cn">简体中文</a> |
  <a href="#en">English</a>
</p>

<p align="center">
  <a href="https://github.com/Neronm/codex-reasonix-orchestrator-skill/stargazers"><img src="https://img.shields.io/github/stars/Neronm/codex-reasonix-orchestrator-skill?style=for-the-badge" alt="GitHub Stars" /></a>
  <a href="https://github.com/Neronm/codex-reasonix-orchestrator-skill/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Neronm/codex-reasonix-orchestrator-skill?style=for-the-badge" alt="GitHub License" /></a>
  <img src="https://img.shields.io/badge/Codex-Skill-1f6feb?style=for-the-badge" alt="Codex Skill" />
  <img src="https://img.shields.io/badge/DeepSeek-Reasonix-0f766e?style=for-the-badge" alt="DeepSeek Reasonix" />
  <img src="https://img.shields.io/badge/Plugin-Ready-f59e0b?style=for-the-badge" alt="Plugin Ready" />
</p>

---

<a id="zh-cn"></a>

## 简体中文

> 让 `Codex Desktop` 负责思考、确认、验收，让 `Reasonix CLI` 负责按合同执行代码修改。

### 🧭 快速导航

- [🚀 项目简介](#zh-overview)
- [✨ 功能特点](#zh-features)
- [🗂️ 项目结构](#zh-structure)
- [📦 安装方式](#zh-installation)
- [🧭 使用方法](#zh-usage)
- [🧩 Codex Skill / Plugin 说明](#zh-skill-plugin)
- [💬 示例指令](#zh-example)
- [❓常见问题](#zh-faq)
- [📄 License](#zh-license)

<a id="zh-overview"></a>
### 🚀 项目简介

`Reasonix Orchestrator` 是一个可复用的 Codex Skill / Plugin，用来固定一套清晰的协作分工：

- `Codex Desktop` 负责 `Brain / Judge / Orchestrator`
- `Reasonix CLI` 负责 `Hand / Executor`
- Windows 正常入口是 `.\scripts\ai-hand.ps1 "<task-slug>"`
- macOS / Linux 正常入口是 `./scripts/ai-hand.sh "<task-slug>"`

它解决的问题很直接：很多人希望由 `Codex Desktop` 先理解需求、拆任务、生成交接文档、拿到确认，再把实际代码修改交给另一个执行器，而不是让同一个 AI 一上来就直接改代码。

<a id="zh-features"></a>
### ✨ 功能特点

- 明确固定 `Codex Desktop` 与 `Reasonix CLI` 的职责边界。
- 保留 `SPEC / ACCEPTANCE / REASONIX_HANDOFF` 这类可审查、可复跑的交接文件。
- 按平台选择固定入口脚本，而不是临时换执行方式。
- 默认保留用户确认环节，不把执行权静默下放给 Hand。
- 提供 Skill 目录与 Plugin 打包元数据，方便复用、分发、维护。
- 对危险操作设置安全边界，避免自动 `commit`、`push`、`reset`、`clean` 等动作。

<a id="zh-structure"></a>
### 🗂️ 项目结构

```text
.
├─ assets/
│  ├─ reasonix-mascot.jpg
│  └─ reasonix-logo.png              # 预留 logo 路径，可后续补充
├─ .codex-plugin/
│  └─ plugin.json
├─ skills/
│  └─ reasonix-orchestrator/
│     ├─ SKILL.md
│     ├─ agents/
│     ├─ references/
│     └─ scripts/
├─ LICENSE
└─ README.md
```

安装到目标项目后，常见会新增这些工作流文件：

- `AGENTS.md`
- `.ai/tasks/README.md`
- `.ai/prompts/reasonix-hand.md`
- `.reasonix/system-hand.md`
- `scripts/ai-hand.ps1`
- `scripts/ai-hand.sh`

<a id="zh-installation"></a>
### 📦 安装方式

如果你只想把 Skill 装进 Codex skills 目录，最直接路径如下。

macOS / Linux:

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/reasonix-orchestrator ~/.codex/skills/reasonix-orchestrator
chmod +x ~/.codex/skills/reasonix-orchestrator/scripts/ai-hand.sh
```

Windows 可理解为放到用户目录下的：

```text
.codex\skills\reasonix-orchestrator\
```

如果你使用自定义 `CODEX_HOME`，就放到对应的 `skills/` 目录里。

仓库同时包含 `.codex-plugin/plugin.json`，可作为 Plugin 打包入口继续扩展。

<a id="zh-usage"></a>
### 🧭 使用方法

正常使用时，用户主要只在 `Codex Desktop` 里提需求和确认，典型流程如下：

```text
你 → Codex Desktop 规划
  → 生成 SPEC / ACCEPTANCE / HANDOFF
  → 你确认
  → Codex Desktop 按系统选择 ai-hand 脚本
  → Reasonix 执行
  → Codex Desktop 审查
  → PASS / REVISE / REJECT
```

最重要的工作流约束：

- `Codex Desktop` 是正常的 `Brain / Judge / Orchestrator`
- `Reasonix CLI` 是正常的 `Hand / Executor`
- `ai-chain.ps1` 仅作为 `legacy / fallback`
- 不使用 `codex` CLI 承担这套模式里的 `Brain / Judge`

<a id="zh-skill-plugin"></a>
### 🧩 Codex Skill / Plugin 说明

这个仓库同时覆盖两层用途：

- `Skill`：核心工作流定义在 [skills/reasonix-orchestrator/SKILL.md](skills/reasonix-orchestrator/SKILL.md)
- `Plugin`：插件元数据位于 [.codex-plugin/plugin.json](.codex-plugin/plugin.json)

适合这类场景：

- 想让 `Codex Desktop` 负责规划、确认、验收
- 想让 `Reasonix CLI` 只负责按交接文档执行代码修改
- 想把这套分工固化成可复用、可审查的仓库工作流
- 想给团队或多个项目复用同一套 orchestration contract

如果你更想要的是同一个 AI 直接从头改到尾，不保留交接文件，也不保留确认环节，那这套模式可能不适合你。

<a id="zh-example"></a>
### 💬 示例指令

可以直接在 `Codex Desktop` 里这样发起：

```text
按 Codex Desktop Orchestrator 模式处理。
任务名：example-task

需求：这里写你的需求。
请先作为 Brain 生成 SPEC / ACCEPTANCE / REASONIX_HANDOFF，
展示摘要后问我是否确认交给 Reasonix 执行。
```

如果你愿意写得更完整，可以继续补：

- 范围
- 不要改什么
- 验收标准

### 🔒 安全边界

这套工作流默认不会自动做下面这些危险操作：

- `git push`
- `git commit`
- `git reset --hard`
- `git clean`
- 删除重要文件
- 修改 `.env`
- 修改密钥、证书、SSH、凭据文件
- 未经用户明确批准自动安装依赖

换句话说，它默认不会偷偷提交代码、偷偷推远端、偷偷清工作区，也不会绕过你直接让 `Reasonix` 自己决定高风险操作。

<a id="zh-faq"></a>
### ❓常见问题

#### 1. 我需要很懂 Reasonix 吗？

不需要。普通使用者只需要知道：真正动代码的是 `Reasonix CLI`，但主要交互入口仍然是 `Codex Desktop`。

#### 2. 为什么不直接让 Codex 改代码？

因为这套模式强调把“先想清楚怎么做”和“真正去动代码”拆开。这样更容易审查、更容易回滚，也更容易复用同一套交接合同。

#### 3. 为什么要保留 SPEC / ACCEPTANCE / HANDOFF？

因为这些文件就是任务合同，明确：

- 这次到底要做什么
- 做到什么算完成
- Reasonix 可以动哪些内容
- 哪些内容不能碰

#### 4. 为什么不把 `ai-chain.ps1` 当正常入口？

因为这套模式要求用户确认留在 `Codex Desktop`，Brain / Judge 也留在 `Codex Desktop`。所以 `ai-chain.ps1` 只能是 `legacy / fallback`，不是主路径。

#### 5. Reasonix 改错了怎么办？

正常处理方式是让 `Codex Desktop` 给出 `REVISE` 或 `REJECT`，然后收紧 `SPEC / ACCEPTANCE / HANDOFF`，再决定是否重新执行。

#### 6. 这个 Skill 会不会自动提交或推送代码？

不会。默认不自动 `commit`、`push`、`reset`、`clean`。

### 🧪 附加说明

首次接入建议先跑一个很小的 smoke test，不要直接拿重要需求上来跑。最简单检查项如下：

- `Codex Desktop` 先生成 `SPEC.md`、`ACCEPTANCE.md`、`REASONIX_HANDOFF.md`
- 它先向你确认是否执行
- Windows 走 `.\scripts\ai-hand.ps1 "<task-slug>"`
- macOS / Linux 走 `./scripts/ai-hand.sh "<task-slug>"`
- `Reasonix CLI` 执行后写出 `.ai/tasks/<task-slug>/EXECUTION_REPORT.md`
- 最终由 `Codex Desktop` 读取结果并给出 `PASS / REVISE / REJECT`

如果你要继续维护或扩展这套 Skill，建议从这些入口继续看：

- [skills/reasonix-orchestrator/SKILL.md](skills/reasonix-orchestrator/SKILL.md)
- [skills/reasonix-orchestrator/references/workflow-details.md](skills/reasonix-orchestrator/references/workflow-details.md)
- [skills/reasonix-orchestrator/references/file-contracts.md](skills/reasonix-orchestrator/references/file-contracts.md)
- [skills/reasonix-orchestrator/references/reasonix-hand-contract.md](skills/reasonix-orchestrator/references/reasonix-hand-contract.md)
- [skills/reasonix-orchestrator/references/plugin-packaging.md](skills/reasonix-orchestrator/references/plugin-packaging.md)
- [skills/reasonix-orchestrator/references/test-checklist.md](skills/reasonix-orchestrator/references/test-checklist.md)

<a id="zh-license"></a>
### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<a id="en"></a>

## English

> Keep planning, confirmation, and review inside `Codex Desktop`. Let `Reasonix CLI` execute against explicit handoff contracts.

### 🧭 Quick Navigation

- [🚀 Overview](#en-overview)
- [✨ Features](#en-features)
- [🗂️ Project Structure](#en-structure)
- [📦 Installation](#en-installation)
- [🧭 Usage](#en-usage)
- [🧩 Codex Skill / Plugin](#en-skill-plugin)
- [💬 Example Prompt](#en-example)
- [❓FAQ](#en-faq)
- [📄 License](#en-license)

<a id="en-overview"></a>
### 🚀 Overview

`Reasonix Orchestrator` is a reusable Codex Skill / Plugin for a workflow with fixed responsibilities:

- `Codex Desktop` = `Brain / Judge / Orchestrator`
- `Reasonix CLI` = `Hand / Executor`
- Windows entrypoint = `.\scripts\ai-hand.ps1 "<task-slug>"`
- macOS / Linux entrypoint = `./scripts/ai-hand.sh "<task-slug>"`

It is designed for teams who want planning, confirmation, and review to stay inside `Codex Desktop`, while code execution is delegated to `Reasonix CLI` through explicit handoff files.

<a id="en-features"></a>
### ✨ Features

- Clear Brain / Judge / Hand separation.
- Reusable handoff documents such as `SPEC`, `ACCEPTANCE`, and `REASONIX_HANDOFF`.
- Platform-specific fixed execution entrypoints.
- Human confirmation remains inside `Codex Desktop`.
- Skill packaging plus plugin metadata for reuse and distribution.
- Built-in safety boundaries around risky operations.

<a id="en-structure"></a>
### 🗂️ Project Structure

```text
.
├─ assets/
├─ .codex-plugin/
├─ skills/
│  └─ reasonix-orchestrator/
├─ LICENSE
└─ README.md
```

Main workflow entrypoints and references live under:

- [skills/reasonix-orchestrator/SKILL.md](skills/reasonix-orchestrator/SKILL.md)
- [.codex-plugin/plugin.json](.codex-plugin/plugin.json)

<a id="en-installation"></a>
### 📦 Installation

Install the skill into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/reasonix-orchestrator ~/.codex/skills/reasonix-orchestrator
chmod +x ~/.codex/skills/reasonix-orchestrator/scripts/ai-hand.sh
```

On Windows, the target is typically:

```text
.codex\skills\reasonix-orchestrator\
```

If you use a custom `CODEX_HOME`, place it inside that `skills/` directory instead.

<a id="en-usage"></a>
### 🧭 Usage

Typical execution flow:

```text
User request
  → Codex Desktop plans
  → SPEC / ACCEPTANCE / HANDOFF generated
  → user confirms
  → platform-specific ai-hand script runs
  → Reasonix executes
  → Codex Desktop reviews
  → PASS / REVISE / REJECT
```

Key constraints:

- `Codex Desktop` remains the normal `Brain / Judge`
- `Reasonix CLI` remains the normal `Hand`
- `ai-chain.ps1` is `legacy / fallback` only
- `codex` CLI is not the normal Brain / Judge in this mode

<a id="en-skill-plugin"></a>
### 🧩 Codex Skill / Plugin

This repository serves both as:

- a reusable Skill
- a Plugin-ready package with `.codex-plugin/plugin.json`

Use it when you want Codex Desktop to own planning and review, while Reasonix only performs code changes defined by the generated contract files.

<a id="en-example"></a>
### 💬 Example Prompt

```text
Handle this in Codex Desktop Orchestrator mode.
Task name: example-task

Requirement: describe the task here.
First generate SPEC / ACCEPTANCE / REASONIX_HANDOFF as Brain,
show me the summary, then ask for confirmation before Reasonix executes.
```

<a id="en-faq"></a>
### ❓FAQ

#### 1. Do I need to know Reasonix deeply?

No. Most users only need to know that `Reasonix CLI` performs the code changes, while `Codex Desktop` remains the main interaction surface.

#### 2. Why not let Codex edit code directly?

Because this workflow intentionally separates planning from execution. That makes review, rollback, and reuse easier.

#### 3. Why keep SPEC / ACCEPTANCE / HANDOFF?

They act as the explicit contract for scope, completion, editable areas, and protected areas.

#### 4. Why is `ai-chain.ps1` not the default path?

Because confirmation and Brain / Judge ownership must stay in `Codex Desktop`. `ai-chain.ps1` is therefore only `legacy / fallback`.

<a id="en-license"></a>
### 📄 License

Licensed under the [MIT License](LICENSE).
