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


## Deep derivation and conventions

The depth target for this module is to **derive EKF predict/update equations, Jacobians, and covariance form**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: The world frame uses +x right, +y up, and positive counterclockwise yaw; the state stores yaw in radians.

The governing relations are:

- $$x_minus=f(x,u), P_minus=F P F^T+Q$$ — The nonlinear process and its Jacobian propagate state and covariance.
- $$K=P_minus H^T(H P_minus H^T+R)^-1$$ — The Kalman gain balances predicted and measured uncertainty.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: position and GPS noise: m; heading: rad internal and displayed deg; time: s; Q and R: state-unit variances. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare missing measurement and vanishing-noise limits**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Consistent noiseless initial state and sensors keep estimation error near zero.
- Sparse GPS makes the filter approach dead reckoning between updates.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **inconsistent covariance, wrong Jacobian, and frame mismatch**. In the executable counterexample, **Radian state used as degrees** is triggered by: Set broken_mode true. Its observable failure is: The motion function and Jacobian evaluate a unit-corrupted heading. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and keep the nonlinear state and Jacobian in radians. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `gps_noise_m` at [0.05, 0.25, 1.0]: Noisier GPS has less correction authority.
- `gps_interval_s` at [0.1, 0.5, 2.0]: Longer prediction spans produce larger uncertainty peaks.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

Controls/GNC owns general EKF theory; Robotics applies it to embodied sensing. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
