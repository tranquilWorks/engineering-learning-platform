# P11 course checkpoint

## Predict and derive

Close roll moment and determine how stiffness distribution changes axle transfer without changing the total demand.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `One-equation roll solve with physical axle moments`

## Controlled comparison

- `front_roll_stiffness_n_m_rad`: 32000.0 → 10000.0. Hold the other controls at baseline; predict and explain the change before executing.
- `rear_roll_stiffness_n_m_rad`: 26000.0 → 60000.0. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Front and rear elastic moments divide according to their stiffness fractions. If front stiffness rises with rear fixed, its share increases; that does not create extra total roll moment. Convert each moment into the amount moved across that axle using its own track. Sum transferred-load times track and compare with the demanded roll moment. Keep geometric and elastic paths separate to avoid counting the same moment twice.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Static roll balance omits roll-rate damping, unsprung mass transients and post-lift-off behavior.

Competency links: VD-RIDE-SUSPENSION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P11 evidence task

At the defaults verify moment closure and the two axle load shifts. Increase only front stiffness, then only rear stiffness, and compare angle and front share. Activate omission and calculate the extra physical moment. Explain the load-shift factor of two without changing the track definition.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

Both stiffness increases lower angle, but they move front share in opposite directions. Nominal shifts sum to M/t; omission gives excess moment k_r M/k_f. A complete answer distinguishes stiffness sum, allocation and the shift/difference convention, without claiming a complete understeer model.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

At k_f = 32000 and k_r = 26000 N·m/rad, φ = 4620/58000 = 0.0796552 rad, about 4.564°. Front share is 0.551724. Front and rear load shifts are about 1665.991 and 1353.617 N. Their sum times 1.53 m equals 4620 N·m. The front share exceeds the assumed static front weight fraction 0.53, but this comparison alone is not a complete understeer prediction.

Reducing roll angle is not the same as reducing total lateral load transfer. For fixed imposed moment and equal track, the summed shift is fixed. Do not confuse the inner-to-outer shift with the full wheel-load difference.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
