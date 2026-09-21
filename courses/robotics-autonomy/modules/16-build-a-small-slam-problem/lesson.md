# Build a Small SLAM Problem

**Guiding question:** What inputs, observable effects, and failure modes matter when you build a Small SLAM Problem?

## Concept and prediction

Simultaneous localization and mapping estimates robot poses and landmarks from a graph of uncertain constraints. Relative measurements determine geometry, but they do not select an absolute coordinate origin. That unobservable freedom is a gauge.

Predict whether removing the pose prior produces a large factor residual. Then predict what happens to matrix rank and absolute pose error.

## Model, symbols, and equations

- $$x_i-x_{i-1}=u_i+n_i$$ — odometry factor between consecutive poses.
- $$\ell-x_i=z_i+v_i$$ — landmark-range factor.
- $$\mathbf x^*=\arg\min_{\mathbf x}\|A\mathbf x-\mathbf b\|_2^2$$ — whitened linear graph solution.

The toy world is one-dimensional: +x follows robot travel, poses and landmark use metres, and residual units are normalized standard deviations after each row is divided by its sensor sigma.

## Manipulation: two one-variable sweeps

1. Sweep `odometry_sigma_m` through [0.01,0.05,0.3]. Relative odometry weight should trade against landmark factors.
2. Restore baseline, then sweep `range_sigma_m` through [0.02,0.1,0.5]. Landmark coupling weakens as range uncertainty grows.

The state plot compares true and estimated poses and the landmark. The mechanism plot shows each whitened factor residual.

## Evidence and limiting cases

Production solves the rectangular least-squares system directly. The independent reference forms the normal equations and applies a pseudoinverse, providing a separate numerical path.

- With an infinite-strength correct prior, the first pose is effectively fixed at zero.
- Without any absolute constraint, translating every pose and landmark equally leaves all relative factors unchanged.
- Low residual does not imply observability or a correct global frame.

This is a small deterministic software SLAM problem, not physical mapping, loop-closure field evidence, or robot/HIL validation.

## Intentionally broken assumption

**Missing gauge prior.** Broken mode removes the absolute pose constraint. The solver returns one minimum-norm representative of infinitely many translated maps and loses one matrix rank.

## Explanation and recovery

Restore the gauge prior, solve the weighted system, and inspect both residual and singular values/rank. In nonlinear SLAM the same principle applies even when the gauge spans translation and rotation.

## Common mistakes

- Declaring success from low residual while ignoring rank deficiency.
- Weighting a factor by variance instead of inverse standard deviation.
- Treating an arbitrary gauge choice as physical information.
- Comparing maps in different frames without alignment.

## Focused check and teach-back

At baseline, cite pose RMSE, landmark estimate, residual RMS, and rank. Remove the prior, explain why residual remains plausible, recover rank, and teach back the factor equations, units, gauge freedom, and recovery.
