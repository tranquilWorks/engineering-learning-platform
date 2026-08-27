# Generate a Feasible Trajectory

**Guiding question:** What inputs, observable effects, and failure modes matter when you generate a Feasible Trajectory?

Generate a rest-to-rest quintic and test speed/acceleration feasibility. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Shortening duration should raise peak acceleration faster than peak speed. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$x=x_f(10s^3-15s^4+6s^5)$$ — The quintic satisfies zero endpoint velocity and acceleration.
- $$s=t/T$$ — Duration scales velocity by 1/T and acceleration by 1/T squared.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `target_position_m` through [5.0, 20.0, 30.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `move_duration_s` through [4.0, 8.0, 14.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case forces the 20 m move into 4 s, exceeding the declared speed/acceleration limits. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and lengthen the move until both constraints pass. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P21 lesson: Generate a Feasible Trajectory

## Guiding question

What inputs, observable effects, and failure modes matter when you generate a Feasible Trajectory?

## Compounds on P20

P20 compared controllers only over a declared uncertainty set and command-effort limit. P21 brings that
boundary-first reasoning into guidance: before asking a controller to follow a reference, test whether the
reference's own kinematic demands fit declared speed and acceleration limits.

## Mental model

Imagine moving a vehicle along one straight axis from rest at zero metres to rest at `xf` metres. A quintic
time law gives position, speed, and acceleration that join smoothly at both ends:

```text
tau = t/T
h(tau)   = 10*tau^3 - 15*tau^4 + 6*tau^5
h'(tau)  = 30*tau^2 - 60*tau^3 + 30*tau^4
h''(tau) = 60*tau - 180*tau^2 + 120*tau^3
```

Position is `xf*h`, speed is `(xf/T)*h'`, and acceleration is `(xf/T^2)*h''`. The shape in normalized time
does not change when duration changes; only its physical time scale and derivative demands change.

## What the exact peaks reveal

- Peak speed occurs halfway through the move and equals `(15/8)*abs(xf)/T`.
- Peak acceleration magnitude occurs at normalized times `(3-sqrt(3))/6` and `(3+sqrt(3))/6`, and equals
  `(10*sqrt(3)/3)*abs(xf)/T^2`.
- Peak jerk magnitude occurs at the endpoints and equals `60*abs(xf)/T^3`.
- The speed constraint requires `T >= (15/8)*abs(xf)/vmax`.
- The acceleration constraint requires `T >= sqrt((10*sqrt(3)/3)*abs(xf)/amax)`.
- The larger duration bound is the active constraint. A zero-distance move has zero demand and no active
  constraint.

These analytic peaks determine feasibility. A plotted sample grid is only a visualization and can miss the
exact acceleration peak between samples.

## Deliberately broken request

Request `20 m` in `4 s` while retaining `5 m/s` and `2 m/s^2` limits. The polynomial remains smooth and
hits both endpoints, but its peak speed is `9.375 m/s` and peak acceleration is about `7.217 m/s^2`.
Smooth is not the same as feasible. A fresh `8 s` call exactly recovers the baseline because the model has
no persistent state or partial plan to roll back.

## Misconceptions to correct directly

- A smooth path is not automatically feasible.
- More plot samples do not reduce the physical speed or acceleration demand.
- Tightening a limit changes the feasibility verdict, not the already chosen polynomial trajectory.
- Doubling duration halves peak speed, quarters peak acceleration, and divides peak jerk by eight.
- Reversing the target changes derivative signs but not absolute utilization.
- Feasible reference generation does not prove closed-loop tracking, collision avoidance, actuator
  feasibility, HIL behavior, or field safety.
- Independent reference arithmetic is not MATLAB-runtime or rendered-UI evidence.

Ask one observation question at a time. Request the teach-back only after executable checks pass.

## Source walkthrough

# P21 walkthrough: Generate a Feasible Trajectory

## Learner sequence

1. Read the guiding question and P20 connection before running code.
2. Predict only whether the `20 m` in `8 s` baseline fits `5 m/s` and `2 m/s^2` limits.
3. Visualize position and speed first. Observe zero endpoint speed and the midpoint peak.
4. Visualize acceleration and constraint bands. Compare analytic peaks, utilization, and minimum duration.
5. Sweep only target distance while duration and both limits remain at baseline. Observe demands grow
   linearly and identify where the active minimum-duration constraint changes.
6. Explain that a longer distance applies the same normalized shape over more metres.
7. Reset distance to `20 m`, then sweep only duration. Observe peak speed scale as `1/T`, acceleration as
   `1/T^2`, and jerk as `1/T^3`.
8. Explain the changed view from the chain rule and time scaling, not from MATLAB plotting mechanics.
9. Run the `4 s` broken request. Identify both violated constraints even though endpoint conditions and
   smoothness remain intact, then restore the `8 s` baseline.
10. Run `run_module_checks("P21")`, answer one interpretation prompt at a time, and give the required
    two-sentence teach-back.

No MATLAB-runtime, rendered-UI, plant-tracking, HIL, or physical evidence is claimed by this walkthrough.

## Source checks

# P21 checks: Generate a Feasible Trajectory

Run `run_module_checks("P21")`, then answer one prompt at a time:

1. Why can a trajectory meet its endpoint position, speed, and acceleration conditions yet still be infeasible?
2. Why does doubling duration divide peak speed by two, peak acceleration by four, and peak jerk by eight?
3. Why must feasibility use analytic peaks rather than only the largest value on a plot grid?
4. What do target position, duration, speed limit, and acceleration limit each change, and which changes the
   polynomial path rather than only its verdict?
5. What additional plant, obstacle, actuator, and feedback evidence would be needed before calling the move
   trackable or safe?

## Teach-back

In exactly two sentences, name the trajectory inputs and the observable time-scaling effects. Then state the
speed/acceleration feasibility rule and explain why the smooth `4 s` request fails.

The source and independent oracle provide static and simulated evidence only. No MATLAB-runtime,
rendered-UI, numerical-fidelity, plant-tracking, bench, HIL, field, or production validation is claimed.
