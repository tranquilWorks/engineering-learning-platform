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


## Deep derivation and conventions

The depth target for this module is to **derive discrete bias integration and attitude-error growth**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: The stationary platform uses positive sensor bias as positive state drift; degrees/s are converted to radians/s.

The governing relations are:

- $$delta theta=b_g t$$ — Gyro bias integrates to linear angle drift.
- $$delta p=(1/2)b_a t^2$$ — Acceleration bias integrates twice to quadratic position drift.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: gyro bias: deg/s control, rad/s internal; acceleration bias: m/s^2; velocity drift: m/s; position drift: m. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare zero bias, zero motion, and sample-rate change**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Zero biases keep every drift state at zero.
- Doubling duration quadruples position drift.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **treating bias as white noise or ignoring frame/gravity conventions**. In the executable counterexample, **Degree/radian unit mismatch** is triggered by: Set broken_mode true. Its observable failure is: A degree-per-second number is integrated as radians per second. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and convert angular-rate units. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `gyro_bias_deg_s` at [0, 0.2, 1]: Angle drift scales linearly with gyro bias.
- `accel_bias_m_s2` at [0, 0.03, 0.1]: Velocity is linear and position quadratic in time.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

Controls/GNC owns full inertial-navigation mechanization; P49 studies observability. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
