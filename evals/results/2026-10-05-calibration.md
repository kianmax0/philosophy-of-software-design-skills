# Full-book calibration and validation

Date: 2026-10-05. Scope: all 17 skill entrypoints and repository documentation/tooling. The source is the supplied 2021 second-edition PDF; identity and chapter-to-action mapping are in [sources](../../docs/sources.md).

## Delivered changes

All 17 skills now guide concrete caller/interface inspection, book-specific design decisions, supported retention conditions, and bounded implementation with contract/caller updates and actual verification. The standalone entrypoint handles review, new design, and implementation. Comments-first, ongoing strategic modification, coherent abstraction design, context-object tradeoffs, specialization placement, four error-design techniques, and critical-path performance design are operational steps rather than chapter summaries.

The corpus now covers every skill. The validator checks its integrity/coverage alongside packaging; [prepare_eval.py](../../scripts/prepare_eval.py) exports task-only input with opaque identifiers. The [independent source review](source-review.txt) found no material remaining fidelity issue. Its scope and source passages are recorded in that report.

## Observed behavior and grading

**20/20 final corpus cases passed** an independent qualitative review against every acceptance/rejection criterion. A separate initial obvious-code attempt failed and is retained below. Two cases produced implementation artifacts and executable checks rather than advice alone.

Each task used a fresh collaboration agent with no inherited conversation, the specified single skill, request, and raw fixture; rubric and previous responses were withheld. No model override was requested. The tool did not expose an exact runtime model identifier. The initial full-corpus runs used descriptive case IDs and paths, so they are **criterion-withheld forward-tests, not fully blinded trials**. Tooling review identified that cue; the exporter was fixed and three cases were repeated using opaque IDs and filenames. Synthetic requests and fixture documentation still provide substantial guidance. No comparison against skill-free ordinary prompting or general efficacy claim is made.

The [manifest](calibration-manifest.json) records base commit, source/corpus/skill/fixture/response hashes and exact requests. The [per-criterion grading](grading.json) and [reviewer summary](grading-review.txt) preserve evidence and limitations. The summary's original “blind-response” title is retained as received; the actual input conditions are specified here. Retained supplementary task payloads normalize skill file paths for portability; use the exporter for live paths.

| Case | Skill | Result | Observed decision / evidence | Raw output |
| --- | --- | --- | --- | --- |
| `shared-storage-knowledge` | `posd-information-hiding` | Pass | Storage owner, source kind, exact conversion/order and unknown consumers | [response](responses/shared-storage-knowledge.txt) |
| `justified-authorization-boundary` | `posd-abstraction-layers` | Pass | Retains centralized authorization; removal would distribute enforcement | [response](responses/justified-authorization-boundary.txt) |
| `absence-is-not-failure` | `posd-error-design` | Pass | Only documented KeyError becomes absence; operational failures remain visible | [response](responses/absence-is-not-failure.txt) |
| `trace-change-cost` | `posd-complexity` | Pass | Traces duplicated schema/conversion knowledge to coordinated edits | [response](responses/trace-change-cost.txt) |
| `combine-shared-record-policy` | `posd-module-boundaries` | Pass | Shared import policy separated from source kind and legacy Store contract | [response](responses/combine-shared-record-policy.txt) |
| `consistency-with-meaningful-differences` | `posd-consistency` | Pass | Aligns retry mechanics while preserving non-idempotent payment semantics | [response](responses/consistency-with-meaningful-differences.txt) |
| `comments-preserve-nonobvious-truth` | `posd-comments` | Pass | Corrects stale conversion claim and retains unit precision | [response](responses/comments-preserve-nonobvious-truth.txt) |
| `compare-delivery-contracts` | `posd-design-twice` | Pass | Selects inline notification for immediate delivery-failure reporting | [response](responses/compare-delivery-contracts.txt) |
| `reduce-export-interface-depth-cost` | `posd-deep-modules` | Pass | Retains output control; does not claim grouping alone creates depth | [response](responses/reduce-export-interface-depth-cost.txt) |
| `review-entrypoint-scope` | `posd-design-review` | Pass | Limits review to supported authorization/layer facts and missing context | [response](responses/review-entrypoint-scope.txt) |
| `generality-from-real-use-cases` | `posd-general-purpose` | Pass | CSV/JSON/selection capability without a speculative plugin framework | [response](responses/generality-from-real-use-cases.txt) |
| `decision-owner-for-storage-format` | `posd-information-hiding` | Pass | Localizes changing representation and preserves source identity | [response](responses/decision-owner-for-storage-format.txt) |
| `choose-caller-visible-export-decisions` | `posd-decide-what-matters` | Pass | Header control remains; ISO assumption and migration need are explicit | [response](responses/choose-caller-visible-export-decisions.txt) |
| `name-by-role-and-contract` | `posd-naming` | Pass | Semantic names, public keyword compatibility and uninspected consumers | [response](responses/name-by-role-and-contract.txt) |
| `make-unexpected-branch-obvious` | `posd-obvious-code` | Pass | Rerun preserves positional behavior and accounts for keyword migration | [response](responses/make-unexpected-branch-obvious.txt) |
| `measure-before-adding-index` | `posd-performance` | Pass | No invented speedup; accounts for duplicates, mutation and baseline workload | [response](responses/measure-before-adding-index.txt) |
| `move-shared-retry-mechanics-down` | `posd-pull-complexity-down` | Pass | Opt-in retry mechanism; domain validation and payment semantics remain | [response](responses/move-shared-retry-mechanics-down.txt) |
| `bounded-design-investment` | `posd-strategic-design` | Pass | Compares duplication with bounded ownership improvement for third importer | [response](responses/bounded-design-investment.txt) |
| `fix-optional-setting-failure-contract` | `posd-error-design` | Pass | Implemented narrow absence handling; actual executable checks retained | [response](responses/fix-optional-setting-failure-contract.txt) |
| `centralize-versioned-record-construction` | `posd-information-hiding` | Pass | Implemented record ownership; exact legacy/partial-write semantics replayed | [response](responses/centralize-versioned-record-construction.txt) |

