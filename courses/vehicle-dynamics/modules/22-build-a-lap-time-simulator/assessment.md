# P22 course checkpoint

## Predict and derive

Reconstruct the forward acceleration and backward braking constraints on a periodic lap.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `v_grip=sqrt(mu*g/|kappa|); v_i^2<=v_prev^2+2*a*ds; v_i^2<=v_next^2+2*b*ds; dt=2*ds/(v_i+v_next)`

## Controlled comparison

- `friction_coefficient`: 1.05 → 0.7. Hold the other controls at baseline; predict and explain the change before executing.
- `acceleration_limit_m_s2`: 3.5 → 6. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Squared-speed propagation gives v_next²-v²=2*a*ds. A corner speed ceiling alone is insufficient: the car must brake early enough to reach it and accelerate out subject to its force bound. Check the closing segment as well as interior segments. Increasing acceleration capability need not improve a lap dominated by corner grip or braking. Explain the active constraint at the slowest and fastest segments.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This synthetic circuit and simplified force envelope are not measured lap performance or driver validation.

Competency links: VD-PERFORMANCE-OPTIMIZATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
