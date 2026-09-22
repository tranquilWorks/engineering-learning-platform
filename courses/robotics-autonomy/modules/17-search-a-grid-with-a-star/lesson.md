# Search a Grid with A-Star

**Guiding question:** What inputs, observable effects, and failure modes matter when you search a Grid with A-Star?

## Concept and prediction

A-star orders candidate nodes by known path cost plus estimated remaining cost. A useful heuristic reduces search without changing the optimal solution only when its assumptions match the motion and cost model. Collision validity is separate from numerical path length.

Predict how moving the only wall gap changes safe path cost, and why a path that is shorter than the Dijkstra optimum should be treated as suspicious rather than superior.

## Model, symbols, and equations

- $$f(n)=g(n)+w_h h(n)$$ — search priority from cost-to-come and weighted heuristic.
- $$h(n)=|x_g-x_n|+|y_g-y_n|$$ — Manhattan distance for four-connected unit-cost motion.
- $$g(n')=g(n)+1$$ — one-cell transition cost.

Grid coordinates use integer cells, +x right and +y up. Path cost units are cell steps. With $w_h=1$, Manhattan distance is admissible and consistent for this model; larger weights trade optimality guarantees for greedier search.

## Manipulation: two one-variable sweeps

1. Sweep `heuristic_weight` through [0,1,2]. Expansion count should fall as the search becomes more goal-directed; weight zero is Dijkstra.
2. Restore baseline, then sweep `gap_offset` through [-7,0,7]. Safe path cost follows the detour required to reach the gap.

The grid plot overlays blocked cells and the returned path. The mechanism plot shows expansion-priority evolution.

## Evidence and limiting cases

An independent Dijkstra search provides the safe optimum; a separate collision audit checks every returned cell.

- With heuristic weight zero, A-star reduces to Dijkstra.
- With the gap on the direct start-goal row, the safe optimum is the straight path.
- A finite path cost is meaningless if any path cell is occupied.

This is software planning evidence, not vehicle clearance, map fidelity, physical navigation, HIL, or field validation.

## Intentionally broken assumption

**Obstacle checks disabled.** Broken mode treats every in-bounds neighbor as traversable. The direct route crosses the wall and appears cheaper than the independently computed safe optimum.

## Explanation and recovery

Restore occupancy rejection during neighbor expansion and re-audit the reconstructed path. Do not infer validity solely from reaching the goal or from a low cost.

## Common mistakes

- Using Manhattan distance with diagonal moves and assuming it remains admissible.
- Marking a node closed before a better cost can be considered.
- Comparing paths without the same cost and collision model.
- Treating an obstacle-violating path as an optimization win.

## Focused check and teach-back

At baseline, cite returned cost, safe optimum, collision count, and expansions. Move the gap, disable collision checks, recover them, and teach back $g$, $h$, units, admissibility, and independent path validation.


## Deep derivation and conventions

The depth target for this module is to **derive admissibility/consistency roles and graph cost accounting**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Integer grid +x points right and +y up; motion uses four-connected unit cell steps.

The governing relations are:

- $$f(n)=g(n)+w_h h(n)$$ — A-star combines known and estimated remaining cost.
- $$h=abs(dx)+abs(dy)$$ — Manhattan distance is admissible for four-connected unit-cost motion at unit weight.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: position: cells; path and heuristic cost: cell steps; expansions: nodes. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare Dijkstra, A-star, and a blocked goal**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Heuristic weight zero reduces A-star to Dijkstra.
- A gap on the direct row permits the straight safe path.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **inadmissible heuristic and diagonal/corner-cutting errors**. In the executable counterexample, **Obstacle checks disabled** is triggered by: Set broken_mode true. Its observable failure is: The returned shortest route crosses occupied wall cells. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and reject occupied neighbors, then audit the path. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `heuristic_weight` at [0, 1, 2]: Higher weight reduces expansions but can weaken optimality guarantees.
- `gap_offset` at [-7, 0, 7]: Safe path cost follows the wall-gap detour.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P54 extends search to incremental replanning. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
