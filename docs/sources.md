# Sources and provenance

This repository contains original AI-oriented review procedures inspired by ideas in John Ousterhout's *A Philosophy of Software Design*. The book itself was not supplied as source material for this project. This page and the individual skill files link to public author/Stanford materials that support the principle-level framing.

The [author's book page](https://web.stanford.edu/~ouster/cgi-bin/book.php) identifies the second edition as released in July 2021, notes that Chapter 6 was expanded, and identifies “Decide What Matters” as a new chapter. The linked book extract is limited. Stanford course notes from different years are teaching outlines and may reflect different editions or emphasis. This repository therefore does not claim a definitive complete table of contents or assign chapter numbers to principles unless the cited primary page explicitly does so. Consult a lawfully obtained copy of the relevant edition for full context.

The procedures, checklists, decision questions, output formats, and examples in these skills are project-authored adaptations. They are not quotations, chapter summaries, or official guidance from Ousterhout or Stanford. This project is independent and is not endorsed by the author or Stanford University.

## Primary references

- [Ousterhout's book page](https://web.stanford.edu/~ouster/cgi-bin/book.php): edition facts, limited extract, and the stated changes to the second edition.
- [Stanford CS190, Winter 2018: The Nature of Complexity](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=complexity): complexity, dependencies, obscurity, and reader-facing design concerns.
- [Stanford CS190, Winter 2018: Working Isn't Good Enough](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=working): strategic and tactical programming; explicitly labels the reading as Chapter 3.
- [Stanford CS190, Winter 2018: Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign): interfaces, deep modules, information hiding, general-purpose design, distinct layer abstractions, and pulling complexity down; explicitly labels readings as Chapters 4–7 and 14.
- [Stanford CS190, Winter 2020: book discussion](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview): a broad list of discussed topics, including error design, comments, naming, what matters, designing twice, complexity placement, and abstraction layers.
- [Stanford CS190, Winter 2024: wrap-up slides](https://web.stanford.edu/~ouster/cs190-winter24/slides/wrapup.pdf): red flags including shallow modules, inconsistency, unnecessary specialization, information leakage, pass-through methods, obscurity, duplication, and special cases.
- [Stanford CS190, Winter 2022 course information](https://web.stanford.edu/~ouster/cs190-winter22/info/): identifies the second edition as the course text and describes an iterative code-review and revision approach.
- [Stanford CS190, Winter 2018: Raft project review](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=raftReview2): examples of combining and separating responsibilities and focusing on significant performance costs.
- [Author-hosted second-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf): limited text; includes material from “Decide What Matters.”

## Principle coverage by skill

| Skill ID | Principle focus | Primary grounding |
| --- | --- | --- |
| `posd-design-review` | Route a concrete review to relevant checks; evidence-bounded findings | [CS190 course information](https://web.stanford.edu/~ouster/cs190-winter22/info/), [book page](https://web.stanford.edu/~ouster/cgi-bin/book.php) |
| `posd-complexity` | Change amplification, cognitive load, unknown dependencies; minimize apparent complexity | [Nature of Complexity](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=complexity) |
| `posd-strategic-design` | Strategic vs tactical programming; improve design within a bounded change | [Working Isn't Good Enough](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=working) |
| `posd-decide-what-matters` | Focus on important caller needs and hide details that need not matter to callers | [Book page](https://web.stanford.edu/~ouster/cgi-bin/book.php), [book extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf) |
| `posd-deep-modules` | Rich functionality behind a simple interface | [Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign) |
| `posd-information-hiding` | Encapsulate design decisions and avoid information leakage | [Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign) |
| `posd-general-purpose` | Choose generality based on real reuse and caller needs | [Book page](https://web.stanford.edu/~ouster/cgi-bin/book.php), [Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign) |
| `posd-abstraction-layers` | Each layer should provide a distinct abstraction; pass-through methods are a warning sign | [Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign), [wrap-up slides](https://web.stanford.edu/~ouster/cs190-winter24/slides/wrapup.pdf) |
| `posd-pull-complexity-down` | Put difficult mechanism behind an interface that reduces user burden | [Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign) |
| `posd-module-boundaries` | Compare combining and separating around shared knowledge and dependencies | [Raft project review](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=raftReview2), [book discussion](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview) |
| `posd-error-design` | Reduce exceptional cases and clarify where failures are handled | [Book discussion](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview) |
| `posd-design-twice` | Compare multiple plausible designs before committing | [Book discussion](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview), [Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign) |
| `posd-comments` | Use comments to communicate knowledge that code cannot make clear | [Book discussion](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview), [wrap-up slides](https://web.stanford.edu/~ouster/cs190-winter24/slides/wrapup.pdf) |
| `posd-naming` | Names make important meaning easier to recognize | [Book discussion](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview), [wrap-up slides](https://web.stanford.edu/~ouster/cs190-winter24/slides/wrapup.pdf) |
| `posd-consistency` | Reuse conventions to reduce surprise while preserving justified semantic differences | [Wrap-up slides](https://web.stanford.edu/~ouster/cs190-winter24/slides/wrapup.pdf) |
| `posd-obvious-code` | Make code structure and behavior understandable to readers | [Nature of Complexity](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=complexity), [wrap-up slides](https://web.stanford.edu/~ouster/cs190-winter24/slides/wrapup.pdf) |
| `posd-performance` | Focus on significant performance costs and assess design tradeoffs | [Raft project review](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=raftReview2) |

This mapping says which primary materials support each skill's principle-level inspiration. It does not imply that every checklist item or operational rule appears in those sources.
