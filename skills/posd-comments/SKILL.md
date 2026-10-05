---
name: posd-comments
description: Use when reviewing or writing code comments, interface documentation, invariants, units, or explanations of non-obvious behavior
license: MIT
---

# Comments

Use this skill to decide whether a comment preserves knowledge that the code alone does not communicate. Useful comments explain intent, constraints, invariants, units, side effects, or a non-obvious reason. Comments that translate each line into prose add maintenance work without clarifying behavior.

The design principle is associated with John Ousterhout's *A Philosophy of Software Design*. The procedure and examples here are original adaptations. See the [Stanford CS190 book discussion](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview) for the principle-level source.

## Procedure

1. Identify the audience and decision the comment should support: API caller, maintainer, operator, or future author of an implementation.
2. Read the surrounding code and contract first. Record path:line evidence and distinguish facts verified in code or tests from assumptions stated by the comment.
3. Ask what a careful reader could not infer: why a choice exists, what must remain true, how to interpret units or sentinel values, what side effects occur, or what callers may rely on.
4. Keep the comment at the right boundary. Put stable usage and behavior guidance near the interface; put local rationale or an invariant near the implementation. Update or remove stale claims when behavior changes.
5. When designing an interface, draft its comment before implementation as a probe. If the intended behavior cannot be described clearly without mentioning internal steps, reconsider the interface. Treat the comment as a design aid, then verify it against the implementation.
6. For reviews, report only. If comment changes are requested, preserve verified technical meaning and check that every claim matches current behavior.

## Output

For each comment issue, report:

- **Evidence:** path:line and the code or interface it describes.
- **Reader question:** what remains unclear or what is repeated.
- **Action:** add, move, correct, shorten, or remove, with the knowledge to preserve.
- **Verification:** source, test, or contract supporting the resulting claim.

Do not infer intent from an old comment alone. If the rationale cannot be established, flag it for an owner rather than rewriting speculation as fact.

## Example

Before: `// Add 1 to retryCount` above `retryCount++` repeats the code.

After: `// Keep the original request deadline across retries so retries cannot extend the caller's timeout.` This belongs only if the deadline behavior is confirmed by the implementation or contract.

## Leave the Comment Alone When

- It documents a subtle invariant, externally relied-on behavior, units, side effects, or a justified workaround.
- Removing it would force readers to rediscover non-obvious context.
- The supposed redundancy disappears only to someone who already knows the domain.
- The evidence does not establish whether a claim is stale or still required.

Comments should capture knowledge rather than narrate syntax. A concise interface comment can be more valuable than a detailed description of internal steps, especially when implementations may change.
