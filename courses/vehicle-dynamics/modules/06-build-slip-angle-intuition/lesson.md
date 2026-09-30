# Relate Slip-Angle Convention to Lateral Force

Which direction should lateral tire force point under the stated slip-angle convention?

## Physical model

This lesson defines slip angle α as **velocity direction minus wheel direction**. Positive α means the contact motion points left of the wheel plane. With left force positive, a restoring tire force therefore has the opposite sign:

α = (π/180) slip_angle_deg; F_y = −μF_z tanh(C_α α/(μF_z)).

Use C_α = 78000 N/rad and μ = 1.05. Near zero, F_y ≈ −C_α α; at large signed angles, force approaches the opposite signed capacity. The response has slip angle in degrees on x and lateral force in N on y. The slope expressed per degree is −78000π/180 ≈ −1361.36 N/deg, different numerically from the slope per radian.

P07 uses the opposite, force-positive axle-slip convention. This does not change physics: changing the definition of α must also change the sign in the tire law. State the convention before comparing equations across lessons.

\[
F_y=-\mu F_z\tanh\!\left(\frac{C_\alpha\alpha}{\mu F_z}\right),\qquad \alpha=\frac{\pi}{180}\alpha_{\deg}.
\]

## Worked baseline

At +4° and 3600 N, α = 0.0698132 rad, capacity is 3780 N and the tanh argument is about 1.44059. The left-positive lateral force is about −3378.6 N. The small-angle linear estimate is −5445.43 N, which exceeds capacity in magnitude and demonstrates why the saturating curve matters. At −4° the force has equal magnitude and positive sign.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Hold load at 3600 N and vary slip angle from −14° through zero to +14°. Predict a decreasing odd curve, with horizontal capacity asymptotes. Estimate the near-zero slope using degrees and convert it to N/rad before comparing with C_α.
2. Hold α at +4° and vary load from 1000 to 6000 N. Predict an increasingly negative force magnitude that remains bounded by the load-dependent capacity. At negative α the trend has the opposite sign; at zero angle it vanishes.

## Named broken behavior

The toggle reverses the lateral-force sign while preserving angle conversion and saturation magnitude. The faulty curve rises through zero, whereas the declared restoring law falls. Both modes still obey the force-capacity inequality and odd symmetry. The discriminating sign test is F_y α ≤ 0 under this lesson's convention. Zero angle is a benign case because both forces vanish.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

The model excludes combined slip, camber thrust, tire relaxation and transient vehicle yaw. The plateau is a smooth approximation without an identified peak or thermal evolution. A restoring force direction alone does not prove complete vehicle stability. Degree conversion is essential even when an angle appears numerically small; the constitutive stiffness is specified per radian.

## Common mistakes

Do not apply a memorized plus or minus sign without declaring α. Do not use a degree number directly with a stiffness in N/rad. Do not transfer P07's force-positive axle angle into this equation unchanged.

## Formative checks

Compare +4° and −4° at 3600 N and estimate the slope near zero. State α in radians, force sign and capacity. Explain why the faulty model can pass magnitude and symmetry checks while remaining wrong, and translate this lesson's α into P07's convention.

Check your reasoning: Positive velocity-minus-wheel angle demands negative left force. Reversing angle reverses force. The slope is −78000 N/rad, or about −1361.36 N/deg. The opposite convention uses α_new = −α and a positive constitutive sign. Full reasoning includes units and convention, not merely the graph's direction.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
