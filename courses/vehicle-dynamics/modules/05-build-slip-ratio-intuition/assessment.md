# P05 course checkpoint

## Predict and derive

Explain the sign and local slope of longitudinal tire force and distinguish stiffness from peak force.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Logistic evaluation of signed tire saturation`

## Controlled comparison

- `slip_ratio`: 0.08 → -0.3. Hold the other controls at baseline; predict and explain the change before executing.
- `normal_load_n`: 3600.0 → 6000.0. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A signed slip input must produce an odd force response in this symmetric model: reversing slip reverses force. Near zero, differentiate the declared law to obtain stiffness; at larger slip compare force with mu*Fz. Increasing load can raise capacity without changing the interpretation of slip as a dimensionless ratio. Use a negative-slip prediction to expose a sign or percent-versus-fraction error that a positive baseline could hide.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The model does not resolve contact-patch dynamics, low-speed slip singularities or a measured road surface.

Competency links: VD-TIRE-LONG. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P05 evidence task

At 3600 N, compare ±0.001 and ±0.08 slip. Check signs, odd symmetry, initial slope and force capacity. Activate the sign fault and state which checks it still passes. Then explain the zero-slip result while changing load.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

The initial slope is approximately 85000 N per unit slip, whereas the larger-slip points bend toward ±3780 N. The sign-reversed curve remains odd and bounded but violates the declared force/slip sign. Zero slip gives zero force at every allowed load, so a nonzero test is essential.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

At κ = 0.08 and F_z = 3600 N, capacity is 3780 N and the dimensionless argument is 6800/3780 ≈ 1.79894. The force is about 3578.5 N, below capacity. The linear prediction 85000 × 0.08 = 6800 N would greatly exceed the bound. Near κ = 0.001, the force is approximately 85 N, because this point lies in the nearly linear part of the curve.

A bounded force can still point the wrong way. A force plateau does not mean the initial stiffness has changed, and larger load does not produce a simple proportional scaling at every slip.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
