# From map evidence to an executed trajectory

The original capstone demonstrates source ordering, map changes, graph replanning and continuous separation along ideal line segments. This additional study connects a probabilistic occupancy update to a planned route, a state estimator and a physical tracking model. Both studies are retained because they isolate different assumptions. They are not one shared simulator, and success in either cannot establish hardware navigation performance.

## Observation and map

A synthetic sensor supplies position observations at 5 Hz with deterministic perturbation `0.015[sin(0.7k), cos(0.9k)]` metres. A known-associated range landmark reports occupancy of cell (4, 0) when the robot is within 4.1 m. Starting from prior odds 1, each positive observation adds `log(3)` to log odds, capped at 6. A probability threshold 0.7 triggers a graph replan. Because `log(3) > log(0.7/0.3)`, the first positive observation suffices in this constructed scene. This is evidence accumulation for one cell, not scan matching, a dense map or SLAM. The robot's position estimate comes from the separate position observations, not from jointly estimating this landmark.

Broken mode suppresses occupancy updates, so the route remains straight through the occupied cell. Its eventual arrival at the goal is deliberately insufficient: compare arrival with minimum clearance. A requirement that counts goal arrival alone would accept a collision.

## Estimation and covariance

The state is `[x, y, vx, vy]` in metres and metres per second. Each 0.1 s tick applies the constant-acceleration transition `p_next = p + v dt + 0.5 u dt²`, `v_next = v + u dt`. The Kalman filter uses the same transition and actual applied acceleration, process covariance `10⁻⁵ I`, position measurement covariance `0.0025 I`, and initial covariance `0.04 I`. The diagonal entries therefore have the squared units of their respective state components; the identity notation does not make position and velocity interchangeable.

Prediction propagates both mean and covariance. Measurement correction uses the innovation covariance and a Joseph covariance update, preserving symmetry and positive definiteness within floating-point accuracy. The independent check reconstructs each update in information form from the synthetic measurement model, checks every state and covariance, and verifies positive covariance eigenvalues. Small estimation error here reflects a known plant, direct position measurements and deterministic disturbances. It is not empirical consistency or a validated localization sensor model.

## Planning, tracking and braking

A bounded grid planner routes around the occupied cell. The controller tracks successive waypoints using estimated position and velocity. Desired speed is limited to 0.8 m/s and also reduced by a stopping-distance expression near a waypoint. Each acceleration component is limited to ±1 m/s². Actual velocity evolves under the plant; it never jumps instantly to a desired velocity or to zero during hold.

Missing observations begin at candidate range frame seven. The dropout control removes a fraction of a fixed 125-frame schedule; it does not remove that percentage of an arbitrarily long executed mission. Source age above 0.4 s requests zero desired velocity. The actual robot then brakes with bounded acceleration. Fresh observations restore tracking and leave an event record. The map and covariance remain available during the gap, and covariance continues to propagate.

The moving obstacle follows `(6, −2 + speed × t)` metres. A short-horizon separation check can also request braking. It is a heuristic supervisor, not a proof of collision avoidance. In some selected speeds the obstacle has already crossed before the robot reaches its x coordinate; changing its speed can then leave the tracking path unchanged. Use the clearance trace and crossing time to identify this inactive regime rather than requiring an artificial response to every control change.

## Continuous clearance and completion

Between ticks, relative position is quadratic: `r(τ)=r₀+v_rel τ+0.5u τ²`. Minimum separation is evaluated at both endpoints and every real root of the derivative of squared distance within the interval. The derivative is cubic; checking endpoints alone can miss an interior collision. An independent dense-time check bounds the polynomial minimum, while exact state-transition checks verify the acceleration integration.

The goal test requires actual position error below 0.1 m and actual speed below 0.1 m/s. Clearance remains a separate requirement. Report goal error, estimation RMSE, continuous clearance and hold/resume times together. Baseline healthy navigation detours around the static cell and resumes after the observation gap; broken navigation can reach the goal while crossing the static obstacle. A point-robot clearance is not vehicle-footprint clearance, and this model omits wheel slip, heading constraints, sensor extrinsic uncertainty, map association ambiguity and actuator delay.

Predict the stop interval for baseline dropout, then increase dropout alone and compare covariance growth, braking and resume time. Restore baseline and sweep moving-obstacle speed; explain whether the crossing actually intersects the robot's arrival interval. Finally enable the named failure and identify the first missing map update, the changed route and the violated clearance requirement. Restore healthy mode and verify deterministic recovery of all four stages, retaining actual state and event evidence for the mobile portfolio.
