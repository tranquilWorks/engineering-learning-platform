# Plan with Random Samples

**Guiding question:** What inputs, observable effects, and failure modes matter when you plan with Random Samples?

## Concept and prediction

Sampling-based planning avoids enumerating an entire continuous configuration space. An RRT repeatedly samples, finds the nearest tree node, steers a bounded distance, and accepts only collision-free extensions. Sampling coverage and collision validity solve different problems.

Predict how sample budget and goal bias affect time-to-connection. Then predict whether checking only sampled states can guarantee that the segment between them is safe.

## Model, symbols, and equations

- $$q_{\mathrm{new}}=q_{\mathrm{near}}+\min(\eta,\|q_s-q_{\mathrm{near}}\|)\frac{q_s-q_{\mathrm{near}}}{\|q_s-q_{\mathrm{near}}\|}$$ — bounded tree extension.
- $$c(e)=\min_{\alpha\in[0,1]}\|q_a+\alpha(q_b-q_a)-q_o\|-r_o$$ — continuous edge clearance from a circular obstacle.
- $$L=\sum_e\|q_{e+1}-q_e\|$$ — returned path length.

World coordinates and step size use metres. The 10 m by 10 m plane has +x right and +y up. The low-discrepancy sequence is deterministic so verification can compare exact planner behavior.

## Manipulation: two one-variable sweeps

1. Sweep `sample_budget` through [200,700,1200]. A larger budget increases the opportunity to find a valid connection but does not guarantee optimality.
2. Restore baseline, then sweep `goal_bias` through [0.05,0.15,0.35]. More goal samples can shorten search, but excessive bias may underexplore detours.

The first plot displays the full tree, obstacle, and returned path. The second gives continuous clearance for each path edge.

## Evidence and limiting cases

The independent reference rebuilds the deterministic RRT and analytically audits segment-circle clearance. The production implementation uses vectorized nearest-neighbor selection and its own tree state.

- With no obstacle, direct goal-biased growth eventually connects start to goal.
- A zero sample budget cannot establish a path.
- Infinite samples do not validate edges if the collision checker is missing.

This is bounded software planning evidence, not dynamics, footprint, map, physical robot, HIL, or field validation.

## Intentionally broken assumption

**Edge collision checking omitted.** Broken mode accepts every extension and goal connection. The returned polyline crosses the obstacle, producing negative clearance despite successful goal status.

## Explanation and recovery

Restore analytic segment collision checks with a positive safety margin, then audit every edge in the final parent chain. Goal reachability is necessary but not sufficient.

## Common mistakes

- Checking only node endpoints rather than the continuous edge.
- Confusing probabilistic completeness with optimality or finite-run success.
- Increasing sample count to compensate for invalid geometry.
- Reporting path length without clearance and reached/failed status.

## Focused check and teach-back

At baseline, cite node count, path length, minimum clearance, and collision edges. Omit collision checks, recover them, and teach back steering, units, sampling tradeoffs, and why validation must follow the full path.


## Deep derivation and conventions

The depth target for this module is to **derive sampling, steering, collision, and probabilistic-completeness boundaries**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: The planar workspace uses +x right and +y up; all positions, step sizes, radii, and clearances use metres.

The governing relations are:

- $$q_new=q_near+min(eta,d) direction$$ — The RRT extends a bounded distance toward each sample.
- $$c(e)=min_alpha distance(segment(alpha), obstacle)-r$$ — Continuous edge clearance determines validity.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: workspace and path: m; goal bias: ratio; sample budget: samples. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare goal bias, step size, and unreachable budget**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- No obstacle permits direct growth toward the goal.
- No finite sample budget validates a path when edge checking is absent.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **unchecked edges and confusing failure-to-find with infeasibility**. In the executable counterexample, **Edge collision checking omitted** is triggered by: Set broken_mode true. Its observable failure is: The tree and final path accept segments through the circular obstacle. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and require positive analytic segment clearance. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `sample_budget` at [200, 700, 1200]: More samples increase the opportunity to connect through free space.
- `goal_bias` at [0.05, 0.15, 0.35]: Goal bias trades direct progress against detour exploration.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P55-P56 add PRM and asymptotically improving RRT-star. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
