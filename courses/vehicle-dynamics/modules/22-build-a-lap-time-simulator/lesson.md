# Build a Lap-Time Simulator

> **Guiding question:** Why must future braking constraints propagate backward before segment times are credible?

## Physical model, passes, and units

The deterministic course has 13 speed nodes and 12 segments of 25 m. Each node has a known curvature `kappa`. Straight nodes are capped at 50 m/s; curved nodes use `v_grip = sqrt(mu g / |kappa|)`. A forward pass enforces `v_i² <= v_(i-1)² + 2 a_accel ds` and the local grip cap.

That is not enough. Starting from the declared terminal speed, a backward pass enforces `v_i² <= v_(i+1)² + 2 a_brake ds` with `a_brake = 6 m/s²`. Segment time uses the average-speed trapezoid `dt = 2 ds/(v_i + v_(i+1))`. Summing 12 finite segment times gives the lap-time proxy. The retained braking residual is the maximum violation of the squared-speed inequality.

This Python-first native P22 model is derived from a scaffold, not source- or MATLAB-runtime equivalence. Its fixed curvature list is an instructional track, not a surveyed venue.

## Predict and sweep one variable at a time

1. Hold acceleration at 3.5 m/s² and sweep friction from 0.70 through 1.05 to 1.40. Predict which curved nodes bind and how time changes.
2. Restore friction 1.05 and sweep acceleration from 1 through 3.5 to 6 m/s². Predict where the forward pass changes and where grip or braking makes extra acceleration irrelevant.

Inspect the whole speed profile: a single lap-time number cannot show which constraint is active.

## Named broken behavior and exact recovery

**Broken behavior:** omit the backward pass. Every node can satisfy its local grip cap and forward reachability while arriving too fast to brake for a later corner. The positive squared-speed braking residual makes this explicit.

**Exact recovery:** set the terminal condition, sweep backward with the 6 m/s² limit, then integrate segment time. Restore `mu=1.05` and `a=3.5 m/s²` for zero violation and the exact baseline.

## Limits and limiting cases

Low friction reduces curved-node limits. Low acceleration can dominate straights. A very high acceleration limit cannot beat downstream grip and braking caps. The model omits power versus speed, gear shifts, combined tire force, aero, grade, closed-loop periodic convergence, temperature, traffic, and driver variability.

## Common mistakes

- Applying only forward reachability.
- Braking after the slow-corner node instead of before it.
- Integrating `ds/v_i` without handling endpoint speeds consistently.
- Using signed curvature inside the square root without magnitude.
- Calling a fixed-segment proxy a validated lap prediction.

## Formative checks

1. Derive both squared-speed reachability inequalities.
2. Locate one grip-limited and one braking-limited node.
3. Explain why the backward pass starts from the future.
4. Verify that every denominator in the time integration is positive.

## Teach-back checklist

- [ ] I can explain local grip, forward acceleration, and backward braking.
- [ ] I predicted both sweeps.
- [ ] I can interpret the braking residual.
- [ ] I diagnosed the named broken behavior and exact recovery.
- [ ] I can state the simulator’s evidence boundary.

This is not measured-vehicle, surveyed-track, driver, browser/learner, hardware/HIL, certification, release, or production evidence.
