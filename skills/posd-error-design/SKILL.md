---
name: posd-error-design
description: Use when callers catch, retry, suppress, translate, or duplicate handling for a module's exceptional outcomes
license: MIT
---

# Error Design

Use this procedure to reduce the number of places that must handle failures while preserving outcomes callers need. An exception, error return, sentinel, or status branch all count as an exceptional path when they disrupt normal control flow.

## Inputs

- The requested operation and promised postcondition.
- The contract, implementation, tests, representative callers, and handlers from origin to the user/system boundary.
- For each failure: trigger, affected state, existing recovery, stop/continue behavior, and information available to the next layer.

## Procedure

1. Trace concrete normal and failing executions through caller and handler. Classify each condition: valid already-satisfied state, invalid request, expected absence, transient dependency problem, partial completion, violated invariant/defect, or fatal resource failure. A catch does not prove recoverability.
2. Choose among the four techniques below; they solve different problems. State explicitly whether the operation continues, completes its promised postcondition, aborts a request, or terminates the process.
3. **Define the error out of existence** when a broader, natural postcondition makes the condition ordinary. Example: `ensureAbsent(key)` can succeed if the key is already absent. Do not reinterpret an invalid request, permission denial, data loss, or incomplete required action as success merely to avoid a handler.
4. **Mask the exception inside the owning lower-level module** only when that module can complete the promised result and callers have no useful action to take. Bound/reason about retries, idempotency, cancellation, and waiting semantics. Keep failures observable when callers need them for robustness or recovery; never catch and continue with corrupted/unknown state.
5. **Aggregate exceptions at a higher-level boundary** when many lower-level failures have the same recovery/response, such as aborting one request, restoring its state, producing one error response, and continuing with the next request. Keep the specific cause/category/context from the source so the boundary can respond correctly. Distinguish request-scoped aborts from failures fatal to the whole service.
6. **Stop/fail the process** when recovery is unavailable, unsafe, or not worth its complexity for this application, such as an unrecoverable invariant violation or a resource failure that makes continued execution unsafe. Emit actionable diagnostics before termination. Do not apply this choice to a service that promises resilience or has a valid recovery mechanism.
7. If no technique fits, retain a meaningful error contract. Preserve cause, operation/resource, stable category, and context needed by the owner who can act. Do not branch on unstable message text or invent sentinels that collide with valid results.
8. In review/read-only mode, report the proposed error contract without editing files. For an authorized interface change, first draft the contract and expected caller behavior; then update the narrowest contract and affected callers. Check compatibility and partial effects. Verify actual ordinary outcomes and each failure that remains visible, masked, aggregated, or terminating; distinguish planned checks from commands actually run.

## Decision test

Reduce handlers, not truth. A condition disappears only if the new operation's postcondition is genuinely satisfied. Masking is low in the stack; aggregation is high where one recovery policy is shared. Crashing is appropriate only when process continuation cannot meet the application's contract. A fatal system error and a rejected individual request are different stop scopes.

Retain a distinct failure when the caller can make a meaningful decision, the module cannot satisfy the outcome itself, or hiding it would make successful completion ambiguous. If intent or recovery ownership is unclear, report it as unresolved instead of suppressing it.

## Output

For each condition report: trace evidence; meaning and affected state; chosen technique and stop scope; cause/context preserved; affected callers and compatibility; and verification of normal and failure behavior. Label uncertain intent and unrun checks.

## Worked example

Before: a batch-notification worker catches every provider error, records “sent,” and advances the cursor, so transient failure and success become indistinguishable. After: define the contract so a notification is marked sent only after provider acceptance; retry only transient, idempotent deliveries, aggregate permanent per-recipient failures into the batch result, and stop the worker on corrupted cursor state with diagnostics. The invariant is that the cursor never advances past an unaccounted recipient. The application contract determines whether a failed batch is retried, reported, or terminates the worker.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Ch. 10 §§10.1–10.10, one-based physical PDF file pages 96–111. This procedure and project-original example are adaptations, not quotations.
