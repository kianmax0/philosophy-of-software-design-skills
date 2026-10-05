---
name: posd-performance
description: Design or review a performance change around an explicit target, measured bottleneck, simple common path, and before/after evidence.
license: MIT
---

# Design for performance without losing simplicity

Favor designs that are naturally efficient and clean. Avoid optimizing every statement: many supposed improvements do not help and add complexity. Also do not ignore known expensive operations or a clear system objective; making a few important design choices early can prevent widespread inefficiency.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Chapter 20, §§20.1–20.5 (PDF file-page numbers, pp. 186–197), especially measurement and critical-path design in §§20.2–20.3. The workflow applies those ideas to a new example.

## Procedure

1. **State the target.** Identify the operation, user-visible latency/throughput or resource goal, common and exceptional input cases, environment, and correctness contract. Record why performance matters: an explicit objective, known expensive operation, profile, or observed problem.
2. **Choose the right scale of evidence.** If the target is not already clear, benchmark or profile representative work. Measure deep enough to identify the specific costs and call path; a slow top-level result alone does not locate the cause. Record the baseline before changing code. For naturally efficient alternatives (for example, hash lookup when ordering is unnecessary), compare the relevant constraints instead of adding tuning machinery without need.
3. **Look for a fundamental fix first.** Consider an algorithm, data-flow, representation, ownership, or I/O change that removes the cost. Prefer it when it is clean and meets the contract. Add hidden implementation complexity only when evidence or a clear requirement justifies it; avoid exposing new interface choices unless callers genuinely own them.
4. **For a measured hot path, define the ideal common path.** Set aside the current structure. Write down the minimum work and data needed for the most common case, including unavoidable operations and checks. Compare the current call chain, layer crossings, repeated tests, and special-case handling with this ideal.
5. **Refactor toward the ideal while keeping useful abstractions.** Remove shallow pass-through layers, redundant checks, and common-path work that exists only for uncommon cases. Keep data and work close to the critical path without exposing implementation detail to callers. Prefer one early guard that detects exceptional conditions; route those cases to a separate slow path that can be organized for clarity. Do not compress code into an opaque fast path.
6. **Measure again and verify semantics.** Use the same harness, workload, environment, and relevant warm-up/cache conditions as the baseline. Repeat enough to expose noise; report variance or a range. Verify results, ordering, errors, ownership, and resource guarantees separately from speed. Keep added complexity only for a meaningful measured gain or a design that also became simpler; otherwise back it out.
7. **Carry out the requested mode.** For an implementation request, make the bounded optimization and update affected callers/contracts; run the benchmark/profile and relevant correctness checks, then report exact commands and results. For review-only work, report evidence and recommendations without editing. If measurement cannot be run, state that plainly and do not claim a speedup.

## Example: value serializer

Suppose a service profile shows that serialization dominates because a common integer field repeatedly enters a general type-dispatch path with checks for rare value kinds. After recording a baseline, compare a direct common-integer path guarded once at entry with the existing general serializer handling uncommon values. Keep the branch only if the representative workload improves and outputs, errors, and encoding remain identical; report the actual measured result rather than inferring a gain from fewer calls.

## Report

Give the objective and workload, measurement command/harness, baseline and candidate results, environment and variability, the identified cost, the common-path change and exceptional path, correctness checks, and resource or maintenance tradeoffs. Distinguish measured results from estimates and hypotheses. If the evidence is missing, specify the bounded measurement needed before claiming a speedup.
