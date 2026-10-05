---
name: posd-strategic-design
description: Add a feature or fix a defect while improving the affected abstraction when a local patch would accumulate special cases, hidden dependencies, or repeated workarounds.
license: MIT
---

# Improve the abstraction while delivering the change

Make a continual small design investment in the code being changed. Correct behavior is necessary, but repeatedly adding exceptions to a poor abstraction makes later work harder. The smallest diff is not automatically the simplest resulting design.

## Understand the change

Inspect the requested behavior, working-tree state, implementation, callers, contracts, and tests. Identify the current design assumption challenged by the change. Look for repeated workarounds, one more special case, exposed internal data, or a fix repeated across consumers. Tie that pressure to concrete locations.

For review or design requests return a recommendation. For requested implementation, select and execute the in-scope improvement without treating this skill as another permission gate.

## Find the clean resulting design

Ask: **if this requirement had existed when this component was designed, what would its interface and knowledge ownership look like?** Sketch that shape before settling for an extra conditional. Design the affected abstraction as a coherent unit, including its core operations and failure/lifecycle contract; passing the next feature test is not the design criterion.

Compare plausible choices, with effort scaled to the decision:

- **Direct patch:** correctly delivers the behavior. Identify the additional fact or exception maintainers and callers must remember.
- **Bounded design investment:** removes the evidenced cause by adjusting the affected owner/interface. Show what caller knowledge disappears, which consumers migrate, and what internal complexity is added.
- **Constrained compromise:** useful when a clean migration conflicts with an actual deadline, compatibility commitment, or task boundary. Seek a smaller improvement before deferring the whole issue. State the remaining cost and concrete revisit trigger.

Prefer the cleanest attainable design within the constraints, including a proactive improvement before repetition appears. Do not require an arbitrary number of callers to justify a simple useful abstraction. Do not build speculative extension hooks, plugins, or a repository-wide redesign. Retain the direct patch when the abstraction remains sound or the alternative creates more knowledge and coupling.

## Implement and maintain the design

For requested edits, write/update the affected interface contract first, implement the selected change, migrate in-scope callers, and keep unrelated changes out of the patch. Preserve behavior beyond the requested change. Put lasting rationale and subtle constraints near their owner in code; a commit message alone is not discoverable enough. Review changed comments against the diff and avoid duplicated explanations across modules.

Use existing behavior checks to support restructuring. For a bug, reproduce it with a failing check before the fix when feasible, then verify that check and the affected boundary. For new behavior, choose tests from the designed contract rather than letting isolated tests dictate a series of ad hoc API additions. Report actual results and any unverified compatibility constraints.

## Original example

A scheduler has one branch per job category to choose a retention duration. A new category needs another branch in the scheduler and another in cleanup. If both implement the same retention rule, a single owner exposing `expires_at(job)` can absorb the decision and leave both consumers independent of categories. If cleanup has a different legal retention policy, merging the two policies hides a real distinction; keep that distinction explicit while simplifying shared mechanism.

## Avoid turning investment into a slogan

The book's suggested time investment and payoff curves express an investment mindset, not a validated task budget or guaranteed return. Do not impose a percentage, mandatory refactor, or universal delay. A disposable prototype or urgent compatibility fix can justify a compromise, but “we can clean it up later” alone does not assess its cost.

## Output

State the required behavior, challenged assumption, clean intended shape, plausible options and decisive tradeoff. For implementation requests deliver the patch, caller/contract updates, and checks with results. Record any remaining limitation with a concrete revisit trigger. A design report alone is insufficient when the user requested the change itself.

Source: Ousterhout, *A Philosophy of Software Design*, second edition (2021), ch. 3 §§3.1–3.5 (PDF pp. 27–33), ch. 16 §§16.1–16.6 (PDF pp. 159–165), ch. 19 §§19.2–19.4 (PDF pp. 180–183). PDF pages are one-based file pages, not printed page numbers. [Author's book page](https://web.stanford.edu/~ouster/cgi-bin/book.php). Procedures and examples are original adaptations.
