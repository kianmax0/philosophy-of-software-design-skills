# Behavioral evaluation

These original fixtures exercise three decisions. Metadata and link checks do not run the cases or establish recommendation quality.

The [initial smoke report](results/2026-10-05-smoke.md) records observed collaboration-agent responses and their limitations.

## Run a case

Read [cases.json](cases.json). Give a fresh agent only the selected skill, its case request, and the corresponding raw fixture. It can inspect the supplied artifacts but should not edit files. Do not supply the acceptance/rejection criteria or an intended answer to that agent.

For example:

```text
Use the skill at skills/posd-abstraction-layers/SKILL.md for this request:
Review this layer. Is its mostly forwarding interface a design problem?
Give your assessment with code evidence. Do not edit files.

Raw artifact: evals/fixtures/document_gateway.py
```

Then assess the actual response against the case criteria. A case passes only if all acceptance criteria are met and no rejection condition occurs. Record limitations and contested judgments rather than replacing the response with an idealized answer.

## Cases

| Case | Artifact | Decision |
| --- | --- | --- |
| Shared storage knowledge | [importers.py](fixtures/importers.py) | Localize storage schema and timestamp representation |
| Justified authorization boundary | [document_gateway.py](fixtures/document_gateway.py) | Retain a forwarding layer that owns a meaningful invariant |
| Absence is not failure | [settings_store.py](fixtures/settings_store.py) | Simplify expected absence without suppressing operational errors |

The fixtures isolate review decisions and are not production implementations. An agent should not infer unprovided product requirements or a complete system audit from them.

## Record and compare

Record the date, skill revision, agent/model information available, request, raw artifact, observed response, criterion results, and review limitations. Preserve actual output. If evaluation uses collaboration subagents, say so; it is not proof of installation and discovery in a separate client.

For a comparison against an ordinary prompt, repeat each case with the same request and artifact without the skill, using an independent agent under the same conditions. Report both outputs and disagreements. The initial smoke cases cannot support a broad performance or design-quality improvement claim.
