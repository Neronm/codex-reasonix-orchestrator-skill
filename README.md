<p align="center">
  <img src="assets/reasonix-mascot.jpg" alt="Reasonix Mascot" width="320" />
</p>

<h1 align="center">Reasonix Orchestrator</h1>

<p align="center">
  面向 <code>Codex Desktop + Reasonix CLI</code> 的可复用编排工作流
</p>

<p align="center">
  <a href="#zh-cn">简体中文</a> | <a href="#en">English</a>
</p>

<p align="center">
  <a href="https://github.com/Neronm/codex-reasonix-orchestrator-skill/stargazers"><img src="https://img.shields.io/github/stars/Neronm/codex-reasonix-orchestrator-skill?style=for-the-badge" alt="GitHub Stars" /></a>
  <a href="https://github.com/Neronm/codex-reasonix-orchestrator-skill/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Neronm/codex-reasonix-orchestrator-skill?style=for-the-badge" alt="GitHub License" /></a>
  <img src="https://img.shields.io/badge/Codex-Skill-2563eb?style=for-the-badge" alt="Codex Skill" />
  <img src="https://img.shields.io/badge/DeepSeek-Reasonix-0f766e?style=for-the-badge" alt="DeepSeek Reasonix" />
  <img src="https://img.shields.io/badge/Plugin-Ready-f59e0b?style=for-the-badge" alt="Plugin Ready" />
</p>

---

<a id="zh-cn"></a>

## 简体中文

> 让 `Codex Desktop` 负责规划、确认与验收，让 `Reasonix CLI` 负责按交接合同执行代码修改。

## 🧭 快速导航

