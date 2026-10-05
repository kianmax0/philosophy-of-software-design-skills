---
name: posd-obvious-code
description: Review a code path for behavior readers cannot infer from nearby code, names, types, or contracts, and recommend a bounded clarification.
license: MIT
---

# Make code obvious

Help a maintainer understand what the code does and why at the point where they need that knowledge. “Obvious” is judged from the reader's perspective and context, not from the author's familiarity with the implementation.

## Establish the reading task

Identify the requested behavior, entry point, and relevant callers. Read surrounding code, types, contracts, comments, and tests. For a review, inspect without editing. Keep requested edits in scope and preserve unrelated behavior.

Choose a concrete question a maintainer might ask: What does this return? Which resource is owned? What happens on retry? Can this branch be reached? Follow the control and data flow needed to answer it. Search hits are leads; inspect actual uses before treating behavior as established.

## Find the source of obscurity

Check whether the answer is hard to infer because of:

- a name that suggests the wrong role or omits a consequential distinction;
- hidden state, non-local side effects, or an implicit ordering requirement;
- control flow routed through callbacks, wrappers, or several small helpers without a useful abstraction;
- behavior that depends on undocumented conventions or a caller's prior action;
- a comment or interface contract that conflicts with implementation.

Explain the inference a reader must make and where evidence lives. Do not call code obscure merely because it is unfamiliar, concise, long, or uses a language feature. A helper improves clarity when it names an operation or hides details; splitting every statement can make the path harder to follow.

## Make the necessary fact visible

Recommend a direct name, explicit type or state transition, locally visible condition, useful abstraction, or concise comment that supplies the missing “what” or “why.” Put knowledge near the decision or behavior it explains. Preserve essential details such as units, failure semantics, ownership, and security checks. If the intended behavior cannot be inferred from evidence, report the uncertainty instead of choosing semantics on the maintainer's behalf.

Trace the proposed explanation back to its source. Prefer expressing a stable
invariant in the contract or type system, and a local exception beside the
branch that handles it. Avoid duplicating implementation line by line in a
comment. If a comment is necessary, check that it matches behavior and stays
close enough to remain maintainable.

### Example

An API calls `save(record)` and returns `false` on a version conflict, but callers treat every `false` as a disk failure. The return value hides two distinct outcomes. An explicit result such as `Saved`, `Conflict`, and `StorageFailure` makes the contract visible and lets each caller handle the cases it actually owns. Changing this public type requires checking callers and compatibility boundaries.

## Output

For each finding, give the path and line, the reader question, the evidence needed to answer it, why that information is not visible at the use site, the consequence, and a bounded recommendation. Note uncertain or uninspected behavior. If a reader can reliably infer the contract and no material burden is supported, report that.

Keep observation and inference separate. Quote only the small identifier or
expression needed to locate behavior. Do not claim that every reader is
confused; show the particular inference step or caller error the design
requires. If a proposed rename or extraction changes behavior, describe that
separately from the clarity improvement.

Evidence checklist:

- State the concrete reader question and where it arises.
- Point to the code, contract, or test that answers it today.
- Explain what extra fact the reader must infer or discover elsewhere.
- Recommend a local change and name the behavior it must preserve.

Principle provenance: John Ousterhout treats code obviousness and obscurity as design concerns in the [Stanford CS190 materials](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=complexity). The workflow and example here are original adaptations.
