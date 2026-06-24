<p align="center">
  <img src="assets/reasonix-mascot.jpg" alt="Reasonix Mascot" width="360" />
</p>

<h1 align="center">Reasonix Orchestrator</h1>

<p align="center">
  面向 <code>Codex Desktop + Reasonix CLI</code> 的可复用编排工作流。
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

> 让 `Codex Desktop` 负责规划、确认与验收，让 `Reasonix CLI` 负责按交接合同执行代码修改。

### 🧭 快速导航

- [🚀 项目简介](#zh-overview)
- [✨ 功能特点](#zh-features)
- [🗂️ 项目结构](#zh-structure)
- [📦 安装方式](#zh-installation)
- [🧭 使用方法](#zh-usage)
- [🧩 Codex Skill / Plugin 说明](#zh-skill-plugin)
- [💬 示例指令](#zh-example)
- [🔒 安全边界](#zh-safety)
- [❓常见问题](#zh-faq)
- [📝 附加说明](#zh-notes)
- [🙏 致谢](#zh-acknowledgements)
- [📄 License](#zh-license)

<a id="zh-overview"></a>

### 🚀 项目简介

`Reasonix Orchestrator` 是一个可复用的 Codex Skill / Plugin，用于确立一条职责清晰、边界明确的协作链路：

- `Codex Desktop` 承担 `大脑 / 裁判 / 编排者（Brain / Judge / Orchestrator）` 的角色
- `Reasonix CLI` 承担 `手 / 执行者（Hand / Executor）` 的角色
- Windows 正常入口为 `.\scripts\ai-hand.ps1 "<task-slug>"`
- macOS / Linux 正常入口为 `./scripts/ai-hand.sh "<task-slug>"`

这套工作流的出发点非常实际：让 `Codex Desktop` 负责它更擅长的架构规划、任务拆解和验收审查；让 `Reasonix CLI` 负责具体的代码执行。这样可以在有限的 Codex 使用额度下，更高效地利用 GPT 的结构化思考能力与 Reasonix 的高命中执行能力。

这套方案并不是让同一个模型一口气完成所有事情，而是将“思考与裁决”和“执行与落地”明确分层：由 Codex 生成任务合同、控制边界、做出最终判断；由 Reasonix 按合同执行并回写执行报告。

<a id="zh-features"></a>

### ✨ 功能特点

- 明确固定 `Codex Desktop` 与 `Reasonix CLI` 的职责边界。
- 保留 `SPEC / ACCEPTANCE / REASONIX_HANDOFF` 这类可审查、可重复执行的交接文件。
- 按操作系统选择固定的入口脚本，避免运行时临时切换执行方式。
- 默认保留用户确认环节，不将执行权静默下放给 Hand。
- 提供 Skill 目录与 Plugin 打包元数据，方便复用、分发与维护。
- 对危险操作设置安全边界，避免自动执行 `commit`、`push`、`reset`、`clean` 等动作。
- 适用于 Codex 承担高价值推理、而执行层希望交由外部工具完成的场景。

<a id="zh-structure"></a>

### 🗂️ 项目结构

```text
.
├─ assets/
│  ├─ reasonix-mascot.jpg
│  ├─ reasonix-logo.png
│  └─ reasonix-logo.svg
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

安装到目标项目后，通常会新增以下工作流文件：

- `AGENTS.md`
- `.ai/tasks/README.md`
- `.ai/prompts/reasonix-hand.md`
- `.reasonix/system-hand.md`
- `scripts/ai-hand.ps1`
- `scripts/ai-hand.sh`

<a id="zh-installation"></a>

### 📦 安装方式

如果只想把 Skill 装进 Codex 的 `skills` 目录，最直接的路径如下。

macOS / Linux：

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/reasonix-orchestrator ~/.codex/skills/reasonix-orchestrator
chmod +x ~/.codex/skills/reasonix-orchestrator/scripts/ai-hand.sh
```

Windows：

```text
.codex\skills\reasonix-orchestrator\
```

如果你使用了自定义的 `CODEX_HOME`，则放入对应的 `skills/` 目录。

仓库同时包含 `.codex-plugin/plugin.json`，可作为 Plugin 打包入口进一步扩展。

<a id="zh-usage"></a>

### 🧭 使用方法

正常使用时，用户主要在 `Codex Desktop` 中提出需求并做确认，典型流程如下：

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

- `Codex Desktop` 是正常的 `大脑 / 裁判 / 编排者（Brain / Judge / Orchestrator）`
- `Reasonix CLI` 是正常的 `手 / 执行者（Hand / Executor）`
- `ai-chain.ps1` 仅作为 `遗留 / 备用方案（legacy / fallback）`
- Desktop Orchestrator 模式下不使用 `codex` CLI 承担 `大脑 / 裁判` 角色

<a id="zh-skill-plugin"></a>

### 🧩 Codex Skill / Plugin 说明

这个仓库同时覆盖两种用途：

- **Skill**：核心工作流定义在 [skills/reasonix-orchestrator/SKILL.md](skills/reasonix-orchestrator/SKILL.md)
- **Plugin**：插件元数据位于 [.codex-plugin/plugin.json](.codex-plugin/plugin.json)

适合以下场景：

- 希望由 `Codex Desktop` 负责规划、确认和验收
- 希望由 `Reasonix CLI` 按交接文档执行代码修改
- 希望将这组分工固化为可复用、可审查的仓库工作流
- 希望在有限的 Codex 高价值推理资源下，让 Codex 更聚焦于规划、拆解和验收，让 Reasonix 承担具体执行

如果你更希望由同一个 AI 从头直接改到尾，不保留交接文件，也不设置确认环节，那么这套模式可能不太适合你。

<a id="zh-example"></a>

### 💬 示例指令

可以直接在 `Codex Desktop` 中这样发起：

```text
按 Codex Desktop Orchestrator 模式处理。
任务名：example-task

需求：这里写你的需求。
请先作为 Brain 生成 SPEC / ACCEPTANCE / REASONIX_HANDOFF，
展示摘要后问我是否确认交给 Reasonix 执行。
```

如果需要更完整的信息，可以继续补充：

- 范围（scope）
- 禁止修改的内容（protected areas）
- 验收标准（acceptance criteria）

<a id="zh-safety"></a>

### 🔒 安全边界

这套工作流默认不会自动执行以下危险操作：

- `git push`
- `git commit`
- `git reset --hard`
- `git clean`
- 删除重要文件
- 修改 `.env`
- 修改密钥、证书、SSH 文件或凭据文件
- 未经用户明确批准自动安装依赖

另外，Desktop Orchestrator 模式默认：

- 不使用 `ai-chain.ps1` 作为正常入口
- 不使用 `codex` CLI 承担 `大脑 / 裁判` 角色

也就是说，它默认不会绕过调用者的确认环节，也不会将高风险动作直接下放给执行层。

<a id="zh-faq"></a>

### ❓常见问题

#### 1. 我需要很懂 Reasonix 吗？

不需要。作为这套管道中的编排者、Codex 用户或操作员，你不需要成为 Reasonix 专家。你只需要知道：Codex 负责生成交接合同，Reasonix 负责执行这些合同，并将执行结果写回执行报告。

#### 2. 为什么不直接让 Codex 改代码？

因为这套模式强调将“先想清楚怎么做”和“真正去动代码”拆分开来。这样更容易审查、回滚，也更容易复用同一套交接合同。

#### 3. 为什么要保留 SPEC / ACCEPTANCE / HANDOFF？

因为这些文件本质上就是任务合同，明确规定了：

- 本次到底要做什么
- 做到什么程度算完成
- Reasonix 可以修改哪些内容
- 哪些内容绝对不能碰

#### 4. 为什么不把 `ai-chain.ps1` 当成正常入口？

因为这套模式要求用户的确认权和 `大脑 / 裁判` 权都保留在 `Codex Desktop`。因此 `ai-chain.ps1` 只能是 `遗留 / 备用方案（legacy / fallback）`，不是主路径。

#### 5. Reasonix 改错了怎么办？

正常处理方式是让 `Codex Desktop` 给出 `REVISE`（修改合同）或 `REJECT`（驳回）的裁定，然后收紧 `SPEC / ACCEPTANCE / HANDOFF` 的内容，再决定是否重新执行。

#### 6. 这个 Skill 会不会自动提交或推送代码？

不会。默认不自动执行 `commit`、`push`、`reset`、`clean`。

<a id="zh-notes"></a>

### 📝 附加说明

**首次接入建议**：先跑一个很小的冒烟测试（smoke test），不要直接拿重要需求上来尝试。

**最简单的检查流程如下：**

1. `Codex Desktop` 先生成 `SPEC.md`、`ACCEPTANCE.md` 和 `REASONIX_HANDOFF.md`
2. 它先向你确认是否执行
3. Windows 走 `.\scripts\ai-hand.ps1 "<task-slug>"`
4. macOS / Linux 走 `./scripts/ai-hand.sh "<task-slug>"`
5. `Reasonix CLI` 执行后输出 `.ai/tasks/<task-slug>/EXECUTION_REPORT.md`
6. 最终由 `Codex Desktop` 读取结果并给出 `PASS / REVISE / REJECT` 裁定

**扩展阅读**：如果需要继续维护或扩展这套 Skill，建议从以下入口开始：

- [skills/reasonix-orchestrator/SKILL.md](skills/reasonix-orchestrator/SKILL.md)
- [skills/reasonix-orchestrator/references/workflow-details.md](skills/reasonix-orchestrator/references/workflow-details.md)
- [skills/reasonix-orchestrator/references/file-contracts.md](skills/reasonix-orchestrator/references/file-contracts.md)
- [skills/reasonix-orchestrator/references/reasonix-hand-contract.md](skills/reasonix-orchestrator/references/reasonix-hand-contract.md)
- [skills/reasonix-orchestrator/references/plugin-packaging.md](skills/reasonix-orchestrator/references/plugin-packaging.md)
- [skills/reasonix-orchestrator/references/test-checklist.md](skills/reasonix-orchestrator/references/test-checklist.md)

<a id="zh-acknowledgements"></a>

### 🙏 致谢

本项目的执行层设计受到 [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) 的启发。感谢 Reasonix 项目及其作者为开发者提供的关于“执行层”能力的思路参考。

本仓库并非 Reasonix 官方项目，也不代表 Reasonix 官方立场。此处引用的链接仅为说明灵感来源，不表示官方合作、授权或背书。

<a id="zh-license"></a>

### 📄 License

本项目基于 [MIT License](LICENSE) 开源。

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
- [🔒 Safety Boundaries](#en-safety)
- [❓ FAQ](#en-faq)
- [🙏 Acknowledgements](#en-acknowledgements)
- [📄 License](#en-license)

<a id="en-overview"></a>

### 🚀 Overview

`Reasonix Orchestrator` is a reusable Codex Skill / Plugin for a workflow with fixed responsibilities:

- `Codex Desktop` = `Brain / Judge / Orchestrator`
- `Reasonix CLI` = `Hand / Executor`
- Windows entrypoint = `.\scripts\ai-hand.ps1 "<task-slug>"`
- macOS / Linux entrypoint = `./scripts/ai-hand.sh "<task-slug>"`

The practical goal is straightforward: keep architecture planning, task decomposition, and acceptance review inside Codex Desktop; delegate concrete code execution to Reasonix CLI. This makes the pipeline more suitable for situations where high-value Codex reasoning should be spent on planning and judgment, while execution is handled by a separate tool.

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

**macOS / Linux:**

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/reasonix-orchestrator ~/.codex/skills/reasonix-orchestrator
chmod +x ~/.codex/skills/reasonix-orchestrator/scripts/ai-hand.sh
```

**Windows:** the target is typically:

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
- Desktop Orchestrator mode does not use `codex` CLI as `Brain / Judge`

<a id="en-skill-plugin"></a>

### 🧩 Codex Skill / Plugin

This repository serves both as:

- a reusable **Skill**
- a **Plugin**-ready package with `.codex-plugin/plugin.json`

Use it when you want Codex Desktop to own planning and review, while Reasonix performs code changes defined by explicit handoff contracts.

<a id="en-example"></a>

### 💬 Example Prompt

```text
Handle this in Codex Desktop Orchestrator mode.
Task name: example-task

Requirement: describe the task here.
First generate SPEC / ACCEPTANCE / REASONIX_HANDOFF as Brain,
show me the summary, then ask for confirmation before Reasonix executes.
```

<a id="en-safety"></a>

### 🔒 Safety Boundaries

By default, this workflow does not automatically:

- `git push`
- `git commit`
- `git reset --hard`
- `git clean`
- delete important files
- modify `.env`
- modify keys, certificates, SSH files, or credential files
- install dependencies unless the user explicitly approves

It also does not use `ai-chain.ps1` as the normal entrypoint, and it does not use `codex` CLI as `Brain / Judge` in Desktop Orchestrator mode.

<a id="en-faq"></a>

### ❓ FAQ

#### 1. Do I need to know Reasonix deeply?

No. As the orchestrator, Codex user, or operator in this pipeline, you do not need to become a Reasonix expert. You only need to understand that Codex produces the handoff contracts, Reasonix executes them, and the result is written back as an execution report.

#### 2. Why not let Codex edit code directly?

Because this workflow intentionally separates planning from execution. That makes review, rollback, and reuse easier.

#### 3. Why keep SPEC / ACCEPTANCE / HANDOFF?

They act as the explicit contract for scope, completion criteria, editable areas, and protected areas.

#### 4. Why is `ai-chain.ps1` not the default path?

Because confirmation and Brain / Judge ownership must stay in `Codex Desktop`. `ai-chain.ps1` is therefore only `legacy / fallback`.

#### 5. What if Reasonix makes a mistake?

The normal process is to have `Codex Desktop` issue a `REVISE` or `REJECT`, then tighten the `SPEC / ACCEPTANCE / HANDOFF` and decide whether to re-run.

#### 6. Will this Skill automatically commit or push code?

No. It does not automatically `commit`, `push`, `reset`, or `clean` by default.

<a id="en-acknowledgements"></a>

### 🙏 Acknowledgements

This project is inspired by [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) as an execution layer. It is not an official Reasonix project and does not imply endorsement by the Reasonix author or maintainers.

<a id="en-license"></a>

### 📄 License

Licensed under the [MIT License](LICENSE).
