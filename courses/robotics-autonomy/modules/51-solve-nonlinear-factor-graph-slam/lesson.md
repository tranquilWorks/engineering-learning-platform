# Solve Nonlinear Factor-Graph SLAM

**Guiding question:** What must be fixed, relinearized, and audited before a low factor residual can support a SLAM claim?

A pose graph is not just a large least-squares matrix. Every factor states a relationship in a frame, every covariance determines its leverage, nonlinear factors are valid only near their current linearization point, and relative constraints leave a global gauge unconstrained. An optimizer can drive its residual down while the entire map remains translated or rotated away from the declared world frame. This laboratory makes those mechanisms visible in a small two-dimensional graph.

The synthetic robot follows a closed elliptical path. Consecutive poses are connected by noisy two-dimensional odometry. The final pose is connected back to the first by a loop vector whose declared noise is adjustable. Selected poses also observe ranges to two fixed landmarks, creating genuinely nonlinear factors. A prior on the first pose fixes the translation gauge. The solver performs Gauss-Newton relinearization, and the plots show both the optimized geometry and the residual history.

## Model, derivation, and conventions

Let $X=[x_0^T,\ldots,x_{N-1}^T]^T$ with each $x_i=[e_i,n_i]^T$ in metres. For factor $i$ with measurement $z_i$, prediction $h_i(X)$, and square-root information $\Omega_i^{1/2}$, define

$$r_i(X)=\Omega_i^{1/2}(h_i(X)-z_i).$$

The maximum-likelihood estimate under independent Gaussian factors is

$$X^*=\arg\min_X\sum_i r_i(X)^Tr_i(X).$$

Odometry factors use $h_{i,i+1}=x_{i+1}-x_i$. Their Jacobian has $-I$ in the first pose columns and $I$ in the second. The loop factor has the same structure between the final and initial poses. A range factor to landmark $\ell$ uses

$$h_{i\ell}(X)=\|x_i-\ell\|_2,$$

with Jacobian $(x_i-\ell)^T/\|x_i-\ell\|$. Because that direction depends on the current estimate, it must be recomputed after every update.

At a current estimate $X_k$, stack residual $r$ and Jacobian $J$. Gauss-Newton solves

$$J^TJ\,\delta=-J^Tr,\qquad X_{k+1}=X_k+\delta.$$

The implementation uses a least-squares solve on $J\delta=-r$ rather than explicitly inverting $J^TJ$, but reports the normal-matrix condition number as a diagnostic. East and north coordinates are metres. Whitened residual RMS and condition number are dimensionless. The first-pose residual is reported in metres so gauge error remains physically interpretable.

## Predict before running

With the first pose prior and landmark ranges enabled, the graph should be anchored near the declared world path. Repeated linearization should reduce residual and trajectory error. A noisier loop measurement has two competing effects: its observed closure is more biased, but its declared covariance also gives it less weight. Predict which effect dominates in this particular deterministic case, then verify rather than assuming “more noise always means more error.”

Increasing pose count adds variables, odometry edges, and range factors. The geometry is similar, but the normal system becomes larger and can become more poorly conditioned. Predict that the condition number may grow even when the plotted trajectory still looks smooth.

## Baseline workflow

Run 30 poses with loop noise 0.08 m. Start with the geometry plot. The estimated curve should follow the ellipse and close near its start. A visually closed loop is not sufficient, so record trajectory RMSE and first-pose gauge residual.

Next inspect the residual history. The first point is the residual at the perturbed initial trajectory. Each subsequent point follows a complete relinearization and update. Convergence means both residual and increment have settled; a single descending step is not proof. Finally inspect the normal-matrix condition. It should be finite when the prior and landmark factors are present.

Trace one factor manually. For an odometry measurement from pose $i$ to $i+1$, subtract the two estimated positions, subtract the stored displacement, and divide by 0.05 m. For a range factor, recompute the direction from the current pose to the landmark before writing its Jacobian. This distinction separates linear graph assembly from nonlinear optimization.

## Two one-variable sweeps

