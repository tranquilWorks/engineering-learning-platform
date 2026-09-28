# Twelve-lesson semantic revision specification

This is a scoped next-batch design, not implementation evidence. The delivery
batch preserves all course payloads. Existing lesson identities, source pins,
prerequisite graphs and native inventory remain unchanged.

| Lessons | Demonstrated gap | Required executable repair and independent check |
| --- | --- | --- |
| Controls P66 | Algebraic tracking/NEES stand in for identification, control and estimation | Identify a bounded discrete plant from a deterministic excitation record; derive feedback from the identified model; execute a noisy estimator/closed loop with actuator bounds and stress cases. Compute tracking, estimation consistency and effort from histories. Compare separate scalar recurrences/normal-equation oracles plus model-recovery and zero-noise limits. |
| Controls P67 | Survey error/alarm surrogates without vehicle navigation | Execute planar motion, inertial prediction, GNSS dropout, waypoint guidance, turn saturation and monitor recovery. Measure cross-track/turn violations from the trajectory and timestamped monitor trace. Check dead-reckoning, heading/position geometry and dropout recovery independently. |
| Controls P68 | Latency/drop fractions without an actual timed control interface | Schedule source/arrival events, drops and stale packets; feed accepted commands to a bounded plant through an age-based fail-zero watchdog. Derive deadlines and safe-command verdicts from event histories. Compare independent event reconstruction and a zero-delay closed-loop limit. Physical HIL remains excluded. |
| Robotics P68 | Fixed replay and dropout-recovery margins | Feed deterministic timed range observations into occupancy and planner decisions; apply source-time ordering and a stale-sensor safe stop; resume only on a fresh validated observation. Compute replay and recovery margins from the event trace, retain route and dynamic-obstacle separation checks, and independently reconstruct ordering/recovery. |
| Robotics P69 | Fixed interface recovery flag | Couple timestamped command delivery and watchdog recovery to the existing calibrated kinematic/contact/passivity chain. Measure freshness, fail-zero response and post-fault force recovery; independently replay delayed commands and check energy/force recurrences. |
| Vehicle P61 | Dimensional signature metadata and generic limits | Preserve the executed closed-geometry model; correct m, 1/m, degree and radian quantities, derive the circular/elliptical limits and sample convergence, and cross-check curvature closure independently. |
| Vehicle P62 | Dimensional signature metadata and generic limits | Audit the speed-dependent tire/aero/power envelope against force balance and zero-speed/limiting-speed cases; correct signature units and evidence. |
| Vehicle P63 | Dimensional metadata and weak performance interpretation | State the bounded offset-family approximation, integrate travel time over arc length consistently, test corridor feasibility and zero-width behavior, and compare an independent candidate evaluation. |
| Vehicle P64 | Energy budget only caps a reported value; artificial failure residual | Execute curvature-limited forward/backward reachability with power, drag and combined grip; couple a finite energy budget into the speed solution. Derive braking and energy residuals directly from physics, including broken forward-only mode. Independently solve the constrained reachability/energy problem and zero-budget limit. |
| Vehicle P65 | Dimensional metadata and generic limits | Preserve the legitimate synthetic factorial design while clearly distinguishing its response surface from measured car performance. Correct effect/time/rank units, demonstrate rank loss and interaction aliasing, evaluate the held-out metric at genuinely unused design points (the old metric reuses a fitted corner), and retain an independent coefficient solution. |
| Vehicle P66 | Hardcoded telemetry subsystem pass flags | Execute synthetic provenance-bearing replay, clock alignment, sensor calibration, trajectory/state reconstruction, chronological parameter fitting, held-out residuals, identifiability/covariance and corrupt-record diagnosis. Every requirement references computed evidence. Independently assess decoded/calibrated records, fitted parameters and held-out predictions. |
| Vehicle P67 | Linear lap surrogate and hardcoded subsystem verdicts | Execute a bounded calibrated tire/chassis/propulsion/brake/aero/track/line/lap chain, propagate uncertainty and compare setups. Requirements use derived force/energy/geometry/validation residuals. Independent calculations must cover the cumulative chain and its named double-counted-aero failure, not reproduce arbitrary pass flags. |

For each changed lesson retain a concrete prediction, meaningful controls and
units, explanation of every plotted quantity, worked dimensional example,
lesson-specific limiting cases, two sweeps, a named failure, recovery, focused
questions with answer rationale and cumulative assessment trace where relevant.
Update five independent scenarios and their origin/formulation metadata without
importing or consuming production output. Preserve independent reference
behavior for every unaffected lesson; add tests that detect the specific
surrogate/fixed-flag failure rather than merely accepting new snapshots.

Validation includes focused physical invariants and metamorphic changes,
existing expansion/course/schema suites, all mandatory local gates, actual
browser controls and plots for the twelve lessons on desktop/mobile, and an
updated baked read-only container. Reassess only the repaired lesson scope. The additional 60 findings, including
Vehicle P01–P16 dimensional charts, keep all three course aggregates blocked. Human learning/accessibility, MATLAB, vehicle,
physical HIL and production evidence remain unperformed.

Primary method references for the implementation review:
[MIT system identification](https://underactuated.csail.mit.edu/sysid.html),
[MIT feedback design](https://underactuated.mit.edu/lqr.html), and
[SciPy discrete system routines](https://docs.scipy.org/doc/scipy/reference/signal.html).
These references support methods; they do not validate this implementation.
