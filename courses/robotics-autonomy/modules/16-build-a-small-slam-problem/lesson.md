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


## Deep derivation and conventions

The depth target for this module is to **derive pose-landmark constraints, gauge freedom, and linearized residuals**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: A one-dimensional world uses increasing +x along robot travel; the first pose defines the absolute origin when the prior is present.

The governing relations are:

- $$x_i-x_(i-1)=u_i+n_i$$ — Odometry factors constrain consecutive poses.
- $$l-x_i=z_i+v_i$$ — Range factors connect poses to a landmark.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: poses and landmark: m; sensor sigmas: m; whitened residual: sigma. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare open trajectory with a loop closure**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- A strong correct prior effectively fixes the first pose.
- Without an absolute constraint, every common state translation has equal relative residual.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **anchoring errors, false association, and overconfident constraints**. In the executable counterexample, **Missing gauge prior** is triggered by: Set broken_mode true. Its observable failure is: All relative factors remain invariant to a common translation and the matrix loses rank. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and anchor one pose with an absolute prior. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `odometry_sigma_m` at [0.01, 0.05, 0.3]: Odometry weighting trades against landmark factors.
- `range_sigma_m` at [0.02, 0.1, 0.5]: Landmark coupling weakens as range uncertainty grows.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P51-P53 provide the substantial nonlinear factor-graph continuation. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
