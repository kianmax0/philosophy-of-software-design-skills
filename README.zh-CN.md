# Philosophy of Software Design → AI Skills

[English](README.md) · [来源说明](docs/sources.md) · [行为评估案例](evals/README.md)

将 John Ousterhout《A Philosophy of Software Design》的设计原则转成 coding agent 可执行、可复用的 skills。每个 skill 包含代码检查与设计取舍步骤、限定范围的实施流程、原创示例，以及可验证的产物要求。

适合审查代码改动、设计新接口，以及完成用户要求的重构。重点是说明调用者需要掌握哪些知识、维护者需要协调哪些修改。

这是一个独立项目，已于 2026-10-05 根据提供的 **2021 年第二版完整原书**校准。[来源映射](docs/sources.md)将全书 22 章对应到具体执行流程，并标明章节、节号和 PDF 页码。原书不随仓库分发，运行 skills 无需读取原书。操作流程、示例和 agent 的证据要求由本项目编写，项目与作者无隶属或背书关系。

## 开始使用

先安装 `posd-design-review` 作为审查、设计和实施任务的独立总入口，再按常遇到的问题选择专用 skill。每个文件夹都是独立的 [Agent Skill](https://agentskills.io/specification)，包含 `SKILL.md` 和许可证声明，无需同时安装其他 skill。

在 Codex 中可以这样调用：

```text
使用 $posd-design-review 审查当前 diff，并查看有代表性的调用者。
只报告有实质影响的问题，提供文件和行号、调用者受到的影响、
限定范围的改进建议及其代价。先不要修改文件。
```

针对接口设计：

```text
使用 $posd-design-twice 为批量导入模块比较两种实质不同的接口设计。
明确现有的失败语义和顺序保证，并说明每种设计由谁掌握哪些知识。
```

需要直接实施时：

```text
使用 $posd-strategic-design 添加指定的 importer。
比较直接补丁与调整存储记录知识归属的局部改进，然后实施选定方案。
保留时间转换和写入顺序，更新契约与调用者，报告实际执行的检查。
```

Claude Code 安装后可用 `/posd-design-review` 或 `/posd-design-twice`。显式调用语法及自动发现方式取决于所用的 agent。

## Skill 目录

| Skill | 处理的问题 |
| --- | --- |
| [posd-design-review](skills/posd-design-review/SKILL.md) | 为审查、设计或实施任务选择相关原则 |
| [posd-complexity](skills/posd-complexity/SKILL.md) | 修改放大、认知负担、隐含依赖 |
| [posd-strategic-design](skills/posd-strategic-design/SKILL.md) | 直接补丁与限定范围的设计投入如何取舍 |
| [posd-decide-what-matters](skills/posd-decide-what-matters/SKILL.md) | 区分调用者必需控制的事项与内部选择 |
| [posd-deep-modules](skills/posd-deep-modules/SKILL.md) | 用更简单的调用契约封装有用功能 |
| [posd-information-hiding](skills/posd-information-hiding/SKILL.md) | 让表示方式或策略拥有明确的知识归属 |
| [posd-general-purpose](skills/posd-general-purpose/SKILL.md) | 用简单通用操作减少不必要的专用情况 |
| [posd-abstraction-layers](skills/posd-abstraction-layers/SKILL.md) | 判断抽象层与转发边界是否有实际价值 |
| [posd-pull-complexity-down](skills/posd-pull-complexity-down/SKILL.md) | 下沉共同机制，同时保留调用者的策略选择 |
| [posd-module-boundaries](skills/posd-module-boundaries/SKILL.md) | 按共享知识与不变量决定合并或拆分 |
| [posd-error-design](skills/posd-error-design/SKILL.md) | 简化错误处理，同时保留有意义的失败语义 |
| [posd-design-twice](skills/posd-design-twice/SKILL.md) | 比较接口和职责归属实质不同的方案 |
| [posd-comments](skills/posd-comments/SKILL.md) | 补充代码未表达的意图与契约 |
| [posd-naming](skills/posd-naming/SKILL.md) | 让使用处的语义与关键区别更清楚 |
| [posd-consistency](skills/posd-consistency/SKILL.md) | 保持有意义的一致性，识别合理例外 |
| [posd-obvious-code](skills/posd-obvious-code/SKILL.md) | 揭示非局部假设与意外行为 |
| [posd-performance](skills/posd-performance/SKILL.md) | 根据实测工作负载判断性能设计 |

目录按工程决策组织。“先写注释”是 comments、design-twice 和总入口中的接口设计步骤；修改已有代码由 strategic-design 和注释维护流程处理。第 19 章对继承、模式、getters/setters 和测试的讨论融入相应设计判断。没有一章对应一个 skill 的要求；问题明确时使用专用 skill，需要选择检查方向时使用总入口。

## 安装

将仓库克隆到你选择的位置：

```sh
git clone https://github.com/kianmax0/philosophy-of-software-design-skills.git
cd philosophy-of-software-design-skills
```

Codex 个人使用时，将选中的文件夹复制到 `~/.agents/skills`；项目内使用时，放到目标仓库的 `.agents/skills`。路径依据 [Codex 官方文档](https://learn.chatgpt.com/docs/build-skills)。

```sh
mkdir -p ~/.agents/skills
cp -R -n skills/posd-design-review ~/.agents/skills/
```

Claude Code 个人使用时放到 `~/.claude/skills`，项目内使用时放到 `.claude/skills`。见 [Claude Code 官方文档](https://code.claude.com/docs/en/skills)。

```sh
mkdir -p ~/.claude/skills
cp -R -n skills/posd-design-review ~/.claude/skills/
```

安装整套时，将 `skills/posd-design-review` 换成 `skills/posd-*`。`-n` 会保留已有文件，macOS 跳过这些文件时可能返回退出码 1；更新已安装的 skill 时，应先检查再替换该文件夹。必要时重新启动 agent 或刷新 skill 发现。这些是手动安装说明，尚未验证所有客户端的集成行为。

## 一条有用的审查意见应包含

- 具体位置，以及已查看的调用者或修改场景。
- 造成问题的共享决策、隐含假设或不变量。
- 对行为或维护工作的实际影响。
- 限定范围的改进，以及兼容性或迁移代价。
- 已执行的验证，和建议执行的检查分开说明。

仅凭方法很长、类很小、只有一个实现，或存在转发包装层，不能认定设计有问题。每个 skill 都包含适用边界，使 agent 可以保留有实际价值的现有设计。审查请求只输出建议；用户要求实施时，修改范围遵循原任务。

## 验证与评估

使用 skills 本身无需 Python。维护仓库时，结构检查需要 Python 3.9+ 和 PyYAML：

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 evals/results/verify_implementations.py
```

验证器检查 frontmatter、目录命名、本地链接、独立分发边界，以及评估案例的完整性和技能覆盖；它不评判设计建议。[行为评估案例](evals/README.md)覆盖全部 17 个 skills，包含审查、设计、应保留现状的案例，以及在临时工作区实施改动的任务。执行协议将任务材料与评分标准分开，并保存实际输出。实际结果见评估文档；案例通过不代表已经证明普遍优于普通提示词，也不代表验证了客户端自动发现。

## 贡献与复用

编写要求和评估方法见 [CONTRIBUTING.md](CONTRIBUTING.md)。仓库原创指令、代码和示例采用 [MIT License](LICENSE)。原书及链接的资料保留各自版权，本仓库未包含或重新许可这些资料。
