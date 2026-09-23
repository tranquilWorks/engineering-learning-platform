# Optimize a trajectory through obstacle constraints

Path smoothing chooses among a small set of geometric shortcuts. Trajectory optimization instead adjusts many waypoints together to balance smoothness, length, and feasibility. That flexibility introduces a central danger: an optimizer faithfully minimizes the objective it receives. If obstacle constraints are missing or checked only after convergence, the mathematically best smooth curve can be physically impossible.

## Model, derivation, and conventions

The decision variable is a sequence of thirty-one two-dimensional positions from a fixed start to a fixed goal. The smoothness term uses second finite differences, `q_(i-1)-2q_i+q_(i+1)`, which approximate curvature or acceleration under uniform time spacing. A smaller length regularizer penalizes squared first differences. The two endpoint rows never move.

A circular obstacle at the centre of the direct route is expanded by required clearance. For each interior waypoint, a squared hinge penalty activates when distance is smaller than the safety radius. Gradient descent uses deterministic backtracking: propose a step, reduce step size until the objective does not increase, and keep endpoints fixed. After each accepted proposal, a feasibility projection checks complete segments and moves offending interior endpoints outward. The final audit reports the exact closest-point segment margin, not only waypoint distance.

The objective is dimensionless in this pedagogical implementation because weights normalize unlike terms. Geometry and reported margins remain metres. This distinction prevents the common claim that an arbitrary weighted sum has physical energy units.

## Predict before running

Predict the unconstrained solution first. Fixed endpoints plus curvature and length penalties favor the straight line. That line crosses the obstacle, so smoothness reduction alone cannot certify a route. With constraints active, expect a longer arc whose segment margins are nonnegative. Increasing required clearance should expand the forbidden disk and lengthen the feasible route. Changing smoothness weight should change the compromise within the feasible set but must not permit penetration.

## Baseline workflow

Run with `0.35 m` required clearance and smoothness weight eighteen. In the response plot, compare the optimized trajectory with the expanded boundary, not the smaller physical obstacle. The curve should remain on one side because the initial trajectory selects that homotopy. Gradient descent is local; it does not search both “above” and “below” classes.

The mechanism plot shows objective value over 1,200 bounded iterations. It should never increase under accepted backtracking steps. A flat tail indicates local convergence or a step limited by feasibility projection. Read this together with minimum constraint margin and violated-segment count. A small objective is useful only when the count is zero.

The path-length metric uses ordinary segment lengths rather than the internal squared-length regularizer. Keeping review metrics separate from optimization terms avoids presenting a tuning-dependent objective as a physical distance.

## Two one-variable sweeps

First increase only required clearance from `0.35 m` to `0.8 m`. The expanded boundary grows while endpoints and optimizer settings remain fixed. Expect a longer trajectory. The signed margin is measured relative to the new boundary, so its numeric value need not grow with the requested clearance; it reports extra margin beyond the request.

For the second sweep, restore clearance and reduce only smoothness weight from eighteen to three. Length regularization then has more relative influence, while obstacle feasibility remains hard-projected. The exact trajectory and length should change slightly, but segment violations must remain zero. This sweep demonstrates that tuning changes quality inside the admissible set, not the definition of admissibility.

## Intentionally broken case

Broken mode removes both obstacle penalty and feasibility projection and initializes the unconstrained minimizer. It returns the direct ten-metre line with ten colliding segment intervals near the obstacle. Objective convergence is excellent because the optimizer was asked to do precisely the wrong job.

This failure separates numerical optimization from engineering validation. A solver success flag means its specified problem was solved; it does not mean the specified problem contained every safety constraint. Post-solve auditing against independently expressed geometry is therefore part of the module, not an optional visualization.

## Recovery

Recovery has three layers. Put signed-distance violation into the objective so descent feels the obstacle before collision. Project proposed trajectories back into the feasible region when a segment still penetrates. Finally, compute exact segment margins after optimization and reject any remaining violation.

Keep endpoints immutable throughout. In a larger system, also constrain velocity, acceleration, curvature, actuator effort, and time. Use a trust region or sequential convexification when linearized constraints are valid only locally, and carry solver termination, residuals, and constraint margins into the plan contract consumed by control.

## Alternative and limiting cases

CHOMP uses a functional gradient and a geometry-aware smoothness metric; STOMP estimates updates through noisy trajectory samples; sequential quadratic programming and sequential convex programming solve local approximations with explicit constraints. The compact projected descent here exposes their shared concern without claiming equivalence.

With no obstacle, the straight line is both shortest and zero-curvature. With obstacle weight zero but projection active, feasibility can survive while convergence becomes inefficient and boundary-chattering may occur. With projection absent but a finite penalty, some residual penetration can be optimal because a soft constraint trades violation against smoothness. As clearance grows until no route exists in the workspace, a correct optimizer must report infeasibility rather than push through geometry.

## Independent evidence and MATLAB-style design boundary

The independent reference rebuilds finite-difference objectives, gradients, backtracking, segment projection, and final clearance from the scenario inputs. It neither imports the experiment nor perturbs its outputs. Baseline, clearance, smoothness, broken, and recovery cases retain exact physical signatures.

The algorithm uses deterministic Python/NumPy and stays within a bounded local iteration budget. MATLAB or an optimization toolbox could solve a related problem, but no MATLAB runtime comparison was performed. There is no claim about nonconvex global optimality, browser accessibility, learner outcomes, real robot dimensions, tracking error, dynamic obstacles, HIL, safety certification, or deployment.

## Engineering review checklist

- State every decision variable, fixed endpoint, frame, and unit.
- Distinguish physical metrics from normalized objective terms.
- Evaluate obstacle clearance over segments, not waypoints alone.
- Verify accepted objective values are nonincreasing.
- Record feasibility residuals independently of solver status.
- Preserve the selected homotopy or search alternatives explicitly.
- Bound iteration count and handle infeasibility without fabricated paths.

## Common mistakes

Common errors include checking only waypoints, assuming a large penalty is a hard constraint, moving endpoints during smoothing, reporting squared segment sum as path length, and treating local convergence as global optimality. A particularly subtle sign error makes the obstacle gradient pull points inward. Plotting can hide that bug if the displayed circle omits required clearance. Another mistake increases clearance but leaves the collision audit tied to the physical radius.

## Focused check and teach-back

Explain why the second finite difference penalizes bending and why the zero-clearance unconstrained optimum is a line. Then describe the difference between a soft hinge penalty and feasibility projection. Your teach-back should include the final independent segment audit and should explain why the broken solver can have a lower objective, shorter trajectory, and worse engineering outcome.
