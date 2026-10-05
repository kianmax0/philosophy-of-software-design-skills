---
name: posd-information-hiding
description: Use when the same change-prone decision appears in multiple modules or a caller depends on another module's representation
license: MIT
---

# Information Hiding

Use this procedure to locate knowledge that should change in one place. Information hiding is ownership of a change-prone decision behind a useful contract; making fields private or adding a wrapper does not establish it by itself.

## Inputs

- The requested behavior/change and the suspected decision, such as a file format, parsing rule, retry policy, storage representation, or protocol detail.
- Relevant module interfaces and implementations, tests, and all discoverable call sites that depend on the decision.
- A concrete example of what changes when that decision changes, if available.

## Procedure

1. Describe the required behavior without naming the current representation or mechanism.
2. Trace where the decision is defined and every place that relies on it. Inspect both visible leakage (public types, signatures, returned collections, defaults, errors) and back-door leakage (multiple implementations independently interpreting the same format or invariant).
3. Check whether the dependency is an actual caller requirement or an implementation detail. A representation remains part of the effective interface when callers must know it to use the module correctly, even if it is private or undocumented.
4. Look for temporal decomposition: separate stages may share knowledge because they happen at different times. Compare the information each stage needs; runtime order alone is not a reason to split modules.
5. Choose the smallest ownership change supported by evidence: combine tightly coupled code, move the decision into one existing owner, or extract a cohesive owner with a genuinely simpler contract. Do not extract a nominal “abstraction” that republishes most of the same knowledge.
6. Keep caller-required choices visible. Check that the new contract does not hide required tuning, lifecycle, security, or error information, and that it avoids broad forwarding layers or hidden global state.
7. In review/read-only mode, report the proposed ownership change without editing files. For an authorized interface change, first draft the contract and expected caller usage; then update only affected modules/callers and preserve behavior unless requested otherwise. Verify actual results by tracing the same dependency and representative success/failure paths again.

## Decision test

The design hides information when a change to the decision can be made at its owner without coordinated edits elsewhere, while callers can still express legitimate needs. Partial hiding can be useful: rare controls can live behind separate operations so ordinary callers need not learn them.

Retain or expose a decision when callers truly need it to meet different requirements, such as meaningful performance tuning. Do not confuse hidden implementation with unknowable behavior: the contract must still explain relevant guarantees and limits.

## Output

Name the decision, its owner, each observed dependency, the edits a change would require today, and the focused boundary change or reason to retain it. Separate observed dependencies from predicted change impact; identify uninspected callers and relevant verification.

## Worked example

Before: a thumbnail job reads `cacheRoot + "/v2/" + imageId + ".bin"`, while cleanup independently reconstructs the same path and version rule. After: both call `thumbnailStore.load(imageId)` / `thumbnailStore.remove(imageId)`; the store owns path layout and versioning. The invariant is that a cache-format change edits one owner, while callers retain the choice of whether a miss triggers regeneration.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Ch. 5 §§5.1–5.10, one-based physical PDF file pages 44–54. This procedure and project-original example are adaptations, not quotations.
