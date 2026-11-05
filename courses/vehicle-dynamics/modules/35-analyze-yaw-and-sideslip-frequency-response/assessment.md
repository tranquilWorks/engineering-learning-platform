# P35 course checkpoint

## Predict and derive

Recover the zero-frequency limit and explain the Hz-to-rad/s factor in the complex response.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `(j omega I-A) X=B Delta`
- `G_r(j omega)=r/Delta`
- `omega=2 pi f`

## Controlled comparison

- `speed_m_s`: 25 → 40. Hold the other controls at baseline; predict and explain the change before executing.
- `frequency_hz`: 1 → 2. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Solve (j*omega*I-A)H=B with omega=2*pi*f. At f=0 this becomes H=-A inverse B, the steady gain. At 1 Hz, omega is 6.283185 rad/s, not 1 rad/s; confusing them shifts both magnitude and phase. Yaw-rate gain has units 1/s and sideslip gain is dimensionless, so they use separate axes. The complex residual uses beta/steer and a one-second-scaled yaw/steer coordinate before taking its norm.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The frequency response assumes a linear time-invariant small-signal model; it does not include nonlinear limit handling or large-amplitude tire saturation.

Competency links: VD-HANDLING-LINEAR. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
