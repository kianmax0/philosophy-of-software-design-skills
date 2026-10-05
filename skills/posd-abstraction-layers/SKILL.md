---
name: posd-abstraction-layers
description: Use when callers at one conceptual level must understand lower-level mechanics or when a layer leaks implementation details into its clients
license: MIT
---

# Abstraction Layers

Use this skill when reviewing a boundary between conceptual levels, such as
application behavior and storage mechanics. A useful layer presents operations
in the vocabulary of its clients and contains the lower-level knowledge needed
to carry them out. A layer is not automatically valuable because it has an
interface or wrapper; its value depends on whether it removes details from the
code above it.

## Inputs and evidence

Inspect the public contract, implementation, dependencies, and representative
callers on both sides of the proposed boundary. Note the concepts and
decisions each side must understand. Trace a normal operation and a failure
path, including how errors and resource lifetimes cross the boundary. Cite
paths with line numbers or named symbols. A pass-through adapter may be
justified when it enforces a real protocol, security, platform, or
compatibility contract.

## Review procedure

1. State each side's responsibility in its own conceptual vocabulary.
2. Find lower-level details used directly by higher-level code: wire formats,
   SQL, file names, vendor types, retry mechanics, or resource cleanup.
3. Verify whether those details are repeated or constrain change. Distinguish
   necessary caller choices from knowledge the lower layer can own.
4. Propose a contract expressed in the higher-level task, then verify the lower
   layer can fulfill it without exposing the mechanics again through return
   values, errors, or configuration.
5. Check dependency direction, error semantics, lifecycle behavior, tests, and
   concrete call sites. Flag tradeoffs if the proposed boundary hides control
   callers actually need.

For a requested change, update the smallest affected boundary and callers,
preserving observable behavior unless explicitly changed. Do not introduce
layers solely to match a diagram or pattern.

## Output

Describe the two conceptual levels, cite the leaked detail and its effect, and
give a focused recommendation or patch. State the contract in terms callers
can use, identify affected call sites, and report relevant checks for
implementation work.

When recommending retention, explain the invariant or adaptation the layer
owns and what knowledge callers would inherit if it were removed. State the
inspected scope and any enforcement paths or dependencies not supplied; do not
claim whole-system correctness from one wrapper.

## Example

Before: a reminder scheduler builds a vendor SDK request, converts timestamps,
and interprets provider error codes. After: it calls
`deliverReminder(recipient, message, dueAt)` on a delivery layer that owns
those mechanics and returns a stable delivery result. Scheduling policy
remains with the scheduler.

## Leave the design alone when

- Higher-level code needs low-level control to satisfy a real requirement.
- The wrapper preserves an important boundary such as authorization or protocol
  compatibility.
- The layer would only rename calls while forwarding all mechanics and failures
  unchanged.
- There is no evidence that the dependency causes duplication, coupling, or
  meaningful change cost.

Principle provenance: John Ousterhout's [Stanford CS190 Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign). The workflow and example here are original adaptations.