## Failed attempt and correction

The [first obvious-code response](responses/make-unexpected-branch-obvious-attempt-1.txt) recommended a keyword-only selector without a migration path for existing positional callers. Independent grading marked the caller-compatibility criterion unmet. The [loaded skill snapshot](snapshots/posd-obvious-code-attempt-1.txt) is retained. Guidance was narrowed to check positional, keyword, result-shape, and external consumers and make unsupported signature changes conditional. A fresh agent's [final response](responses/make-unexpected-branch-obvious.txt) preserved positional behavior and required keyword migration; it passed. No first response was replaced by an idealized answer.

## Opaque-identifier supplementary repeats

[Supplementary per-criterion grading](opaque-grading.json) records three fresh repeats after hiding semantic case IDs and using neutral task paths: authorization boundary, standalone entrypoint scope, and unmeasured index proposal. [Response 01](responses/opaque-response-01.txt), [response 02](responses/opaque-response-02.txt), and [response 03](responses/opaque-response-03.txt) retain actual output. **3/3 supplementary repeats passed** their mapped criteria. These repeats are distinct from the original 20-case run.

## Tooling review and regression fixes

The [initial tooling review](tooling-review-initial.txt) found three concrete issues. All were fixed and [independently rechecked](tooling-review-final.txt):

- Semantic case IDs revealed judgment cues. Exported IDs are now opaque, and the output-boundary regression checks omit rubric fields and original IDs.
- A list/object `mode` caused an unhashable-type crash. The validator now checks type first and reports a normal validation error for list/dict/null/integer modes.
- The agent's importer check script comment claimed unknown kinds were rejected, while its checks only covered schema/type failures. The comment now states the actual checks; [the original script](implementations/centralize-versioned-record-construction/check_contract-original.txt) is retained. Legacy unknown-kind acceptance remains preserved.

Regression tests were observed failing before the relevant fixes, then passing. The earlier absolute-fixture-path portability gap was also reproduced and fixed. No skill behavior was changed by the exporter/type/comment fixes.

## Reproducible verification

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 evals/results/verify_implementations.py
python3 evals/results/implementations/fix-optional-setting-failure-contract/check_settings_store.py
(cd evals/results/implementations/centralize-versioned-record-construction && python3 check_contract.py)
```

Maintenance validation covers 17 packages, local links, all case records, and 22 unit tests. The independent implementation verifier has four tests comparing importer results and partial-write effects with the original, checking legacy storage behavior/copying, required/optional/falsy setting values, and operational exception identity/cause. The agent settings suite has five tests; its importer contract script also passes. All skill folders passed the skill-creator frontmatter validator and copied in isolation with matching MIT licenses. Final command results were checked after assembling these artifacts; no client installation/discovery test is claimed.

Implementation artifacts: [settings_store.py](implementations/fix-optional-setting-failure-contract/settings_store.py), [its checks](implementations/fix-optional-setting-failure-contract/check_settings_store.py), [importers.py](implementations/centralize-versioned-record-construction/importers.py), and [its checks](implementations/centralize-versioned-record-construction/check_contract.py). They use deterministic fakes and fixture-scale inputs; they do not contact live systems or supply runtime performance evidence.

This is source calibration plus specific behavioral/implementation verification on small examples. It does not establish coverage of production workloads, unbiased comparative benefit, or reliability across models and repeated samples. Source principles and project-authored execution conventions remain distinct.
