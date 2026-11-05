# P67 course checkpoint

## Predict and derive

Defend the digital twin's complete interface ledger and explain what its uncertainty envelope does and does not mean.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `synthetic Fy=min(C_alpha*slip,mu*Fz0); fit C_alpha and mu on separate linear/saturated records`
- `sum wheel_loads=mg+downforce; capacity=sum mu*Fz0*(Fz/Fz0)^0.9 N`
- `wheel_force=m delta(v^2)/(2ds)+drag+rolling; gear, brake and combined-grip bounds constrain cyclic speeds`
- `lap_time=sum(ds/v); friction endpoint envelope from independently executed parameter cases`

## Controlled comparison

- `setup_delta`: 0.08 → 0.02. Hold the other controls at baseline; predict and explain the change before executing.
- `uncertainty_fraction`: 0.05 → 0.1. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Fit stiffness and friction from separate synthetic linear/saturated samples and check the unused tire samples. Trace calibrated forces through individual wheel loads, gear selection, cyclic acceleration/braking and lap time. The 0.8 lateral and 0.6 longitudinal reserve fractions satisfy 0.8²+0.6²=1; neither reserve is independently available in full. Check minimum wheel load, load sum, power, brake and combined-grip bounds on every segment. Execute both friction endpoints to obtain a scenario envelope, and reject the double-downforce fault from the physical load ledger.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Nine constant-offset paths and a 96-segment lap are a bounded discrete design search. The endpoint envelope is not a confidence interval; brake temperature is adiabatic without fade feedback, and no real GR86 performance or safety claim follows.

Competency links: VD-PERFORMANCE-OPTIMIZATION, VD-SYSTEM-INTEGRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