- [📌 项目简介](#zh-overview)
- [✨ 功能特点](#zh-features)
- [📁 项目结构](#zh-structure)
- [📦 安装方式](#zh-installation)
- [🧭 使用方法](#zh-usage)
- [🛠 Codex Skill / Plugin 说明](#zh-skill-plugin)
- [💬 示例指令](#zh-example)
- [🔒 安全边界](#zh-safety)
- [❓ 常见问题](#zh-faq)
- [📝 附加说明](#zh-notes)
- [🙏 致谢](#zh-acknowledgements)
- [📄 License](#zh-license)

<a id="zh-overview"></a>

## 📌 项目简介

`Reasonix Orchestrator` 用来固化一套职责清晰、边界明确、可审查复用的协作方式：

- `Codex Desktop` 负责规划、确认、验收
- `Reasonix CLI` 负责按交接合同执行
- `Codex Desktop = Brain / Judge / Orchestrator`
- `Reasonix CLI = Hand / Executor`
- Windows 正常入口：`.\scripts\ai-hand.ps1 "<task-slug>"`
- macOS / Linux 正常入口：`./scripts/ai-hand.sh "<task-slug>"`
- `ai-chain.ps1` 仅 `legacy/fallback`
- Desktop Orchestrator 模式不用 `codex` CLI 承担 Brain/Judge；`codex` CLI is not used for Brain/Judge in Desktop Orchestrator mode

这套工作流的出发点是：Codex Desktop 负责架构规划、任务拆解、验收审查；具体代码执行交给 Reasonix CLI。在有限的 Codex 使用额度下，可以更稳妥高效地利用 GPT / Codex 的结构化思考能力，以及 Reasonix 超高缓存命中率上的优势。

尤其在 Codex 额度逐渐减少的趋势下，这种分工会更有意义：Codex Desktop 作为“大脑、总控、验收官”，负责判断方向、约束范围、审核结果；Reasonix CLI 作为“执行手”，负责按交接合同落地修改。整个链路仍然保持可追踪、可回放、可复核。

这不是把所有事情一次性交给同一个模型完成，而是把“思考、裁决”和“执行、落地”明确拆层：由 Codex 生成任务合同、约束边界、给出验收结论；由 Reasonix 读取合同、执行修改、回写执行报告。

<a id="zh-features"></a>

## ✨ 功能特点

- 明确固定 `Codex Desktop` 与 `Reasonix CLI` 的职责边界
- 保留 `SPEC / ACCEPTANCE / REASONIX_HANDOFF` 这类可审查、可复用、可重复执行的交接文件
- 按操作系统选择固定入口，避免运行时临时切换执行方式
- 用户确认仍保留在 `Codex Desktop`，不把最终放行动作静默下放给 Hand
- 同时提供 Skill 目录与 Plugin 元数据，便于复用、分发与维护
- 对高风险动作设置清晰安全边界，避免协作链路失控
- 适合让 Codex 聚焦高价值推理，让 Reasonix 承担高命中执行的工作流场景

<a id="zh-structure"></a>

## 📁 项目结构

```text
.
├── assets/
│   ├── reasonix-mascot.jpg
│   ├── reasonix-logo.png
│   └── reasonix-logo.svg
├── .codex-plugin/
│   └── plugin.json
├── .github/
│   └── workflows/
├── scripts/
│   ├── skill_validator.py
│   ├── validate-skill.ps1
│   ├── validate-skill.sh
│   └── validate_skill.py
├── skills/
│   └── reasonix-orchestrator/
│       ├── SKILL.md
│       ├── agents/
│       ├── references/
│       └── scripts/
├── tests/
├── LICENSE
└── README.md
```

如果把这套 Skill 安装进目标仓库，通常还会配合以下工作流文件使用：

- `AGENTS.md`
- `.ai/tasks/README.md`
- `.ai/prompts/reasonix-hand.md`
- `.reasonix/system-hand.md`
- `scripts/ai-hand.ps1`
- `scripts/ai-hand.sh`

<a id="zh-installation"></a>

## 📦 安装方式

如果只想把 Skill 装进 Codex 的 `skills/` 目录，最直接的路径如下。

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

如果使用自定义 `CODEX_HOME`，放入对应的 `skills/` 目录即可。

仓库同时包含 `.codex-plugin/plugin.json`，可作为 Plugin 打包入口继续扩展。

<a id="zh-usage"></a>

## 🧭 使用方法

正常使用时，调用者主要在 `Codex Desktop` 中提出需求并做确认，典型流程如下：

```text
你 -> Codex Desktop 规划
   -> 生成 SPEC / ACCEPTANCE / REASONIX_HANDOFF
   -> 你确认
   -> Codex Desktop 按系统选择 ai-hand 脚本
   -> Reasonix 执行
   -> Codex Desktop 审查
   -> PASS / REVISE / REJECT
```

核心约束如下：

- `Codex Desktop` 是正常的 `Brain / Judge / Orchestrator`
- `Reasonix CLI` 是正常的 `Hand / Executor`
- `ai-chain.ps1` 仅作为 `legacy / fallback`
- Desktop Orchestrator 模式下不使用 `codex` CLI 承担 `Brain / Judge`

<a id="zh-skill-plugin"></a>

## 🛠 Codex Skill / Plugin 说明

这个仓库同时覆盖两种用途：

- **Skill**：核心工作流定义位于 [skills/reasonix-orchestrator/SKILL.md](/C:/Projects/codex-reasonix-orchestrator-skill/skills/reasonix-orchestrator/SKILL.md)
- **Plugin**：插件元数据位于 [.codex-plugin/plugin.json](/C:/Projects/codex-reasonix-orchestrator-skill/.codex-plugin/plugin.json)

适合以下场景：

- 希望由 `Codex Desktop` 负责规划、确认和验收
- 希望由 `Reasonix CLI` 按交接文档执行代码修改
- 希望把这套协作边界沉淀为可复用、可审查的仓库工作流
- 希望在有限的 Codex 高价值推理资源下，让 Codex 更聚焦规划、拆解和验收，让 Reasonix 承担具体执行

如果你的目标是让同一个 AI 从头直接改到尾，不保留交接文件，也不设置确认环节，这套模式通常不适合。

<a id="zh-example"></a>

## 💬 示例指令

可以直接在 `Codex Desktop` 中这样发起：

```text
按 Codex Desktop Orchestrator 模式处理。
任务名：example-task

需求：这里写你的需求。
请先作为 Brain 生成 SPEC / ACCEPTANCE / REASONIX_HANDOFF，
展示摘要后向我确认这次交给 Reasonix 执行。
```

如果需要更完整的边界，可以继续补充：

- 范围（scope）
- 禁止修改的内容（protected areas）
- 验收标准（acceptance criteria）

<a id="zh-safety"></a>

## 🔒 安全边界

这套工作流默认不会自动执行以下高风险操作：

- `git push`
- `git commit`
- `git reset --hard`
- `git clean`
- 删除重要文件
- 修改 `.env`
- 修改密钥、证书、SSH 文件或凭据文件
- install dependencies without explicit approval

另外，Desktop Orchestrator 模式默认：

- 不使用 `ai-chain.ps1` 作为正常入口
- 不使用 `codex` CLI 承担 `Brain / Judge`

也就是说，它不会绕过调用者确认，也不会把高风险动作直接下放给执行层。

<a id="zh-faq"></a>

## ❓ 常见问题

### 1. 需要很懂 Reasonix 吗？

不需要。作为这套链路里的编排者、调用者或操作员，只需要知道：Codex 负责生成交接合同，Reasonix 负责按合同执行，并把结果回写为执行报告。

### 2. 为什么不直接让 Codex 改代码？

因为这套模式强调把“先想清楚怎么做”和“真正去改代码”拆开。这样更容易审查、回滚，也更容易复用同一套交接合同。

### 3. 为什么要保留 SPEC / ACCEPTANCE / HANDOFF？

因为这些文件本质上就是任务合同，明确规定了：

- 这次到底要做什么
- 做到什么程度算完成
- Reasonix 可以改哪些内容
- 哪些内容不能碰

### 4. 为什么不把 `ai-chain.ps1` 当成正常入口？

因为这套模式要求确认权和 `Brain / Judge` 都留在 `Codex Desktop`。因此 `ai-chain.ps1` 只能是 `legacy / fallback`，不能是主路径。

### 5. Reasonix 改错了怎么办？

正常做法是由 `Codex Desktop` 给出 `REVISE` 或 `REJECT`，收紧 `SPEC / ACCEPTANCE / REASONIX_HANDOFF` 后再决定是否重跑。

### 6. 这个 Skill 会自动提交或推送代码吗？

不会。默认不自动执行 `commit`、`push`、`reset`、`clean`。

<a id="zh-notes"></a>

## 📝 附加说明

首次接入建议先跑一个很小的 smoke test，不要直接把重要需求丢给执行链。

最简单的检查流程如下：

1. `Codex Desktop` 先生成 `SPEC.md`、`ACCEPTANCE.md` 和 `REASONIX_HANDOFF.md`
2. 它先向你确认是否执行
3. Windows 走 `.\scripts\ai-hand.ps1 "<task-slug>"`
4. macOS / Linux 走 `./scripts/ai-hand.sh "<task-slug>"`
5. `Reasonix CLI` 执行后输出 `.ai/tasks/<task-slug>/EXECUTION_REPORT.md`
6. 最终由 `Codex Desktop` 读取结果并给出 `PASS / REVISE / REJECT`

仓库级验证入口：

- `.\scripts\validate-skill.ps1`
- `./scripts/validate-skill.sh`
- `python scripts/validate_skill.py --repo-root .`

`skills/reasonix-orchestrator/agents/openai.yaml` 是可选 agent metadata，用来提供显示名称、简短说明和默认 prompt 文案；其中的 `default_prompt` 字段用于声明默认提示内容。

如果需要继续维护或扩展这套 Skill，建议从这些文件开始：

- [skills/reasonix-orchestrator/SKILL.md](/C:/Projects/codex-reasonix-orchestrator-skill/skills/reasonix-orchestrator/SKILL.md)
- [skills/reasonix-orchestrator/references/workflow-details.md](/C:/Projects/codex-reasonix-orchestrator-skill/skills/reasonix-orchestrator/references/workflow-details.md)
- [skills/reasonix-orchestrator/references/file-contracts.md](/C:/Projects/codex-reasonix-orchestrator-skill/skills/reasonix-orchestrator/references/file-contracts.md)
- [skills/reasonix-orchestrator/references/reasonix-hand-contract.md](/C:/Projects/codex-reasonix-orchestrator-skill/skills/reasonix-orchestrator/references/reasonix-hand-contract.md)
- [skills/reasonix-orchestrator/references/plugin-packaging.md](/C:/Projects/codex-reasonix-orchestrator-skill/skills/reasonix-orchestrator/references/plugin-packaging.md)
- [skills/reasonix-orchestrator/references/test-checklist.md](/C:/Projects/codex-reasonix-orchestrator-skill/skills/reasonix-orchestrator/references/test-checklist.md)

<a id="zh-acknowledgements"></a>

## 🙏 致谢

本项目的执行层设计受到 [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) 的启发。感谢 Reasonix 项目及其作者为开发者提供的执行层思路参考。

本仓库并非 Reasonix 官方项目，也不代表 Reasonix 官方立场。这里引用相关链接，仅用于说明灵感来源，不表示官方合作、授权或背书。

<a id="zh-license"></a>

## 📄 License

本项目基于 [MIT License](/C:/Projects/codex-reasonix-orchestrator-skill/LICENSE) 开源。

---

<a id="en"></a>

## English

Keep planning, confirmation, and review inside `Codex Desktop`. Let `Reasonix CLI` execute against explicit handoff contracts.

## 📌 Overview

`Reasonix Orchestrator` is a reusable Codex Skill / Plugin for a workflow with fixed responsibilities:

- `Codex Desktop = Brain / Judge / Orchestrator`
- `Reasonix CLI = Hand / Executor`
- Windows entrypoint: `.\scripts\ai-hand.ps1 "<task-slug>"`
- macOS / Linux entrypoint: `./scripts/ai-hand.sh "<task-slug>"`
- `ai-chain.ps1` is `legacy/fallback` only
- `codex` CLI is not used for Brain/Judge in Desktop Orchestrator mode

The goal is practical: keep architecture planning, task decomposition, and acceptance review in Codex Desktop, while handing concrete code execution to Reasonix CLI.

## ✨ Features

- Clear Brain / Judge / Hand separation
- Reusable handoff artifacts such as `SPEC`, `ACCEPTANCE`, and `REASONIX_HANDOFF`
- Fixed OS-specific entrypoints
- User confirmation stays inside `Codex Desktop`
- Skill packaging plus plugin metadata for reuse and distribution
- Explicit safety boundaries for risky operations

## 📁 Project Structure

```text
.
├── assets/
├── .codex-plugin/
├── .github/
├── scripts/
├── skills/
├── tests/
├── LICENSE
└── README.md
```

## 📦 Installation

Install the skill into your Codex `skills/` directory.

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

## 🧭 Usage

```text
User request
  -> Codex Desktop plans
  -> SPEC / ACCEPTANCE / REASONIX_HANDOFF generated
  -> user confirms
  -> matching ai-hand script runs
  -> Reasonix executes
  -> Codex Desktop reviews
  -> PASS / REVISE / REJECT
```

## 🛠 Codex Skill / Plugin

- Skill entry: [skills/reasonix-orchestrator/SKILL.md](/C:/Projects/codex-reasonix-orchestrator-skill/skills/reasonix-orchestrator/SKILL.md)
- Plugin metadata: [.codex-plugin/plugin.json](/C:/Projects/codex-reasonix-orchestrator-skill/.codex-plugin/plugin.json)

## 💬 Example Prompt

```text
Handle this in Codex Desktop Orchestrator mode.
Task name: example-task

Requirement: describe the task here.
First generate SPEC / ACCEPTANCE / REASONIX_HANDOFF as Brain,
show the summary, then ask for confirmation before Reasonix executes.
```

## 🔒 Safety Boundaries

The workflow does not automatically:

- `git push`
- `git commit`
- `git reset --hard`
- `git clean`
- delete important files
- modify `.env`
- modify keys, certificates, SSH files, or credential files
- install dependencies without explicit approval

Repository validation entrypoints:

- `.\scripts\validate-skill.ps1`
- `./scripts/validate-skill.sh`
- `python scripts/validate_skill.py --repo-root .`

## ❓ FAQ

### Do I need deep Reasonix knowledge?

No. Codex defines the handoff contract, Reasonix executes it, and Codex reviews the result.

### Why not let Codex edit code directly?

Because this workflow intentionally separates planning from execution, which makes review, rollback, and reuse easier.

## 📝 agents/openai.yaml

`skills/reasonix-orchestrator/agents/openai.yaml` is optional agent metadata used to provide a display name, short description, and default prompt text.

## 🙏 Acknowledgements

Inspired by [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix). This repository is not an official Reasonix project and does not imply endorsement.

## 📄 License

Released under the [MIT License](/C:/Projects/codex-reasonix-orchestrator-skill/LICENSE).
