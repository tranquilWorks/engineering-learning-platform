# Fuse Sensors with an EKF

**Guiding question:** What inputs, observable effects, and failure modes matter when you fuse Sensors with an EKF?

## Concept and prediction

An extended Kalman filter alternates a nonlinear state prediction with a locally linear covariance prediction and a measurement correction. The state equation, its Jacobian, units, and noise assumptions must describe the same system.

Predict how position error and covariance change between GPS updates, and whether frequent GPS can completely hide a degree/radian error in the motion model.

## Model, symbols, and equations

- $$\hat{\mathbf x}_{k+1}^-=f(\hat{\mathbf x}_k,u_k),\quad P_{k+1}^-=F_kP_kF_k^T+Q$$ — nonlinear prediction and covariance propagation.
- $$K=P^-H^T(HP^-H^T+R)^{-1}$$ — innovation weighting.
- $$\hat{\mathbf x}^+=\hat{\mathbf x}^-+K(\mathbf z-h(\hat{\mathbf x}^-))$$ — measurement update.
- $$P^+=(I-KH)P^-(I-KH)^T+KRK^T$$ — Joseph covariance update.

The state is $[x,y,\theta]^T$ in a world frame with +x right, +y up, and positive yaw counterclockwise. Position is in metres; yaw is radians internally and displayed in degrees. $Q$ and $R$ are process and GPS covariance models.

## Manipulation: two one-variable sweeps

1. Sweep `gps_noise_m` through [0.05,0.25,1]. Larger measurement uncertainty should reduce correction authority and leave larger position error.
2. Restore baseline, then sweep `gps_interval_s` through [0.1,0.5,2]. Longer prediction-only spans should produce a covariance sawtooth with higher peaks.

The path plot shows truth, estimate, and GPS observations. The mechanism plot compares actual position error with the filter's position uncertainty scale.

## Evidence and limiting cases

The independent oracle evaluates the same stated process with a separately formulated finite-difference Jacobian. Production uses the analytic Jacobian and a linear solve for the gain.

- With zero initial error and noiseless consistent sensors, state error remains near numerical precision.
- As GPS interval grows, the filter approaches dead reckoning between updates.
- Setting process noise unrealistically low can make the filter overconfident even when the trajectory still looks plausible.

This is deterministic software estimation evidence, not physical GPS/IMU, robot, HIL, bench, field, or production validation.

## Intentionally broken assumption

**Radian state used as degrees.** Broken mode multiplies the radian heading by $\pi/180$ before evaluating the motion. Both prediction and analytic Jacobian are then consistently wrong about the real plant.

## Explanation and recovery

Disable the unit corruption, keep the state in radians, and differentiate the exact motion function used for prediction. Confirm that error drops and covariance contractions align with measurement times.

## Common mistakes

- Linearizing a different equation than the one used to propagate state.
- Mixing standard deviation with variance in $Q$ or $R$.
- Updating covariance with $(I-KH)P$ and ignoring numerical symmetry/positivity.
- Treating small residuals from frequent GPS as proof that the process model is correct.

## Focused check and teach-back

At baseline, identify one prediction interval and one correction, cite RMS error and covariance trace, reproduce the unit failure, and recover it. Teach back the frame, nonlinear function, Jacobian role, innovation, and why covariance is an engineering claim rather than decoration.
