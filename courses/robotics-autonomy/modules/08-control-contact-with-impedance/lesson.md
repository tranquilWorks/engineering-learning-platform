# Control Contact with Impedance

**Guiding question:** What inputs, observable effects, and failure modes matter when you control Contact with Impedance?

## Concept and prediction

Impedance control commands a spring-damper relationship instead of a rigid position. In contact, the controller spring and wall compliance share the requested displacement.

Before running the model, predict this: Higher virtual stiffness raises contact force and moves penetration toward the command; damping mainly changes the transient. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$m\ddot x=K(x_d-x)-B\dot x-F_c$$ — Virtual spring and damper drive penetration while contact force opposes it.
- $$F_c=K_e\max(x,0)$$ — A unilateral linear wall produces force only during positive penetration.
- $$x_{ss}=\frac{K}{K+K_e}x_d$$ — Static controller and environment forces balance.

Symbols and units:

- $x,x_d$ — actual and desired wall penetration (m; control displayed in mm).
- $m$ — effective endpoint mass (kg).
- $K,B$ — virtual stiffness (N/m) and damping (N s/m).
- $K_e$ — environment stiffness (N/m); $F_c$ — contact force (N).

Positive x points into the wall. Contact force magnitude is reported positive, but its signed contribution to the dynamics is negative (opposes penetration).

## Manipulation: two one-variable sweeps

1. Sweep `stiffness_n_m` through [75,200,600] while holding the other controls at baseline. Compare steady penetration and force sharing with the wall.
2. Restore baseline, then sweep `damping_ns_m` through [4,20,60]. Compare overshoot and settling without changing the static balance.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent independent linear-system equilibrium and separately formulated state recurrence; the actual vectors come from this Python experiment.

- With $x_d=0$ and zero initial state, force and motion remain zero.
- At static balance, $K(x_d-x)=K_e x$.
- Increasing damping changes settling but not the ideal static penetration.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Disconnected wall reaction.** The broken model removes $F_c$ from the dynamics and reports zero contact force even while commanding penetration into the wall. It violates the action-reaction path.

## Explanation and recovery

Disable the disconnected-contact mode so the wall reaction opposes penetration in the dynamics and force diagnostic. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Using the contact-force magnitude with the wrong sign in the motion equation.
- Interpreting large controller stiffness as proof of safe physical contact.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.


## Deep derivation and conventions

The depth target for this module is to **derive the virtual spring-damper wrench and stored/dissipated energy**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Positive x enters the wall; reported force is a positive magnitude but enters dynamics with a negative sign.

The governing relations are:

- $$m x_ddot=K(x_d-x)-B x_dot-F_c$$ — Virtual impedance drives penetration against contact.
- $$F_c=K_e max(x,0)$$ — The unilateral wall opposes positive penetration.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: penetration: mm in UI, m internally; stiffness: N/m; damping: N s/m; contact force: N. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare free space, rigid contact, and zero damping**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Zero desired penetration keeps the zero state.
- Static controller force equals wall force.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **excess stiffness under delay or saturation**. In the executable counterexample, **Disconnected wall reaction** is triggered by: Set broken_mode true. Its observable failure is: The wall reaction is removed from dynamics and force reporting. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and reconnect the opposing contact force. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `stiffness_n_m` at [75, 200, 600]: Stiffness changes static sharing with the wall.
- `damping_ns_m` at [4, 20, 60]: Damping changes transient settling but not static balance.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P37-P39 add admittance, hybrid force, and passivity analysis. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
