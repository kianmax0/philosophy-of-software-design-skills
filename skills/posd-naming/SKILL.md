---
name: posd-naming
description: Choose or review names that give readers a precise, consistent mental picture of a symbol and its distinctions.
license: MIT
---

# Choose names that create the right image

A name is a compact abstraction: it should help a reader guess what an entity is and, just as importantly, what it is not. Optimize for a correct first reading at the point of use, not for the writer's typing convenience or an abstract preference for short or long names.

Source: John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Chapter 14, §§14.1–14.7 (PDF file-page numbers, pp. 144–153). The checks here adapt the chapter into a coding-agent workflow.

## Procedure

1. Locate the declaration and usages, including representative callers, tests, serialized or reflected forms, generated bindings, and public interfaces. Record the search boundary; text search may miss dynamic and external references.
2. State what the symbol represents and the important ways it differs from nearby concepts. Imagine a reader seeing the name without its declaration: what would they guess? Compare that guess with actual behavior.
3. Check **precision**. Replace broad terms such as `count`, `status`, `data`, or `block` when they conceal which entity, state, unit, or domain is meant. Boolean names should read as predicates whose true/false meanings are apparent. Distinguish concepts that can be confused with one another; use distinct types when they can prevent an invalid interchange.
4. Check **consistency**. Find the established term for this same purpose and use it consistently. Never use that common name for a different meaning. If there are two values of one kind, add a useful distinction such as source/destination. Ensure the repeated name has a narrow enough meaning that readers can safely transfer their knowledge.
5. Remove words that add no information, such as a redundant `Object`, type encoding readily visible from the declaration, or a class name repeated inside its own context. Keep enough words to disambiguate the role.
6. Match name length to context. A short local loop variable can work when its complete scope is visible. As declaration-to-use distance or semantic ambiguity grows, make the name more descriptive. Local conventions and audience familiarity matter; do not impose a universal length rule.
7. If no concise name fits, treat that as design evidence. Check whether one variable combines distinct concepts, a responsibility is unclear, or the abstraction needs a different factoring. Improve the design when evidence supports it instead of hiding the problem in a long label.
8. **Complete the requested mode.** For an implementation request, rename the symbol and verified references, update affected callers/contracts, and preserve API, storage, reflection, and generated-code compatibility. Run relevant builds/tests and report edits, verification, and usages that could not be inspected. For review-only tasks, recommend without editing.

## Example

In a filtered table, `rowIndex` may mean a visible position while `recordIndex` means the underlying dataset position. Passing one where the other is expected can update the wrong record. Use distinct names, or distinct types when the boundary merits enforcement, and preserve the distinction consistently in callers.

## Retain the name when

- It is precise in its local context and the proposed alternative changes only style.
- It is established domain language and readers already infer the right meaning.
- A short name's full scope is visible and unambiguous.
- A migration could alter a public or persisted contract, or usage coverage is incomplete; report the risk rather than imply the rename is safe.

## Output

For a supported issue, provide declaration and representative-use locations, the likely mistaken reading, a candidate name and the distinction it makes visible, and migration/search limits. If the name is adequate, say what evidence makes its meaning clear. Separate naming clarity from behavior changes.
