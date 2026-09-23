# Avoid dynamic obstacles with local predictive control

Static collision checking asks whether two shapes overlap at a configuration. Dynamic avoidance asks whether robot and obstacle will occupy unsafe relative positions at the same future time. A purely reactive controller can discover a crossing too late: current separation is large, yet bounded acceleration means the robot must begin moving sideways before the obstacle reaches the path. This laboratory implements a compact receding-horizon controller to make that timing visible.

## Model, derivation, and conventions

The robot moves forward at `1.25 m/s` while controlling lateral acceleration from a finite set. Lateral speed integrates acceleration and is saturated. A circular obstacle crosses at fixed `x=5 m` with selectable upward speed. Both states advance in `0.2 s` samples.

At every control step, each candidate constant lateral acceleration is rolled forward across the selected horizon. The robot prediction uses its current lateral speed, acceleration, and saturation. The obstacle prediction is constant velocity: `p_o(k+j|k)=p_o(k)+j Delta t v_o`. Candidate cost includes cross-track displacement, lateral speed, control effort, and a large penalty plus fixed surcharge whenever predicted separation enters the `0.9 m` safety radius.

Only the first action of the best candidate is executed. The next observation initializes a new optimization, which is the receding-horizon principle. Minimum separation and violation count are computed from executed robot and obstacle positions, not optimistic predictions. The path-length metric integrates executed two-dimensional motion.

## Predict before running

Predict that a sufficiently long horizon sees the future crossing while current separation is still large. It should begin a lateral maneuver, maintain at least the safety radius, and later return toward the centreline because cross-track cost remains active. A faster obstacle may cross before the robot arrives and require less deviation. A short but nontrivial horizon may still succeed with a longer path. Broken one-step frozen prediction should react late and accumulate violation samples.

## Baseline workflow

Run with fifteen prediction steps and obstacle speed `0.55 m/s`. The horizon spans three seconds. In the response plot, the robot progresses left to right while the obstacle rises vertically. The curves may cross geometrically in the plane at different times; safety is determined by synchronized samples, not by static path intersection alone.

The mechanism plot therefore uses elapsed time and actual Euclidean separation. The separation curve must remain above the `0.9 m` threshold in the baseline, and safety-violation steps must be zero. Minimum separation is the tightest executed margin. Path length exceeds the ten-metre forward distance when lateral avoidance is needed.

Check that the controller remains bounded: forty control updates, five action candidates, and a finite horizon. The lesson is an auditable local decision model, not an unbounded nonlinear solver.

## Two one-variable sweeps

First reduce only prediction horizon from fifteen to five steps, giving one second of lookahead. The obstacle model, action limits, costs, and speed remain fixed. In this scenario the controller can still preserve the threshold, but it may choose a different lateral sequence and a longer executed route. This shows that “shorter horizon” does not mechanically mean “collision”; it reduces anticipation margin and changes behavior.

For the second sweep, restore fifteen steps and increase only obstacle speed to `1.0 m/s`. The obstacle clears the crossing earlier relative to robot arrival, so the optimal response may remain near the centreline. Minimum separation can increase and path length can approach the straight ten metres. Dynamic planning depends on relative timing, not obstacle speed in isolation.

## Intentionally broken case

Broken mode forces a one-step horizon and freezes the obstacle during prediction. At early times the obstacle is below the route and the next robot sample is far from it, so zero lateral action looks inexpensive. When current geometry finally appears dangerous, the lateral acceleration and speed limits prevent an instantaneous escape. Executed separation falls below the safety radius for multiple samples.

This combines two named assumption failures that often travel together in reactive code: insufficient horizon and a static-world prediction. The controller still evaluates a cost and selects bounded actions, so unit tests that check only output type or saturation would pass. The temporal separation audit detects the real defect.

## Recovery

Recover by propagating both participants over a horizon longer than the maneuver lead time. Evaluate safety at every future sample, choose among bounded actions, execute only the first, and replan after the next observation. Retain an independent executed-separation monitor because prediction can be wrong.

Operational systems also need uncertainty tubes, obstacle intent models, emergency braking or safe-stop fallback, latency compensation, and a rule for infeasible horizons. If all candidates violate safety, minimizing penalty is not authorization to continue silently; the planner must raise the condition to a safety supervisor.

## Alternative and limiting cases

Velocity Obstacles and Reciprocal Velocity Obstacles reason directly about collision cones in velocity space. Dynamic Window methods sample reachable velocities over a short horizon. Nonlinear MPC optimizes a sequence of controls with explicit dynamics and constraints. This module uses a small constant-action shooting set so every candidate can be inspected; it does not claim optimal equivalence to those methods.

When obstacle speed is zero, constant-velocity prediction equals a frozen model, so that part of the broken assumption disappears. When lateral acceleration is unbounded, a reactive horizon can evade unrealistically late. When horizon covers the entire encounter and prediction is exact, the controller has the information needed for anticipation, though finite candidate actions can still be conservative. A very long horizon can also distort behavior if model uncertainty grows without bound.

## Independent evidence and MATLAB-style design boundary

The independent reference separately propagates robot and obstacle candidates, applies the same stated action bounds and cost terms, and audits synchronized executed separation. It retains baseline, horizon, obstacle-speed, broken, and recovery signatures without importing the production experiment or altering its results.

This is deterministic Python evidence only. No MATLAB MPC implementation was executed. The model does not validate perception latency, track uncertainty, human motion, multi-agent reciprocity, browser accessibility, learner performance, physical braking, HIL, certification, release, or production deployment.

## Engineering review checklist

- Use synchronized robot and obstacle predictions in one frame and clock.
- Keep action and lateral-speed bounds inside every rollout.
- Evaluate separation at every horizon step, not only the endpoint.
- Execute one action and replan from the next observation.
- Audit actual separation independently of predicted cost.
- Define explicit behavior when every candidate is unsafe.
- Bound candidate count, horizon, and computation time.

## Common mistakes

Common errors freeze a moving obstacle, compare paths without time, check only terminal separation, optimize an unbounded acceleration, or use predicted rather than executed distance as evidence. Another subtle mistake advances the obstacle before the robot in one code path and after it in another, creating a one-sample timing bias. A controller may also dodge correctly but never return toward its route if cross-track or goal terms are absent.

## Focused check and teach-back

Convert fifteen `0.2 s` samples into horizon duration. Explain why two planar curves can intersect while the synchronized actors remain safe, or remain disjoint while finite-radius bodies collide. Then teach back the one-step frozen failure as a lead-time problem: identify what the controller knows, what it assumes, and why bounded lateral acceleration makes late detection unrecoverable.
