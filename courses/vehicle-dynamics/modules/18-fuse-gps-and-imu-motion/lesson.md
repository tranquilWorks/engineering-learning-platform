# Fuse GPS and IMU Motion

> **Guiding question:** How does a complementary correction bound inertial drift without hiding sensor bias or timestamp skew?

## Physical model, timestamps, and units

The synthetic vehicle starts at rest and moves in one dimension with constant truth acceleration `a = 0.4 m/s²` for 10 seconds. Samples arrive every `dt = 0.5 s`. The IMU reports `a + b`, where `b` is the selected bias. GPS position is truth plus a deterministic sinusoidal error; no random generator is used.

At each aligned timestamp the predictor computes `p- = p + v dt + 0.5(a+b)dt²` and `v = v + (a+b)dt`. The corrector applies `p = p- + w(p_gps - p-)`, where `w` is the GPS correction weight. The parenthesized term is the innovation. Position is in metres, velocity in m/s, acceleration in m/s², and timestamps in seconds.

The model exposes final errors, position RMSE, mean absolute innovation, GPS residual, maximum sensor-time skew, and 21 bounded samples. It is a Python-first native design from the reviewed P18 scaffold, not source- or MATLAB-runtime equivalence.

## Predict and sweep one variable at a time

1. Hold bias at 0.05 m/s² and sweep GPS weight through 0, 0.25, and 1. Predict how uncorrected inertial drift and direct GPS tracking differ.
2. Restore weight 0.25 and sweep bias from -0.30 through 0.05 to +0.30 m/s². Predict the sign of terminal velocity error and the change in position RMSE.

Weight is not a universal quality knob. It expresses a trade between drift and GPS disturbance only after timestamps and units agree.

## Named broken behavior and exact recovery

**Broken behavior:** associate each prediction with GPS from one second earlier. The model reports a 1.0 s skew and marks the fusion invalid. Old measurements can still form smooth, finite output, which is why skew is retained as evidence.

**Exact recovery:** align measurements by source timestamp before forming innovations. Restore weight 0.25 and bias 0.05 m/s²; maximum skew returns to zero and the exact baseline signature is recovered.

## Limits and limiting cases

At weight zero, position is pure IMU propagation. At weight one, position is reset to each GPS fix, but velocity bias remains because this teaching corrector does not estimate bias. The model omits three-dimensional attitude, gravity removal, covariance propagation, asynchronous interpolation beyond the named fault, outlier rejection, and Kalman tuning.

## Common mistakes

- Fusing arrival order without checking source timestamps.
- Subtracting gravity in a frame whose attitude is undefined.
- Treating GPS position corrections as direct velocity-bias estimates.
- Comparing RMSE from different truth horizons or units.
- Hiding timestamp skew behind a visually smooth line.

## Formative checks

1. Derive the predictor units term by term.
2. Explain why bias accumulates in velocity.
3. Predict which weight endpoint follows the GPS disturbance most closely.
4. Diagnose the skew using innovation and maximum-time-skew fields.

## Teach-back checklist

- [ ] I can explain predictor, innovation, and correction.
- [ ] I predicted both sweeps before running.
- [ ] I can diagnose the named broken behavior and exact recovery.
- [ ] I can distinguish alignment validity from visual smoothness.
- [ ] I can state what the bounded fusion does not estimate.

This is not measured-vehicle, browser/learner validation, firmware, radio, bench, track, hardware/HIL, certification, release, or production evidence.
