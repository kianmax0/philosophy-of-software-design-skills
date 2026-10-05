---
name: posd-complexity
description: Diagnose change amplification, cognitive load, and unknown dependencies in a concrete code path or proposed change using evidence from callers and contracts.
license: MIT
---

# Diagnose complexity

Find the knowledge and coordination a developer needs to make a specific change. Prioritize an observed maintenance burden over a stylistic preference.

## Start from a change

Identify the requested behavior, affected code, representative callers, and public contracts. If the task is a review, inspect without editing. If implementation is requested, keep changes within its scope and preserve behavior outside the requested change.

Pick a concrete change scenario, such as adding a file format or altering an expiration policy. Trace it from the entry point through the modules that must agree. A search result suggests a dependency; read the relevant code before treating it as evidence.

## Diagnose the burden

1. **Change amplification:** List the places that must change together and the shared decision that connects them. Distinguish genuine duplication of knowledge from independent occurrences of similar syntax.
2. **Cognitive load:** List facts the caller must remember beyond the signature: ordering, units, paired operations, configuration combinations, failure semantics, or ownership. Show where the contract communicates each fact.
3. **Unknown unknowns:** Look for effects that the interface or nearby documentation does not reveal. Examples include an undocumented cache invalidation requirement or a serializer that silently changes a stored schema. Report the inspected dependency; do not speculate about missing files.

Find the underlying cause: a leaked representation, an unclear owner, a split invariant, an unnecessary caller decision, or an implicit dependency. Several symptoms may have one cause; merge those findings.

## Recommend a bounded improvement

Compare leaving the code as it is with an improvement that hides or localizes the shared knowledge. State what callers no longer need to know and where that knowledge will live instead. Account for migration, compatibility, and any additional internal complexity.

For requested edits, verify the actual behavior and contract at the changed boundary. Avoid inventing a complexity score or claiming that fewer lines proves a better design.

## Example

Three importers each choose a timestamp unit, validate it, and convert it before calling a storage function. A proposed fourth importer would repeat all three decisions. A storage boundary accepting an explicit duration type can own validation and conversion once. The improvement is local ownership of the unit invariant; merely extracting the repeated arithmetic into a helper still leaves callers responsible for choosing the right unit.

## When to retain the design

- Several files can legitimately change for an independent cross-cutting requirement.
- A small, explicit duplication can be clearer than coupling modules with different ownership or release cycles.
- A long function or large implementation is insufficient evidence of caller burden.
- A search cannot establish a full repository dependency graph. Mark uninspected paths as a limitation.

## Output

For each supported finding give the code location, concrete change scenario, symptom, root cause, caller consequence, recommended improvement, and compatibility or verification concern. Rank by the demonstrated burden. When no material issue is supported, say so and identify the inspected scope.

Principle provenance: John Ousterhout's [Stanford CS190 The Nature of Complexity](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=complexity). The workflow and example here are original adaptations.
