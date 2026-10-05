---
name: posd-design-twice
description: Use before committing to a new module, API, or subsystem design when the first plausible structure may constrain future changes
license: MIT
---

# Design Twice

Use this skill to compare genuinely different ways to assign responsibility before a design hardens. The comparison should expose costs and assumptions, not create alternatives that differ only in names, syntax, or diagram layout.

The design principle is associated with John Ousterhout's *A Philosophy of Software Design*. The procedure and examples here are original adaptations. See the [Stanford CS190 book discussion](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview) for the principle-level source.

## Procedure

1. State the concrete problem, users, required behavior, constraints, and evidence. Separate known requirements from forecasts and preferences.
2. Sketch the simplest plausible design, including its public interface, ownership of state, and which component decides policy. Identify its largest uncertainty.
3. Create at least one alternative that changes a meaningful design dimension: who owns a decision, state, lifecycle, or failure response. Keep required behavior and constraints constant.
4. Compare alternatives against concrete change scenarios: a new caller, changed policy, partial failure, new data source, or scaling constraint where relevant. Trace which components and callers change.
5. Name the costs: exposed knowledge, coordination, indirection, migration, test burden, and risks of assumptions. Use evidence where available; label forecasts as uncertain.
6. Recommend a design only when the comparison shows a useful advantage under the stated constraints. Otherwise recommend a small, reversible step that gathers the missing evidence.

## Output

Present each design in the same compact format:

- **Responsibility:** who owns state, policy, and failure handling.
- **Interface:** what callers must know and do.
- **Change scenario:** components affected and why.
- **Costs and assumptions:** supported facts versus uncertain predictions.
- **Recommendation:** choice, rationale, and evidence that could change it.

For code review, report the comparison and recommendation only. If implementation is explicitly requested, implement only the selected in-scope design, preserve behavior and contracts, and verify the change scenarios most affected.

## Example

Before: a shipment service asks a global rules module for a delivery window, then separately reserves capacity. The two operations can disagree when rules change.

Alternative A keeps policy global and passes the computed window into reservation. Alternative B makes the reservation owner evaluate policy and reserve atomically. These differ in policy and state ownership. Compare consistency needs, other policy consumers, and transaction limits before choosing; naming the combined operation `reserveShipment` alone is not a second design.

## Leave the Current Design When

- Alternatives only rephrase the same ownership structure.
- Constraints or likely change scenarios are unknown and cannot be responsibly inferred.
- Existing evidence shows the current design already localizes relevant change.
- A broad redesign costs more than a small experiment or a reversible seam.
- The requested scope does not authorize the interface or migration changes required.

Do not invent hypothetical requirements to justify complexity. Prefer a focused comparison over exhaustive architecture diagrams, and make uncertainty visible.
