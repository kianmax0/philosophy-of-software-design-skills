---
name: posd-consistency
description: Compare similar code paths for conventions readers can safely reuse, and distinguish justified variation from surprising inconsistency.
license: MIT
---

# Use consistency as cognitive leverage

Consistency lets a reader transfer knowledge from one place to another: similar things should work similarly, while dissimilar things should look or behave differently. It reduces repeated learning and prevents false assumptions. Uniformity by itself is not the goal.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Chapter 17, §§17.1–17.4 (PDF file-page numbers, pp. 166–170). See also Chapter 14 on consistent names and Chapter 19 §19.5 on over-applying patterns. The procedure is an original adaptation.

## Procedure

1. Identify the concrete operation or change and its callers. Read declarations, contracts, implementations, tests, and local conventions. Search to find comparison candidates, then inspect them; matching syntax is not proof of matching semantics.
2. Select a small set a maintainer would reasonably expect to work alike: sibling methods, parallel lifecycle transitions, related error paths, repeated data representations, or the same pattern in nearby code.
3. Compare the observable contract, not just spelling or structure: inputs and units, defaults, result meaning, side effects, ownership, errors, ordering, lifecycle, security, performance assumptions, and compatibility.
4. State the reusable expectation established by names, documentation, an existing convention, or a shared abstraction. Show at least one ordinary caller for each case so the reader consequence is concrete.
5. Investigate differences. Is there a real domain or compatibility constraint? Is the reason visible where a reader encounters the exception? If cases are semantically the same, recommend alignment. If they differ, make the distinction visible in a name, type, contract, invariant, or local explanation. Do not force dissimilar cases into one pattern.
6. Recommend proportionally. For an established convention, follow it in the new change. Do not introduce a competing convention merely because it seems cleaner. Change an existing convention only when significant new information supports the improvement and the affected old uses can be migrated together; explain rollout and compatibility costs.
7. Where repetition invites drift, suggest a proportionate guard: document the convention, enforce mechanically checkable rules with a tool, or use review guidance for semantic rules. Do not add tooling for a one-off difference without demonstrated recurrence.
8. **Carry out the requested mode.** For implementation requests, make the bounded alignment or clarification, update affected callers/contracts, and verify both sides still satisfy their intended behavior with relevant tests or checks. Report the changes and results. For review-only requests, give recommendations without editing.

## Example

Two `parse_time` methods accept bare numeric values. One interprets them as seconds and the other as milliseconds. The shared name leads callers to transfer the wrong assumption. First inspect units and actual callers; if both represent the same domain operation, align the contract or use an explicit unit-bearing type/name. Preserve a legacy difference only when its compatibility need is real and visible.

## When variation is right

- Different units, ownership, lifecycle, authorization, or failure guarantees require different behavior.
- A compatibility adapter intentionally preserves an older contract.
- Similar-looking code represents different domain concepts.
- A one-off difference has no caller consequence and making it uniform would add abstraction or obscure intent.

## Output

For each finding, give both locations, the reusable expectation, observed behavior, a caller-level consequence, evidence for or against a semantic reason, and the smallest alignment or clarification that preserves required behavior. For implementation, report edits, affected callers/contracts, and verification results. State the search boundary and unresolved consumers. If the comparison is unsupported, say what contract or usage evidence is missing.
