# P06 course checkpoint

## Predict and derive

Translate slip angle into radians and derive the small-angle lateral-force prediction.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Logistic evaluation with opposite slip convention and degree conversion`

## Controlled comparison

- `slip_angle_deg`: 4.0 → -14.0. Hold the other controls at baseline; predict and explain the change before executing.
- `normal_load_n`: 3600.0 → 6000.0. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Four degrees is 0.0698132 rad. A stiffness stated in N/rad must multiply that number, not 4. The force sign follows the lesson's explicitly declared slip convention; it should reverse under an angle sign reversal. Compare the linear tangent with the saturation boundary as normal load changes. A factor of about 57.3 is a unit defect, not evidence for a different tire stiffness.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Symmetric synthetic tire behavior omits hysteresis, transient camber and measured parameter uncertainty.

Competency links: VD-TIRE-LAT. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P06 evidence task

Compare +4° and −4° at 3600 N and estimate the slope near zero. State α in radians, force sign and capacity. Explain why the faulty model can pass magnitude and symmetry checks while remaining wrong, and translate this lesson's α into P07's convention.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

Positive velocity-minus-wheel angle demands negative left force. Reversing angle reverses force. The slope is −78000 N/rad, or about −1361.36 N/deg. The opposite convention uses α_new = −α and a positive constitutive sign. Full reasoning includes units and convention, not merely the graph's direction.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

At +4° and 3600 N, α = 0.0698132 rad, capacity is 3780 N and the tanh argument is about 1.44059. The left-positive lateral force is about −3378.6 N. The small-angle linear estimate is −5445.43 N, which exceeds capacity in magnitude and demonstrates why the saturating curve matters. At −4° the force has equal magnitude and positive sign.

Do not apply a memorized plus or minus sign without declaring α. Do not use a degree number directly with a stiffness in N/rad. Do not transfer P07's force-positive axle angle into this equation unchanged.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
