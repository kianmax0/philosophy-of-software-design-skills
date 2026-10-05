---
name: posd-error-design
description: Simplify an error contract when preventable exceptional cases burden callers, failure handling is scattered, or meaningful operational failures lose context
license: MIT
---

# Error Design

Use this skill to reduce unnecessary exceptional cases and give meaningful failures a useful contract. A design can make an expected condition ordinary when the operation's intended postcondition is still satisfied. It must preserve operational failures, invariant violations, and partial completion that prevent the promised outcome.

The design principle is associated with John Ousterhout's *A Philosophy of Software Design*. The procedure and examples here are original adaptations. See the [Stanford CS190 book discussion](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview) for the principle-level source.

## Procedure

1. Trace a concrete failing operation from its origin through each caller to the user or system boundary. Record path:line evidence, the operation, and the observed outcome.
2. Classify the failure using existing contracts: expected absence, invalid request, unavailable dependency, violated invariant, cancellation, or unexpected defect. Do not infer that a failure is recoverable just because code catches it.
3. Look for a better operation contract that removes an unnecessary exceptional case. Could an operation be idempotent, an expected absence be represented directly, or inputs be validated at a boundary? Explain why the new outcome satisfies the intended operation. Account for existing callers and compatibility before changing semantics.
4. Consider local recovery or aggregating handling only when that layer can satisfy the promised result and owns the recovery policy. Do not hide failed work, retry a non-idempotent action blindly, or collapse failures callers must distinguish.
5. Inspect the information surviving remaining failures: original cause, operation or resource, stable category, and context needed for correction or escalation. Avoid message-text branching and undocumented sentinels. Add useful context at its knowledgeable owner and preserve the cause.
6. For reviews, report only. If implementation is requested within scope, preserve meaningful failure behavior, avoid expanding catch scope, and verify both exceptional and ordinary outcomes. A new operation contract needs relevant caller and compatibility checks.

## Output

For each finding, report:

- **Evidence:** path:line, operation, and caller.
- **Failure meaning:** what happened and whether the contract treats it as expected.
- **Information lost or added:** cause, context, category, or recovery signal.
- **Recommendation:** the narrowest useful change and its compatibility implications.
- **Verification:** meaningful checks for the proposed contract, including ordinary outcomes and failures that must remain visible. Separate proposed checks from commands actually run and their results.

Distinguish verified behavior from inferred intent. If no failure contract or call site establishes the right recovery behavior, mark it unresolved rather than prescribing suppression.

## Example

Before: a cache reader catches every exception and returns an empty list; the caller cannot distinguish a cache miss from corrupt data.

After candidate: represent a normal miss explicitly, while allowing corruption to retain its cause and reach the component responsible for reporting or fallback. This is appropriate only if evidence confirms a miss is an expected condition and identifies the fallback contract.

## Leave the Design Alone When

- The catch is required by an established boundary contract and preserves diagnostics.
- A caller cannot act differently on more detailed error categories.
- Cancellation, retries, transaction rollback, or cleanup semantics are unclear.
- A new exception hierarchy would duplicate existing typed errors without improving decisions.
- The proposed fix would turn data loss, partial completion, or an invariant violation into apparent success.

For example, an explicitly idempotent `ensure_absent(key)` can succeed when the key is already absent because its postcondition holds; a permission or transport failure still cannot count as success. This differs from silently changing an established `delete_required(key)` contract. Keep error messages useful, but avoid using unstable message text as a programmatic interface.
