# P12 course checkpoint

## Predict and derive

Separate camber-induced lateral force from the energy lost through toe scrub.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Independent sine/cosine toe ratio and dimensional angle conversion`

## Controlled comparison

- `camber_deg`: -2.0 → -5.0. Hold the other controls at baseline; predict and explain the change before executing.
- `toe_deg`: 0.1 → 0.5. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Camber thrust follows the signed camber angle in the linear approximation. Scrub power is dissipative and should remain nonnegative when toe reverses: the relevant force and lateral sliding velocity reverse together. Convert degrees once and retain the per-wheel versus axle convention. A sign-preserving force prediction and an even power prediction provide different tests of the same alignment change.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

These local linear alignment relations are not a setup recommendation or a model of tire wear over a stint.

Competency links: VD-RIDE-SUSPENSION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P12 evidence task

Compare camber ±2° with toe ±0.1°, then set one angle at a time to zero. Record force and power units and parity. Activate the degree/radian fault at the defaults and explain why its camber-force ratio differs from its scrub-power ratio.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

Camber force is odd in camber; toe scrub and power are even in toe. The camber error factor is exactly 180/π because that law is linear, whereas tan makes the scrub ratio nonlinear. A complete response separates the two mechanisms and declines to infer temperature or full suspension geometry from these estimates.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

At camber −2° and toe +0.1°, γ = −0.0349066 rad and τ = 0.00174533 rad. Camber thrust is about +2094.40 N, scrub force 6.28319 N and scrub power 125.664 W. Reversing toe leaves scrub and power unchanged; reversing camber reverses thrust. Zeroing only toe removes scrub power but does not remove camber thrust.

Do not infer a full camber curve through suspension travel from two static alignment inputs. Do not report watts as heat in joules or as temperature. Squaring a small angle would change this model's intended near-zero |toe| dependence.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
