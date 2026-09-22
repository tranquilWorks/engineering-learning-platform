# Avoid Moving Obstacles

**Guiding question:** What inputs, observable effects, and failure modes matter when you avoid Moving Obstacles?

## Concept and prediction

Dynamic collision avoidance asks whether two moving bodies violate separation at the same future time. Current distance and static-map clearance are insufficient; relative velocity determines closest point of approach.

The default obstacle starts at $(5,-5)$ m and crosses upward while the robot moves generally toward +x. Predict the collision time for a straight robot heading and which turn direction gives the smallest safe deviation.

## Model, symbols, and equations

- $$\mathbf r(t)=\mathbf r_0+(\mathbf v_o-\mathbf v_r)t$$ — relative position.
- $$t_{\mathrm{CPA}}=\operatorname{clip}\left(-\frac{\mathbf r_0^T\mathbf v_{rel}}{\|\mathbf v_{rel}\|^2},0,T\right)$$ — closest-approach time over horizon $T$.
- $$d_{\mathrm{CPA}}=\|\mathbf r(t_{\mathrm{CPA}})\|$$ — predicted minimum separation.

World +x is the robot's nominal goal direction, +y is left, velocities use m/s, position and separation use metres, time uses seconds, and positive heading is counterclockwise.

## Manipulation: two one-variable sweeps

1. Sweep `obstacle_speed_m_s` through [0.2,1,2]. The crossing time moves relative to the robot's arrival and can create or remove conflict.
2. Restore baseline, then sweep `prediction_horizon_s` through [2,8,10]. A short horizon may not see the future crossing soon enough.

The encounter plot shows actual trajectories. The candidate plot shows predicted closest separation versus robot heading and the required safety threshold.

## Evidence and limiting cases

An independent scalar loop enumerates heading candidates and analytically evaluates closest approach. Production uses a vectorized candidate calculation, then simulates actual trajectories.

- With zero relative velocity, separation remains constant.
- A horizon shorter than the collision time cannot reject that future conflict.
- Large current distance does not imply safety when relative motion closes it.

This is constant-velocity software prediction, not a full dynamics, perception, physical robot, HIL, or field result.

## Intentionally broken assumption

**Moving obstacle treated as static.** Broken mode predicts zero obstacle velocity. It chooses a straight path because the initial obstacle is off-axis, but actual motion puts both bodies at the crossing together.

## Explanation and recovery

Restore measured obstacle velocity in the relative-motion equation, select the least-deviating safe candidate, and replay the actual encounter. Real systems also need uncertainty, acceleration bounds, and receding-horizon updates.

## Common mistakes

- Checking geometric path intersection without checking time coincidence.
- Using absolute rather than relative velocity in closest-approach time.
- Looking beyond the model-valid prediction horizon.
- Calling a constant-velocity safe candidate collision-proof under arbitrary acceleration.

## Focused check and teach-back

At baseline, cite selected heading, closest separation, and CPA time. Freeze predicted obstacle motion, observe the safety violation, recover it, and teach back the relative frame, units, horizon limit, and candidate-selection rule.


## Deep derivation and conventions

The depth target for this module is to **derive relative-motion prediction and time-to-collision**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: World +x is the nominal robot goal direction, +y is left, and positive candidate heading is counterclockwise.

The governing relations are:

- $$r(t)=r_0+(v_o-v_r)t$$ — Relative position determines the dynamic encounter.
- $$t_CPA=clip(-r_0 dot v_rel / norm(v_rel)^2,0,T)$$ — Closest-approach time is bounded by the prediction horizon.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: position and separation: m; velocity: m/s; heading: deg; time: s. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare static, crossing, and receding obstacles**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Zero relative velocity keeps separation constant.
- A horizon shorter than the collision time cannot reject that conflict.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **myopic velocity choice, oscillation, and infeasible braking**. In the executable counterexample, **Moving obstacle treated as static** is triggered by: Set broken_mode true. Its observable failure is: The planner chooses the straight route using zero predicted obstacle velocity. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and use relative velocity in closest-approach prediction. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `obstacle_speed_m_s` at [0.2, 1, 2]: Changing crossing time can create or remove conflict.
- `prediction_horizon_s` at [2, 8, 10]: A short horizon can miss a later collision.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P59-P60 add dynamic feasibility and local predictive constraints. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
