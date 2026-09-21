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
