# P60 course checkpoint

## Predict and derive

Classify missing, duplicate, inverted and malformed records before deciding what can actually be recovered.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `missing=expected_sequences-valid_unique_sequences`
- `malformed={k where payload_length(k)!=4+DLC(k)}`
- `recovered=sort(unique(valid_packets)) subject to bounded reorder window`

## Controlled comparison

- `inspection_limit`: 309 → 180. Hold the other controls at baseline; predict and explain the change before executing.
- `reorder_window`: 2 → 0. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Dropping sequence 37 and truncating 89 create two unusable expected records in the full fixture; a duplicate at 52 and inversion at 71/72 are different faults. Deduplicate and sort only valid records, and enforce the declared reordering window. Recovery means a valid ordered subset, not inventing the missing payloads. Compare record identities and payload lengths with the nominal fixture, then replay the same diagnosis after reset.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Known nominal lengths and a deterministic fault plan make this an auditable protocol exercise, not a general live-stream intrusion detector or proof of lossless recovery.

Competency links: VD-TELEMETRY-PROTOCOL, VD-IDENTIFICATION-UNCERTAINTY, VD-SYSTEM-INTEGRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
