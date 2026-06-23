# Reasonix Orchestrator

这是一个给 `Codex Desktop + Reasonix CLI` 工作流准备的可复用 Skill / Plugin。

它解决的是一个很实际的问题：

很多人希望 `Codex` 先把事情想清楚、拆清楚、讲清楚，再交给另一个执行器去真正改代码，而不是一上来就让 AI 直接动手。

这套工作流就是为这个目的准备的。

* `Codex Desktop` 负责规划、确认、验收
* `Reasonix CLI` 负责按交接文件执行代码修改
* 用户只需要在 `Codex Desktop` 里提需求和确认

**如果你是第一次接触这套流程，先记住这一句话：**

用户只在 Codex Desktop 里提需求和确认；Codex 负责规划和验收；Reasonix 只负责按 Codex 的交接文件执行代码修改。

## 它到底是怎么分工的

你可以把它想成两个人配合干活：

### Codex Desktop

它是：

* 大脑
* 总指挥
* 验收官

它负责：

* 理解你的需求
* 把任务拆清楚
* 生成交接文件
* 在执行前问你要不要继续
* 在执行后检查结果
* 给出最终判断

### Reasonix CLI

它是：

* 手
* 执行者

它负责：

* 读取 Codex 生成的任务文件
* 按范围修改代码
* 运行需要的验证
* 写出执行报告

## 这套流程最适合谁

如果你符合下面这些情况，这个项目就很适合你：

* 你主要使用 `Codex Desktop`
* 你不想让 AI 直接跳过规划就改代码
* 你希望“谁负责想、谁负责做、谁负责验收”分得很清楚
* 你希望任务过程有明确的 Markdown 交接文件，方便复查和重跑
* 你想把同一套工作流复用到不同项目里

如果你希望 `Codex Desktop` 负责规划和验收、`Reasonix CLI` 负责执行，并且中间保留明确的确认环节，那这套模式很适合你。

如果你更想要的是“不经过交接文件、不经过确认、让同一个 AI 自己一路直接改到尾”，那这套模式可能不适合你。

## 3 分钟快速开始

如果你想先跑通一遍，按下面做就可以。

如果你只是想先用起来，不用先看完全部细节。

1. 下载或 clone 这个仓库
2. 把 `skills/reasonix-orchestrator/` 放到你的 Codex skills 目录
3. 打开你真正要工作的目标项目
4. 在 `Codex Desktop` 里让它安装这套 workflow
5. 跑一次 smoke-test，确认流程能通

### Skills 目录放哪里

常见位置：

```text
~/.codex/skills/reasonix-orchestrator/
```

Windows 用户通常可以理解成自己用户目录下的：

```text
.codex\skills\reasonix-orchestrator\
```

如果你使用了自定义 `CODEX_HOME`，那就放到对应的 `skills/` 目录里。

## 正常使用时，你只需要这样做

打开 `Codex Desktop`，直接发这样的请求：

```text
按 Codex Desktop Orchestrator 模式处理。

任务名：example-task

需求：这里写你的需求。

请先作为 Brain 生成 SPEC / ACCEPTANCE / REASONIX_HANDOFF，展示摘要后问我是否确认交给 Reasonix 执行。
```

如果你愿意写得更完整，也可以继续补：

* 范围
* 不要改什么
* 验收标准

但对大多数人来说，上面那段模板已经够用了。

## 整个流程是怎么跑的

```text
你
 ↓
Codex Desktop 规划
 ↓
生成 SPEC / ACCEPTANCE / HANDOFF
 ↓
你确认
 ↓
Codex 调用 ai-hand.ps1
 ↓
Reasonix 执行
 ↓
Codex 审查
 ↓
PASS / REVISE / REJECT
```

这里最重要的 5 条规则是：

1. `Codex Desktop` 是正常的 `Brain / Judge / Orchestrator`
2. `Reasonix CLI` 是正常的 `Hand / Executor`
3. 正常入口只有：

```powershell
.\scripts\ai-hand.ps1 "<task-slug>"
```

4. 不使用 `ai-chain.ps1` 作为正常入口
5. 不使用 `codex` CLI 做 `Brain / Judge`

## 安装到目标项目后，会多出什么

这套 workflow 安装到目标项目后，通常会加入这些文件：

* `AGENTS.md`
* `.ai/tasks/README.md`
* `.ai/prompts/reasonix-hand.md`
* `.reasonix/system-hand.md`
* `scripts/ai-hand.ps1`

它们的作用可以简单理解成：

* `AGENTS.md` 负责讲清楚谁干什么
* `SPEC / ACCEPTANCE / HANDOFF` 负责交接任务
* `ai-hand.ps1` 负责调用 `Reasonix CLI`
* `EXECUTION_REPORT.md` 负责记录执行结果

## Smoke Test

第一次装好以后，建议先用一个很小的测试任务试跑，不要直接拿重要需求上来就跑。

