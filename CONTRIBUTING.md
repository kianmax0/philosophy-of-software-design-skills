# Contributing

Improve a skill when a concrete task demonstrates a missing decision rule or a misleading recommendation. Keep each skill independently installable and its description specific enough for discovery.

## Skill contract

- Identify the engineering task and the evidence needed from code, callers, or requirements.
- Give a procedure that changes decisions rather than a chapter summary.
- Require a concrete consequence and a bounded recommendation.
- Include an exception or counterexample that prevents overgeneralization.
- Write original examples and attribute the principle with a primary source link.
- Preserve the user's scope. Reviews report findings; implementation requires an implementation request.
- Keep instructions self-contained. Links to optional references must stay within the skill folder.

Avoid mandatory class sizes, complexity scores without a validated definition, universal bans on wrappers or exceptions, unnecessary frameworks, and copied source passages. Document source limitations in [docs/sources.md](docs/sources.md).

## Verification

Run the commands in [README.md](README.md). For a decision-rule change, also run a relevant [evaluation case](evals/README.md) with a fresh agent. Provide the request, loaded skill, raw code, and observed output. Include a case where the recommendation should be withheld.

Do not report behavioral success from metadata validation alone. To claim that a skill improves an ordinary prompt, compare both under the same task and resources, record agent/model conditions, and retain outputs. Small smoke tests establish only that specific cases were handled.

Keep changes focused. If a new skill largely repeats an existing procedure, improve that skill or make its routing more precise before adding another entrypoint.
