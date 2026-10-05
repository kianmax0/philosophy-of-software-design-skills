---
name: posd-comments
description: Design or review comments that define an abstraction, add precision or intuition, preserve a cross-module decision, or explain non-obvious code.
license: MIT
---

# Comments as design

Use comments to record important information that declarations and nearby code cannot express. They reduce the reader's need to inspect implementations, recover a designer's reasoning, or guess an invariant. A useful comment adds a different level of information; it does not paraphrase a line.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Chapters 12–16, especially §§13.2–13.7, 15.1–15.3, and 16.1–16.6 (PDF file-page numbers, pp. 116–165). The workflow below is an original application of those ideas.

## Procedure

1. **Find the contract and audience.** Read the declaration, implementation, representative callers, tests, and nearby comments. Decide whether the reader is an API caller, a maintainer of the implementation, or an author working across modules. Keep verified behavior distinct from an assumption or historical rationale.
2. **Draft abstraction comments during design.** Before implementing a new module or method, write its interface comment: what it provides, its arguments and result, side effects or failures, and caller obligations. Describe behavior at a level callers need, not the steps used to implement it. If this is hard to state simply, revisit the interface or ownership before coding. Recheck the comment after implementation.
3. **Add precision at declarations.** For fields, arguments, and results, state details not carried by the name or type: units, inclusive/exclusive bounds, null or sentinel meaning, resource ownership and release, and invariants. Describe what a value represents (nouns), not every place that changes it.
4. **Add intuition near decisions.** For a method or code block, explain its overall purpose, why it is needed, or the condition that brings execution here. Use a lower-level comment only when exact semantics matter and cannot be encoded clearly in the type or API. A reader should be able to connect the comment to the code without tracing unrelated modules.
5. **Record cross-module decisions at their owner.** If correctness depends on a rule spanning modules, document the rule where the responsible module's design is visible and point to the other side when useful. Name the dependency, the invariant or ordering rule, and who must preserve it. Avoid scattering duplicate copies that can drift.
6. **Carry requested edits through.** For an implementation request, update the comment and the behavior it documents, then update affected callers/contracts where the interface changed. Run the relevant tests or checks and inspect the diff for stale, duplicated, contradicted, and overly detailed comments. Report edits and verification performed. For review-only requests, recommend changes without editing.

## Decision checks

- Could someone write this comment by looking only at the adjacent code and names? If so, it probably repeats rather than explains.
- Does it give a caller enough information to use the abstraction without reading its implementation? Include the behavior and meaningful constraints, not internal steps.
- Is a claim about units, ownership, failure, ordering, or rationale supported by the implementation, tests, contract, or an owner? Do not convert an unverified guess into documentation.
- Can the code or type make an invariant precise while the comment still records the caller-facing abstraction or design rationale? Use both at their proper levels: types carry enforceable facts; comments preserve the simplified contract and reasoning callers need.

## Example

`// Increment retryCount` above `retryCount++` restates syntax. A useful interface or implementation comment might instead explain that retries share the original request deadline, if the contract and code confirm that rule. Place the rule near the retry policy or API that owns it; do not copy it beside every increment.

## Output

For each proposed comment change, give the location, intended reader, missing or repeated information, exact knowledge to preserve, and evidence supporting its claims. For an implementation request, report files/contracts/callers changed and the relevant tests or checks run, including failures. For review-only work, give bounded recommendations without editing. If rationale is not established, state the uncertainty and identify the owner who can resolve it.
