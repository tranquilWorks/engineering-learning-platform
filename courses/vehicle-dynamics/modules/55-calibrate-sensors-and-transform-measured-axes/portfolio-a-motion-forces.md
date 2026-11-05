# A-MOTION-FORCES integration evidence

Integrate these existing lessons: P01, P02, P03, P04, P25, P38, P48, P55.

Required evidence: Close independent frame, unit, load-transfer, and force/moment balance checks including saturation and zero-input limits.

## Derive and predict

Use P01: Derive curvature from steering-wheel angle and predict separately what doubles when speed doubles. Wheel angle is steering-wheel angle divided by 13, then converted to radians. Curvature is tan(delta)/L. At fixed steering, radius is unchanged, yaw rate v*kappa doubles and lateral demand v²*kappa quadruples when speed doubles. A zero-steer limit must approach a straight path continuously. Bypassing the ratio can preserve a smooth trajectory while violating the declared input convention; inspect curvature and grip demand, not smoothness. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P03: Derive axle loads from vertical force and pitch moment equilibrium; explain which axle gains load under acceleration. The amount transferred is T=m*a*h/L, with front decreasing and rear increasing for forward acceleration. Hence front+rear=mg and the moment produced by the moved load is T*L=m*a*h. Doubling height doubles T without changing total weight. A transfer quantity is not the difference between the two axle loads, which also contains static weight distribution. Audit both equations before accepting a plausible percentage. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P38: Derive wheel loads from the transferred amount and detect when a four-contact equilibrium becomes impossible. If T is the load moved, inner load is W/2-T and outer load W/2+T; their difference is 2T. Multiplying that difference by half-track gives T*track, the roll moment. Using +/-T/2 halves the moment and underestimates the load-sensitive capacity loss. First subtract geometric moment from total before distributing the elastic remainder. A negative requested inner load marks lift-off: the displayed capped capacity is only a bound and cannot close the original four-contact equilibrium. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P55: Invert sensor bias and scale before rotating to body axes, and explain why norm closure alone is insufficient. The forward sensor model scales R(-angle)*truth and then adds sensor bias. Inversion must subtract bias and divide channelwise by scale before applying R(angle). With the declared truth, corrected body acceleration returns (1.20,4.50) m/s² and corrected yaw returns 12 deg/s. A wrong rotation angle still preserves norm, so compare direction and truth residual too. Mixed acceleration and yaw errors use declared 1 m/s² and 1 deg/s scales. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Build one signed interface ledger from steering-wheel degrees to road-wheel radians, curvature, yaw, lateral demand and tire-force feasibility. Add longitudinal force and axle-load balances at the same declared mass and geometry; do not silently combine constants from different lessons. Include a zero-steer limit, a sign reversal and a doubled-speed case. Show why an orthogonal but wrong frame transform can pass norm preservation while failing directional truth. Report each interface's value and units, and identify one model boundary that prevents the demanded path from being called physically realized.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
