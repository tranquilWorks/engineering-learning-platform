# P02 course checkpoint

## Predict and derive

Reconstruct the signed force ledger before computing longitudinal acceleration.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Signed force vector sum and Newton balance`

## Controlled comparison

- `tractive_force_n`: 4200.0 → 0.0. Hold the other controls at baseline; predict and explain the change before executing.
- `speed_mps`: 20.0 → 55.0. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Apply m*a=tractive force minus drag, rolling resistance and the declared grade term. Each term is newtons; dividing only the final signed sum by kilograms gives m/s². Doubling speed multiplies quadratic drag by four, not two. A request smaller than resistance implies deceleration, not negative mass or a force-unit conversion. Compare the physical ledger with the broken result and identify the first omitted or mis-signed term.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Constant coefficients and a lumped mass do not identify a real coastdown curve or model wheel slip.

Competency links: VD-MOTION-FRAMES, VD-FORCE-BALANCE. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P02 evidence task

At 20 m/s, calculate the traction request for zero acceleration. Compare the nominal and road-load-omission results at that request. Repeat the force accounting at 40 m/s, keeping the request fixed. Explain the sign of acceleration in each case and the limitation of the zero-speed endpoint.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

At 20 m/s the balancing request is 346.138 N. Nominal acceleration is zero; omission incorrectly predicts about 0.262226 m/s². At 40 m/s the nominal result becomes negative because drag rises by 455.7 N. A complete response names all three force terms and avoids treating the low-speed approximation as a start/stop simulator.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

For 4200 N and 20 m/s, rolling resistance is 194.238 N and drag is 151.900 N. The net force is 3853.862 N and acceleration is 2.91959 m/s². At 40 m/s, drag becomes 607.600 N, four times its previous value. The acceleration is then about 2.57437 m/s². Doubling speed does not quarter acceleration: only the quadratic drag term changes, while traction and rolling resistance remain fixed.

Drag depends on V², while aerodynamic power would depend on V³. Do not label the force-budget chart as power or time response. A traction ceiling that never activates is not evidence that a saturation implementation has been tested.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
