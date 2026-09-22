# Drive a Differential Robot with Wheel Speeds

**Guiding question:** How do left and right wheel speeds determine a differential-drive robot's path?

## Concept and prediction

A differential drive has one body-forward velocity from the average wheel rim speed and one yaw rate from their difference. Constant commands trace a line, circle, or in-place rotation.

Before running the model, predict this: Equal wheel speeds make a straight line; increasing the right-minus-left speed bends the path counterclockwise. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$v=\frac{r}{2}(\omega_R+\omega_L)$$ — The mean wheel rim speed is the body-forward speed.
- $$\Omega=\frac{r}{b}(\omega_R-\omega_L)$$ — Wheel-speed difference divided by track width sets positive counterclockwise yaw.
- $$x=\frac{v}{\Omega}\sin(\Omega t),\quad y=\frac{v}{\Omega}[1-\cos(\Omega t)]$$ — For nonzero yaw rate, the exact pose follows a circular arc.

Symbols and units:

- $r$ — wheel radius (m); $b$ — wheel track (m).
- $\omega_L,\omega_R$ — left and right angular speeds (rad/s).
- $v$ — body-forward speed (m/s); $\Omega$ — yaw rate (rad/s).
- $x,y$ — robot-center position (m); heading is positive counterclockwise (rad or deg).

The world frame starts at the robot center with +x forward and +y left. Positive wheel speed drives forward; positive yaw is counterclockwise.

## Manipulation: two one-variable sweeps

1. Sweep `left_wheel_rad_s` through [-6,6,12] while holding the other controls at baseline. Watch average and difference create spin, arc, and opposite-curvature motion.
2. Restore baseline, then sweep `track_width_m` through [0.2,0.35,0.7]. For the same wheel-speed difference, a wider track must reduce yaw rate.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent closed-form source-model calculation; the actual vectors come from this Python experiment.

- When $\omega_L=\omega_R$, $\Omega=0$ and the arc limit becomes $x=vt, y=0$.
- When $\omega_R=-\omega_L$, $v=0$ and the center rotates in place.
- Doubling $b$ at fixed wheel speeds halves $\Omega$.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Decoupled translation.** The broken model accumulates heading but keeps translating along world +x. It violates the body-to-world velocity rotation and produces zero lateral displacement during a turn.

## Explanation and recovery

Disable the decoupled-translation mode so the instantaneous heading rotates the velocity vector. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Mapping one wheel directly to world x and the other to world y.
- Confusing commanded wheel angular speed with rim speed or achieved speed under slip.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.


## Deep derivation and conventions

The depth target for this module is to **derive the nonholonomic rolling constraints and wheel/body Jacobian**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: World +x is the initial forward direction, +y is left, and positive yaw is counterclockwise.

The governing relations are:

- $$v=r(omega_R+omega_L)/2$$ — Mean rim speed sets body-forward velocity.
- $$Omega=r(omega_R-omega_L)/b$$ — Differential rim speed sets yaw rate.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: wheel speed: rad/s; length: m; body speed: m/s; yaw rate: rad/s. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare straight, pure-spin, and unequal-wheel curvature**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Equal wheel speeds produce a straight line.
- Equal-and-opposite speeds rotate the center in place.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **wheel-radius mismatch and lateral slip**. In the executable counterexample, **Decoupled translation** is triggered by: Set broken_mode true. Its observable failure is: Heading changes while translation remains on world +x. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and rotate velocity through the body heading. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `left_wheel_rad_s` at [-6, 6, 12]: Average and difference create spin, arc, and reversed curvature.
- `track_width_m` at [0.2, 0.35, 0.7]: A wider track reduces yaw rate for the same wheel-speed difference.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

controls/gnc owns general tracking design; vehicle dynamics owns tire-force depth. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
