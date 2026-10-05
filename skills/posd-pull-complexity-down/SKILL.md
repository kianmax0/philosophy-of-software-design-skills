---
name: posd-pull-complexity-down
description: Use when callers repeatedly branch, validate, sequence, or recover around a lower-level operation that could own those details
license: MIT
---

# Pull Complexity Down

Use this skill when call sites carry coordination logic that appears to belong
with the operation they invoke. Moving complexity down means giving a lower-
level module enough responsibility to handle recurring mechanics behind a
clear contract. It can simplify callers, but it can also make a module harder
to understand if the moved policy belongs to the caller or combines unrelated
concerns.

## Inputs and evidence

Inspect the target operation, its callers, tests, and error behavior. Find
concrete repeated decisions such as ordering steps, validating the same
invariant, interpreting the same result, or applying the same recovery rule.
Cite each example by path and line or symbol. Compare call sites; a single
caller or a single implementation does not prove the design needs a new
general mechanism.

## Review procedure

1. Describe the task callers are trying to complete and list the extra steps they
   perform around the lower-level operation.
2. Check which steps are stable mechanics of that operation and which express
   caller-specific policy. Use call sites, tests, and contracts as evidence.
3. If mechanics are repeated, move them behind one cohesive operation with a
   result and error contract callers can handle directly.
4. Keep genuine caller choices explicit. Do not silently absorb a policy that
   changes user-visible behavior or remove meaningful caller control.
5. Trace success, failure, retry, ordering, and lifecycle paths. Verify every
   affected caller and preserve observable behavior unless the requested
   change says otherwise.

For implementation requests, make a focused change at the module that owns the
repeated mechanics. Do not broaden it into unrelated cleanup or refactor
distant call chains without evidence that the same complexity belongs there.

## Output

Show the caller-side complexity with concrete references, explain why the
callee owns it, and recommend or implement one focused contract change. Note
caller-specific policy retained, affected call sites, behavior implications,
and relevant verification results.

## Example

Before: each export caller creates a temporary file, writes rows, flushes,
renames it, and removes it on failure. After: `exportReport(destination,
rows)` owns the atomic-write sequence and reports success or a typed failure.
A caller still chooses the destination because that is part of its own policy.

## Leave the design alone when

- The surrounding logic differs because callers have distinct requirements.
- Moving it would make the callee depend on unrelated presentation or workflow
  policy.
- A boundary must expose a deliberate choice for security, platform, or protocol
  reasons.
- The suggested change rests only on visual complexity, line count, method
  count, or a preference for fewer call-site lines.

Principle provenance: John Ousterhout's [Stanford CS190 Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign). The workflow and example here are original adaptations.
