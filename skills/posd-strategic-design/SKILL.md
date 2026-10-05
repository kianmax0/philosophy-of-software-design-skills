---
name: posd-strategic-design
description: Choose a bounded design investment while adding a feature or fixing a defect when a local patch risks creating repeated special cases or maintenance debt.
license: MIT
---

# Make a strategic design investment

Deliver the requested behavior while considering how the chosen design will affect subsequent work. Use the actual change as the boundary of the exercise.

## Inspect the decision

Read the relevant implementation, tests, callers, and compatibility constraints. Identify the immediate fix and the design assumption it changes. For review or planning requests, provide a recommendation without modifying files; implement only when that work is requested.

Look for a chain of special cases, repeated caller workarounds, a new exception to a poorly owned invariant, or a fix that would need repeating in several places. Tie each observation to a location and the requested behavior.

## Compare three practical choices

- **Direct patch:** The smallest change that correctly satisfies the requirement. Describe any extra fact future maintainers must remember.
- **Bounded improvement:** Change the owner or interface of the affected decision so the feature fits naturally. Describe the local migration and the caller knowledge it removes.
- **Defer the structural change:** Deliver a correct patch with its limitation recorded when a wider migration would exceed scope or available information.

Use only choices that are plausible for this codebase. Do not turn every bug fix into an architecture exercise. Evaluate the total work of implementation, caller migration, verification, and subsequent changes that are supported by current requirements. Avoid invented future customers or numeric return-on-investment claims.

Recommend the bounded improvement when it resolves an evidenced source of repeated complexity at an acceptable migration cost. Recommend the direct patch when the current abstraction is sound or when the supposedly better design adds more decisions than it removes.

## Execute within scope

For requested implementation, make the selected change, keep unrelated work out of the patch, and run relevant verification. A structural improvement should preserve existing behavior except for the user's requested change. If a needed public migration is outside the assignment, describe it as follow-up work instead of silently undertaking it.

When a limitation remains, record the concrete trigger that would justify revisiting it. “Refactor later” does not explain what evidence should prompt action.

## Example

A retry function has separate branches for three operations because each operation supplies a different delay constant. A fourth operation is being added. If all operations share the same retry semantics, making delay an explicit policy value may remove branching without changing callers' failure contract. If one operation is non-idempotent, the common policy must still express or retain that distinction; sharing code must not create unsafe retries.

## Avoid false positives

- A deadline can make a correct local patch the responsible choice.
- A prototype with a disposable lifetime has different maintenance costs.
- A one-off requirement does not automatically justify a general framework.
- The principle supplies a decision criterion, not a mandatory percentage of time to spend refactoring.

## Output

State the requested behavior, evidenced design pressure, plausible options, selected approach, migration cost, and verification plan or results. Explain any deferred limitation with a concrete revisit trigger. Keep the recommendation proportional to the change.

Principle provenance: John Ousterhout's [Stanford CS190 Working Is Not Good Enough](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=working). The workflow and example here are original adaptations.