Sweep loop noise from 0.005 through 0.08 to 0.5 m while holding 30 poses. The measurement bias grows with the slider, but the factor's standard deviation also grows, so the loop contributes less information. Observe trajectory RMSE, gauge error, and condition number together. If RMSE falls at the high-noise endpoint, explain that the optimizer has downweighted a biased closure; do not misstate the result as noise improving the sensor.

Then restore loop noise to 0.08 m and sweep pose count from 5 through 30 to 100. More poses describe the curve at higher resolution but expand the state dimension. Compare the geometric error with matrix conditioning and runtime sample count. A denser graph is not automatically better constrained per degree of freedom.

## Intentionally broken case

Broken mode removes the absolute prior and nonlinear landmark factors, offsets every initial pose by $[0.40,-0.30]$ m, and performs one solve using only relative odometry and loop edges. Those factors are invariant to a common translation:

$$h(x_i+c,x_j+c)=h(x_i,x_j).$$

Therefore the graph cannot determine $c$. The normal matrix loses two translation directions. Least squares can still return a minimum-norm increment, and relative residual can still be small, but the map remains displaced from the declared world frame. The expected evidence is large trajectory RMSE, nonzero gauge-origin residual, and a singular condition sentinel.

This failure matters because many optimizers add damping or a tiny diagonal term that makes the matrix invertible. Numerical invertibility created by regularization does not equal a physical reference. The gauge must be fixed intentionally and documented.

## Recovery

Recovery reinstates the first-pose prior, the two fixed landmarks, and repeated relinearization. It restores the exact baseline parameter set and verifies that the baseline signature returns. Merely translating the final map by eye is not recovery: that post-processing hides the missing model constraint. Likewise, increasing damping is not a substitute for an absolute datum.

In a larger SLAM system, recovery also requires checking frame IDs, loop timestamps, covariance transport, and whether the chosen prior is a coordinate convention or a trusted physical measurement. This module fixes only translation because its states contain positions, not orientations.

## Alternative and limiting cases

With exact consistent factors and a fixed gauge, residual can approach zero. Without a prior or absolute observation, any common translation produces the same relative-factor cost. If orientations were included, a common global rotation would add another gauge direction. In three dimensions, six rigid-body gauge freedoms usually appear.

Levenberg-Marquardt adds damping to improve steps when Gauss-Newton is far from the solution. It can improve convergence but does not create missing observability. Incremental solvers exploit sparsity and update only affected portions of the graph; this dense laboratory favors transparency over scale.

## Independent evidence and MATLAB-style design boundary

The retained scenario signatures were evaluated independently for the reviewed deterministic graph inputs. The reference path neither imports the experiment nor consumes its output. Production evidence comes from the actual catalog runtime and separately records baseline, both sweeps, broken mode, and exact recovery.

No MATLAB optimization toolbox, GTSAM, Ceres, ROS graph, real bag file, or physical sensor ran. The result demonstrates a bounded NumPy factor graph with known truth. It does not prove global convergence, correct loop association, real covariance calibration, field map accuracy, or production computational performance.

## Engineering review checklist

- Declare every state coordinate and factor frame.
- Verify residual sign, Jacobian blocks, and covariance whitening.
- Count gauge freedoms before solving and fix them intentionally.
- Relinearize every nonlinear factor after the state changes.
- Inspect residual history, increment norm, condition number, and held-out geometry.
- Distinguish coordinate convention priors from physical absolute measurements.

## Common mistakes

- Calling a relative pose graph globally observable without a prior.
- Inverting $J^TJ$ directly when a least-squares or factorization solve is available.
- Linearizing range or bearing factors once and reusing stale Jacobians.
- Treating a low weighted residual as proof of map accuracy.
- Ignoring that declared covariance changes factor influence.
- Using regularization to conceal rank deficiency.

## Focused check and teach-back

Write the two nonzero Jacobian blocks for an odometry factor and the direction row for a range factor. Explain why a common translation cancels from every relative factor. Then identify which evidence distinguishes nominal convergence from the broken gauge-free solution. Close by stating the boundary: deterministic two-dimensional software optimization only, with MATLAB, learner/accessibility, physical HIL, certification, release, and production validation unperformed.
