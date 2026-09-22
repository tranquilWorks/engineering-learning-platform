# Calibrate Sensor Extrinsics

**Guiding question:** What inputs, observable effects, and failure modes matter when you calibrate Sensor Extrinsics?

## Concept and prediction

Extrinsic calibration estimates the rigid transform from a sensor frame to the robot body frame. In two dimensions that transform contains one yaw angle and two translation components. Translation and rotation must be observable in the correspondence geometry.

Predict what the residual vectors will look like if the true sensor yaw is 12 deg but the calibration solves only translation. Will adding more correspondences remove that systematic pattern?

## Model, symbols, and equations

- $$\mathbf p_i^B=R(\psi_{BS})\mathbf p_i^S+\mathbf t_{BS}+\mathbf n_i$$ — sensor-to-body correspondence model.
- $$R^*=\arg\min_{R\in SO(2)}\sum_i\|\tilde{\mathbf p}_i^B-R\tilde{\mathbf p}_i^S\|^2$$ — centered rigid alignment.
- $$\mathbf t^*=\bar{\mathbf p}^B-R^*\bar{\mathbf p}^S$$ — translation recovered from centroids.

Superscripts identify the frame in which a point is expressed. +x is forward, +y is left, and positive yaw is counterclockwise. Units are metres for translation, millimetres for displayed residuals, and degrees at the interface but radians internally for yaw.

## Manipulation: two one-variable sweeps

1. Sweep `sensor_yaw_deg` through [-30,0,30]. A correct rigid fit should track yaw while keeping residual RMS near the noise floor.
2. Restore baseline, then sweep `noise_mm` through [0,2,20]. Parameter error and residual RMS should grow with correspondence noise.

The first plot overlays transformed sensor points and body-frame references. The second shows whether residual error is random or index-dependent.

## Evidence and limiting cases

The independent reference uses the closed-form planar Procrustes angle from cross/dot sums, whereas the production calibration uses an SVD-based proper-rotation solution.

- With zero yaw, translation-only and rigid fits coincide apart from noise.
- With zero noise and non-collinear correspondences, the rigid transform is recovered to numerical precision.
- Repeating one point cannot make rotation observable; spatially distributed correspondences are required.

This is simulated calibration evidence, not a physical metrology, robot, sensor, bench, HIL, or field result.

## Intentionally broken assumption

**Translation-only extrinsic.** Broken mode fixes $R=I$ and fits only the centroid offset. It can align the center but not the orientation.

## Explanation and recovery

Disable translation-only fitting, center both point sets, estimate the proper $SO(2)$ rotation, then recover translation. Reject a reflected solution by enforcing determinant +1.

## Common mistakes

- Reversing the body-to-sensor and sensor-to-body transform.
- Estimating translation before accounting for rotation.
- Using nearly coincident or collinear calibration poses and assuming all degrees of freedom are observable.
- Interpreting low residual on a narrow calibration set as guaranteed extrapolation accuracy.

## Focused check and teach-back

At baseline, cite estimated translation, yaw, and residual RMS. Reproduce the translation-only residual pattern, recover the rigid fit, and teach back the frame convention, observability requirement, equation order, and reflection check.


## Deep derivation and conventions

The depth target for this module is to **derive rigid extrinsic calibration residuals and identifiability**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Body and sensor use +x forward, +y left, and positive counterclockwise yaw; the estimated transform maps sensor coordinates into body coordinates.

The governing relations are:

- $$p_B=R_BS p_S+t_BS+n$$ — A planar rigid transform relates sensor and body correspondences.
- $$t=mean(p_B)-R mean(p_S)$$ — Translation follows after rotation is estimated.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: translation: m; yaw: deg control, rad internal; residual: m and displayed mm. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare exact alignment with degenerate collinear observations**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Zero yaw makes translation-only fitting sufficient apart from noise.
- Zero noise with distributed correspondences recovers the rigid transform to numerical precision.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **inverting the wrong transform or accepting unobservable calibration**. In the executable counterexample, **Translation-only extrinsic** is triggered by: Set broken_mode true. Its observable failure is: The fit fixes rotation to identity and leaves a position-dependent residual. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and solve a proper SO(2) rotation before translation. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `sensor_yaw_deg` at [-30, 0, 30]: Rigid calibration tracks yaw without structured residual.
- `noise_mm` at [0, 2, 20]: Parameter error and residual RMS grow with correspondence noise.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P42 covers camera intrinsics; P66 integrates the frame tree. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
