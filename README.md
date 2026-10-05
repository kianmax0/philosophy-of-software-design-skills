# Philosophy of Software Design → AI Skills

[简体中文](README.zh-CN.md) · [Sources](docs/sources.md) · [Evaluation cases](evals/README.md)

Reusable coding-agent skills grounded in John Ousterhout's *A Philosophy of Software Design*. Each skill turns a design principle into a concrete inspection and decision procedure, a bounded edit workflow, an original example, and verifiable outputs.

Use them to review a diff, design a new interface, or complete a requested refactor. Findings should explain the knowledge callers must carry and the changes maintainers must coordinate.

This is an independent project, calibrated against the supplied complete **2021 second edition** on 2026-10-05. The [source map](docs/sources.md) connects all 22 chapters to operational workflows and gives chapter/section and PDF-page locators. The book is not bundled or needed at runtime. Procedures, examples, and agent-specific evidence requirements are project adaptations; the project is not affiliated with or endorsed by the author.

## Start here

Install `posd-design-review` as the standalone entrypoint for review, design, and requested implementation. Add specialized skills for recurring design problems. Each folder is a standalone [Agent Skill](https://agentskills.io/specification) containing `SKILL.md` and its license notice; no other skills or tools are required by these instructions.

Example request in Codex:

```text
Use $posd-design-review to review the current diff.
Inspect representative callers. Report material findings with file/line evidence,
caller consequences, a bounded recommendation, and its tradeoff. Do not edit files.
```

Example request for a focused design task:

```text
Use $posd-design-twice to compare two materially different interfaces for
the batch importer. Keep existing failure and ordering guarantees explicit.
```

For an implementation task:

```text
Use $posd-strategic-design to add the requested importer.
Compare a direct patch with a bounded improvement to record ownership,
then implement the selected design. Preserve timestamp conversion and ordering,
update the contract/callers, and report the checks you actually ran.
```

For Claude Code, use `/posd-design-review` or `/posd-design-twice` after installation. Explicit invocation syntax and automatic discovery depend on the agent.

## Skills

| Skill | Use it to |
| --- | --- |
| [posd-design-review](skills/posd-design-review/SKILL.md) | Review, design, or implement with relevant principles |
| [posd-complexity](skills/posd-complexity/SKILL.md) | Trace change amplification, cognitive load, and hidden dependencies |
| [posd-strategic-design](skills/posd-strategic-design/SKILL.md) | Compare a direct patch with a bounded design investment |
| [posd-decide-what-matters](skills/posd-decide-what-matters/SKILL.md) | Separate essential caller controls from internal choices |
| [posd-deep-modules](skills/posd-deep-modules/SKILL.md) | Put useful behavior behind a simpler caller contract |
| [posd-information-hiding](skills/posd-information-hiding/SKILL.md) | Give a representation or policy one knowledgeable owner |
| [posd-general-purpose](skills/posd-general-purpose/SKILL.md) | Replace needless special cases with a simple useful operation |
| [posd-abstraction-layers](skills/posd-abstraction-layers/SKILL.md) | Assess layer value and justified forwarding boundaries |
| [posd-pull-complexity-down](skills/posd-pull-complexity-down/SKILL.md) | Absorb shared mechanism without taking away caller policy |
| [posd-module-boundaries](skills/posd-module-boundaries/SKILL.md) | Join or separate code around shared knowledge and invariants |
| [posd-error-design](skills/posd-error-design/SKILL.md) | Simplify failures while preserving meaningful error semantics |
| [posd-design-twice](skills/posd-design-twice/SKILL.md) | Compare different ownership and interface designs |
| [posd-comments](skills/posd-comments/SKILL.md) | Document intent and contracts missing from the code |
| [posd-naming](skills/posd-naming/SKILL.md) | Make semantics and distinctions clear at use sites |
| [posd-consistency](skills/posd-consistency/SKILL.md) | Preserve meaningful conventions and justified exceptions |
| [posd-obvious-code](skills/posd-obvious-code/SKILL.md) | Reveal nonlocal assumptions and surprising behavior |
| [posd-performance](skills/posd-performance/SKILL.md) | Evaluate design changes against a measured workload |

The catalog groups principles by engineering decision. Comments-first is an interface-design step in comments, design-twice, and the entrypoint; modifying existing code belongs in strategic design and comment maintenance. Chapter 19's treatment of inheritance, patterns, getters/setters, and tests is integrated into those decisions. There is no one-skill-per-chapter requirement. Choose a focused skill for a known problem; use the entrypoint when deciding which checks matter.

## Install

Clone this repository into a location of your choice:

```sh
git clone https://github.com/kianmax0/philosophy-of-software-design-skills.git
cd philosophy-of-software-design-skills
```

For personal use in Codex, copy the selected folders into `~/.agents/skills`. For project use, place them in `.agents/skills` inside your target repository. These locations follow the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills).

```sh
mkdir -p ~/.agents/skills
cp -R -n skills/posd-design-review ~/.agents/skills/
```

For personal use in Claude Code, use `~/.claude/skills`; for project use, use `.claude/skills`. See the [Claude Code skill documentation](https://code.claude.com/docs/en/skills).

```sh
mkdir -p ~/.claude/skills
cp -R -n skills/posd-design-review ~/.claude/skills/
```

To install the entire collection, replace `skills/posd-design-review` with `skills/posd-*`. The `-n` option preserves existing files; macOS may return exit status 1 when it skips them. Updating an existing installation requires reviewing and replacing that folder deliberately. Restart or refresh your agent's skill discovery if needed. These are manual installation instructions; integration with every client has not been tested.

## What a useful finding contains

- A concrete location and an inspected caller or change scenario.
- The shared decision, hidden assumption, or invariant causing the problem.
- The consequence for behavior or maintenance.
- A bounded improvement and its compatibility or migration cost.
- Verification actually performed, separated from proposed checks.

A long method, small class, single implementation, or forwarding wrapper alone is insufficient evidence. The skills include contextual exceptions so an agent can retain a design that serves its purpose. Reviews produce recommendations; requested implementation work stays within the user's scope.

## Validate and evaluate

Skill usage itself has no Python dependency. Repository maintenance checks require Python 3.9+ and PyYAML:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 evals/results/verify_implementations.py
```

The validator checks frontmatter, folder names, local links, standalone packaging, and evaluation-corpus integrity/coverage. It does not grade recommendations. The [behavioral corpus](evals/README.md) covers all 17 skills, with review/design cases, retain-design cases, and isolated implementation tasks. Its run protocol separates raw tasks from grading criteria and preserves actual responses. See the recorded results there; case success does not establish general superiority over an ordinary prompt or installed-client discovery.

## Contribute and reuse

See [CONTRIBUTING.md](CONTRIBUTING.md) for the skill contract and evaluation expectations. Original repository instructions, code, and examples use the [MIT License](LICENSE). The book and linked source materials retain their own copyrights and are not included or licensed by this repository.
