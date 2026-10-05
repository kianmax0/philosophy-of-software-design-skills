# Behavioral evaluation

The corpus contains **20 tasks covering all 17 skills**: 18 review/design tasks and two isolated implementation tasks. The fixtures deliberately contain design problems or justified differences; passing maintenance tests does not mean those fixtures have been repaired. Formatting and corpus checks do not grade agent decisions.

The [full-book calibration run](results/2026-10-05-calibration.md) preserves actual responses, the failed first obvious-code attempt and its rerun, skill hashes, qualitative grading, and executable implementation artifacts. The initial full-corpus run withheld the rubric and earlier answers but exposed descriptive case IDs; the revised exporter hides those IDs, and selected cases were repeated with opaque filenames/IDs. These conditions are recorded separately. The [initial smoke report](results/2026-10-05-smoke.md) is historical evidence for the earlier public-source revision.

## Run a blind task

Install maintenance dependencies as described in the repository README, then export one task without grading criteria:

```sh
python3 scripts/prepare_eval.py justified-authorization-boundary --output /tmp/posd-task.json
```

Give a fresh agent only that JSON payload and its referenced skill. The payload contains an opaque task ID, the request, and exact raw fixture; do not give it `cases.json`, intended answers, other skills, or prior outputs. A review/design task must remain read-only. For an implementation task, copy the raw fixture into an isolated temporary workspace and let the agent edit and check that copy. Keep production/source fixtures unchanged.

A portable evaluator instruction is:

```text
Read the task JSON and its single referenced skill. Complete the request using
its raw fixture. Save the unabridged response. For implementation, work only in
an isolated copy and preserve the executable changes/checks. Distinguish checks
actually run from proposed checks; record the loaded skill's SHA-256.
Do not read grading criteria or earlier answers and do not self-grade.
```

The helper validates corpus integrity before exporting, but does not execute the task, choose an agent, or grade its answer. `--root` accepts another repository checkout; without `--output` it emits JSON to stdout.

## Grade and record

A separate reviewer reads [cases.json](cases.json) and the actual response/artifacts. A case passes only if all acceptance criteria are met and no rejection condition occurs. Record per-criterion evidence and limitations. Judge decisions and compatibility, not prescribed wording or headings. Runtime/benchmark claims require executed evidence; asymptotic reasoning may be labeled as analysis.

Retain the full first response when a case fails. Change only guidance supported by the failure, then rerun with a fresh agent and retain the new response. Record skill revision/hash, request/fixture identity, date, agent conditions available, criterion results, and exact verification commands. Never replace an observed answer with an idealized version.

## Cases

| Case | Skill | Mode | Raw artifact |
| --- | --- | --- | --- |
| `shared-storage-knowledge` | `posd-information-hiding` | review | [importers.py](fixtures/importers.py) |
| `justified-authorization-boundary` | `posd-abstraction-layers` | review | [document_gateway.py](fixtures/document_gateway.py) |
| `absence-is-not-failure` | `posd-error-design` | review | [settings_store.py](fixtures/settings_store.py) |
| `trace-change-cost` | `posd-complexity` | review | [importers.py](fixtures/importers.py) |
| `combine-shared-record-policy` | `posd-module-boundaries` | review | [importers.py](fixtures/importers.py) |
| `consistency-with-meaningful-differences` | `posd-consistency` | review | [batch_writer.py](fixtures/batch_writer.py) |
| `comments-preserve-nonobvious-truth` | `posd-comments` | review | [comments_and_units.py](fixtures/comments_and_units.py) |
| `compare-delivery-contracts` | `posd-design-twice` | review | [notification_designs.py](fixtures/notification_designs.py) |
| `reduce-export-interface-depth-cost` | `posd-deep-modules` | review | [export_options.py](fixtures/export_options.py) |
| `review-entrypoint-scope` | `posd-design-review` | review | [document_gateway.py](fixtures/document_gateway.py) |
| `generality-from-real-use-cases` | `posd-general-purpose` | review | [export_options.py](fixtures/export_options.py) |
| `decision-owner-for-storage-format` | `posd-information-hiding` | review | [importers.py](fixtures/importers.py) |
| `choose-caller-visible-export-decisions` | `posd-decide-what-matters` | review | [export_options.py](fixtures/export_options.py) |
| `name-by-role-and-contract` | `posd-naming` | review | [search_names.py](fixtures/search_names.py) |
| `make-unexpected-branch-obvious` | `posd-obvious-code` | review | [search_names.py](fixtures/search_names.py) |
| `measure-before-adding-index` | `posd-performance` | review | [search_catalog.py](fixtures/search_catalog.py) |
| `move-shared-retry-mechanics-down` | `posd-pull-complexity-down` | review | [batch_writer.py](fixtures/batch_writer.py) |
| `bounded-design-investment` | `posd-strategic-design` | review | [importers.py](fixtures/importers.py) |
| `fix-optional-setting-failure-contract` | `posd-error-design` | implementation | [settings_store.py](fixtures/settings_store.py) |
| `centralize-versioned-record-construction` | `posd-information-hiding` | implementation | [importers.py](fixtures/importers.py) |

## Replay implementation evidence

```sh
python3 evals/results/verify_implementations.py
python3 evals/results/implementations/fix-optional-setting-failure-contract/check_settings_store.py
(cd evals/results/implementations/centralize-versioned-record-construction && python3 check_contract.py)
```

The independent checks compare importer behavior with the source fixture, including fractional/truncated timestamps, failures after partial writes, record kind/order, and legacy storage acceptance. They also check missing/present/false-valued settings, required reads, and operational exception identity/cause. The agent's own scripts are retained. A misleading comment in `check_contract.py` was corrected without changing checks or behavior; its original is preserved as `check_contract-original.txt`. Unknown record kinds remain accepted by the original storage contract, as the independent checks confirm.

## Limits of this evaluation

The tasks are small synthetic examples with one sample per final case. A passing run establishes those specific decisions and edits, not production effectiveness, client discovery, or general superiority over an ordinary prompt. Source calibration, package validation, agent behavior, and runtime performance are different claims. To compare ordinary prompting with these skills, run the same tasks and resources without skills under matched agent conditions and retain both distributions; the recorded calibration run is not that experiment.
