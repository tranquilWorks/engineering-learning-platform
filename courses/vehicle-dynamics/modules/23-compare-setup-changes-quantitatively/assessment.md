# P23 course checkpoint

## Predict and derive

Preserve sector pairing and separate aero, tire and interaction effects in a setup comparison.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `delta_i=t_i,candidate-t_i,baseline; delta_lap=sum(delta_i)=aero+tire+interaction`

## Controlled comparison

- `aero_change_percent`: 10 → -20. Hold the other controls at baseline; predict and explain the change before executing.
- `tire_mu_change_percent`: 5 → 15. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The four baseline sectors sum to 116 s. Candidate-minus-baseline deltas must be paired by sector and sum to the lap delta. The declared aero, tire and interaction contributions must close that same delta. A shuffled sector pairing can leave a total unchanged while corrupting variability and explanation. Distinguish the 0.20 s decision threshold from uncertainty or a statistical significance claim.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Deterministic sensitivities and sector variation are not repeated independent track trials or an empirically calibrated confidence interval.

Competency links: VD-PERFORMANCE-OPTIMIZATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
