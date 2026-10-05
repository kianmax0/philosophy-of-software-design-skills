---
name: posd-naming
description: Use when a name obscures a symbol's role, callers infer inconsistent meanings, or a rename is proposed across an API or codebase
license: MIT
---

# Naming

Use this skill to evaluate whether a name helps readers form the right mental model at the point of use. Judge the name in context, including nearby types, call sites, and domain vocabulary. Do not optimize for cleverness or length alone.

The design principle is associated with John Ousterhout's *A Philosophy of Software Design*. The procedure and examples here are original adaptations. See the [Stanford CS190 book discussion](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview) for the principle-level source.

## Procedure

1. Locate the declaration and representative usages. Record path:line evidence for the symbol, its contract, and call sites that show how readers interpret it.
2. State the symbol's role, owned responsibility, and important distinction from nearby concepts in a plain sentence. Check whether the current name implies a broader, narrower, or different role.
3. Inspect domain terms, established local conventions, overloads, serialized forms, reflection, generated bindings, and external callers. Search usages before recommending a rename; visible text may be part of a compatibility contract.
4. Offer a candidate only when it better communicates meaning at real call sites. Explain the ambiguity it removes and any tradeoff in length or consistency. Prefer changing the contract or ownership when the name cannot be made accurate without disguising a deeper design problem.
5. For reviews, report recommendations only. If a rename is explicitly requested and within scope, update all verified usages, preserve behavior and serialized/public compatibility, and check references, builds, and relevant tests.

## Output

For each recommendation, report:

- **Evidence:** declaration and representative path:line usages.
- **Current reading:** plausible interpretation and why it misleads.
- **Candidate:** proposed name and its meaning at a call site.
- **Impact:** compatibility, search, generated code, or migration concerns.
- **Confidence:** verified coverage or unresolved usage risk.

Do not claim a repository-wide rename is safe from a partial text search. State the boundaries of the usage search and identify dynamic or external references when relevant.

## Example

Before: `cache.refresh(key)` sounds like it updates stored data, but the implementation only invalidates an entry.

After candidate: `cache.invalidate(key)` accurately describes the visible effect. Before renaming, inspect all usages and public API guarantees; if callers rely on `refresh` to fetch a replacement, changing the name alone would conceal a behavior mismatch.

## Leave the Name Alone When

- The current term is established domain language and users understand it.
- The alternative differs only in style or personal preference.
- A rename affects a public, serialized, reflected, or generated identifier without an authorized migration.
- Usages are incomplete or dynamic, so semantic impact is unclear.
- The true problem lies in unclear responsibility or behavior rather than wording.

Names should communicate distinctions that matter. A longer precise name may reduce repeated explanation; a short name may be clear when its local context is strong.