最简单的 smoke-test 可以这样做：

1. 打开一个目标项目
2. 在 `Codex Desktop` 里发一个很小的测试请求
3. 确认 `Codex Desktop` 先生成：
   * `SPEC.md`
   * `ACCEPTANCE.md`
   * `REASONIX_HANDOFF.md`
4. 确认它先问你是否执行
5. 确认执行时走的入口是：

```powershell
.\scripts\ai-hand.ps1 "<task-slug>"
```

6. 确认 `Reasonix CLI` 执行后写出了：

```text
.ai/tasks/<task-slug>/EXECUTION_REPORT.md
```

7. 确认最后由 `Codex Desktop` 读取结果，并给出：

* `PASS`
* `REVISE`
* `REJECT`

如果你之后还想继续调整这套流程，再看后面的说明。

如果你要维护或扩展这套 Skill，可以继续往下看：

* [skills/reasonix-orchestrator/references/test-checklist.md](skills/reasonix-orchestrator/references/test-checklist.md)

## 安全边界

这套工作流默认不会自动做下面这些危险操作：

* `git push`
* `git commit`
* `git reset --hard`
* `git clean`
* 删除重要文件
* 修改 `.env`
* 修改密钥、证书、SSH、凭据文件
* 自动安装依赖，除非用户明确批准

换句话说，它默认不会：

* 偷偷帮你提交代码
* 偷偷帮你推到远端
* 偷偷清空工作区
* 偷偷去碰配置和凭据
* 绕过你，直接让 `Reasonix` 自己决定怎么做

## FAQ

### 我需要会 Reasonix 吗？

不需要很熟。

普通用户只要知道一件事：真正改代码的是 `Reasonix CLI`，但你主要打交道的还是 `Codex Desktop`。

### 为什么不直接让 Codex 改代码？

因为很多人更希望把“想清楚怎么做”和“真的去动代码”拆开。

这样有几个好处：

* 先规划，后执行
* 先确认，后落地
* 过程更容易检查
* 出问题更容易回滚和重跑

### 为什么要保留 SPEC / ACCEPTANCE / HANDOFF？

因为它们就是交接合同。

这些文件能帮你明确：

* 这次到底要做什么
* 做到什么算完成
* Reasonix 可以动哪些内容
* 哪些内容不能碰

这比“全靠聊天上下文记忆”稳得多。

### 为什么不使用 ai-chain.ps1？

因为这套模式强调：

* 用户确认要留在 `Codex Desktop`
* 正常的 Brain / Judge 也要留在 `Codex Desktop`

`ai-chain.ps1` 可以保留，但它不是这套工作流的正常入口，只是 `legacy / fallback`。

### Reasonix 改错了怎么办？

这正是为什么最后还要让 `Codex Desktop` 来审查。

如果改错了，正常做法是：

* 由 `Codex Desktop` 给出 `REVISE` 或 `REJECT`
* 收紧 `SPEC / ACCEPTANCE / HANDOFF`
* 再决定是否重新执行

### 这个 Skill 会不会自动提交或推送代码？

不会。

默认不会自动：

* commit
* push
* reset
* clean

这些都被当成危险操作处理。

## 给准备继续维护这套 Skill 的人看的入口

如果你要维护或扩展这套 Skill，可以从这里继续往下看：

* [skills/reasonix-orchestrator/SKILL.md](skills/reasonix-orchestrator/SKILL.md)
* [skills/reasonix-orchestrator/references/workflow-details.md](skills/reasonix-orchestrator/references/workflow-details.md)
* [skills/reasonix-orchestrator/references/file-contracts.md](skills/reasonix-orchestrator/references/file-contracts.md)
* [skills/reasonix-orchestrator/references/reasonix-hand-contract.md](skills/reasonix-orchestrator/references/reasonix-hand-contract.md)
* [skills/reasonix-orchestrator/references/plugin-packaging.md](skills/reasonix-orchestrator/references/plugin-packaging.md)
* [skills/reasonix-orchestrator/references/test-checklist.md](skills/reasonix-orchestrator/references/test-checklist.md)

---

## English

Reasonix Orchestrator is a reusable Codex Skill / Plugin for teams who want:

* `Codex Desktop` to act as the normal `Brain / Judge / Orchestrator`
* `Reasonix CLI` to act as the normal `Hand / Executor`
* a fixed execution entrypoint:

```powershell
.\scripts\ai-hand.ps1 "<task-slug>"
```

* no normal use of `ai-chain.ps1`
* no normal use of `codex` CLI for `Brain / Judge`

In short:

* the user talks to `Codex Desktop`
* `Codex Desktop` plans and reviews
* `Reasonix CLI` executes code changes from the generated handoff files

For detailed documentation, see:

* [skills/reasonix-orchestrator/SKILL.md](skills/reasonix-orchestrator/SKILL.md)
* [skills/reasonix-orchestrator/references/](skills/reasonix-orchestrator/references/)
