---
name: posd-deep-modules
description: Use when a module's public contract makes callers learn internal sequencing, policy, representation, or failure details
license: MIT
---

# Deep Modules

Use this procedure when an implementation may be carrying complexity that its callers could avoid. Depth compares useful behavior with the knowledge and work imposed by the module's whole contract; file size, method count, and class count are not proxies.

## Inputs

- The requested behavior or change, including explicit compatibility constraints.
- The candidate module's public declarations, implementation, tests, and representative callers.
- At least one normal path and one meaningful edge or failure path, traced through the boundary.

If the repository does not expose a caller, contract, or failure path, name that evidence gap and keep any conclusion provisional.

## Procedure

1. State the job in caller language: what outcome should one operation provide?
2. Inventory the complete caller-facing contract: signatures, defaults, ordering rules, required setup, mutable representations, resource lifetime, errors, and informal constraints. Include every detail a caller must know for correct use.
3. Trace representative callers. Record repeated sequencing, duplicated validation or policy, exposed data structures, and caller code that interprets low-level results. Separate evidence from guesses about future use.
4. Compare that caller burden with the useful capability behind the contract. Ask whether a cohesive operation could own the repeated mechanism and leave genuine product choices to callers.
5. Test the candidate contract against ordinary, edge, and failure paths. A simple-looking contract is false depth if it hides information callers need, makes important behavior unpredictable, or exports that complexity again through configuration, callbacks, return values, or exceptions.
6. In review/read-only mode, report the proposed contract without editing files. For an authorized interface change, first write the proposed contract and expected caller usage; then change the smallest boundary that removes demonstrated caller knowledge. Update only affected callers, preserve observable behavior unless requested otherwise, and avoid unrelated decomposition or consolidation.
7. Verify actual results against the proposed contract at representative call sites, including relevant failure/lifecycle behavior and focused checks. State commands actually run and what they establish.

## Decision test

Prefer the deeper design when it reduces the total knowledge callers must hold and the owning module can implement the behavior coherently. A few general operations may replace many feature-specific ones when callers can plainly compose them. Do not optimize for the shortest call site if it hides behavior the caller must understand.

Retain a small or shallow boundary when it is a necessary protocol/platform adapter, exposes a real caller choice, or would otherwise add indirection without removing any caller burden. Name the specific benefit and the cost callers would incur if it were removed.

## Output

Report the capability, contract elements callers must learn, evidence from callers and paths, proposed or retained contract, affected callers, behavior/compatibility effects, and verification. Mark unverified assumptions explicitly.

## Worked example

Before: three report jobs each create a temporary file, write a header and rows, flush, rename on success, and remove the temporary file on failure. After: a proposed `publishReport(destination, rows)` contract states whether publication is atomic and what failure means; the report module owns that sequence. The invariant is that readers see either the previous complete report or the new complete report, never a partial file. Keep a caller-specific destination choice outside.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Ch. 4 §§4.1–4.8, one-based physical PDF file pages 34–43. This procedure and project-original example are adaptations, not quotations.
