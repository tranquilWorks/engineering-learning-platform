# P51 course checkpoint

## Predict and derive

Show how an unknown landmark changes the nonlinear graph state.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `X*=argmin_X sum_i ||h_i(X)-z_i||^2_{Omega_i}`
- `(J^T J) delta=-J^T r, followed by X<-X+delta and relinearization`
- `one absolute prior removes the two-dimensional translation gauge`

## Controlled comparison

- `loop_noise_m`: 0.08 → 0.5. Hold the other controls at baseline and explain the mechanism before executing.
- `pose_count`: 30.0 → 100.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Robot position, heading and landmark coordinates are optimized jointly; relative observations leave three planar gauge freedoms without an anchor.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Known correspondences and a single initialized circuit omit loop discovery and global SLAM.

Competency links: SLAM-MAPPING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
