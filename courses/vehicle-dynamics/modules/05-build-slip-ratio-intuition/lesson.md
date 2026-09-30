# Relate Signed Slip Ratio to Tire Force

Why does more normal load increase force capacity without changing the initial slip stiffness here?

## Physical model

Positive slip ratio κ denotes driving; negative slip denotes braking. This signed convention fixes the direction of forward force. Use C_κ = 85000 N per unit slip and μ = 1.05:

F_x = μF_z tanh(C_κ κ / (μF_z)).

The argument of tanh is dimensionless. Near zero, tanh(z) ≈ z, so F_x ≈ C_κ κ. At large positive or negative slip the force approaches ±μF_z. Thus the small-slip slope remains C_κ while the asymptotic capacity scales with load. The response plots forward tire force in N against dimensionless slip ratio, with the signed capacity interpreted from the separate capacity metric.

This memoryless curve relates a supplied slip value to force. It does not derive slip from wheel speed or integrate wheel rotation. A positive product F_x κ is consistent with the declared driving convention; this product is a sign diagnostic, not energy or power.

\[
F_x=\mu F_z\tanh\!\left(\frac{C_\kappa\kappa}{\mu F_z}\right).
\]

## Worked baseline

At κ = 0.08 and F_z = 3600 N, capacity is 3780 N and the dimensionless argument is 6800/3780 ≈ 1.79894. The force is about 3578.5 N, below capacity. The linear prediction 85000 × 0.08 = 6800 N would greatly exceed the bound. Near κ = 0.001, the force is approximately 85 N, because this point lies in the nearly linear part of the curve.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Hold load at 3600 N and sweep slip from −0.3 through zero to +0.3. Predict an odd saturating curve, with negative braking force and positive driving force. Compare opposite slips and estimate the slope near zero using a small symmetric difference.
2. Restore κ = 0.08 and vary load from 1000 to 6000 N. Predict increasing positive force with increasing capacity, but not a force proportional to load everywhere. Raising load also reduces the tanh argument. At zero slip, changing load leaves force exactly zero.

## Named broken behavior

The fault reverses the computed longitudinal-force sign. It preserves the capacity bound and odd symmetry, so those checks alone cannot detect the wrong convention. For nonzero slip, F_x κ becomes negative and the nominal and faulty curves reflect vertically. At zero slip both outputs are zero; this is a benign excitation rather than proof of correctness. Recovery restores the sign law without changing load or slip.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

This smooth saturating law is an instructional constitutive model, not an identified tire dataset. It excludes relaxation length, temperature, road-water effects, load sensitivity of μ and combined lateral force. It contains no post-peak falloff, so the plateau cannot be used to identify a realistic optimum slip. The permitted positive loads avoid the singular unloaded-tire expression.

## Common mistakes

A bounded force can still point the wrong way. A force plateau does not mean the initial stiffness has changed, and larger load does not produce a simple proportional scaling at every slip.

## Formative checks

At 3600 N, compare ±0.001 and ±0.08 slip. Check signs, odd symmetry, initial slope and force capacity. Activate the sign fault and state which checks it still passes. Then explain the zero-slip result while changing load.

Check your reasoning: The initial slope is approximately 85000 N per unit slip, whereas the larger-slip points bend toward ±3780 N. The sign-reversed curve remains odd and bounded but violates the declared force/slip sign. Zero slip gives zero force at every allowed load, so a nonzero test is essential.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
