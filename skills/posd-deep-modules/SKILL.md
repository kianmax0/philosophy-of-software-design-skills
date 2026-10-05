---
name: posd-deep-modules
description: Use when a module exposes many details, forces callers to coordinate internals, or has a small implementation behind an awkward interface
license: MIT
---

# Deep Modules

Use this skill when reviewing or changing a module whose interface seems
expensive relative to the work it performs. A deep module gives callers a
small, stable set of operations while handling substantial internal
complexity. Depth is a relationship between the public contract and the
behavior behind it; file size and method count do not establish it.

## Inputs and evidence

Inspect the module's public declarations, implementation, tests, and
representative call sites. Record the caller-visible concepts, parameters,
return values, errors, and setup steps. Trace at least one ordinary path and
one failure or edge path through the implementation. Cite file paths and line
numbers or named symbols in your findings. A large implementation can still be
shallow if callers must understand its internals, while a short adapter can be
appropriately narrow when it translates a necessary boundary.

## Review procedure

1. State what callers need the module to accomplish in domain terms.
2. Compare that job with the choices callers must make to use it. Look for
   repeated sequencing, duplicated policy, exposed storage or protocol
   details, and errors callers must interpret.
3. Identify which details belong to the module and which are true caller
   decisions. Use call sites and contracts as evidence; do not infer ownership
   from a class name.
4. If the interface makes callers reproduce internal knowledge, propose one
   cohesive operation that absorbs that knowledge. Keep caller-controlled
   choices explicit when they represent genuinely different product needs.
5. Check the proposal against existing call sites, error behavior, lifecycle
   requirements, and tests. Report any behavior that cannot be preserved from
   available evidence.

For a requested implementation, make the smallest interface and implementation
change that moves internal coordination behind the module boundary. Preserve
observable behavior unless the request explicitly changes it. Avoid broad
refactors to unrelated callers.

## Output

Return the module and caller evidence, the specific complexity crossing the
boundary, and a focused recommendation or patch. Include the new or retained
contract, affected call sites, behavior-preservation notes, and a relevant
verification result when implementation was requested. If evidence is
incomplete, label the inference and identify what would settle it.

## Example

Before: callers invoke `readConfig`, choose a fallback, validate fields, and
format the same error. After: `loadServiceConfig(path)` owns parsing,
defaults, validation, and a stable error result; callers still choose the path
because that is their responsibility. This is useful only if the policy is
shared and belongs to this module.

## Leave the design alone when

- The apparent complexity expresses legitimate choices that differ by caller.
- The module is a justified adapter around a security, platform, protocol, or
  vendor boundary.
- A simpler interface would hide required control, weaken error handling, or add
  indirection without reducing caller knowledge.
- The concern is based only on line counts, method counts, one implementation,
  or personal preference.

Principle provenance: John Ousterhout's [Stanford CS190 Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign). The workflow and example here are original adaptations.
