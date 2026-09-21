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
