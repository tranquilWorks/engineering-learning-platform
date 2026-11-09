# P03 course checkpoint

## Predict and derive

Derive axle loads from vertical force and pitch moment equilibrium; explain which axle gains load under acceleration.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Two-by-two reaction and moment balance`

## Controlled comparison

- `acceleration_mps2`: 4.0 → -9.0. Hold the other controls at baseline; predict and explain the change before executing.
- `cg_height_m`: 0.5 → 0.85. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The amount transferred is T=m*a*h/L, with front decreasing and rear increasing for forward acceleration. Hence front+rear=mg and the moment produced by the moved load is T*L=m*a*h. Doubling height doubles T without changing total weight. A transfer quantity is not the difference between the two axle loads, which also contains static weight distribution. Audit both equations before accepting a plausible percentage.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Quasi-static load transfer omits suspension pitch transients and ceases to represent two-axle contact after a negative axle load.

Competency links: VD-MOTION-FRAMES, VD-FORCE-BALANCE. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P03 evidence task

Compare +4 and −4 m/s² at h = 0.5 m. Calculate both axle loads and verify vertical and pitch balance. Activate the fault at +4 m/s². Explain why one balance passes and the other fails, then identify an input at which that fault becomes invisible.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

The transfer magnitude is 1027.23735 N, reversing with acceleration. Both nominal balances close. Omission preserves total weight but misses the nonzero pitch moment; zero acceleration hides it. Credit requires a signed transfer and a moment in N·m, rather than only a statement that the rear load should increase.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

At 4 m/s² and h = 0.5 m, total weight is 12949.2 N and transfer is 1027.23735 N. The front axle carries 5835.83865 N and the rear 7113.36135 N. Multiplying the transfer by 2.57 m gives 2640 N·m, equal to 1320 × 4 × 0.5. Under −4 m/s² braking, transfer changes sign: the front gains what the rear loses. The static values themselves do not exchange.

A car does not gain total weight during acceleration. Redistribution changes axle loading while the total remains mg. Checking only the sum can allow an incorrect distribution to pass; moment closure is essential.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
