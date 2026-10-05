---
name: posd-module-boundaries
description: Use when deciding whether to combine or separate code that shares knowledge, must be used together, duplicates work, or changes independently
license: MIT
---

# Module Boundaries

Use this procedure at function, class, and service boundaries. Choose the arrangement that gives the system the simplest total contracts and least duplicated knowledge. Fewer files or shorter functions alone do not make a better boundary.

## Inputs

- The requested scope and behavior, including compatibility constraints.
- Candidate declarations, implementations, tests, and representative call paths.
- Knowledge/invariants each part owns, how users invoke them, and which changes require coordinated edits.

## Procedure

1. Describe each part's responsibility and trace one ordinary path plus relevant failure, state, transaction, or lifecycle behavior.
2. Look for reasons to bring code together: shared change-prone information, bidirectional use together, a clear shared conceptual category, difficult cross-reading, repeated policy, or interfaces that divide one solution into caller-managed steps.
3. Look for reasons to keep code apart: independent responsibilities, distinct reasons/lifetimes/consumers, or a general-purpose mechanism that should not know one feature's policy. “Used together” is strongest when use is bidirectional; a block cache using a hash table does not mean hash tables belong in the cache.
4. Compare whole-system costs on both sides: interfaces added or removed, cross-calls, duplicated knowledge, caller sequencing, implementation clarity, state representation, compatibility, and ability to evolve separately.
5. For methods, do not split by a line limit. Extract a helper when it is a separable subtask a reader can understand without its parent and the parent can use without reading the helper's implementation. A one-off helper that just logs the caller's error often adds an interface and forces cross-reading; a tiny helper can still earn its place when it names a meaningful concept, is reused, or owns an invariant.
6. Split a public operation into multiple operations only when the original combines unrelated tasks and most callers can use the simpler operations independently. If callers must invoke both and shuttle state between them, the split likely worsens the contract. Join methods/classes when that removes interfaces, duplication, dependencies, or shared knowledge leakage.
7. In review/read-only mode, report the proposed boundary without editing files. For an authorized interface change, first draft the contract and expected caller usage; then change only the relevant boundary and affected callers. Preserve observable behavior unless requested otherwise, and verify actual results for each call path and relevant focused checks.

## Decision test

Ask which decision or invariant would become local, which interfaces vanish or appear, and whether readers can understand each part independently. Keep the split if a coherent contract lets parts evolve independently; combine when the boundary only distributes a single idea across places that must be read and changed together.

Retain separate general-purpose and special-purpose parts when they represent different conceptual levels. Do not merge merely because two values are related or often manipulated in the same workflow. Do not split merely because an implementation is long or has sequential phases.

## Output

For a review, report evidence, shared versus independent knowledge, combine/separate comparison, recommendation, and tradeoffs. For implementation, add the changed boundary, affected callers, compatibility effects, and focused verification. Identify incomplete call-site evidence.

## Worked example

Before: `buildMonthlyReport` is split into `readRows`, `filterRows`, `sumRows`, and `appendRows`; each helper has a coupled state parameter and none has another use. After: keep this cohesive report operation together if readers must follow the shared filtering/aggregation state; extract a helper only for a separable, meaningful subtask such as date-range validation. The invariant is that filtering and summation use the same normalized interval. If another report truly shares that rule, move it behind a clear contract with callers evidence.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Ch. 9 §§9.1–9.9, one-based physical PDF file pages 82–95. This procedure and project-original example are adaptations, not quotations.
