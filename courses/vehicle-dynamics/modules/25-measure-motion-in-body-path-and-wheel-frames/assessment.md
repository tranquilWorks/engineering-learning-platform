# P25 course checkpoint

## Predict and derive

Compare path, body and wheel velocity components while proving norm preservation and checking direction.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `v_path=R(-psi_path)*v_inertial`
- `v_body=R(-psi_body)*v_inertial`
- `v_wheel=R(-delta)*v_body`
- `||R(theta)*v||_2=||v||_2`

## Controlled comparison

- `path_heading_deg`: 32 → 90. Hold the other controls at baseline; predict and explain the change before executing.
- `wheel_steer_deg`: 8 → 25. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A planar rotation preserves vx²+vy² because R transpose times R is identity. Rotating a 10 m/s inertial x-vector into a frame turned 90 degrees gives approximately (0,-10) m/s under R(-psi). Norm preservation alone cannot expose using a degree value as radians: the wrong angle still makes an orthogonal matrix. Compare the actual expected components and inverse transform, not only the norm residual.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

These are planar rigid-frame transforms with declared headings, not full three-dimensional sensor alignment.

Competency links: VD-MOTION-FRAMES, VD-STATE-RECONSTRUCTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
