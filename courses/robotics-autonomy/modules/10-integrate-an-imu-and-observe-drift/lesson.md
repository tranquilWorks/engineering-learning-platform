# Integrate an IMU and Observe Drift

**Guiding question:** What inputs, observable effects, and failure modes matter when you integrate an IMU and Observe Drift?

## Concept and prediction

Integration turns small constant inertial-sensor biases into growing state errors. Sampling faster does not remove deterministic bias; calibration or estimation must address it.

Before running the model, predict this: Constant gyro bias creates angle error proportional to time; constant acceleration bias creates velocity error proportional to time and position error proportional to time squared. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$\delta\theta(t)=b_g t$$ — Constant gyro bias integrates once into orientation error.
- $$\delta v(t)=b_a t$$ — Constant accelerometer bias integrates once into velocity error.
- $$\delta p(t)=\tfrac{1}{2}b_a t^2$$ — The same acceleration bias integrates twice into quadratic position error.

Symbols and units:

- $b_g$ — gyro bias (deg/s at the control, rad/s internally).
- $b_a$ — acceleration bias (m/s^2).
- $\delta\theta$ — orientation error (rad or displayed deg).
- $\delta v,\delta p$ — velocity (m/s) and position error (m).

The simulated platform is otherwise stationary. Positive sensor bias integrates into positive state error. The gyro control is explicitly converted from degrees/s to radians/s.

## Manipulation: two one-variable sweeps

1. Sweep `gyro_bias_deg_s` through [0,0.2,1] while holding the other controls at baseline. Confirm final angle drift is linear in gyro bias and time.
2. Restore baseline, then sweep `accel_bias_m_s2` through [0,0.03,0.1]. Confirm velocity is linear and position is quadratic in time.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent closed-form constant-bias integration; the actual vectors come from this Python experiment.

- With both biases zero, every integrated state remains zero.
- Doubling duration doubles angle and velocity drift but quadruples position drift.
- Increasing sample rate refines the displayed trace but does not change the ideal final bias drift.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Degree/radian unit mismatch.** The broken integrator treats a degree-per-second number as radians per second, exaggerating angle drift by $180/\pi$.

## Explanation and recovery

Disable the degree/radian mismatch and convert gyro bias to radians per second before integration. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Expecting a higher sample rate to remove a constant bias.
- Subtracting gravity in the wrong frame and then integrating the leakage as translation.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.

