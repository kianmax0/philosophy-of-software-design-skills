# Sources and book calibration

The primary source for this revision is John Ousterhout, *A Philosophy of Software Design*, **second edition, July 2021 (v2.0)**, ISBN 978-1-7321022-1-7. The supplied PDF's copyright/printing-history page identifies that edition. The collection was checked against its substantive chapters and the concluding principle/red-flag lists on 2026-10-05. Earlier public-course grounding is superseded by this full-book calibration; the [initial smoke report](../evals/results/2026-10-05-smoke.md) describes the earlier revision only.

## Source identity and locators

- Local input filename: `Ousterhout - 2021 - A philosophy of software design.pdf`.
- Length: **215 PDF pages**.
- SHA-256: `c51c08a01b89a82fbc87c6b41f3f22228a21c0e5e769e601742b8f69b76e5d39`.
- All page ranges below and in skills mean **one-based physical PDF file pages**, not the book's printed page references. Chapter/section identifiers are the portable locators across other copies. This digital layout does not support assuming a single printed-to-PDF offset.
- [Author's book page](https://web.stanford.edu/~ouster/cgi-bin/book.php) is a public identification link. The supplied full book, rather than the site's limited extract or a course outline, grounds this revision.

The PDF and extracted full text are not distributed in this repository. Installed skills contain their own concise chapter/section attribution and do not require access to this machine or the book at runtime. Procedures, task routing, evidence requirements, evaluation criteria, and executable fixtures are project-authored adaptations. They are not official rules, quotations, or a claim of author endorsement. The MIT license covers project-authored material, not the book.

## Operational coverage

This table is a source-to-action map, not a chapter summary. Related chapters share entrypoints when they improve the same engineering decision; there is no requirement for one skill per chapter.

| Book chapter / PDF pages | Operational home | What the agent does |
| --- | --- | --- |
| 1 Introduction / 14–18 | `posd-design-review`, all focused skills | Use concrete code/caller tasks; investigate red flags and compare alternatives with moderation |
| 2 The Nature of Complexity / 19–26 | `posd-complexity` | Trace developer burden to dependencies/obscurity; prioritize common tasks without inventing a score |
| 3 Working Code Isn’t Enough / 27–33 | `posd-strategic-design` | Compare the clean resulting abstraction with a patch and make a bounded investment now |
| 4 Modules Should Be Deep / 34–43 | `posd-deep-modules` | Examine formal and informal caller contracts and simplify common use, not merely count methods |
| 5 Information Hiding (and Leakage) / 44–54 | `posd-information-hiding` | Give a representation/policy one owner; test temporal decomposition and necessary visibility |
| 6 General-Purpose Modules are Deeper / 55–66 | `posd-general-purpose` | Design a small somewhat general interface, placing specialization above or below the reusable core |
| 7 Different Layer, Different Abstraction / 67–77 | `posd-abstraction-layers` | Test layer value and pass-through variables; weigh contexts against hidden coupling |
| 8 Pull Complexity Downwards / 78–81 | `posd-pull-complexity-down` | Move repeated difficulty/default choices to a knowledgeable owner while preserving meaningful controls |
| 9 Better Together Or Better Apart? / 82–95 | `posd-module-boundaries` | Join shared knowledge; separate independent or specialized work; keep conceptual methods complete |
| 10 Define Errors Out Of Existence / 96–111 | `posd-error-design` | Distinguish elimination, masking, aggregation, and termination; preserve failures that matter |
| 11 Design it Twice / 112–115 | `posd-design-twice` | Compare substantively different interfaces or implementations using the same caller scenarios |
| 12 Why Write Comments? The Four Excuses / 116–122 | `posd-comments` | Preserve abstraction knowledge the code cannot express; avoid self-documenting-code excuses |
| 13 Comments Should Describe Things that Aren’t Obvious from the Code / 123–143 | `posd-comments` | Separate precision, intuition, interface contracts, implementation rationale, and shared design notes |
| 14 Choosing Names / 144–153 | `posd-naming` | Test the reader's mental picture at use sites and treat hard naming as design evidence |
| 15 Write The Comments First / 154–158 | `posd-comments`, `posd-design-twice`, `posd-design-review` | Draft the contract before implementation and use difficulty explaining it as design feedback |
| 16 Modifying Existing Code / 159–165 | `posd-strategic-design`, `posd-comments` | Improve the affected abstraction; retain rationale near its owner and check comments against the diff |
| 17 Consistency / 166–170 | `posd-consistency` | Transfer learning across genuinely similar operations, retaining visible semantic exceptions |
| 18 Code Should be Obvious / 171–177 | `posd-obvious-code` | Compare a reader's first inference with actual behavior; expose needed information at the reading site |
| 19 Software Trends / 178–185 | `posd-design-review`, `posd-strategic-design`, focused boundary skills | Judge inheritance, patterns, getters/setters, and development processes by complexity; design abstractions coherently |
| 20 Designing for Performance / 186–197 | `posd-performance` | Measure before/after, remove fundamental costs, and design a simple common critical path with a clear slow path |
| 21 Decide What Matters / 198–201 | `posd-decide-what-matters` | Find leverage, minimize where important facts must be understood, and make essential distinctions prominent |
| 22 Conclusion / 202–203; end lists / 210–212 | Whole collection | Check the common objective and red flags across workflows without making every red flag a mandatory finding |

## Fidelity boundaries

**Book principles:** complexity concerns understanding/modification; interfaces include informal obligations; hiding knowledge and allocating responsibility can matter more than shortening implementations; principles require judgment rather than universal bans. Chapter 19 distinguishes useful unit tests and bug reproduction from letting feature-by-feature TDD replace abstraction design. Its criticism is preserved as a design criterion; these skills do not dictate a development methodology.

**Project adaptations:** review/design/implementation modes, path-and-caller evidence, scope limits, migration accounting, and behavioral grading make the principles usable by coding agents. The book does not prescribe these output schemas, case IDs, or tooling. The suggested investment percentages and illustrative payoff estimates in Chapter 3 are not treated as empirical guarantees or per-task quotas. No method length, class count, reuse count, or depth ratio is used as a quality metric.

**Verification scope:** source calibration is distinct from packaging checks, behavioral case results, installed-client discovery, and performance measurement. See [behavioral evaluation](../evals/README.md) for the actual run protocol and results. A checked source map or valid YAML alone does not establish that an agent will make good design decisions in production.
