# Plan dynamically feasible kinodynamic motion

A geometric planner answers where the robot can go. A kinodynamic planner must also answer whether the plant can execute the motion under velocity and acceleration limits. The difference is visible even on a straight, obstacle-free track. A line from start to goal is geometrically perfect, yet commanding full speed at the first sample and zero speed at the last demands impulses that no finite actuator can provide.

## Model, derivation, and conventions

The laboratory uses a one-dimensional double integrator with state `(x,v)`, acceleration input `a`, and a `0.5 s` step. Each state-lattice edge applies one of three actions: negative limit, zero, or positive limit. The exact constant-acceleration update is

`x_next=x+v Delta t+0.5 a Delta t^2`, and `v_next=v+a Delta t`.

Edges that create negative velocity, exceed the speed limit, leave the track, or overshoot the goal tolerance are rejected. A* searches position–velocity states, not position alone. Edge cost is elapsed time, and a distance divided by maximum speed provides an optimistic heuristic. The goal requires position within tolerance and speed equal to zero. Parent records retain both predecessor state and applied acceleration so the trajectory can be reconstructed.

The displayed position and speed are SI quantities. Acceleration violation is `max(peak_abs_acceleration-a_max,0)`. Terminal-speed error is absolute terminal velocity, making the dynamic contract explicit.

## Predict before running

Predict a bang–coast–brake pattern: acceleration raises speed, zero input may hold the ceiling, and negative acceleration reaches rest at the goal. Increasing acceleration limit should reduce arrival time. Reducing speed limit should increase time once cruising becomes active. A higher speed ceiling may have no effect when distance is too short for the acceleration-limited trajectory to reach it. Broken geometric timing should appear faster while reporting positive acceleration and terminal-speed violations.

## Baseline workflow

Run with `1 m/s^2` acceleration and `2 m/s` speed limits. The position trace must begin at zero, increase monotonically, and end at eight metres. The velocity trace starts and ends at zero and never rises above the speed-limit line. Arrival time is the accumulated lattice-edge duration.

Check both violation metrics. Zero acceleration violation proves every reconstructed action stayed within the selected limit; zero terminal-speed error proves the goal is reached at rest. The plot alone can miss a half-sample violation, so these values are computed directly from state/action history.

The observation reports how many states were settled. This is diagnostic bounded-search work, not a teaching objective. A faster search that omits velocity is solving a weaker problem.

## Two one-variable sweeps

First increase only acceleration limit from `1` to `2 m/s^2`, keeping the `2 m/s` speed ceiling. Faster acceleration and braking reduce time spent away from the ceiling, so arrival should improve while both violations remain zero. The velocity slopes change because they are acceleration.

For the second sweep, restore acceleration to `1 m/s^2` and reduce only speed limit to `1 m/s`. The planner must spend more time cruising and arrives later. This case contrasts with raising the ceiling to a value the short maneuver never reaches, a limiting situation in which the output remains acceleration-dominated.

Both sweeps reuse the same target, time step, action alphabet, heuristic structure, and terminal tolerance. That makes their causal interpretation clean.

## Intentionally broken case

Broken mode divides distance by speed limit to obtain a four-second geometric traversal. It inserts a half-second start interval that jumps from rest to `2 m/s`, holds speed, and then commands rest. The implied acceleration magnitude is `4 m/s^2`, exceeding the selected limit by three. It also reports terminal-speed error because the geometric timing has no dynamically planned braking state.

Nothing about the position line reveals the complete failure. It reaches the correct coordinate earlier than the feasible plan. This is why feeding an un-timed geometric path directly to an actuator can saturate, lag, overshoot, or violate safety separation.

## Recovery

Recover by including every dynamic variable needed for transition feasibility in the search state. Generate successors with the plant equation, reject limit violations before queue insertion, and define the goal in full state space. Reconstruct actions along with positions and verify them after search.

For a physical platform, state should include dimensions relevant to nonholonomic motion, steering, attitude, or actuator lag. Discretization must be fine enough to represent a useful solution, yet bounded enough for timing. A controller can track the resulting state trajectory, but it should not be expected to repair a plan that is dynamically impossible.

## Alternative and limiting cases

State lattices use precomputed dynamically feasible motion primitives and are common for cars and aerial vehicles. Kinodynamic RRT propagates sampled controls rather than enumerating a regular lattice. Direct collocation and trajectory optimization treat states and controls as decision variables. Each approach trades resolution, optimality, and computation differently.

As acceleration becomes unbounded, travel time approaches geometric distance divided by speed limit, with instantaneous velocity changes. As speed limit becomes very high over a short track, acceleration and braking dominate, so raising the ceiling no longer helps. If terminal velocity is unconstrained, the planner can cross the goal quickly but hand the controller an unsafe stopping problem. If the time step is too coarse, a feasible continuous solution may be absent from the lattice.

## Independent evidence and MATLAB-style design boundary

The independent reference performs a separate state-lattice search from scenario inputs and separately constructs the broken geometric timing. It retains arrival, acceleration violation, and terminal error for five scenarios without importing production code or reading its result.

No MATLAB runtime or toolbox planner was executed. This deterministic one-dimensional model does not validate motor torque, friction, multidimensional obstacles, nonholonomic steering, browser accessibility, learner effectiveness, real-time performance, HIL, physical hardware, certification, or deployment.

## Engineering review checklist

- Include velocity and every other transition-relevant state component.
- Integrate position and velocity with one consistent action convention.
- Reject speed and acceleration violations before accepting an edge.
- Require terminal position and velocity, not position alone.
- Keep heuristic optimistic relative to elapsed-time cost.
- Bound the state lattice and report no-solution honestly.
- Replay reconstructed actions through the same dynamics.

## Common mistakes

Frequent mistakes plan only position, clip velocity after transition, ignore braking distance, accept a goal crossing with nonzero velocity, or use a heuristic that overestimates remaining time and breaks optimality. Rounding states inconsistently can create duplicate near-identical nodes or erase valid transitions. Another error calculates acceleration from widely spaced plotted samples, hiding instantaneous command jumps at the first and last control updates.

## Focused check and teach-back

Starting from rest, compute the first successor under `1 m/s^2` for `0.5 s`: give its position and velocity. Then explain why the goal includes velocity and why eight metres divided by `2 m/s` is not an executable four-second plan. Finish by identifying the limiting regime in which increasing speed ceiling no longer changes arrival time.
