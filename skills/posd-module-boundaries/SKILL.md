---
name: posd-module-boundaries
description: Decide whether to combine or separate functions, classes, or modules when shared knowledge couples them or unrelated responsibilities change independently
license: MIT
---

# Module Boundaries

Use this skill to decide what belongs together and what should be separate. Organize code around shared knowledge and coherent responsibilities. Code that runs consecutively does not necessarily belong together, and code in separate functions can still share an inseparable invariant.

The principle is inspired by John Ousterhout's [Stanford discussion of combining and separating code](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=raftReview2). The procedure and example here are original adaptations.

## Procedure

1. Establish the requested scope and behavior. Find the module declaration, public interface, implementations, and representative call sites. Record evidence as repository path, line, and relevant caller or symbol.
2. Identify the knowledge owned by each part and the invariant connecting them. Trace a change to that knowledge: which parts must change together? Include shared state, error handling, ordering, and transaction or lifecycle rules.
3. Compare keeping the current boundary with combining the parts. Combining is useful when they share information, each is hard to understand without the other, or the interface distributes a single invariant across callers. Explain the knowledge that becomes local.
4. Compare separating the parts when they have distinct responsibilities, lifetimes, consumers, or reasons to change. Separation is useful when one part can expose a coherent contract without leaking the other's knowledge. Avoid decomposing merely by execution phase or line count.
5. Recommend the arrangement with the simpler total contract for callers and maintainers. Account for internal readability, ownership, and compatibility. A cohesive public operation can contain private helpers; joining knowledge does not require one giant function.
6. If implementation was explicitly requested and the candidate is within scope, change only the relevant boundary. Preserve observable behavior and public contracts unless the request explicitly authorizes a change. Verify representative callers and the boundary's relevant tests or checks.

## Output

For reviews, report findings only. Use:

- **Evidence:** path:line and symbol or call site.
- **Shared or independent knowledge:** what couples the parts or lets them evolve separately.
- **Comparison:** effects of retaining, combining, or separating on callers and maintainers.
- **Boundary opportunity:** the coherent responsibility and owner in the recommendation.
- **Tradeoff:** migration, flexibility, or compatibility cost; say when evidence is insufficient.

For requested implementation, add the change made and the focused verification performed. Do not claim a design is better merely because it has fewer methods or files.

## Example

Before: a record parser and validator both interpret byte offsets and format-version flags. Changing the format requires coordinated edits even though parsing and validation occur in separate phases.

After candidate: a format reader owns byte interpretation and structural validation together, returning a stable domain record. A presentation formatter can stay separate because display policy has different consumers and no need to know those byte offsets. Verify that validation outcomes and the record contract remain unchanged.

## Leave the Design Alone When

- The apparent duplication represents real variation in caller needs.
- A proposed wrapper only renames or forwards the same decisions.
- The module boundary crosses ownership or transaction rules that are not understood.
- The evidence comes from one contrived call site, generated code, or an incomplete trace.
- Changing the interface would break users outside the authorized scope.

Small functions are not inherently shallow, and broad modules are not automatically deep. Explain the caller cost and the hidden responsibility before recommending a change.
