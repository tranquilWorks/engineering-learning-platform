# Capstone: navigate and replan with perception

This capstone asks for one coherent mobile-autonomy mission, not five unrelated demonstrations. A perceived obstacle changes the occupancy model, the changed model invalidates a route, replanning produces a collision-free alternative, a moving obstacle constrains execution time, sensor dropout triggers recovery, and deterministic replay retains the decisions. Mission success is the conjunction of those requirements. Reaching the goal while violating any one of them is a failed capstone trace.

## Model, derivation, and conventions

The robot operates on a bounded nine-by-three metre grid from `(0,0)` to `(8,0)`. A range observation marks `(4,0)` occupied. In a full mapper, inverse sensor updates would add log odds `l_i=log(p_i/(1-p_i))`; here the binary thresholded result is the explicit handoff to planning. A-star searches four-connected cells with unit edge cost and Manhattan heuristic, retaining the full updated path.

A dynamic obstacle crosses the route at `x=6 m` with constant vertical speed from `y=-2 m`. Route index supplies nominal crossing time. The local predictive layer delays crossing in one-second increments until synchronized separation is at least `0.85 m`. Range dropout is recoverable through fifty percent; a larger value makes the declared sensor requirement negative. Replay and recovery each contribute their own signed requirement margin.

Five normalized margins represent map validity, dynamic separation, dropout tolerance, replay, and recovery. Success requires every margin nonnegative. The separate `requirements-trace.yaml` names the contributing prerequisite modules and observable evidence.

## Predict before running

Predict that the stale direct route crosses the newly occupied cell. Nominal perception should add that cell, forcing a detour through the upper grid row. The longer route changes arrival time at the dynamic crossing. At the baseline speed, immediate crossing remains too close, so the local layer should wait until the obstacle clears the safety radius.

Increasing range dropout alone to forty percent approaches but does not cross the recoverable bound. Increasing obstacle speed alone should let the obstacle clear earlier, reducing or eliminating wait. Broken integration should follow the direct route, omit recovery and replay evidence, and cross the dynamic obstacle without synchronized prediction.

## Baseline workflow

Run with ten-percent range dropout and obstacle speed `0.30 m/s`. In the mission plot, verify that the executed route does not contain the discovered occupied cell. The path should leave the direct row, pass above the obstruction, and return toward the goal. The dynamic crossing marker shows the obstacle's executed position at robot arrival after any wait.

Next inspect all five requirement margins. The map margin proves route validity, dynamic margin proves the `0.85 m` separation, dropout margin proves operation stayed inside the declared recovery envelope, and replay/recovery margins prove those integration mechanisms ran. Confirm mission success one and violation count zero. The minimum-separation metric is independent of the normalized display and retains metres.

## Two one-variable sweeps

For sweep one, change only range dropout from ten to forty percent. Occupancy location, route graph, obstacle motion, safety radius, and replay rules remain fixed. The dropout margin shrinks while map and dynamic requirements remain valid. This is a useful near-boundary case: mission success can remain true without implying generous sensor robustness.

For sweep two, restore dropout and increase only dynamic-obstacle speed from `0.30` to `0.55 m/s`. The obstacle travels farther before the robot reaches `x=6`, so synchronized separation grows and less waiting is needed. Higher obstacle speed is not inherently more dangerous; relative timing determines the encounter. The route still must avoid the perceived static cell.

## Intentionally broken case

Broken mode disables four integration handoffs. The range observation never updates occupancy, so the planner follows a stale route through `(4,0)`. Dynamic prediction freezes the obstacle for decision-making, while the independent executed audit propagates its actual motion and finds unsafe separation. Dropout produces no recovery record, and replay evidence is absent.

The robot may still arrive at the geometric goal. That fact does not override requirement violations. Counting only goal distance would turn a capstone into a single navigation metric and erase perception, timing, monitoring, and systems integration. The cumulative violation count preserves each failure, while the trace identifies which margins fell below zero.

## Recovery

Recover in causal order. First accept the range observation only after frame and timestamp checks. Fuse it into the occupancy state and invalidate every route segment through the newly occupied cell. Search the updated graph and collision-check the replacement. Predict robot and moving-obstacle positions at common times, delay or change motion until separation passes the bound, and execute only the first approved local action.

When dropout occurs, enter the declared recovery path without discarding the valid map update. Retain observations, replans, waits, monitor decisions, and recovery events in source-time order. If any requirement cannot be restored within its bound, stop with mission failure rather than weakening the threshold.

## Alternative and limiting cases

Production navigation systems may use probabilistic occupancy, pose-graph SLAM, D-star or LPA-star incremental repair, lattice or kinodynamic global planning, and model-predictive local avoidance. Behavior trees or mission executives coordinate recovery. This capstone chooses small deterministic counterparts so the complete requirement trace stays inspectable.

If no new obstacle is perceived and the crossing is already clear, the mission reduces to the direct shortest path. If the occupied wall blocks every grid row, replanning must report no route. If dropout exceeds fifty percent, this contract fails even if cached data happens to reach the goal. If the moving obstacle is stationary on the crossing, waiting alone never restores safety and another spatial route or stop decision is required.

## Independent evidence and MATLAB-style design boundary

The independent reference creates its own occupancy set, bounded A-star queue, route audit, crossing-time calculation, wait policy, and five requirement margins. It imports no production experiment, consumes no production result, and perturbs no production value. Baseline, dropout sweep, speed sweep, broken integration, and exact recovery signatures are retained separately.

This is a requirements-traced software capstone, not a physical field trial. No MATLAB navigation stack, range sensor, SLAM system, browser accessibility evaluation, learner validation, physical HIL, braking test, human interaction, safety certification, release, deployment, or production operation was performed.

## Engineering review checklist

- Trace every capstone requirement to named prerequisite mechanisms and evidence.
- Apply perceived map changes before route validity is evaluated.
- Audit every executed segment against the updated occupancy state.
- Compare moving actors at synchronized times with declared body radius.
- Preserve valid state across dropout recovery rather than resetting the world.
- Bound planning, waiting, retry, and replay resources.
- Count goal arrival as success only when every requirement margin passes.
- Retain a deterministic event and decision trace for diagnosis.

## Common mistakes

Common mistakes update the visualization but not the planner's occupancy array, or replan yet continue executing queued commands from the stale route. Static path intersection is sometimes used instead of synchronized separation. A dropout handler may rebuild an empty map and forget the obstacle that caused replanning. Other capstones concatenate prior plots without sharing state or requirements. Finally, a single success flag can hide which constraint failed unless signed margins and trace identifiers are retained.

## Focused check and teach-back

Walk through the baseline causal chain from range observation to map update, route invalidation, replanning, crossing prediction, wait, recovery, and replay. Name the prerequisite modules traced by each requirement. Explain why a goal-reaching broken route still fails. Then predict the effect of faster obstacle motion using synchronized time rather than intuition. State what the mission should do if every updated path is blocked or dropout exceeds its bound, and identify the evidence still missing before physical deployment.
