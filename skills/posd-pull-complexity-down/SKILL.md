---
name: posd-pull-complexity-down
description: Use when callers or operators repeatedly handle mechanics, exceptions, defaults, or configuration for a module's core operation
license: MIT
---

# Pull Complexity Downwards

Use this procedure when users of a module perform work that may belong inside it. The goal is to reduce total system complexity and simplify the module's interface, even when its implementation becomes more involved. Do not move work merely because a lower layer can technically perform it.

## Inputs

- The requested outcome and candidate module.
- The module contract/implementation, its representative callers, tests, and relevant operational configuration.
- Concrete caller-side mechanics, branches, defaults, exception handling, or parameter choices, with path/line or symbol evidence.

## Procedure

1. Name the caller task and the repeated or difficult work currently outside the module.
2. Decide whether each piece is unavoidable complexity of the module's own capability, or instead represents caller domain policy. Use contracts and multiple callers; do not treat caller count alone as proof.
3. Estimate the system-level effect of moving the work: which caller code and interface elements disappear, what implementation work is added, and whether the callee's contract becomes simpler and more complete.
4. Prefer the module to determine ordinary defaults or policy when it has the information to choose well. Before adding configuration, ask whether a user or higher-level caller can actually choose a better value than the module. If not, compute/adapt internally and provide a sensible default; expose an override only for evidenced cases that need control.
5. If specialization must remain, choose its direction. Keep feature-specific behavior upward in the feature layer when it would leak that feature into a general mechanism. Push specialization downward into a driver/adapter when it translates external particulars into a general operation and shields the core. Do not mix special handlers with a generic mechanism without a concrete ownership reason.
6. In review/read-only mode, report the proposed contract without editing files. For an authorized interface change, first draft the contract and expected caller usage; then make a focused contract change and update demonstrated callers. Preserve externally visible behavior unless requested otherwise; trace normal, edge, error, cleanup, retry, and lifecycle paths.
7. Verify actual results against the new contract at representative callers and focused checks. Report what was run and any unverified operational choice.

## Decision test

Pull complexity down when it is closely related to the module's functionality, it measurably simplifies higher-level code, and it reduces the interface burden. A more involved implementation is acceptable when one module can solve the user's task more completely.

Keep complexity upward when it expresses genuine user or business policy the lower-level module cannot infer. Avoid exporting knobs as a substitute for deciding a problem; avoid a mega-module that absorbs unrelated workflow concerns. When requirements differ, provide a narrow explicit choice with a default if appropriate.

## Output

Show the current caller burden and evidence, what responsibility moves and why its owner can handle it, the new or retained interface, caller-specific choices left outside, behavior/compatibility effects, and verification.

## Worked example

Before: each invoice caller checks whether a line has a discount, computes the discounted amount, and handles rounding before totaling. After: a proposed `invoiceTotals(lines, currency)` contract owns the domain calculation and rounding rule; screens retain presentation choices such as how to display the total. The invariant is that every caller gets the same monetary total for the same lines and currency. Keep a discount policy outside only if callers have a demonstrated choice the module cannot infer.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Ch. 8 §§8.1–8.4, one-based physical PDF file pages 78–81. This procedure and project-original example are adaptations, not quotations.
