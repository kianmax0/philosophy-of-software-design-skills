---
name: posd-decide-what-matters
description: Identify which requirements and ideas should shape a design, make them prominent, and hide or minimize details that need not burden callers.
license: MIT
---

# Decide what matters

Structure a system around the few facts that determine correct use and broad understanding. Make those facts visible and central. Hide, localize, or give sensible defaults to details that do not need to affect other modules or callers. The aim is not simply the shortest API: overlooking an important policy is as costly as exposing many unimportant choices.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Chapter 21, §§21.1–21.5 (PDF file-page numbers, pp. 198–201). The examples and workflow here are original adaptations.

## Procedure

1. **Set the boundary.** Identify the task, actual consumers, externally imposed constraints, and behavior that must remain correct. Inspect requirements, representative callers, contracts, and current design. Mark assumptions rather than filling gaps with an imagined roadmap.
2. **Find leverage.** Ask which solution, interface, or invariant would solve several recurring problems or let readers predict behavior in many places. Compare realistic alternatives when available. A general operation can carry more leverage than a collection of caller-specific commands; a stable invariant can eliminate repeated reasoning and special cases.
3. **Classify what matters.** For each policy, distinction, parameter, method, special case, or ordering rule, determine whether it changes correctness, caller-visible behavior, an external constraint, or a broadly reused mental model. Then ask who has the information needed to choose it: caller, module, or system. Do not classify importance by frequency alone; rare security, durability, unit, or failure decisions may be essential.
4. **Minimize how much matters.** Put implementation decisions with the module that can make them consistently. Use a well-supported default for common cases and keep a narrow extension for demonstrated exceptional cases. Reduce the number of places where an important invariant or policy must be understood. A configuration object does not simplify anything if callers still have to learn every option.
5. **Emphasize essentials.** Put important distinctions where readers will see them: names, types, interface documentation, widely used operations, or the center of a shared design. Repeat a key idea only where repetition helps readers apply it consistently. Keep uncommon details localized so they do not shape unrelated interfaces.
6. **Check both error directions.** Too many things treated as important clutter interfaces and increase cognitive load. A missed important fact hides required functionality, causes callers to recreate it, or creates unknown unknowns. Compare a normal caller and a meaningful exceptional caller to ensure the default serves the former without erasing what the latter needs.
7. **When uncertain, make and test a design hypothesis.** State what you believe matters most, why the evidence points there, and what change follows. Evaluate the result against real use; if the hypothesis was wrong, identify the clue that could guide the next decision. Do not present a guess as an established requirement.
8. **Carry out the requested mode.** For implementation requests, make the bounded design change, update affected callers/contracts, and verify normal and exceptional behavior with relevant tests or checks. Report edits and results. For review-only requests, give recommendations without editing.

## Example

A batch reader asks every caller to choose a scratch-buffer size, decoding implementation, and output format. If current consumers all need UTF-8 records and the module can size its own buffer, make `read_records(path)` the ordinary operation and keep the format explicit only where another supported format is required. Buffer allocation is a local implementation choice; encoding can remain an essential caller choice for a real legacy consumer. Check both caller types before settling the contract.

## Output

Give the task and consumers, evidence for essential requirements and leverage points, choices moved to module ownership, defaults and exceptions, and the normal and exceptional caller experience. For implementation, report edits, caller/contract updates, and verification results. State assumptions and compatibility costs. Explain which ideas are prominent or central and which are localized, and why.
