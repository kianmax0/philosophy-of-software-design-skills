---
name: posd-abstraction-layers
description: Use when adjacent modules expose the same abstraction, forward arguments unchanged, or pass unused values through a call chain
license: MIT
---

# Abstraction Layers

Use this procedure to check whether each layer contributes a distinct capability. Different layers should give callers a different conceptual view; a new interface, wrapper, or argument is useful only when it removes more complexity than it adds.

## Inputs

- The requested behavior/change, boundary contract, implementation, and dependencies.
- Representative callers above the boundary and callees below it.
- A trace of an ordinary path and a failure/resource-lifetime path, including values and errors passed between layers.

## Procedure

1. State what each layer promises in the vocabulary of its clients. Compare those promises with what each layer actually implements.
2. Trace one operation across the boundary. Mark pass-through methods (same arguments and similar signature, with no meaningful selection, policy, validation, or adaptation) and pass-through variables (carried through methods that do not use them).
3. For a pass-through method, ask which class owns the feature. Consider direct access to the implementer, moving functionality to the proper owner, or merging inseparable modules. Retain a forwarding method only when it contributes a real contract such as dispatch, security, compatibility, or policy.
4. Compare the interface abstraction with the implementation representation. A useful layer may expose character ranges while storing lines, or a reliable byte stream while using packets. If callers must reproduce lower-level translation, move that mechanism behind the higher-level contract.
5. For a pass-through value, first check whether a relevant object already has legitimate shared access to producer and consumer. If no such owner exists and several values are genuinely per-instance application state, consider a context object. Avoid a global singleton: it prevents independent instances and complicates tests.
6. Before adopting a context, inventory every proposed field and its consumers. Keep it cohesive, immutable where possible, and no broader than the state that truly spans layers. A context is still global-like shared state: a grab-bag obscures dependencies and mutable state can create thread-safety problems. Keep explicit parameters when they clarify local data flow or prevent hidden coupling.
7. In review/read-only mode, report the proposed boundary without editing files. For an authorized interface change, first draft the contract and expected caller usage; then remove or reshape only the demonstrated boundary. Recheck actual results for ordinary and failure behavior, ownership, dependency direction, independent instances, tests, and compatibility.

## Decision test

Inventory the contract burden added by interfaces, wrappers, arguments, and context fields, then name the complexity each removes. Identical signatures can be valuable for distinct implementations selected by a dispatcher; decorators can be justified when they add substantial behavior or translate an unmodifiable external interface. Similarity alone is a signal to inspect, not an automatic defect.

Retain a layer that enforces a real protocol/security/compatibility boundary, contributes substantial distinct behavior, or protects clients from representation changes. Remove a pure forwarding layer when its callers can reach the actual owner safely and no useful contract would be lost.

## Output

Describe layer responsibilities, traced pass-throughs or abstraction mismatch, caller and failure-path evidence, alternatives considered, chosen contract/value-flow, affected call sites, compatibility tradeoffs, and verification. State why retained adapters/context fields earn their cost.

## Worked example

Before: a report export request's locale and time zone travel through four formatting-neutral functions to a final renderer, which alone uses them. After: if the export pipeline already has a per-export context shared by the renderer and its creator, store the settings there; otherwise, keep explicit inputs if they make dependencies clearer. The invariant is that concurrent exports with different locales cannot affect one another. Do not add a mutable process-wide context; verify two exports independently.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Ch. 7 §§7.1–7.6, one-based physical PDF file pages 67–77. This procedure and project-original example are adaptations, not quotations.
