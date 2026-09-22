# Test Observability in Multi-Rate Sensor Fusion

**Guiding question:** When do faster samples add a genuinely new state direction rather than repeat information the estimator already has?

An estimator can produce smooth states and small innovations even when one combination of initial state, sensor scale, and bias is not identifiable. Multi-rate fusion makes that trap easier to miss: hundreds of inertial samples look like abundant evidence, while a slow position sensor may be the only measurement that connects the inertial parameters to displacement. This laboratory builds the information matrix from the actual measurement times and asks three separate questions: Is the four-parameter state structurally observable? How poorly conditioned is the weakest direction? What normalized posterior variance remains after the batch?

The unknown parameter vector is

$$
\theta=[p_0,\;v_0,\;s_a,\;b_a]^T,
$$

where $p_0$ and $v_0$ are initial position and velocity, $s_a$ multiplies a known commanded acceleration, and $b_a$ is an additive accelerometer bias. The fast sensor measures commanded acceleration through scale and bias. The slow sensor measures position after the command and bias have been integrated twice. This is a local, deterministic identifiability experiment, not a complete navigation filter.

## Model, derivation, and conventions

For commanded acceleration $u(t)$, the fast measurement is

$$a_m(t)=s_a u(t)+b_a+v_a(t).$$

Its sensitivity row is $h_a=[0,0,u(t),1]$. Starting with $p_0$ and $v_0$, the slow position measurement is

$$p_m(t)=p_0+v_0t+s_a\int_0^t\int_0^\tau u(\lambda)d\lambda d\tau+\tfrac12b_at^2+v_p(t),$$

so $h_p=[1,t,I_u(t),t^2/2]$. The implementation uses a two-tone command whose double integral is evaluated analytically. Each row is whitened by its sensor standard deviation: $0.04\ \mathrm{m/s^2}$ for acceleration and $0.08\ \mathrm{m}$ for position. Stacking whitened rows $H$ gives the Fisher information matrix

$$W=H^TH=\sum_k h_k^TR_k^{-1}h_k.$$

The matrix rank counts independently constrained directions. Its condition number $\kappa(W)=\sigma_{\max}/\sigma_{\min}$ compares the strongest and weakest directions. The normalized variance metric is $\operatorname{tr}(W^{-1})$ only when all four directions are present. If rank is lost, the laboratory reports an explicit large sentinel rather than pretending a pseudoinverse is finite evidence.

Time is seconds, position is metres, velocity is metres per second, acceleration is metres per second squared, and the reported information metrics are normalized by the declared measurement noise. Rows are ordered by their real timestamps. A fast sample is not silently snapped onto the next slow measurement.

## Predict before running

Before running, predict rank, condition number, and variance separately. The nominal two-tone command should expose accelerometer scale because $u(t)$ changes sign and magnitude. Position fixes connect the integrated command to displacement and separate the initial-condition columns. Therefore the baseline should reach rank four.

Increasing the fast/slow rate ratio adds acceleration rows. It should generally reduce posterior variance, but it need not improve the condition number: repeated fast rows can strengthen the already dominant bias direction faster than the weak scale or initial-condition direction. Increasing excitation should strengthen the scale column, but again the condition number is a ratio and can move differently from total variance. This distinction is the point of the experiment. “More data” is not synonymous with “better-balanced information.”

## Baseline workflow

Run the default ratio of 10 and excitation of 0.6. The response plot shows cumulative observable rank as measurements arrive. Early acceleration rows span only scale and bias; slow position rows add initial position and velocity information. Do not expect rank to be four at the first timestamp.

Then inspect the weakest singular value. A nonzero value is necessary but not sufficient. Record the final rank, condition number, and normalized variance. Verify that the rank is an integer count and that the other two quantities are dimensionless only because the state sensitivities were whitened and normalized. Finally, identify which physical parameter combination corresponds to the weak direction by asking which columns would become similar if the command amplitude were reduced.

## Two one-variable sweeps

First hold excitation at 0.6 and move the rate ratio from 1 through 10 to 40. The number of fast inertial rows grows while the seven slow position fixes remain unchanged. Compare the variance reduction with the condition-number change. If variance falls while conditioning worsens, explain why that is not a contradiction: the information ellipsoid shrank overall but became more elongated.

