---
name: posd-complexity
description: Diagnose why a concrete code path or change is hard to understand or modify by tracing change amplification, cognitive load, dependencies, and obscurity.
license: MIT
---

# Diagnose the developer's burden

Complexity is the difficulty of understanding and changing a system for a task. System size, sophisticated functionality, short code, and cyclomatic counts do not establish that burden. Complexity isolated behind a stable interface can be preferable to smaller code every caller must understand.

## Start from a real task

Read the target, relevant contracts, representative callers, and existing checks. Choose a concrete change or caller operation from the request. For a new design, sketch the callers and label assumptions. For review requests inspect without editing; for requested implementation carry the diagnosis through an in-scope change and verification.

Trace the task from its entry point to the modules that must agree. Search for signatures, data fields, constants, or policies, then read the matches before claiming dependencies. Pay particular attention to frequently used interfaces and frequently changed paths. Describe frequency qualitatively when no measurements exist; do not turn the book's explanatory weighting into a numerical design score.

## Separate symptoms from causes

| Symptom | Concrete inspection | Evidence to retain |
| --- | --- | --- |
| Change amplification | Walk a requirement change and list sites that must change together | Shared decision and why each site depends on it |
| Cognitive load | Walk one caller task without reading internals; list required units, sequencing, lifecycle, error, and policy facts | Which facts are in the contract and which require external knowledge |
| Unknown unknowns | Follow effects not signaled by the interface, such as another derived value, invalidation step, or coupled serializer | An actual hidden dependency and where a maintainer would need to discover it |

Unknown unknowns are especially dangerous because a developer cannot know what to inspect. Do not fabricate unseen dependencies: mark uninspected consumers as uncertainty.

Then locate the underlying **dependency** (code cannot be understood/changed independently) and **obscurity** (needed information is hard to discover). A leaked representation, implicit sequencing rule, or vague name can cause several symptoms. Merge findings with the same cause. Dependencies are inevitable; the aim is fewer, simpler, more visible dependencies, not complete independence.

## Change the cause

Compare retaining the design with a bounded improvement that eliminates a decision or hides it behind a knowledgeable owner. Show the before/after caller sequence, facts callers no longer carry, and new dependencies introduced. A helper that merely moves arithmetic can leave the invariant distributed; a comment can reveal a dependency without eliminating it. Choose based on the actual burden.

For requested implementation, update the owning boundary, affected callers and contract documentation, then verify the behavior exposed there. If the desired interface change exceeds scope, name the smaller achievable improvement and remaining dependency.

## Original example

A thumbnail service changes its crop rule in one configuration field, but two preview consumers also keep derived aspect-ratio constants that must change with it. Updating the crop rule appears local until those constants are discovered. This is obscurity producing an unknown unknown, plus change amplification. Exposing preview dimensions through the crop-policy owner makes the relationship discoverable and the change local. Naming all three constants clearly still leaves the relationship distributed.

## When to retain the design

Independent policies can legitimately have similar syntax. A cross-cutting requirement can legitimately touch several owners. A rarely modified complex implementation behind a stable contract may burden developers less than a simple implementation that exposes its choices. Check those circumstances before recommending consolidation.

## Output

For each material finding give location, inspected task/caller, symptom, dependency or obscurity causing it, and consequence. Show a bounded before/after improvement, its migration or compatibility cost, and checks run or proposed. Rank by demonstrated developer burden; state the inspected scope if no material finding is supported.

Source: Ousterhout, *A Philosophy of Software Design*, second edition (2021), ch. 2 §§2.1–2.4 (PDF pp. 19–26); ch. 1 §1.1 (PDF pp. 17–18). PDF pages are one-based file pages, not printed page numbers. [Author's book page](https://web.stanford.edu/~ouster/cgi-bin/book.php). Procedures and examples are original adaptations.
