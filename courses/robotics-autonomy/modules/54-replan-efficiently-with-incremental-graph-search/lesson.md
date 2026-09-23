# Replan efficiently with incremental graph search

A global route is rarely planned once. A range return closes a doorway, a mapper clears a corridor, or a cost layer changes while the robot is already moving. Running a fresh search is valid, but it throws away graph values that remain correct. This laboratory studies Lifelong Planning A* (LPA*), an incremental shortest-path algorithm that keeps two values per vertex and repairs only inconsistencies induced by the changed map. The important result is not simply a shorter queue. It is a route that is valid in the new graph and a precise account of which old computations were safe to reuse.

## Model, derivation, and conventions

The workspace is a four-connected occupancy grid. Each free horizontal or vertical edge has unit graph cost; the displayed physical length is that cost multiplied by the selected grid resolution in metres. The start is on the left and the goal on the right. A vertical wall has two passages. The initial route uses the nearby passage; the map update occupies that passage, forcing a detour through the second opening.

Ordinary A* stores the best known cost-to-come, usually written `g`. LPA* also stores a one-step lookahead:

`rhs(start)=0`, and `rhs(s)=min(g(s')+c(s',s))` over predecessors `s'` for every other vertex.

A vertex is locally consistent when `g(s)=rhs(s)`. If an edge changes, only vertices whose best predecessor relation can be affected become inconsistent. The priority key is the ordered pair `[min(g,rhs)+w h, min(g,rhs)]`, where Manhattan distance supplies `h` and the displayed heuristic weight `w` lies between zero and one. Processing continues until the goal is consistent and no queued key can improve it. Path extraction walks backward from the goal through the predecessor minimizing `g+c`.

The code deliberately uses an explicit stale-entry priority queue. Each pushed vertex carries a version, and obsolete heap entries are ignored. That detail matters in real implementations: Python heaps do not support decrease-key directly, and treating every duplicate as current can expand incorrect states or make runtime nondeterministic.

## Predict before running

First predict three facts. The original direct path will collide after the passage is blocked. A correct repair will return a longer path with zero occupied cells. Finally, changing physical resolution will scale path length but will not change the graph topology or the number of occupied cells. Do not predict that incremental search must always expand fewer nodes than every possible fresh A* implementation. Queue work depends on heuristic, topology, tie breaking, and the location of the changed edge. The defensible claim is narrower: unchanged consistent values are reused, and validity is re-established by processing the affected dependency structure.

## Baseline workflow

Run the baseline at `0.5 m` resolution and heuristic weight `1`. Read the response plot as map geometry, not time history. The occupied wall cells and the repaired route use metres on both axes. Confirm that the route leaves the first passage, travels to the remaining opening, and returns to the goal side of the wall. The occupied-cell metric must be zero.

Then inspect the mechanism plot. The first point records work for the initial plan. The second compares the incremental repair with a cold uniform-cost calculation on the updated grid. The ratio metric divides repair expansions by that cold benchmark. It is a work indicator, not a proof of asymptotic superiority. The path-length metric is the sum of equal grid-edge lengths, so no hidden diagonal corner cutting is present.

Finally, toggle broken mode. Its path looks impressively short because it is the cached path through the now-blocked cell. The collision metric exposes why wall-clock work or route length cannot be reviewed independently of map revision and collision validity.

## Two one-variable sweeps

For the first sweep, change only grid resolution from `0.5 m` to `1.0 m`. The sequence of grid vertices should remain the same, so the physical path length doubles while collision count and graph work ratios retain their dimensionless meaning. This sweep catches the common error of reporting cell count as metres.

For the second sweep, restore `0.5 m` and move only heuristic weight from `1` to `0`. The key then becomes uniform-cost incremental search. The optimal path cost should remain unchanged because both admissible settings solve the same graph; queue work may change. This separates solution correctness from search guidance. If path cost changes, the heuristic has leaked into edge cost or termination is premature.

## Intentionally broken case

Broken mode represents a real autonomy failure: a planner caches a path but misses the map-update notification. It reports zero repair expansions and continues commanding the old route. That output is internally consistent with the old map and invalid in the current one. The named failure is not “LPA* is slow” or “the heuristic is bad.” It is revision incoherence between occupancy data and the route consumer.

The failure also illustrates why checking only whether a path exists is weak. A list of connected grid coordinates can be perfectly well formed while containing a cell that is no longer traversable. The experiment therefore retains both graph cost and an explicit post-plan collision audit against the updated occupancy set.

## Recovery

Recovery starts at the update boundary. Insert the changed cell into the occupancy set, recompute that vertex's lookahead, and update its adjacent vertices because their predecessor choices may include it. Continue processing until the LPA* termination condition is satisfied. Extract a new path only after consistency is restored, then independently scan every path vertex against the current occupancy revision.

In a production stack, the same reasoning implies versioned cost maps, atomic route publication, and a controller rule that refuses paths planned against an obsolete map. Incremental values are an optimization cache, never an authority that overrides current collision data.

## Alternative and limiting cases

D* Lite is a closely related formulation oriented toward a moving start and backward search from the goal. It is often a better operational choice for a robot that advances while sensing. LPA* is used here because its `g/rhs` derivation makes local inconsistency visible. A fresh A* search is also correct and may be simpler when updates are rare or the graph is small.

If no edge cost changes, no vertex becomes inconsistent and repair work tends to zero. If the update disconnects start from goal, the correct result is no finite path, not a route through infinity-valued predecessors. If heuristic weight is zero, the method retains incremental repair but loses informed ordering. Values above one can reduce work but sacrifice the optimality guarantee, so this laboratory intentionally disallows them.

## Independent evidence and MATLAB-style design boundary

The independent reference reconstructs the grid, the initial/update occupancy sets, the `g/rhs` recursion, and a separate cold search without importing the production experiment or reading its output. Five retained cases cover baseline, resolution, heuristic, broken, and recovery scenarios. Equality is checked on path length, occupied-cell count, and repair ratio with explicit tolerances.

This is deterministic Python software evidence. The lesson uses matrix-and-vector conventions familiar from MATLAB, but no MATLAB runtime comparison was executed. It does not validate a ROS navigation stack, asynchronous cost-map transport, browser accessibility, learner outcomes, timing on an embedded computer, or a physical robot.

## Engineering review checklist

- Confirm the map revision used for path extraction matches the collision audit.
- Confirm changed vertices and adjacent predecessor relations are updated.
- Confirm the heuristic is admissible for the selected edge costs.
- Confirm priority-queue duplicates are invalidated deterministically.
- Confirm unreachable goals terminate without fabricating predecessors.
- Confirm grid cells are converted to metres exactly once.
- Confirm the controller rejects a route with any occupied vertex.

## Common mistakes

The most damaging mistake is to equate low repair work with correctness. Other errors include blocking a cell without updating its neighbors, using Euclidean physical distance with unscaled grid cost, terminating when the goal first enters the queue, extracting through an infinite `g` value, and forgetting that removal as well as insertion of obstacles can create inconsistency. Another subtle bug mutates the occupancy set after planning but before plotting, making the route appear invalid even though it was valid for the revision actually searched. Version the inputs instead of relying on timing.

## Focused check and teach-back

Explain why `rhs` is called a one-step lookahead and identify which equality marks local consistency. Then describe, without saying “run A* again,” what must happen after the near passage becomes occupied. Your teach-back should distinguish path optimality, map validity, and computational reuse. Finish by explaining why the broken result's shorter path and zero search work are evidence of failure rather than improvement.
