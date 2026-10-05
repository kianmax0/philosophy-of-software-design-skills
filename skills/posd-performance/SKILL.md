---
name: posd-performance
description: Evaluate a performance-driven code or design change against an explicit workload, measured bottleneck, correctness contract, and reproducible comparison.
license: MIT
---

# Evaluate performance-driven design

Treat performance as a requirement when evidence or an explicit service objective makes it one. A speed claim alone does not justify more configuration, special cases, or a harder-to-understand interface.

## Establish the target

Identify the operation, user-visible latency or throughput objective, workload, input distribution, environment, and correctness contract. Read the affected implementation and callers. For a review, report without editing. Implement only when requested; preserve semantics outside the requested performance behavior.

Ask what measurement demonstrates the bottleneck. Prefer an existing profile, benchmark, production trace, or reproducible workload. Record baseline and candidate with the same inputs and environment, relevant repetitions, and the metric that matters. If no measurement exists, label the suspected bottleneck as a hypothesis and recommend a bounded measurement before adding complexity.

## Inspect the tradeoff

Trace the costly work from the caller through the relevant modules. Determine whether time, memory, I/O, allocation, contention, or another resource dominates under the target workload. Consider whether a simpler ownership or data-flow change can address it before introducing a cache, special fast path, tuning option, or duplicated implementation.

For each proposed optimization, explain:

1. Which measured cost it changes and for which workload.
2. What state, branches, invalidation rules, configuration, or maintenance burden it adds.
3. Whether it preserves results, ordering, error behavior, and resource guarantees.
4. How it performs against the baseline, including regressions in relevant workloads or resource use.

Do not infer that fewer calls or allocations are faster without measurement. Do not trade correctness or an essential contract for an unquantified improvement. Keep a fast path only when its measured benefit is meaningful and its conditions remain understandable.

## Verify and report

Run the relevant benchmark or profile on the same workload and environment when feasible. Verify correctness separately from speed. Report the exact command or harness, workload characteristics, baseline and candidate metrics, variability or limitations, and the semantic checks performed. Distinguish measured results from estimates and hypotheses. If measurements are unavailable, state what evidence would resolve the decision and avoid claiming a speedup.

For repeatable comparisons, record the runtime and relevant machine or service
conditions, input size and distribution, warm-up or cache state, and number of
runs. Use the same harness for both versions. Report variance or a useful range
when results fluctuate; do not present a single noisy run as a reliable gain.
If the target environment differs from the measurement environment, name that
limitation and avoid extrapolating beyond the evidence.

### Example

A developer proposes caching parsed configuration because startup “looks slow.” First profile startup with representative configuration sizes and repeat the baseline. If parsing is not a material cost, leave the cache out. If parsing dominates, compare a cache against reparsing and account for invalidation when configuration changes; verify that both paths produce the same configuration and error behavior.

## Retain simpler behavior

- A speculative speedup is insufficient evidence for extra state or special cases.
- A workload-specific optimization may be valid when the workload is part of the stated requirement.
- Keep the ordinary path clear and make exceptional fast-path assumptions explicit.
- Report resource tradeoffs even when the target latency improves.

## Evidence checklist

- A stated performance objective or a measured user-visible problem.
- A representative workload and comparable baseline.
- A profile or measurement identifying the expensive operation.
- A candidate result plus correctness and contract checks.
- A note about variance, workload coverage, and resource tradeoffs.

Principle provenance: John Ousterhout discusses focusing on significant performance costs in his [Stanford CS190 project review](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=raftReview2). The measurement procedure and workflow here are original adaptations.
