# Coordinate multiple robots with assurance boundaries

Two robots can each hold a collision-free geometric path and still collide because they occupy a shared place at the same time. Multi-robot coordination therefore plans in space-time, not space alone. This laboratory gives robot A a fixed reserved route and plans robot B through a bounded time-expanded grid. Vertex reservations, opposing-edge checks, and a selectable temporal buffer create an explicit assurance boundary that independent shortest paths lack.

## Model, derivation, and conventions

The workspace is a five-by-five grid measured in cells. Robot A moves horizontally through the centre. Robot B starts below the centre and must move upward. A time-expanded state is `(p,t)`, and each transition either waits or moves one cardinal cell during one discrete step. Robot A remains at its goal after its listed route ends so late plans cannot pass through an unmodelled disappearing robot.

For buffer `b`, robot A's vertex at source time `tau` reserves the same cell for candidate times satisfying `|tau-t|<=b`. Robot B may not enter any reserved vertex. It also may not traverse an edge while robot A traverses the reverse edge during the same step. A bounded A-star search minimizes arrival time with Manhattan distance as an admissible heuristic. The final independent audit extends both trajectories to the shared horizon and counts vertex and opposing-edge conflicts.

## Predict before running

With independent shortest paths and no release delay, both robots reach the central cell on step two. Predict one vertex conflict and zero minimum separation. Nominal planning with a one-step temporal buffer should make robot B wait or detour until the centre reservation clears. Its makespan will increase, but conflicts should be zero and synchronized separation positive.

Removing only the temporal buffer still forbids simultaneous vertex occupancy and edge swaps, so the schedule may be shorter while remaining conflict-free. Adding only a two-step release delay changes relative timing before space-time search. The planner must still audit the full synchronized trajectory rather than assuming delay alone guarantees safety.

## Baseline workflow

Run with buffer one and no release delay. The route plot shows both geometric paths, which still cross at the centre. Geometry alone does not display the safe timing decision, so use the separation plot to inspect synchronized execution. Confirm that the curve never reaches zero and that the conflict metric is zero.

The makespan metric reports the last occupied time step, including waits. It is deliberately not path length: a wait has zero spatial length but nonzero scheduling cost. The minimum separation uses Euclidean cell distance at matching time indices. A positive value proves absence of same-cell occupancy for this discrete point model, not clearance for finite robot footprints.

## Two one-variable sweeps

For sweep one, reduce only reservation buffer from one step to zero. Vertex and opposing-edge exclusions remain active. Robot B can use a cell immediately after robot A leaves it, so makespan may fall. This isolates the cost of temporal conservatism. It does not disable coordination.

For sweep two, restore buffer one and increase only robot B's release delay to two steps. The search prefix holds B at its start while A advances. Depending on remaining reservations, the later launch can reduce or redistribute waits. The comparison shows that release scheduling and path reservation are related but distinct mechanisms; a delayed robot still needs conflict checks.

## Intentionally broken case

Broken mode plans robot B independently as the vertical shortest route. Both lists of grid cells look valid when viewed separately. At time two, however, A and B occupy `(2,2)` simultaneously. The conflict audit counts the violation and the minimum-separation metric reaches zero. No numerical instability or random seed is involved.

A related failure is an edge swap: robots exchange adjacent cells in one step without ever sharing a sampled vertex. Checking only vertex equality misses that continuous-time collision. The nominal reservation function therefore rejects opposing edges. Systems that sample coarsely must also consider longer moves and finite bodies, because vertex and edge rules inherit the discretization assumptions.

## Recovery

Recover by publishing a time-indexed reservation for the higher-priority route, extending terminal occupancy, and searching the next robot in space-time. Apply the declared temporal buffer consistently, reject vertex and edge conflicts, and audit the returned joint schedule. If no path exists within the time horizon, report coordination failure or revise priorities rather than deleting reservations silently.

Operational fleets also need clock synchronization, communication timeout handling, localization uncertainty, footprint inflation, deadlock resolution, and reservation ownership. A robot that loses connectivity should transition to a documented safe behavior. Centralized planning is not itself an assurance case; the executed trajectories and monitor boundaries must match the plan.

## Alternative and limiting cases

Prioritized planning scales by planning robots sequentially but is incomplete because priority order can block a solution. Conflict-Based Search detects conflicts between independently optimal paths and branches on constraints, often yielding optimal discrete solutions. Windowed hierarchical cooperative A-star limits the reservation horizon. Reciprocal velocity obstacles coordinate continuous velocities locally. Mixed-integer formulations can optimize schedules with richer constraints at greater computation cost.

With spatially disjoint routes, independent planning already yields zero conflicts. With zero buffer, exact synchronous vertex and edge checks still provide discrete collision avoidance. Very large buffers can make the bounded problem infeasible even when a physically safe schedule exists. If localization uncertainty exceeds a cell, point-cell reservations are insufficient. If all robots share the same goal, terminal occupancy requires explicit sequencing or goal-capacity rules.

## Independent evidence and MATLAB-style design boundary

The independent reference rebuilds robot A's terminally extended reservation, performs its own bounded time-expanded search for B, and audits vertex, opposing-edge, makespan, and separation evidence. It imports no production experiment, consumes no production result, and perturbs no production value. Baseline, buffer, delay, independent-planning failure, and recovery signatures are retained separately.

This laboratory does not execute MATLAB, ROS traffic management, radios, distributed clocks, browser accessibility validation, learner trials, physical HIL, or multiple robots. It does not characterize localization, braking, latency, packet loss, deadlock frequency, or human interaction. The evidence boundary is deterministic grid software only.

## Engineering review checklist

- Plan and validate trajectories in a shared clock and coordinate frame.
- Reserve terminal occupancy instead of letting a finished robot disappear.
- Check both same-time vertices and opposing edge traversals.
- State the temporal and spatial inflation represented by each reservation.
- Bound search horizon, wait count, and coordination computation.
- Audit the joint schedule after planning each individual route.
- Define behavior for lost communication, stale reservations, and no-path outcomes.
- Separate discrete conflict freedom from physical safety certification.

## Common mistakes

Typical mistakes compare path polylines without timestamps, check only vertices, or release a goal cell as soon as a path list ends. Others mix time-step durations between robots, apply delay to plotted data but not reservations, or count path length as makespan. A buffer can be applied only backward or only forward by an off-by-one error. Fleet systems also deadlock when every robot waits for a reservation held by another and no priority or recovery policy breaks the cycle.

## Focused check and teach-back

Identify the central vertex conflict in the two independent shortest paths and state its time index. Explain an opposing-edge swap and why vertex-only logic misses it. Then teach back what a one-step temporal buffer reserves and why it increases schedule cost. Distinguish geometric path length, arrival time, and synchronized separation. Finally, describe how the coordinator should respond when its bounded search finds no route and list at least three physical uncertainties that the cell-based software model does not cover.
