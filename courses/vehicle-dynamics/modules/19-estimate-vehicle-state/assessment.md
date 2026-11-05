# P19 course checkpoint

## Predict and derive

Derive the constant-turn radius and independently predict the endpoint from speed and yaw rate.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `kappa=r/v; a_y=v*r; x_dot=v*cos(psi); y_dot=v*sin(psi); psi_dot=r`

## Controlled comparison

- `speed_m_s`: 20 → 5. Hold the other controls at baseline; predict and explain the change before executing.
- `yaw_rate_deg_s`: 8 → 30. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Convert 8 deg/s to 0.139626 rad/s; at 20 m/s the turn radius is about 143.24 m. Midpoint heading integration approximates the circular path. As yaw rate tends to zero, endpoint displacement tends to speed times duration and physical radius tends to infinity. A zero radius sentinel in the historical signature means the straight-line branch, not a zero-radius turn.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Constant speed and yaw do not constitute state estimation from noisy sensors; no observability or uncertainty claim follows.

Competency links: VD-STATE-RECONSTRUCTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
