---
name: posd-design-review
description: Review a concrete diff, module, or design using Ousterhout-inspired complexity principles and select the relevant design checks without expanding the requested scope.
license: MIT
---

# Review software design

Produce a small set of supported findings that explain how a design affects callers and future changes. This entrypoint works on its own; separately installed specialized `posd-*` skills can deepen an applicable check.

## Establish scope and evidence

Identify the diff, module, or proposal requested for review. Inspect the relevant code, contracts, representative callers, and existing verification. Read repository instructions and working-tree state before any requested edits. If no target is supplied and none can be inferred, ask for the target instead of reviewing an arbitrary repository.

For review requests, report findings without editing. If refactoring is explicitly requested, choose a supported improvement within that scope and preserve behavior outside the requested change. A design review does not authorize a repository-wide rewrite.

## Select checks

Start with a concrete caller task or change scenario. Apply only checks that bear on it:

| Evidence or question | Check | Optional specialized skill |
| --- | --- | --- |
| One change requires coordinated edits or hidden knowledge | Trace shared decisions and implicit dependencies | `posd-complexity` |
| A patch adds another workaround or special case | Compare patch cost with a bounded design improvement | `posd-strategic-design` |
| Many public choices do little for callers | Identify essential controls and internal choices | `posd-decide-what-matters` |
| Callers orchestrate low-level implementation steps | Evaluate capability behind the full caller contract | `posd-deep-modules` |
| Representation or policy appears across modules | Find an owner that can hide the shared decision | `posd-information-hiding` |
| Similar operations proliferate as named special cases | Consider a simple general operation with real use cases | `posd-general-purpose` |
| Layers expose the same concepts or only forward calls | Check abstraction value and justified boundary roles | `posd-abstraction-layers` |
| Every caller solves the same difficult problem | Move shared mechanism to its knowledgeable owner | `posd-pull-complexity-down` |
| An invariant is split or unrelated responsibilities are coupled | Compare joining and separating around shared knowledge | `posd-module-boundaries` |
| Failures require repetitive or ambiguous handling | Simplify the failure contract without hiding failures | `posd-error-design` |
| The proposed interface has no credible alternative | Compare two materially different ownership choices | `posd-design-twice` |
| Important intent, units, or side effects are hard to discover | Document knowledge missing from code | `posd-comments` |
| A name admits several interpretations at its uses | Test a precise name against actual semantics | `posd-naming` |
| Similar operations surprise readers in different ways | Identify the invariant convention and valid exception | `posd-consistency` |
| Correctness depends on nonlocal or implicit interpretation | Make relevant behavior visible at the reading site | `posd-obvious-code` |
| A design choice is justified by speed | Require a workload, measurement, and preserved contract | `posd-performance` |

If a specialized skill is unavailable, use the check in this table directly. Do not assume sibling files exist or load every skill just because a broad review was requested.

## Assess findings

Read enough surrounding code to explain the issue. Give a path and line, representative caller, violated or obscured invariant, and concrete consequence. Distinguish an observed defect, a demonstrated maintenance burden, and a speculative concern.

Recommend a change that removes or localizes knowledge, then account for the knowledge it introduces. Consider leaving the design intact. Long methods, many classes, a single implementation, or the presence of wrappers are insufficient evidence by themselves. A wrapper can earn its place through authorization, adaptation, observability, compatibility, or independent lifecycle.

Merge findings with the same cause. Lead with correctness and demonstrated caller burden. Do not invent numerical design scores, demand a fixed number of findings, or fill a report with cosmetic preferences.

## Output and verification

Give the inspected scope and a concise overall assessment. For each material finding provide location, evidence, consequence, recommendation, and tradeoff. Report uncertainty or uninspected consumers where it affects the conclusion. If no material issue is supported, say so.

For requested edits, summarize what changed and verify meaningful behavior at the affected boundary. Report checks actually run and their results; distinguish proposed verification from completed verification.

Principle provenance: John Ousterhout's [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php). The routing, review workflow, and evidence requirements here are original adaptations.
