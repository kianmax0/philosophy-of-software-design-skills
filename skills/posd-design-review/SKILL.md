---
name: posd-design-review
description: Review a diff or module, design a new interface, or carry out a requested design refactor using Ousterhout's complexity and knowledge-ownership principles.
license: MIT
---

# Apply software design principles to the task

Deliver the user's requested review, design, or code change. Work from concrete caller tasks and knowledge ownership. This skill works alone; specialized skills can deepen a relevant decision when installed.

## Establish the task and evidence

Read repository instructions, working-tree state, the target code/proposal, contracts, representative callers, and relevant tests. For a new design, use required caller operations from the request and label assumptions instead of demanding nonexistent code evidence. If the target cannot be inferred, request the missing target.

Choose the work mode from the user's request:

- **Review:** inspect and report supported findings without editing.
- **Design:** compare plausible structures and deliver a chosen interface/ownership sketch with a contract and verification strategy.
- **Implement/refactor:** select a supported design improvement, make the in-scope changes, update callers and documentation, and run meaningful checks. A report or sample alone does not finish this mode.

Preserve existing behavior beyond the requested change and respect compatibility constraints. The skill does not add stage approvals to already authorized work.

## Walk the caller's task

Trace a common operation and a meaningful boundary/failure case. Record what callers must know: units, representation, configuration, ordering, ownership, side effects, and error semantics. Trace one supported change scenario to see which modules must agree.

Distinguish change amplification, cognitive load, and unknown unknowns from their causes: dependencies and obscurity. Prioritize common use and frequently modified paths. A red flag prompts investigation and an alternative; it does not establish a defect by itself.

## Select the relevant design checks

Use only the checks that affect the task. The questions below are executable without another installed skill.

| Signal | Inspect and compare | Optional depth |
| --- | --- | --- |
| Coordinated edits or surprising effects | Trace the shared decision and hidden dependency; make it local or discoverable | `posd-complexity` |
| Another workaround added by a patch | Sketch the design as if this requirement had existed initially; choose a bounded improvement | `posd-strategic-design` |
| Numerous choices, hidden essential rules | Remove unneeded choices and emphasize necessary distinctions in contracts and structure | `posd-decide-what-matters` |
| Caller orchestrates low-level steps | Compare the full formal/informal contract with the useful behavior it hides; simplify common use | `posd-deep-modules` |
| Format/policy known in several modules | Assign that decision one owner; test whether a representation change leaves callers unchanged | `posd-information-hiding` |
| Many named special operations | Try a small somewhat general operation against actual caller tasks; separate specialized policy | `posd-general-purpose` |
| Forwarding layers or parameters | Identify each layer's different abstraction/invariant; consider collapse or a scoped context while checking coupling | `posd-abstraction-layers` |
| Repeated caller mechanism/configuration | Move the difficulty to the owner capable of solving it; preserve essential caller policy | `posd-pull-complexity-down` |
| Split invariants or unrelated responsibilities | Join shared knowledge; separate independent/general and specialized code; test method conceptual completeness | `posd-module-boundaries` |
| Repetitive or ambiguous failure paths | Consider contract elimination, complete internal recovery, boundary aggregation, or justified termination; keep meaningful failures visible | `posd-error-design` |
| First plausible design chosen immediately | Sketch a different interface or implementation; walk the same operations and compare caller burden | `posd-design-twice` |
| Contract cannot be understood from interface | Write missing precision/intent independently of implementation; use draft comments to expose design problems | `posd-comments` |
| Ambiguous identifier at use sites | Match a precise semantic name against all uses; revisit entities that are hard to name | `posd-naming` |
| Similar operations behave unexpectedly differently | Identify the existing convention and meaning, preserve it or explain a real semantic exception | `posd-consistency` |
| Correctness needs nonlocal interpretation | Make control/data effects visible where read; test understanding without reconstructing internals | `posd-obvious-code` |
| Speed justifies exposed complexity | Use a workload and before/after measurements; simplify the critical path with a clear slow path | `posd-performance` |

Do not load the entire collection for a small task. Judge patterns, inheritance, getters/setters, and development processes by the dependencies they remove or expose; adopting a named technique is not evidence of simpler design. Interface reuse can help while shared mutable implementation state can leak knowledge. Tests support refactoring; passing tests alone does not establish a good abstraction.

## Compare and execute

For a consequential decision, sketch materially different alternatives with the same required behavior. Compare the common caller sequence, knowledge exposed/hidden, useful generality, ownership, implementation cost, and migration. When neither alternative is satisfactory, use their weaknesses to seek a better design. Consider retaining the current design.

Before implementing a new or changed interface, draft its contract comment: semantics, input/output precision, side effects, failures, and lifecycle constraints. Keep implementation mechanics separate. A long or hard-to-explain contract is feedback to simplify the design, not an invitation to write around it.

For requested code changes, implement the chosen design and migrate affected consumers. Keep lasting rationale near its code owner, update stale comments, and verify the contract at the changed boundary. Do not freeze a sketch when implementation reveals a better design.

## Output and verification

Lead with the assessment/decision and inspected scope. For each material review finding give location, caller/change scenario, dependency or obscurity, consequence, bounded recommendation, and tradeoff. Merge findings with the same cause. Distinguish observed defects, demonstrated maintenance burdens, and uncertain concerns. If no material finding is supported, explain what invariant or useful boundary earns its place.

For design requests, provide the compared sketches and chosen contract. For implementation, deliver the code and describe caller/contract changes with commands and actual results. Separate proposed checks from checks run; identify uninspected consumers when they limit confidence.

Do not infer poor design merely from a long method, small class, single implementation, or wrapper. Do not invent complexity scores or demand a fixed finding count.

Source: Ousterhout, *A Philosophy of Software Design*, second edition (2021), ch. 1 §1.1 (PDF pp. 17–18), chs. 2–11 (pp. 19–115), chs. 12–21 (pp. 116–201), ch. 22 (pp. 202–203). PDF pages are one-based file pages, not printed page numbers. [Author's book page](https://web.stanford.edu/~ouster/cgi-bin/book.php). Routing, evidence requirements, procedures, and examples are project-authored adaptations.
