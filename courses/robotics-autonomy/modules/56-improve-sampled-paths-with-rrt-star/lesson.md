# Improve sampled paths with RRT-Star

Rapidly exploring random trees are good at finding a feasible motion without discretizing the entire configuration space. Their first solution, however, depends heavily on early parent choices. RRT-Star adds local cost optimization: a new vertex chooses the best collision-free parent in a neighborhood, and existing neighbors are rewired through it when that lowers their cost. The result is an anytime planner whose incumbent can improve as samples accumulate.

## Model, derivation, and conventions

The state is a point in a bounded two-dimensional workspace measured in metres. Circular obstacles are inflated by a fixed robot radius. Samples use a deterministic Halton sequence, with a periodic goal sample to make replay and finite-budget comparison reliable. `Steer` limits each growth edge to `0.68 m`; every proposed edge is tested using exact closest-point segment distance.

For an ordinary RRT extension, the nearest existing vertex becomes the parent and receives cost `J(parent)+edge_length`. RRT-Star instead forms a near set using the selected rewire radius. Among collision-free candidates it chooses the parent minimizing that expression. After insertion, each nearby vertex is tested for a cheaper route through the new vertex. A successful rewire changes the parent and propagates the cost difference to descendants.

Goal connection is treated as another collision-checked edge. The incumbent is the minimum cost of any tree vertex within the goal-connection radius plus its Euclidean distance to the goal. The straight start-to-goal distance is a lower bound, even when that chord crosses an obstacle. Reported excess is `J_best/J_lower-1`, a dimensionless measure that must remain nonnegative.

## Predict before running

Predict that a larger sample budget will not make the best known cost worse: an anytime planner can retain its previous incumbent. More samples need not improve every run, because they may fall in irrelevant regions. Predict also that a larger rewire radius considers more parents but can increase computation. Finally, predict that disabling rewiring will preserve collision freedom yet return a longer path with zero rewires. This is a subtler broken case than an outright collision; feasibility alone is below the competency target.

## Baseline workflow

Run 220 samples with a `1.6 m` rewire radius. The response plot shows the incumbent path and inflated obstacle boundaries. Trace the route around both obstacles and verify that no edge cuts a boundary. The primary metric is the sum of its Euclidean edge lengths.

The mechanism plot records best goal cost after every sampling attempt. Rejected samples repeat the previous incumbent. The curve should be nonincreasing once a finite connection exists. The straight-line lower-bound trace remains below it because obstacles and tree discretization require a detour. Successful rewires quantify structural improvement, but a large count is not itself a goal: only valid cost reduction matters.

Review the excess ratio rather than comparing costs across differently scaled workspaces. It states how far the current solution lies above a geometric bound while preserving metres in the primary cost.

## Two one-variable sweeps

First reduce only the sample budget from 220 to 100. Obstacles, step size, Halton prefix, and rewire radius are unchanged. Because the smaller run is a prefix of the larger deterministic sequence, it offers a clean anytime comparison. The larger run can retain everything found by the shorter run and may improve it.

For the second sweep, restore 220 samples and increase only rewire radius to `3.0 m`. More vertices become parent and rewire candidates. The best cost should remain above the lower bound and every accepted edge must still pass collision checking. The number of rewires need not increase monotonically: a wider radius can choose better parents initially and thereby eliminate later repairs. Interpret cost and validity before counts.

## Intentionally broken case

Broken mode grows the same collision-checked tree but always keeps the nearest parent and never rewires. That is an ordinary RRT with deterministic samples. It can reach the goal safely, yet early detours become permanent. The named failure is therefore “feasible path presented as an improving RRT-Star solution.”

This distinction matters for specifications. If the requirement is merely to find any path under a time limit, RRT may be acceptable. If the product claims asymptotic improvement or uses cost as a planning invariant, removing rewiring violates that claim even though a demo still reaches the goal.

## Recovery

Restore three linked operations. Build the near set with a bounded metric radius. Choose the lowest-cost collision-free parent before adding the vertex. Then test whether routing any neighbor through the new vertex lowers its cost, updating descendants so cached path costs remain coherent.

After each structural change, the parent relation must remain a tree: no self-parenting, no cycles, and exactly one route to the root. A production implementation often uses spatial indexing and explicit child lists so near-neighbor queries and descendant propagation are efficient. This small implementation favors auditable lists over those optimizations.

## Alternative and limiting cases

In theoretical RRT*, the neighborhood radius usually shrinks with sample count according to a dimension-dependent expression while retaining enough neighbors for asymptotic optimality. A fixed radius is used here to expose the mechanism over a small deterministic budget; no asymptotic convergence claim is made.

Informed RRT* restricts later sampling to an ellipsoidal subset after a solution exists. RRT-Connect emphasizes rapid feasibility with two trees but does not provide the same cost-improvement argument. In obstacle-free space with enough favorable samples, incumbent cost approaches the straight-line bound. With radius too small, the algorithm behaves much like RRT because no useful alternative parents enter the near set. With an excessively large radius, correctness remains possible but pair checking dominates.

## Independent evidence and MATLAB-style design boundary

The independent reference regenerates the sample sequence, rebuilds its own tree and costs, checks geometry independently, and retains baseline, budget, radius, broken, and recovery signatures. It imports no production experiment and consumes no production result. Numerical agreement covers best cost, successful rewire count, and excess ratio.

This software demonstration does not execute MATLAB or establish parity with a robotics toolbox. It does not model steering dynamics, localization uncertainty, asynchronous cancellation, browser accessibility, learner performance, physical collision margins, real-time deadlines, certification, or deployment.

## Engineering review checklist

- Verify each Steer edge and goal connection against inflated obstacles.
- Verify parent choice minimizes total cost, not only edge length.
- Propagate a rewire's cost change to every descendant.
- Prevent cycles and self-parent assignments.
- Keep incumbent history nonincreasing after the first solution.
- Keep best cost at or above the Euclidean lower bound.
- Bound samples, neighborhood work, and runtime deterministically.

## Common mistakes

Common bugs choose the nearest node after computing a near set, rewire without collision checking, update a parent's cost but leave descendants stale, compare squared edge length with unsquared path cost, or connect the goal through an obstacle. Another error calls any RRT with a cost metric “RRT-Star” even though no parent optimization occurs. Tie breaking also matters for deterministic evidence; unordered container iteration can change the exact tree and rewire count.

## Focused check and teach-back

Write the inequality that permits rewiring a neighbor through a new vertex, including both accumulated and edge cost. Explain why collision freedom must be checked again even when both endpoint vertices are valid. Then teach back why the straight-line distance remains a lower bound when it crosses an obstacle, and why the broken planner can be safe yet still fail the lesson's optimization competency.
