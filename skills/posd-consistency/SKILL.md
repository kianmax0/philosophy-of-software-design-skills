---
name: posd-consistency
description: Review a concrete code change or code path for surprising inconsistency in behavior, naming, or structure, while preserving meaningful differences in units, lifecycles, and contracts.
license: MIT
---

# Review consistency

Use consistency to help readers transfer knowledge from one part of a codebase to another. First establish whether two cases really share a contract; matching syntax alone does not prove they should behave alike.

## Inspect comparable cases

Identify the operation, data, callers, and behavior under review. Read the relevant implementation, documentation, tests, and representative uses. For a review, report findings without editing. If an edit is requested, keep it within scope and preserve behavior outside the requested change.

Choose a pair or small group that a maintainer would reasonably expect to work alike: sibling APIs, related error paths, parallel state transitions, or repeated naming patterns. Compare the observable behavior and the reasons for any difference. A repository search can locate candidates, but inspect their contracts before calling them inconsistent.

## Test the difference

For each apparent mismatch, ask:

1. Would a caller reasonably infer the same behavior from the shared name, shape, or documented convention?
2. Does the difference follow from a real semantic constraint, such as distinct units, ownership, security policy, lifecycle, or compatibility requirement?
3. Is the reason visible where a reader encounters the exception?
4. Would aligning the cases reduce learning, or conceal a distinction callers must understand?

Prefer a shared convention when semantics match. If behavior must differ, make the distinguishing contract explicit in a name, type, documentation, or local control flow. Do not normalize away a meaningful difference merely to make code look uniform.

## Recommend proportionally

Describe the reader expectation, observed behavior, reason the cases differ, and practical consequence. Recommend the smallest change that makes the convention predictable: align equivalent cases, or clarify a justified exception. Include migration and compatibility effects when changing a public contract.

Before recommending alignment, check the surrounding type and contract, not only
the method name. Compare at least one ordinary caller for each case. If these
uses are not comparable, narrow the claim or report that evidence is insufficient.
For a requested edit, state how existing callers will retain their expected
behavior after the convention is changed.

### Example

Two parsers both accept timestamps and expose `parse_time`, but one interprets bare values as seconds and the other as milliseconds. Matching names suggest one contract, while the units materially differ. Either give both APIs an explicit unit-bearing type/name or route them through a shared unit contract. Silently changing one parser's unit could corrupt existing callers; first inspect stored data and consumers.

## Retain justified differences

- Distinct units, state lifetimes, authorization rules, or failure guarantees can justify different behavior.
- A compatibility layer may intentionally preserve a legacy convention.
- Similar-looking code can represent separate domain concepts.
- A one-off variation without caller impact is not automatically a defect.

## Evidence to capture

- The shared expectation: a common name, documented promise, or local convention.
- The observed behavior for each side, with a path and line.
- A caller or test showing the practical consequence.
- The semantic or compatibility reason that may justify the difference.
- The smallest change that would clarify or align the cases.

## Output

Give locations for both sides of a supported comparison, the expected convention, observed difference, evidence for or against a semantic reason, caller consequence, and a bounded recommendation. State uninspected consumers or unresolved contract questions. If no meaningful inconsistency is supported, say so.

Principle provenance: John Ousterhout discusses consistency as a way to reduce reader effort in his [Stanford CS190 course materials](https://web.stanford.edu/~ouster/cs190-winter24/slides/wrapup.pdf). The comparison steps and example here are original adaptations.
