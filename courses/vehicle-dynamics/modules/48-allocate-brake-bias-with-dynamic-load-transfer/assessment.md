# P48 course checkpoint

## Predict and derive

Calculate the requested-deceleration axle loads and explain why a clipped result is only a conditional allocation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Delta F_z=m a_x h/L`
- `F_zf=m g b/L+Delta F_z and F_zr=m g a/L-Delta F_z`
- `F_b,k<=mu F_z,k and a_achieved=(F_bf+F_br)/(m g)`

## Controlled comparison

- `deceleration_g`: 0.9 → 1.1. Hold the other controls at baseline; predict and explain the change before executing.
- `front_brake_bias`: 0.62 → 0.72. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Front load is static front weight plus m*a*h/L; rear loses the same amount. Ideal force fraction equals front dynamic load divided by mg if both axles share the same friction coefficient. Clipping front and rear brake requests separately can produce an achieved deceleration below the requested one. The displayed loads were computed from the request, so this one-pass study is not a self-consistent solution using the lower achieved acceleration. Diagnose the broken static-load allocation with axle utilization.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Do not treat the conditional allocation as a full braking equilibrium or ABS controller. Re-solving load transfer with achieved acceleration would be a separate coupled model.

Competency links: VD-FORCE-BALANCE, VD-BRAKES. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
