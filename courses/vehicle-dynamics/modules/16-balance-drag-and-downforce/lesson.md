# Separate Aerodynamic Force, Power and Axle Allocation

Downforce adds normal load, drag requires propulsion power, and aero balance distributes the aerodynamic contribution between axles. These effects are related but have different units and implications. A correct total-downforce sum can conceal a wrong allocation; a familiar force magnitude can conceal a wrong resistance sign. Use several independent checks before interpreting a setup change.

## Physical model: empirical coefficients and declared signs

Air density is 1.225 kg/m³ and vehicle speed V is in m/s. Dynamic pressure is q = ½ρV², in Pa. This lesson uses coefficient-area products rather than separate dimensionless coefficients and a reference area:

\[
C_DA=0.65+0.0015\alpha^2,\qquad
C_LA=0.30+0.045\alpha.
\]

Both products have units of m². The empirical angle input α is the numerical wing angle in degrees, so the angle coefficients carry the corresponding m²/deg² and m²/deg units. These formulas do not define a universal aerodynamic law or a measured wing calibration. They specify the small teaching model that is actually executed.

\[
D=qC_DA,\qquad F_{\mathrm{down}}=qC_LA,\qquad
P_{\mathrm{drag}}=DV.
\]

Drag D is a positive resistance magnitude, opposing forward motion. Positive downforce acts downward. A negative drag value therefore violates this lesson’s resistance convention; do not silently reinterpret it as ordinary positive drag. Force is in N and power is in W, so the main response plots force while the primary sweep plots power on its own axis.

## Allocate aerodynamic contributions before adding weight

Nominal front aero share is s_f = 0.48 + 0.006α. Front contribution is s_f F_down and rear contribution is (1−s_f)F_down. Over the available 0–18 degree range, the nominal share remains between 0 and 1, so both contributions are downward under the declared convention.

Static vehicle weight is mg with m = 1320 kg and g = 9.81 m/s². The model places 53% on the front and 47% on the rear. Total axle normal loads are static contributions plus the corresponding aero contributions. Front and rear aero forces must sum to total downforce, and total normal loads must sum to mg + F_down.

The displayed tire capacity is μ(mg + F_down), with constant μ = 1. This is a lumped normal-load estimate. It omits tire load sensitivity and does not allocate lateral or longitudinal demand between tires. It cannot determine handling balance, understeer, cornering speed or whether the extra downforce compensates for drag on a particular track.

## Worked baseline and wing change

At 40 m/s and 8 degrees, dynamic pressure is 980 Pa. The area products are 0.746 m² for drag and 0.660 m² for downforce. Drag is 731.08 N, downforce 646.8 N and drag power demand 29243.2 W. The front share is 0.528, giving 341.5104 N front aero contribution and 305.2896 N rear contribution. Rear total normal load is approximately 6391.4136 N, after static weight is added.

At the same speed, increase wing angle to 18 degrees. Downforce becomes 1087.8 N, drag 1113.28 N and power demand 44531.2 W. Compared with the baseline, this gains 441 N of downforce and adds 15288 W of drag power demand. Those numbers describe a tradeoff; they do not identify an optimal wing setting without a defined objective and additional vehicle/track models.

## Predict and sweep

1. Hold wing angle at 8 degrees and compare speeds 20 and 40 m/s. Predict four times the drag and downforce, but eight times the drag power. Use the force response and the separate power sweep to verify those different exponents. Only the aero increment in tire capacity quadruples; the 12949.2 N static-weight contribution remains unchanged.
2. Hold speed at 40 m/s and vary wing angle from 0 to 18 degrees. The secondary sweep compares drag and downforce on a common force axis. Predict a quadratic drag-area trend, a linear downforce-area trend and an increasing front aero share. Check the selected axle contributions rather than assuming the additional downforce is split equally.

The sweep panels retain nominal behavior with the other selected input fixed. The main response follows the selected mode across speed. The same-input comparison shows drag and rear aero contribution for both modes; all its traces are forces in N, not a mixture of force and power.

## Named broken behavior and exact recovery

The fault reverses drag and assigns 120% of total downforce to the front axle. Rear aero contribution then becomes −20% of total downforce. At the default input, drag power is −29243.2 W and rear aero contribution is −129.36 N. Yet rear total normal load is still positive at approximately 5956.764 N, and the total downforce and lumped capacity sums remain unchanged.

This is why checking only aggregate capacity or force sums misses the declared fault. Inspect resistance sign, power sign and the bounded front-share convention as well. A negative aerodynamic contribution is distinct from a negative total wheel load. The fault is invalid under this model’s downward-allocation convention; the lesson does not claim that every possible real aerodynamic configuration must have downward force at both axles.

Disable the fault without changing speed or wing angle. Verify restoration of positive drag power and nominal axle contributions, then reset separately.

## Limits and limiting cases

The empirical formulas omit wind, ground effect, ride-height coupling, pitch balance, coefficient uncertainty and measured aerodynamic data. Their synthetic consistency supports the declared lesson, not vehicle qualification or full-course acceptance.

## Common mistakes

Do not connect watts and newtons on one response axis. Do not scale static weight with speed. A negative rear aero contribution is not automatic wheel lift, and a conserved total does not validate an axle allocation convention.

## Formative checks

Which checks detect the fault when aggregate capacity is unchanged? Check your reasoning: resistance/power signs and the front-share bound expose it, while total-force closure alone does not. Explain why the static rear load can keep the total reaction positive.

## Teach-back checklist

Derive the force and power exponents, account for both aero contributions and static weight, and quantify the wing tradeoff without claiming an optimum. This is synthetic teaching evidence, not measured-vehicle validation.
