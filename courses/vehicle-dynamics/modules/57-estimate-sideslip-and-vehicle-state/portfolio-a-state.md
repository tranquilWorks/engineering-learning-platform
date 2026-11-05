# A-STATE integration evidence

Integrate these existing lessons: P01, P02, P03, P18, P19, P25, P55, P56, P57.

Required evidence: Reconstruct a driven trajectory and state with calibration, frame, timing, and independent kinematic residual checks.

## Derive and predict

Use P01: Derive curvature from steering-wheel angle and predict separately what doubles when speed doubles. Wheel angle is steering-wheel angle divided by 13, then converted to radians. Curvature is tan(delta)/L. At fixed steering, radius is unchanged, yaw rate v*kappa doubles and lateral demand v²*kappa quadruples when speed doubles. A zero-steer limit must approach a straight path continuously. Bypassing the ratio can preserve a smooth trajectory while violating the declared input convention; inspect curvature and grip demand, not smoothness. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P18: Explain exactly which state a GPS position correction changes and which IMU error continues to accumulate. At a 0.5 s sample interval, an acceleration bias of 0.05 m/s² adds 0.025 m/s of velocity error each prediction step. The complementary correction pulls position toward GPS, but does not directly repair the integrated velocity bias. Raising GPS weight can reduce position drift while increasing sensitivity to GPS error or delay. Diagnose a delayed observation by its timestamp and residual, not just the final position. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P55: Invert sensor bias and scale before rotating to body axes, and explain why norm closure alone is insufficient. The forward sensor model scales R(-angle)*truth and then adds sensor bias. Inversion must subtract bias and divide channelwise by scale before applying R(angle). With the declared truth, corrected body acceleration returns (1.20,4.50) m/s² and corrected yaw returns 12 deg/s. A wrong rotation angle still preserves norm, so compare direction and truth residual too. Mixed acceleration and yaw errors use declared 1 m/s² and 1 deg/s scales. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P57: Derive fixed-gain covariance propagation and distinguish a conditional uncertainty calculation from empirical error. In normalized coordinates [beta/(1 rad),r/(1 rad/s),bias/(1 rad)], prediction is Pminus=F*P*F transpose+Q. For fixed gain L and direct measurements, posterior is (I-L)*Pminus*(I-L) transpose+L*R*L transpose. Both plant propagation and measurement noise are necessary; shrinking P only by I-L is not a covariance update. Increasing noise must increase the conditional posterior even if the chosen gain is unchanged. Compare state histories and actual truth error separately. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Create a timestamped state-reconstruction report with calibration order, angle units, frame transforms, prediction timing and correction weights. Compute one decoded speed by hand, one rotated acceleration vector and one constant-turn endpoint. Compare known-offset alignment with the affine synchronization fit used in P66. Separate position-only complementary correction from the fixed-gain three-state observer. For the latter show normalized state scales, the Joseph covariance calculation and actual truth errors; explain why conditional covariance under independent noise does not validate the correlated fixture. Retain a delayed/sign-fault trajectory and exact recovery.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
