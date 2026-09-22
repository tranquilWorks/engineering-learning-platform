# Integrate Wheel Odometry

**Guiding question:** What inputs, observable effects, and failure modes matter when you integrate Wheel Odometry?

## Concept and prediction

Wheel odometry composes many small relative motions. Encoder counts constrain wheel rotation, not ground motion, so correct integration can still drift when a wheel slips or its radius is miscalibrated.

Predict which error dominates at baseline: encoder quantization, the 2% right-wheel slip, or the choice between an exact twist and old-heading Euler integration.

## Model, symbols, and equations

- $$\Delta s=\tfrac12(\Delta s_R+\Delta s_L),\quad\Delta\theta=(\Delta s_R-\Delta s_L)/b$$ — local differential-drive twist.
- $$\Delta s_w=r\,\Delta n_w\,2\pi/(4N)$$ — x4 quadrature counts converted to wheel travel.
- $$\Delta\mathbf p=\Delta s\,\operatorname{sinc}(\Delta\theta/2)[\cos(\theta+\Delta\theta/2),\sin(\theta+\Delta\theta/2)]^T$$ — exact constant-twist translation.

$r$ is wheel radius, $b$ is track width, $N$ is encoder lines/rev, and $\theta$ is positive counterclockwise world yaw. Units are metres for geometry and position, radians internally for yaw, and lines/rev for encoder resolution. Body +x points forward and body +y left.

## Manipulation: two one-variable sweeps

1. Sweep `encoder_cpr` through [128,1024,4096]. Quantization ripple should shrink, but slip-driven bias should remain.
2. Restore baseline, then sweep `slip_percent` through [0,2,15]. Position and heading error should grow systematically.

The trajectory plot shows accumulated path disagreement. The diagnostic plot separates translational and heading errors versus time.

## Evidence and limiting cases

An independent oracle reconstructs the same count increments and composes closed-form SE(2) exponentials; the production experiment owns its own integration path.

- Equal wheel increments produce straight motion and the sinc limit approaches one.
- Infinite encoder resolution removes quantization but not slip.
- Zero slip and sufficiently fine counts recover the commanded differential-drive path.

This is software odometry evidence, not physical encoder, tire/track, robot, HIL, bench, or field validation.

## Intentionally broken assumption

**Old-heading Euler step.** Broken mode translates using the heading at the start of each interval instead of the twist midpoint. Finite rotations then introduce a systematic integration chord error.

## Explanation and recovery

Disable Euler mode and compose each wheel increment as an SE(2) twist. Then separate residual drift into quantization and wheel-to-ground model error; integration cannot infer unmeasured slip.

## Common mistakes

- Treating encoder rotation as guaranteed ground displacement.
- Forgetting x4 quadrature when converting line count to edge count.
- Updating translation with the new or old heading instead of the twist midpoint.
- Comparing wrapped and unwrapped heading differences directly.

## Focused check and teach-back

At baseline, cite final position and heading error, run both sweeps, reproduce the Euler failure, and recover it. Teach back the count conversion, twist equation, frame convention, and why perfect integration does not eliminate slip drift.


## Deep derivation and conventions

The depth target for this module is to **derive SE(2) odometry propagation and small-angle limit**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: World +x and +y form a right-handed plane; body +x is forward and positive yaw is counterclockwise.

The governing relations are:

- $$Delta s=(Delta s_R+Delta s_L)/2$$ — Mean wheel travel gives local forward motion.
- $$Delta theta=(Delta s_R-Delta s_L)/b$$ — Differential wheel travel gives yaw change.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: wheel radius and position: m; track width: m; heading: rad internal and displayed deg; encoder resolution: lines/rev. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare straight motion, pure rotation, and unequal ticks**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Equal wheel increments produce straight translation.
- Infinite encoder resolution removes quantization but not wheel slip.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **timestamp, wrap, slip, and left/right convention faults**. In the executable counterexample, **Old-heading Euler step** is triggered by: Set broken_mode true. Its observable failure is: Finite translation is projected along the interval start heading instead of the exact twist midpoint. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and compose the SE(2) wheel increment. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `encoder_cpr` at [128, 1024, 4096]: Quantization decreases with resolution but slip bias remains.
- `slip_percent` at [0, 2, 15]: Unmeasured wheel slip accumulates position and heading error.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P49-P53 extend odometry into observable multi-sensor SLAM. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
