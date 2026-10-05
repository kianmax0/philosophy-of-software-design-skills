---
name: posd-general-purpose
description: Use when an interface is shaped around one feature or when similar callers duplicate operations through a lower-level API
license: MIT
---

# General-Purpose Modules

Use this procedure when a module may encode one caller's special case instead of a coherent capability. Aim for “somewhat general-purpose”: implement the functionality current needs require, with an interface that can serve multiple related uses without making today's use awkward.

## Inputs

- The requested change and the concrete use cases in scope.
- The candidate contract and implementation, plus tests and current call sites.
- For each evidenced use case: outcome, caller knowledge, policy choices, and any request or test that establishes the need.

## Procedure

1. Describe the shared capability as an outcome, not as the current UI action or caller sequence.
2. Compare concrete use cases. Identify feature-specific operations (for example `backspace`, `deleteSelection`) that could be expressed through a smaller set of domain-level operations, and also identify low-level APIs that would force callers into loops or repeated mechanics.
3. Propose the simplest contract covering the established needs. Reducing operation count is useful only if each operation remains simple; a single operation with many flags, callbacks, modes, or coupled arguments can be more complex than several clear operations.
4. Check today's use case for friction: estimate the caller code and duplicated policy the general contract requires. If it makes ordinary use cumbersome or inefficient, add the missing capability rather than pursuing minimal signatures as an end in themselves.
5. Place unavoidable specialization deliberately. Push it upward into feature code when the feature's semantics should remain visible there. Push it downward into a specialized adapter/driver when that module translates a specific device or external protocol into a stable general contract for the core. Do not let specialization leak across unrelated layers.
6. In review/read-only mode, report the proposed contract without editing files. For an authorized interface change, first draft the contract and expected caller usage; then change only the implicated contract and callers. Preserve existing behavior unless the request authorizes change, compare interface and implementation complexity, and verify actual results for the task and relevant failures.

## Decision test

The interface can be more general than the immediate feature while the implementation includes only functionality needed for today's task. Prefer a simple, broadly meaningful operation that makes today's use clear and avoids baking a UI gesture or caller sequence into a lower-level contract. Do not add speculative functionality or options. Generality does not require evidence of multiple current callers or planned reuse.

Retain a purpose-specific API when it names an essential domain operation, or when a broader contract makes today's use harder or requires unsupported choices. A single current caller alone is not a reason to reject a simple general interface. Do not build a framework, unused hooks, or speculative options.

## Output

Report the evidenced cases and their sources, the common capability, candidate contract and why it remains easy for current use, where specialization belongs, affected callers, compatibility effects, and verification. Identify any speculative case separately.

## Worked example

Before: the first consumer is a dashboard's “clear selected readings” action, and the time-series store exposes `clearChartSelection(view)`, learning about UI state. After: the store offers `remove_interval(start, end)` with an explicit endpoint contract; the dashboard translates its selection to that interval. The store owns deletion while the UI owns selection. Implement only the interval operation needed today; do not add future query/filter features. A single current caller can justify this cleaner interface.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Ch. 6 §§6.1–6.9, one-based physical PDF file pages 55–66. This procedure and project-original example are adaptations, not quotations.
