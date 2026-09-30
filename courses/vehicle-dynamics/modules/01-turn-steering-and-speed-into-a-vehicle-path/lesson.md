# Constant-Curvature Paths and Tire-Grip Demand

Does doubling speed change the path radius, the yaw rate, or the grip demand?

## Physical model

Use a body frame with forward x, left y and positive counterclockwise yaw. The input is **steering-wheel angle**, not road-wheel angle. Convert degrees to radians, divide by the steering ratio i = 13, and use wheelbase L = 2.57 m:

δ = (π/180) steering_deg / i; κ = tan(δ)/L; r = Vκ; a_y = Vr = V²κ.

Curvature κ has units 1/m, yaw rate r has units rad/s, and lateral acceleration has units m/s². The plotted path integrates this constant yaw rate over four seconds: x(t) = sin(rt)/κ and y(t) = [1 − cos(rt)]/κ. At zero curvature the continuous limit is x = Vt, y = 0. Equal horizontal and vertical distance scales preserve the geometry of a turn. No integration of tire slip is hidden behind this curve.

A separate demand check compares |a_y| with μg = 9.81 m/s². This is a deliberately simple grip budget. Crossing it means the prescribed path cannot be justified by the assumed tire capacity; the plot remains a demanded kinematic path.

\[
\kappa=\frac{\tan\delta}{L},\qquad r=V\kappa,\qquad a_y=V^2\kappa.
\]

## Worked baseline

At 5° steering-wheel angle and 15 m/s, road-wheel angle is 0.00671280 rad. The resulting curvature is 0.00261203 1/m, radius about 382.845 m, yaw rate 0.0391804 rad/s and demand 0.587706 m/s². At the same angle and 30 m/s, curvature stays fixed, yaw rate doubles and demand quadruples to 2.35082 m/s². In four seconds the faster car travels farther along the same circle, so the two visible end points differ even though radius does not.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Hold speed at 15 m/s. Change steering-wheel angle from −20° through 0° to +20°. Predict an odd curvature curve, a straight zero-angle path and mirrored left/right turns. The primary sweep measures curvature, not lateral acceleration.
2. Restore 5° and vary speed from 1 to 45 m/s. Predict a constant turning radius and quadratic demand. At 45 m/s the nominal demand is about 5.28935 m/s². Read the secondary sweep in m/s² and compare it with the stated grip budget; a rising curve alone does not establish sliding.

## Named broken behavior

The toggle bypasses the 13:1 steering ratio, treating the steering-wheel angle as the road-wheel angle. At the default inputs curvature and yaw rise by approximately thirteenfold, with a slightly different factor because tangent is nonlinear. This is an executed input-conversion error, not an arbitrary multiplier attached to the final acceleration. The comparison shows two actual same-input paths. Even when the faulty path remains below the grip limit, it still fails the declared steering-ratio check. At exactly zero steering both models coincide, so lack of separation there does not prove the conversion correct.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

At zero steer the path is straight and radius is mathematically unbounded; the implementation uses the finite straight-line limit rather than dividing by zero. Steering reversal mirrors the turn. This model omits tire compliance, sideslip, transient steering and body roll. A failed grip check supplies no prediction of the actual sliding trajectory. Positive speeds are required by the controls; extrapolating into reverse motion is outside this lesson.

## Common mistakes

Do not infer equal acceleration from equal curvature. Curvature describes geometry; speed determines the force demand needed to follow it. Do not compare metres, rad/s and m/s² as if they were samples on one response axis.

## Formative checks

At 5° steering, compare 15 and 30 m/s, then repeat at −5°. Record κ, r and a_y with units. Predict which values reverse sign and which ratios remain unchanged. At fixed nonzero steer, activate the ratio fault and explain why passing the grip budget would still be insufficient evidence of a correct steering model.

Check your reasoning: Curvature is unchanged by speed and reverses with steering. Yaw doubles and lateral demand quadruples when speed doubles. All three signed quantities reverse under steering reversal. A sufficient explanation checks both the input conversion and the independent grip budget; it does not call the demanded faulty path a simulated skid.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
