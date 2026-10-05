---
name: posd-general-purpose
description: Use when an API or module has been shaped around one current caller and similar callers are duplicating work or requesting awkward extensions
license: MIT
---

# General-Purpose Modules

Use this skill when deciding whether an interface should serve a broader set
of related needs. A general-purpose module offers a coherent capability rather
than encoding one caller's immediate sequence. Good generality comes from
concrete expected use cases. It does not mean adding options for imagined
futures or building a framework around one implementation.

## Inputs and evidence

Inspect the proposed API, its implementation, tests, and current call sites.
Gather the request that prompted the change plus nearby use cases already
present in the code or explicitly required. For each use case, record the
desired outcome and the caller choices it needs. Cite the source of each use
case by path, line, symbol, or request statement. Do not infer demand from the
possibility that another caller might exist.

## Review procedure

1. Write the common capability in terms of outcomes, not the current caller's
   sequence of steps.
2. Compare the interface against each evidenced use case. Mark where callers must
   reproduce module policy or where the API cannot express a real need.
3. Propose the smallest stable set of operations that supports those cases. Keep
   policy choices explicit only when callers legitimately differ.
4. Check that the implementation can support the interface without speculative
   flags, mode parameters, unused extension hooks, or caller-specific names
   and defaults.
5. Trace existing use cases and errors through the proposal. Identify migration
   costs and any changed behavior before editing.

For implementation work, expand the contract only as far as the evidenced
cases require. Preserve existing behavior for existing callers unless the
request authorizes a change. Avoid broadening the task to unrelated API
redesign.

## Output

Return the use cases and their evidence, the proposed contract, and a short
explanation of what each operation enables. For a patch, identify
compatibility effects and relevant verification. State when the evidence
supports keeping a narrow, specialized interface.

## Example

Before: `invoicePage` calls `fetchInvoice`, retries once, then translates
status codes; a second caller repeats that sequence. After:
`invoiceClient.getInvoice(id)` owns transport and retry behavior and returns a
stable result. The page still owns layout, while a caller with a genuinely
different retry policy can request an explicit option if that need is
established.

## Leave the design alone when

- Only one narrow use case exists and specialization keeps its contract clear.
- Broader use would require guesses about policy or incompatible semantics.
- The proposed abstraction adds configuration and indirection without reducing
  duplicated knowledge.
- Apparent duplication is a justified adapter for separate security, platform,
  or vendor boundaries.

Principle provenance: John Ousterhout's [Stanford CS190 Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign). The workflow and example here are original adaptations.
