---
name: posd-design-twice
description: Compare materially different interfaces, implementations, or decompositions before choosing a consequential design, including when the first approach seems obvious.
license: MIT
---

# Compare designs before committing

Use alternatives to discover a simpler design. A second design is a thinking tool, not a requirement to build two systems or to seek another approval for already authorized work.

## Frame the decision

Read the requested behavior, relevant code, representative callers, contracts, and constraints. For a new module, use concrete caller operations from the request and label assumptions. Select the level being decided: public interface, internal representation/algorithm, or subsystem decomposition. Keep required semantics constant across alternatives.

For review or design requests, return the comparison and recommendation. For requested implementation, continue through the selected design and verification within scope.

## Sketch and compare

1. Sketch the first plausible approach: key signatures or data structures, state and policy owners, and one realistic caller sequence.
2. Sketch another approach that changes a substantive dimension. An interface can change operation granularity; an implementation can keep the same interface while using a different representation. Naming changes and extra indirection around the same decisions do not constitute another design. Consider an alternative even if you expect it to lose; give its strongest plausible rationale.
3. Walk the **same** common caller task and boundary condition through each design. For interfaces, prioritize ease of use: facts, ordering constraints, exceptional cases, and manipulations callers must perform. Also compare interface simplicity, useful generality, and implementability. For implementations, prioritize internal simplicity and relevant performance/resource constraints.
4. Test a supported change scenario, such as another existing consumer, policy change, partial failure, or changed representation. Identify which owners and callers would need to change. Label forecasts; do not invent a speculative platform to make an option win.
5. Use weaknesses to create a better option. If both approaches export work that belongs inside the module, seek a different abstraction rather than picking the less awkward one automatically. A synthesis is useful when it removes the weaknesses rather than accumulating both interfaces.
6. Choose and explain the decisive tradeoff. If an unresolved constraint controls the choice, propose or run a bounded probe that can resolve it; do not pretend a speculative comparison proves the answer.

## Make the choice executable

Write the chosen interface contract before filling in implementation: observable behavior, arguments/results, ownership, side effects, failure semantics, and boundary conditions. If that contract is difficult to explain independently of implementation, revisit the design.

For requested edits, implement the selected in-scope option, migrate affected callers, and check the scenarios used in the comparison. Reconsider the choice if implementation reveals a new dependency; a sketch is not a frozen design. Report actual checks separately from proposed ones.

## Original example

A reservation operation must select an available slot and reserve it without races. Design A exposes `available_slots()` plus `reserve(slot)`; callers choose a slot and handle a stale availability result. Design B exposes `reserve_matching(criteria)` and lets the reservation owner select and reserve atomically. Walk both through two competing callers and the no-match case. B hides coordination when the owner can enforce atomicity; A may be needed when caller-specific ranking cannot be expressed simply as criteria. This is a real tradeoff, not a rename of `reserve`.

For B's internal implementation, compare scanning an ordered collection with maintaining an availability index while keeping its public contract fixed. The second comparison asks about update costs and measured workload, not about a second API.

## Output

Give the decision and constraints, each alternative's sketch and caller sequence, the same scenarios compared, costs and assumptions, and the chosen contract with its rationale. Include migration and verification results for implementation requests. A compact comparison is sufficient; two full implementations or exhaustive architecture documents are unnecessary.

Retain the current design when the comparison supports it. A design can win because alternatives increase caller knowledge, coordination, or migration cost; do not manufacture a flaw to justify a change.

Source: Ousterhout, *A Philosophy of Software Design*, second edition (2021), ch. 11 (PDF pp. 112–115); ch. 15 §§15.2–15.3 (PDF pp. 155–156). PDF pages are one-based file pages, not printed page numbers. [Author's book page](https://web.stanford.edu/~ouster/cgi-bin/book.php). Procedures and examples are original adaptations.