Second restore the rate ratio to 10 and sweep excitation from 0.02 through 0.6 to 2.0. Near zero excitation, the scale sensitivity column approaches zero even though the bias column remains populated by every inertial sample. Stronger excitation should improve the scale estimate. Record the smallest information mode rather than relying on final rank alone, because a numerically tiny singular value can pass an arbitrary rank threshold while remaining unusable in practice.

## Intentionally broken case

Broken mode represents a robot held stationary while an estimator claims it can calibrate accelerometer scale from repeated samples. The implementation sets the commanded excitation to zero but retains the same timing structure. Then every fast row becomes $[0,0,0,1]$: it says something about bias and nothing about scale. Slow position rows contain initial position, initial velocity, and bias curvature, but their scale column is also zero. The fourth parameter direction is structurally absent.

The expected symptom is rank three, an effectively infinite condition number, and unbounded scale variance. A large sample count does not rescue the missing column. This falsifies the common practice of declaring observability because a covariance implementation happened to remain numerically positive definite after regularization.

## Recovery

Recovery restores the baseline command, not merely a different tuning that produces a smaller number. Confirm that excitation is present in both the fast acceleration sensitivity and the double-integrated slow position sensitivity. Preserve asynchronous timestamps, rebuild the matrix, and verify exact return of the baseline signature.

In a real system, recovery would also require confirming actuator execution, sensor time alignment, and the assumed noise model. This software exercise proves only that the displayed linearized batch has the intended information structure. It does not prove that a physical trajectory supplied the modeled excitation.

## Alternative and limiting cases

At exactly zero excitation, the scale column is zero and rank cannot reach four. Increasing rate alone duplicates the bias direction. At very large excitation, scale information becomes strong, but the condition number can still be dominated by position/velocity scaling or by the $t^2/2$ bias term. Column normalization can improve numerical solution without creating physical information; it must not be confused with a sensor or maneuver improvement.

A nonlinear estimator would use an empirical observability Gramian or repeated Jacobians along the estimated trajectory. The local matrix here is the small, inspectable analogue. It intentionally avoids claiming global observability or convergence from arbitrary initial conditions.

## Independent evidence and MATLAB-style design boundary

The five reviewed scenarios retain expected signatures separately from production execution. The reference path imports no production experiment, consumes no production result, and perturbs no production output. It evaluates the reviewed sensitivity relations for the exact inputs, while the learner-facing experiment constructs its own rows, plots, and diagnostics.

The design follows a MATLAB-style model/experiment/evidence separation, but no licensed MATLAB runtime was executed. Agreement establishes deterministic Python behavior for these equations, schedules, and noise assumptions only. It does not establish equivalence to an Extended Kalman Filter implementation, real timestamp jitter, colored sensor noise, hardware calibration, or field observability.

## Engineering review checklist

- List every estimated state and the measurement row that can expose it.
- Check timestamp ordering and the units used to whiten each row.
- Compare rank, smallest singular value, condition number, and covariance; never substitute one for all four.
- Verify that added samples change an information direction rather than only its multiplicity.
- Reproduce the zero-excitation rank loss without numerical regularization hiding it.
- Confirm recovery returns the original parameter set and signature.

## Common mistakes

- Declaring a state observable because the filter covariance is finite.
- Counting measurements instead of inspecting independent sensitivity directions.
- Using synchronized copies of one measurement as if they were independent sensors.
- Treating a smaller trace as proof of a better-conditioned problem.
- Normalizing columns and then claiming the physical maneuver improved.
- Ignoring sensor timing, which changes the state transition and therefore the sensitivity row.

## Focused check and teach-back

From the equations, explain why a stationary run cannot identify accelerometer scale. Point to the zero column in both measurement families. Then explain why a higher fast rate can lower total variance while worsening the condition number. Finally, state the evidence boundary: this module verifies a deterministic local information calculation for a four-parameter one-dimensional model; it does not run MATLAB, a browser accessibility study, a learner study, or physical HIL.
