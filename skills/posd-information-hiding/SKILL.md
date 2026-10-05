---
name: posd-information-hiding
description: Use when a design change exposes internal decisions across modules or makes callers depend on details likely to change
license: MIT
---

# Information Hiding

Use this skill to review whether a design keeps change-prone decisions local.
Information hiding means a module owns a decision and presents a contract that
lets other code work without knowing how that decision is implemented. The
goal is to reduce the number of places that must change together; it does not
mean concealing behavior from maintainers or making every field private.

## Inputs and evidence

Inspect the relevant module contracts, implementations, tests, and call sites.
List the design decisions visible at each boundary, such as a storage format,
retry policy, parsing rule, or vendor API. For each suspected leak, show where
another module relies on it and what change would force that caller to change.
Use file paths with line numbers or symbols. A single implementation behind an
abstraction is not evidence of needless indirection by itself.

## Review procedure

1. Name the behavior callers require without naming its current implementation.
2. Trace one important decision from where it is made to every place that depends
   on it.
3. Ask whether the dependency reflects an actual caller requirement or merely
   exposes an internal representation. Check tests and callers before
   deciding.
4. When internal knowledge leaks, propose a contract that expresses caller intent
   and lets the owning module make the decision. Keep information needed for
   legitimate caller control in the contract.
5. Check whether the change localizes future edits without creating a vague
   interface, hidden global state, or an extra forwarding layer. Trace error
   and lifecycle behavior as well as the happy path.

For an implementation request, change the narrowest boundary that owns the
decision, update only affected callers, and preserve observable behavior
unless the request says otherwise. Do not convert a focused finding into a
repository-wide encapsulation campaign.

## Output

Provide the decision that is exposed, evidence of the dependency it creates,
and the proposed boundary or reason to retain the current one. For code
changes, name affected contracts and callers and report relevant checks.
Separate observed facts from predictions about future change.

## Example

Before: a report builder reads `store.rootDir + "/v3/records.json"` and
implements its own fallback when the file is absent. After: it calls
`recordStore.listRecent()` and handles an explicit empty result. The store
owns file layout and missing-file semantics; the report builder retains its
own presentation policy.

## Leave the design alone when

- Callers truly need to choose or inspect the detail as part of their task.
- The boundary represents a required protocol, security check, or platform
  contract.
- An added interface would merely rename one operation and provide no local
  decision or stable contract.
- The alleged leak has no demonstrated dependency or plausible change impact.

Principle provenance: John Ousterhout's [Stanford CS190 Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign). The workflow and example here are original adaptations.
