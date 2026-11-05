# P01 course checkpoint

## Predict and derive

Derive curvature from steering-wheel angle and predict separately what doubles when speed doubles.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Trigonometric curvature and independent sinc/half-angle path integration`

## Controlled comparison

- `steering_deg`: 5.0 → -20.0. Hold the other controls at baseline; predict and explain the change before executing.
- `speed_mps`: 15.0 → 45.0. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Wheel angle is steering-wheel angle divided by 13, then converted to radians. Curvature is tan(delta)/L. At fixed steering, radius is unchanged, yaw rate v*kappa doubles and lateral demand v²*kappa quadruples when speed doubles. A zero-steer limit must approach a straight path continuously. Bypassing the ratio can preserve a smooth trajectory while violating the declared input convention; inspect curvature and grip demand, not smoothness.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This kinematic path is demanded geometry; exceeding mu*g does not simulate tire saturation or a realizable maneuver.

Competency links: VD-MOTION-FRAMES. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P01 evidence task

At 5° steering, compare 15 and 30 m/s, then repeat at −5°. Record κ, r and a_y with units. Predict which values reverse sign and which ratios remain unchanged. At fixed nonzero steer, activate the ratio fault and explain why passing the grip budget would still be insufficient evidence of a correct steering model.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

Curvature is unchanged by speed and reverses with steering. Yaw doubles and lateral demand quadruples when speed doubles. All three signed quantities reverse under steering reversal. A sufficient explanation checks both the input conversion and the independent grip budget; it does not call the demanded faulty path a simulated skid.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

At 5° steering-wheel angle and 15 m/s, road-wheel angle is 0.00671280 rad. The resulting curvature is 0.00261203 1/m, radius about 382.845 m, yaw rate 0.0391804 rad/s and demand 0.587706 m/s². At the same angle and 30 m/s, curvature stays fixed, yaw rate doubles and demand quadruples to 2.35082 m/s². In four seconds the faster car travels farther along the same circle, so the two visible end points differ even though radius does not.

Do not infer equal acceleration from equal curvature. Curvature describes geometry; speed determines the force demand needed to follow it. Do not compare metres, rad/s and m/s² as if they were samples on one response axis.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
