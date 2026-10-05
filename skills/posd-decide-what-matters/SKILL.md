---
name: posd-decide-what-matters
description: Simplify a proposed interface or design by identifying essential caller decisions, invariants, and exceptional details that can be hidden or given sensible defaults.
license: MIT
---

# Decide what matters

Shape a design around the facts that determine correct use. Reduce attention spent on choices the module can make without losing meaningful caller control.

## Establish the task

Identify the actual consumers, their required operations, and the behavior that must remain explicit. Read representative uses and relevant contracts. For a new design, use supplied requirements and label assumptions; do not invent a broad product roadmap.

For a review, report without editing. For requested implementation, simplify only the selected interface or code path and verify the affected behavior.

## Separate decisions

For each public parameter, method, option, or ordering rule, ask:

1. Does changing it alter a caller-visible requirement, correctness invariant, or supported operating constraint?
2. Is the caller the party with enough information to decide it?
3. Can the module choose it consistently from existing information?
4. Would a documented default serve the common case without disguising a meaningful tradeoff?

Classify each candidate as essential caller control, internal choice, or uncommon extension point. Show the evidence for contested classifications. Security policy, destructive behavior, durability guarantees, units, and failure semantics can be essential even when few callers mention them.

## Shape the design

Make the normal correct operation easy to express. Move implementation choices behind the interface when callers do not need to control them. Give related choices one coherent owner. Keep a narrow, explicit escape hatch when there is an evidenced exceptional need.

Do not merely hide options in a configuration object: that retains the caller's learning burden. Do not trade explicit required policy for a silent default. Explain what the default guarantees, when it stops applying, and how an exceptional caller chooses otherwise.

Compare the current and proposed interface using a normal caller and one meaningful exceptional caller. Count decisions only as an explanatory aid; the goal is better ownership of knowledge, not the smallest possible signature.

## Example

A batch reader asks every caller for a decoder, scratch-buffer size, and output encoding, although all current callers need UTF-8 records and the module can size its own buffer. A `read_records(path)` operation can hide buffer management and use a documented encoding default. A caller processing a supported legacy encoding still needs an explicit encoding option. Hiding that option would remove required behavior rather than simplify it.

## When to retain detail

- A policy choice belongs to the caller because only it knows the requirement.
- An explicit argument prevents a costly or irreversible misunderstanding.
- Existing integrations rely on an option; changing it requires a migration plan.
- A low-frequency use case can still carry a critical invariant.

## Output

Provide the important caller task, essential decisions and invariants, details proposed for internal ownership, normal and exceptional use examples, and any compatibility cost. Explain how the design makes the important distinctions visible. Mark unsupported assumptions.

Principle provenance: the second-edition addition described on John Ousterhout's [book page](https://web.stanford.edu/~ouster/cgi-bin/book.php). The decision procedure and example here are original adaptations.
