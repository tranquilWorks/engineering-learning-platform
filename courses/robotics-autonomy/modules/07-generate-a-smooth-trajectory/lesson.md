# Generate a Smooth Trajectory

**Guiding question:** What inputs, observable effects, and failure modes matter when you generate a Smooth Trajectory?

## Concept and prediction

A time-normalized quintic polynomial connects rest-to-rest boundary conditions without velocity or acceleration jumps. Differentiating the same polynomial exposes actuator demand.

Before running the model, predict this: Increasing distance scales position, velocity, and acceleration; increasing duration reduces peak velocity as $1/T$ and acceleration as $1/T^2$. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$s(\tau)=10\tau^3-15\tau^4+6\tau^5$$ — The quintic progress variable satisfies position, velocity, and acceleration endpoint constraints.
- $$x=Ds,\quad\dot x=\frac{D}{T}s',\quad\ddot x=\frac{D}{T^2}s''$$ — Distance and duration scale the trajectory derivatives predictably.
- $$\tau=t/T\in[0,1]$$ — Normalized time keeps the shape independent of physical duration.

Symbols and units:

- $D$ — commanded travel distance (m); $T$ — move duration (s).
- $t$ — physical time (s); $\tau$ — dimensionless normalized time.
- $x,\dot x,\ddot x$ — position (m), velocity (m/s), and acceleration (m/s^2).
- $s',s''$ — derivatives with respect to normalized time.

Motion is one-dimensional in the positive x direction. Endpoint derivatives are evaluated from the analytic polynomial, not inferred from a coarse numerical difference.

## Manipulation: two one-variable sweeps

1. Sweep `distance_m` through [0.5,2,4] while holding the other controls at baseline. Check linear scaling of all dimensional outputs.
2. Restore baseline, then sweep `duration_s` through [1.5,4,8]. Check inverse-time scaling of peak velocity and acceleration.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent symbolic polynomial and endpoint-constraint evaluation; the actual vectors come from this Python experiment.

- At $t=0$, $x=\dot x=\ddot x=0$.
- At $t=T$, $x=D$ while velocity and acceleration return to zero.
- Doubling $T$ halves peak velocity and quarters peak acceleration.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Insufficient endpoint constraints.** The cubic smoothstep preserves zero endpoint velocity but has nonzero endpoint acceleration. A controller following it sees an acceleration jump at motion start and finish.

## Explanation and recovery

Disable the cubic profile and restore the quintic polynomial that enforces zero endpoint acceleration. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Differentiating with respect to normalized time and forgetting the $1/T$ factors.
- Calling a position-continuous profile smooth without checking its derivatives.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.


## Deep derivation and conventions

The depth target for this module is to **derive cubic/quintic boundary conditions and velocity/acceleration continuity**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Positive one-dimensional motion uses normalized time tau=t/T in [0,1].

The governing relations are:

- $$s(tau)=10tau^3-15tau^4+6tau^5$$ — Quintic progress satisfies rest-to-rest endpoint constraints.
- $$x=Ds, dx/dt=(D/T)s', d2x/dt2=(D/T^2)s''$$ — Distance and time scale derivatives predictably.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: position: m; velocity: m/s; acceleration: m/s^2; jerk: m/s^3. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare time scaling and a zero-displacement move**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Start and finish velocity are zero.
- Start and finish acceleration are zero only for the quintic.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **discontinuous acceleration and infeasible joint limits**. In the executable counterexample, **Insufficient endpoint constraints** is triggered by: Set broken_mode true. Its observable failure is: A cubic profile leaves nonzero endpoint acceleration. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and restore the quintic polynomial. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `distance_m` at [0.5, 2, 4]: All dimensional outputs scale with distance.
- `duration_s` at [1.5, 4, 8]: Velocity scales as 1/T and acceleration as 1/T^2.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P33 and P58 extend this scalar profile to bounded multijoint and optimized trajectories. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
