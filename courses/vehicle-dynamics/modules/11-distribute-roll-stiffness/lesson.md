# Close the Roll-Moment and Axle-Transfer Balance

How do total roll stiffness and its front/rear distribution affect different outputs?

## Physical model

Use lateral acceleration a_y = 7 m/s², mass m = 1320 kg and effective roll arm h = 0.5 m. The imposed roll moment is M = m a_y h = 4620 N·m. For front and rear roll stiffnesses k_f and k_r in N·m/rad, equilibrium is (k_f + k_r)φ = M.

Physical axle moments are M_f = k_f φ and M_r = k_r φ. With track t = 1.53 m at both axles, the load shifted from the inner wheel to the outer wheel is ΔF_f = M_f/t and ΔF_r = M_r/t. The resulting outer-minus-inner load difference is twice the shift. This convention avoids an otherwise common factor-of-two error.

Front moment share is k_f/(k_f + k_r). Total stiffness sets angle; relative stiffness allocates moment. The response plots moment in N·m versus roll angle in degrees, showing the stiffness used by the solver, the physical total stiffness and the imposed moment. The nominal lines coincide because the solver includes both axles.

\[
\phi=\frac{M}{k_f+k_r},\qquad \Delta F_f=\frac{k_f\phi}{t},\quad \Delta F_r=\frac{k_r\phi}{t}.
\]

## Worked baseline

At k_f = 32000 and k_r = 26000 N·m/rad, φ = 4620/58000 = 0.0796552 rad, about 4.564°. Front share is 0.551724. Front and rear load shifts are about 1665.991 and 1353.617 N. Their sum times 1.53 m equals 4620 N·m. The front share exceeds the assumed static front weight fraction 0.53, but this comparison alone is not a complete understeer prediction.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Hold rear stiffness at 26000 N·m/rad and increase front stiffness from 10000 to 60000. Predict smaller roll angle and larger front moment share. The primary sweep shows angle in radians.
2. Hold front stiffness at 32000 and increase rear stiffness over its range. Predict smaller roll angle but smaller front share. The secondary sweep displays that dimensionless share. Explain why two changes that both reduce roll can redistribute axle load in opposite directions.

## Named broken behavior

The toggle omits rear stiffness from the angle solve, using φ = M/k_f. It still evaluates both physical axle moments at that angle. Their sum then exceeds the imposed moment by k_r M/k_f. At defaults the faulty angle is 0.144375 rad and the moment residual is 3753.75 N·m. Positive permitted front stiffness makes this fault nonsingular, so a large residual cannot be dismissed as a numerical division-by-zero artifact.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

This quasi-static roll balance uses a fixed effective arm and equal tracks. It omits geometric/unsprung transfer, nonlinear suspension, roll transients, tire load sensitivity and wheel-lift constraints. The original model includes a share-minus-static-front-fraction diagnostic; that is a distribution comparison, not a measured handling verdict. Declared stiffnesses remain positive. A hypothetical zero total stiffness would have no finite static solution under nonzero moment and must not be assigned zero angle.

## Common mistakes

Reducing roll angle is not the same as reducing total lateral load transfer. For fixed imposed moment and equal track, the summed shift is fixed. Do not confuse the inner-to-outer shift with the full wheel-load difference.

## Formative checks

At the defaults verify moment closure and the two axle load shifts. Increase only front stiffness, then only rear stiffness, and compare angle and front share. Activate omission and calculate the extra physical moment. Explain the load-shift factor of two without changing the track definition.

Check your reasoning: Both stiffness increases lower angle, but they move front share in opposite directions. Nominal shifts sum to M/t; omission gives excess moment k_r M/k_f. A complete answer distinguishes stiffness sum, allocation and the shift/difference convention, without claiming a complete understeer model.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
