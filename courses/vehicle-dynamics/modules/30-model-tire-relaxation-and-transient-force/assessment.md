# P30 course checkpoint

## Predict and derive

Predict the tire force at one relaxation length and distinguish spatial from temporal response.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `dF/ds=(F_ss-F)/sigma`
- `tau=sigma/v`
- `F(s)=F_ss*(1-exp(-s/sigma))`

## Controlled comparison

- `relaxation_length_m`: 0.45 → 1.35. Hold the other controls at baseline; predict and explain the change before executing.
- `speed_m_s`: 20 → 55. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The time constant is tau=lambda/v. At lambda=0.45 m and v=20 m/s, tau=0.0225 s. After traveling one relaxation length, a first-order step response reaches 1-exp(-1), about 63.2 percent of its final force. Doubling speed halves the time constant but leaves the distance constant unchanged. Treating lambda as seconds makes the result incorrectly insensitive to speed.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This first-order relaxation model assumes constant speed and a fixed target force; it does not resolve contact-patch physics.

Competency links: VD-TIRE-LONG, VD-TIRE-LAT. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
