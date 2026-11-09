# P36 course checkpoint

## Predict and derive

Classify the sign of the understeer gradient and test its singular boundary without treating a sentinel as a speed.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `K=W_f/C_f-W_r/C_r`
- `delta=L/R+K a_y/g`
- `V_char=sqrt(g L/K) for K>0`

## Controlled comparison

- `front_cornering_n_rad`: 65000 → 90000. Hold the other controls at baseline; predict and explain the change before executing.
- `rear_cornering_n_rad`: 80000 → 60000. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

For the declared axle loads, K=Wf/Cf-Wr/Cr. Increasing front stiffness reduces K; increasing rear stiffness raises K. When K is positive, characteristic speed is sqrt(g*L/K); when negative, the separate linear critical speed is sqrt(-g*L/K). At neutral steer neither is finite. The plot omits an unavailable characteristic-speed point and the metric exposes applicability. Near neutrality, large speed sensitivity reflects the denominator, not a reliable operating limit.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

These characteristic quantities belong to the linear model and do not imply tire feasibility, safe operation or global stability.

Competency links: VD-HANDLING-LINEAR. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
